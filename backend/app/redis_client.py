import json
import logging
import redis.asyncio as aioredis
from app.config import settings

logger = logging.getLogger("livepitch")

redis_client = aioredis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    decode_responses=True
)

LIVE_SNAPSHOT_KEY = "livepitch:matches:live"
CACHE_TTL_LIVE = 10


async def cache_live_matches(matches: list[dict]):
    """Cache live match snapshots with short TTL, failing gracefully if Redis is down."""
    try:
        await redis_client.set(
            LIVE_SNAPSHOT_KEY,
            json.dumps(matches),
            ex=CACHE_TTL_LIVE
        )
    except Exception as e:
        logger.warning(f"Redis cache write skipped: {e}")


async def get_cached_live_matches() -> list[dict] | None:
    """Read live matches from Redis cache, returning None if Redis is unavailable."""
    try:
        data = await redis_client.get(LIVE_SNAPSHOT_KEY)
        logger.info(f"Redis cache data: {data}")
        if data:
            return json.loads(data)
    except Exception as e:
        logger.warning(f"Redis cache read skipped: {e}")
    return None