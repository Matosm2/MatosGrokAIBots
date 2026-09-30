"""Static registry and helpers for active paper trading strategies."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Iterable, Optional

from app.target_book import (
    EQUITY_FRACTION,
    FEE_PCT,
    LEVERAGE,
    START_EQUITY_USDT,
    STRATEGY_ID as BTC_DD2H_ID,
    SYMBOL as BTC_DD2H_SYMBOL,
)

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
    book_equity_usdt: Optional[float] = None
    position_equity_pct: Optional[float] = None
    leverage: Optional[float] = None
    fee_pct: Optional[float] = None


# Locked paper seats. btc-dd2h is the only target-style book.
# bostian / accdist stay visible but parked (not on the allowlist).
STRATEGY_REGISTRY: dict[str, StrategyInfo] = {
    BTC_DD2H_ID: StrategyInfo(
        strategy_id=BTC_DD2H_ID,
        name="BTC DD2h",
        symbol=BTC_DD2H_SYMBOL,
        timeframe="2h",
        description=(
            "Separate paper book. Target position long, short, or flat "
            "(not spot long-only). Stays off until ALLOWED_STRATEGIES includes "
            "btc-dd2h. No live path."
        ),
        build="target in {long, short, flat}; size = 100% of book equity × 1x",
        entry_rule="Set target long or short at 100% of this book's equity, 1x leverage.",
        exit_rule="Set target flat, or flip to the opposite target. Fee 0.055% on traded notional.",
        entry_signal='target "long" | "short"',
        exit_signal='target "flat"',
        mode="Target (paper only)",
        direction="Long / short / flat",
        status="Paper",
        book_equity_usdt=START_EQUITY_USDT,
        position_equity_pct=EQUITY_FRACTION * 100.0,
        leverage=LEVERAGE,
        fee_pct=FEE_PCT,
    ),
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
        status="Parked",
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
        status="Parked",
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
