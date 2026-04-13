"""Rotating log setup — /var/log/bus-client/ with 7-day retention (spec §6.3)."""

from __future__ import annotations

import logging
import logging.handlers
from pathlib import Path


def configure(log_dir: str, level: str = "INFO", retention_days: int = 7) -> None:
    """Configure the root logger with both a rotating file handler and stderr.

    Parameters
    ----------
    log_dir:
        Directory where ``bus-client.log`` is written.
        Created automatically if it does not exist.
    level:
        Log level string, e.g. ``"INFO"``, ``"DEBUG"``.
    retention_days:
        Number of daily log files to keep (spec §6.3: 7 days).
    """
    path = Path(log_dir)
    path.mkdir(parents=True, exist_ok=True)

    fmt = logging.Formatter(
        fmt="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
    )

    # Rotating file: one file per day, keep `retention_days` backups
    file_handler = logging.handlers.TimedRotatingFileHandler(
        filename=str(path / "bus-client.log"),
        when="midnight",
        backupCount=retention_days,
        encoding="utf-8",
        utc=True,
    )
    file_handler.setFormatter(fmt)

    # Console handler (captured by systemd journal)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(fmt)

    root = logging.getLogger()
    root.setLevel(getattr(logging, level, logging.INFO))
    root.addHandler(file_handler)
    root.addHandler(console_handler)
