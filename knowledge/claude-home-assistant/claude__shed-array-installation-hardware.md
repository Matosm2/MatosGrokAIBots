# Shed Array — installation hardware list and sourcing

Written 2026-09-04. Follows `claude/venus-d-pv-array-and-relocation-plan.md`, which is now **closed on the
panel question**: the JA Solar route was taken.

Illustrated build sheet published as an artifact (roof plan, hanger-bolt section, ground-row elevation,
MPPT channel schematic): <https://claude.ai/code/artifact/1e16863f-b3cb-469c-832c-d33f0d67427c>

## Decisions taken

- **Panels bought: 8 × JA Solar JAM54D41-455/LB** (2ememain Charleroi route). 3 640 Wp, ~€600.
- **Siting: 4 on the shed roof (timber), 2 + 2 on the ground around the shed**, orientation of the
  ground pairs not yet fixed — the plan's east/west recommendation applies to them.
- Roof layout assumed for quantities: **one row of four in portrait**, 4 600 mm wide × 1 762 mm
  up-slope, on two horizontal 40 × 40 rails at the frame quarter-points (880 mm apart).

## Bill of materials — ≈ €1 032 incl. VAT

| Assembly | Contents | Cost |
|---|---|---|
| **A — roof** | 10 × hanger bolt M10×200 w/ plate + EPDM (€4.97), 8 × rail 40×40 1.19 m (€8.23), 2 × rail connector (€4.08), 4 × end cap (€1.10), 6 × mid clamp 30 mm (€2.02), 4 × end clamp 30 mm (€2.06) | €148.46 |
| **B — ground** | 6 × adjustable triangle 15–35° (€43.87), 8 × rail, 8 × end clamp, 4 × mid clamp, 8 × end cap, 12 × ballast slab | €410.42 |
| **C — DC** | 4 × MC4 Y-splitter pair (€16.48), ~52 m H1Z2Z2-K 6 mm² single-core, 20× MC4 pack, crimp tool, earth clips + 6 mm² G/Y, UV cable ties | €228.52 |
| **D — AC** | ~25 m EXVB 3G2.5, 16 A curve C breaker, 30 mA type A RCD, IP65 enclosure + socket, conduit + warning tape | €245.00 |

All-in ≈ **€0.45/Wp** including the panels (€1 632). Payback ~3.5 years against ~€450/yr of displaced
peak-band imports.

**Assembly B is the weak line.** €263 of aluminium triangles for four panels; two treated-timber
A-frames come to €100–130 at any Charleroi merchant and hold 22 kg panels fine. Rails and clamps are
bought either way.

**Assembly C alternative.** Wattuneed's prefab 2 × 6 mm² with MC4 fitted is €8.63/m — ~€224 for the
26 m of two-core needed, against ~€123 for bulk cable + connectors + crimp tool.

## Five site measurements that change the order

1. **Roof width along the eaves.** Four in portrait needs 4 600 mm clear + ~100 mm rail overhang each
   end. Narrower → 2 wide × 2 high (2 290 × 3 570 mm), which needs **4 rails not 2** and roughly
   doubles rail and bolt count.
2. **Rafter spacing and section.** Bolts must land in a rafter or purlin, never deck boarding alone;
   ≥ 50 mm of thread into solid wood. Nominal bolt spacing is 1 190 mm — move each to the nearest
   rafter centre and add one rather than stretch a span.
3. **Roof covering** (felt / shingle / EPDM / sheet) — decides the sealing detail at the penetration,
   not the bolt. On felt or shingle, dress flashing over the plate as well as the EPDM washer.
4. **Roof pitch and azimuth** — decides whether the roof four are the south plane or one of the E/W pair.
5. **Cable run lengths**, DC and AC. Section D assumes 25 m of AC.

## Electrical checks done

- Per channel, 2 in parallel: **Imp 27.6 A vs 32 A (14 % headroom)**, Isc 29.1 A vs 40 A, Voc cold
  ~43 V vs 60 V ceiling. 910 W of 1000 W per channel.
- **Series is forbidden**: 2 × Voc 39.5 = 79 V, above the 60 V absolute input.
- **Bifacial gain applies to the ground rows only.** Tilted on triangles over grass, +5–10 % rear gain
  takes a channel to ~30 A — still inside 32 A, but **do not site them over gravel, white chippings or
  a light concrete apron.** The roof four, flush to a dark covering, gain almost nothing.
- Roof load 88 kg over ~8 m² ≈ 11 kg/m² panel-only; Belgian design snow adds ~50 kg/m², wind uplift more.
  **If the rafters are under 38 × 100 mm at 600 mm centres, sister them or add a purlin first.**
- AC: fixed circuit only — dedicated 16 A curve C behind a 30 mA type A RCD, **EXVB not XVB** (XVB may
  not be buried in open ground per RGIE/AREI), trench ~60 cm with warning tape, IP65 enclosure at the unit.
- **Phase choice is deliberate**: the outdoor circuit's phase becomes the Venus D's phase. Phase 2
  carries the heaviest load. Below firmware V149 the two Marstek units do not coordinate.

## Sourcing — two trips

| Store | Covers | Where | Pickup |
|---|---|---|---|
| **Wattuneed** · +32 87 45 00 34 | A, B, C in one stop | Rue Henripré 12, 4821 Andrimont (Dison), ~1 h 10 | Sells to private buyers. **Call to confirm counter pickup** and stock of 6 triangles + 16 rail units. |
| Ecostal | Structure/cable fallback, has *déstockage* | Soumagne, ~15 min past Wattuneed | Primarily B2B — phone before travelling. |
| **Cebeo Charleroi (Jumet)** · 071 29 73 73 | D — EXVB, breaker, RCD, IP65 | Première Rue 1, 6040 Jumet, ~10 min | B2B counter; Rexel Charleroi equivalent. |
| Brico / Gamma / Hubo Charleroi | Slabs, timber, conduit, coach screws, tape | Several branches | Walk-in. |
| offgridtec.com | MC4 + made-to-length cable | DE, delivery only | In-house cable shop, MC4 fitted. |

## Still open

1. **Low-temperature charging on the Venus D — still blocking the outdoor plan.** Spec gives
   −20/+60 °C operating with no separate charge window and no heater mentioned. Charging LFP below
   0 °C plates lithium, and winter is when this array earns. Ask Plug-in Solar Energy, Gent
   (09 296 30 29), the Belgian Marstek partner, before committing the unit to a garden. If the BMS
   does not block sub-zero charge, the unit stays somewhere above freezing and the DC cable loss is
   accepted instead.
2. **Declare the array to the DSO** (ORES or RESA) — separate from the existing Huawei installation.
3. **HA changes before go-live**, unchanged from the PV array plan: add Venus D PV to the `solar` term
   in the discharge-cap formula; move the forecast-accuracy recorder on both sides when the third
   Forecast.Solar string is added; correct `energy-battery-architecture.md` where it claims `anti_feed`
   is the only recharge path.
4. Confirm the MC4 connector family on the delivered JA panels (Evo2 or standard) before buying splitters.
5. Confirm the M10×200 fixing screw is a **wood** double-thread, not a sheet-metal thread.
