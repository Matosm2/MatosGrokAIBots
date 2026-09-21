"""Static registry and helpers for active paper trading strategies."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Iterable, Optional

if TYPE_CHECKING:
    from app.models import TradeRecord


@dataclass(frozen=True)
class StrategyInfo:
    """Metadata describing a strategy seat, its rules, and signals."""

    strategy_id: str
    name: str
    symbol: str
    timeframe: str
    description: str
    build: str
    entry_rule: str
    exit_rule: str
    entry_signal: str
    exit_signal: str
    mode: str = "Mode A (closed bar)"
    direction: str = "Long-only"
    status: str = "Paper Active"


# Locked paper seats (source of truth: PAPER_PARAMS)
STRATEGY_REGISTRY: dict[str, StrategyInfo] = {
    "bostian-iii-sma-zero": StrategyInfo(
        strategy_id="bostian-iii-sma-zero",
        name="Bostian III SMA(21) Zero-Line",
        symbol="BTCUSDT",
        timeframe="4h",
        description=(
            "Bostian Intraday Intensity Index (III) smoothed with SMA(21); "
            "trades the zero-line of that smoothed III. Long-only, Mode A, symbol BTCUSDT only."
        ),
        build="rng = high - low; iii = ((2*close - high - low) / rng) * volume (0 if rng == 0); iiiS = ta.sma(iii, 21)",
        entry_rule="Enter long when smoothed III (SMA 21) crosses above 0 on a closed bar.",
        exit_rule=(
            "Exit long when smoothed III (SMA 21) crosses below 0 on a closed bar (primary exit). "
            "Optional ATR trail may exist as secondary only."
        ),
        entry_signal="ta.crossover(iiiS, 0)",
        exit_signal="ta.crossunder(iiiS, 0)",
        mode="Mode A (closed bar)",
        direction="Long-only",
        status="Paper Active",
    ),
    "accdist-sma-cross-v1": StrategyInfo(
        strategy_id="accdist-sma-cross-v1",
        name="ADL SMA(50) Cross",
        symbol="ETHUSDT",
        timeframe="4h",
        description=(
            "Accumulation/Distribution line vs its SMA(50); "
            "trades the cross of ADL vs that signal. Long-only, Mode A, symbol ETHUSDT only."
        ),
        build="adl = ta.accdist; sig = ta.sma(adl, 50)",
        entry_rule="Enter long when Accumulation/Distribution line (ADL) crosses above its SMA(50) signal line on a closed bar.",
        exit_rule=(
            "Exit long when Accumulation/Distribution line (ADL) crosses below its SMA(50) signal line on a closed bar (primary exit). "
            "Optional ATR trail secondary only."
        ),
        entry_signal="ta.crossover(adl, sig)",
        exit_signal="ta.crossunder(adl, sig)",
        mode="Mode A (closed bar)",
        direction="Long-only",
        status="Paper Active",
    ),
}


def get_active_strategies(
    trades: Optional[Iterable[TradeRecord]] = None,
) -> list[StrategyInfo]:
    """Return all active strategies.

    Always includes the locked paper seats. If any additional strategy_ids
    are observed in recent trades, dynamic entries are added.
    """
    result: dict[str, StrategyInfo] = dict(STRATEGY_REGISTRY)
    if trades:
        for t in trades:
            sid = getattr(t, "strategy_id", None)
            if sid and sid not in result:
                result[sid] = StrategyInfo(
                    strategy_id=sid,
                    name=sid,
                    symbol=getattr(t, "symbol", "—"),
                    timeframe="—",
                    description="Strategy observed in recent trade execution alerts.",
                    build="—",
                    entry_rule="Defined via webhook alert signal.",
                    exit_rule="Defined via webhook alert signal.",
                    entry_signal="—",
                    exit_signal="—",
                    mode="Observed",
                    direction=getattr(t, "side", "trade").value
                    if hasattr(getattr(t, "side", None), "value")
                    else str(getattr(t, "side", "—")),
                    status="Observed in trades",
                )
    return list(result.values())
