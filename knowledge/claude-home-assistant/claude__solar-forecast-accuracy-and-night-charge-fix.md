# Solar Forecast Accuracy, Load Calibration & the Overnight-Charge Fixes — night of 2026-08-19/20

Companion to `claude/peak-prep-and-overnight-charging.md`. Three faults found and fixed in one
session, plus the measurement that settles the "is the forecast inflated?" question.

> **Cost figures in this doc are superseded by `claude/tariffs-and-cost-asymmetry.md`.** The
> "morning floor is unnecessary" conclusion below rested on a cost argument that did not survive
> checking — see the correction inline.

## Fault 1 — the overnight decision read the wrong day (FIXED 00:45)

`automation.battery_overnight_charge_decision_01_00` fires at **01:00** and computed
`solar_fc = energy_production_tomorrow + _tomorrow_2`. At 01:00 on the 20th, "tomorrow" is the
**21st**; the day that actually charges the battery is the **20th**. One day out at every firing.
It only reads correctly if you inspect the config in the evening, which is when it was written.

Now reads `energy_production_today_remaining (+_2)` — the whole coming day at 01:00, and unlike
`_today` it self-corrects if the automation re-evaluates later in the window.

## Fault 2 — `battery_day_load_estimate` was less than half the real figure (FIXED 00:56)

Seven days of hourly `sensor.house_load_energy` and `sensor.utility_room_inverter_solar_pv_daily`:

| Day | PV | Load | 07–11 gross | 07–11 PV | **07–11 net** | 11–17 load | 17–22 gross | **17–22 net** | PV crossover |
|---|---|---|---|---|---|---|---|---|---|
| Aug 13 | 82.2 | 95.6 | 5.00 | 6.01 | −1.01 | 37.79 | 26.15 | 8.70 | 10:00 |
| Aug 14 | 79.1 | 86.8 | 5.51 | 6.18 | −0.67 | 21.62 | 16.33 | 1.47 | 10:00 |
| Aug 15 | 55.7 | 48.3 | 4.77 | 4.29 | 0.48 | 14.57 | 14.28 | 6.29 | 08:00 |
| Aug 16 | 52.1 | 72.5 | 5.26 | 3.53 | 1.73 | 9.12 | 9.63 | −0.40 | 10:00 |
| Aug 17 | 46.3 | 70.5 | 5.84 | 7.00 | −1.16 | 13.81 | 8.24 | 2.19 | 09:00 |
| Aug 18 | 16.9 | 42.6 | 5.23 | 3.34 | 1.89 | 9.64 | 11.98 | 8.35 | 09:00 |
| Aug 19 | 19.7 | 65.7 | 10.19 | 6.83 | 3.36 | 11.78 | 7.78 | 5.86 | 09:00 |
| | | | mean **5.97** | | max **3.36** | median **13.81** | mean **13.48** | max **8.70** | |

> Superseded by the 17-day sample in `claude/load-and-forecast-measurement.md`. The values set
> that night (6.0 / 14.0 / 15.0) were revised the same night to 6.1 / 16.0 / 14.5.

Only the day-load figure was materially off, and it sits in the `surplus` term, so an 8 kWh value
inflated surplus by ~6 kWh every night and suppressed buying.

Note this load figure **includes EV charging** — the 05:00/06:00 hours run 4.5–7 kWh and Aug 13
put 10 kWh into the midday hours. That is correct for the energy balance when the car charges
during the day, and slightly pessimistic when it charges only at night.

## Fault 3 — the Venus RS485 control mode drops out ~30 s after being set (GUARDED 01:10)

Observed live at the 01:00 firing:

```
01:00:32  both RS485 switches -> on          (automation, correct)
01:00:34  charge_to_soc 25, power 1200, force_mode charge — all accepted
01:01:03  both RS485 switches -> OFF          (nobody asked)
01:01:22  fleet AC 0 W. Units idle. Huawei charging fine at 1091 W.
01:01:39  RS485 re-asserted by hand
01:02:35  Venus E -1195 W, Venus D -1188 W. Held ever since.
```

The timeout appears to trip only while the units are **idle** — once they draw, RS485 stays on.
Every write in that sequence carries `continue_on_error: true`, so this failed exactly as silently
as the 2026-08-18 charge-cap latch: writes accepted, nothing moving, no alert.

Two guards added:

1. **Inline VERIFY step**, 45 s after the write sequence: if `sensor.marstek_fleet_ac_power` is
   above −200 W, re-assert RS485 + `force_mode: charge`, wait 45 s, and **notify** if it still is
   not drawing. Failure becomes visible instead of silent.
2. **Widened /15 re-issue condition** — was "session running AND Huawei back to Stopped". Now also
   fires on a non-drawing fleet, gated on combined SOC still being more than 2 points below
   `battery_night_target_soc` so it cannot loop against packs that have legitimately finished.

## The forecast itself — measured, and NOT inflated

Forecast at 01:00 (both strings) against measured PV:

| Date | Forecast | Actual | Ratio |
|---|---|---|---|
| Aug 11 | 63.9 | 85.6 | 1.34 |
| Aug 12 | 70.2 | 82.1 | 1.17 |
| Aug 13 | 68.2 | 82.2 | 1.20 |
| Aug 14 | 64.5 | 79.1 | 1.23 |
| Aug 15 | 34.3 | 55.7 | 1.62 |
| Aug 16 | 37.2 | 52.2 | 1.40 |
| Aug 17 | 35.4 | 46.3 | 1.31 |
| Aug 18 | 30.5 | 16.9 | **0.55** |
| Aug 19 | 30.5 | 19.7 | **0.65** |
| **Total** | **434.6** | **519.7** | **1.196** |

It under-predicts ~20% in aggregate; seven of nine days came in above forecast. The "inflated"
impression comes from 18 and 19 August, where it overshot by 45% and 35%. Both readings are true —
different regimes.

**Nine days is the permanent ceiling for this analysis** — the Forecast.Solar sensors carry no
`state_class`, so no long-term statistics exist and raw recorder rows are purged at ~10 days. The
Forecast Accuracy Recorder built the same night fixes that going forward; see
`claude/load-and-forecast-measurement.md`.

Likely cause of the low bias: both `forecast_solar` config entries carry `damping_morning: 0.4`
and `inverter_size: 10000`, while measured string peaks reach 10 274 W and 10 180 W. **Not
changed** — it drives the Energy dashboard too.

`battery_night_solar_trust` stays at **0.8**. It only matters where it flips the decision
(`forecast ≈ 27/trust`): at 0.8 that is 34 kWh, firing on exactly the two days that needed it; at
1.0 it fires on none of them; at 0.6 it adds three false alarms on days that made 46–56 kWh. The
forecast's error flips sign with the weather, which is why a single scalar works better than the
aggregate ratio suggests.

## Result of the corrected 01:00 run

```
solar_fc 39.05 × 0.8 − dayload 14.0 = surplus 17.24
avail 0.91 (csoc 15.2%)   peakneed 21.0   ->  deficit 2.85
target 25%   Huawei 1000 W + Venus 1200 W each = 3.4 kW
```

Bought ~2.9 kWh at 28.84 c€ (~€0.84), landing the fleet at 25% ≈ **3.7 kWh above the 12% reserve**
— which covers the worst measured 07:00–11:00 net draw of the last seven days (3.36 kWh) with a
small margin. Later the same night the estimates were revised to the 17-day medians and the new
RE-EVALUATE branch lifted the target to 31% on its own.

### The morning-floor decision, and why its justification was wrong

On the night, the conclusion drawn was: *"the morning-floor guarantee turned out to be
unnecessary — with honest inputs the deficit formula lands within 0.4 kWh of the measured
worst-case morning bridge on its own, and forcing `battery_morning_floor` would have bought
5.6 kWh instead of 2.9."*

The arithmetic there is fine. **The cost argument underneath it was not.** It leaned on
"under-buying is cheap because the afternoon Peak Prep fallback catches it at 3.87 c€/kWh" —
and Peak Prep runs 11:00–16:55 and sizes against the *evening* peak. **Nothing recovers a morning
shortfall**; it is imported at 43.20, a flat 14.35 c€/kWh penalty. See
`claude/tariffs-and-cost-asymmetry.md`.

So the outcome was harmless that night — the corrected estimates put the target at 31%, close to
the 35% floor — but the reasoning does not generalise. It should be revisited, in this order:

1. Fix the Adaptive Floor's morning-solar assumption (5% assumed, 7–15% measured), which is what
   inflates the 35% floor.
2. Then decide whether to bind the overnight target to the corrected floor.

## Follow-ups

1. **`automation.battery_adaptive_floor_cap_calculator` — the 5% morning-solar assumption is low.**
   Measured share is 7–15%. Raising it lowers the floor and stops the Discharge Cap Controller
   over-reserving the Huawei overnight. Its 07:00–10:00 window also does not match the 07:00–11:00
   peak band.
2. **Capacity inconsistency.** The floor calculator sums Huawei 21.9 + Marstek 5.12 = 27.02 kWh
   and omits the Venus D's 2.56; the overnight decision uses 28.38. One of them is wrong.
3. **`damping_morning: 0.4`** — see above. Coupled to trust: lowering damping raises every forecast
   ~20% and would need trust dropped by roughly the same to hold the decision threshold.
4. **Watch whether the RS485 drop-out recurs** at tomorrow's 01:00 firing now that VERIFY exists —
   the notification is the signal. If it fires nightly, the real fix is the Marstek's RS485
   disconnection-timeout register rather than a retry.
5. **Revisit the morning floor** once #1 is done — see the correction above.
