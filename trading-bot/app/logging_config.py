"""Structured logging setup."""

from __future__ import annotations

import logging
import sys


def setup_logging(level: str = "INFO") -> None:
    root = logging.getLogger()
    if root.handlers:
        root.setLevel(level.upper())
        return

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        logging.Formatter(
            fmt='{"time":"%(asctime)s","level":"%(levelname)s","logger":"%(name)s","msg":%(message)s}',
            datefmt="%Y-%m-%dT%H:%M:%S%z",
        )
    )
    root.addHandler(handler)
    root.setLevel(level.upper())

    # Quiet noisy libs
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)


def log_event(logger: logging.Logger, event: str, **fields: object) -> None:
    parts = [f'"event":"{event}"']
    for k, v in fields.items():
        if isinstance(v, str):
            parts.append(f'"{k}":"{v}"')
        elif v is None:
            parts.append(f'"{k}":null')
        else:
            parts.append(f'"{k}":{v}')
    logger.info("{" + ",".join(parts) + "}")
