"""fresh-wave-v6 harness: Mass/KST/Twiggs/DeM/Darvas sprays (BTCUSDT).

LEAD gate: 6m Mode-A ≥ 1.2× B&H. Also report full(~2y) Mode-A + ops 2.5%.
Costs: 0.1%/side + 5 bps. Bar-close; long-only Spot. Part B top 5. No paper.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from backtest.data import Bar
from backtest.path_b.engine import run_long_only, slice_result_to_window
from backtest.path_b.fresh_wave_v6 import (
    COARSE_FIRST_TFS,
    PREFERRED_1D_2D,
    PREFERRED_4H_1D,
    RESEARCH_ID,
    STRATEGY_IDS,
)
from backtest.path_b.fresh_wave_v6.darvas_box_v1 import (
    DarvasBoxParams,
    compute_signals as darvas_signals,
)
from backtest.path_b.fresh_wave_v6.demarker_zone_v1 import (
    DemarkerZoneParams,
    compute_signals as dem_signals,
)
from backtest.path_b.fresh_wave_v6.kst_pring_v1 import (
    KstPringParams,
    compute_signals as kst_signals,
)
from backtest.path_b.fresh_wave_v6.mass_index_bulge_v1 import (
    MassIndexBulgeParams,
    compute_signals as mi_signals,
)
from backtest.path_b.fresh_wave_v6.twiggs_mf_v1 import (
    TwiggsMfParams,
    compute_signals as tmf_signals,
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
    """Prefer listed TFs first (still within `tfs`), then remaining coarse-first."""
    if not prefer:
        return tfs
    pref = [t for t in prefer if t in tfs]
    rest = [t for t in tfs if t not in set(pref)]
    return tuple(pref + rest)


def run_mass_cells(btc: dict[str, list[Bar]], tfs: tuple[str, ...]) -> list[CellResult]:
    results: list[CellResult] = []
    sid = "mass-index-bulge-v1"
    order = _ordered_tfs(tfs, PREFERRED_4H_1D + ("2d",))
    for tf in order:
        tag = f"{tf}|sum25|ema9|27/26.5"
        print(f"[fresh-wave-v6] {sid} @ {tag} ...", flush=True)
        cell = CellResult(strategy_id=sid, tf=tag)
        try:
            buys, sells = mi_signals(btc[tf], MassIndexBulgeParams())
            cell.metrics = _eval_windows(sid, btc[tf], buys, sells)
            _finish(cell)
        except Exception as exc:  # noqa: BLE001
            cell.error = repr(exc)
            cell.gate_6m = "ERROR"
            cell.gate_full = "ERROR"
        _print_cell(cell)
        results.append(cell)
    return results


def run_kst_cells(btc: dict[str, list[Bar]], tfs: tuple[str, ...]) -> list[CellResult]:
    results: list[CellResult] = []
    sid = "kst-pring-v1"
    order = _ordered_tfs(tfs, PREFERRED_1D_2D)
    for mode in ("A", "B"):  # Mode-A before Mode-B
        for tf in order:
            tag = f"{tf}|{mode}"
            print(f"[fresh-wave-v6] {sid} @ {tag} ...", flush=True)
            cell = CellResult(strategy_id=sid, tf=tag)
            try:
                buys, sells = kst_signals(btc[tf], KstPringParams(mode=mode))
                cell.metrics = _eval_windows(sid, btc[tf], buys, sells)
                _finish(cell)
            except Exception as exc:  # noqa: BLE001
                cell.error = repr(exc)
                cell.gate_6m = "ERROR"
                cell.gate_full = "ERROR"
            _print_cell(cell)
            results.append(cell)
    return results


def run_twiggs_cells(btc: dict[str, list[Bar]], tfs: tuple[str, ...]) -> list[CellResult]:
    results: list[CellResult] = []
    sid = "twiggs-mf-v1"
    # Mode A primary (N=20), then Mode B; optional N=55 Mode A labeled
    configs: list[tuple[str, int]] = [("A", 20), ("A", 55), ("B", 20)]
    for mode, channel_n in configs:
        for tf in tfs:
            tag = f"{tf}|p21|{mode}"
            if mode == "A":
                tag += f"|n{channel_n}"
            print(f"[fresh-wave-v6] {sid} @ {tag} ...", flush=True)
            cell = CellResult(strategy_id=sid, tf=tag)
            try:
                buys, sells = tmf_signals(
                    btc[tf], TwiggsMfParams(period=21, mode=mode, channel_n=channel_n)
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


def run_demarker_cells(btc: dict[str, list[Bar]], tfs: tuple[str, ...]) -> list[CellResult]:
    results: list[CellResult] = []
    sid = "demarker-zone-v1"
    configs: list[tuple[int, float, float]] = [
        (14, 0.30, 0.70),
        (14, 0.20, 0.80),
        (9, 0.30, 0.70),
    ]
    for length, lo, hi in configs:
        for tf in tfs:
            tag = f"{tf}|{length}|{lo}/{hi}"
            print(f"[fresh-wave-v6] {sid} @ {tag} ...", flush=True)
            cell = CellResult(strategy_id=sid, tf=tag)
            try:
                buys, sells = dem_signals(
                    btc[tf], DemarkerZoneParams(length=length, low_level=lo, high_level=hi)
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


def run_darvas_cells(btc: dict[str, list[Bar]], tfs: tuple[str, ...]) -> list[CellResult]:
    results: list[CellResult] = []
    sid = "darvas-box-v1"
    order = _ordered_tfs(tfs, PREFERRED_1D_2D)
    configs: list[tuple[int, int]] = [(90, 3), (180, 3)]
    for lookback, confirm in configs:
        for tf in order:
            tag = f"{tf}|lb{lookback}|c{confirm}"
            print(f"[fresh-wave-v6] {sid} @ {tag} ...", flush=True)
            cell = CellResult(strategy_id=sid, tf=tag)
            try:
                buys, sells = darvas_signals(
                    btc[tf], DarvasBoxParams(lookback=lookback, confirm=confirm)
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


def run_fresh_wave_v6(
    *,
    years: float = 2.5,
    refresh: bool = False,
    tfs: tuple[str, ...] | None = None,
    prefer_coarse: bool = False,
) -> list[CellResult]:
    tfs = tfs or COARSE_FIRST_TFS
    if prefer_coarse:
        # Restrict to 2d→4h band first
        band = {"2d", "1d", "12h", "9h", "7h", "6h", "5h", "4h"}
        tfs = tuple(t for t in COARSE_FIRST_TFS if t in band)
    need = list(dict.fromkeys([*tfs, *SWEEP_TFS, "5m", "1d", "2d"]))
    btc = materialize_symbol("BTCUSDT", tfs=tuple(need), years=years, refresh=refresh)
    results: list[CellResult] = []

    # Priority: Mode-A-heavy families; coarse TFs ordered inside each runner
    results.extend(run_mass_cells(btc, tfs))
    results.extend(run_kst_cells(btc, tfs))
    results.extend(run_twiggs_cells(btc, tfs))
    results.extend(run_demarker_cells(btc, tfs))
    results.extend(run_darvas_cells(btc, tfs))
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
    path = path or (RESULTS_DIR / "fresh-wave-v6-scoreboard.md")
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
        "- Mass Index: sum **25**; bulge **>27** then **<26.5**; EMA9 slope; prefer 4h–1d.",
        "- KST: (10,15,20,30)/(10,10,10,15)+Signal9; Mode A (KST>0 & cross) before Mode B; prefer 1d–2d.",
        "- Twiggs MF **21** ≠ CMF; Mode A channel+N=20 primary (+N=55 labeled); Mode B zero-cross.",
        "- DeMarker **14** @0.30/0.70 (no RSI); + labeled 0.20/0.80 and length 9.",
        "- Darvas lookback **90** confirm **3** (≠ Donchian); + lb180 labeled; prefer 1d–2d.",
        "- Parked: RVI / CHOP / Elder Impulse. Chandelier = exit-module only (v5; not a primary seat).",
        "",
        "## Strategy rules (documented)",
        "",
        "1. **mass-index-bulge-v1** — MI bulge setup + EMA9 rising; exit EMA9 flip down.",
        "2. **kst-pring-v1** — Mode A: KST>0 & cross above Signal; Mode B: pure cross; exit crossunder or KST<0.",
        "3. **twiggs-mf-v1** — Mode A: close > prior N high & TMF>0; Mode B: TMF cross >0; exit opposite / TMF<0.",
        "4. **demarker-zone-v1** — was ≤0.30 then cross >0.30; exit mid-0.50 or ≥0.70. **No RSI.**",
        "5. **darvas-box-v1** — stateful box after lookback high + confirm top/bottom; buy close > top; trail floor.",
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
            "- Strategy Mode A/B (KST/Twiggs) ≠ sizing Mode-B ops 2.5%.",
            "- No param retune on 6m after freeze. Parked RVI/CHOP/Elder Impulse not scored.",
            "- Hold prior PRs #15–#23 unmerged; this PR is additive fresh-wave-v6 only.",
            "- No OOS (ETH/SOL/BNB) in this PR — BTC scoreboard only.",
            "- Watchlist (no paper): ema-rsi@9h, schaff@2d.",
            "",
            f"## IDs frozen: {', '.join(STRATEGY_IDS)}",
            "",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path
