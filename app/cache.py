from redis import asyncio as aioredis
from config import settings

redis_client = aioredis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)

async def get_cache():
    return redis_client

async def cache_task(task):
    return {
        "id": task.id,
        "title": task.title,
        "isCompleted": task.isCompleted,
        "created_at": task.created_at.isoformat(),
    }