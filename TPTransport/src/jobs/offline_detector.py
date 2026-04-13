"""Asyncio background job — offline bus detection (spec §5.4).

Usage (from FastAPI lifespan):

    from src.jobs.offline_detector import OfflineDetector

    detector = OfflineDetector()

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        task = asyncio.create_task(detector.run())
        yield
        task.cancel()
        await asyncio.gather(task, return_exceptions=True)

The job runs every POLL_INTERVAL_S seconds (default 10).  For each bus in
bus_status it checks whether the time since last_seen_at exceeds
OFFLINE_THRESHOLD_S (30 s) and flips is_online accordingly.
"""

from __future__ import annotations

import asyncio
import logging
from datetime import datetime, timezone

from app.db.base import AsyncSessionLocal
from src.repositories import BusStatusRepository

logger = logging.getLogger(__name__)

POLL_INTERVAL_S: int = 10       # spec §5.4: run every 10 s
OFFLINE_THRESHOLD_S: int = 30   # spec §5.4
STALE_THRESHOLD_S: int = 300    # spec §5.4 — for logging/alerting only


class OfflineDetector:
    """Long-running asyncio task; safe to cancel."""

    async def run(self) -> None:
        logger.info("OfflineDetector started (interval=%ds)", POLL_INTERVAL_S)
        while True:
            try:
                await self._tick()
            except asyncio.CancelledError:
                logger.info("OfflineDetector cancelled")
                raise
            except Exception:
                logger.exception("OfflineDetector tick failed — will retry")
            await asyncio.sleep(POLL_INTERVAL_S)

    async def _tick(self) -> None:
        now = datetime.now(tz=timezone.utc)
        async with AsyncSessionLocal() as session:
            repo = BusStatusRepository(session)
            statuses = await repo.list_all()

            changed = 0
            for status in statuses:
                if status.last_seen_at is None:
                    # Never received a fix — keep offline
                    if status.is_online:
                        status.is_online = False
                        changed += 1
                    continue

                seen = status.last_seen_at
                if seen.tzinfo is None:
                    seen = seen.replace(tzinfo=timezone.utc)

                delta = (now - seen).total_seconds()

                if delta > OFFLINE_THRESHOLD_S:
                    if status.is_online:
                        status.is_online = False
                        logger.info(
                            "Bus %s went offline (silent for %.0fs)",
                            status.bus_id,
                            delta,
                        )
                        changed += 1
                    if delta > STALE_THRESHOLD_S:
                        logger.warning(
                            "Bus %s stale (%.0fs > %ds) — signal loss",
                            status.bus_id,
                            delta,
                            STALE_THRESHOLD_S,
                        )
                else:
                    if not status.is_online:
                        status.is_online = True
                        logger.info(
                            "Bus %s back online (last seen %.0fs ago)",
                            status.bus_id,
                            delta,
                        )
                        changed += 1

            if changed:
                await session.commit()
