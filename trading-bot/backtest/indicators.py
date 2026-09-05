"""Pure-Python EMA and RSI (Wilder) matching TradingView/Pine semantics."""

from __future__ import annotations


def ema(values: list[float], length: int) -> list[float | None]:
    """Exponential moving average. Seed = SMA of first `length` closes (Pine/TV)."""
    n = len(values)
    out: list[float | None] = [None] * n
    if length <= 0 or n < length:
        return out
    seed = sum(values[:length]) / length
    out[length - 1] = seed
    mult = 2.0 / (length + 1)
    prev = seed
    for i in range(length, n):
        prev = (values[i] - prev) * mult + prev
        out[i] = prev
    return out


def rsi(values: list[float], length: int = 14) -> list[float | None]:
    """Wilder RSI as used by TradingView `ta.rsi`."""
    n = len(values)
    out: list[float | None] = [None] * n
    if length <= 0 or n < length + 1:
        return out

    gains = 0.0
    losses = 0.0
    for i in range(1, length + 1):
        diff = values[i] - values[i - 1]
        if diff >= 0:
            gains += diff
        else:
            losses -= diff
    avg_gain = gains / length
    avg_loss = losses / length

    def _rsi(ag: float, al: float) -> float:
        if al == 0:
            return 100.0
        rs = ag / al
        return 100.0 - (100.0 / (1.0 + rs))

    out[length] = _rsi(avg_gain, avg_loss)

    for i in range(length + 1, n):
        diff = values[i] - values[i - 1]
        gain = diff if diff > 0 else 0.0
        loss = -diff if diff < 0 else 0.0
        avg_gain = (avg_gain * (length - 1) + gain) / length
        avg_loss = (avg_loss * (length - 1) + loss) / length
        out[i] = _rsi(avg_gain, avg_loss)
    return out


def crossover(a: list[float | None], b: list[float | None], i: int) -> bool:
    """True when a crosses above b on bar i (Pine ta.crossover)."""
    if i < 1:
        return False
    ai, bi = a[i], b[i]
    ap, bp = a[i - 1], b[i - 1]
    if ai is None or bi is None or ap is None or bp is None:
        return False
    return ap <= bp and ai > bi


def crossunder(a: list[float | None], b: list[float | None], i: int) -> bool:
    """True when a crosses below b on bar i (Pine ta.crossunder)."""
    if i < 1:
        return False
    ai, bi = a[i], b[i]
    ap, bp = a[i - 1], b[i - 1]
    if ai is None or bi is None or ap is None or bp is None:
        return False
    return ap >= bp and ai < bi
