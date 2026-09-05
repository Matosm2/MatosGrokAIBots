"""dual-mom-btc-eth-v1 — Daily BTC+ETH dual momentum rotation (Path B research)."""

from __future__ import annotations

from dataclasses import dataclass, field

from backtest.data import Bar
from backtest.path_b.engine import SketchResult, Trade

STRATEGY_ID = "dual-mom-btc-eth-v1"
INTERVAL = "1d"


@dataclass(frozen=True)
class DualMomParams:
    lookback: int = 20  # closed days total return


def momentum(closes: list[float], i: int, lookback: int) -> float | None:
    """Total return over `lookback` closed days ending at i (close[i]/close[i-lookback]-1)."""
    if i < lookback:
        return None
    base = closes[i - lookback]
    if base == 0:
        return None
    return closes[i] / base - 1.0


def align_bars(
    btc: list[Bar], eth: list[Bar]
) -> tuple[list[Bar], list[Bar]]:
    """Inner-join on open_time_ms."""
    eth_map = {b.open_time_ms: b for b in eth}
    btc_a: list[Bar] = []
    eth_a: list[Bar] = []
    for b in btc:
        e = eth_map.get(b.open_time_ms)
        if e is not None:
            btc_a.append(b)
            eth_a.append(e)
    return btc_a, eth_a


@dataclass
class DualMomResult:
    """Portfolio result with primary 50/50 B&H and secondary BTC-only B&H."""

    strategy_id: str = STRATEGY_ID
    trades: list[Trade] = field(default_factory=list)
    equity_curve: list[float] = field(default_factory=list)
    timestamps_ms: list[int] = field(default_factory=list)
    initial_equity: float = 10_000.0
    final_equity: float = 10_000.0
    buy_hold_return_pct: float = 0.0  # primary 50/50
    btc_only_bh_return_pct: float = 0.0
    fee_rate: float = 0.001
    slippage_rate: float = 0.0005
    buy_qty_pct: float = 100.0
    window_label: str = ""
    symbol: str = "BTC+ETH"
    notes: list[str] = field(default_factory=list)

    def as_sketch(self) -> SketchResult:
        return SketchResult(
            symbol=self.symbol,
            strategy_id=self.strategy_id,
            trades=self.trades,
            equity_curve=self.equity_curve,
            timestamps_ms=self.timestamps_ms,
            initial_equity=self.initial_equity,
            final_equity=self.final_equity,
            buy_hold_return_pct=self.buy_hold_return_pct,
            fee_rate=self.fee_rate,
            slippage_rate=self.slippage_rate,
            buy_qty_pct=self.buy_qty_pct,
            window_label=self.window_label,
            notes=self.notes,
        )


def run_dual_mom(
    btc_bars: list[Bar],
    eth_bars: list[Bar],
    *,
    params: DualMomParams | None = None,
    initial_equity: float = 10_000.0,
    buy_qty_pct: float = 100.0,
    fee_rate: float = 0.001,
    slippage_rate: float = 0.0005,
    window_label: str = "",
    window_start_ms: int | None = None,
) -> DualMomResult:
    """
    mom = total return over 20 closed days.
    If max(BTC_mom, ETH_mom) ≤ 0 → flat (cash).
    Else Mode-A/B: allocate buy_qty_pct of equity to argmax symbol (switch on bar close).
    Primary B&H: 50/50 BTC+ETH hold. Secondary: BTC-only B&H.
    """
    params = params or DualMomParams()
    btc, eth = align_bars(btc_bars, eth_bars)
    n = len(btc)
    btc_c = [b.close for b in btc]
    eth_c = [b.close for b in eth]

    cash = initial_equity
    qty = 0.0
    held: str | None = None  # "BTCUSDT" | "ETHUSDT"
    entry_price = 0.0
    entry_bar = -1
    entry_notional = 0.0
    fees_on_trade = 0.0
    trades: list[Trade] = []
    equity_curve: list[float] = []
    timestamps: list[int] = []

    def _close_pos(i: int, bar: Bar, reason: str) -> None:
        nonlocal cash, qty, held, entry_price, entry_bar, entry_notional, fees_on_trade
        if qty <= 0 or held is None:
            return
        fill = bar.close * (1.0 - slippage_rate)
        proceeds = qty * fill
        fee = proceeds * fee_rate
        cash += proceeds - fee
        cost = entry_notional + fees_on_trade
        pnl = (proceeds - fee) - cost
        pnl_pct = (pnl / cost) * 100.0 if cost else 0.0
        trades.append(
            Trade(
                symbol=held,
                entry_bar=entry_bar,
                exit_bar=i,
                entry_time_ms=btc[entry_bar].open_time_ms,
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
        held = None
        entry_price = 0.0
        entry_bar = -1
        entry_notional = 0.0
        fees_on_trade = 0.0

    def _open_pos(i: int, symbol: str, bar: Bar) -> None:
        nonlocal cash, qty, held, entry_price, entry_bar, entry_notional, fees_on_trade
        equity = cash
        notional = equity * (buy_qty_pct / 100.0)
        if notional > cash:
            notional = cash
        fill = bar.close * (1.0 + slippage_rate)
        if notional <= 0 or fill <= 0:
            return
        fee = notional * fee_rate
        spend = notional + fee
        if spend > cash:
            notional = cash / (1.0 + fee_rate)
            fee = notional * fee_rate
            spend = notional + fee
        qty = notional / fill
        cash -= spend
        held = symbol
        entry_price = fill
        entry_bar = i
        entry_notional = notional
        fees_on_trade = fee

    for i in range(n):
        ts = btc[i].open_time_ms
        in_window = window_start_ms is None or ts >= window_start_ms
        bm = momentum(btc_c, i, params.lookback)
        em = momentum(eth_c, i, params.lookback)

        if in_window and bm is not None and em is not None:
            best = max(bm, em)
            target: str | None
            if best <= 0:
                target = None
            elif bm >= em:
                target = "BTCUSDT"
            else:
                target = "ETHUSDT"

            # switch / exit / enter on bar close
            if held is not None and target != held:
                bar_exit = btc[i] if held == "BTCUSDT" else eth[i]
                _close_pos(i, bar_exit, "switch" if target else "flat")
            if held is None and target is not None:
                bar_in = btc[i] if target == "BTCUSDT" else eth[i]
                _open_pos(i, target, bar_in)
            elif held is not None and target == held:
                pass  # hold
        elif not in_window:
            # stay flat before window (no entries)
            pass

        # MTM
        if held == "BTCUSDT":
            mtm = cash + qty * btc[i].close
        elif held == "ETHUSDT":
            mtm = cash + qty * eth[i].close
        else:
            mtm = cash
        if in_window or window_start_ms is None:
            equity_curve.append(mtm)
            timestamps.append(ts)

    # Force-close open book on last bar
    if qty > 0.0 and held is not None and n > 0:
        i = n - 1
        bar_exit = btc[i] if held == "BTCUSDT" else eth[i]
        _close_pos(i, bar_exit, "eod")
        if equity_curve:
            equity_curve[-1] = cash

    # Slice equity to window if needed
    if window_start_ms is not None:
        # rebuild: only keep from window; rebase
        start_i = 0
        for i, b in enumerate(btc):
            if b.open_time_ms >= window_start_ms:
                start_i = i
                break
        win_btc = btc[start_i:]
        win_eth = eth[start_i:]
        # filter trades to those entering in window
        trades = [t for t in trades if t.entry_time_ms >= window_start_ms]
        if equity_curve:
            # equity_curve already only appended in_window in loop above
            pass
        init = initial_equity
        if equity_curve:
            # rebase so first point ~ init if we started flat
            base = equity_curve[0]
            equity_curve = [init + (e - base) for e in equity_curve]
        final = equity_curve[-1] if equity_curve else init
        if win_btc and win_eth:
            r_btc = win_btc[-1].close / win_btc[0].close - 1.0
            r_eth = win_eth[-1].close / win_eth[0].close - 1.0
            bh_50 = ((1 + r_btc) * 0.5 + (1 + r_eth) * 0.5 - 1.0) * 100.0
            bh_btc = r_btc * 100.0
        else:
            bh_50 = 0.0
            bh_btc = 0.0
        timestamps = [b.open_time_ms for b in win_btc]
    else:
        init = initial_equity
        final = equity_curve[-1] if equity_curve else init
        if btc and eth:
            r_btc = btc[-1].close / btc[0].close - 1.0
            r_eth = eth[-1].close / eth[0].close - 1.0
            bh_50 = ((1 + r_btc) * 0.5 + (1 + r_eth) * 0.5 - 1.0) * 100.0
            bh_btc = r_btc * 100.0
        else:
            bh_50 = 0.0
            bh_btc = 0.0

    return DualMomResult(
        trades=trades,
        equity_curve=equity_curve,
        timestamps_ms=timestamps,
        initial_equity=initial_equity,
        final_equity=final,
        buy_hold_return_pct=bh_50,
        btc_only_bh_return_pct=bh_btc,
        fee_rate=fee_rate,
        slippage_rate=slippage_rate,
        buy_qty_pct=buy_qty_pct,
        window_label=window_label,
        notes=[
            "Primary B&H = 50/50 BTC+ETH hold; secondary BTC-only reported separately.",
            "Flat when max(mom_btc, mom_eth) ≤ 0; else 100%/ops size in argmax.",
            f"strategy_id={STRATEGY_ID} — RESEARCH; not paper/live.",
        ],
    )
