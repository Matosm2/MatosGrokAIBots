# Grid injection — root-cause analysis (2026-08-27)

Question: why does power get injected into the grid from time to time? Reviewed 7 days of meter history plus the coordinator trio and Discharge Cap Controller. **No automation exports deliberately or by fault.** Three distinct mechanisms:

## 1. Batteries full + PV surplus — dominant (kWh scale)

Every sustained export block coincides exactly with `sensor.combined_battery_soc` = 100%:

| Date | Window (local) | Export | SoC |
|---|---|---|---|
| Aug 24 | 14:00–19:00 | ~12.5 kWh, up to 8.9 kW peak | 99–100% |
| Aug 25 | 16:00–19:00 | ~4.5 kWh | reached 100 ~18h |
| Aug 26 | 13:00–19:00 | ~17 kWh at 2.6–4.5 kW sustained | 100% from ~14:00 |

With ~10–11 kW PV and 29.6 kWh total storage filling by early afternoon in late August, the surplus has no sink. The coordinator's export-absorb window correctly requires fleet SoC < 99%, so it cannot help here — this is physics, not logic.

## 2. Cloud-edge charge-lag spikes (seconds, multi-kW)

While charging hard (Huawei at ~9.3 kW), PV swings on cloud edges faster than the charge controller ramps → brief exports to −6.3 kW observed Aug 27 midday. Same weather condition as the cloudy-sky mode-flapping fixed 2026-08-27 (thresholds widened). Controller lag, benign.

## 3. Night/evening handoff transients (seconds, negligible Wh)

Both packs discharge against separate meters; a load step-off or a mode handoff briefly over-covers the house:

- Aug 27 01:55 → −1518 W spike as Huawei stepped −588→−1229 W with Marstek holding ~1000 W.
- Aug 27 02:20–02:35 → −2135 W bursts as a Venus unit stood down (fleet 900→124 W) and the Huawei stepped up.
- Aug 26 ~20:00 → −4560 W for seconds on a large load step-off with both packs discharging.
- The 01:00 night-cap branch boundary also produces a transition blip (import +4.1 kW / small export within one 5-min bucket).

Ramp-down lag on the Huawei plus the Venus anti_feed loop reacting to its own P1 meter — not preventable from HA without harming stand-down behaviour. Cost per event ≪ 1 Wh-cent scale.

## Perception note

`binary_sensor.utility_room_hw_p1meter_grid_exporting` latches ON below −400 W and OFF only above 0 W, so it flips visibly for transients worth almost nothing, and hovers/flickers near zero during normal anti_feed regulation ripple (midday buckets: mean ~+10 W).

## Verified during review

- Coordinator trio (Force Manual / Restore Auto / Watchdog) thresholds agree post the 2026-08-27 widening: stand-down −1200 W (60 s) / +800 W (20 s), quiet band −300..+400 W, per-unit SoC floor 15/release 20.
- Discharge Cap Controller branches cap discharge only; nothing writes a discharge that could exceed house load by design.
- Absorb window gates (marstek_first + exporting + fleet<99% + daylight) behaved correctly in all episodes — fleet was at 100% during the big exports.

## Recommendation

The only meaningful lever is a bigger sink before the packs fill: solar-surplus EV charging — e.g. sustained export > ~1.5 kW for 5 min + car plugged in + fleet SoC high → start/raise charging amps; stop on sustained import. Otherwise the afternoon surplus (~15 kWh/day in this weather) goes to grid at injection rates, which is unavoidable and still better than a zero-export limit that would curtail the PV.
