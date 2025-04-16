import pytest
from httpx import AsyncClient
from fastapi import FastAPI
from app.main import app
from app.core.redis import init_redis, get_redis
import asyncio

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def redis_client():
    """Create a Redis client for testing."""
    await init_redis()
    redis = await get_redis()
    yield redis
    await redis.close()

@pytest.fixture
async def client():
    """Create a test client for the FastAPI application."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.fixture(autouse=True)
async def clear_redis(redis_client):
    """Clear Redis before each test."""
    await redis_client.flushdb() 