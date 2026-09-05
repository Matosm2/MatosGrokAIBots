"""Spot long-only bar-close replay for jewel-strength-hold-v1."""

from __future__ import annotations

from dataclasses import dataclass, field

from backtest.jewel_replay.csv_loader import JewelBar
from backtest.jewel_replay.signals import JewelParams, Variant, compute_signals


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
    exit_reason: str  # zone | atr_stop | zone+atr_stop


@dataclass
class ReplayResult:
    symbol: str
    variant: str
    trades: list[Trade] = field(default_factory=list)
    equity_curve: list[float] = field(default_factory=list)
    timestamps_ms: list[int] = field(default_factory=list)
    initial_equity: float = 10_000.0
    final_equity: float = 10_000.0
    buy_hold_return_pct: float = 0.0
    fee_rate: float = 0.001
    slippage_rate: float = 0.0005
    buy_qty_pct: float = 2.5
    params: JewelParams = field(default_factory=JewelParams)
    notes: list[str] = field(default_factory=list)


def run_replay(
    symbol: str,
    bars: list[JewelBar],
    *,
    params: JewelParams | None = None,
    initial_equity: float = 10_000.0,
    buy_qty_pct: float = 2.5,
    fee_rate: float = 0.001,
    slippage_rate: float = 0.0005,
) -> ReplayResult:
    """
    Process on bar close; pyramiding 0; spot long-only.

    fee_rate default 0.001 = 0.10%/side; slippage_rate default 0.0005 = 5 bps.
    V-wide stop: close < entry_close - atr_mult * ATR(entry)  (matches Pine).
    """
    params = params or JewelParams()
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]
    slow = [b.slow for b in bars]
    jhigh = [b.jewel_high for b in bars]
    sig = compute_signals(
        highs=highs, lows=lows, closes=closes, slow=slow, high_j=jhigh, params=params
    )

    cash = initial_equity
    qty = 0.0
    entry_price = 0.0
    entry_close_ref = 0.0  # Pine entryPx := close (pre-slip) for stop
    entry_bar = -1
    entry_notional = 0.0
    fees_on_trade = 0.0
    entry_atr: float | None = None
    trades: list[Trade] = []
    equity_curve: list[float] = []
    timestamps: list[int] = []

    notes = [
        "strategy_id jewel-strength-hold-v1 — RESEARCH Path B replay.",
        "Bar-close fills; Jewel Slow/High from CSV (no RSI/Stoch proxy).",
        f"Variant={params.variant.value}; fee {fee_rate * 100:.2f}%/side; "
        f"slippage {slippage_rate * 100:.3f}% adverse; size {buy_qty_pct}% equity.",
        "V-wide ATR stop uses ATR frozen at entry; threshold vs entry bar close.",
        "Not wired to paper/live webhooks.",
    ]

    for i, bar in enumerate(bars):
        if qty > 0.0:
            zone = sig.zone_exit[i]
            atr_hit = False
            if (
                params.variant == Variant.V_WIDE
                and entry_atr is not None
                and entry_atr > 0
            ):
                atr_hit = bar.close < entry_close_ref - params.atr_mult * entry_atr
            if zone or atr_hit:
                fill = bar.close * (1.0 - slippage_rate)
                proceeds = qty * fill
                fee = proceeds * fee_rate
                cash += proceeds - fee
                cost = entry_notional + fees_on_trade
                pnl = (proceeds - fee) - cost
                pnl_pct = (pnl / cost) * 100.0 if cost else 0.0
                if atr_hit and zone:
                    reason = "zone+atr_stop"
                elif atr_hit:
                    reason = "atr_stop"
                else:
                    reason = "zone"
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
                        exit_reason=reason,
                    )
                )
                qty = 0.0
                entry_price = 0.0
                entry_close_ref = 0.0
                entry_bar = -1
                entry_notional = 0.0
                fees_on_trade = 0.0
                entry_atr = None

        if sig.raw_long[i] and qty == 0.0:
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
                entry_close_ref = bar.close
                entry_bar = i
                entry_notional = notional
                fees_on_trade = fee
                entry_atr = sig.atr[i]

        mtm = cash + qty * bar.close
        equity_curve.append(mtm)
        timestamps.append(bar.open_time_ms)

    final = equity_curve[-1] if equity_curve else initial_equity
    bh = (bars[-1].close / bars[0].close - 1.0) * 100.0 if bars else 0.0

    return ReplayResult(
        symbol=symbol,
        variant=params.variant.value,
        trades=trades,
        equity_curve=equity_curve,
        timestamps_ms=timestamps,
        initial_equity=initial_equity,
        final_equity=final,
        buy_hold_return_pct=bh,
        fee_rate=fee_rate,
        slippage_rate=slippage_rate,
        buy_qty_pct=buy_qty_pct,
        params=params,
        notes=notes,
    )
