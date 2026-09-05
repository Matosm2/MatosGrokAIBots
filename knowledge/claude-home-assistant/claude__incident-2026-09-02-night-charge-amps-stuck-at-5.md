# Incident 2026-09-02 — Night charge stuck at 5 A

Companion to `claude/ev-charge-control-and-actuator-verification.md` and
`claude/huawei-modbus-unavailability-write-storm.md`. Same family as both: **the decision logic
was fine, the loop that carries it just stopped existing, and nothing noticed.**

## Symptom

Xursina charging normally at 01:40, `number.xursina_charging_amps` latched at 5 (≈3 kW on 3 phases).
`sensor.xursina_time_charge_complete` projected **19:14 the next evening** instead of 07:00.
House batteries visibly oscillating at the same time.

## Timeline (local)

| Time | Event |
|---|---|
| 01:00:00 | `Tesla - Smart Night Charging` time trigger fires. Car **not yet charging** → conditions fail, no loop. |
| 01:01:18 | `binary_sensor.xursina_charging` → `on`. State trigger fires, loop starts. |
| 01:01:34 | Loop iteration 1 sets amps **5 → 17**. Correct. Enters its 10-minute delay. |
| ~01:07:30 | **HA restart / automation reload.** The running loop is killed mid-delay. |
| 01:08:05 | huawei_solar sensors → `unknown`, then back. |
| 01:16:12 | huawei_solar sensors → `unavailable` (Modbus timeouts). |
| 01:20:15 | Sensors recover. `Set Min Amps on Solar Exit` fires twice → amps **17 → 5**. |
| 01:25:10 → 01:26:20 | Same unavailable/recover cycle, fires again. |
| — | Nothing ever re-armed the night loop. Car held 5 A. |

## Root cause 1 — the amp loop cannot survive a restart

`Tesla - Smart Night Charging` keeps its whole control loop inside **one automation run**
(`repeat` + `delay: 10 min`). Its only triggers were `binary_sensor.xursina_charging → on` and
`at: 01:00`. After the 01:07 restart:

- the 01:00 time trigger had already passed, and
- a `to: "on"` state trigger **does not re-fire** for a sensor that is already `on` when HA starts.

So the loop was gone for the night with no error, no trace, no notification. **Any long-running
in-run loop needs an idempotent re-arm trigger** — this is the general lesson, and it applies to
every other loop-shaped automation in this instance.

### Fix

Added two re-arm triggers; `mode: restart` makes them harmless (a re-trigger just recalculates):

```yaml
- trigger: homeassistant
  event: start
  id: ha_start
- trigger: time_pattern
  minutes: "/15"
  id: rearm
```

All four existing conditions (charging on, 01:00–07:00, force-charge off, car home) still gate
every run, so the `/15` pattern is a no-op outside the night window.

## Root cause 2 — `numeric_state` re-fires on Modbus recovery

`Set Min Amps on Solar Exit` triggers on `sensor.inverter_input_power below: 300` and
`sensor.batteries_state_of_capacity below: 95`.

**A `numeric_state` trigger also fires when the entity returns from `unavailable`/`unknown` to a
value that is already below the threshold.** The huawei_solar Modbus link times out and recovers
repeatedly (`Timeout communicating with HV2520094217`), so *every recovery* re-fired both triggers
and re-slammed the car to 5 A — at 01:20 and again at 01:26, in the middle of the night charge.

### Fix

Two conditions added:

```yaml
- condition: not          # night charging owns the amps
  conditions:
    - condition: time
      after: "01:00:00"
      before: "07:00:00"
- condition: template     # ignore unavailable -> value recoveries
  value_template: >
    {{ trigger.from_state is not defined or trigger.from_state is none
       or trigger.from_state.state not in ['unavailable', 'unknown'] }}
```

The template is deliberate and is the one place here where native loses: `numeric_state` has no
`not_from:`. The best-practice checker flags it; the description records why.

**This guard is worth auditing across every other automation triggered by a huawei_solar
`numeric_state`** — the same spurious crossing hits all of them.

## Immediate recovery

`automation.trigger` on `Tesla - Smart Night Charging` → amps 5 → 17, 11.0 kW, ETA back inside the
07:00 target.

## Still open

- **Marstek Venus E is oscillating.** `sensor.utility_room_marstek_venus_e_battery_power` swings
  between ≈ −27 W and ≈ −880 W every 7–14 s, continuously (403 state changes in 40 min), while
  `sensor.utility_room_marstek_venus_e_ac_power` reads 0 and the work mode is `manual`. Venus D is
  flat at −23 W. Not caused by the EV issue and not diagnosed yet. Suspect the manual-mode power
  write being re-issued or the unit hitting a cutoff and restarting.
- **Why did HA restart at 01:07?** Not established. `huawei_solar` took >10 s to set up and
  `bootstrap` logged a 5530 s wait on it.
- **The huawei_solar Modbus link is unhealthy**: repeated batch-update timeouts plus an illegal
  address error on device HV2520094217.
- **No alarm exists for "night charge is not on track."** A cheap one: between 02:00 and 06:00,
  if charging is on, car is home, force-charge off and `minutes_to_full_charge` projects past
  07:00 by more than 30 min, notify. That would have caught this in minutes.
