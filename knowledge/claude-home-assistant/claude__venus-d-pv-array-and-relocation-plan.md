# Venus D PV Array & Outdoor Relocation — plan and parts

Written 2026-08-21, sourcing updated 2026-08-27. DC-coupled PV array for the Venus D, the decision to relocate the unit outdoors
next to the panels, and sourcing. Also records the **three-phase discovery**, which contradicts an
assumption in `energy-battery-architecture.md`.

**Panel status (2026-08-27):** the Aiko A440 at €48.95 (solar-outlet.nl) was sold out. Two live options:

1. **Dealer route (preferred for warranty/invoice): Wattuneed, Rue Henripré 12, 4821 Dison —
   HT-SAAE Jupiter 455 W bifacial N-TOPCon full black at €90/pc on sale** (from €104.99). 8 pcs =
   €720, €0.198/Wp. Confirm stock of 8 + pickup by phone before driving (~1h10 from Charleroi).
2. **Cheapest: 2ememain Charleroi pickup — JA Solar JAM54D41 455 W €74.99 / 460 W €69.99**
   (professional-looking sellers, but classifieds — verify seller status, batch, invoice).

Backup: Luxen LNDB-500ND from offgridtec.com, €102.84 incl. VAT, single units orderable.

## Three-phase discovery (2026-08-21) — supersedes a pooled-capability assumption

`sensor.hw_p1meter_power_phase_1/2/3` read 2249 / 3604 / 3063 W. **The house is three-phase.**

1. Marstek's FAQ: three-phase multi-device means **one device per phase**, and *"with only two
   devices, one phase must remain unused."* With two units today, one phase has no Marstek coverage.
2. Coordination is firmware-gated: **V149+** for three-phase one-per-phase, **V151** for
   single-phase multi-device (plus CT002 V118 / CT003 V114, app 1.6.21+).
   Current: **E = V148.119.113, D = V147.115.1177** — both below V149. The units are not
   coordinating today; they are two independent controllers watching one meter. Consistent with both
   stopping within 1 s when 192.168.20.109 dropped on 08-17.
3. **`marstek_discharge_capability` pools rated power across units** and the cap formula subtracts it
   from *total* house load. If units become phase-assigned that is wrong — a unit on phase 1 cannot
   cover a load on phase 3. Review before adding a third unit.
4. Wallonia has no capacity tariff (Flanders since 2023), so `peak_demand_current_month` of
   22 959 W is not billed.

## Venus D 25 % stop — resolved, not a DoD floor

13 days of daily SoC minima: **3, 7, 11, 11, 11, 12, 12, 12, 13, 14, 24 %.** The 2026-08-17 22:22
stop at 25 % was a transient, not a device limit. Closes open item #2 in
`energy-battery-architecture.md`.

Manual confirms rated AC output **800 VA / 2200 VA, 9.57 A @ 230 V** — matches the 2150 W HA
reports. The web store's "2.5 kW" is peak.

## The PV input is low-voltage and unforgiving

| Spec | Value |
|---|---|
| MPPTs | 4 independent |
| MPPT range | 16–55 V (startup 22 V) |
| **Absolute max input** | **60 V — series connection forbidden** |
| Max current / channel | 32 A (40 A Isc) |
| Max total PV | 4000 W |
| Connector | MC4 |

Max 4 panels direct, 8 in parallel pairs.

### Selection rules for any candidate

- **Voc_STC ≤ 50 V** (cold Voc rises ~10 % at −10 °C; the ceiling is really ~53 V)
- **Imp ≤ 15 A** so two in parallel stay under the 32 A channel limit
- **You need 4 matched pairs, not 8 identical panels.** Nothing is in series and each MPPT is
  independent, so channel 1 and channel 3 can be different models. Only the two panels *within* a
  pair must match (shared voltage node). This makes clearance shopping viable.
- Beware **large-wafer / low-cell-count designs** (G12, 96-cell): low voltage, high current, e.g.
  DMEGC DM470G12RT ~16 A Imp → 32 A in parallel, on the limit.
- **Never an AC module.** SunPower P6 AC with Enphase IQ8MC outputs 230 V AC — cannot connect to a
  DC MPPT input at all.

## Panel candidates evaluated

| Module | Voc | Imp | 2-par Imp vs 32 A | 8× total | Price ea | €/Wp |
|---|---|---|---|---|---|---|
| **Aiko A440-MAH54Db** (sold out) | 40.05 V | 13.07 A | 26.1 A — **18 %** | 3520 W | €48.95 | 0.111 |
| **JA Solar JAM54D41-455 LB** (2ememain Charleroi) | 39.5 V | 13.79 A | 27.6 A — 14 % | 3640 W | €74.99 | 0.165 |
| **HT-SAAE HT54-18X(ND)-F 455** (Wattuneed dealer) | 39.1 V | 13.92 A | 27.8 A — 13 % | 3640 W | €90.00 | 0.198 |
| **Luxen LNDB-500ND** | 40.0 V | 14.92 A | 29.8 A — 7 % | **4000 W** | €102.84 | 0.206 |
| Luxen LNDX-450ND | 35.21 V | 14.96 A | 29.9 A — 7 % | 3600 W | €92.86 | 0.206 |
| Aiko A500 MCE54Mw-B (glass-foil) | 41.3 V | ~14.4 A | 28.7 A — 10 % | 4000 W | €146.95 | 0.294 |
| DMEGC DM470G12RT | ~34.7 V | ~16.2 A | ~32.4 A — **over** | 3760 W | €99.95 | 0.213 |
| Jolywood 455 bifacial | 35.11 V | 15.09 A | 30.2 A — 6 % | 3640 W | €59.00 | 0.130 |

**Note on the two Luxen modules:** the 450 is a *96-cell* design and the 500 a *108-cell* one. They
carry essentially the same current (14.96 vs 14.92 A), so the 500 gives 11 % more power at higher
voltage for €10 more. **The 500 dominates the 450 — do not buy the 450.**

### HT-SAAE Jupiter 455 detail (dealer option — Wattuneed, 2026-08-27)

HT54-18X(ND)-F-455: Voc 39.1 V · Isc 14.61 A · Vmp 32.7 V · Imp 13.92 A · 108-cell N-TOPCon
bifacial double-glass full black · 1762 × 1134 × 30 mm · 25 kg · Voc temp coeff **−0.25 %/°C**
(cold Voc at −10 °C ≈ 40.1 V — trivially safe).

- 2-parallel Imp 27.8 A vs 32 A = 13 % headroom; bifacial → mount flush / low albedo.
- 8 × 455 = 3640 W; 8 × 25 kg = 200 kg.
- **€90/pc on sale (from €104.99) → €720, €0.198/Wp.** Real dealer: invoice, product warranty,
  Belgian consumer protection.
- Wattuneed also stocks: Aiko Neostar 3S 475 W €148.34 / 485 W €171.43, Jinko Tiger Neo 510 W
  €135.45 (Voc ~46.6 V — passes, less margin), Jolywood 500 W full black €113.74 (out of stock).
- **Call before driving:** confirm ≥ 8 in stock and store pickup in Dison.

### JA Solar JAM54D41-455/LB detail (cheapest — 2ememain Charleroi, 2026-08-27)

Voc 39.5 V · Isc 14.56 A · Vmp 33.0 V · Imp 13.79 A · 108-cell n-type TOPCon full-black bifacial
double-glass · 1762 × 1134 mm · ~22 kg · MC4 · bifaciality 80 %±10 %.

- Cold Voc at −10 °C ≈ 43 V — safe with margin.
- 2-parallel Imp 27.6 A vs 32 A = **14 % headroom**; Isc 29.1 A vs 40 A = 27 %.
- **Bifacial double-glass** — mount flush / low albedo to keep current headroom.
- 8 × 455 = 3640 W; 8 × ~22 kg = ~176 kg.
- **Cost 8 × €74.99 ≈ €600 → €0.165/Wp**, no shipping.
- Sellers: 2ememain Charleroi — [460 W listing €69.99, seller "W - SRL"](https://www.2ememain.be/v/bricolage-construction/panneaux-solaires-accessoires/m2431584294-panneaux-solaires-460w-69-99)
  and [455 W listing €74.99, seller "MB"](https://www.2ememain.be/v/bricolage-construction/panneaux-solaires-accessoires/m2413821390-panneaux-solaires-455w-fullblack).
  Both marked new, pickup available — but these are **classifieds, not a storefront**. Verify:
  registered business + invoice, exact model suffix on the label, quantity ≥ 8 from one batch.

### Luxen LNDB-500ND detail

Voc 40.0 V · Isc 15.84 A · Vmp 33.51 V · Imp 14.92 A · 108 cells (6×18) LECO N-TOPCon bifacial
SMBB half-cut · 1961 × 1134 × 30 mm · 27.5 kg · MC4 · IP68 JB, 3 bypass diodes · 1500 V system.

- Cold Voc at −10 °C ≈ **43.6 V** (assuming −0.26 %/°C). Safe even at a pessimistic −0.35 %/°C
  (46.3 V). **Voltage is not a risk at Voc 40 V.**
- 2-parallel Imp **29.84 A vs 32 A = 7 % headroom.** Isc 31.68 A vs 40 A = 21 %. Safe from damage,
  but will clip in bright cold conditions.
- **It is bifacial** — rear gain of +5–15 % on an elevated or high-albedo mount would push current
  past the limit. **Mount flush / low albedo** to preserve headroom.
- 8 × 500 = **exactly 4000 W, 100 % of the input limit.** Expect a few percent of clipping on the
  best days. Acceptable (normal DC oversizing behaviour), but there is no headroom left.
- 8 × 27.5 kg = **220 kg**; 17.8 m² of array.
- **Cost 8 × €102.84 = €822.72 → €0.206/Wp.**
- **VAT caution:** the €86.42 "0 % VAT" is §12 UStG, Germany's domestic zero-rate for PV delivered to
  the installation operator. Cross-border B2C to Belgium normally means Belgian VAT (21 %) instead —
  €86.42 × 1.21 = €104.57. Budget ~€103–105 either way; do not count on €86.42.

## Decision: relocate the Venus D outdoors, next to the array

**IP65**, rated −20 to +60 °C, grid connection is a **Euro16A three-wire household plug**. Moving it
to the panels and running AC back:

- DC, ~30 A @ ~33 V, 20 m on 6 mm²: **~9 %**
- AC, 9.57 A @ 230 V, 20 m on 2.5 mm²: **1.2 %**

With the unit beside the array, DC runs are ~3 m → ~1.4 %. Best change in the design.

### Conditions

1. **Cold-weather charging — VERIFY WITH MARSTEK.** Manual gives −20/+60 °C operating but does not
   separate charge from discharge limits and mentions no heater. LFP charging below 0 °C causes
   lithium plating. Winter is when this array earns. **Resolve before buying.**
2. **Choose the phase deliberately.** The outdoor socket's phase becomes the D's phase. Phase 2
   carries the highest load (3604 W).
3. **Fixed circuit, not an extension lead.** XVB/EXVB in conduit, dedicated 16 A breaker, 30 mA RCD
   per RGIE/AREI. 2.5 mm² fine to ~30 m.
4. **Shade the unit.** 500 mm top / 150 mm rear clearance. North side or under the array.
5. **Mounting must carry ~176–220 kg** depending on module choice, plus wind load.

## Orientation: split the four MPPTs — free, and worth more than extra wattage

Tariff bands (from `tariffs-and-cost-asymmetry.md`):

| Band | Hours | c€/kWh |
|---|---|---|
| Super off-peak | 01:00–07:00 | 28.84 |
| MID | 11:00–17:00, 22:00–01:00 | 32.71 |
| **PEAK** | **07:00–11:00, 17:00–22:00** | **43.20** |
| Injection | — | **1.82** |

South peaks ~13:00 — MID band, and in summer exported at 1.82. **East peaks 09:00–10:00, inside the
morning PEAK window**; west peaks 16:00–18:00, feeding the evening PEAK. The spread between
displacing a PEAK import and exporting is **24×**, so losing ~20 % of gross yield to E/W is strongly
positive.

It also targets the one documented gap: *"There is no fallback for the morning peak. Peak Prep's
window opens at 11:00... A morning shortfall is imported at 43.20, full stop."*

Mixing orientations is normally costly because series-string modules drag each other down. **Four
independent MPPTs make it free.** Recommend 2 channels east, 2 west.

## HA changes required before the array goes live

1. **Add Venus D PV to the `solar` term** in `need = house_load − solar − marstek_discharge_capability
   + margin`. DC PV into the D never touches the Huawei, so the term under-reports, inflates `need`,
   lifts the Huawei cap and discharges the Huawei into a house solar already covers.
2. **Forecast-accuracy recorder must move on both sides together.** Adding a third Forecast.Solar
   string while the actual still reads `sensor.utility_room_inverter_solar_pv_daily` (Huawei DC only)
   collapses the ratio and poisons `sensor.solar_forecast_ratio_median_60d`, which governs
   `input_number.battery_night_solar_trust` and the overnight buy.
3. **`energy-battery-architecture.md` is now wrong** where it says *"`anti_feed` is the only recharge
   path — `manual` follows `force_mode`=standby, i.e. idle."* DC PV charges the D regardless of work
   mode. The SoC-floor deadlock escape logic assumes it.

## Sourcing

**Rejected for order-quantity restrictions:** advancedtec.de, gigatek.be, ev-power.be.
Kabelpro.be sells genuine Stäubli but mostly in 100-packs.
**solar-outlet.nl** is a clearance outlet — Longi 375 had 2 units, Swiss Solar 400 had 1 (marked
*restvoorraad*, possible cosmetic damage). Only its current-gen lines are properly stocked.

| Source | What | Note |
|---|---|---|
| **Wattuneed** (Rue Henripré 12, 4821 Dison) | **HT-SAAE 455 W €90 on sale; Aiko 475/485, Jinko 510** | **Real Belgian dealer, sells to individuals, physical store, ~1h10 from Charleroi.** Call to confirm ≥ 8 in stock + pickup. |
| 2ememain.be (Charleroi) | JA Solar JAM54D41 455 W €74.99 / 460 W €69.99 | Cheapest, local pickup — but classifieds. Verify seller is a registered business, invoice, batch of ≥ 8. |
| **offgridtec.com** (DE) | Luxen LNDB-500ND €102.84 | Mail-order backup. In-house *Kabelmanufaktur* — makes PV cable **to length with MC4 fitted**, stocks *Abzweigbuchsen Y-Stecker*. Best source for prepared cables. |
| Ecostal (BE) | Wholesaler with a *déstockage* (clearance) section | Primarily B2B/installers — call before travelling to ask if they sell to individuals. |
| Off Grid Power Station (Vught, NL) | JA Solar 445 W bifacial all black €119, pickup by appointment | ~150 km; dominated by Wattuneed on price and distance. |
| solar-outlet.nl | JA Solar 470 glass-glass €104.95 | Best-value properly-stocked line there. Get datasheet first. |
| pluginsolarenergy.be (Gent) | Official **Marstek partner in Belgium** | Free BE/NL shipping. Phone 09 296 30 29 re Venus D cold-charging and V149 firmware. |
| kleineskraftwerk.de | Pre-assembled MC4 cables 1.5 m €11.90 → 25 m €51.90; **Y-set €10.90** | Ships Germany only. EU alternatives: balkonkraftwerk-express.de, solago.de, pvundso.de. |
| 2dehands.be / 2ememain.be | Surplus/individual panels | Commonly 4–10 panel lots. No warranty unless seller is professional with invoice. |

**Avoid CCA cable.** Insist on tinned copper H1Z2Z2-K.

**Optimizers: buy none.** All Huawei, requiring a SUN2000 inverter with FusionSolar — without the
handshake they sit in safety shutdown at ~1 V. The SUN2000-450W-P2 outputs up to 80 V, above the D's
60 V threshold. Optimizers fix series-string mismatch, which cannot exist here.
(They *would* suit the existing Huawei array if it has shading — MERC-1300W-P, ~€30–44.)

### Remaining bill of materials

- 4 × MC4 Y-splitter sets, Evo2-compatible if the panels use Evo2 (~€40)
- Short MC4 extensions if the ~1200 mm factory leads don't reach (~€40)
- Mounting for ~176–220 kg (~€300–500)
- AC circuit: XVB/EXVB, 16 A breaker, 30 mA RCD, outdoor socket (~€150–250)

**Total ≈ €1300–1650 for 4.0 kWp** at Luxen 500 pricing; **≈ €1100–1450 for 3.64 kWp** at the
JA Solar or HT-SAAE price.

## Economics

Export mean 10.3 kWh/day, median 7.1; import mean 16.8 kWh/day. Summer marginal PV is worth almost
nothing (1.82 c€); value is concentrated Oct–Mar when imports run 36–51 kWh/day and production is
~100 % self-consumed at ~35 c€. ~4 kWp ≈ 3600 kWh/yr → roughly **€450/yr**, payback ~3–4 years —
the inverter cost is already sunk in the Venus D.

**Install before winter.** The months that justify the array start in October. Module prices
stabilised through 2026 with a slight downward drift and no meaningful fall forecast for 2027.

## Open questions

1. **Low-temperature charging on the Venus D** — blocking issue for the outdoor plan.
2. **Declare the array to the DSO** (ORES or RESA).
3. Whether pooled `marstek_discharge_capability` needs to become per-phase.
4. **Wattuneed:** confirm ≥ 8 × HT-SAAE 455 in stock and store pickup in Dison.
5. **2ememain sellers (if pursued):** registered business? invoice? exact model, batch of ≥ 8.
