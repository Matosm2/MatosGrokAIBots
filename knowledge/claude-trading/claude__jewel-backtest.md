# The Jewel — mechanical backtest

Run 2026-09-04 in TradingView's own Strategy Tester, on Matos's chart
(`BTC Krown Daily - Main`), BINANCE:BTCUSDT, 1h, **1 Jan 2024 → 5 Sep 2026**.

## Method

The Jewel is invite-only, so its source is not readable and was not touched. Instead a
small Pine strategy ("Jewel harness") consumes the plots The Jewel already publishes on
the chart via `input.source()` — a supported TradingView feature. Its exposed plots are:

`GodModeAlert, DI-, DI+, ADX, Fast, Slow, High, Fib, Fib Green, Fib Red, EmaCross, EMA Long/Short`

The harness maps **Fast / Slow / High** and trades crossovers of Fast against Slow.
Costs: 0.05% commission per side, 2 ticks slippage. Sizing: 1% equity risk, 3x notional cap.

## Results

| Variant | Trades | Win % | Profit factor | Return | Max DD |
|---|---|---|---|---|---|
| Fast/Slow cross in OS/OB zone, ATR stop+target | 96 | 35.4% | 0.80 | **−10.6%** | 20.3% |
| Same, but exit on opposite cross | 98 | 44.9% | 0.71 | **−22.2%** | 26.7% |
| Cross anywhere (no zone filter), ATR exit | 538 | 36.4% | 0.84 | **−41.3%** | 45.7% |
| Cross in zone + 4h EMA trend agreement | 20 | 25.0% | 0.47 | **−6.6%** | 7.9% |

Profit factor never exceeds 0.84. BTC itself roughly doubled over the same window.

Commission load is 14.6% of gross in the baseline and 26.0% in the filtered variant —
at 3x notional the fee drag is large relative to a 1% risk budget, and the 538-trade
variant is mostly destroyed by it.

## What this does NOT show

**This is not a test of Krown's method.** The Jewel is sold as a discretionary confluence
tool taught alongside a course — market structure, higher-timeframe context, and trader
judgment. Mechanical Fast/Slow crossovers are *my* interpretation of its lines, not the
publisher's documented system. A negative result here says the oscillator's raw crossovers
have no standalone mechanical edge on BTC 1h. It does not say the indicator is worthless
in the hands of someone using it the way it was designed.

Other limits: one symbol, one timeframe, one set of Jewel settings (its current chart
config, including TimeFrame Multiplier 1). And because the source is hidden, there is no
way to verify The Jewel does not repaint — if it recalculates historically, these numbers
would be *optimistic*, not pessimistic.

## Comparison with spec v1

Spec v1 (own rules, Python, 206 days): 35.8% win, negative expectancy.
Jewel baseline (TradingView, 2.7 years): 35.4% win, PF 0.80.

Two independent rule sets landing on ~35% with 1.5:2.5 stops points at something
structural: on BTC 1h, a tight ATR stop behind a mean-reversion entry gets taken out by
noise regardless of what triggers the entry. The trigger is not the problem — the stop
geometry and the cost of trading at that frequency are.

## Housekeeping

The "Jewel harness" script is now on the `BTC Krown Daily - Main` layout. Remove it by
right-clicking the legend entry and choosing Remove, or say so and it can be taken off.
