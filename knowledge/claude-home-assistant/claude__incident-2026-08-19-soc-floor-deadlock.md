# Incident 2026-08-19 — peak-tariff grid import from the SoC-floor deadlock

**Status: fixed and verified live 21:16.**

Investigated ~20:55–21:00. Repeated ~1 kW imports at peak tariff. **Not** a meter dropout — `device_tracker.wlan0_2` had been `home` since 05:49.

## Chain

1. **Venus D at 14 %**, below `input_number.marstek_floor_soc` (15 %). The Force Manual SoC-floor rule used **either** unit, so the whole fleet — including Venus E at 36 % — was parked in `manual`.
2. `manual` follows `force_mode` = standby → fleet AC power **0 W**.
3. Capability correctly fell to 0 → `sensor.huawei_discharge_cap_target` short-circuited to 10 000 W.
4. **But the Huawei number had already been written to 200 W.** Trace `4143986494535c19be0587e8f90a91ca`: branch 5 fired on the `/5` time pattern at **20:55:00.24** and wrote 200; the Marstek flipped to `manual` at **20:55:04**, 4 s later. The Modbus write takes ~8 s and then started the 2 min lockout.
5. Result: Huawei pinned at 200 W (delivering 139 W against 44 % SoC), Marstek idle, **grid +877 → +1 142 W for a full 5 minutes**, until the 21:00 poll wrote 10 000 W at 21:00:28.

The `grid_import` trigger **did** fire on time at 20:55:34 — a 2 ms run that did nothing, because every branch able to raise the cap is gated on the write lockout. The delivery-shortfall failsafe was also blocked: it needs capability > 1 000 W to latch, and capability had honestly fallen to 0. Nothing miscalculated; the only writer able to fix it had just throttled itself.

Fleet mode changed **17 times** between 19:40 and 21:00 as the D hovered on the 14/15 % edge.

## Fixes applied 2026-08-19 ~21:05

### 1. Discharge Cap Controller — new branch 4B "MARSTEK IDLE RESCUE"

Inserted between branches 4 and 5, **deliberately not gated on `timer.huawei_battery_write_lockout`** (the same exemption branch 1 has). Fires only when marstek-first is on, outside the night window, no car charging, no EV force-charge, no forced grid charge, **capability < 1 W and cap < 1 000 W** — i.e. only when the house is provably uncovered. Writes `sensor.huawei_discharge_cap_target`.

Mutually exclusive with branch 5 on the situation: after 4B writes, its own `cap < 1000` guard goes false, and branch 5 then sees cap == target so its 400 W deadband is not met.

New trigger `capability_lost`: `sensor.marstek_discharge_capability` below 1 **for 15 s**. The delay is deliberate — the automation is `mode: single` and the branch-5 write takes ~8 s, so an instant trigger would be silently dropped.

Worst-case exposure drops from ~5 min to ~15–20 s.

### 2. SoC floor made per-unit, across all three coordinator automations

The floor is the only stand-down reason that is a property of an **individual pack** (it protects that pack's EPS backup reserve — freezer on the D port, water heater on the E). The other six — Huawei busy either direction, Tesla drawing, either EV force-charge, cross-charging — are properties of the **system** and still stand both units down together.

- **Force Manual** — action is now `choose` (fleet reason → both to `manual`) with `default` → per-unit `numeric_state` tests against `marstek_floor_soc`.
- **Restore Auto** — the "both units above release" condition replaced by a per-unit `to_anti_feed` set; the write is a `repeat` over that set.
- **Watchdog** — restructured. The old multi-entity drift guards (`not (all manual)`, `not (all anti_feed)`) would have reverted any deliberate split on the next 30 s tick, so changing Force Manual alone would have done nothing. It now computes `to_floor_manual` and `to_anti_feed` per unit at the top of each run and corrects only genuine disagreement. The floor step moved ahead of the `choose` as an `if/then` so it no longer blocks the anti_feed branch from releasing the healthy unit in the same tick. Dwell (3 min) moved into the template and is now per-unit — the old `or` clause switched the dwell off entirely whenever the fleet was split.

`to_floor_manual` (SoC < 15) and `to_anti_feed` (SoC > 20, or absorb window) are disjoint by construction; 15–20 % remains a hold band, now per pack.

## Verification, live

| Time | Event |
|---|---|
| 21:10:30 | Watchdog released **Venus E only** → `anti_feed`. Venus D stayed `manual`. |
| — | `sensor.marstek_discharge_capability` 0 → **2 500 W** (E's rating alone) |
| 21:15:08 | Branch 5 wrote cap **200 W** (Marstek now leads) |
| 21:15:18 | Fleet AC 7 → **1 175 → 1 538 W** — the E picked up the house in ~10 s |
| 21:16:33 | **grid +5 W**, fleet AC 1 526 W, Huawei −146 W, D safe at 14 % |

Zero mode changes in the six minutes after the split, against 17 in the preceding 80.

## Still open

1. **Venus D is at 14 % and cannot recharge tonight** — `anti_feed` is the only recharge path and its escape hatch needs daylight + export. It will sit there until tomorrow's export window. A deliberate overnight top-up to ~30 % would clear it. Ties into the unexplained 08-17 stop at 25 % (per-unit depth-of-discharge setting in the Marstek app?).
2. Raising `input_number.battery_marstek_first_min_cap` 200 → ~700 W still worth doing — caps the damage of any future race at hundreds of watts.
3. Watch for `to_anti_feed` / `to_floor_manual` template errors in the log over the next day; they replaced schema-validated native conditions and fail silently by nature.
