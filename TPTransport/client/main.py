"""Bus-client main loop — spec §6.2.

Main loop (every LOOP_INTERVAL_S, default 5 s):
  1. Read GPS fix from gpsd.
  2. If valid fix   → POST to server; on network failure push to buffer.
  3. If no fix      → log and skip (server will detect the silence).
  4. On every cycle after a successful send → drain the offline buffer.
  5. Sleep for the remainder of the interval.

Exit codes
----------
0  — clean shutdown (SIGINT / SIGTERM)
1  — fatal configuration error (missing token, etc.)
"""

from __future__ import annotations

import logging
import signal
import sys
import time

import client.config as cfg
from client.buffer import OfflineBuffer
from client.gps import read_fix
from client.logger import configure as configure_logging
from client.sender import Sender

log = logging.getLogger(__name__)

_SHUTDOWN = False


def _handle_signal(signum, frame) -> None:  # noqa: ANN001
    global _SHUTDOWN
    log.info("Signal %d received — shutting down gracefully…", signum)
    _SHUTDOWN = True


def _validate_config() -> None:
    if not cfg.API_TOKEN:
        log.critical(
            "BUS_API_TOKEN is not set. "
            "Set it in /etc/bus-client/env before starting the service."
        )
        sys.exit(1)
    if not cfg.SERVER_URL or cfg.SERVER_URL == "https://bus.example.com":
        log.warning(
            "BUS_SERVER_URL is not configured or still set to the placeholder. "
            "Positions will fail until a real URL is provided."
        )


def main() -> None:
    configure_logging(cfg.LOG_DIR, cfg.LOG_LEVEL, cfg.LOG_RETENTION_DAYS)
    log.info("bus-client starting up")
    log.info(
        "Config: server=%s gpsd=%s:%d interval=%.1fs buffer=%s (max %d)",
        cfg.SERVER_URL, cfg.GPSD_HOST, cfg.GPSD_PORT,
        cfg.LOOP_INTERVAL_S, cfg.BUFFER_DB_PATH, cfg.BUFFER_MAX_ENTRIES,
    )

    _validate_config()

    signal.signal(signal.SIGTERM, _handle_signal)
    signal.signal(signal.SIGINT,  _handle_signal)

    buffer = OfflineBuffer(cfg.BUFFER_DB_PATH, cfg.BUFFER_MAX_ENTRIES)
    sender = Sender(
        server_url=cfg.SERVER_URL,
        token=cfg.API_TOKEN,
        buffer=buffer,
        timeout_s=cfg.HTTP_TIMEOUT_S,
        ca_bundle=cfg.TLS_CA_BUNDLE,
    )

    log.info("Entering main loop (interval=%.1f s)", cfg.LOOP_INTERVAL_S)

    while not _SHUTDOWN:
        cycle_start = time.monotonic()

        # Step 1 — read GPS
        fix = read_fix(cfg.GPSD_HOST, cfg.GPSD_PORT)

        if fix is not None:
            log.debug(
                "Fix: lat=%.6f lon=%.6f speed=%s km/h heading=%s°",
                fix.latitude, fix.longitude, fix.speed_kmh, fix.heading,
            )
            # Step 2 — send (buffers automatically on failure)
            sender.send_fix(fix)
        else:
            # Step 3 — no valid fix; server will detect silence
            log.debug("No GPS fix — skipping this cycle")

        # Step 5 — sleep for the remainder of the interval
        elapsed = time.monotonic() - cycle_start
        sleep_s = max(0.0, cfg.LOOP_INTERVAL_S - elapsed)
        if sleep_s > 0 and not _SHUTDOWN:
            time.sleep(sleep_s)

    log.info("bus-client stopped")


if __name__ == "__main__":
    main()
