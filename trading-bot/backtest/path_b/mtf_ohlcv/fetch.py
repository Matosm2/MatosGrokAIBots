"""Fetch/cache native 5m + 1d; materialize aggregated TFs under cache/mtf/."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from backtest.data import (
    DEFAULT_CACHE_DIR,
    Bar,
    bars_from_csv,
    bars_to_csv,
    load_or_fetch,
)
from backtest.path_b.mtf_ohlcv.aggregate import aggregate_bars
from backtest.path_b.mtf_ohlcv.timeframes import (
    NATIVE_SOURCES,
    SWEEP_TFS,
    TF_SOURCE,
    normalize_tf,
    ordered_tfs,
)

MTF_CACHE_DIR = DEFAULT_CACHE_DIR / "mtf"
DEFAULT_YEARS = 2.5


def _meta_path(cache_dir: Path, symbol: str, interval: str) -> Path:
    return cache_dir / f"{symbol}_{interval}.meta.json"


def _cache_path(cache_dir: Path, symbol: str, interval: str) -> Path:
    return cache_dir / f"{symbol}_{interval}.csv"


def load_native(
    symbol: str,
    interval: str,
    *,
    years: float = DEFAULT_YEARS,
    refresh: bool = False,
) -> list[Bar]:
    """Load native Binance interval via backtest.data (vision host), shared cache/."""
    interval = normalize_tf(interval)
    if interval not in NATIVE_SOURCES:
        raise ValueError(f"Not a native source interval: {interval}")
    # Store natives also under mtf/ for a clear data dir, while load_or_fetch
    # uses DEFAULT_CACHE_DIR — copy path: fetch into DEFAULT then mirror.
    bars = load_or_fetch(symbol, interval, years=years, refresh=refresh)
    MTF_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    path = _cache_path(MTF_CACHE_DIR, symbol.upper(), interval)
    bars_to_csv(path, bars)
    _meta_path(MTF_CACHE_DIR, symbol.upper(), interval).write_text(
        json.dumps(
            {
                "symbol": symbol.upper(),
                "interval": interval,
                "bars": len(bars),
                "source": f"native:{interval}",
                "fetched_at": datetime.now(timezone.utc).isoformat(),
            },
            indent=2,
        )
    )
    return bars


def materialize_tf(
    symbol: str,
    tf: str,
    *,
    bars_5m: list[Bar] | None = None,
    bars_1d: list[Bar] | None = None,
    years: float = DEFAULT_YEARS,
    refresh: bool = False,
    cache: bool = True,
) -> list[Bar]:
    """Return bars for tf, aggregating from 5m or 1d as mapped."""
    tf = normalize_tf(tf)
    src, factor = TF_SOURCE[tf]
    if tf in NATIVE_SOURCES and factor == 1:
        return load_native(symbol, tf, years=years, refresh=refresh)

    if src == "5m":
        base = bars_5m if bars_5m is not None else load_native(
            symbol, "5m", years=years, refresh=refresh
        )
    elif src == "1d":
        base = bars_1d if bars_1d is not None else load_native(
            symbol, "1d", years=years, refresh=refresh
        )
    else:
        raise ValueError(f"Unknown source {src} for {tf}")

    if factor == 1:
        out = list(base)
    else:
        out = aggregate_bars(base, tf)

    if cache:
        MTF_CACHE_DIR.mkdir(parents=True, exist_ok=True)
        path = _cache_path(MTF_CACHE_DIR, symbol.upper(), tf)
        bars_to_csv(path, out)
        _meta_path(MTF_CACHE_DIR, symbol.upper(), tf).write_text(
            json.dumps(
                {
                    "symbol": symbol.upper(),
                    "interval": tf,
                    "bars": len(out),
                    "source": f"aggregate:{src}×{factor}",
                    "fetched_at": datetime.now(timezone.utc).isoformat(),
                },
                indent=2,
            )
        )
    return out


def materialize_symbol(
    symbol: str,
    *,
    tfs: tuple[str, ...] | None = None,
    years: float = DEFAULT_YEARS,
    refresh: bool = False,
) -> dict[str, list[Bar]]:
    """Cache 5m+1d once, then materialize requested TFs (priority order default)."""
    tfs = tfs or ordered_tfs()
    # Always include 1w for M2/M4 on 2d cells
    want = list(tfs)
    if "1w" not in want:
        want.append("1w")
    print(f"[mtf_ohlcv] caching native 5m+1d for {symbol} (~{years:g}y)...", flush=True)
    bars_5m = load_native(symbol, "5m", years=years, refresh=refresh)
    bars_1d = load_native(symbol, "1d", years=years, refresh=refresh)
    print(f"[mtf_ohlcv] 5m={len(bars_5m)} 1d={len(bars_1d)}", flush=True)
    out: dict[str, list[Bar]] = {"5m": bars_5m, "1d": bars_1d}
    for tf in want:
        tf = normalize_tf(tf)
        if tf in out:
            continue
        print(f"[mtf_ohlcv] materialize {symbol} {tf}...", flush=True)
        out[tf] = materialize_tf(
            symbol, tf, bars_5m=bars_5m, bars_1d=bars_1d, years=years, refresh=False
        )
        print(f"[mtf_ohlcv] {tf} -> {len(out[tf])} bars", flush=True)
    return out
