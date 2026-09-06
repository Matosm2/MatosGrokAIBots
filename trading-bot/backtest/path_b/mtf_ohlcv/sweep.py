"""owned-tf-sweep-v1 harness: 10 strategies × 16 TFs = 160 cells (BTCUSDT).

Gate: 6m Mode-A ≥ 1.2× B&H (dual-mom vs 50/50; ETH fetched for dual-mom only).
Hold #14 BB params untouched. No Jewel invite. No new IDs.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from backtest.data import Bar
from backtest.path_b.engine import run_long_only, slice_result_to_window
from backtest.path_b.report import summarize_path_b
from backtest.path_b.bb_squeeze_breakout_v1 import compute_signals as bb_signals
from backtest.path_b.kama_er_trend_v1 import compute_signals as kama_signals
from backtest.path_b.sma200_trend_v1 import Sma200Params, compute_signals as sma_signals
from backtest.path_b.supertrend_atr_v1 import compute_signals as st_signals
from backtest.path_b.dual_mom_btc_eth_v1 import DualMomParams, run_dual_mom
from backtest.signals import StrategyParams as EmaParams
from backtest.signals import apply_position_and_cooldown, compute_indicators
from backtest.path_b.mtf_ohlcv.fetch import materialize_symbol
from backtest.path_b.mtf_ohlcv.openproxy_signals import (
    signals_m1,
    signals_m2,
    signals_m3,
    signals_m4,
)
from backtest.path_b.mtf_ohlcv.timeframes import (
    M2_M4_HTF,
    SWEEP_TFS,
    htf_for,
    ordered_tfs,
)

RESEARCH_ID = "owned-tf-sweep-v1"
STRATEGY_IDS: tuple[str, ...] = (
    "ema-rsi-trend-v1.1",
    "openproxy-M1",
    "openproxy-M2",
    "openproxy-M3",
    "openproxy-M4",
    "bb-squeeze-breakout-v1",
    "kama-er-trend-v1",
    "dual-mom-btc-eth-v1",
    "sma200-trend-v1",
    "supertrend-atr-v1",
)

GATE_MULT = 1.2
GATE_SIZE_PCT = 100.0
FEE = 0.001
SLIP = 0.0005
INITIAL = 10_000.0
RESULTS_DIR = Path(__file__).resolve().parent / "results"

# Frozen params
SMA_PARAMS = Sma200Params(length=200)
DM_PARAMS = DualMomParams(lookback=20)
EMA_PARAMS = EmaParams(cooldown_bars=6)


@dataclass
class CellResult:
    strategy_id: str
    tf: str
    gate: str  # PASS | FAIL | ERROR | SKIP
    mode_a_return_pct: float = 0.0
    bh_return_pct: float = 0.0
    ratio: float = 0.0
    trades: int = 0
    notes: list[str] = field(default_factory=list)
    error: str = ""


def _window_start_ms(months: float = 6.0) -> int:
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


def _eval_long_only(
    strategy_id: str,
    tf: str,
    bars: list[Bar],
    buys: list[bool],
    sells: list[bool],
    *,
    stop_prices: list[float | None] | None = None,
    bh_override_pct: float | None = None,
) -> CellResult:
    start = _window_start_ms(6.0)
    buys_m = _mask_buys_before(buys, bars, start)
    res = run_long_only(
        "BTCUSDT",
        strategy_id,
        bars,
        buys_m,
        sells,
        stop_prices=stop_prices,
        initial_equity=INITIAL,
        buy_qty_pct=GATE_SIZE_PCT,
        fee_rate=FEE,
        slippage_rate=SLIP,
        window_label="6m",
    )
    sliced = slice_result_to_window(res, bars, start, window_label="6m")
    m = summarize_path_b(sliced)
    ret = float(m["return_pct"])
    bh = float(bh_override_pct) if bh_override_pct is not None else float(m["buy_hold_return_pct"])
    ratio = (ret / bh) if bh != 0 else (float("inf") if ret > 0 else 0.0)
    # Path B gate: n>0 AND Mode-A >= 1.2× B&H
    gate = "PASS" if (m["trades"] > 0 and ret >= GATE_MULT * bh) else "FAIL"
    return CellResult(
        strategy_id=strategy_id,
        tf=tf,
        gate=gate,
        mode_a_return_pct=ret,
        bh_return_pct=bh,
        ratio=999.0 if ratio == float("inf") else ratio,
        trades=int(m["trades"]),
    )


def run_cell(
    strategy_id: str,
    tf: str,
    btc: dict[str, list[Bar]],
    eth: dict[str, list[Bar]] | None,
) -> CellResult:
    try:
        bars = btc[tf]
        if strategy_id == "ema-rsi-trend-v1.1":
            buys, sells = _ema_signals(bars)
            return _eval_long_only(strategy_id, tf, bars, buys, sells)

        if strategy_id == "openproxy-M1":
            fr = signals_m1(bars, tf)
            return _eval_long_only(strategy_id, tf, fr.bars, fr.buys, fr.sells)

        if strategy_id == "openproxy-M3":
            fr = signals_m3(bars, tf)
            return _eval_long_only(strategy_id, tf, fr.bars, fr.buys, fr.sells)

        if strategy_id == "openproxy-M2":
            htf = htf_for(tf)
            fr = signals_m2(bars, btc[htf], tf)
            return _eval_long_only(strategy_id, tf, fr.bars, fr.buys, fr.sells)

        if strategy_id == "openproxy-M4":
            htf = htf_for(tf)
            fr = signals_m4(bars, btc[htf], tf)
            return _eval_long_only(strategy_id, tf, fr.bars, fr.buys, fr.sells)

        if strategy_id == "bb-squeeze-breakout-v1":
            buys, sells, stops = bb_signals(bars)  # Path B #14 params untouched
            return _eval_long_only(
                strategy_id, tf, bars, buys, sells, stop_prices=stops
            )

        if strategy_id == "kama-er-trend-v1":
            buys, sells = kama_signals(bars)
            return _eval_long_only(strategy_id, tf, bars, buys, sells)

        if strategy_id == "sma200-trend-v1":
            buys, sells = sma_signals(bars, SMA_PARAMS)
            return _eval_long_only(strategy_id, tf, bars, buys, sells)

        if strategy_id == "supertrend-atr-v1":
            buys, sells = st_signals(bars)
            return _eval_long_only(strategy_id, tf, bars, buys, sells)

        if strategy_id == "dual-mom-btc-eth-v1":
            if eth is None or tf not in eth:
                return CellResult(
                    strategy_id, tf, "ERROR", error="ETH bars missing for dual-mom"
                )
            start = _window_start_ms(6.0)
            dm = run_dual_mom(
                btc[tf],
                eth[tf],
                params=DM_PARAMS,
                initial_equity=INITIAL,
                buy_qty_pct=GATE_SIZE_PCT,
                fee_rate=FEE,
                slippage_rate=SLIP,
                window_label="6m",
                window_start_ms=start,
            )
            sketch = dm.as_sketch()
            m = summarize_path_b(sketch)
            ret = float(m["return_pct"])
            bh = float(dm.buy_hold_return_pct)  # primary 50/50 on window
            ratio = (ret / bh) if bh != 0 else (float("inf") if ret > 0 else 0.0)
            gate = "PASS" if (m["trades"] > 0 and ret >= GATE_MULT * bh) else "FAIL"
            return CellResult(
                strategy_id=strategy_id,
                tf=tf,
                gate=gate,
                mode_a_return_pct=ret,
                bh_return_pct=bh,
                ratio=999.0 if ratio == float("inf") else ratio,
                trades=int(m["trades"]),
                notes=["dual-mom gate vs 50/50 BTC+ETH B&H on 6m window"],
            )

        return CellResult(strategy_id, tf, "ERROR", error=f"unknown strategy {strategy_id}")
    except Exception as exc:  # noqa: BLE001
        return CellResult(strategy_id, tf, "ERROR", error=repr(exc))


def run_sweep(
    *,
    years: float = 2.5,
    refresh: bool = False,
    tfs: tuple[str, ...] | None = None,
) -> list[CellResult]:
    tfs = tfs or ordered_tfs()
    # Ensure HTFs for M2/M4 present
    need: list[str] = []
    for tf in ordered_tfs():
        if tf in tfs or tf in M2_M4_HTF.values():
            if tf not in need:
                need.append(tf)
    for tf in tfs:
        h = M2_M4_HTF[tf]
        if h not in need:
            need.append(h)
    if "1w" not in need:
        need.append("1w")
    for tf in tfs:
        if tf not in need:
            need.append(tf)
    btc = materialize_symbol("BTCUSDT", tfs=tuple(need), years=years, refresh=refresh)
    eth = materialize_symbol("ETHUSDT", tfs=tuple(tfs), years=years, refresh=refresh)

    results: list[CellResult] = []
    for tf in tfs:
        for sid in STRATEGY_IDS:
            print(f"[sweep] {sid} @ {tf} ...", flush=True)
            cell = run_cell(sid, tf, btc, eth)
            print(
                f"  -> {cell.gate} ret={cell.mode_a_return_pct:.2f}% "
                f"bh={cell.bh_return_pct:.2f}% ratio={cell.ratio:.3f} "
                f"trades={cell.trades} {cell.error}",
                flush=True,
            )
            results.append(cell)
    return results


def write_scoreboard(results: list[CellResult], path: Path | None = None) -> Path:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    path = path or (RESULTS_DIR / "owned-tf-sweep-v1-scoreboard.md")
    # pivot
    by: dict[tuple[str, str], CellResult] = {(r.strategy_id, r.tf): r for r in results}
    lines: list[str] = []
    lines.append(f"# {RESEARCH_ID} scoreboard")
    lines.append("")
    lines.append(f"Generated (UTC): {datetime.now(timezone.utc).isoformat()}")
    lines.append("")
    lines.append("Gate: 6m Mode-A ≥ 1.2× B&H (dual-mom vs 50/50 BTC+ETH).")
    lines.append("Symbol: BTCUSDT (ETH only for dual-mom cells). Hold #14 BB params.")
    lines.append("Agg: 5m/1d native cache; UTC bucket aggregate; #12 no-lookahead HTF join.")
    lines.append("")
    lines.append("## M2/M4 HTF map (frozen)")
    lines.append("")
    lines.append("| LTF | HTF |")
    lines.append("|-----|-----|")
    for ltf, htf in M2_M4_HTF.items():
        lines.append(f"| {ltf} | {htf} |")
    lines.append("")
    lines.append("## Scoreboard (PASS/FAIL)")
    lines.append("")
    header = "| strategy \\ tf | " + " | ".join(SWEEP_TFS) + " |"
    sep = "|" + "|".join(["---"] * (len(SWEEP_TFS) + 1)) + "|"
    lines.append(header)
    lines.append(sep)
    for sid in STRATEGY_IDS:
        cells = []
        for tf in SWEEP_TFS:
            r = by.get((sid, tf))
            if r is None:
                cells.append("—")
            elif r.gate == "PASS":
                cells.append(f"PASS({r.ratio:.2f})")
            elif r.gate == "FAIL":
                cells.append(f"FAIL({r.ratio:.2f})")
            else:
                cells.append(f"ERR")
        lines.append("| " + sid + " | " + " | ".join(cells) + " |")
    lines.append("")
    lines.append("## PASS cells")
    lines.append("")
    passes = [r for r in results if r.gate == "PASS"]
    if not passes:
        lines.append("_none_")
    else:
        for r in passes:
            lines.append(
                f"- `{r.strategy_id}` @ `{r.tf}`: ret={r.mode_a_return_pct:.2f}% "
                f"bh={r.bh_return_pct:.2f}% ratio={r.ratio:.3f} trades={r.trades}"
            )
    lines.append("")
    lines.append("## Cell detail")
    lines.append("")
    lines.append("| strategy | tf | gate | modeA% | bh% | ratio | trades | error |")
    lines.append("|----------|----|------|--------|-----|-------|--------|-------|")
    for r in results:
        lines.append(
            f"| {r.strategy_id} | {r.tf} | {r.gate} | {r.mode_a_return_pct:.2f} | "
            f"{r.bh_return_pct:.2f} | {r.ratio:.3f} | {r.trades} | {r.error} |"
        )
    path.write_text("\n".join(lines) + "\n")
    return path
