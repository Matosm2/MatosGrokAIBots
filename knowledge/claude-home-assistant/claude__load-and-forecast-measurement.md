# Load & Forecast Measurement — how big the sample can actually be

Written 2026-08-20 02:00. Companion to `claude/peak-prep-and-overnight-charging.md` (the design),
`claude/solar-forecast-accuracy-and-night-charge-fix.md` (the night the faults were found) and
`claude/tariffs-and-cost-asymmetry.md` (the prices, which govern the mean-vs-median choice below).
This doc answers one question: **how far back can we measure, and what does the fullest sample say?**

## How far back the data goes

| Source | Earliest data | Why |
|---|---|---|
| Recorder database | ~2025-07-16 (392 days) | Not the limit |
| `sensor.hw_p1meter_energy_import` / `_export` | ~2026-04-16 (122 days) | HomeWizard P1, older install |
| `sensor.house_load_energy` | **2026-08-02** | Sensor created then |
| `sensor.utility_room_inverter_solar_pv_daily` | **2026-08-01** | Huawei integration set up then |
| `sensor.energy_production_today` (+`_2`) | **~10 days, rolling** | **No `state_class` → no long-term statistics at all** |

Two hard ceilings, for two different reasons:

**Load and PV: 17 complete days (3–19 August).** The recorder holds 392 days, but the house-load
and Huawei sensors were only created on 1–2 August, so nothing older exists. The P1 meter reaches
back 122 days, but grid ≠ house load, and the battery and PV sensors needed to reconstruct house
load from it don't exist before 1 August either. 17 days is genuinely all there is.

**Forecast accuracy: ~10 days, permanently.** The Forecast.Solar sensors carry no `state_class`,
so HA keeps no long-term statistics for them — only raw recorder rows, purged at ~10 days. Re-running
that analysis in six months would still only see 10 days. Fixed going forward by the recorder below.

## The 17-day load sample (3–19 August), gross house load per band

| Day | AM 07–11 | MID 11–17 | PM 17–22 | night | total |
|---|---|---|---|---|---|
| Aug 03 | 6.25 | 19.94 | 14.64 | 19.27 | 60.10 |
| Aug 04 | 7.19 | 18.36 | 18.39 | 14.20 | 58.14 |
| Aug 05 | 6.08 | 9.89 | 13.25 | 33.12 | 62.34 |
| Aug 06 | 6.18 | 16.08 | 9.60 | 21.89 | 53.75 |
| Aug 07 | 10.02 | 27.47 | 19.11 | 53.75 | 110.35 |
| Aug 08 | 5.76 | **41.89** | 20.08 | 34.13 | 101.86 |
| Aug 09 | 4.16 | 7.04 | 8.87 | 13.15 | 33.22 |
| Aug 10 | 6.44 | 10.96 | 14.88 | 13.64 | 45.92 |
| Aug 11 | 6.84 | 32.46 | 21.84 | 13.65 | 74.79 |
| Aug 12 | 6.71 | 16.68 | 17.91 | 14.25 | 55.55 |
| Aug 13 | 5.00 | 37.79 | 26.15 | 26.63 | 95.57 |
| Aug 14 | 5.51 | 21.62 | 16.33 | 43.37 | 86.83 |
| Aug 15 | 4.77 | 14.57 | 14.28 | 14.71 | 48.33 |
| Aug 16 | 5.26 | 9.12 | 9.63 | 48.52 | 72.53 |
| Aug 17 | 5.84 | 13.81 | 8.24 | 42.64 | 70.53 |
| Aug 18 | 5.23 | 9.64 | 11.98 | 15.75 | 42.60 |
| Aug 19 | 10.19 | 11.78 | 7.78 | 35.99 | 65.74 |

| Band | mean | median | min | max | stdev | now in force |
|---|---|---|---|---|---|---|
| morning 07–11 | 6.32 | **6.08** | 4.16 | 10.19 | 1.63 | 6.1 |
| MID 11–17 | 18.77 | **16.08** | 7.04 | 41.89 | **10.39** | 16.0 |
| evening 17–22 | 14.88 | **14.64** | 7.78 | 26.15 | 5.25 | 14.5 |

### What the wider sample changed

**The 7-day window was understating every band** — morning 5.97 vs 6.32, MID 16.90 vs 18.77,
evening 13.48 vs 14.88. Small, but consistently in the direction that suppresses buying.

**More important: it showed the *statistic* matters more than the window.** MID has a standard
deviation of 10.39 kWh on a mean of 18.77 — range 7.04 to 41.89 — because midday EV charging lands
in that band on some days and not others (`sensor.house_load_energy` includes the car). Mean 18.77
against median 16.08: the mean is dragged up by a handful of car days.

**Why the median wins** (corrected 02:05 — the original justification here used a cost asymmetry
that did not survive checking; see `claude/tariffs-and-cost-asymmetry.md`):

Over-stating demand makes this system **buy**. Per kWh, over-buying costs `28.84 − 1.82 = 27.0 c€`
— and only when the day turns out sunny enough that the battery fills and exports. Under-buying
costs `3.87 c€` if the afternoon Peak Prep recovers it, `14.35 c€` if it does not, and a flat
`14.35 c€` for any morning-peak shortfall, which Peak Prep cannot reach at all.

So over-buying is still the dearer mistake, but by roughly 2–7× rather than the ~5× flat figure
claimed earlier. Concretely on MID: mean vs median is 2.7 kWh a night — about €0.73 lost if it
turns out unnecessary against about €0.39 saved if it was needed. **Median stands, on a narrower
margin than first stated.** Morning and evening are tight enough (stdev 1.63 and 5.25) that mean
and median agree within 0.3 kWh, so the choice is free there.

**Helpers changed accordingly**: `mean over 7 days` → **`median over 21 days`**, entities renamed
`sensor.{peak_am,mid,peak_pm}_load_median_21d`. 21 days rather than longer is a compromise: three
weeks covers three weekday/weekend cycles while still tracking into autumn heating load.

Hand-set values in force until the buckets fill, from the 17-day medians: **6.1 / 16.0 / 14.5**.

## Forecast Accuracy Recorder — so this sample grows

`☀️ Solar — Forecast Accuracy Recorder` + `input_number.solar_forecast_snapshot` +
`input_number.solar_forecast_ratio` + `sensor.solar_forecast_ratio_daily` (template) +
`sensor.solar_forecast_ratio_median_60d` (statistics, median, 60 days).

- **01:00** — both string forecasts for the coming day are summed and frozen into the snapshot.
  Deliberately the value the Overnight Charge Decision *saw*, not a later refreshed one: the
  question is "was the number we bet on any good", not "was Forecast.Solar eventually right".
- **23:55** — actual PV ÷ snapshot → ratio, and a notification. Above 1 = the array beat the
  forecast; below 1 = the forecast overshot.
- Actual comes from `sensor.utility_room_inverter_solar_pv_daily` (the PV figure), **not**
  `sensor.inverter_daily_yield`, which is AC output after conversion and battery routing and runs
  ~10% lower. Comparing AC yield against a DC forecast would bake in a permanent bias.
- Guards: does nothing if the snapshot is <1 kWh (HA was down at 01:00) or actual <0.5 kWh, rather
  than poisoning the 60-day median with a garbage ratio.

Seeded with 39.05 kWh for 20 August, so the first data point scores tonight.

`sensor.solar_forecast_ratio_median_60d` is the number to consult before touching
`input_number.battery_night_solar_trust` or the `forecast_solar` `damping_morning` setting — those
two are coupled and neither should be moved on a hunch. For reference, the 9-day sample measured on
19/20 August gave an aggregate ratio of **1.196**, but with the sign of the error flipping by
weather: 1.17–1.62 on bright days, 0.55–0.65 on the two dull ones.

## Live verification, 2026-08-20 01:45

The estimates were updated to the 17-day medians at ~01:33 mid-session. At the next `/15` poll the
new RE-EVALUATE branch fired on its own:

```
01:45:00  target 25% -> 31%
          forcible "Charging at 1000W until 31.0%"
          venus_e charge_to_soc 31 · venus_d charge_to_soc 31
```

Exactly the intended behaviour: a demand estimate written at any time takes effect on the next
poll rather than waiting for the next night. Confirms the RE-EVALUATE branch, the 3-point deadband,
and the re-issue path across all three packs.

## Follow-ups

1. **Re-read this table in mid-September.** 17 days spanning one weather break is thin, and the
   21-day median will be the first genuinely settled figure around 10 September.
2. **`sensor.house_load_energy` includes EV charging.** For MID that is the dominant source of
   variance. If the car's charging schedule becomes predictable, splitting house-only from
   house+EV would tighten the MID estimate far more than any window change.
3. **The forecast ratio needs ~3 weeks** before its median means anything. Do not touch trust or
   damping before then.
4. **The morning peak has no fallback.** That is the sharpest consequence of the corrected cost
   picture — see `claude/tariffs-and-cost-asymmetry.md` Follow-ups.
