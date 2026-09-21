"""Additional tests for Chande Kroll data utilities, sweep runner, and scoreboard generation."""

from __future__ import annotations

from pathlib import Path

from backtest.data import Bar
from backtest.path_b.stage23_chande_kroll_optimize_v1.data import filter_last_months
from backtest.path_b.stage23_chande_kroll_optimize_v1.runner import (
    ScoreboardEntry,
    evaluate_smoke,
    is_pass_6m,
    write_scoreboard,
)


def test_filter_last_months():
    bars: list[Bar] = []
    ms = 1700000000000
    # 200 bars spaced by 1 day (86400 * 1000 ms)
    for i in range(200):
        bars.append(
            Bar(
                open_time_ms=ms + i * 86400 * 1000,
                open=100.0,
                high=105.0,
                low=95.0,
                close=100.0,
                volume=100.0,
                close_time_ms=ms + (i + 1) * 86400 * 1000 - 1,
            )
        )
    # Filter 3 months (~91 days)
    filtered = filter_last_months(bars, months=3.0)
    assert len(filtered) < len(bars)
    assert len(filtered) >= 90


def test_is_pass_6m():
    # Pass case: B&H 20%, strategy 25% (1.25x), n=10 > 5
    passed, ratio = is_pass_6m(25.0, 20.0, 10)
    assert passed is True
    assert ratio == 1.25

    # Tiny-n kill: n=5 <= 5
    passed_tiny, ratio_tiny = is_pass_6m(50.0, 20.0, 5)
    assert passed_tiny is False

    # Under-threshold: strategy 22%, B&H 20% (1.10x)
    passed_under, ratio_under = is_pass_6m(22.0, 20.0, 15)
    assert passed_under is False
    assert ratio_under == 1.10


def test_evaluate_smoke():
    assert evaluate_smoke("BTC", 4, 10.0, 5.0, 2.0, True, 10, 1.0, 9).startswith("KILL: tiny-n")
    assert evaluate_smoke("BTC", 10, -5.0, 10.0, -0.5, False, 10, 1.0, 9).startswith("KILL: negative ret")
    assert evaluate_smoke("BTC", 10, 8.0, 20.0, 0.4, False, 10, 1.0, 9).startswith("FAIL: lag B&H")
    assert evaluate_smoke("ETH", 10, 8.0, 20.0, 0.4, False, 10, 1.0, 9).startswith("FAIL: under 1.2x")
    assert evaluate_smoke("SOL", 10, 8.0, 20.0, 0.4, False, 10, 1.0, 9).startswith("FAIL: under 1.2x")
    assert evaluate_smoke("BNB", 10, 8.0, 20.0, 0.4, False, 10, 1.0, 9).startswith("FAIL: under 1.2x")


def test_write_scoreboard_smoke(tmp_path: Path):
    sample = [
        ScoreboardEntry(
            strategy_id="chande-kroll-stop-flip",
            timeframe="1h",
            mode="A",
            p=10,
            x=1.0,
            q=9,
            btc_n_6m=104,
            btc_wr_6m=28.85,
            btc_ret_6m=-7.58,
            btc_bh_6m=26.77,
            btc_x_bh_6m=-0.283,
            btc_pass_6m=False,
            btc_smoke="KILL: negative ret",
            eth_n_6m=119,
            eth_ret_6m=-8.50,
            eth_bh_6m=35.57,
            eth_x_bh_6m=-0.239,
            eth_pass_6m=False,
            eth_smoke="FAIL",
            sol_n_6m=114,
            sol_ret_6m=-5.82,
            sol_bh_6m=38.52,
            sol_x_bh_6m=-0.151,
            sol_pass_6m=False,
            sol_smoke="FAIL",
            bnb_n_6m=109,
            bnb_ret_6m=-7.65,
            bnb_bh_6m=28.88,
            bnb_x_bh_6m=-0.265,
            bnb_pass_6m=False,
            bnb_smoke="FAIL",
            full_ladder_pass_6m=False,
            btc_ret_2y=-64.64,
            btc_n_2y=463,
            btc_bh_2y=37.55,
            btc_ops_ret_2y=-2.33,
            notes="BANKED_BASELINE_(10,1.0,9)",
        )
    ]
    csv_p, md_p = write_scoreboard(sample, tmp_path)
    assert csv_p.exists()
    assert md_p.exists()
    assert "chande-kroll-stop-flip" in csv_p.read_text()
    assert "chande-kroll-stop-flip" in md_p.read_text()
