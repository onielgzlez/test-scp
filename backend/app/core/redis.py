from redis import asyncio as aioredis
from loguru import logger

from app.core.config import settings

redis_client = None

async def init_redis():
    """Initialize Redis connection."""
    global redis_client
    try:
        redis_client = aioredis.Redis(
            host=settings.redis_host,
            port=settings.redis_port,
            db=settings.redis_db,
            decode_responses=True
        )
        # Test the connection
        await redis_client.ping()
        logger.info("Redis connection established successfully")
    except Exception as e:
        logger.error(f"Failed to connect to Redis: {str(e)}")
        raise

async def get_redis():
    """Get Redis client instance."""
    if redis_client is None:
        await init_redis()
    return redis_client 