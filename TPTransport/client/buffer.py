"""SQLite offline buffer — spec §6.2.

Stores up to BUFFER_MAX_ENTRIES GPS fixes when the server is unreachable.
On the next successful HTTP cycle the oldest rows are drained and sent first.

Schema
------
    CREATE TABLE buffer (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        latitude    REAL    NOT NULL,
        longitude   REAL    NOT NULL,
        speed_kmh   REAL,
        heading     REAL,
        recorded_at TEXT    NOT NULL   -- ISO-8601 with timezone
    );

All operations are synchronous (called from the main thread, never concurrently).
"""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterator


@dataclass(frozen=True, slots=True)
class BufferedFix:
    rowid: int
    latitude: float
    longitude: float
    speed_kmh: float | None
    heading: float | None
    recorded_at: str   # ISO-8601


_DDL = """
CREATE TABLE IF NOT EXISTS buffer (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    latitude    REAL    NOT NULL,
    longitude   REAL    NOT NULL,
    speed_kmh   REAL,
    heading     REAL,
    recorded_at TEXT    NOT NULL
);
"""


class OfflineBuffer:
    """Thread-safe wrapper around a local SQLite file.

    Parameters
    ----------
    db_path:
        Filesystem path to the SQLite database file.
        Parent directory is created automatically if needed.
    max_entries:
        Hard cap on stored rows.  When full, the *oldest* row is evicted
        before inserting a new one (FIFO ring-buffer behaviour).
    """

    def __init__(self, db_path: str, max_entries: int = 1000) -> None:
        path = Path(db_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        self._path = str(path)
        self._max = max_entries
        self._init_db()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def push(
        self,
        latitude: float,
        longitude: float,
        speed_kmh: float | None,
        heading: float | None,
        recorded_at: datetime,
    ) -> None:
        """Append a fix to the buffer, evicting the oldest if at capacity."""
        ts = recorded_at.isoformat()
        with self._conn() as conn:
            count = conn.execute("SELECT COUNT(*) FROM buffer").fetchone()[0]
            if count >= self._max:
                # Evict oldest
                conn.execute(
                    "DELETE FROM buffer WHERE id = (SELECT MIN(id) FROM buffer)"
                )
            conn.execute(
                "INSERT INTO buffer (latitude, longitude, speed_kmh, heading, recorded_at)"
                " VALUES (?, ?, ?, ?, ?)",
                (latitude, longitude, speed_kmh, heading, ts),
            )

    def drain(self, batch: int = 50) -> list[BufferedFix]:
        """Return the *batch* oldest rows without deleting them yet.

        Call ``ack(rowids)`` after successful transmission.
        """
        with self._conn() as conn:
            rows = conn.execute(
                "SELECT id, latitude, longitude, speed_kmh, heading, recorded_at"
                " FROM buffer ORDER BY id ASC LIMIT ?",
                (batch,),
            ).fetchall()
        return [BufferedFix(*r) for r in rows]

    def ack(self, rowids: list[int]) -> None:
        """Delete rows that were successfully sent."""
        if not rowids:
            return
        placeholders = ",".join("?" * len(rowids))
        with self._conn() as conn:
            conn.execute(
                f"DELETE FROM buffer WHERE id IN ({placeholders})", rowids
            )

    def __len__(self) -> int:
        with self._conn() as conn:
            return conn.execute("SELECT COUNT(*) FROM buffer").fetchone()[0]

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _init_db(self) -> None:
        with self._conn() as conn:
            conn.executescript(_DDL)

    def _conn(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self._path, timeout=10)
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA synchronous=NORMAL")
        return conn
