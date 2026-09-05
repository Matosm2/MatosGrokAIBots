"""Idempotency store for duplicate TradingView alerts (memory + optional disk)."""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from app.persistence import JsonStore


@dataclass
class _Entry:
    trade_id: str
    expires_at: float  # monotonic for TTL checks
    wall_expires_at: float  # time.time() for persistence


class IdempotencyStore:
    """
    Thread-safe TTL map of alert_id -> trade_id.

    Use claim()/commit()/abort() under an external asyncio lock to avoid
    check-then-act (TOCTOU) races with concurrent webhook handlers.
    """

    def __init__(
        self,
        ttl_seconds: int = 86_400,
        store: Optional["JsonStore"] = None,
        filename: str = "idempotency.json",
    ) -> None:
        self._ttl = ttl_seconds
        self._lock = threading.Lock()
        self._seen: dict[str, _Entry] = {}
        self._pending: set[str] = set()
        self._store = store
        self._filename = filename
        self._load()

    def _load(self) -> None:
        if not self._store or not self._store.enabled:
            return
        raw = self._store.load(self._filename, default={})
        if not isinstance(raw, dict):
            return
        now_wall = time.time()
        now_mono = time.monotonic()
        with self._lock:
            for alert_id, meta in raw.items():
                if not isinstance(meta, dict):
                    continue
                wall_exp = float(meta.get("wall_expires_at", 0))
                if wall_exp <= now_wall:
                    continue
                remaining = wall_exp - now_wall
                self._seen[str(alert_id)] = _Entry(
                    trade_id=str(meta.get("trade_id", "")),
                    expires_at=now_mono + remaining,
                    wall_expires_at=wall_exp,
                )

    def _persist_locked(self) -> None:
        if not self._store or not self._store.enabled:
            return
        now_mono = time.monotonic()
        payload = {
            k: {
                "trade_id": e.trade_id,
                "wall_expires_at": e.wall_expires_at,
            }
            for k, e in self._seen.items()
            if e.expires_at > now_mono
        }
        self._store.save(self._filename, payload)

    def _purge_locked(self, now: float) -> None:
        expired = [k for k, e in self._seen.items() if e.expires_at <= now]
        for k in expired:
            del self._seen[k]

    def seen(self, alert_id: str) -> str | None:
        """Return prior trade_id if alert already committed, else None."""
        now = time.monotonic()
        with self._lock:
            self._purge_locked(now)
            entry = self._seen.get(alert_id)
            if entry and entry.expires_at > now:
                return entry.trade_id
            return None

    def claim(self, alert_id: str) -> str | None:
        """
        Atomically begin processing an alert_id.

        Returns prior trade_id if already committed (duplicate),
        raises ConcurrentClaimError if another handler holds a pending claim,
        or None if this caller acquired the claim.
        """
        now = time.monotonic()
        with self._lock:
            self._purge_locked(now)
            entry = self._seen.get(alert_id)
            if entry and entry.expires_at > now:
                return entry.trade_id
            if alert_id in self._pending:
                raise ConcurrentClaimError(alert_id)
            self._pending.add(alert_id)
            return None

    def commit(self, alert_id: str, trade_id: str) -> None:
        """Finalize successful processing; persists if a store is configured."""
        now = time.monotonic()
        wall = time.time()
        with self._lock:
            self._purge_locked(now)
            self._pending.discard(alert_id)
            self._seen[alert_id] = _Entry(
                trade_id=trade_id,
                expires_at=now + self._ttl,
                wall_expires_at=wall + self._ttl,
            )
            self._persist_locked()

    def abort(self, alert_id: str) -> None:
        """Release pending claim so a failed live order can be retried."""
        with self._lock:
            self._pending.discard(alert_id)

    def mark(self, alert_id: str, trade_id: str) -> bool:
        """
        Record alert_id (legacy helper). Returns True if newly marked.
        Prefer claim/commit/abort under an async lock for new code.
        """
        now = time.monotonic()
        wall = time.time()
        with self._lock:
            self._purge_locked(now)
            if alert_id in self._seen and self._seen[alert_id].expires_at > now:
                return False
            self._pending.discard(alert_id)
            self._seen[alert_id] = _Entry(
                trade_id=trade_id,
                expires_at=now + self._ttl,
                wall_expires_at=wall + self._ttl,
            )
            self._persist_locked()
            return True

    def clear(self) -> None:
        with self._lock:
            self._seen.clear()
            self._pending.clear()
            self._persist_locked()


class ConcurrentClaimError(RuntimeError):
    def __init__(self, alert_id: str) -> None:
        super().__init__(f"alert_id={alert_id} is already being processed")
        self.alert_id = alert_id
