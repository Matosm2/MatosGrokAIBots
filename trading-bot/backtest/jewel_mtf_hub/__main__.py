"""Synthetic smoke: print 1D→4H no-lookahead join on toy OHLCV."""

from __future__ import annotations

from datetime import datetime, timezone

from backtest.jewel_mtf_hub.join import TF_MS, map_htf_indices_onto_ltf
from backtest.jewel_mtf_hub.ohlcv import OhlcvBar, join_htf_ohlcv_onto_ltf


def _ms(y: int, m: int, d: int, h: int = 0) -> int:
    return int(datetime(y, m, d, h, tzinfo=timezone.utc).timestamp() * 1000)


def main() -> int:
    # Two daily bars + eight 4H bars spanning those days
    htf = [
        OhlcvBar(_ms(2024, 1, 1), 100, 110, 90, 105, 1.0),
        OhlcvBar(_ms(2024, 1, 2), 105, 120, 100, 115, 1.0),
    ]
    ltf: list[OhlcvBar] = []
    for day, base in ((1, 100.0), (2, 110.0)):
        for h in (0, 4, 8, 12, 16, 20):
            t = _ms(2024, 1, day, h)
            ltf.append(OhlcvBar(t, base, base + 1, base - 1, base + 0.5, 1.0))

    idxs = map_htf_indices_onto_ltf(
        ltf_open_ms=[b.open_time_ms for b in ltf],
        ltf_tf="4H",
        htf_open_ms=[b.open_time_ms for b in htf],
        htf_tf="1D",
    )
    joined = join_htf_ohlcv_onto_ltf(
        ltf_bars=ltf, ltf_tf="4H", htf_bars=htf, htf_tf="1D"
    )

    print("jewel-mtf-hub-regime-v1 — multi-TF join smoke (synthetic OHLCV)")
    print(f"TF_MS: {TF_MS}")
    print("LTF open (UTC) | HTF idx | htf_close")
    for bar, j, jb in zip(ltf, idxs, joined, strict=True):
        t = datetime.fromtimestamp(bar.open_time_ms / 1000, tz=timezone.utc)
        hc = f"{jb.htf_close:.1f}" if jb.htf_close is not None else "None"
        print(f"  {t:%Y-%m-%d %H:%M} | {j!s:>7} | {hc}")
    print(
        "Note: day-1 daily bar is available only after 2024-01-02 00:00 UTC "
        "(no lookahead). Signal scoring parked."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
