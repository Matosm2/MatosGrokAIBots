"""Simple authenticated paper dashboard (session cookie; secret never in URL)."""

from __future__ import annotations

import hashlib
import hmac
from html import escape
from typing import Optional

from fastapi import APIRouter, Depends, Form, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse

from app.config import Settings, get_settings
from app.deps import get_executor, get_portfolio, secrets_equal
from app.executor import TradeExecutor
from app.risk import PortfolioState

COOKIE_NAME = "dashboard_session"
COOKIE_MAX_AGE = 60 * 60 * 24 * 7  # 7 days

router = APIRouter(tags=["dashboard"])


def session_token(webhook_secret: str) -> str:
    """Derive a cookie token from the webhook secret (raw secret not stored in cookie)."""
    return hmac.new(
        webhook_secret.encode("utf-8"),
        b"dashboard-session-v1",
        hashlib.sha256,
    ).hexdigest()


def is_dashboard_authed(request: Request, settings: Settings) -> bool:
    cookie = request.cookies.get(COOKIE_NAME)
    if not cookie or not settings.webhook_secret:
        return False
    expected = session_token(settings.webhook_secret)
    return secrets_equal(cookie, expected)


def _layout(title: str, body: str, authed: bool = False) -> str:
    nav = (
        '<form method="post" action="/dashboard/logout" class="nav-form">'
        '<button type="submit">Log out</button></form>'
        if authed
        else ""
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>{escape(title)}</title>
  <style>
    :root {{
      --bg: #0f1419;
      --card: #1a2332;
      --text: #e7ecf3;
      --muted: #8b9bb4;
      --accent: #3d8bfd;
      --ok: #3dd68c;
      --bad: #f31260;
      --border: #2a3548;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0; font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, sans-serif;
      background: var(--bg); color: var(--text); line-height: 1.45;
    }}
    header {{
      display: flex; align-items: center; justify-content: space-between;
      padding: 1rem 1.25rem; border-bottom: 1px solid var(--border);
      background: #121820;
    }}
    header h1 {{ margin: 0; font-size: 1.15rem; font-weight: 600; }}
    main {{ max-width: 960px; margin: 0 auto; padding: 1.25rem; }}
    .cards {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 0.75rem; }}
    .card {{
      background: var(--card); border: 1px solid var(--border); border-radius: 10px;
      padding: 0.9rem 1rem;
    }}
    .card .label {{ color: var(--muted); font-size: 0.75rem; text-transform: uppercase; letter-spacing: .04em; }}
    .card .value {{ font-size: 1.25rem; font-weight: 600; margin-top: 0.25rem; }}
    .badge {{
      display: inline-block; padding: 0.15rem 0.5rem; border-radius: 999px;
      font-size: 0.8rem; font-weight: 600; text-transform: uppercase;
    }}
    .badge.paper {{ background: #1e3a5f; color: #8ec8ff; }}
    .badge.live {{ background: #3a1e1e; color: #ff8e8e; }}
    .pos {{ color: var(--ok); }}
    .neg {{ color: var(--bad); }}
    h2 {{ font-size: 1rem; margin: 1.5rem 0 0.6rem; color: var(--muted); font-weight: 600; }}
    table {{ width: 100%; border-collapse: collapse; background: var(--card); border-radius: 10px; overflow: hidden; border: 1px solid var(--border); }}
    th, td {{ text-align: left; padding: 0.55rem 0.75rem; border-bottom: 1px solid var(--border); font-size: 0.9rem; }}
    th {{ color: var(--muted); font-weight: 500; background: #121820; }}
    tr:last-child td {{ border-bottom: none; }}
    .login-box {{
      max-width: 380px; margin: 3rem auto; background: var(--card);
      border: 1px solid var(--border); border-radius: 12px; padding: 1.5rem;
    }}
    label {{ display: block; color: var(--muted); font-size: 0.85rem; margin-bottom: 0.35rem; }}
    input[type=password] {{
      width: 100%; padding: 0.65rem 0.75rem; border-radius: 8px; border: 1px solid var(--border);
      background: #0f1419; color: var(--text); font-size: 1rem;
    }}
    button {{
      margin-top: 0.9rem; width: 100%; padding: 0.65rem; border: none; border-radius: 8px;
      background: var(--accent); color: white; font-weight: 600; cursor: pointer; font-size: 0.95rem;
    }}
    button:hover {{ filter: brightness(1.08); }}
    .nav-form {{ margin: 0; }}
    .nav-form button {{
      width: auto; margin: 0; padding: 0.4rem 0.8rem; background: transparent;
      border: 1px solid var(--border); color: var(--muted);
    }}
    .error {{ color: var(--bad); font-size: 0.9rem; margin-top: 0.75rem; }}
    .muted {{ color: var(--muted); }}
    .alert-box {{
      background: var(--card); border: 1px solid var(--border); border-radius: 10px;
      padding: 0.9rem 1rem; font-size: 0.9rem;
    }}
  </style>
</head>
<body>
  <header>
    <h1>Paper trading dashboard</h1>
    {nav}
  </header>
  <main>
    {body}
  </main>
</body>
</html>"""


def _login_page(error: Optional[str] = None) -> HTMLResponse:
    err = f'<p class="error">{escape(error)}</p>' if error else ""
    body = f"""
    <div class="login-box">
      <p class="muted">Enter the webhook secret once. It is stored as an HttpOnly session cookie — never in the URL.</p>
      <form method="post" action="/dashboard/login">
        <label for="secret">Webhook secret</label>
        <input id="secret" name="secret" type="password" autocomplete="current-password" required autofocus/>
        <button type="submit">Sign in</button>
      </form>
      {err}
    </div>
    """
    return HTMLResponse(_layout("Dashboard login", body), status_code=401 if error else 200)


def _fmt_pct(v: float) -> str:
    cls = "pos" if v >= 0 else "neg"
    sign = "+" if v > 0 else ""
    return f'<span class="{cls}">{sign}{v:.2f}%</span>'


def _fmt_money(v: float) -> str:
    return f"{v:,.2f}"


def _dashboard_page(
    settings: Settings,
    state: PortfolioState,
    executor: TradeExecutor,
) -> HTMLResponse:
    state.reset_day_if_needed()
    state.mark_equity()
    mode = settings.trading_mode
    badge = f'<span class="badge {escape(mode)}">{escape(mode)}</span>'
    pnl_pct = state.daily_pnl_pct
    pnl_usdt = state.daily_realized_pnl_usdt

    pos_rows = []
    for sym, qty in sorted(state.open_positions.items()):
        if abs(qty) <= 1e-12:
            continue
        entry = state.avg_entry.get(sym)
        px = state.prices.get(sym)
        notional = (qty * px) if px is not None else None
        u_pnl = None
        if entry is not None and px is not None:
            u_pnl = (px - entry) * qty
        u_cell = _fmt_money(u_pnl) if u_pnl is not None else "—"
        if u_pnl is not None:
            u_cls = "pos" if u_pnl >= 0 else "neg"
            u_cell = f'<span class="{u_cls}">{u_cell}</span>'
        pos_rows.append(
            "<tr>"
            f"<td>{escape(sym)}</td>"
            f"<td>{qty:.6g}</td>"
            f"<td>{_fmt_money(entry) if entry is not None else '—'}</td>"
            f"<td>{_fmt_money(px) if px is not None else '—'}</td>"
            f"<td>{_fmt_money(notional) if notional is not None else '—'}</td>"
            f"<td>{u_cell}</td>"
            "</tr>"
        )
    positions_html = (
        "<table><thead><tr>"
        "<th>Symbol</th><th>Qty</th><th>Avg entry</th><th>Mark</th><th>Notional</th><th>Unrealized</th>"
        "</tr></thead><tbody>"
        + (
            "".join(pos_rows)
            if pos_rows
            else '<tr><td colspan="6" class="muted">No open positions</td></tr>'
        )
        + "</tbody></table>"
    )

    trades = list(executor.recent)[:50]
    last = trades[0] if trades else None
    if last:
        last_html = (
            "<div class='alert-box'>"
            f"<strong>{escape(last.side.value.upper())}</strong> {escape(last.symbol)} "
            f"qty={last.qty:.6g} @ {escape(str(last.price) if last.price is not None else 'n/a')} "
            f"— <span class='muted'>{escape(last.status.value)}</span> "
            f"<span class='muted'>({escape(last.created_at.isoformat())})</span>"
            f"<br/><span class='muted'>alert_id={escape(last.alert_id)}</span>"
            "</div>"
        )
    else:
        last_html = "<p class='muted'>No alerts / trades yet.</p>"

    trade_rows = []
    for t in trades:
        trade_rows.append(
            "<tr>"
            f"<td>{escape(t.created_at.strftime('%Y-%m-%d %H:%M:%S'))}</td>"
            f"<td>{escape(t.symbol)}</td>"
            f"<td>{escape(t.side.value)}</td>"
            f"<td>{t.qty:.6g}</td>"
            f"<td>{escape(str(t.price) if t.price is not None else '—')}</td>"
            f"<td>{escape(t.status.value)}</td>"
            f"<td class='muted'>{escape(t.reason or '—')}</td>"
            "</tr>"
        )
    trades_html = (
        "<table><thead><tr>"
        "<th>Time (UTC)</th><th>Symbol</th><th>Side</th><th>Qty</th><th>Price</th><th>Status</th><th>Reason</th>"
        "</tr></thead><tbody>"
        + (
            "".join(trade_rows)
            if trade_rows
            else '<tr><td colspan="7" class="muted">Empty trade log</td></tr>'
        )
        + "</tbody></table>"
    )

    body = f"""
    <div class="cards">
      <div class="card"><div class="label">Mode</div><div class="value">{badge}</div></div>
      <div class="card"><div class="label">Equity (USDT)</div><div class="value">{_fmt_money(state.equity_usdt)}</div></div>
      <div class="card"><div class="label">Open positions</div><div class="value">{state.open_count}</div></div>
      <div class="card"><div class="label">Daily PnL</div><div class="value">{_fmt_pct(pnl_pct)} <span class="muted" style="font-size:.85rem">({_fmt_money(pnl_usdt)} USDT)</span></div></div>
      <div class="card"><div class="label">Cash (USDT)</div><div class="value">{_fmt_money(state.cash_usdt or 0)}</div></div>
    </div>

    <h2>Last alert</h2>
    {last_html}

    <h2>Open positions</h2>
    {positions_html}

    <h2>Trade log</h2>
    {trades_html}
    """
    return HTMLResponse(_layout("Paper dashboard", body, authed=True))


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(
    request: Request,
    settings: Settings = Depends(get_settings),
    state: PortfolioState = Depends(get_portfolio),
    executor: TradeExecutor = Depends(get_executor),
) -> HTMLResponse:
    if not is_dashboard_authed(request, settings):
        return _login_page()
    return _dashboard_page(settings, state, executor)


@router.post("/dashboard/login")
async def dashboard_login(
    request: Request,
    secret: str = Form(...),
    settings: Settings = Depends(get_settings),
) -> Response:
    if not secrets_equal(secret, settings.webhook_secret):
        return _login_page(error="Invalid webhook secret")
    resp = RedirectResponse(url="/dashboard", status_code=303)
    resp.set_cookie(
        key=COOKIE_NAME,
        value=session_token(settings.webhook_secret),
        httponly=True,
        samesite="lax",
        max_age=COOKIE_MAX_AGE,
        secure=request.url.scheme == "https",
        path="/",
    )
    return resp


@router.post("/dashboard/logout")
async def dashboard_logout() -> Response:
    resp = RedirectResponse(url="/dashboard", status_code=303)
    resp.delete_cookie(COOKIE_NAME, path="/")
    return resp
