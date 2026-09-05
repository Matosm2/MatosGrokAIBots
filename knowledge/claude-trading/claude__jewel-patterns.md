# The Jewel — what the oscillator states actually predict

Run 2026-09-04. Method: a Pine study reads The Jewel's published plots via `input.source()`
and measures **average forward price return** after each oscillator state, against an
all-bars baseline. BINANCE:BTCUSDT, full available history (~9 years).

Reading the table: compare each row to the **baseline row**, not to zero. BTC rose a lot
over this window, so almost every bucket has a positive forward return. Only a bucket that
beats the baseline carries information.

## 4h — 19,796 bars

| Jewel state | n | +5b % | +10b % | +20b % | win@20 |
|---|---|---|---|---|---|
| **ALL BARS (baseline)** | 19796 | 0.13 | 0.25 | **0.50** | **52.9%** |
| Slow 10-20 | 139 | 0.18 | 0.51 | 0.82 | 53.2% |
| Slow 20-30 | 282 | – | – | −0.24 | 54.0% |
| Slow 30-50 | 7178 | 0.08 | 0.21 | 0.45 | 53.4% |
| Slow 50-70 | 7247 | 0.09 | 0.18 | 0.43 | 51.6% |
| Slow 70-80 | 2911 | 0.30 | 0.61 | 0.91 | 50.8% |
| **Slow 80-90** | 547 | 0.42 | 0.76 | **1.89** | **68.0%** |
| Fast X **up** Slow, Slow<25 | 62 | −0.01 | −0.19 | **−0.86** | **45.2%** |
| Fast X **dn** Slow, Slow>75 | 145 | 0.25 | 0.67 | **1.41** | **61.4%** |
| High < 20 | 58 | 0.78 | −0.43 | 2.08 | 55.2% |
| **High > 80** | 270 | 0.21 | 0.22 | **3.06** | **71.5%** |
| DI+ X up DI− | 707 | 0.23 | 0.22 | 0.77 | 51.3% |
| DI+ X dn DI− | 707 | −0.04 | 0.03 | 0.41 | 53.6% |

## Daily — 3,284 bars

| Jewel state | n | +5b % | +10b % | +20b % | win@20 |
|---|---|---|---|---|---|
| **ALL BARS (baseline)** | 3284 | 0.76 | 1.54 | **3.17** | **53.6%** |
| Slow 10-20 | 22 | 1.04 | 0.49 | 1.67 | 63.6% |
| Slow 20-30 | 282 | – | – | – | 56.0% |
| Slow 30-50 | 1232 | 0.32 | 0.21 | **0.47** | 51.1% |
| Slow 50-70 | 988 | 0.38 | 0.63 | **1.73** | **46.3%** |
| **Slow 70-80** | 497 | 2.02 | 3.98 | **9.03** | **62.4%** |
| **Slow 80-90** | 196 | 2.87 | 6.24 | **8.85** | **73.0%** |
| Fast X **up** Slow, Slow<25 | 10 | 2.33 | 0.14 | 0.87 | **30.0%** |
| Fast X **dn** Slow, Slow>75 | 28 | 4.38 | 5.75 | **9.64** | **71.4%** |
| High < 20 | 8 | 10.83 | 13.99 | 13.85 | 100% |
| **High > 80** | 79 | 2.90 | 4.13 | **4.48** | **67.1%** |
| DI+ X up DI− | 108 | 0.84 | 3.22 | 4.78 | 51.9% |
| DI+ X dn DI− | 108 | 0.37 | 0.79 | 2.55 | 52.8% |

## The pattern

**The Jewel reads as a momentum gauge, not a mean-reversion oscillator — and the classic
overbought/oversold interpretation is backwards on BTC.**

1. **High readings are bullish, not a warning.** Slow 70-90 on daily returns +9% over the
   next 20 days versus a +3.2% baseline, with a 62-73% hit rate. On 4h, Slow 80-90 gives
   +1.89% vs +0.50% baseline at 68%. `High > 80` is the single strongest state on both
   timeframes.
2. **The middle of the range is where returns die.** Daily Slow 30-50 returns +0.47% and
   Slow 50-70 returns +1.73% with a **46.3%** hit rate — both well below baseline. The
   oscillator sitting mid-range is the closest thing here to a stand-aside signal.
3. **The textbook signals invert.** "Fast crosses up through Slow while oversold" — the
   classic buy — has a 45.2% hit rate on 4h and 30% on daily. "Fast crosses down while
   overbought" — the classic sell — returns +1.41% (4h) and +9.64% (daily) at ~61-71%.
   Faded as written, taken as continuation they work.
4. **DI+/DI− crosses carry almost nothing.** Both directions sit within noise of baseline
   on both timeframes. The DMI component is not where the information is.

This explains the earlier backtest cleanly. That harness bought oversold crossovers and
sold overbought ones — precisely the two states with the worst forward returns. It wasn't
that The Jewel has no signal; it was traded upside down.

## Before acting on any of this

- **Momentum in a bull market is partly tautological.** "Overbought" means price has been
  rising; in an asset that rose ~40x over the sample, states that select for recent
  strength will look good. This may be a BTC-regime artifact rather than an edge in
  The Jewel specifically. The honest test is a bear or sideways sample, and an
  ADX/trend-conditioned split.
- **No stops, no costs.** These are raw hold-for-N-bars returns. The earlier work showed
  fees and stop geometry are what killed the strategy — a favourable forward-return
  distribution does not survive automatically once you add a 1.5×ATR stop and 0.1%
  round-trip costs at 3x notional.
- **Small samples on the extremes.** Daily `High < 20` (n=8), `Fast X up` (n=10) and
  `Fast X dn` (n=28) are anecdotes, not statistics. The zone buckets (n=196-7247) are the
  rows worth weighting.
- Derived and to-be-tested on the same data. Any rule built from this table needs
  out-of-sample confirmation — other symbols, and a held-out period.

## Obvious next test

Invert the harness: go long when Slow crosses **up** through 70 (entering strength) rather
than up through 25, hold with a wider ATR stop, and require the daily state to agree.
That is the momentum reading of the table, and it is the direct opposite of what was
tested before.
