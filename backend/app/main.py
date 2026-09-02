from __future__ import annotations

import asyncio
import logging
import json

import datetime

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.event_detector import diff_events
from app.livescore_client import LEAGUE_ID_MAP, get_client
from app.social_poster import broadcast_to_social
from app.websocket_manager import manager

from app.redis_client import cache_live_matches, get_cached_live_matches

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("livepitch")

app = FastAPI(title="LivePitch API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory snapshot of the last poll, keyed by fixture id.
# For multi-instance deployments, replace this with Redis so every
# worker/process shares the same "previous state".
_last_snapshot: dict[str, dict] = {}


@app.get("/api/fixtures/live")
async def get_live_fixtures():
    """Serve cached live matches to reduce backend processing load."""
    cached_data = await get_cached_live_matches()
    if cached_data is not None:
        return {"matches": cached_data, "source": "redis_cache"}

    return {"matches": list(_last_snapshot.values()), "source": "memory"}

_standings_cache: dict[str, dict] = {}
STANDINGS_CACHE_SECONDS = 60 * 30  # standings only need refreshing a few times a day

@app.get("/api/standings/{league_id}")
async def get_standings(league_id: str, season: int | None = None):
    """
    league_id is our internal slug (pl, laliga, seriea, ...) — see
    LEAGUE_ID_MAP in app/livescore_client.py. Cached for 30 minutes since
    a table doesn't meaningfully change mid-poll-cycle.
    """
    if league_id not in LEAGUE_ID_MAP:
        return {"standings": [], "error": f"Unknown league_id '{league_id}'"}

    season = season or datetime.date.today().year
    cache_key = f"{league_id}:{season}"
    cached = _standings_cache.get(cache_key)
    now = datetime.datetime.utcnow()

    if cached and (now - cached["fetched_at"]).total_seconds() < STANDINGS_CACHE_SECONDS:
        return {"standings": cached["data"]}

    try:
        client = get_client()
        standings = await client.fetch_standings(LEAGUE_ID_MAP[league_id], season)
        _standings_cache[cache_key] = {"data": standings, "fetched_at": now}
        return {"standings": standings}
    except Exception:
        logger.exception("Failed to fetch standings for %s", league_id)
        # Serve stale cache rather than nothing, if we have it.
        if cached:
            return {"standings": cached["data"]}
        return {"standings": [], "error": "Could not fetch standings right now"}

@app.websocket("/ws/live")
async def ws_live(websocket: WebSocket):
    await manager.connect(websocket)
    # Send the current snapshot immediately so new clients aren't empty.
    await websocket.send_json({"type": "snapshot", "matches": list(_last_snapshot.values())})
    try:
        while True:
            # We don't expect client messages, but keep the connection open.
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)


async def poll_loop() -> None:
    """
    Background task: polls the live-score provider on an interval,
    diffs against the last known state per fixture, and for anything
    new — broadcasts to connected websocket clients and posts to social.
    """
    client = get_client()
    while True:
        try:
            # 1. Fetch fresh data from provider (or mock)
            fixtures = await client.fetch_live_fixtures()

            # 2. Store live snapshot in Redis cache with short TTL
            await cache_live_matches(fixtures)
            # 3. Detect state changes against in-memory or Redis state
            for match in fixtures:
                previous = _last_snapshot.get(match["id"])
                new_events = diff_events(previous, match)

                _last_snapshot[match["id"]] = match

                # 4. Push updates to connected WebSockets
                if new_events:
                    await manager.broadcast({"type": "update", "match": match})
                    for event in new_events:
                        await broadcast_to_social(match, event)

        except Exception:
            logger.exception("Poll loop error")

        await asyncio.sleep(settings.POLL_INTERVAL_SECONDS)


@app.on_event("startup")
async def start_background_tasks():
    asyncio.create_task(poll_loop())
