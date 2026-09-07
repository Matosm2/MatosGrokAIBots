"""fresh-wave-v10 harness: VWAP/SMI/Woodie/Chaikin/Laguerre sprays (BTCUSDT).

LEAD gate: 6m Mode-A ≥ 1.2× B&H. Also report full(~2y) Mode-A + ops 2.5%.
Costs: 0.1%/side + 5 bps. Bar-close; long-only Spot. No paper. BTC only.
SOL is the hard OOS filter — not run in this PR (BTC scoreboard first).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from backtest.data import Bar
from backtest.path_b.engine import run_long_only, slice_result_to_window
from backtest.path_b.fresh_wave_v10 import (
    CHAIKIN_FAST,
    CHAIKIN_SLOW,
    COARSE_FIRST_TFS,
    LAGUERRE_GAMMA,
    PREFERRED_15M_4H,
    PREFERRED_1H_4H,
    RESEARCH_ID,
    SMI_LENGTH,
    SMI_OB,
    SMI_OS,
    SMI_SIGNAL,
    SMI_SMOOTH1,
    SMI_SMOOTH2,
    STRATEGY_IDS,
    VWAP_SIGMA_MULT,
    VWAP_TFS,
    WOODIE_TFS,
)
from backtest.path_b.fresh_wave_v10.chaikin_osc_v1 import (
    ChaikinOscParams,
    compute_signals as chaikin_signals,
)
from backtest.path_b.fresh_wave_v10.laguerre_price_v1 import (
    LaguerrePriceParams,
    compute_signals as laguerre_signals,
)
from backtest.path_b.fresh_wave_v10.smi_blau_v1 import (
    SmiBlauParams,
    compute_signals as smi_signals,
)
from backtest.path_b.fresh_wave_v10.vwap_utc_sigma_v1 import (
    VwapUtcSigmaParams,
    compute_signals as vwap_signals,
)
from backtest.path_b.fresh_wave_v10.woodie_utc_v1 import (
    WoodieParams,
    compute_signals as woodie_signals,
)
from backtest.path_b.mtf_ohlcv.fetch import materialize_symbol
from backtest.path_b.mtf_ohlcv.timeframes import SWEEP_TFS
from backtest.path_b.report import GATE_SIZE_PCT, OPS_SIZE_PCT, summarize_path_b

GATE_MULT = 1.2
FEE = 0.001
SLIP = 0.0005
INITIAL = 10_000.0
RESULTS_DIR = Path(__file__).resolve().parent / "results"

SIZING = (("gate", GATE_SIZE_PCT), ("ops", OPS_SIZE_PCT))
WINDOWS: tuple[tuple[str, float], ...] = (("6m", 6.0), ("full(~2y)", 24.0))


@dataclass
class WindowModeMetrics:
    window: str
    mode: str
    size_pct: float
    return_pct: float = 0.0
    bh_return_pct: float = 0.0
    ratio: float = 0.0
    win_rate_pct: float = 0.0
    trades: int = 0
    wins: int = 0
    losses: int = 0
    max_drawdown_pct: float = 0.0
    gate: str = "—"


@dataclass
class CellResult:
    strategy_id: str
    tf: str
    gate_6m: str = "FAIL"
    gate_full: str = "FAIL"
    metrics: list[WindowModeMetrics] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
    error: str = ""
    skipped: bool = False


def _window_start_ms(months: float) -> int:
    now = datetime.now(timezone.utc).timestamp() * 1000
    return int(now - months * 30.4375 * 24 * 3600 * 1000)


def _mask_buys_before(buys: list[bool], bars: list[Bar], start_ms: int) -> list[bool]:
    out = list(buys)
    for i, b in enumerate(bars):
        if b.open_time_ms < start_ms:
            out[i] = False
    return out


def _ratio(ret: float, bh: float) -> float:
    if bh != 0:
        r = ret / bh
    else:
        r = float("inf") if ret > 0 else 0.0
    if r == float("inf"):
        return 999.0
    if r == float("-inf"):
        return -999.0
    return r


def _gate_label(trades: int, ret: float, bh: float) -> str:
    return "PASS" if (trades > 0 and ret >= GATE_MULT * bh) else "FAIL"


def _eval_windows(
    strategy_id: str,
    bars: list[Bar],
    buys_full: list[bool],
    sells_full: list[bool],
    stop_prices: list[float | None] | None = None,
) -> list[WindowModeMetrics]:
    out: list[WindowModeMetrics] = []
    for label, months in WINDOWS:
        start = _window_start_ms(months)
        buys = _mask_buys_before(buys_full, bars, start)
        for mode_name, buy_pct in SIZING:
            res = run_long_only(
                "BTCUSDT",
                strategy_id,
                bars,
                buys,
                sells_full,
                stop_prices=stop_prices,
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
            ratio = _ratio(ret, bh)
            gate = _gate_label(int(m["trades"]), ret, bh) if mode_name == "gate" else "—"
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
    return out


def _finish(cell: CellResult) -> CellResult:
    if cell.error or cell.skipped or not cell.metrics:
        return cell
    g6 = next(m for m in cell.metrics if m.window == "6m" and m.mode == "gate")
    gf = next(m for m in cell.metrics if m.window == "full(~2y)" and m.mode == "gate")
    cell.gate_6m = g6.gate
    cell.gate_full = gf.gate
    return cell


def _print_cell(cell: CellResult) -> None:
    if cell.skipped:
        print(f"  -> N/A ({'; '.join(cell.notes)})", flush=True)
        return
    if cell.error:
        print(f"  -> ERROR {cell.error}", flush=True)
        return
    g6 = next(m for m in cell.metrics if m.window == "6m" and m.mode == "gate")
    gf = next(m for m in cell.metrics if m.window == "full(~2y)" and m.mode == "gate")
    print(
        f"  -> 6m={cell.gate_6m}({g6.ratio:.3f}) n={g6.trades} wr={g6.win_rate_pct:.1f}% | "
        f"full={cell.gate_full}({gf.ratio:.3f}) n={gf.trades}",
        flush=True,
    )


def _ordered_tfs(tfs: tuple[str, ...], prefer: tuple[str, ...] | None = None) -> tuple[str, ...]:
    if not prefer:
        return tfs
    pref = [t for t in prefer if t in tfs]
    rest = [t for t in tfs if t not in set(pref)]
    return tuple(pref + rest)


def _intersect_prefer(tfs: tuple[str, ...], prefer: tuple[str, ...]) -> tuple[str, ...]:
    """Score preferred band only (intersect with requested tfs when provided)."""
    want = [t for t in prefer if t in tfs or t in prefer]
    # Always score the prefer band when data present; filter to tfs if subset requested
    out = [t for t in prefer if t in tfs]
    return tuple(out) if out else tuple(want)


def run_vwap_cells(btc: dict[str, list[Bar]], tfs: tuple[str, ...]) -> list[CellResult]:
    results: list[CellResult] = []
    sid = "vwap-utc-sigma-v1"
    for tf in VWAP_TFS:
        if tf not in btc:
            for mode, tag_suffix in (("mode_a", "tag-2sig"), ("mode_b", "reclaim-vwap")):
                results.append(
                    CellResult(
                        strategy_id=sid,
                        tf=f"{tf}|{mode}|{tag_suffix}|sig{VWAP_SIGMA_MULT:g}",
                        skipped=True,
                        notes=[f"missing bars for {tf}"],
                        gate_6m="N/A",
                        gate_full="N/A",
                    )
                )
            continue
        for mode, tag_suffix in (("mode_a", "tag-2sig"), ("mode_b", "reclaim-vwap")):
            tag = f"{tf}|{mode}|{tag_suffix}|sig{VWAP_SIGMA_MULT:g}"
            print(f"[fresh-wave-v10] {sid} @ {tag} ...", flush=True)
            cell = CellResult(strategy_id=sid, tf=tag)
            try:
                buys, sells = vwap_signals(btc[tf], VwapUtcSigmaParams(mode=mode))
                cell.metrics = _eval_windows(sid, btc[tf], buys, sells)
                _finish(cell)
            except Exception as exc:  # noqa: BLE001
                cell.error = repr(exc)
                cell.gate_6m = "ERROR"
                cell.gate_full = "ERROR"
            _print_cell(cell)
            results.append(cell)
    _ = tfs
    return results


def run_smi_cells(btc: dict[str, list[Bar]], tfs: tuple[str, ...]) -> list[CellResult]:
    results: list[CellResult] = []
    sid = "smi-blau-v1"
    order = _intersect_prefer(tfs, PREFERRED_15M_4H)
    for tf in order:
        if tf not in btc:
            continue
        for mode, tag_suffix in (
            ("mode_a", "xsig-or-0"),
            ("mode_b", f"os{int(SMI_OS)}-reclaim"),
        ):
            tag = (
                f"{tf}|{mode}|{tag_suffix}|n{SMI_LENGTH}|"
                f"sm{SMI_SMOOTH1}/{SMI_SMOOTH2}|sig{SMI_SIGNAL}|ob{int(SMI_OB)}"
            )
            print(f"[fresh-wave-v10] {sid} @ {tag} ...", flush=True)
            cell = CellResult(strategy_id=sid, tf=tag)
            try:
                buys, sells = smi_signals(btc[tf], SmiBlauParams(mode=mode))
                cell.metrics = _eval_windows(sid, btc[tf], buys, sells)
                _finish(cell)
            except Exception as exc:  # noqa: BLE001
                cell.error = repr(exc)
                cell.gate_6m = "ERROR"
                cell.gate_full = "ERROR"
            _print_cell(cell)
            results.append(cell)
    return results


def run_woodie_cells(btc: dict[str, list[Bar]], tfs: tuple[str, ...]) -> list[CellResult]:
    results: list[CellResult] = []
    sid = "woodie-utc-v1"
    for tf in WOODIE_TFS:
        if tf not in btc:
            for mode, tag_suffix in (("mode_a", "fadeS1"), ("mode_b", "breakR1")):
                results.append(
                    CellResult(
                        strategy_id=sid,
                        tf=f"{tf}|{mode}|{tag_suffix}",
                        skipped=True,
                        notes=[f"missing bars for {tf}"],
                        gate_6m="N/A",
                        gate_full="N/A",
                    )
                )
            continue
        for mode, tag_suffix in (("mode_a", "fadeS1"), ("mode_b", "breakR1")):
            tag = f"{tf}|{mode}|{tag_suffix}"
            print(f"[fresh-wave-v10] {sid} @ {tag} ...", flush=True)
            cell = CellResult(strategy_id=sid, tf=tag)
            try:
                buys, sells, stops = woodie_signals(btc[tf], WoodieParams(mode=mode))
                cell.metrics = _eval_windows(sid, btc[tf], buys, sells, stops)
                _finish(cell)
            except Exception as exc:  # noqa: BLE001
                cell.error = repr(exc)
                cell.gate_6m = "ERROR"
                cell.gate_full = "ERROR"
            _print_cell(cell)
            results.append(cell)
    _ = tfs
    return results


def run_chaikin_cells(btc: dict[str, list[Bar]], tfs: tuple[str, ...]) -> list[CellResult]:
    results: list[CellResult] = []
    sid = "chaikin-osc-v1"
    order = _intersect_prefer(tfs, PREFERRED_15M_4H)
    for tf in order:
        if tf not in btc:
            continue
        tag = f"{tf}|ema{CHAIKIN_FAST}-{CHAIKIN_SLOW}|adl-zx"
        print(f"[fresh-wave-v10] {sid} @ {tag} ...", flush=True)
        cell = CellResult(strategy_id=sid, tf=tag)
        try:
            buys, sells = chaikin_signals(btc[tf], ChaikinOscParams())
            cell.metrics = _eval_windows(sid, btc[tf], buys, sells)
            _finish(cell)
        except Exception as exc:  # noqa: BLE001
            cell.error = repr(exc)
            cell.gate_6m = "ERROR"
            cell.gate_full = "ERROR"
        _print_cell(cell)
        results.append(cell)
    return results


def run_laguerre_cells(btc: dict[str, list[Bar]], tfs: tuple[str, ...]) -> list[CellResult]:
    results: list[CellResult] = []
    sid = "laguerre-price-v1"
    order = _intersect_prefer(tfs, PREFERRED_1H_4H)
    for tf in order:
        if tf not in btc:
            continue
        tag = f"{tf}|g{LAGUERRE_GAMMA:g}|price-x"
        print(f"[fresh-wave-v10] {sid} @ {tag} ...", flush=True)
        cell = CellResult(strategy_id=sid, tf=tag)
        try:
            buys, sells = laguerre_signals(btc[tf], LaguerrePriceParams())
            cell.metrics = _eval_windows(sid, btc[tf], buys, sells)
            _finish(cell)
        except Exception as exc:  # noqa: BLE001
            cell.error = repr(exc)
            cell.gate_6m = "ERROR"
            cell.gate_full = "ERROR"
        _print_cell(cell)
        results.append(cell)
    return results


def run_fresh_wave_v10(
    *,
    years: float = 2.5,
    refresh: bool = False,
    tfs: tuple[str, ...] | None = None,
    prefer_coarse: bool = False,
) -> list[CellResult]:
    tfs = tfs or COARSE_FIRST_TFS
    if prefer_coarse:
        band = {"4h", "3h", "2h", "1h", "90m", "30m", "15m"}
        tfs = tuple(t for t in COARSE_FIRST_TFS if t in band)
    need = list(
        dict.fromkeys(
            [
                *tfs,
                *SWEEP_TFS,
                *VWAP_TFS,
                *WOODIE_TFS,
                *PREFERRED_15M_4H,
                *PREFERRED_1H_4H,
                "5m",
                "1d",
                "15m",
                "30m",
            ]
        )
    )
    btc = materialize_symbol("BTCUSDT", tfs=tuple(need), years=years, refresh=refresh)

    results: list[CellResult] = []
    results.extend(run_vwap_cells(btc, tfs))
    results.extend(run_smi_cells(btc, tfs))
    results.extend(run_woodie_cells(btc, tfs))
    results.extend(run_chaikin_cells(btc, tfs))
    results.extend(run_laguerre_cells(btc, tfs))
    return results


def _gate_cell(gate: str, ratio: float) -> str:
    if gate == "PASS":
        return f"PASS({ratio:.2f})"
    if gate == "FAIL":
        return f"FAIL({ratio:.2f})"
    if gate == "ERROR":
        return "ERR"
    if gate == "N/A":
        return "N/A"
    return "—"


def write_scoreboard(results: list[CellResult], path: Path | None = None) -> Path:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    path = path or (RESULTS_DIR / "fresh-wave-v10-scoreboard.md")
    now = datetime.now(timezone.utc).isoformat()
    lines: list[str] = [
        f"# {RESEARCH_ID} scoreboard",
        "",
        f"Generated (UTC): {now}",
        "",
        "**RESEARCH ONLY — not paper/live. No Claude/TV. No Jewel. No remakes / burned grafts.**",
        "",
        "## Scoring",
        "",
        f"- **LEAD gate:** 6m Mode-A ≥ **{GATE_MULT}×** B&H → `PASS/FAIL_6m` (≥1 trade). WR informational.",
        f"- **Also:** full(~2y) Mode-A ≥ **{GATE_MULT}×** B&H → `PASS/FAIL_full` (informational)",
        f"- Costs: 0.10%/side fee + 5 bps slip; Mode-A **{GATE_SIZE_PCT:.0f}%** + Mode-B ops **{OPS_SIZE_PCT}%** (ops not scored)",
        "- Symbol: BTCUSDT only (no ETH OOS in this PR). **SOL is the hard OOS filter** — deferred; BTC scoreboard first.",
        "- Agg: 5m→sub-daily; 1d native; 2d=2×1d. Reuse `mtf_ohlcv`.",
        f"- VWAP UTC σ: reset 00:00 UTC; ±{VWAP_SIGMA_MULT:g}σ bands; Mode A tag −2σ reclaim; Mode B reclaim above VWAP; exit VWAP/EOD. TF 15m–1h. ≠ BB.",
        f"- SMI Blau: N=**{SMI_LENGTH}** smooth **{SMI_SMOOTH1}/{SMI_SMOOTH2}** sig **{SMI_SIGNAL}**; OB/OS ±**{int(SMI_OB)}**; Mode A ×sig/0; Mode B OS reclaim. TF 15m–4h. Forbidden Stoch/Connors/RSI.",
        "- Woodie UTC: prior UTC day P=(H+L+2C)/4; Mode A fade S1 (SL S2); Mode B close>R1. TF 5m–1h. ≠ Camarilla; ≠ Session ORB.",
        f"- Chaikin Osc: EMA(**{CHAIKIN_FAST}**)−EMA(**{CHAIKIN_SLOW}**) of ADL zero-cross. TF 15m–4h. Forbidden CMF/OBV/MFI twin.",
        f"- Laguerre price: γ=**{LAGUERRE_GAMMA:g}** on close; price×filter cross. TF 1h–4h. Forbidden Laguerre RSI / EMA×RSI.",
        "- Parked: Klinger, VR+breakout, % Envelopes — not this wave.",
        "- Watchlist (no paper): ema-rsi@9h, schaff@2d. v9 hard-stop 0 PASS_6m. Hold #15–#27 unmerged.",
        "",
        "## Strategy rules (documented)",
        "",
        "1. **vwap-utc-sigma-v1** — Mode A: tag −2σ then reclaim toward VWAP; Mode B: close reclaim above VWAP; exit VWAP touch / EOD UTC.",
        "2. **smi-blau-v1** — Mode A: crossover(SMI, signal) OR cross above 0; Mode B: was ≤−40 then cross >−40; exit ×signal / mid-0 / ≥+40.",
        "3. **woodie-utc-v1** — Mode A: fade S1 long SL=S2 exit P/R1; Mode B: close>R1 exit ≤P or EOD.",
        "4. **chaikin-osc-v1** — crossover(Osc, 0) / crossunder(Osc, 0).",
        "5. **laguerre-price-v1** — close crossover above Laguerre / crossunder below.",
        "",
        "## PASS_6m cells (LEAD)",
        "",
    ]
    six_pass = [r for r in results if r.gate_6m == "PASS"]
    if not six_pass:
        lines.append("_none_")
    else:
        for r in six_pass:
            g = next(m for m in r.metrics if m.window == "6m" and m.mode == "gate")
            gf = next(m for m in r.metrics if m.window == "full(~2y)" and m.mode == "gate")
            lines.append(
                f"- `{r.strategy_id}` @ `{r.tf}`: 6m ret={g.return_pct:.2f}% "
                f"bh={g.bh_return_pct:.2f}% ratio={g.ratio:.3f} wr={g.win_rate_pct:.1f}% "
                f"n={g.trades} | full={r.gate_full} ratio={gf.ratio:.3f} n={gf.trades}"
            )
    lines.append("")
    lines.append("## PASS_full cells (informational; not LEAD)")
    lines.append("")

    full_pass = [r for r in results if r.gate_full == "PASS"]
    if not full_pass:
        lines.append("_none_")
    else:
        for r in full_pass:
            g = next(m for m in r.metrics if m.window == "full(~2y)" and m.mode == "gate")
            lines.append(
                f"- `{r.strategy_id}` @ `{r.tf}`: full ret={g.return_pct:.2f}% "
                f"bh={g.bh_return_pct:.2f}% ratio={g.ratio:.3f} wr={g.win_rate_pct:.1f}% "
                f"n={g.trades} | 6m={r.gate_6m}"
            )
    lines.append("")
    lines.append("## LEAD 6m by family (all scored cells)")
    lines.append("")

    for sid in STRATEGY_IDS:
        fam = [r for r in results if r.strategy_id == sid]
        if not fam:
            continue
        lines.append(f"### {sid}")
        lines.append("")
        lines.append(
            "| cell | 6m | 6m_ret% | 6m_bh% | 6m_ratio | 6m_wr% | 6m_n | "
            "full | full_ratio | full_n | ops_6m% | ops_full% | error |"
        )
        lines.append(
            "|------|----|---------|--------|----------|--------|------|"
            "------|------------|--------|---------|-----------|-------|"
        )
        for r in fam:
            if r.skipped:
                lines.append(
                    f"| {r.tf} | N/A | — | — | — | — | — | N/A | — | — | — | — | "
                    f"{'; '.join(r.notes)} |"
                )
                continue
            if r.error:
                lines.append(
                    f"| {r.tf} | ERROR | — | — | — | — | — | ERROR | — | — | — | — | "
                    f"{r.error} |"
                )
                continue
            g6 = next(m for m in r.metrics if m.window == "6m" and m.mode == "gate")
            gf = next(m for m in r.metrics if m.window == "full(~2y)" and m.mode == "gate")
            o6 = next(m for m in r.metrics if m.window == "6m" and m.mode == "ops")
            of = next(m for m in r.metrics if m.window == "full(~2y)" and m.mode == "ops")
            lines.append(
                f"| {r.tf} | {_gate_cell(r.gate_6m, g6.ratio)} | {g6.return_pct:.2f} | "
                f"{g6.bh_return_pct:.2f} | {g6.ratio:.3f} | {g6.win_rate_pct:.1f} | {g6.trades} | "
                f"{_gate_cell(r.gate_full, gf.ratio)} | {gf.ratio:.3f} | {gf.trades} | "
                f"{o6.return_pct:.2f} | {of.return_pct:.2f} |  |"
            )
        lines.append("")

    lines.extend(
        [
            "## Caveats",
            "",
            "- LEAD = 6m Mode-A sizing only. full(~2y) context only.",
            "- No param retune on 6m after freeze. Scout-wave-4 seats.",
            "- Hold prior PRs #15–#27 unmerged; this PR is additive fresh-wave-v10 only.",
            "- No OOS (ETH/SOL/BNB) in this PR — BTC scoreboard only. **SOL = hard filter** when OOS runs.",
            "- Watchlist (no paper): ema-rsi@9h, schaff@2d.",
            "- v9 hard-stop 0 PASS_6m — do not revive without Strategy OK.",
            "- Parked: Klinger, VR+breakout, % Envelopes.",
            "",
            f"## IDs frozen: {', '.join(STRATEGY_IDS)}",
            "",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path
