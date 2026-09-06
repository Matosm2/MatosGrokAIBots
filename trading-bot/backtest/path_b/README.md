# Path B research batch

TV-free offline backtests. **Not wired to paper/live.** Does not change bot defaults.
FAIL ⇒ hard-stop promotion (no paper/alerts/webhook).

| ID | TF | Idea |
|----|----|------|
| `bb-squeeze-breakout-v1` | Daily | BB squeeze + volume breakout + ATR stop |
| `kama-er-trend-v1` | Daily | KAMA(10)+ER entry/exit |
| `dual-mom-btc-eth-v1` | Daily | BTC/ETH 20d momentum rotation |
| `sma200-trend-v1` | Daily | SMA200 cross-above / exit below |
| `supertrend-atr-v1` | Daily | SuperTrend ATR10×3 flip |

## Gate

Mode-A (100%-when-in) return **≥ 1.2 × B&H** on 6m; WR informational.
Mode-B 2.5% ops parallel. Costs: 0.10%/side + 5bps. Data: Binance via **ccxt**.

```bash
cd trading-bot && source .venv/bin/activate
python -m backtest.path_b
pytest tests/test_path_b_signals.py -q
```
