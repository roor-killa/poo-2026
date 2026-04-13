"""HTTP sender — POST fixes to the server and drain the offline buffer.

Responsibilities
----------------
1. POST a single fix to ``POST /api/v1/positions`` with Bearer-token auth.
2. On HTTP success, drain the SQLite buffer and replay stored fixes FIFO.
3. On any network / server error, push the fix into the buffer instead.

Error mapping (spec §3.1)
--------------------------
- 401 — token rejected: log CRITICAL, do NOT buffer (fix won't be accepted later).
- 422 — invalid payload: log ERROR, do NOT buffer (re-sending won't help).
- 429 — rate limited: log WARNING, buffer the fix.
- 5xx / network error: log WARNING, buffer the fix.
"""

from __future__ import annotations

import json
import logging
from dataclasses import asdict
from datetime import datetime

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from client.buffer import BufferedFix, OfflineBuffer
from client.gps import GpsFix

log = logging.getLogger(__name__)

_ENDPOINT = "/api/v1/positions"

# Retry only on connection errors, not on HTTP status codes
# (status-code retries are handled explicitly below)
_RETRY = Retry(total=2, backoff_factor=0.3, status_forcelist=(), raise_on_status=False)


def _session(token: str, ca_bundle: str | None) -> requests.Session:
    s = requests.Session()
    s.headers["Authorization"] = f"Bearer {token}"
    s.headers["Content-Type"] = "application/json"
    s.verify = ca_bundle if ca_bundle else True
    adapter = HTTPAdapter(max_retries=_RETRY)
    s.mount("https://", adapter)
    s.mount("http://", adapter)
    return s


def _fix_payload(
    latitude: float,
    longitude: float,
    speed_kmh: float | None,
    heading: float | None,
    recorded_at: str | datetime,
) -> str:
    if isinstance(recorded_at, datetime):
        recorded_at = recorded_at.isoformat()
    return json.dumps({
        "latitude": latitude,
        "longitude": longitude,
        "speed_kmh": speed_kmh,
        "heading": heading,
        "recorded_at": recorded_at,
    })


class Sender:
    """Stateless HTTP sender.  Re-create the session once and reuse it."""

    def __init__(
        self,
        server_url: str,
        token: str,
        buffer: OfflineBuffer,
        timeout_s: float = 8.0,
        ca_bundle: str | None = None,
    ) -> None:
        self._url = server_url.rstrip("/") + _ENDPOINT
        self._buffer = buffer
        self._timeout = timeout_s
        self._session = _session(token, ca_bundle)

    # ------------------------------------------------------------------
    # Public
    # ------------------------------------------------------------------

    def send_fix(self, fix: GpsFix) -> None:
        """Try to POST ``fix``.  On failure push it to the offline buffer."""
        success = self._post(
            fix.latitude, fix.longitude,
            fix.speed_kmh, fix.heading, fix.recorded_at,
        )
        if success:
            self._drain_buffer()
        else:
            self._buffer.push(
                fix.latitude, fix.longitude,
                fix.speed_kmh, fix.heading, fix.recorded_at,
            )
            log.info(
                "Fix buffered (buffer size=%d/%d)",
                len(self._buffer), self._buffer._max,
            )

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _post(
        self,
        latitude: float,
        longitude: float,
        speed_kmh: float | None,
        heading: float | None,
        recorded_at: str | datetime,
    ) -> bool:
        """Return True on HTTP 201, False on retriable errors.

        Raises nothing — all exceptions are caught and logged.
        """
        payload = _fix_payload(latitude, longitude, speed_kmh, heading, recorded_at)
        try:
            resp = self._session.post(self._url, data=payload, timeout=self._timeout)
        except requests.RequestException as exc:
            log.warning("Network error: %s", exc)
            return False

        if resp.status_code == 201:
            log.debug("Position accepted (server_time=%s)", resp.json().get("server_time"))
            return True

        if resp.status_code == 401:
            log.critical(
                "Server rejected token (401) — check BUS_API_TOKEN. "
                "Fix will NOT be buffered."
            )
            return True   # return True to avoid buffering an unfixable error

        if resp.status_code == 422:
            log.error(
                "Server rejected payload (422): %s — fix discarded.",
                resp.text[:200],
            )
            return True   # don't buffer; re-sending won't help

        if resp.status_code == 429:
            retry_after = resp.headers.get("Retry-After", "?")
            log.warning("Rate limited (429) — Retry-After: %s s", retry_after)
            return False

        log.warning("Unexpected HTTP %d: %s", resp.status_code, resp.text[:120])
        return False

    def _drain_buffer(self) -> None:
        """Replay buffered fixes FIFO.  Stops on first failure."""
        batch = self._buffer.drain(batch=50)
        if not batch:
            return
        log.info("Draining buffer (%d fixes)…", len(batch))
        sent: list[int] = []
        for fix in batch:
            ok = self._post(
                fix.latitude, fix.longitude,
                fix.speed_kmh, fix.heading, fix.recorded_at,
            )
            if ok:
                sent.append(fix.rowid)
            else:
                break   # server still unreachable; stop, try again next cycle
        self._buffer.ack(sent)
        if sent:
            log.info("Drained %d buffered fix(es)", len(sent))
