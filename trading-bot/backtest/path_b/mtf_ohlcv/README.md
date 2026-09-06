# owned-tf-sweep-v1

Path B multi-TF scoreboard: **10 strategies × 16 TFs = 160 cells** (BTCUSDT).

## Aggregation

| TF | Source |
|----|--------|
| 5m | native Binance `5m` (cached once) |
| 10m…12h | aggregate from `5m` (UTC bucket, complete bars only) |
| 1d | native Binance `1d` (cached once) |
| 2d | aggregate 2× `1d` |
| 1w | aggregate 7× `1d` (M2/M4 HTF for 2d only) |

Cache dir: `backtest/cache/mtf/` (gitignored CSV/meta).

## M2/M4 HTF map (frozen — no alternate ladder)

| LTF | HTF |
|-----|-----|
| 5m,10m,15m | 1h |
| 30m,90m,1h,2h,3h | 4h |
| 4h,5h,6h,7h | 1d |
| 9h,12h,1d | 2d |
| 2d | 1w |

Join rule: #12 no-lookahead (`htf_close <= ltf_close`).

## Frozen params

- SMA200 length = **200** bars
- dual-mom lookback = **20** bars; ETH fetched for dual-mom cells only; gate vs 50/50
- ema-rsi cooldown = **6**; regime ADX≥20+DI; RSI 60/50
- KAMA ER 0.30/0.20; ST ATR10×3; BB = Path B #14 (**no retune**)

## Run

```bash
cd trading-bot && source .venv/bin/activate
pytest tests/test_path_b_mtf_ohlcv.py tests/test_jewel_mtf_hub_join.py -q
python -m backtest.path_b.mtf_ohlcv            # full 160
python -m backtest.path_b.mtf_ohlcv --mapping-only
python -m backtest.path_b.mtf_ohlcv --eth-oos   # ETH OOS on 4 BTC PASS cells
```

Scoreboard: `results/owned-tf-sweep-v1-scoreboard.md`

ETH OOS (PASS cells only): `results/owned-tf-sweep-v1-eth-oos.md`

Gate: 6m Mode-A ≥ 1.2× B&H. Not wired to paper/live. Hold merge until asked.
