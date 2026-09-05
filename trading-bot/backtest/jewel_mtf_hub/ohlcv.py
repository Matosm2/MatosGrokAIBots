"""Join HTF OHLCV fields onto an LTF bar series (no lookahead).

Uses the same close-time rule as join.map_htf_onto_ltf. Values are generic
floats (e.g. close, SMA of close) — not Jewel/Hub plots.
"""

from __future__ import annotations

from dataclasses import dataclass

from backtest.jewel_mtf_hub.join import map_htf_onto_ltf


@dataclass(frozen=True)
class OhlcvBar:
    open_time_ms: int
    open: float
    high: float
    low: float
    close: float
    volume: float = 0.0


@dataclass(frozen=True)
class JoinedBar:
    """LTF bar plus the latest completed HTF OHLCV snapshot (or None)."""

    open_time_ms: int
    open: float
    high: float
    low: float
    close: float
    volume: float
    htf_open_time_ms: int | None
    htf_open: float | None
    htf_high: float | None
    htf_low: float | None
    htf_close: float | None
    htf_volume: float | None


def join_htf_ohlcv_onto_ltf(
    *,
    ltf_bars: list[OhlcvBar],
    ltf_tf: str,
    htf_bars: list[OhlcvBar],
    htf_tf: str,
) -> list[JoinedBar]:
    """Attach completed HTF OHLCV onto each LTF bar (no lookahead)."""
    htf_open_ms = [b.open_time_ms for b in htf_bars]
    mapped = map_htf_onto_ltf(
        ltf_open_ms=[b.open_time_ms for b in ltf_bars],
        ltf_tf=ltf_tf,
        htf_open_ms=htf_open_ms,
        htf_values=htf_bars,
        htf_tf=htf_tf,
    )
    out: list[JoinedBar] = []
    for ltf, htf in zip(ltf_bars, mapped, strict=True):
        if htf is None:
            out.append(
                JoinedBar(
                    open_time_ms=ltf.open_time_ms,
                    open=ltf.open,
                    high=ltf.high,
                    low=ltf.low,
                    close=ltf.close,
                    volume=ltf.volume,
                    htf_open_time_ms=None,
                    htf_open=None,
                    htf_high=None,
                    htf_low=None,
                    htf_close=None,
                    htf_volume=None,
                )
            )
        else:
            out.append(
                JoinedBar(
                    open_time_ms=ltf.open_time_ms,
                    open=ltf.open,
                    high=ltf.high,
                    low=ltf.low,
                    close=ltf.close,
                    volume=ltf.volume,
                    htf_open_time_ms=htf.open_time_ms,
                    htf_open=htf.open,
                    htf_high=htf.high,
                    htf_low=htf.low,
                    htf_close=htf.close,
                    htf_volume=htf.volume,
                )
            )
    return out
