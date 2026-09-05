# Energy & Battery Control Architecture — reference

Captured 2026-08-17/18 from live HA state. Policy per Matos: **battery covers the house by default, grid only feeds the cars.** `input_boolean.battery_marstek_first` stays ON.

## Hardware & meters (the key asymmetry)

| Pack | Capacity | Rated discharge | Control path |
|---|---|---|---|
| Huawei LUNA2000 | 21.9 kWh (derived, verify module count) | 10 000 W | Modbus `number.utility_room_inverter_maximum_discharging_power` |
| Marstek Venus E | 5.12 kWh | 2 500 W | `select.utility_room_marstek_venus_e_user_work_mode` |
| Marstek Venus D | 2.56 kWh | 2 150 W | `select.utility_room_marstek_venus_d_user_work_mode` |

Three separate grid meters, and **no device reads another's**:

- Huawei internal meter (`power_meter_active_power`) — the Huawei sizes its own charge/discharge from this. Blind to Marstek.
- HomeWizard P1 (`sensor.hw_p1meter_power`) — HA's view of the grid.
- **Marstek P1 meter @ 192.168.20.109 (IoT VLAN)** — the *only* input the Venus units obey in `anti_feed`. Not exposed to HA except indirectly as `device_tracker.wlan0_2` (~4 min lag).

This asymmetry is the origin of both the cross-charging class of faults and the capability-overreporting class.

## Three control surfaces

1. **Marstek mode** (`manual` | `anti_feed`) — coordinator trio: Force Manual (event), Restore Auto (1 min delay), Watchdog (30 s poll). All three must carry identical thresholds; divergence is the 2026-08-09 bug.
2. **Huawei discharge ceiling** — Discharge Cap Controller, 6 branches, first match wins:
   - 1 FORCE (EV force-charge on) → 0 W
   - 2 NIGHT FLOOR (01:00–07:00, at `battery_morning_floor`) → 0 W
   - 2B NIGHT CAR (01:00–07:00, above floor, car charging) → 400 W
   - 3 NIGHT ACTIVE (01:00–07:00, above floor, no car) → `battery_night_cap`
   - 4 DAY CAR → 400 W
   - 5 MARSTEK FIRST → `sensor.huawei_discharge_cap_target`
   Guarded by `timer.huawei_battery_write_lockout` (2 min) and a 400 W deadband on branch 5.
3. **Forced charging** — Force Grid Charge (all 3 packs → 50 %) and Peak Prep 16:15 / stop 17:00.

## Hysteresis latches (never share an edge)

| Axis | Stand down (manual) | Hold band | Release (anti_feed) |
|---|---|---|---|
| Huawei discharging | < −900 W, 30 s | −900 … −400 | > −400 W |
| Huawei charging | > +500 W, immediate | +200 … +500 | < +200 W |
| Marstek SoC | either < 15 % | 15 … 20 % | both > 20 % |

Stand-down uses **either** unit (safety = pessimistic). Release requires **both** (permission = conservative).

Escape hatch from the SoC-floor deadlock: genuine-export absorb window = marstek_first ON + `binary_sensor.utility_room_hw_p1meter_grid_exporting` ON + fleet SoC < 99 % + **sun between sunrise and sunset**. `anti_feed` is the only recharge path — `manual` follows `force_mode`=standby, i.e. idle.

## The Marstek-first cap formula

```
need = house_load − solar − marstek_discharge_capability + margin
cap  = clamp(need, 200, 10000)   →  sensor.huawei_discharge_cap_target
       (short-circuits to 10000 when capability <= 0)
```

`marstek_discharge_capability` is **rated** power, not measured — deliberate, because measured output closes a feedback loop (lift cap → Marstek backs off → need rises → lift cap further).

**Consequence:** every way the Venus units can silently stop delivering becomes an un-covered load and a grid import. Three gates now sit on that template:
- 2026-08-13 — **mode-aware** (unit in manual+standby was counted)
- 2026-08-17 19:47 — **meter-aware** via `device_tracker.wlan0_2`
- 2026-08-18 00:05 — **delivery-aware** via `input_boolean.marstek_delivery_fault` (below)

## Delivery-shortfall failsafe — built 2026-08-18 00:05

Guards the *symptom* rather than each new cause.

| Entity | Role |
|---|---|
| `sensor.marstek_fleet_ac_power` | min_max SUM helper over both units' `ac_power` — measured truth |
| `input_boolean.marstek_delivery_fault` | Latch. Gates capability to 0 → cap target → 10 000 W |
| `automation.marstek_delivery_shortfall_failsafe` | Sets and clears the latch |

**Latches** when grid > 400 W for 90 s AND fleet AC < 200 W AND capability > 1 000 W. Blocked while either car charges, during 01:00–07:00, during force grid charge, and when marstek-first is off.

**Releases** on fleet AC crossing ±300 W for 30 s (both directions — the daytime recovery signal is *charging* from solar, i.e. negative AC power), **or** a silent 30-minute probe.

**Why a probe:** once the Huawei covers the house the grid sits at zero, so a healthy Venus in `anti_feed` correctly does nothing. No power-flow signal distinguishes "recovered" from "still broken", so without the probe a single transient would demote the fleet permanently. Cost of a persistent fault: ~90 s of import per 30 min instead of continuous.

**Why no feedback loop:** one-way hysteretic latch fired by a *contradiction* between predicted and measured, not a continuous setpoint.

## Incidents 2026-08-17

- **19:33:36** Marstek P1 meter dropped off the VLAN. Both Venus units stopped within 1 s at 98 % SoC. Capability held 4 650 W → Huawei pinned at 200 W → grid imported at peak tariff. Fixed 19:47 by the meter-aware gate (capability 4650→0, cap 200→1300, grid +981→−315 W).
- **21:10:28** meter returned; units resumed.
- **22:22:23** Venus D stopped at 25 % SoC, meter online, mode correct. **Unexplained.** Suspect a device-level discharge cut-off on the D, or firmware difference (D V147.115.1177 vs E V148.119.113).
- **23:47:41** Venus E stopped; tracker `not_home` 23:51:40 → `home` 23:53:01 (81 s — below the alert's 5 min debounce, so **silent**). Capability jumped back to 4 650 W before either unit resumed → cap 200 W → grid **+1 846 W** with Huawei at 85 %.
- **2026-08-18 00:07** resolved: latch set, capability 0, cap 10 000 W, Huawei −2 069 W, grid +32 W.

Meter dropouts on 08-17: 00:32 (16 s), 02:35 (1 s), 09:24 (1 s), 19:37–21:10 (93 min), 23:51–23:53 (81 s). **The meter is the physical root cause.**

## Still open

1. **Stabilise 192.168.20.109** — static lease, fixed AP, check PSU / VLAN. Root cause; everything else is containment.
2. **Venus D 25 % stop** — check the Marstek app for a per-unit depth-of-discharge setting.
3. **Tighten the P1-offline alert** — 5 min `for:` misses sub-5-min dropouts that still stop the fleet for hours. Consider 60 s.
4. **Consider raising `input_number.battery_marstek_first_min_cap`** 200 → ~700 W, so an arithmetic failure the latch misses costs hundreds of watts not kilowatts.
5. **Resume-lag guard** — capability is credited the instant the tracker reads `home`, before the units actually resume. The delivery latch now covers this in practice, but a 2 min `for:` on the tracker would be cleaner.

## Containment recipe if the failsafe is ever bypassed

Turn **off** `input_boolean.battery_marstek_first`. Branch 5 stops, "Restore Full Discharge" returns the Huawei to 10 000 W. Setting the cap by hand only buys ~5 min (next `/5` poll overwrites it).
