# Tariffs & Cost Asymmetry — the authoritative numbers

Written 2026-08-20 02:05, after Matos challenged a figure I had repeated twice without checking it.
**This doc supersedes any cost-asymmetry claim in the other battery docs.** Where they say
"under-buying costs 3.87 c€/kWh", read this instead.

## Prices — all available as live sensors, not just prose

| Quantity | Value | Sensor |
|---|---|---|
| Current all-in price | 0.28841 €/kWh (read 01:50, super-off-peak band) | `sensor.engie_engie_empower_flextime_wallonia_current_price` |
| Injection (export) price | **0.01822 €/kWh** | `sensor.engie_engie_empower_flextime_wallonia_injection_price` |
| Energy component | 0.10665 €/kWh | `..._energy_component` |
| Network component | 0.1013 €/kWh | `..._network_component` |

Band structure (ENGIE Empower Flextime, Wallonia), confirmed against the live `current_price`:

| Band | Hours | c€/kWh |
|---|---|---|
| Super off-peak | 01:00–07:00 | 28.84 |
| MID | 11:00–17:00, 22:00–01:00 | 32.71 |
| PEAK | 07:00–11:00, 17:00–22:00 | 43.20 |

No automation reads these sensors — all logic keys off time-of-day bands, and prices live only in
descriptions. That is deliberate (ENGIE re-indexes every ~5 days) but it does mean the numbers
written in prose go stale silently. **The injection price in particular was guessed at "about 5 c€"
in earlier notes and is actually 1.82.**

## The correction

Earlier notes asserted a clean asymmetry: "over-buying costs ~24 c€/kWh, under-buying costs
3.87 c€/kWh because the afternoon Peak Prep fallback catches it — so over-buying is ~5× dearer."

The 3.87 is real arithmetic — `32.71 − 28.84`, MID minus super-off-peak. **It was applied far too
broadly.**

### Over-buy — 27.0 c€/kWh, conditionally

`28.84 paid − 1.82 recovered = 27.02 c€/kWh`.

Full-day balance: buying X kWh overnight means PV fills X kWh less of the battery during the day,
so X kWh more is exported at the injection price. The house is served from storage either way.

**This loss only materialises if the battery actually fills and exports.** On a day that turns out
as dull as forecast, the purchased energy simply displaces a later import at ≥28.84 and costs
nothing — or saves money. So the over-buy penalty is really the penalty for *the forecast having
been too pessimistic*, which the measured data says happens: ratios up to 1.62 on bright days.

### Under-buy, evening peak — 3.87 c€/kWh *if recovered*, 14.35 if not

Peak Prep Continuous runs `/10` across **11:00–16:55** and buys in the MID band at 32.71 instead of
28.84 — hence 3.87. But it only closes the gap when it can:

- **Huawei only.** The Venus units are not charged by it.
- **Confidence-ramped threshold** — at 11:00 it takes a 4.25 kWh deficit to commit.
- **5000 W power clamp** and a hard stop at 17:00.

When it does not close the gap, the energy is imported during the evening peak instead:
`43.20 − 28.84 = 14.35 c€/kWh`.

### Under-buy, morning peak — 14.35 c€/kWh, always

**There is no fallback for the morning peak.** Peak Prep's window opens at 11:00; the morning peak
is 07:00–11:00 and is over by then. Nothing else buys in that window. A morning shortfall is
imported at 43.20, full stop.

This is a real gap in the design, not a rounding detail — see Follow-ups.

## Where that leaves the tuning arguments

| Claim made earlier | Status |
|---|---|
| "Over-buying is ~5× dearer than under-buying" | **Overstated.** True range is ~2× (vs an unrecovered under-buy) to ~7× (vs a recovered evening one). |
| "Use the MEDIAN for the band load estimates, not the mean" | **Still correct**, but on narrower grounds. Mean 18.77 vs median 16.08 on MID is 2.7 kWh/night: ~€0.73 lost if wasted, ~€0.39 saved if needed. Over-buying is still the dearer mistake. |
| "The Adaptive Floor calculator should use a MAX, this one a MEDIAN" | **Still correct**, and now better founded — the floor guards the morning peak specifically, which is the one with no fallback and a flat 14.35 penalty. |
| "The morning floor is unnecessary because Peak Prep catches under-buying" | **Wrong.** This was the argument used on 2026-08-20 to drop the morning-floor guarantee. Peak Prep cannot catch a morning shortfall. The decision happened to be harmless that night — the corrected estimates put the target at 31%, near the 35% floor — but the reasoning was not sound. |

## Follow-ups

1. **Reconsider the morning-floor guarantee.** The argument against it does not survive this
   correction. `target = max(target, battery_morning_floor)` in the Overnight Charge Decision is a
   two-line change; the open question is whether the Adaptive Floor's 35% is itself inflated (its
   5% morning-solar assumption should be 7–15% — see `peak-prep-and-overnight-charging.md`
   Still open #2). Fix the floor first, then decide whether to bind the overnight target to it.
2. **Consider a morning-band fallback** analogous to Peak Prep, buying in the 22:00–01:00 MID band
   for the next morning. Same 3.87 spread, and it would give the morning peak the recovery path it
   currently lacks.
3. **Sanity-check prose prices against the live sensors** whenever these docs are revised. The
   injection price being off by 3× went unnoticed because nothing reads it.
