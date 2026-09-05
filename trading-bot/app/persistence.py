"""JSON persistence for portfolio state and idempotency map."""

from __future__ import annotations

import json
import logging
import os
import tempfile
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class JsonStore:
    """Atomic JSON file read/write under a data directory."""

    def __init__(self, data_dir: str | Path) -> None:
        self.root = Path(data_dir)
        if data_dir:
            self.root.mkdir(parents=True, exist_ok=True)

    @property
    def enabled(self) -> bool:
        return bool(str(self.root)) and str(self.root) not in (".", "")

    def path(self, name: str) -> Path:
        return self.root / name

    def load(self, name: str, default: Any = None) -> Any:
        if not self.enabled:
            return default
        path = self.path(name)
        if not path.exists():
            return default
        try:
            with path.open("r", encoding="utf-8") as f:
                return json.load(f)
        except (OSError, json.JSONDecodeError) as exc:
            logger.warning("Failed to load %s: %s", path, exc)
            return default

    def save(self, name: str, data: Any) -> None:
        if not self.enabled:
            return
        path = self.path(name)
        path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp_name = tempfile.mkstemp(
            dir=str(path.parent), prefix=f".{name}.", suffix=".tmp"
        )
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, sort_keys=True, default=str)
                f.write("\n")
            os.replace(tmp_name, path)
        except Exception:
            try:
                os.unlink(tmp_name)
            except OSError:
                pass
            raise
