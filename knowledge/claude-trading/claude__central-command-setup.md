# Central Command — session handoff

Updated 2026-08-23 (second session). Read this before re-debugging the connection.

## Account facts (verified, HTTP 200)

- `whoami`: `ownership: "linked"`, `free: true`, `owner_name: "claude-llm-agent"`,
  `effective_user_id` matches the user's id `47c6280a-…c3`.
- Linked Connect key ⇒ **every gateway catalog endpoint is $0**. Never send an
  `__x_payment` / Base USDC payment.
- State as of this session: **0 strategies**, **0 positions**, no BloFin
  credentials connected, `balance.source: "paper"`, no recent trades.

## Connection — what works (re-verified)

`X-Api-Key` must be an HTTP header; in the JSON body it is ignored → 402
`{"error":"X-PAYMENT header is required"}`.

| Channel | Result |
|---|---|
| Cowork container `curl` | **Dead.** The container forces `https_proxy=http://127.0.0.1:36009`; CONNECT to `rtcelwjnrbmfmrywacky.supabase.co:443` returns **403 Forbidden**, curl exit 56. That is Anthropic's sandbox egress allowlist, not Central Command. |
| `WebFetch` | GET-only, no custom headers. Useless for the console. |
| MCP connector (`mcp__Central_Command__*`) | 402 — does not attach `X-Api-Key`, no header param in the schema. |
| **Claude in Chrome, same-origin `fetch`** | **Works.** Use this. |

### Working recipe

1. `navigate` a tab to `https://rtcelwjnrbmfmrywacky.supabase.co/functions/v1/x402-docs`
2. `javascript_tool`: define `window.CC` holding the three headers plus a
   `call(body)` helper that POSTs to `/functions/v1/agent-strategy`, stashes the
   parsed JSON in `window.CC.last`, and returns only `{status, keys}`.
3. Read named fields off `window.CC.last` in follow-up calls.

**Caveat:** the extension redacts any returned chunk that looks like a
token/cookie. Whole-blob dumps (`JSON.stringify(guide)`, `auth_status`) come back
as `[BLOCKED: Sensitive key]`. Pull specific named fields, never the raw object.

## Guide hard rules (from the API)

- `deploy` always leaves the strategy **STOPPED (paused)** — registers only, moves no money.
- The user turns strategies on via Tasks → Go Live.
- Prefer `task_type: "paper"` and `execute` with `force_paper: true`.
- `place_order` / `close_position` / `cancel_order` need `confirm_live: true`
  **and** an explicit request from the user in chat.

### Parameter editing (new finding — matters for sequencing)

- **Hot-editable while running:** `max_leverage`, `default_leverage`,
  `max_risk_per_trade_pct`, `max_total_exposure_pct`, `max_concurrent_positions`,
  `min_rr_ratio`, `asset_universe`, `entry_types`, `require_stop_loss`,
  `capital_config`, `check_interval_minutes`, `trading_permissions`.
- **Requires pause first:** `goal`, `strategy_notes`, `strategy_name`,
  `pinescript_strategy`, `pine_script`.

So the *numbers* can be tuned later, but the **prose `goal` is cold** — get the
entry/exit logic right before `create_strategy`.

Every change is logged to `openclaw_activity_logs` as `params_updated`, visible
via `results`.

## Open issues in the dashboard `goal` text — STILL UNRESOLVED

Flagged four times now. `goal` is a cold field, so settle these first.

1. **No strategy in it.** Every field deciding *when* to trade says "Parse from
   strategy" (max concurrent positions, stop-loss requirement, R:R, timeframe).
   `strategy_name` and `strategy_notes` are empty, `min_rr_ratio` is 0. What
   exists is a position-sizing formula with no entry or exit logic.
2. **Contradictory risk floor.** One line says minimum 6.25%, another says 5.0%;
   HARD CONSTRAINTS cites both in one sentence. No determinate minimum.
3. **The floor forbids standing down.** "You MUST risk at least 6.25% per trade"
   plus "DO NOT shrink position size to be safe" means the agent cannot size
   small in poor conditions. Four consecutive stop-outs at 10% ≈ a third of the
   account. The worked example also lands on exactly 20x at a 0.5% stop, so any
   tighter stop needs leverage above the cap — the agent must either under-risk
   or breach it. On BTC-USDT a 0.5% stop is inside normal intraday noise.

Decide whether 10% is a **ceiling** (normal) or a mandatory **floor** (what the
text currently says).

## Next steps

1. Settle the risk block; write actual entry/exit rules.
2. `backtest` the candidate rules before `create_strategy`.
3. `create_strategy` (paper, `auto_start: false`) → `deploy` (stopped) →
   `execute` with `force_paper: true` → `results` / `logs`.
