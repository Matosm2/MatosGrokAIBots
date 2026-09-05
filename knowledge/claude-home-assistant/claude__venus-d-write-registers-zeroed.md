# Venus D — every writable Modbus register reads 0 since 2026-08-25/26

Found 2026-08-31 while investigating the fleet outage (`claude/incident-2026-08-31-marstek-fleet-unreachable.md`). **Not written yet — investigation only, at Matos's instruction.**

This is very likely the root cause behind the long-running "D is always the problem" pattern: D at 3 % on 08-16, D at 14 % on 08-30, D's Backup Function dropping repeatedly, D triggering the 08-19 SoC-floor deadlock.

## The finding

All five of Venus D's **writable** registers read **0**. Venus E's read correctly, on the same integration.

| Register | Venus D | Venus E |
|---|---|---|
| `max_charge_power` | **0** | 2500 |
| `max_discharge_power` | **0** | 2500 |
| `set_charge_power` | **0** | 0 |
| `set_discharge_power` | **0** | 0 |
| `charge_to_soc` | **0** | — |

Every **read-only** sensor on D is fine — SoC, battery power, AC power, temperatures, energy counters, firmware strings all update normally. It is specifically the writable block.

## When

`max_charge_power` **2200 → 0** and `max_discharge_power` **2150 → 0** at the same moment, between **2026-08-25 01:22:49** (last good read) and **2026-08-26 05:34:21** (first 0). Both correct model-specific values before, both zero after, flat zero ever since. Nothing in between.

D's firmware did **not** change across that boundary: `V147.115.1177`, EMS `147`, BMS `1177` on both sides.

## It is not a real limit

D is physically charging at **1047 W right now** with `max_charge_power` reading 0. So the register is not throttling the hardware — it is a bad read of a register that HA also writes to.

## But D has effectively stopped working

| | Venus D | Venus E |
|---|---|---|
| Monthly discharge | **2.07 kWh** | 168.76 kWh |
| Today: charge / discharge | 0.7 / **0** | 192.62 / 163.46 |
| Lifetime discharge | 43.4 kWh | 353.78 kWh |

D has done roughly **1 %** of the fleet's discharge work this month.

## Why it matters — two silent failures

**1. The capability formula under-credits the fleet.** `sensor.marstek_discharge_capability` sums each unit's `max_discharge_power`. D therefore contributes **0 W**, so the Marstek-first calculation has treated the fleet as 2500 W, not 4650 W, since 08-26. This errs toward a *higher* Huawei cap, so it costs nothing directly — the Huawei simply does work D could have done. But D's 2.56 kWh is invisible to the entire controller.

**2. D's force-charge path may be a silent no-op — this is the serious one.** Four automations write to D's zeroed registers:

- `automation.battery_overnight_charge_decision_01_00` (`charge_to_soc`, `set_charge_power`)
- `automation.battery_overnight_charge_stop` (`set_charge_power`)
- `automation.force_grid_charge_start_both_batteries` (both)
- `automation.force_grid_charge_stop_and_return_to_normal` (`set_charge_power`)

Every Marstek write in the stack carries `continue_on_error`, so a failed write is silent by design. If D's writable block is unreachable, **every commanded charge of Venus D since 08-26 went nowhere and nothing said so.** That is the same dead-actuator class as the 2026-08-18 forcible-charge and 2026-08-19 EV incidents, for a third time.

It also explains the pattern directly: a pack that cannot be commanded to charge drifts down on its own, reaches the SoC floor, gets driven under the firmware's ~12 % backup reserve, and drops its Backup Function — which is exactly D's history and exactly the freezer-port problem.

## Leading hypothesis — a register-map / firmware mismatch

The two packs are on **different firmware branches**:

- **Venus D — `V147.115.1177`, EMS 147** (not updated)
- **Venus E — `V148.119.115`, EMS 148** (updated; the docs recorded `.113` earlier, and the peak-prep notes mention a manual firmware push on 08-30)

Same integration (`ViperRNMC/marstek_venus_modbus` **2026.6.4**, no pending update), same code path, opposite results. An integration release that moved the writable-register block to suit EMS 148 would break D and leave E working — and the 08-25/26 transition with no device-side firmware change fits an *integration* update, not a device one.

Not proven: HACS does not expose install dates here, so the 2026.6.4 install date could not be confirmed against the 08-25/26 window.

Ruled out: **nothing in Home Assistant wrote those zeros.** A config-body search across all automations, scripts, scenes and helpers finds no writer for `max_charge_power` or `max_discharge_power` on either unit — the only matches are reads (the capability template and the Discharge Cap Controller's description).

## Decisive test, not yet run

**Write 2150 to `number.utility_room_marstek_venus_d_max_discharge_power` and read it back.**

- Reads back **2150** → the register is writable; something zeroed it once and it is simply a value to restore. Cheap fix.
- Reads back **0** → the writable block is unreachable, the register-map hypothesis holds, and every commanded write to D has been going nowhere. Fix is a D firmware update to the 148 branch, or an integration version that supports EMS 147.

Either outcome is informative and the write is reversible.

## Related, worth noting

- `switch.*_rs485_control_mode` is **off on both units**. The overnight-charge sequence sets RS485 first (`RS485 → charge_to_soc → power → force_mode`, order matters). Both reading off between sessions is expected, but it is the other half of the command path and worth checking during the same test.
- The registry range for `max_discharge_power` is min 0 / max 2500 / step 50 on **both** units — the integration does not model D's lower 2150 W rating.
- Venus E firmware is now `V148.119.115`; `claude/energy-battery-architecture.md` still records `.113`.

## If confirmed, revisit

- The **C-rate imbalance** noted the same day: D is 2150 W on 2.56 kWh (**0.84 C**) against E's 2500 W on 5.12 kWh (**0.49 C**), so D drains 1.7× faster in relative terms and reaches the floor first — and the stand-down uses *either* unit, so D drags the whole fleet into manual with E still half full. Capping D at ~1250 W would equalise them. Only worth doing once D's registers actually accept writes.
- Whether `sensor.marstek_discharge_capability` should fall back to a **rated constant** per unit when `max_discharge_power` reads 0 but the unit is otherwise healthy — as written, a zeroed register and a genuinely stood-down pack are indistinguishable to the formula.
