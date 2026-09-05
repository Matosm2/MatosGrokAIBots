# EV Charge Control & Actuator Verification — 2026-08-19

Companion to `claude/peak-prep-and-overnight-charging.md` (when we buy) and
`claude/energy-battery-architecture.md` (who supplies the house). This one covers **stopping the
cars**, and the failure mode that made stopping them silently impossible for 32 hours.

## The 2026-08-19 incident

18:34, PEAK band (43.20 c€/kWh). Ursina began charging at 3.4 kW — essentially all grid.
Noticed by hand at ~18:44. Cost ≈ 0.8 kWh ≈ €0.35.

`automation.tesla_default_off_gatekeeper_ursina` **worked perfectly and did nothing**. It fired on
`charging_started` and on every `/5` poll. Every run passed all five conditions. Every run executed
`switch.turn_off` on `switch.ursina_charge`. Traces read `script_execution: finished`, no error.

`switch.ursina_charge` had been **`unavailable` since 2026-08-18 10:07**, because the `tesla_fleet`
config entry was in `setup_error`. **`switch.turn_off` against an unavailable entity is a silent
no-op** — HA logs a WARNING (`Referenced entities … are missing or not currently available`) and
nothing else. Nothing in the automation, the trace, or the system log distinguished a stop that
worked from a command that went nowhere.

### The failure family

Identical shape to the 2026-08-18 battery incident: forcible charge issued and accepted
("Charging at 5000W until 48.0%") while `number.utility_room_inverter_maximum_charging_power` sat
latched at 0 W. **Correct decision, dead actuator, nothing verifying effect.** Treat this as a known
class, not two coincidences. Any automation whose whole job is to make something stop or start needs
to check that it did.

### What actually fixed it

`homeassistant.reload_config_entry` on the `tesla_fleet` entry: `setup_error` → `loaded` in ~20 s,
and the next `switch.turn_off` stopped the car first try. Grid import 3653 W → 13 W.

**There is no cross-integration fallback**, and this was tested, not assumed. With Fleet down,
`STOP_CHARGE` to Ursina via `tesla_custom` (`switch.ursina_charger`) raised a `TeslaException`. The
split in the `tesla-integration-conventions` skill is a hard constraint. Recovery must be
reload-and-retry on the car's **own** integration.

## What changed

### Both Default-Off Gatekeepers — verify-and-escalate

The action is no longer a bare `switch.turn_off`. Four stages:

1. **PREFLIGHT** — command entity `unavailable`/`unknown` → reload its config entry, wait ≤ 90 s for
   it to return, *before* issuing anything.
2. **ATTEMPT 1** — `switch.turn_off`.
3. **VERIFY 1** — `wait_for_trigger` on the **car's own** charging sensor going `off`, ≤ 60 s.
   Proof of effect, not proof of dispatch.
4. **ESCALATE** — (Xursina only: press `button.xursina_force_data_update` first, its telemetry goes
   stale) → reload the entry → ATTEMPT 2 → VERIFY 2 (≤ 90 s) → phone alert + persistent notification.

The escalation gate is a **native state condition on the charging sensor**, not `wait.completed`.
That matters: a wait can time out because the car was already stopped, and checking real state
instead of the wait result means no false alarms. Verified live — a synthetic run on a
non-charging Ursina timed out at VERIFY 1 and correctly declined to escalate.

**Verification watches the CAR, never the Wall Connector.** The connector is shared and cannot tell
which car is drawing; connector power would let one car's session mask a failed stop on the other.

Runs block up to ~4 min on the full escalation path. `mode: single` / `max_exceeded: silent` is
therefore load-bearing: `/5` polls are dropped while it runs instead of stacking redundant stop
commands behind a failing integration.

### New: `🔌 EV — Charge Command Path Watchdog`

Catches the dead path at 10:07 on a Tuesday instead of at 18:34 mid-peak.

- Triggers: either command switch `unavailable` **for 15 min**; hourly poll; HA start.
- Per car: reload the owning config entry, wait 2 min, and only then alert.
- **Self-healing first, alert second** — the reload is what fixed it live, and it's free.
- Notification is **gated on `binary_sensor.tesla_wall_connector_vehicle_connected`**: a dead command
  path with no cable in cannot cost anything, and an hourly alert for a condition needing Tesla
  re-auth would train itself to be ignored. The reload attempt itself is ungated.
- Clears its own persistent notification when the path is healthy again.
- Verified live: both cars evaluated, both healthy, 3 ms.

## Why it's inlined and not a shared script

It was first written as `script.ev_stop_charge_verified`, parameterised, called by both gatekeepers —
the maintainable shape, and what the project conventions ask for.

**This Home Assistant has zero script entities.** The `script` integration is not set up. The config
saved into storage, `ha_config_get_script` read it back fine, `script.reload` returned success, and
the entity was never created — the only symptom being a WARNING that the referenced script entity was
missing. The same silent-no-op pattern the change exists to remove, hit while removing it.

So the logic is duplicated across the two gatekeepers. **The two copies must be kept in step**; they
differ only in entity IDs, config entry, and Xursina's extra telemetry-refresh step. One consolation:
with entity IDs hardcoded rather than passed as script fields, every condition is a native `state`
condition and every wait is a native `wait_for_trigger` — no templates in logic positions at all.

If the `script` integration is ever enabled, refactoring this back into one script is the first
cleanup worth doing.

## Reference

| Car | Read telemetry | Command | Config entry |
|---|---|---|---|
| Ursina | `tesla_custom` | `switch.ursina_charge` (`tesla_fleet`) | `01KZA699VHEAKCNYH85EYMY2V1` |
| Xursina | `tesla_custom` | `switch.xursina_charger` (`tesla_custom`) | `a6a2a94bfc7182ea7496c5ea1dc5f26a` |

Notify target across the energy automations: `notify.mobile_app_pixel_10_pro_fold`.

## Still open

- **`tesla_fleet` fell into `setup_error` on its own and stayed there for 32 hours.** The reload
  fixed it this time; the root cause of the entry failing is not established. If it recurs, the
  watchdog will now say so — but a repeated `setup_error` means re-authentication, not a nudge.
- `tesla_custom` is not healthy either: `Timeout fetching tesla_custom data` and `TeslaException`
  traces on 2026-08-19. Xursina's command path is one cloud outage from the same failure.
- **Other actuators are still unverified.** The Peak Prep, Overnight Charge, and Force Grid Charge
  automations all issue Modbus writes without confirming movement. The 2026-08-18 incident was
  exactly that. Worth the same treatment.
