# Peak Prep & Overnight Charging — rebuilt 2026-08-18, revised 2026-08-20

Companion to `claude/energy-battery-architecture.md`. That doc covers who supplies the house;
this one covers when we *buy*. See also `claude/solar-forecast-accuracy-and-night-charge-fix.md`
(the night the faults were found), `claude/load-and-forecast-measurement.md` (the measured load
and forecast samples) and `claude/tariffs-and-cost-asymmetry.md` (**the authoritative prices** —
any cost figure quoted below defers to it).

## Tariff (ENGIE Empower Flextime, Wallonia — all-in c€/kWh)

| Band | Hours | Price |
|---|---|---|
| Super off-peak | 01:00–07:00 | **28.84** |
| MID | 11:00–17:00, 22:00–01:00 | 32.71 |
| PEAK | 07:00–11:00, **17:00–22:00** | **43.20** |

Injection (export) is **1.82**. Night→peak spread **14.35**; MID→peak spread 10.49. ENGIE
re-indexes roughly every 5 days, so nothing hardcodes these prices in logic — only in descriptions.
All four are available as live sensors from the Engie integration; nothing reads them yet.

## The 2026-08-18 incident (why this was rebuilt)

Two independent faults, one visible symptom: the evening peak ran on an empty battery.

**Fault 1 — the window was too short by construction.** Peak Prep fired once at 16:15 with power
clamped to 5000 W and a hard stop at 17:00: **3.75 kWh maximum transfer**. Measured deficit that
day was 5.24 kWh. Uncoverable, silently.

**Fault 2 — nothing moved at all.** The forcible charge was issued and accepted
("Charging at 5000W until 48.0%"), but `number.utility_room_inverter_maximum_charging_power` had
been **0 W since 15:31**. Huawei SOC sat at 23.0% for the whole hour.

The 0 was a **latch in the Charge Cap Controller**. Its STARVING branch writes
`actual_intake − 300 W` floored at 0, and 0 is absorbing: at 0 the Huawei draws nothing, so the
branch's own guard (`batteries_charge_discharge_power above 200`) can never be true again.

Neither fault raised anything: the 17:00 peak failsafe only fires on battery charge >500 W, and
there was none.

## Charge Cap Controller

- STARVING floored at `input_number.huawei_charge_cap_floor` (500 W), not 0.
- **UNSTICK branch**, second in the choose: limit below the floor → lift it to the floor,
  unconditionally. Recovers an already-stuck value; the floor alone only prevents the descent.
- RELEASE also fires on `input_boolean.battery_grid_charge_session`.

## Peak Prep — continuous (entity_id still `automation.battery_peak_prep_decision_16_15`, legacy)

- `/10` across 11:00–16:55 instead of one shot at 16:15.
- **Confidence ramp**: `threshold = max(0.5, 0.5 + (hours_left − 1) × 0.75)` kWh.
  6 h left → 4.25 kWh to commit; 0.75 h left → 0.5 kWh, the original figure.
- Power sized to the remaining window: `deficit / hours_left`, clamped 1000–5000 W.
- Hysteresis: start above threshold, stop only at deficit ≤ 0.
- **Derate**: PV forecast trusted only as far as it has proven itself today —
  `actual yield so far / forecast for the same elapsed period`, clamped 0.3–1.2.
- Huawei only. The coordinator's own +500 W charge-side rule parks the Venus units in manual.
- `avail` is read live each tick, so extra afternoon load that drains the battery **already**
  widens the deficit and buys more. Its one remaining static input, `need`, is now measured
  (below).

> **Scope limit, easy to forget:** Peak Prep serves the **evening** peak only. Its window opens at
> 11:00, after the 07:00–11:00 morning peak has already passed, and it sizes against
> `battery_peak_demand_estimate`. **There is no fallback for the morning peak at all.** Any
> reasoning of the form "under-buying overnight is cheap because Peak Prep catches it" is valid for
> the evening and false for the morning.

## Overnight Charge — the primary mechanism

`🌙 Battery — Overnight Charge Decision (01:00)` + `🌙 Battery — Overnight Charge Stop`.

```
avail   = max(0, (combined_SOC − 12) / 100 × fleet_capacity)      # 12 = Venus backup-reserve edge
solar   = (today_REMAINING string1 + string2) × trust             # trust 0.8
surplus = max(0, solar − day_load)                                # day_load, measured
deficit = morning_peak_need + evening_peak_need − avail − surplus  # both measured
target  = min(night_max_SOC, combined_SOC + deficit / fleet × 100) # night_max_SOC 80 %
```

**`today_remaining`, not `tomorrow`.** At 01:00 "tomorrow" is the day *after* the daylight that
will charge the battery — an off-by-one that only reads correctly if you inspect the config in the
evening. `_today_remaining` is the whole coming day at 01:00 and self-corrects if the automation
re-evaluates at 04:00.

**The target is independent of current SOC.** Substituting `avail`:

```
target = 12 + (peakneed − surplus) / fleet × 100
```

This is what makes continuous re-evaluation safe — charging towards the target does not move the
target, so there is no feedback loop.

### Continuous re-evaluation (added 2026-08-20)

The `/15` poll no longer only re-issues a stalled session. Three branches now, first match wins:

1. **CHARGE** — deficit > 1 kWh and target > SOC + 2, on the 01:00 / EV-change / startup triggers,
   or when a running session has stalled.
2. **RE-EVALUATE** — a running session whose recomputed target has moved by **≥3 points**
   (~0.85 kWh of the fleet). Publishes the revised target and re-issues all three packs with
   re-sized power. A revised target *below* current SOC needs no stop logic here: the Stop
   automation triggers on `battery_night_target_soc`, so publishing the lower value closes the
   session on its own /5 poll.
3. **NO ACTION** — 01:00 only, notify and stand down.

The 3-point deadband keeps a six-hour session to a handful of Modbus writes rather than 24.

### Actuator verification

Every Marstek write carries `continue_on_error`, so a failed write is silent. After the write
sequence the automation now **waits 45 s and checks `sensor.marstek_fleet_ac_power`**; if the fleet
is not drawing it re-asserts RS485 + `force_mode: charge`, waits again, and notifies on persistent
failure. The `/15` re-issue condition also fires on a non-drawing fleet, gated on SOC still being
more than 2 points below target so it cannot loop against finished packs.

This exists because of the **RS485 drop-out measured 2026-08-20 01:00**: both switches went ON at
01:00:32, all writes were accepted, and both switches fell back to OFF at 01:01:03 with the units
still idle. Re-asserting by hand started them immediately and it held — the timeout appears to trip
only while the units are idle.

### Other properties

- All three packs, write order RS485 → charge_to_soc → power → force_mode. Order matters.
- Charge power is one shared 1200 W write — below both Venus maxima, so neither is clamped.
- **80 % cap is the solar-headroom guard**: ~5.7 kWh of the 28.4 kWh fleet always left free for
  morning PV, whatever the arithmetic says.
- EV guard: wall connector charging → Huawei 2000 W, Venus 800 W each (7.4 kW → 3.6 kW combined).
- Stop at target / 06:45 / gate off / manual force-charge. 06:45 not 07:00: fifteen minutes of
  slack for nine Modbus calls across three devices.

## Demand estimates are measured, not hand-set (added 2026-08-20)

Three constants used to be typed in by hand. Measured against 17 days of hourly data, morning
(6.0 vs 6.32 mean / 6.08 median) and evening (15.0 vs 14.88 / 14.64) were roughly right by luck;
`day_load` was 8.0 against a measured 16.08 median and inflated `surplus` by ~8 kWh every night.

**Chain:**

```
sensor.house_load_energy
  → utility_meter "Battery Band Load", daily cycle
      tariffs peak_am 07-11 · mid 11-17 · peak_pm 17-22 · night 22-07
      driven by 🏠 Battery Band Load — Tariff Switcher (+ startup resync)
  → template sensors *_last_day exposing each bucket's last_period
  → statistics helpers *_load_median_21d (median, 21 days, keep_last_sample)
  → 🔋 Battery — Band Load Estimate Calculator at 00:50
      writes battery_morning_peak_demand_estimate / battery_day_load_estimate /
             battery_peak_demand_estimate
```

**Median, not max — the opposite of the Adaptive Floor calculator, deliberately.** Over-stating
demand here makes the automations *buy*, and buying is the dearer mistake. The full cost picture is
in `claude/tariffs-and-cost-asymmetry.md`; the short version is over-buy 27.0 c€/kWh (and only on
days sunny enough to export) against under-buy 3.87 c€/kWh if Peak Prep recovers it, 14.35 if not,
and a flat 14.35 for anything the *morning* peak needed. Roughly 2–7× in favour of under-buying, so
the median. The Adaptive Floor calculator faces the reverse asymmetry — it guards the morning peak
specifically, the one with no fallback — and correctly uses a MAX.

**Gross, not net of PV.** The overnight formula already credits the whole day's forecast PV through
`surplus`; subtracting PV here as well would double-count it.

**Cold-start guard**, same idiom as the floor calculator: a statistics helper with no samples
reports a real small number, not `unavailable`, so any median below 1.0 kWh is treated as "no data
yet" and the existing helper value is kept. Clamps (morning 2–20, MID 4–40, evening 4–30) are rails
against a freak day surviving the median — a 41.89 kWh MID day was measured on 2026-08-08.

First real write after one full day; settled after 21. Until then the hand-measured 17-day medians
of 2026-08-20 stand: **6.1 / 16.0 / 14.5**.

Why a second utility meter rather than more tariffs on `house_load_windows`: a utility_meter's
tariff list is fixed at creation, and that meter's morning window is 07:00–10:00, which does not
match the 07:00–11:00 peak band. The Adaptive Floor calculator depends on it, so it was left alone.

## Two booleans, deliberately not one

| Boolean | Releases the Huawei charge cap | Stands the Marstek coordinator down | Suppresses the 17:00 peak failsafe |
|---|---|---|---|
| `battery_grid_charge_session` | yes | **no** | no |
| `battery_night_charge_running` | (set alongside) | yes | no |
| `battery_force_grid_charge` | yes | yes | **yes** |

The afternoon session must never suppress the peak failsafe, and must never stand the coordinator
down (it needs the +500 W rule to park the Venus units). The overnight session must stand it down,
because it owns the units through force_mode + RS485.

## Helpers

`input_boolean`: `battery_grid_charge_session`, `battery_night_charge` (gate, ON),
`battery_night_charge_running`.

`input_number`: `huawei_charge_cap_floor` 500 W · `battery_night_solar_trust` 0.8 ·
`battery_night_max_soc` 80 % · `battery_night_target_soc` (written by the decision) ·
`battery_morning_peak_demand_estimate` / `battery_day_load_estimate` /
`battery_peak_demand_estimate` (written nightly by the Band Load calculator, hand-overridable) ·
`solar_forecast_snapshot` / `solar_forecast_ratio` (Forecast Accuracy Recorder).

`utility_meter` Battery Band Load · 4 template sensors · 4 statistics helpers.

## Verified live, 2026-08-20 01:00–01:45

- Decision fired with the corrected day and day-load: `surplus 17.24, avail 0.91, deficit 2.85 →
  target 25%`, ~2.9 kWh at 28.84 c€.
- Huawei 1093 W + Venus 1195/1188 W = 3.4 kW. Combined SOC 14.4 → 18.0% within 20 minutes.
- RS485 drop-out caught and fixed by hand; guards added so the next occurrence is automatic.
- Estimates revised to the 17-day medians at 01:33; at **01:45:00** the RE-EVALUATE branch lifted
  the target 25% → 31% and re-issued all three packs unprompted. The re-evaluation path works.

## Tuning notes

- If the **morning** peak keeps importing, the lumped formula is the suspect: it credits the whole
  day's surplus against both peaks, which is optimistic for 07:00–09:00. Remember there is no
  afternoon fallback for the morning — prefer lowering `battery_night_solar_trust`, or bind the
  overnight target to `battery_morning_floor` once that floor is itself corrected.
- If the overnight charge keeps under-buying on dull days, lower `battery_night_solar_trust` before
  touching anything else — but read the trust-vs-threshold table in
  `solar-forecast-accuracy-and-night-charge-fix.md` first; 0.8 is near-optimal on measured data.
- If solar starts getting exported on August mornings, lower `battery_night_max_soc`.

## Still open

1. Everything in `energy-battery-architecture.md#still-open` — the 192.168.20.109 Marstek P1 meter
   is still the physical root cause of that family of faults.
2. **Adaptive Floor calculator assumes morning solar is 5% of the daily forecast**; measured
   07:00–11:00 PV is 7–15%. Its floor is correspondingly inflated (35% on 20 August against a real
   need nearer 25%). Its window is also 07:00–10:00, not 07:00–11:00.
3. **Capacity inconsistency**: the floor calculator sums 21.9 + 5.12 = 27.02 kWh and omits the
   Venus D's 2.56; the overnight decision uses 28.38.
4. **`damping_morning: 0.4`** on both `forecast_solar` entries is the prime suspect for the 20%
   low bias in the PV forecast. Coupled to trust — do not change one without the other.
5. **Watch for the RS485 notification** at the next few 01:00 firings. If it fires nightly, fix the
   Marstek's RS485 disconnection-timeout register rather than relying on the retry.
6. **The morning peak has no recovery path.** Either bind the overnight target to a corrected
   `battery_morning_floor`, or build a 22:00–01:00 MID-band prep for the next morning — same
   3.87 c€ spread as the afternoon one. See `claude/tariffs-and-cost-asymmetry.md`.
