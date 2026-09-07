"""fresh-wave-v9 harness: Camarilla / MESA Sine / Funding-fade (BTCUSDT).

LEAD gate: 6m Mode-A ≥ 1.2× B&H. Also report full(~2y) Mode-A + ops 2.5%.
Costs: 0.1%/side + 5 bps. Bar-close; long-only Spot. No paper. BTC only.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from backtest.data import Bar
from backtest.path_b.engine import run_long_only, slice_result_to_window
from backtest.path_b.fresh_wave_v9 import (
    CAMARILLA_TFS,
    COARSE_FIRST_TFS,
    FUNDING_EXIT_SETTLEMENTS,
    FUNDING_MODE_A_THR,
    FUNDING_TFS,
    FUNDING_Z_TAU,
    FUNDING_Z_WINDOW_SETTLEMENTS,
    MESA_ADVANCE_DEG,
    MESA_DOMINANT_CYCLE,
    PREFERRED_1H_4H,
    RESEARCH_ID,
    STRATEGY_IDS,
)
from backtest.path_b.fresh_wave_v9.camarilla_utc_v1 import (
    CamarillaParams,
    compute_signals as camarilla_signals,
)
from backtest.path_b.fresh_wave_v9.funding_data import (
    FundingFetchError,
    FundingPrint,
    load_or_fetch_funding,
)
from backtest.path_b.fresh_wave_v9.funding_fade_v1 import (
    FundingFadeParams,
    compute_signals as funding_signals,
)
from backtest.path_b.fresh_wave_v9.mesa_sine_v1 import (
    MesaSineParams,
    compute_signals as mesa_signals,
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


def run_camarilla_cells(btc: dict[str, list[Bar]], tfs: tuple[str, ...]) -> list[CellResult]:
    results: list[CellResult] = []
    sid = "camarilla-utc-v1"
    want = [t for t in CAMARILLA_TFS if t in tfs or t in CAMARILLA_TFS]
    for tf in CAMARILLA_TFS:
        if tf not in btc:
            for mode, tag_suffix in (("mode_a", "fadeL3"), ("mode_b", "breakH4")):
                results.append(
                    CellResult(
                        strategy_id=sid,
                        tf=f"{tf}|{mode}|{tag_suffix}|adj1.1",
                        skipped=True,
                        notes=[f"missing bars for {tf}"],
                        gate_6m="N/A",
                        gate_full="N/A",
                    )
                )
            continue
        for mode, tag_suffix in (("mode_a", "fadeL3"), ("mode_b", "breakH4")):
            tag = f"{tf}|{mode}|{tag_suffix}|adj1.1"
            print(f"[fresh-wave-v9] {sid} @ {tag} ...", flush=True)
            cell = CellResult(strategy_id=sid, tf=tag)
            try:
                buys, sells, stops = camarilla_signals(
                    btc[tf], CamarillaParams(mode=mode)
                )
                cell.metrics = _eval_windows(sid, btc[tf], buys, sells, stops)
                _finish(cell)
            except Exception as exc:  # noqa: BLE001
                cell.error = repr(exc)
                cell.gate_6m = "ERROR"
                cell.gate_full = "ERROR"
            _print_cell(cell)
            results.append(cell)
    _ = want
    return results


def run_mesa_cells(btc: dict[str, list[Bar]], tfs: tuple[str, ...]) -> list[CellResult]:
    results: list[CellResult] = []
    sid = "mesa-sine-v1"
    order = _ordered_tfs(tfs, PREFERRED_1H_4H + ("1d", "12h", "2d"))
    for tf in order:
        tag = f"{tf}|dc{MESA_DOMINANT_CYCLE}|adv{int(MESA_ADVANCE_DEG)}"
        print(f"[fresh-wave-v9] {sid} @ {tag} ...", flush=True)
        cell = CellResult(strategy_id=sid, tf=tag)
        try:
            buys, sells = mesa_signals(
                btc[tf],
                MesaSineParams(
                    dominant_cycle=MESA_DOMINANT_CYCLE,
                    advance_deg=MESA_ADVANCE_DEG,
                ),
            )
            cell.metrics = _eval_windows(sid, btc[tf], buys, sells)
            _finish(cell)
        except Exception as exc:  # noqa: BLE001
            cell.error = repr(exc)
            cell.gate_6m = "ERROR"
            cell.gate_full = "ERROR"
        _print_cell(cell)
        results.append(cell)
    return results


def run_funding_cells(
    btc: dict[str, list[Bar]],
    tfs: tuple[str, ...],
    funding: list[FundingPrint] | None,
    funding_error: str = "",
) -> list[CellResult]:
    results: list[CellResult] = []
    sid = "funding-fade-v1"
    for tf in FUNDING_TFS:
        if tf not in btc and tf not in tfs:
            pass
        for mode, tag_suffix in (
            ("mode_a", f"thr-{FUNDING_MODE_A_THR*100:.2f}pct"),
            ("mode_b", f"z{FUNDING_Z_TAU:g}|w{FUNDING_Z_WINDOW_SETTLEMENTS}"),
        ):
            tag = f"{tf}|{mode}|{tag_suffix}|exit{FUNDING_EXIT_SETTLEMENTS}"
            print(f"[fresh-wave-v9] {sid} @ {tag} ...", flush=True)
            cell = CellResult(strategy_id=sid, tf=tag)
            if funding_error or funding is None:
                cell.error = funding_error or "FundingFetchError: no series"
                cell.gate_6m = "ERROR"
                cell.gate_full = "ERROR"
                cell.notes.append("funding fetch blocked — rates not invented")
                _print_cell(cell)
                results.append(cell)
                continue
            if tf not in btc:
                cell.skipped = True
                cell.notes.append(f"missing bars for {tf}")
                cell.gate_6m = "N/A"
                cell.gate_full = "N/A"
                _print_cell(cell)
                results.append(cell)
                continue
            try:
                buys, sells = funding_signals(
                    btc[tf],
                    funding,
                    FundingFadeParams(
                        mode=mode,
                        thr=FUNDING_MODE_A_THR,
                        z_tau=FUNDING_Z_TAU,
                        z_window=FUNDING_Z_WINDOW_SETTLEMENTS,
                        exit_settlements=FUNDING_EXIT_SETTLEMENTS,
                    ),
                )
                cell.metrics = _eval_windows(sid, btc[tf], buys, sells)
                _finish(cell)
            except Exception as exc:  # noqa: BLE001
                cell.error = repr(exc)
                cell.gate_6m = "ERROR"
                cell.gate_full = "ERROR"
            _print_cell(cell)
            results.append(cell)
    return results


def run_fresh_wave_v9(
    *,
    years: float = 2.5,
    refresh: bool = False,
    tfs: tuple[str, ...] | None = None,
    prefer_coarse: bool = False,
) -> list[CellResult]:
    tfs = tfs or COARSE_FIRST_TFS
    if prefer_coarse:
        band = {"2d", "1d", "12h", "9h", "7h", "6h", "5h", "4h", "3h", "2h", "1h"}
        tfs = tuple(t for t in COARSE_FIRST_TFS if t in band)
    need = list(
        dict.fromkeys([*tfs, *SWEEP_TFS, *CAMARILLA_TFS, *FUNDING_TFS, "5m", "1d", "15m", "30m"])
    )
    btc = materialize_symbol("BTCUSDT", tfs=tuple(need), years=years, refresh=refresh)

    funding: list[FundingPrint] | None = None
    funding_error = ""
    try:
        funding = load_or_fetch_funding("BTCUSDT", years=years, refresh=refresh)
        print(f"[fresh-wave-v9] funding prints={len(funding)}", flush=True)
    except FundingFetchError as exc:
        funding_error = repr(exc)
        print(f"[fresh-wave-v9] funding ERROR {funding_error}", flush=True)

    results: list[CellResult] = []
    results.extend(run_camarilla_cells(btc, tfs))
    results.extend(run_mesa_cells(btc, tfs))
    results.extend(run_funding_cells(btc, tfs, funding, funding_error))
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
    path = path or (RESULTS_DIR / "fresh-wave-v9-scoreboard.md")
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
        "- Symbol: BTCUSDT only (no ETH OOS in this PR). Agg: 5m→sub-daily; 1d native; 2d=2×1d.",
        "- Camarilla UTC: prior UTC day H/L/C; `adj=(H−L)×1.1`; Mode A fade L3 (SL beyond L4); Mode B close>H4. TF 15m–1h. ≠ Session ORB.",
        f"- MESA Sine: DominantCycle=**{MESA_DOMINANT_CYCLE}** Advance=**{int(MESA_ADVANCE_DEG)}**; Sine×LeadSine cross; prefer 1h–4h; full 16 OK. No Fisher/RSI.",
        f"- Funding fade: Binance USDT-M fundingRate; Mode A ≤ −{FUNDING_MODE_A_THR*100:.2f}%/8h long; Mode B z≤−{FUNDING_Z_TAU:g} vs ~30d; exit neutral / {FUNDING_EXIT_SETTLEMENTS} settlements; Spot 1h–4h. If fetch blocked → ERROR (no invented rates).",
        "- Watchlist (no paper): ema-rsi@9h, schaff@2d. v8 OOS hard-stop 0 survivors. Hold #15–#26 unmerged.",
        "",
        "## Strategy rules (documented)",
        "",
        "1. **camarilla-utc-v1** — Mode A: fade L3 long, SL=L4, exit mid/H3; Mode B: close>H4, exit <H3 or EOD UTC.",
        "2. **mesa-sine-v1** — crossover(Sine, LeadSine) / crossunder(Sine, LeadSine).",
        "3. **funding-fade-v1** — long-only fade of extreme negative funding; skip short side.",
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
    lines.append("## Funding ERROR cells")
    lines.append("")
    fund_err = [r for r in results if r.strategy_id == "funding-fade-v1" and r.error]
    if not fund_err:
        lines.append("_none_")
    else:
        for r in fund_err:
            lines.append(f"- `{r.tf}`: {r.error}")
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
            "- No param retune on 6m after freeze. Scout-wave-3 parked seats.",
            "- Hold prior PRs #15–#26 unmerged; this PR is additive fresh-wave-v9 only.",
            "- No OOS (ETH/SOL/BNB) in this PR — BTC scoreboard only.",
            "- Watchlist (no paper): ema-rsi@9h, schaff@2d.",
            "- v8 OOS hard-stop 0 survivors — do not revive without Strategy OK.",
            "- Funding rates never invented; blocked fetch → ERROR cell.",
            "",
            f"## IDs frozen: {', '.join(STRATEGY_IDS)}",
            "",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path
