"""Runtime configuration — read from environment variables with safe defaults.

Copy .env.example to .env and set values before deploying.
The systemd unit file sources /etc/bus-client/env.
"""

from __future__ import annotations

import os

# ── Server ──────────────────────────────────────────────────────────────────
SERVER_URL: str = os.environ.get(
    "BUS_SERVER_URL", "https://bus.example.com"
).rstrip("/")
"""Base HTTPS URL of the FastAPI server, no trailing slash."""

API_TOKEN: str = os.environ.get("BUS_API_TOKEN", "")
"""Bearer token assigned to this bus by the admin interface."""

# ── GPS ─────────────────────────────────────────────────────────────────────
GPSD_HOST: str = os.environ.get("GPSD_HOST", "127.0.0.1")
GPSD_PORT: int = int(os.environ.get("GPSD_PORT", "2947"))

# ── Timing ──────────────────────────────────────────────────────────────────
LOOP_INTERVAL_S: float = float(os.environ.get("LOOP_INTERVAL_S", "5"))
"""Seconds between position sends (spec §6.2: 5 s ± 500 ms)."""

HTTP_TIMEOUT_S: float = float(os.environ.get("HTTP_TIMEOUT_S", "8"))
"""Per-request HTTP timeout in seconds."""

# ── Buffer ──────────────────────────────────────────────────────────────────
BUFFER_DB_PATH: str = os.environ.get(
    "BUFFER_DB_PATH", "/var/lib/bus-client/buffer.db"
)
BUFFER_MAX_ENTRIES: int = int(os.environ.get("BUFFER_MAX_ENTRIES", "1000"))
"""Maximum rows kept in the offline SQLite buffer (spec §6.2)."""

# ── TLS ─────────────────────────────────────────────────────────────────────
TLS_CA_BUNDLE: str | None = os.environ.get("TLS_CA_BUNDLE") or None
"""Path to a custom CA bundle (PEM) — leave unset to use the system store."""

# ── Logging ─────────────────────────────────────────────────────────────────
LOG_DIR: str = os.environ.get("LOG_DIR", "/var/log/bus-client")
LOG_LEVEL: str = os.environ.get("LOG_LEVEL", "INFO").upper()
LOG_RETENTION_DAYS: int = int(os.environ.get("LOG_RETENTION_DAYS", "7"))
