# Huawei solar "unavailable" — root cause: Modbus write storm from branch 5 / 5B limit cycle

Investigated 2026-09-01. Integration: `huawei_solar` (custom), SUN2000-10K-MAP0-BE at 192.168.20.53:502, slave 1, entry `01KYX9W3DGKKX6TXQA26HBGMGR`, `enable_parameter_configuration: true`.

## Symptom

All four coordinators (`_data`, `_power_meter_data`, `_config_data`, `_battery_data`) fail together with:

> Error fetching HV2520094217_*_data_update_coordinator data: Timeout communicating with HV2520094217: the device did not respond in time

Every Huawei entity goes `unavailable` for ~30 s to ~3 min, then recovers on its own.

Frequency from `sensor.inverter_device_status` history (7 days, 25 Aug – 1 Sep):

| Day | unavailable episodes |
|---|---|
| 08-25 | 3 |
| 08-26 | 3 |
| 08-27 | 2 (+2 `unknown`) |
| 08-28 | 5 |
| 08-29 | 3 (+1) |
| 08-30 | 7 (+1) |
| 08-31 | 8 (+3) |
| 09-01 (to 08:20) | 1 |

~32 episodes plus ~7 `unknown` blips. Clustered in grid-import windows: 06:20–07:10 and 17:50–19:20. The trend worsens sharply from 08-30, the day branch 5B was added to the Discharge Cap Controller.

## Root cause

`automation.huawei_battery_tou_hold_while_car_charges_from_battery` (🔋 Huawei Battery — Discharge Cap Controller) branches **5 (MARSTEK FIRST)** and **5B (GRID SHORTFALL TOP-UP)** are in a stable limit cycle, not mutually exclusive as the description claims.

Live trace, `number.utility_room_inverter_maximum_discharging_power`, 2026-09-01:

```
07:00:10  200      <- branch 5 (target = 200)
07:00:25  1135     <- branch 5B (import + 200)
07:02:36  200      <- branch 5, lockout expired, |1135-200| > 400 deadband
07:02:52  1139     <- branch 5B
07:05:13  200
07:05:33  1129
...repeats every ~2.5 min all morning, and again 08:00–08:15
```

Same pattern on 2026-08-31 evening (18:51–19:18: 200 / 644 / 200 / 936 / 200 / 1228 / 200 / 792 / 200 / 1230 / 200), ending in two `unavailable` episodes at 19:14 and 19:18.

Why they fight: with `marstek_discharge_capability` = 2500 W the branch-5 formula concludes the Marstek fleet covers the house, so `sensor.huawei_discharge_cap_target` = 200 (the `min_cap` clamp). The Marstek does **not** actually deliver it, so grid import persists, so 5B correctly jumps the cap to import+200. Two minutes later the write lockout expires, branch 5 sees an 900 W deviation from its 400 W deadband and writes 200 back. The claimed mutual exclusion ("5B only fires when 5's condition is not met") fails because 5B's own write is what re-arms branch 5's deadband.

Cost of the write storm: each `number.set_value` on this integration takes ~8 s and holds the single Modbus TCP connection (the SDongle accepts one client). Two writes per 2.5 min from this loop, plus up to one write per minute from `automation.huawei_battery_charge_cap_controller` (436 changes on the charge register in 24 h, no write lockout at all on that automation), against four coordinators polling every 30 s. When a write lands on top of a poll, the poll times out and the whole integration flaps.

Secondary cost, not just cosmetic: the discharge cap sits at 200 W for roughly half of every peak-import window, so the Huawei is deliberately not covering the house at 32.71–43.20 c€/kWh — exactly what 5B was added to prevent.

## Recommended fixes, in order

1. **Break the limit cycle.** Add to branch 5's conditions a native `numeric_state` on `sensor.hw_p1meter_power` **below 150** — branch 5's formula must not step the cap *down* while the grid is genuinely importing. Ground truth beats the capability model; this is the same principle 5B was written on. Optionally add `for: "00:02:00"` so a momentary dip to zero import does not release it.
2. **Give the charge-cap controller a write lockout** too, or better, one shared `timer.huawei_modbus_write_lockout` across both cap controllers so the two registers cannot be written back to back.
3. **Investigate the capability over-report** separately: `marstek_discharge_capability` reads 2500 W while the fleet delivers far less (already noted in the automation's own 2026-08-30 correction). Whatever the mechanism, branch 5's target is wrong whenever this is true, and fix 1 only masks it.
4. **Update the custom `huawei_solar` integration.** `py.warnings` reports `services.py:457` and `:500` — `RuntimeWarning: coroutine 'DataUpdateCoordinator.async_request_refresh' was never awaited`. Post-`forcible_charge` refreshes are silently not happening on the installed version.
5. **Housekeeping:** `automation.fusionsolar_integration_auto_reload` is marked obsolete and still reloads five dead cloud config entries at 04:00 / 11:00 / 17:00. Unrelated to this fault but delete it with the integrations. Also, `custom_components.marstek_modbus` is emitting ~1900 warnings per two hours ("sensor 'gateway_ip'/'device_ip' has no scan_interval defined"), which makes the HA log window nearly useless for triage.
