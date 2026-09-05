# Incident 2026-08-31 — both Venus units off Modbus for 18 h, in silence

**Status: guards built and verified live. The units themselves are still unreachable — that part is physical.**

Matos found it by noticing the backup ports were dead. Nothing in the 24-automation battery stack had said a word.

## What happened

Both Venus units stopped answering Modbus TCP: **192.168.20.83:502** and **192.168.20.58:502**, connect refused. Venus E at **00:07**, Venus D at **00:11**. Still down at 18:40.

The 17:10 HA restart made it worse: `marstek_modbus` failed setup outright (`Global task timeout: Bootstrap stage 2 timeout` → *Setup of config entry cancelled*), then a retry collided with the half-set-up entry (`Config entry Marstek Venus Modbus for marstek_modbus.sensor has already been setup!`). 90 of 93 Marstek entities went unavailable. A manual `homeassistant.reload_config_entry` cleared the collision.

The P1 meter at .109 stayed `home` throughout, so the IoT VLAN is fine — it is the two units.

Last readings before the drop: **Venus D 14 %** at 22:03 on 08-30 (below the 15 % floor → stood down to Bypass), **Venus E 42.7 %** flapping Standby/Bypass/Discharge. Backup Function last read **on** for both. D at 14 % and falling sits right at the ~12 % reserve edge where the firmware drops the Backup Function — consistent with what Matos saw.

Not the freezer: `switch.shellyext_frezeer` was on and drawing the whole time. Note that `switch.freezer` / `sensor.freezer_power` are the **Office TV** — misnamed, and actively misleading during an incident.

## The four blind spots

Each was defensible alone. Their union still had a hole exactly the shape of "the packs are gone".

1. **`🔌 Marstek Backup — Keep Backup Function On`** triggered on `to: off` and both guards were `state: off`. `unavailable`/`unknown` match neither, so it went silent precisely when the backup ports were least verifiable. Its 15-min poll ran all day and did nothing, exactly as designed.
2. **`🔌 Marstek P1 Meter — Offline Alert`** watches `device_tracker.wlan0_2` — the meter, not the units.
3. **`🔴 Marstek — Delivery Shortfall Failsafe`** needs capability > 1000 W to latch; capability had gone *unavailable*.
4. **`binary_sensor.battery_control_stack_problem`** only checked that the 24 automations were `on`. They all were.

## The expensive part — an availability template disabled two failsafes

`sensor.marstek_discharge_capability` carried `availability: has_value(both SoC sensors)`. With the packs unreadable it went **unavailable** rather than reporting 0, and `sensor.huawei_discharge_cap_target` (whose availability reads `has_value` on it) followed.

- **Branch 4B (MARSTEK IDLE RESCUE)** is gated on `numeric_state below: 1`. `numeric_state` never matches a non-numeric state — the rescue branch was disabled by the very condition it was written for. The `capability_lost` trigger died the same way.
- **Branch 5** read the unavailable target as 0 through `float(0)` in its deadband, cleared the 400 W deadband, and wrote its `int(200)` fallback. **Huawei pinned at 200 W at 17:15:42 with the whole fleet dead**, heading into the 43.20 c€ evening block. Only 5B could recover it, and only after real import.

Also: from 00:07 to 17:10 the integration served **stale** values instead of going unavailable, so capability read 2500 W repeatedly all day while both packs were dead — a third cause in the capability-over-reporting family (after mode-aware 08-13 and meter-aware 08-17).

**General lesson.** An availability template on a sensor that guards a failsafe converts a detectable fault into an invisible one. Where a sensor feeds a safety gate, prefer a state template that computes the *safe value* from missing inputs over an availability template that withholds the state.

## What was built

| Change | Effect |
|---|---|
| `sensor.marstek_discharge_capability` — availability template **removed** | Reports an honest **0** when the packs cannot be read. Restores branch 4B, the `capability_lost` trigger, and the cap target's 10000 W short-circuit. The state template already computed 0 correctly; the availability gate was the only thing hiding it. |
| Discharge Cap Controller **branch 5** | New `numeric_state above: 0` on the cap target — never writes off an unreadable target. Fallback flipped `int(200)` → `int(10000)`. |
| **`automation.marstek_fleet_unreachable_alert_recovery`** (new) | Owns the link fault. 5-min debounce, `not(both on)` so off/unavailable/unknown all count, either unit is a fault. Latches `input_boolean.marstek_fleet_unreachable`, stamps `input_datetime.marstek_fleet_unreachable_since`, **alerts**, then requests a reload and verifies with a native state condition. Reminds every 30 min via `timer.marstek_fleet_renotify` (native idle check, no counter). |
| **`automation.marstek_reload_modbus_entry_worker`** (new) | Absorbs the blocking reload call, triggered by the event `marstek_reload_modbus_requested`. |
| `🔌 Marstek Backup — Keep Backup Function On` | New `switch_unreadable` trigger (unavailable/unknown 10 min) that alerts **only when that unit's own link is up** — otherwise the fleet automation owns it, so one fault gives one message. New `link_back` trigger re-asserts backup within ~2 min of a reconnect (90 s settle, write, then wait for the switch to actually report `on`). |
| `binary_sensor.battery_control_stack_problem` | Second health axis: ORs in the fleet-unreachable latch. Reads the **latch**, not the raw modbus sensors, so the link's constant flapping cannot make it chatter. |
| `🛡️ Battery — Control Stack Health Check` | Template condition so a link-only fault lights the sensor without producing a second push. Offender list now names removed/renamed automations instead of falling back to "an automation was removed". |

Both new automations are in the stack list **and** the template helper.

## Three traps hit while building this — all the same family

1. **The repair swallowed the alert.** v1 did reload → verify → alert. `homeassistant.reload_config_entry` does not return while the units are unreachable: the trace sat on that one action for **over seven minutes**, and `mode: single` dropped every later trigger as `failed_single`. The automation whose job was to say the fleet was gone had gone silent trying to fix it. → **Alert first, repair second**, and the throttle timer starts with the message.
2. **`script.turn_on` was a silent no-op.** The fire-and-forget was first built as a script. It saved fine and never became an entity — **this HA has no script domain loaded at all, zero script entities** — and `script.turn_on` against a missing entity logs nothing. Caught only because the reload visibly did not happen. → event bus instead. *Remember: any pattern routing through `script.*` is a silent no-op on this instance.*
3. **There are TWO `marstek_modbus` config entries**, `01KZHM0WZSEX4604C2K0R7R5X2` and `01KZJQNTQYH7PVNJ4H2ZDWVK5T`, both titled "Marstek Venus Modbus" and indistinguishable in the UI. The worker reloaded only the first — a fault on the other pack would have been reported, retried, and never repaired. They were in *different* states when found (one `setup_in_progress`, one `loaded`), which is exactly the split that makes reloading one useless. → `repeat/for_each` over both.

## Also found

- **`huawei_solar` config coordinator desynced 18:30–18:36.** `Invalid register count: expected 27, got 1` / `expected 25, got 27`. The *data* coordinator kept working (SoC updating) while `number.utility_room_inverter_maximum_discharging_power` and `select.utility_room_batteries_working_mode` went unavailable — i.e. the cap was unwritable while the readings looked fine. First occurred 17:23, after the restart. A reload of entry `01KYX9W3DGKKX6TXQA26HBGMGR` fixed it. Worth a watchdog of its own if it recurs.
- Standing **"Invalid config: template platform could not be set up"** notification since 15:10, predating this work. The flow-based template helpers are all fine; this is the YAML `template:` platform.
- Disabled `marstek_local_api` entry for VenusE at .58 (`01KPS2Q2SFYG67Y81NKZAXYBD3`). Left alone — re-enabling would put a second client on the same device.

## Verified live 18:40

Capability **0**, cap target **10000**, Huawei **10000 W** (branch 4B lifted it off 200 W at 18:13:00 the moment capability became honest), grid exporting ~2.8 kW, working mode `maximise_self_consumption`. Fleet automation detected the fault from a cold start on its `/10` poll at 18:20:00 with no state transition to trigger on, latched, stamped, alerted, and the worker took the blocking reload. Banner and push both confirmed delivered.

## Still open

1. **The units.** Neither answers on port 502. Needs power/Wi-Fi checked at the hardware, and probably a charge — D was under its reserve. Everything above is containment.
2. **Why both dropped within four minutes at ~00:07.** A shared cause, as on 2026-08-17 when the meter took both down in one second. The meter was up this time, so it is something else shared: AP, DHCP lease, or the packs' own firmware.
3. **Rename `switch.freezer` / `sensor.freezer_power`.** They are the Office TV. Dangerous during exactly this kind of incident.
4. **A `huawei_solar` config-coordinator watchdog**, if the register desync recurs.
