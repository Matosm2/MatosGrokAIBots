"""Spot long-only bar-close engine with dual sizing (Mode-A / Mode-B).

Mode-A: 100% equity when in
Mode-B: 2.5% equity (ops-parallel sizing; does not change live/paper defaults)
"""

from __future__ import annotations

from dataclasses import dataclass, field

from backtest.data import Bar
from backtest.jewel_mtf_hub.signals import SignalFrame

FEE_RATE = 0.001  # 0.10%/side
SLIPPAGE_RATE = 0.0005  # 5 bps
MODE_A_PCT = 100.0
MODE_B_PCT = 2.5


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


@dataclass
class RunResult:
    symbol: str
    variant: str
    mode: str  # Mode-A | Mode-B
    trades: list[Trade] = field(default_factory=list)
    equity_curve: list[float] = field(default_factory=list)
    timestamps_ms: list[int] = field(default_factory=list)
    initial_equity: float = 10_000.0
    final_equity: float = 10_000.0
    buy_hold_return_pct: float = 0.0
    fee_rate: float = FEE_RATE
    slippage_rate: float = SLIPPAGE_RATE
    buy_qty_pct: float = MODE_B_PCT
    window_label: str = ""
    notes: list[str] = field(default_factory=list)


def run_long_only(
    symbol: str,
    frame: SignalFrame,
    *,
    buy_qty_pct: float,
    mode: str,
    initial_equity: float = 10_000.0,
    fee_rate: float = FEE_RATE,
    slippage_rate: float = SLIPPAGE_RATE,
    window_label: str = "",
) -> RunResult:
    bars = frame.bars
    buys = frame.buys
    sells = frame.sells
    assert len(bars) == len(buys) == len(sells)

    cash = initial_equity
    qty = 0.0
    entry_price = 0.0
    entry_bar = -1
    entry_notional = 0.0
    fees_on_trade = 0.0
    trades: list[Trade] = []
    equity_curve: list[float] = []
    timestamps: list[int] = []

    notes = list(frame.notes) + [
        f"research_id jewel-mtf-hub-regime-v1 — open-proxy edition; variant={frame.variant}",
        f"Sizing {mode}: {buy_qty_pct}% equity; fee {fee_rate * 100:.2f}%/side; "
        f"slip {slippage_rate * 100:.3f}% adverse; bar-close; spot long-only.",
        "Not wired to paper/live/alerts/webhooks.",
    ]

    for i, bar in enumerate(bars):
        if sells[i] and qty > 0.0:
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

        if buys[i] and qty == 0.0:
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

        equity_curve.append(cash + qty * bar.close)
        timestamps.append(bar.open_time_ms)

    final = equity_curve[-1] if equity_curve else initial_equity
    bh = (bars[-1].close / bars[0].close - 1.0) * 100.0 if bars else 0.0
    return RunResult(
        symbol=symbol,
        variant=frame.variant,
        mode=mode,
        trades=trades,
        equity_curve=equity_curve,
        timestamps_ms=timestamps,
        initial_equity=initial_equity,
        final_equity=final,
        buy_hold_return_pct=bh,
        fee_rate=fee_rate,
        slippage_rate=slippage_rate,
        buy_qty_pct=buy_qty_pct,
        window_label=window_label,
        notes=notes,
    )


def mask_entries_before(buys: list[bool], bars: list[Bar], start_ms: int) -> list[bool]:
    out = list(buys)
    for i, b in enumerate(bars):
        if b.open_time_ms < start_ms:
            out[i] = False
    return out


def slice_to_window(
    result: RunResult,
    bars: list[Bar],
    window_start_ms: int,
    *,
    window_label: str,
) -> RunResult:
    """Keep trades entering in window; rebase equity curve from window start."""
    start_i = 0
    for i, b in enumerate(bars):
        if b.open_time_ms >= window_start_ms:
            start_i = i
            break
    else:
        start_i = len(bars)

    win_bars = bars[start_i:]
    init = result.initial_equity
    if not win_bars:
        return RunResult(
            symbol=result.symbol,
            variant=result.variant,
            mode=result.mode,
            initial_equity=init,
            final_equity=init,
            fee_rate=result.fee_rate,
            slippage_rate=result.slippage_rate,
            buy_qty_pct=result.buy_qty_pct,
            window_label=window_label,
            notes=result.notes + ["Empty window."],
        )

    trades = [t for t in result.trades if t.entry_time_ms >= window_start_ms]
    if len(result.equity_curve) == len(bars) and start_i < len(result.equity_curve):
        base = result.equity_curve[start_i]
        curve = [init + (e - base) for e in result.equity_curve[start_i:]]
        final = curve[-1] if curve else init
    else:
        eq = init
        curve = []
        pnl_at_exit = {t.exit_bar: t.pnl for t in trades}
        for i in range(start_i, len(bars)):
            if i in pnl_at_exit:
                eq += pnl_at_exit[i]
            curve.append(eq)
        final = eq

    bh = (win_bars[-1].close / win_bars[0].close - 1.0) * 100.0
    return RunResult(
        symbol=result.symbol,
        variant=result.variant,
        mode=result.mode,
        trades=trades,
        equity_curve=curve,
        timestamps_ms=[b.open_time_ms for b in win_bars],
        initial_equity=init,
        final_equity=final,
        buy_hold_return_pct=bh,
        fee_rate=result.fee_rate,
        slippage_rate=result.slippage_rate,
        buy_qty_pct=result.buy_qty_pct,
        window_label=window_label,
        notes=result.notes,
    )


def run_dual_modes(
    symbol: str,
    frame: SignalFrame,
    *,
    window_start_ms: int | None = None,
    window_label: str = "full",
    initial_equity: float = 10_000.0,
) -> dict[str, RunResult]:
    """
    Run Mode-A (100%) and Mode-B (2.5%). If window_start_ms set, mask entries
    before window then slice equity/BH to that window.
    """
    out: dict[str, RunResult] = {}
    for mode, pct in (("Mode-A", MODE_A_PCT), ("Mode-B", MODE_B_PCT)):
        buys = frame.buys
        sells = frame.sells
        if window_start_ms is not None:
            buys = mask_entries_before(buys, frame.bars, window_start_ms)
        # Rebuild gated? buys already gated in SignalFrame; masking entries
        # may leave a sell without matching buy — engine handles (sell ignored if flat).
        # But if we were conceptually "in" from before window, we start flat in window
        # (research convention: independent window book).
        masked = SignalFrame(
            variant=frame.variant,
            bars=frame.bars,
            buys=buys,
            sells=sells,
            notes=frame.notes,
        )
        res = run_long_only(
            symbol,
            masked,
            buy_qty_pct=pct,
            mode=mode,
            initial_equity=initial_equity,
            window_label=window_label,
        )
        if window_start_ms is not None:
            res = slice_to_window(
                res, frame.bars, window_start_ms, window_label=window_label
            )
        out[mode] = res
    return out
