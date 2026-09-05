# Force Grid Charge — Adaptive Target & Conditional Prep Cards (2026-08-20)

Companion to `claude/peak-prep-and-overnight-charging.md`. That doc's "50% cap" references for the
manual Force Grid Charge override are superseded by this one.

## The fixed 50% cap is gone

`🔌 Force Grid Charge — Start All Batteries` no longer charges to a hardcoded combined 50%. On
start it computes, in top-level automation `variables`, the combined SOC needed to carry the house
**from now until 01:00** (when the super off-peak opens):

```
need    = Σ over bands [07-11, 11-17, 17-22, 22-01] of estimate × fraction_of_band_remaining
avail   = max(0, (combined_SOC − 12) / 100 × fleet)       # 12 = Venus reserve edge
solar   = (remaining string1 + string2) × night_solar_trust (0.8)
deficit = need − avail − solar
target  = clamp(combined_SOC + deficit / fleet × 100, combined_SOC, 100)
fleet   = input_number.battery_usable_capacity + sensor.marstek_fleet_capacity  (20.7 + 7.68 = 28.38)
```

Band estimates are the measured helpers (`battery_morning_peak_demand_estimate`,
`battery_day_load_estimate`, `battery_peak_demand_estimate`) plus one **new hand-tuned helper for
22:00–01:00**: `input_number.battery_late_evening_demand_estimate` (default 4.5 kWh) — that slice
has no measured band because the Battery Band Load meter's night bucket is 22–07. A session started
between 01:00 and 07:00 counts the whole coming day as "until 01:00" (h clamps to 07:00).

The target is written to **`input_number.battery_force_charge_target_soc`**, and the Stop
automation's trigger and condition both read that helper as their `above:` bound — start and stop
can never disagree. Per-device targets (Huawei `target_soc`, Marstek `charge_to_soc`) carry the
same value, keeping the belt-and-braces property. The start guard is now a template condition
(`combined_SOC < fc_target`) because the target only exists as a variable at trigger time — a
native bound on the helper would read the previous session's value.

Verified by template render 2026-08-20 ~03:00: h=7, need 41.10, avail 5.22, solar 28.79 →
deficit 7.09 → target 55% (csoc 30.4). Under the old rule this would have stopped at 50%.

**Cost note:** the 22–01 slice bought at MID (32.71) to avoid importing at MID (32.71) is a small
loss after round-trip losses; its value is margin so the battery does not run dry *inside* the
17–22 peak. If that margin proves unnecessary, set `battery_late_evening_demand_estimate` to 0
rather than touching the automation.

## Dashboard: time-conditional prep cards (energy-prices/storage)

New tod helper **`binary_sensor.peak_prep_window`** (11:00–17:00). The "Peak prep" section is now
"Charge prep" with two mutually exclusive markdown cards:

- **Evening peak prep** card — visible while the tod sensor is `on` (11:00–17:00). Same math as
  before, legacy "would charge at 16:15" text corrected.
- **Overnight charge** card — visible the rest of the day. Branches: night session running (live
  SOC → target + both charge powers) / evening waiting for the 01:00 decision / night window idle /
  morning recap with the "morning peak has no fallback" warning.

The Force-override markdown card now shows the adaptive target from
`input_number.battery_force_charge_target_soc` instead of the hardcoded 50% texts. Two tiles added:
"22–01 demand est." and "Force target (auto)".

## New helpers

- `input_number.battery_force_charge_target_soc` (10–100 %, written by the Start automation)
- `input_number.battery_late_evening_demand_estimate` (0–15 kWh, hand-tuned, 4.5)
- `binary_sensor.peak_prep_window` (tod, 11:00–17:00)
