# Config-Drift Watchdogs — built 2026-08-28

## Incident 2026-08-27/28 — working mode drifted to TOU, battery idled all night

At 12:17:16 on 08-27, right after a Modbus reconnect (unavailable → unknown → maximise → TOU within ~2 min), `select.utility_room_batteries_working_mode` changed to `time_of_use_luna2000` — not by any HA automation (nothing in the stack writes that select except the peak-stop failsafe, which didn't fire). Likely set on the inverter/FusionSolar side.

Consequence: in TOU mode with no real discharge windows the LUNA2000 sits idle. Battery at 99 % SoC, discharge cap wide open at 10 000 W, and the house imported ~1.7 kW at 08:44 next morning. **No existing failsafe covered this** — the peak-stop only catches *charging from grid during 17:00–22:00*; an idle battery outside peak was invisible. Same root class as the 2026-08-04 TOU incident (that one grid-charged at 8 kW off a dummy TOU table).

Marstek non-participation that morning was correct behaviour: fleet at 12–13 % SoC (below the 15 % floor → manual standby) and the P1 meter off the VLAN again since 03:13.

## Guard 1 — `automation.battery_working_mode_watchdog` (🛡️ Working Mode Watchdog)

Intended mode is ALWAYS `maximise_self_consumption`; Force Grid Charge uses `huawei_solar.forcible_charge_soc`, which overrides without changing the mode, so any non-maximise reading is drift. Reverts and notifies.

- Triggers: state `not_to` [maximise, unavailable, unknown] with 5-min hold (rides out Modbus reconnect chatter) + `/30` time-pattern poll (restart-proof backstop — `for:` clocks reset on restart/unavailable).
- Guards: never writes while the select is unavailable/unknown; yields while `input_boolean.battery_force_grid_charge` is on.
- To deliberately run a non-maximise mode, turn the watchdog off first — otherwise it wins within 30 min.

## Guard 2 — stack health check (automations themselves)

- `binary_sensor.battery_control_stack_problem` — template helper, device_class `problem`. Holds the canonical list of the 24 battery-control automations; turns on when any is off, unavailable, or **missing** (registry-disabled entities vanish from the state machine, so it compares `expand(ids) | selectattr('state','eq','on') | count` against `ids | count` — a disappeared automation is a count mismatch).
- `automation.battery_control_stack_health_check` — notifies after the problem sensor holds `on` 10 min, and re-notifies daily at 09:00 while unresolved. **Notify-only by design**: an automation may be off deliberately; auto-re-enabling would undo that.
- ⚠️ The entity list lives in BOTH the template helper and the health-check automation's `variables.stack_ids` — keep them in sync when adding/renaming battery automations. Both new watchdogs are themselves on the list.

## Verified after build

Problem sensor `off`, both automations `on`, mode restored to `maximise_self_consumption`, battery active again (charging −814 W from solar), grid balanced at −2 W.
