"""In-memory idempotency store for duplicate TradingView alerts."""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass


@dataclass
class _Entry:
    trade_id: str
    expires_at: float


class IdempotencyStore:
    """Thread-safe TTL map of alert_id -> trade_id."""

    def __init__(self, ttl_seconds: int = 86_400) -> None:
        self._ttl = ttl_seconds
        self._lock = threading.Lock()
        self._seen: dict[str, _Entry] = {}

    def _purge_locked(self, now: float) -> None:
        expired = [k for k, e in self._seen.items() if e.expires_at <= now]
        for k in expired:
            del self._seen[k]

    def seen(self, alert_id: str) -> str | None:
        """Return prior trade_id if alert already processed, else None."""
        now = time.monotonic()
        with self._lock:
            self._purge_locked(now)
            entry = self._seen.get(alert_id)
            if entry and entry.expires_at > now:
                return entry.trade_id
            return None

    def mark(self, alert_id: str, trade_id: str) -> bool:
        """
        Record alert_id. Returns True if newly marked, False if already present.
        """
        now = time.monotonic()
        with self._lock:
            self._purge_locked(now)
            if alert_id in self._seen and self._seen[alert_id].expires_at > now:
                return False
            self._seen[alert_id] = _Entry(trade_id=trade_id, expires_at=now + self._ttl)
            return True

    def clear(self) -> None:
        with self._lock:
            self._seen.clear()
