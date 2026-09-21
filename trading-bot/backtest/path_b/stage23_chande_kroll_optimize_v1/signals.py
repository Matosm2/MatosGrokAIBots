"""Signal logic and backtest execution for Chande Kroll Stop-flip.

Single ID: chande-kroll-stop-flip

Build:
  atr = atr(p)
  highStop = highest(high, p) - x * atr
  lowStop = lowest(low, p) + x * atr
  stopShort = highest(highStop, q)
  stopLong = lowest(lowStop, q)

Mode A:
  long: crossover(close, stopShort)
  exit: crossunder(close, stopLong)

Mode B:
  long: crossover(close, stopShort) AND percentrank(stopShort - stopLong, w_len) > w_min
  exit: crossunder(close, stopLong)
"""

from __future__ import annotations

from dataclasses import dataclass, field

from backtest.data import Bar
from backtest.indicators import crossover, crossunder
from backtest.path_b.stage23_chande_kroll_optimize_v1.indicators import (
    ChandeKrollStops,
    chande_kroll_stops,
    percent_rank,
)


@dataclass(frozen=True)
class ChandeKrollParams:
    p: int = 10
    x: float = 1.0
    q: int = 9
    mode: str = "A"  # "A" or "B"
    # Mode B params (only evaluated when mode == "B")
    w_len: int = 20  # lookback for percentrank of width
    w_min: float = 30.0  # min percentrank threshold (0..100)


@dataclass
class ChandeKrollSignals:
    stops: ChandeKrollStops
    raw_buys: list[bool]
    raw_exits: list[bool]
    buys: list[bool]  # position-gated (pyramiding = 0)
    sells: list[bool]  # position-gated
    width: list[float | None]
    width_pctrank: list[float | None]


def compute_chande_kroll_signals(
    bars: list[Bar],
    params: ChandeKrollParams,
) -> ChandeKrollSignals:
    """Compute indicator stops, raw signals, and position-gated entries/exits."""
    n = len(bars)
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]
    closes_boxed: list[float | None] = list(closes)

    stops = chande_kroll_stops(
        highs, lows, closes, p=params.p, x=params.x, q=params.q
    )

    width: list[float | None] = [None] * n
    for i in range(n):
        s_sh = stops.stop_short[i]
        s_lo = stops.stop_long[i]
        if s_sh is not None and s_lo is not None:
            width[i] = s_sh - s_lo

    width_rank = (
        percent_rank(width, params.w_len)
        if params.mode == "B"
        else [None] * n
    )

    raw_buys = [False] * n
    raw_exits = [False] * n

    for i in range(n):
        # crossover(close, stopShort)
        cross_up = crossover(closes_boxed, stops.stop_short, i)
        # crossunder(close, stopLong)
        cross_down = crossunder(closes_boxed, stops.stop_long, i)

        if params.mode == "A":
            raw_buys[i] = cross_up
        elif params.mode == "B":
            w_ok = (
                width_rank[i] is not None
                and width_rank[i] > params.w_min
            )
            raw_buys[i] = cross_up and w_ok
        else:
            raise ValueError(f"Unknown mode: {params.mode}")

        raw_exits[i] = cross_down

    # Position-gated execution: long-only, pyramiding = 0
    buys = [False] * n
    sells = [False] * n
    in_pos = False

    for i in range(n):
        if not in_pos and raw_buys[i]:
            buys[i] = True
            in_pos = True
        elif in_pos and raw_exits[i]:
            sells[i] = True
            in_pos = False

    return ChandeKrollSignals(
        stops=stops,
        raw_buys=raw_buys,
        raw_exits=raw_exits,
        buys=buys,
        sells=sells,
        width=width,
        width_pctrank=width_rank,
    )


@dataclass
class Trade:
    symbol: str
    entry_bar: int
    exit_bar: int
    entry_time_ms: int
    exit_time_ms: int
    entry_price: float
    exit_price: float
    qty: float
    notional_entry: float
    pnl: float
    pnl_pct: float
    fee_paid: float
    bars_held: int

    @property
    def win(self) -> bool:
        return self.pnl > 0


@dataclass
class BacktestRunResult:
    symbol: str
    timeframe: str
    params: ChandeKrollParams
    trades: list[Trade] = field(default_factory=list)
    equity_curve: list[float] = field(default_factory=list)
    initial_equity: float = 10_000.0
    final_equity: float = 10_000.0
    strategy_return_pct: float = 0.0
    buy_hold_return_pct: float = 0.0
    vs_bh_ratio: float = 0.0  # strategy_return / buy_hold_return (if B&H > 0)
    win_rate_pct: float = 0.0
    max_drawdown_pct: float = 0.0
    fee_rate: float = 0.001
    slippage_rate: float = 0.0005
    buy_qty_pct: float = 100.0  # 100% for Mode-A standard sizing, or 2.5% for ops


def run_chande_kroll_backtest(
    symbol: str,
    bars: list[Bar],
    *,
    params: ChandeKrollParams,
    timeframe: str = "1h",
    initial_equity: float = 10_000.0,
    buy_qty_pct: float = 100.0,
    fee_rate: float = 0.001,
    slippage_rate: float = 0.0005,
) -> BacktestRunResult:
    """Run closed-bar backtest for Chande Kroll stop flip.

    Fills at close * (1 + slippage) on buy, close * (1 - slippage) on sell.
    Fee = notional * fee_rate per side.
    """
    signals = compute_chande_kroll_signals(bars, params)
    cash = initial_equity
    qty = 0.0
    entry_price = 0.0
    entry_bar = -1
    entry_notional = 0.0
    fees_on_trade = 0.0
    trades: list[Trade] = []
    equity_curve: list[float] = []

    for i, bar in enumerate(bars):
        if signals.buys[i] and qty == 0.0:
            equity = cash
            notional = equity * (buy_qty_pct / 100.0)
            if notional > cash:
                notional = cash
            fill = bar.close * (1.0 + slippage_rate)
            if notional > 0 and fill > 0:
                fee = notional * fee_rate
                spend = notional + fee
                if spend > cash:
                    notional = cash / (1.0 + fee_rate)
                    fee = notional * fee_rate
                    spend = notional + fee
                qty = notional / fill
                cash -= spend
                entry_price = fill
                entry_bar = i
                entry_notional = notional
                fees_on_trade = fee

        elif signals.sells[i] and qty > 0.0:
            fill = bar.close * (1.0 - slippage_rate)
            proceeds = qty * fill
            fee = proceeds * fee_rate
            cash += proceeds - fee
            cost = entry_notional + fees_on_trade
            pnl = (proceeds - fee) - cost
            pnl_pct = (pnl / cost) * 100.0 if cost else 0.0
            trades.append(
                Trade(
                    symbol=symbol,
                    entry_bar=entry_bar,
                    exit_bar=i,
                    entry_time_ms=bars[entry_bar].open_time_ms,
                    exit_time_ms=bar.open_time_ms,
                    entry_price=entry_price,
                    exit_price=fill,
                    qty=qty,
                    notional_entry=entry_notional,
                    pnl=pnl,
                    pnl_pct=pnl_pct,
                    fee_paid=fees_on_trade + fee,
                    bars_held=i - entry_bar,
                )
            )
            qty = 0.0
            entry_price = 0.0
            entry_bar = -1
            entry_notional = 0.0
            fees_on_trade = 0.0

        mtm = cash + qty * bar.close
        equity_curve.append(mtm)

    final = equity_curve[-1] if equity_curve else initial_equity
    strat_ret = ((final / initial_equity) - 1.0) * 100.0
    bh_ret = (
        ((bars[-1].close / bars[0].close) - 1.0) * 100.0
        if len(bars) > 1 and bars[0].close > 0
        else 0.0
    )

    # Calculate vs buy-hold ratio
    # When both are positive: strat_ret / bh_ret
    # Standard gate definition: strat_ret >= 1.2 * bh_ret (for positive B&H)
    vs_bh = (strat_ret / bh_ret) if bh_ret != 0.0 else 0.0

    wins = sum(1 for t in trades if t.win)
    wr = (wins / len(trades) * 100.0) if trades else 0.0

    # Max drawdown
    peak = initial_equity
    max_dd = 0.0
    for e in equity_curve:
        if e > peak:
            peak = e
        if peak > 0:
            dd = (peak - e) / peak * 100.0
            if dd > max_dd:
                max_dd = dd

    return BacktestRunResult(
        symbol=symbol,
        timeframe=timeframe,
        params=params,
        trades=trades,
        equity_curve=equity_curve,
        initial_equity=initial_equity,
        final_equity=final,
        strategy_return_pct=strat_ret,
        buy_hold_return_pct=bh_ret,
        vs_bh_ratio=vs_bh,
        win_rate_pct=wr,
        max_drawdown_pct=max_dd,
        fee_rate=fee_rate,
        slippage_rate=slippage_rate,
        buy_qty_pct=buy_qty_pct,
    )
