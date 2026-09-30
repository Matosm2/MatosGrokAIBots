# stage16-dual-sol-bnb-v1 scoreboard (BTC LEAD PRIMARY + Denser n >> 9 without stage12/15 over-damp)

Generated (UTC): 2026-09-18T04:40:57.869725+00:00

**RESEARCH ONLY — not paper/live. No Claude/TV. No Jewel. No remakes / burned grafts.**

## Scoring Criteria

- **LEAD gate:** last-6m Mode-A return >= **1.2×** B&H (same window) with n > 5 on BTC -> `PASS_6m Y/N`. WR informational.
- **TINY-N POLICY:** BTC Mode-A n <= 5 on 6m -> FAIL cell even if xB&H >= 1.2 (over-gated / under-specified). Also flag n in [6..10] as thin.
- **Also reported:** full(~2y) Mode-A + ops **2.5%** sizing.
- **Costs:** 0.10%/side fee + 5 bps slip adverse; Mode-A **100%** equity.
- **Stop-ladder:** BTC first; PASS_6m -> ETH (HARD) -> SOL (HARD) -> BNB (HARD).
- **Dual-Survival Constraint:** Identical parameter sets across BTC, ETH, SOL, and BNB (strictly no per-coin retuning).
- **BTC LEAD PRIMARY Bias:** Dense non-damped cycle/structure signals designed to clear BTC first without stage12/15 over-damp collapse.
- **BTC->ETH Portability:** Keep portability without regressing to stage13 REI wipe.
- **BNB-Survival (CRITICAL):** Withstand quieter BNB regime without quiet wipe (TTF lesson).
- **Mandatory Smoke & Retention Tests:** btc_smoke, eth_smoke, sol_smoke, and bnb_smoke logged; retention_notes checked across ladder.
- **Closed-bar only;** long-only first pass; pyramiding 0.
- **Hard excludes honored** (no stage1-15 IDs, no Spearman/UO2025/CorrCycle/NET/DVI, no TTF/PFE/ASH/APZ/Nadaraya, no REI/PZO/TMO/RF/CLV, no CSI/PMO/Gaussian/US damp, no Roofing, etc.).

## Parameter Locks Summary (LOCKED BEFORE SCORING)

- **Ehlers BandPass (`ehlers-bandpass-zero`):** IIR BandPass zero-cross. (P=20, d=0.3) preferred; (P=14, d=0.3), (P=28, d=0.3). Mode A BP x 0; Mode B quality hold.
- **Two-Pole HighPass (`ehlers-twopole-hp-zero`):** Single 2-pole HP zero-cross. P=40 preferred; P=28, P=48. Mode A HP x 0; Mode B quality hold. Single HP only — no SS after.
- **Three Line Break (`three-line-break-flip`):** Close-only structure flip. N=3 preferred; N=2, N=4. Mode A structure flip; Mode B N=4.
- **Wilder Swing Index (`wilder-swing-index-zero`):** Raw SI zero-cross with ATR proxy. atr14 preferred; atr10, atr20. Mode A raw SI x 0; Mode B quality hold. NOT ASI dual-break.
- **Nison Kagi (`nison-kagi-yang-yin-flip`):** Kagi Yang/Yin reversal structure flip. ATR*1.0 preferred; ATR*0.75, ATR*1.5. Mode A Yin->Yang entry / Yang->Yin exit; Mode B ATR*1.5.

## PASS_6m cells (LEAD)

- `[BTCUSDT] nison-kagi-yang-yin-flip` @ `4h` (mode_a|(atr1.5)) [btc_smoke=Y, eth_smoke=Y, sol_smoke=Y, bnb_smoke=Y, retention=—]: 6m ret=12.16% bh=10.12% ratio=1.202x wr=36.4% n=11 | full=FAIL ratio=0.676x n=39
- `[ETHUSDT] nison-kagi-yang-yin-flip` @ `4h` (mode_a|(atr1.5)) [btc_smoke=Y, eth_smoke=Y, sol_smoke=Y, bnb_smoke=Y, retention=OK (ETH n=7 vs BTC n=11)]: 6m ret=33.15% bh=15.80% ratio=2.099x wr=42.9% n=7 | full=PASS ratio=7.868x n=37

## All Scored Cells by Strategy

### `ehlers-bandpass-zero`

| Symbol | Strategy ID | TF | Params | BTC Smoke | ETH Smoke | SOL Smoke | BNB Smoke | Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `BTCUSDT` | `ehlers-bandpass-zero` | `1h` | `mode_a|(P20,d0.3)` | `Y` | `Y` | `Y` | `Y` | `—` | 215 | 29.3% | -54.78% | +11.37% | -4.817× | FAIL | 838 | 30.0% | -91.47% | +26.94% | -3.395× | FAIL | -1.92% | -5.75% | — |
| `BTCUSDT` | `ehlers-bandpass-zero` | `1h` | `mode_a|(P14,d0.3)` | `Y` | `Y` | `Y` | `Y` | `—` | 304 | 27.0% | -64.79% | +11.37% | -5.697× | FAIL | 1212 | 28.9% | -97.80% | +26.94% | -3.630× | FAIL | -2.53% | -8.90% | — |
| `BTCUSDT` | `ehlers-bandpass-zero` | `1h` | `mode_a|(P28,d0.3)` | `Y` | `Y` | `Y` | `Y` | `—` | 157 | 31.8% | -32.20% | +11.37% | -2.832× | FAIL | 615 | 32.5% | -80.68% | +26.94% | -2.994× | FAIL | -0.93% | -3.81% | — |
| `BTCUSDT` | `ehlers-bandpass-zero` | `1h` | `mode_b|(P20,d0.3)` | `Y` | `Y` | `Y` | `Y` | `—` | 215 | 29.3% | -54.78% | +11.37% | -4.817× | FAIL | 838 | 30.0% | -91.47% | +26.94% | -3.395× | FAIL | -1.92% | -5.75% | — |
| `BTCUSDT` | `ehlers-bandpass-zero` | `4h` | `mode_a|(P20,d0.3)` | `Y` | `Y` | `Y` | `Y` | `—` | 52 | 46.2% | +2.27% | +10.12% | 0.224× | FAIL | 207 | 38.6% | -40.98% | +28.30% | -1.448× | FAIL | +0.09% | -1.11% | — |
| `BTCUSDT` | `ehlers-bandpass-zero` | `4h` | `mode_a|(P14,d0.3)` | `Y` | `Y` | `Y` | `Y` | `—` | 72 | 36.1% | -12.37% | +10.12% | -1.222× | FAIL | 298 | 35.6% | -65.73% | +28.30% | -2.322× | FAIL | -0.29% | -2.41% | — |
| `BTCUSDT` | `ehlers-bandpass-zero` | `4h` | `mode_a|(P28,d0.3)` | `Y` | `Y` | `Y` | `Y` | `—` | 39 | 33.3% | -10.00% | +10.12% | -0.988× | FAIL | 151 | 37.7% | -2.84% | +28.30% | -0.100× | FAIL | -0.20% | +0.16% | — |
| `BTCUSDT` | `ehlers-bandpass-zero` | `4h` | `mode_b|(P20,d0.3)` | `Y` | `Y` | `Y` | `Y` | `—` | 52 | 46.2% | +2.27% | +10.12% | 0.224× | FAIL | 207 | 38.6% | -40.98% | +28.30% | -1.448× | FAIL | +0.09% | -1.11% | — |
| `ETHUSDT` | `ehlers-bandpass-zero` | `1h` | `mode_a|(P20,d0.3)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `ehlers-bandpass-zero` | `1h` | `mode_a|(P14,d0.3)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `ehlers-bandpass-zero` | `1h` | `mode_a|(P28,d0.3)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `ehlers-bandpass-zero` | `1h` | `mode_b|(P20,d0.3)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `ehlers-bandpass-zero` | `4h` | `mode_a|(P20,d0.3)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `ehlers-bandpass-zero` | `4h` | `mode_a|(P14,d0.3)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `ehlers-bandpass-zero` | `4h` | `mode_a|(P28,d0.3)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `ehlers-bandpass-zero` | `4h` | `mode_b|(P20,d0.3)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `SOLUSDT` | `ehlers-bandpass-zero` | `1h` | `mode_a|(P20,d0.3)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `ehlers-bandpass-zero` | `1h` | `mode_a|(P14,d0.3)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `ehlers-bandpass-zero` | `1h` | `mode_a|(P28,d0.3)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `ehlers-bandpass-zero` | `1h` | `mode_b|(P20,d0.3)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `ehlers-bandpass-zero` | `4h` | `mode_a|(P20,d0.3)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `ehlers-bandpass-zero` | `4h` | `mode_a|(P14,d0.3)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `ehlers-bandpass-zero` | `4h` | `mode_a|(P28,d0.3)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `ehlers-bandpass-zero` | `4h` | `mode_b|(P20,d0.3)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `BNBUSDT` | `ehlers-bandpass-zero` | `1h` | `mode_a|(P20,d0.3)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `ehlers-bandpass-zero` | `1h` | `mode_a|(P14,d0.3)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `ehlers-bandpass-zero` | `1h` | `mode_a|(P28,d0.3)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `ehlers-bandpass-zero` | `1h` | `mode_b|(P20,d0.3)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `ehlers-bandpass-zero` | `4h` | `mode_a|(P20,d0.3)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `ehlers-bandpass-zero` | `4h` | `mode_a|(P14,d0.3)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `ehlers-bandpass-zero` | `4h` | `mode_a|(P28,d0.3)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `ehlers-bandpass-zero` | `4h` | `mode_b|(P20,d0.3)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |

### `ehlers-twopole-hp-zero`

| Symbol | Strategy ID | TF | Params | BTC Smoke | ETH Smoke | SOL Smoke | BNB Smoke | Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `BTCUSDT` | `ehlers-twopole-hp-zero` | `1h` | `mode_a|(P40)` | `Y` | `Y` | `Y` | `Y` | `—` | 441 | 20.6% | -75.62% | +11.37% | -6.650× | FAIL | 1732 | 21.5% | -99.35% | +26.94% | -3.687× | FAIL | -3.42% | -11.61% | — |
| `BTCUSDT` | `ehlers-twopole-hp-zero` | `1h` | `mode_a|(P28)` | `Y` | `Y` | `Y` | `Y` | `—` | 528 | 20.6% | -80.14% | +11.37% | -7.048× | FAIL | 2084 | 22.2% | -99.83% | +26.94% | -3.705× | FAIL | -3.91% | -14.49% | — |
| `BTCUSDT` | `ehlers-twopole-hp-zero` | `1h` | `mode_a|(P48)` | `Y` | `Y` | `Y` | `Y` | `—` | 394 | 21.3% | -71.58% | +11.37% | -6.295× | FAIL | 1555 | 21.7% | -98.83% | +26.94% | -3.668× | FAIL | -3.05% | -10.31% | — |
| `BTCUSDT` | `ehlers-twopole-hp-zero` | `1h` | `mode_b|(P40)` | `Y` | `Y` | `Y` | `Y` | `—` | 441 | 20.6% | -75.62% | +11.37% | -6.650× | FAIL | 1732 | 21.5% | -99.35% | +26.94% | -3.687× | FAIL | -3.42% | -11.61% | — |
| `BTCUSDT` | `ehlers-twopole-hp-zero` | `4h` | `mode_a|(P40)` | `Y` | `Y` | `Y` | `Y` | `—` | 100 | 29.0% | -24.74% | +10.12% | -2.444× | FAIL | 402 | 29.9% | -66.34% | +28.30% | -2.344× | FAIL | -0.66% | -2.46% | — |
| `BTCUSDT` | `ehlers-twopole-hp-zero` | `4h` | `mode_a|(P28)` | `Y` | `Y` | `Y` | `Y` | `—` | 116 | 31.0% | -22.76% | +10.12% | -2.249× | FAIL | 494 | 29.1% | -76.31% | +28.30% | -2.696× | FAIL | -0.60% | -3.32% | — |
| `BTCUSDT` | `ehlers-twopole-hp-zero` | `4h` | `mode_a|(P48)` | `Y` | `Y` | `Y` | `Y` | `—` | 93 | 28.0% | -27.20% | +10.12% | -2.688× | FAIL | 360 | 30.0% | -60.17% | +28.30% | -2.126× | FAIL | -0.75% | -2.07% | — |
| `BTCUSDT` | `ehlers-twopole-hp-zero` | `4h` | `mode_b|(P40)` | `Y` | `Y` | `Y` | `Y` | `—` | 100 | 29.0% | -24.74% | +10.12% | -2.444× | FAIL | 402 | 29.9% | -66.34% | +28.30% | -2.344× | FAIL | -0.66% | -2.46% | — |
| `ETHUSDT` | `ehlers-twopole-hp-zero` | `1h` | `mode_a|(P40)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `ehlers-twopole-hp-zero` | `1h` | `mode_a|(P28)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `ehlers-twopole-hp-zero` | `1h` | `mode_a|(P48)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `ehlers-twopole-hp-zero` | `1h` | `mode_b|(P40)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `ehlers-twopole-hp-zero` | `4h` | `mode_a|(P40)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `ehlers-twopole-hp-zero` | `4h` | `mode_a|(P28)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `ehlers-twopole-hp-zero` | `4h` | `mode_a|(P48)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `ehlers-twopole-hp-zero` | `4h` | `mode_b|(P40)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `SOLUSDT` | `ehlers-twopole-hp-zero` | `1h` | `mode_a|(P40)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `ehlers-twopole-hp-zero` | `1h` | `mode_a|(P28)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `ehlers-twopole-hp-zero` | `1h` | `mode_a|(P48)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `ehlers-twopole-hp-zero` | `1h` | `mode_b|(P40)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `ehlers-twopole-hp-zero` | `4h` | `mode_a|(P40)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `ehlers-twopole-hp-zero` | `4h` | `mode_a|(P28)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `ehlers-twopole-hp-zero` | `4h` | `mode_a|(P48)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `ehlers-twopole-hp-zero` | `4h` | `mode_b|(P40)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `BNBUSDT` | `ehlers-twopole-hp-zero` | `1h` | `mode_a|(P40)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `ehlers-twopole-hp-zero` | `1h` | `mode_a|(P28)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `ehlers-twopole-hp-zero` | `1h` | `mode_a|(P48)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `ehlers-twopole-hp-zero` | `1h` | `mode_b|(P40)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `ehlers-twopole-hp-zero` | `4h` | `mode_a|(P40)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `ehlers-twopole-hp-zero` | `4h` | `mode_a|(P28)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `ehlers-twopole-hp-zero` | `4h` | `mode_a|(P48)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `ehlers-twopole-hp-zero` | `4h` | `mode_b|(P40)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |

### `three-line-break-flip`

| Symbol | Strategy ID | TF | Params | BTC Smoke | ETH Smoke | SOL Smoke | BNB Smoke | Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `BTCUSDT` | `three-line-break-flip` | `1h` | `mode_a|(N3)` | `Y` | `Y` | `Y` | `Y` | `—` | 106 | 27.4% | -24.28% | +11.37% | -2.135× | FAIL | 421 | 31.1% | -74.73% | +26.94% | -2.773× | FAIL | -0.61% | -3.14% | — |
| `BTCUSDT` | `three-line-break-flip` | `1h` | `mode_a|(N2)` | `Y` | `Y` | `Y` | `Y` | `—` | 206 | 24.3% | -42.29% | +11.37% | -3.719× | FAIL | 853 | 25.4% | -94.96% | +26.94% | -3.524× | FAIL | -1.28% | -6.95% | — |
| `BTCUSDT` | `three-line-break-flip` | `1h` | `mode_a|(N4)` | `Y` | `Y` | `Y` | `Y` | `—` | 62 | 32.3% | -17.01% | +11.37% | -1.496× | FAIL | 233 | 35.6% | -39.11% | +26.94% | -1.451× | FAIL | -0.39% | -0.98% | — |
| `BTCUSDT` | `three-line-break-flip` | `1h` | `mode_b|(N3)` | `Y` | `Y` | `Y` | `Y` | `—` | 106 | 27.4% | -24.28% | +11.37% | -2.135× | FAIL | 421 | 31.1% | -74.73% | +26.94% | -2.773× | FAIL | -0.61% | -3.14% | — |
| `BTCUSDT` | `three-line-break-flip` | `4h` | `mode_a|(N3)` | `Y` | `Y` | `Y` | `Y` | `—` | 32 | 28.1% | -10.76% | +10.12% | -1.063× | FAIL | 104 | 33.7% | -15.39% | +28.30% | -0.544× | FAIL | -0.22% | -0.11% | — |
| `BTCUSDT` | `three-line-break-flip` | `4h` | `mode_a|(N2)` | `Y` | `Y` | `Y` | `Y` | `—` | 62 | 32.3% | -18.15% | +10.12% | -1.794× | FAIL | 234 | 30.3% | -45.48% | +28.30% | -1.607× | FAIL | -0.44% | -1.25% | — |
| `BTCUSDT` | `three-line-break-flip` | `4h` | `mode_a|(N4)` | `Y` | `Y` | `Y` | `Y` | `—` | 12 | 41.7% | +9.77% | +10.12% | 0.965× | FAIL | 52 | 46.2% | -7.79% | +28.30% | -0.275× | FAIL | +0.28% | +0.12% | Near-miss 6m (0.96x B&H) |
| `BTCUSDT` | `three-line-break-flip` | `4h` | `mode_b|(N3)` | `Y` | `Y` | `Y` | `Y` | `—` | 32 | 28.1% | -10.76% | +10.12% | -1.063× | FAIL | 104 | 33.7% | -15.39% | +28.30% | -0.544× | FAIL | -0.22% | -0.11% | — |
| `ETHUSDT` | `three-line-break-flip` | `1h` | `mode_a|(N3)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `three-line-break-flip` | `1h` | `mode_a|(N2)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `three-line-break-flip` | `1h` | `mode_a|(N4)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `three-line-break-flip` | `1h` | `mode_b|(N3)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `three-line-break-flip` | `4h` | `mode_a|(N3)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `three-line-break-flip` | `4h` | `mode_a|(N2)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `three-line-break-flip` | `4h` | `mode_a|(N4)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `three-line-break-flip` | `4h` | `mode_b|(N3)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `SOLUSDT` | `three-line-break-flip` | `1h` | `mode_a|(N3)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `three-line-break-flip` | `1h` | `mode_a|(N2)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `three-line-break-flip` | `1h` | `mode_a|(N4)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `three-line-break-flip` | `1h` | `mode_b|(N3)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `three-line-break-flip` | `4h` | `mode_a|(N3)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `three-line-break-flip` | `4h` | `mode_a|(N2)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `three-line-break-flip` | `4h` | `mode_a|(N4)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `three-line-break-flip` | `4h` | `mode_b|(N3)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `BNBUSDT` | `three-line-break-flip` | `1h` | `mode_a|(N3)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `three-line-break-flip` | `1h` | `mode_a|(N2)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `three-line-break-flip` | `1h` | `mode_a|(N4)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `three-line-break-flip` | `1h` | `mode_b|(N3)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `three-line-break-flip` | `4h` | `mode_a|(N3)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `three-line-break-flip` | `4h` | `mode_a|(N2)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `three-line-break-flip` | `4h` | `mode_a|(N4)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `three-line-break-flip` | `4h` | `mode_b|(N3)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |

### `wilder-swing-index-zero`

| Symbol | Strategy ID | TF | Params | BTC Smoke | ETH Smoke | SOL Smoke | BNB Smoke | Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `BTCUSDT` | `wilder-swing-index-zero` | `1h` | `mode_a|(atr14)` | `Y` | `Y` | `Y` | `Y` | `—` | 995 | 17.9% | -93.93% | +11.37% | -8.260× | FAIL | 4059 | 18.1% | -99.85% | +26.94% | -3.706× | FAIL | -6.72% | -26.13% | — |
| `BTCUSDT` | `wilder-swing-index-zero` | `1h` | `mode_a|(atr10)` | `Y` | `Y` | `Y` | `Y` | `—` | 995 | 17.9% | -93.93% | +11.37% | -8.260× | FAIL | 4059 | 18.1% | -99.85% | +26.94% | -3.706× | FAIL | -6.72% | -26.13% | — |
| `BTCUSDT` | `wilder-swing-index-zero` | `1h` | `mode_a|(atr20)` | `Y` | `Y` | `Y` | `Y` | `—` | 995 | 17.9% | -93.93% | +11.37% | -8.260× | FAIL | 4059 | 18.1% | -99.85% | +26.94% | -3.706× | FAIL | -6.72% | -26.13% | — |
| `BTCUSDT` | `wilder-swing-index-zero` | `1h` | `mode_b|(atr14)` | `Y` | `Y` | `Y` | `Y` | `—` | 995 | 17.9% | -93.93% | +11.37% | -8.260× | FAIL | 4059 | 18.1% | -99.85% | +26.94% | -3.706× | FAIL | -6.72% | -26.13% | — |
| `BTCUSDT` | `wilder-swing-index-zero` | `4h` | `mode_a|(atr14)` | `Y` | `Y` | `Y` | `Y` | `—` | 260 | 22.3% | -56.28% | +10.12% | -5.561× | FAIL | 1034 | 25.9% | -95.41% | +28.30% | -3.371× | FAIL | -1.98% | -7.24% | — |
| `BTCUSDT` | `wilder-swing-index-zero` | `4h` | `mode_a|(atr10)` | `Y` | `Y` | `Y` | `Y` | `—` | 260 | 22.3% | -56.28% | +10.12% | -5.561× | FAIL | 1034 | 25.9% | -95.41% | +28.30% | -3.371× | FAIL | -1.98% | -7.24% | — |
| `BTCUSDT` | `wilder-swing-index-zero` | `4h` | `mode_a|(atr20)` | `Y` | `Y` | `Y` | `Y` | `—` | 260 | 22.3% | -56.28% | +10.12% | -5.561× | FAIL | 1034 | 25.9% | -95.41% | +28.30% | -3.371× | FAIL | -1.98% | -7.24% | — |
| `BTCUSDT` | `wilder-swing-index-zero` | `4h` | `mode_b|(atr14)` | `Y` | `Y` | `Y` | `Y` | `—` | 260 | 22.3% | -56.28% | +10.12% | -5.561× | FAIL | 1034 | 25.9% | -95.41% | +28.30% | -3.371× | FAIL | -1.98% | -7.24% | — |
| `ETHUSDT` | `wilder-swing-index-zero` | `1h` | `mode_a|(atr14)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `wilder-swing-index-zero` | `1h` | `mode_a|(atr10)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `wilder-swing-index-zero` | `1h` | `mode_a|(atr20)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `wilder-swing-index-zero` | `1h` | `mode_b|(atr14)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `wilder-swing-index-zero` | `4h` | `mode_a|(atr14)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `wilder-swing-index-zero` | `4h` | `mode_a|(atr10)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `wilder-swing-index-zero` | `4h` | `mode_a|(atr20)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `wilder-swing-index-zero` | `4h` | `mode_b|(atr14)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `SOLUSDT` | `wilder-swing-index-zero` | `1h` | `mode_a|(atr14)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `wilder-swing-index-zero` | `1h` | `mode_a|(atr10)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `wilder-swing-index-zero` | `1h` | `mode_a|(atr20)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `wilder-swing-index-zero` | `1h` | `mode_b|(atr14)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `wilder-swing-index-zero` | `4h` | `mode_a|(atr14)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `wilder-swing-index-zero` | `4h` | `mode_a|(atr10)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `wilder-swing-index-zero` | `4h` | `mode_a|(atr20)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `wilder-swing-index-zero` | `4h` | `mode_b|(atr14)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `BNBUSDT` | `wilder-swing-index-zero` | `1h` | `mode_a|(atr14)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `wilder-swing-index-zero` | `1h` | `mode_a|(atr10)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `wilder-swing-index-zero` | `1h` | `mode_a|(atr20)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `wilder-swing-index-zero` | `1h` | `mode_b|(atr14)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `wilder-swing-index-zero` | `4h` | `mode_a|(atr14)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `wilder-swing-index-zero` | `4h` | `mode_a|(atr10)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `wilder-swing-index-zero` | `4h` | `mode_a|(atr20)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `wilder-swing-index-zero` | `4h` | `mode_b|(atr14)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |

### `nison-kagi-yang-yin-flip`

| Symbol | Strategy ID | TF | Params | BTC Smoke | ETH Smoke | SOL Smoke | BNB Smoke | Retention | n (6m) | WR (6m) | Ret (6m) | B&H (6m) | Ratio (6m) | PASS_6m | n (full) | WR (full) | Ret (full) | B&H (full) | Ratio (full) | PASS_full | Ops Ret (6m) | Ops Ret (full) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `BTCUSDT` | `nison-kagi-yang-yin-flip` | `1h` | `mode_a|(atr1.0)` | `Y` | `Y` | `Y` | `Y` | `—` | 61 | 36.1% | +10.03% | +11.37% | 0.882× | FAIL | 261 | 34.9% | -15.60% | +26.94% | -0.579× | FAIL | +0.30% | -0.15% | — |
| `BTCUSDT` | `nison-kagi-yang-yin-flip` | `1h` | `mode_a|(atr0.75)` | `Y` | `Y` | `Y` | `Y` | `—` | 80 | 32.5% | +3.60% | +11.37% | 0.317× | FAIL | 359 | 31.8% | -27.43% | +26.94% | -1.018× | FAIL | +0.13% | -0.54% | — |
| `BTCUSDT` | `nison-kagi-yang-yin-flip` | `1h` | `mode_a|(atr1.5)` | `Y` | `Y` | `Y` | `Y` | `—` | 45 | 33.3% | -3.49% | +11.37% | -0.307× | FAIL | 176 | 31.8% | -28.81% | +26.94% | -1.069× | FAIL | -0.02% | -0.57% | — |
| `BTCUSDT` | `nison-kagi-yang-yin-flip` | `1h` | `mode_b|(atr1.0)` | `Y` | `Y` | `Y` | `Y` | `—` | 61 | 36.1% | +10.03% | +11.37% | 0.882× | FAIL | 261 | 34.9% | -15.60% | +26.94% | -0.579× | FAIL | +0.30% | -0.15% | — |
| `BTCUSDT` | `nison-kagi-yang-yin-flip` | `4h` | `mode_a|(atr1.0)` | `Y` | `Y` | `Y` | `Y` | `—` | 17 | 35.3% | +6.88% | +10.12% | 0.680× | FAIL | 65 | 35.4% | -16.92% | +28.30% | -0.598× | FAIL | +0.24% | -0.19% | — |
| `BTCUSDT` | `nison-kagi-yang-yin-flip` | `4h` | `mode_a|(atr0.75)` | `Y` | `Y` | `Y` | `Y` | `—` | 23 | 30.4% | -3.50% | +10.12% | -0.346× | FAIL | 88 | 33.0% | -22.49% | +28.30% | -0.795× | FAIL | -0.02% | -0.34% | — |
| `BTCUSDT` | `nison-kagi-yang-yin-flip` | `4h` | `mode_a|(atr1.5)` | `Y` | `Y` | `Y` | `Y` | `—` | 11 | 36.4% | +12.16% | +10.12% | 1.202× | **PASS** | 39 | 38.5% | +19.12% | +28.30% | 0.676× | FAIL | +0.36% | +0.81% | — |
| `BTCUSDT` | `nison-kagi-yang-yin-flip` | `4h` | `mode_b|(atr1.0)` | `Y` | `Y` | `Y` | `Y` | `—` | 17 | 35.3% | +6.88% | +10.12% | 0.680× | FAIL | 65 | 35.4% | -16.92% | +28.30% | -0.598× | FAIL | +0.24% | -0.19% | — |
| `ETHUSDT` | `nison-kagi-yang-yin-flip` | `1h` | `mode_a|(atr1.0)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `nison-kagi-yang-yin-flip` | `1h` | `mode_a|(atr0.75)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `nison-kagi-yang-yin-flip` | `1h` | `mode_a|(atr1.5)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `nison-kagi-yang-yin-flip` | `1h` | `mode_b|(atr1.0)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `nison-kagi-yang-yin-flip` | `4h` | `mode_a|(atr1.0)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `nison-kagi-yang-yin-flip` | `4h` | `mode_a|(atr0.75)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `nison-kagi-yang-yin-flip` | `4h` | `mode_b|(atr1.0)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (BTC PASS_6m required) |
| `ETHUSDT` | `nison-kagi-yang-yin-flip` | `4h` | `mode_a|(atr1.5)` | `Y` | `Y` | `Y` | `Y` | `OK (ETH n=7 vs BTC n=11)` | 7 | 42.9% | +33.15% | +15.80% | 2.099× | **PASS** | 37 | 37.8% | +46.25% | +5.88% | 7.868× | **PASS** | +0.82% | +1.59% | ETH hard filter |
| `SOLUSDT` | `nison-kagi-yang-yin-flip` | `1h` | `mode_a|(atr1.0)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `nison-kagi-yang-yin-flip` | `1h` | `mode_a|(atr0.75)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `nison-kagi-yang-yin-flip` | `1h` | `mode_a|(atr1.5)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `nison-kagi-yang-yin-flip` | `1h` | `mode_b|(atr1.0)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `nison-kagi-yang-yin-flip` | `4h` | `mode_a|(atr1.0)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `nison-kagi-yang-yin-flip` | `4h` | `mode_a|(atr0.75)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `nison-kagi-yang-yin-flip` | `4h` | `mode_b|(atr1.0)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (ETH PASS_6m required) |
| `SOLUSDT` | `nison-kagi-yang-yin-flip` | `4h` | `mode_a|(atr1.5)` | `Y` | `Y` | `Y` | `Y` | `OK (SOL n=11 vs ETH n=7)` | 11 | 27.3% | +14.44% | +17.89% | 0.807× | FAIL | 38 | 34.2% | -18.69% | -20.49% | 0.088× | FAIL | +0.46% | +0.08% | SOL hard filter |
| `BNBUSDT` | `nison-kagi-yang-yin-flip` | `1h` | `mode_a|(atr1.0)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `nison-kagi-yang-yin-flip` | `1h` | `mode_a|(atr0.75)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `nison-kagi-yang-yin-flip` | `1h` | `mode_a|(atr1.5)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `nison-kagi-yang-yin-flip` | `1h` | `mode_b|(atr1.0)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `nison-kagi-yang-yin-flip` | `4h` | `mode_a|(atr1.0)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `nison-kagi-yang-yin-flip` | `4h` | `mode_a|(atr0.75)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `nison-kagi-yang-yin-flip` | `4h` | `mode_a|(atr1.5)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |
| `BNBUSDT` | `nison-kagi-yang-yin-flip` | `4h` | `mode_b|(atr1.0)` | `Y` | `Y` | `Y` | `Y` | `—` | — | — | — | — | — | FAIL | — | — | — | — | — | FAIL | — | — | Pruned by stop-ladder (SOL PASS_6m required) |

