# Offline backtest: dual-mom-btc-eth-v1

_Generated: 2026-09-05 23:34 UTC_

**RESEARCH ONLY — not enabled for paper/live. Hard-stop on FAIL (no paper/alerts/webhook).**

## Rules

- TF Daily | BTC+ETH book
- mom = total return over 20 closed days
- If max(BTC_mom, ETH_mom) ≤ 0 → flat (cash)
- Else allocate to argmax symbol (switch on bar close)
- Primary B&H: 50/50 BTC+ETH | Secondary: BTC-only B&H
- Gate on primary 50/50 ≥1.2×

## Common costs / sizing

| Parameter | Value |
|-----------|-------|
| Fee | 0.10% / side |
| Slippage | 5 bps adverse vs close |
| Size Mode A (**gate**) | **100% equity when in** (PASS/FAIL uses this only) |
| Size Mode B (**ops**) | **2.5% equity** (report only) |
| Close | full position |
| Mode | spot long-only, bar-close, no lookahead |
| Data | Binance Spot OHLCV via **ccxt** (owned cache) |

## Gate table (mandatory 6m Mode-A lead)

PASS iff **n>0** AND **Mode-A return ≥ 1.2 × B&H** (same window). WR informational only. Mode B = —.

| Strategy | Symbol | Mode | Size | 6m WR | 6m Mode-A ret | 6m B&H | ret/B&H | PASS/FAIL |
|----------|--------|------|------|-------|---------------|--------|---------|-----------|
| dual-mom-btc-eth-v1 | BTC+ETH | A (gate) | 100% | 53.85% | +23.68% | +23.78% | 0.995 | **FAIL** |
| dual-mom-btc-eth-v1 | BTC+ETH | B (ops) | 2.5% | 53.85% | +0.56% | +23.78% | — | — |

## Window: 6m

### BTC+ETH (6m) — A (gate) 100%

Bars: 182 (2026-03-08 → 2026-09-05 UTC)

| Metric | Value |
|--------|-------|
| Size | 100% equity |
| Trades | 13 |
| Wins / Losses | 7 / 6 |
| Win rate (info) | 53.85% |
| Strategy return | +23.68% |
| Buy & hold | +23.78% |
| ret / B&H | 0.995 |
| Max drawdown | 19.91% |
| Expectancy (USDT) | 182.1251 |
| Avg bars held | 9.5 |
| Gate (ret ≥ 1.2×B&H on 100%) | **FAIL** |
| Promotion | **HARD-STOP** — no paper/alerts/webhook |

<details><summary>Trades (first/last 8)</summary>

| # | Entry UTC | Exit UTC | Entry | Exit | PnL | % | Bars | Why |
|---|-----------|----------|-------|------|-----|---|------|-----|
| 1 | 2026-03-09 00:00 | 2026-03-11 00:00 | 68466.3761 | 70156.7641 | 226.4198 | 2.26% | 2 | switch |
| 2 | 2026-03-11 00:00 | 2026-03-29 00:00 | 2052.9960 | 1983.6477 | -365.1812 | -3.57% | 18 | flat |
| 3 | 2026-03-31 00:00 | 2026-04-02 00:00 | 2106.4827 | 2056.1414 | -254.8985 | -2.58% | 2 | flat |
| 4 | 2026-04-07 00:00 | 2026-04-20 00:00 | 2241.1300 | 2312.6931 | 286.9403 | 2.99% | 13 | switch |
| 5 | 2026-04-20 00:00 | 2026-05-16 00:00 | 75878.8905 | 78108.9760 | 270.4164 | 2.73% | 26 | flat |
| 6 | 2026-05-17 00:00 | 2026-05-21 00:00 | 77496.3988 | 77576.7122 | -9.7950 | -0.10% | 4 | flat |
| 7 | 2026-06-26 00:00 | 2026-06-27 00:00 | 1579.4693 | 1573.2030 | -60.4913 | -0.60% | 1 | flat |
| 8 | 2026-07-02 00:00 | 2026-07-05 00:00 | 1701.4203 | 1784.7572 | 473.2287 | 4.69% | 3 | flat |
| 9 | 2026-07-06 00:00 | 2026-08-03 00:00 | 1800.4598 | 1859.5698 | 325.1026 | 3.08% | 28 | flat |
| 10 | 2026-08-05 00:00 | 2026-08-10 00:00 | 1909.8545 | 1872.2234 | -235.9396 | -2.17% | 5 | flat |
| 11 | 2026-08-12 00:00 | 2026-08-15 00:00 | 1880.7499 | 1881.6987 | -15.9256 | -0.15% | 3 | flat |
| 12 | 2026-08-17 00:00 | 2026-08-19 00:00 | 64564.3660 | 69300.1226 | 757.6106 | 7.12% | 2 | switch |
| 13 | 2026-08-19 00:00 | 2026-09-05 00:00 | 2253.9264 | 2450.6741 | 970.1389 | 8.51% | 17 | eod |

</details>

### BTC+ETH (6m) — B (ops) 2.5%

Bars: 182 (2026-03-08 → 2026-09-05 UTC)

| Metric | Value |
|--------|-------|
| Size | 2.5% equity |
| Trades | 13 |
| Wins / Losses | 7 / 6 |
| Win rate (info) | 53.85% |
| Strategy return | +0.56% |
| Buy & hold | +23.78% |
| ret / B&H | 0.023 |
| Max drawdown | 0.57% |
| Expectancy (USDT) | 4.2841 |
| Avg bars held | 9.5 |
| Gate | — (ops only; not scored) |

## Window: full(~2y)

### BTC+ETH (full(~2y)) — A (gate) 100%

Bars: 730 (2024-09-06 → 2026-09-05 UTC)

| Metric | Value |
|--------|-------|
| Size | 100% equity |
| Trades | 70 |
| Wins / Losses | 29 / 41 |
| Win rate (info) | 41.43% |
| Strategy return | +101.78% |
| Buy & hold | +29.05% |
| ret / B&H | 3.503 |
| Max drawdown | 39.06% |
| Expectancy (USDT) | 145.3961 |
| Avg bars held | 6.3 |
| Gate (ret ≥ 1.2×B&H on 100%) | **PASS** |

<details><summary>Trades (first/last 8)</summary>

| # | Entry UTC | Exit UTC | Entry | Exit | PnL | % | Bars | Why |
|---|-----------|----------|-------|------|-----|---|------|-----|
| 1 | 2024-09-17 00:00 | 2024-10-07 00:00 | 60344.1470 | 62192.8880 | 285.7741 | 2.86% | 20 | switch |
| 2 | 2024-10-07 00:00 | 2024-10-09 00:00 | 2423.9214 | 2369.2848 | -251.9351 | -2.45% | 2 | flat |
| 3 | 2024-10-14 00:00 | 2024-11-09 00:00 | 66117.0320 | 76639.1213 | 1573.5812 | 15.68% | 26 | switch |
| 4 | 2024-11-09 00:00 | 2024-11-11 00:00 | 3127.7731 | 3369.9042 | 873.5812 | 7.53% | 2 | switch |
| 5 | 2024-11-11 00:00 | 2024-11-25 00:00 | 88692.3140 | 92963.5050 | 574.9146 | 4.61% | 14 | switch |
| 6 | 2024-11-25 00:00 | 2024-11-27 00:00 | 3416.1972 | 3651.4534 | 871.2123 | 6.67% | 2 | switch |
| 7 | 2024-11-27 00:00 | 2024-12-01 00:00 | 95911.0416 | 97136.5874 | 149.7781 | 1.08% | 4 | switch |
| 8 | 2024-12-01 00:00 | 2024-12-17 00:00 | 3709.4638 | 3891.0635 | 659.6433 | 4.69% | 16 | switch |
| 63 | 2026-05-17 00:00 | 2026-05-21 00:00 | 77496.3988 | 77576.7122 | -15.9805 | -0.10% | 4 | flat |
| 64 | 2026-06-26 00:00 | 2026-06-27 00:00 | 1579.4693 | 1573.2030 | -98.6913 | -0.60% | 1 | flat |
| 65 | 2026-07-02 00:00 | 2026-07-05 00:00 | 1701.4203 | 1784.7572 | 772.0705 | 4.69% | 3 | flat |
| 66 | 2026-07-06 00:00 | 2026-08-03 00:00 | 1800.4598 | 1859.5698 | 530.4035 | 3.08% | 28 | flat |
| 67 | 2026-08-05 00:00 | 2026-08-10 00:00 | 1909.8545 | 1872.2234 | -384.9344 | -2.17% | 5 | flat |
| 68 | 2026-08-12 00:00 | 2026-08-15 00:00 | 1880.7499 | 1881.6987 | -25.9825 | -0.15% | 3 | flat |
| 69 | 2026-08-17 00:00 | 2026-08-19 00:00 | 64564.3660 | 69300.1226 | 1236.0384 | 7.12% | 2 | switch |
| 70 | 2026-08-19 00:00 | 2026-09-05 00:00 | 2253.9264 | 2450.6741 | 1582.7773 | 8.51% | 17 | eod |

</details>

### BTC+ETH (full(~2y)) — B (ops) 2.5%

Bars: 730 (2024-09-06 → 2026-09-05 UTC)

| Metric | Value |
|--------|-------|
| Size | 2.5% equity |
| Trades | 70 |
| Wins / Losses | 29 / 41 |
| Win rate (info) | 41.43% |
| Strategy return | +2.36% |
| Buy & hold | +29.05% |
| ret / B&H | 0.081 |
| Max drawdown | 1.38% |
| Expectancy (USDT) | 3.3769 |
| Avg bars held | 6.3 |
| Gate | — (ops only; not scored) |

## Caveats

- Warmup on longer history; entries only inside each window.
- Thresholds fixed a priori — **not tuned on the 6m window**.
- Gate PASS/FAIL only on Mode A (100%-when-in); Mode B ops parallel.
- Does not change live/paper bot defaults.
- Fresh Path B IDs — not Jewel / open-proxy / ADX-RSI-EMA-MTF / #13.
- Gate uses primary 50/50 B&H; secondary BTC-only in notes.

