"""ETHUSDT out-of-sample on owned-tf-sweep-v1 BTC PASS cells (frozen params/TF).

Four cells only — no param spray, no paper/alerts.
Gate: 6m Mode-A ≥ 1.2 × ETH buy-and-hold (same window). WR informational.
Also report full(~2y) window; Mode-B ops 2.5% parallel (not scored).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from backtest.data import Bar
from backtest.path_b.engine import run_long_only, slice_result_to_window
from backtest.path_b.report import GATE_SIZE_PCT, OPS_SIZE_PCT, summarize_path_b
from backtest.path_b.sma200_trend_v1 import Sma200Params, compute_signals as sma_signals
from backtest.signals import StrategyParams as EmaParams
from backtest.signals import apply_position_and_cooldown, compute_indicators
from backtest.path_b.mtf_ohlcv.fetch import materialize_symbol
from backtest.path_b.mtf_ohlcv.openproxy_signals import signals_m1
from backtest.path_b.mtf_ohlcv.sweep import FEE, GATE_MULT, INITIAL, SLIP

RESEARCH_ID = "owned-tf-sweep-v1-eth-oos"
SYMBOL = "ETHUSDT"
RESULTS_DIR = Path(__file__).resolve().parent / "results"

# BTC PASS cells from owned-tf-sweep-v1 — priority order, frozen TF/params
ETH_OOS_CELLS: tuple[tuple[str, str], ...] = (
    ("ema-rsi-trend-v1.1", "6h"),
    ("sma200-trend-v1", "9h"),
    ("openproxy-M1", "12h"),
    ("ema-rsi-trend-v1.1", "9h"),
)

SMA_PARAMS = Sma200Params(length=200)
EMA_PARAMS = EmaParams(cooldown_bars=6)
SIZING = (("gate", GATE_SIZE_PCT), ("ops", OPS_SIZE_PCT))
WINDOWS: tuple[tuple[str, float], ...] = (("6m", 6.0), ("full(~2y)", 24.0))


@dataclass
class WindowModeMetrics:
    window: str
    mode: str  # gate | ops
    size_pct: float
    return_pct: float = 0.0
    bh_return_pct: float = 0.0
    ratio: float = 0.0
    win_rate_pct: float = 0.0
    trades: int = 0
    wins: int = 0
    losses: int = 0
    max_drawdown_pct: float = 0.0
    gate: str = "—"  # PASS | FAIL | — (ops)


@dataclass
class EthOosCell:
    strategy_id: str
    tf: str
    gate_6m: str = "FAIL"
    metrics: list[WindowModeMetrics] = field(default_factory=list)
    error: str = ""


def _window_start_ms(months: float) -> int:
    now = datetime.now(timezone.utc).timestamp() * 1000
    return int(now - months * 30.4375 * 24 * 3600 * 1000)


def _mask_buys_before(buys: list[bool], bars: list[Bar], start_ms: int) -> list[bool]:
    out = list(buys)
    for i, b in enumerate(bars):
        if b.open_time_ms < start_ms:
            out[i] = False
    return out


def _ema_signals(bars: list[Bar]) -> tuple[list[bool], list[bool]]:
    closes = [b.close for b in bars]
    frame = compute_indicators(closes, EMA_PARAMS)
    return apply_position_and_cooldown(frame, EMA_PARAMS)


def _signals(strategy_id: str, tf: str, bars: list[Bar]) -> tuple[list[Bar], list[bool], list[bool]]:
    if strategy_id == "ema-rsi-trend-v1.1":
        buys, sells = _ema_signals(bars)
        return bars, buys, sells
    if strategy_id == "sma200-trend-v1":
        buys, sells = sma_signals(bars, SMA_PARAMS)
        return bars, buys, sells
    if strategy_id == "openproxy-M1":
        fr = signals_m1(bars, tf)
        return fr.bars, fr.buys, fr.sells
    raise ValueError(f"unsupported ETH OOS strategy: {strategy_id}")


def _eval_modes(
    strategy_id: str,
    tf: str,
    bars: list[Bar],
    buys_full: list[bool],
    sells_full: list[bool],
) -> list[WindowModeMetrics]:
    out: list[WindowModeMetrics] = []
    for label, months in WINDOWS:
        start = _window_start_ms(months)
        buys = _mask_buys_before(buys_full, bars, start)
        for mode_name, buy_pct in SIZING:
            res = run_long_only(
                SYMBOL,
                strategy_id,
                bars,
                buys,
                sells_full,
                initial_equity=INITIAL,
                buy_qty_pct=buy_pct,
                fee_rate=FEE,
                slippage_rate=SLIP,
                window_label=label,
            )
            sliced = slice_result_to_window(res, bars, start, window_label=label)
            m = summarize_path_b(sliced)
            ret = float(m["return_pct"])
            bh = float(m["buy_hold_return_pct"])
            ratio = float(m["ret_bh_ratio"])
            if ratio == float("inf"):
                ratio = 999.0
            elif ratio == float("-inf"):
                ratio = -999.0
            if mode_name == "gate":
                gate = "PASS" if (m["trades"] > 0 and ret >= GATE_MULT * bh) else "FAIL"
            else:
                gate = "—"
            out.append(
                WindowModeMetrics(
                    window=label,
                    mode=mode_name,
                    size_pct=buy_pct,
                    return_pct=ret,
                    bh_return_pct=bh,
                    ratio=ratio,
                    win_rate_pct=float(m["win_rate_pct"]),
                    trades=int(m["trades"]),
                    wins=int(m["wins"]),
                    losses=int(m["losses"]),
                    max_drawdown_pct=float(m["max_drawdown_pct"]),
                    gate=gate,
                )
            )
            print(
                f"  {SYMBOL} {strategy_id}@{tf} {label} [{mode_name} {buy_pct:g}%]: "
                f"n={m['trades']} wr={m['win_rate_pct']:.1f}% "
                f"ret={ret:+.2f}% bh={bh:+.2f}% ratio={ratio:.3f} [{gate}]",
                flush=True,
            )
    return out


def run_eth_oos(*, years: float = 2.5, refresh: bool = False) -> list[EthOosCell]:
    need_tfs = tuple(dict.fromkeys(tf for _, tf in ETH_OOS_CELLS))
    eth = materialize_symbol(SYMBOL, tfs=need_tfs, years=years, refresh=refresh)
    results: list[EthOosCell] = []
    for sid, tf in ETH_OOS_CELLS:
        print(f"[eth-oos] {sid} @ {tf} ...", flush=True)
        cell = EthOosCell(strategy_id=sid, tf=tf)
        try:
            bars = eth[tf]
            bars_s, buys, sells = _signals(sid, tf, bars)
            cell.metrics = _eval_modes(sid, tf, bars_s, buys, sells)
            g6 = next(
                (m for m in cell.metrics if m.window == "6m" and m.mode == "gate"),
                None,
            )
            cell.gate_6m = g6.gate if g6 else "FAIL"
        except Exception as exc:  # noqa: BLE001
            cell.error = repr(exc)
            cell.gate_6m = "ERROR"
            print(f"  ERROR {exc!r}", flush=True)
        results.append(cell)
    return results


def write_eth_oos_report(results: list[EthOosCell], path: Path | None = None) -> Path:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    path = path or (RESULTS_DIR / "owned-tf-sweep-v1-eth-oos.md")
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines: list[str] = [
        f"# {RESEARCH_ID}",
        "",
        f"_Generated: {now}_",
        "",
        "**RESEARCH ONLY — ETHUSDT OOS on BTC PASS cells. Not paper/live. No retunes.**",
        "",
        "## Scope",
        "",
        "- Parent: `owned-tf-sweep-v1` BTC PASS cells (frozen params / TF / agg)",
        f"- Symbol: **{SYMBOL}** only",
        "- Costs: 0.10%/side fee + 5 bps slip",
        f"- Mode-A gate size: **{GATE_SIZE_PCT:.0f}%** equity; Mode-B ops: **{OPS_SIZE_PCT}%** (parallel, not scored)",
        f"- Gate: 6m Mode-A return ≥ **{GATE_MULT} × ETH B&H** (same window); WR informational",
        "- Agg: 5m/1d native cache; UTC bucket; same Path B harness under `mtf_ohlcv/`",
        "",
        "## Cells (priority order)",
        "",
    ]
    for i, (sid, tf) in enumerate(ETH_OOS_CELLS, 1):
        lines.append(f"{i}. `{sid}` @ `{tf}`")
    lines.append("")
    lines.append("## 6m Mode-A gate table (ETH)")
    lines.append("")
    lines.append(
        "| # | Strategy | TF | Trades | 6m WR | Mode-A ret | ETH B&H | ret/B&H | Ops ret | PASS/FAIL |"
    )
    lines.append(
        "|---|----------|----|--------|-------|------------|---------|---------|---------|-----------|"
    )
    for i, cell in enumerate(results, 1):
        if cell.error:
            lines.append(
                f"| {i} | {cell.strategy_id} | {cell.tf} | — | — | — | — | — | — | **ERROR** |"
            )
            continue
        g = next(m for m in cell.metrics if m.window == "6m" and m.mode == "gate")
        o = next(m for m in cell.metrics if m.window == "6m" and m.mode == "ops")
        lines.append(
            f"| {i} | {cell.strategy_id} | {cell.tf} | {g.trades} | {g.win_rate_pct:.2f}% | "
            f"{g.return_pct:+.2f}% | {g.bh_return_pct:+.2f}% | {g.ratio:.3f} | "
            f"{o.return_pct:+.2f}% | **{cell.gate_6m}** |"
        )
    lines.append("")
    lines.append("## Full window (~2y) Mode-A (info)")
    lines.append("")
    lines.append(
        "| # | Strategy | TF | Trades | WR | Mode-A ret | ETH B&H | ret/B&H | Ops ret |"
    )
    lines.append("|---|----------|----|--------|----|------------|---------|---------|---------|")
    for i, cell in enumerate(results, 1):
        if cell.error:
            lines.append(f"| {i} | {cell.strategy_id} | {cell.tf} | — | — | — | — | — | — |")
            continue
        g = next(m for m in cell.metrics if m.window == "full(~2y)" and m.mode == "gate")
        o = next(m for m in cell.metrics if m.window == "full(~2y)" and m.mode == "ops")
        lines.append(
            f"| {i} | {cell.strategy_id} | {cell.tf} | {g.trades} | {g.win_rate_pct:.2f}% | "
            f"{g.return_pct:+.2f}% | {g.bh_return_pct:+.2f}% | {g.ratio:.3f} | "
            f"{o.return_pct:+.2f}% |"
        )
    lines.append("")
    lines.append("## Cell detail")
    lines.append("")
    for i, cell in enumerate(results, 1):
        lines.append(f"### {i}. `{cell.strategy_id}` @ `{cell.tf}` — 6m gate **{cell.gate_6m}**")
        lines.append("")
        if cell.error:
            lines.append(f"ERROR: `{cell.error}`")
            lines.append("")
            continue
        lines.append(
            "| Window | Mode | Size | Trades | W/L | WR | Ret | ETH B&H | ratio | MDD | Gate |"
        )
        lines.append(
            "|--------|------|------|--------|-----|----|-----|---------|-------|-----|------|"
        )
        for m in cell.metrics:
            lines.append(
                f"| {m.window} | {m.mode} | {m.size_pct:g}% | {m.trades} | "
                f"{m.wins}/{m.losses} | {m.win_rate_pct:.2f}% | {m.return_pct:+.2f}% | "
                f"{m.bh_return_pct:+.2f}% | {m.ratio:.3f} | {m.max_drawdown_pct:.2f}% | "
                f"**{m.gate}** |"
            )
        lines.append("")
    lines.extend(
        [
            "## Caveats",
            "",
            "- Frozen params from owned-tf-sweep-v1 / Path B — **no retune on ETH**.",
            "- Gate PASS/FAIL only on 6m Mode-A vs ETH B&H; full window + ops are informational.",
            "- Not wired to paper/alerts/webhook.",
            "- Same mtf_ohlcv aggregation + signal code as BTC sweep.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")
    return path
