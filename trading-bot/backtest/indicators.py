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


def true_range(
    highs: list[float], lows: list[float], closes: list[float]
) -> list[float | None]:
    """True range; index 0 is high-low only (no prior close)."""
    n = len(closes)
    out: list[float | None] = [None] * n
    if n == 0:
        return out
    out[0] = highs[0] - lows[0]
    for i in range(1, n):
        out[i] = max(
            highs[i] - lows[i],
            abs(highs[i] - closes[i - 1]),
            abs(lows[i] - closes[i - 1]),
        )
    return out


def rma(values: list[float | None], length: int) -> list[float | None]:
    """Wilder RMA (TradingView ta.rma). Seeds with SMA of first `length` contiguous values."""
    n = len(values)
    out: list[float | None] = [None] * n
    if length <= 0 or n < length:
        return out
    nums: list[float] = []
    seeded = False
    prev = 0.0
    for i, v in enumerate(values):
        if v is None:
            nums = []
            seeded = False
            continue
        if not seeded:
            nums.append(v)
            if len(nums) == length:
                prev = sum(nums) / length
                out[i] = prev
                seeded = True
            continue
        prev = (prev * (length - 1) + v) / length
        out[i] = prev
    return out


def atr(
    highs: list[float],
    lows: list[float],
    closes: list[float],
    length: int = 14,
) -> list[float | None]:
    """Average True Range (Wilder), Pine ta.atr."""
    tr = true_range(highs, lows, closes)
    return rma(tr, length)


def adx_di(
    highs: list[float],
    lows: list[float],
    closes: list[float],
    length: int = 14,
) -> tuple[list[float | None], list[float | None], list[float | None]]:
    """
    Wilder +DI, -DI, ADX (TradingView ta.dmi / ta.adx semantics).

    Returns (plus_di, minus_di, adx).
    """
    n = len(closes)
    plus_di: list[float | None] = [None] * n
    minus_di: list[float | None] = [None] * n
    adx: list[float | None] = [None] * n
    if length <= 0 or n < length + 1:
        return plus_di, minus_di, adx

    tr: list[float | None] = [None] * n
    plus_dm: list[float | None] = [None] * n
    minus_dm: list[float | None] = [None] * n
    tr[0] = highs[0] - lows[0]
    plus_dm[0] = 0.0
    minus_dm[0] = 0.0
    for i in range(1, n):
        up = highs[i] - highs[i - 1]
        down = lows[i - 1] - lows[i]
        plus_dm[i] = up if up > down and up > 0 else 0.0
        minus_dm[i] = down if down > up and down > 0 else 0.0
        tr[i] = max(
            highs[i] - lows[i],
            abs(highs[i] - closes[i - 1]),
            abs(lows[i] - closes[i - 1]),
        )

    atr_s = rma(tr, length)
    plus_s = rma(plus_dm, length)
    minus_s = rma(minus_dm, length)

    dx: list[float | None] = [None] * n
    for i in range(n):
        a, p, m = atr_s[i], plus_s[i], minus_s[i]
        if a is None or p is None or m is None or a == 0:
            continue
        plus_di[i] = 100.0 * p / a
        minus_di[i] = 100.0 * m / a
        s = plus_di[i] + minus_di[i]
        if s == 0:
            dx[i] = 0.0
        else:
            dx[i] = 100.0 * abs(plus_di[i] - minus_di[i]) / s

    adx = rma(dx, length)
    return plus_di, minus_di, adx
