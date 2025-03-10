from redis import asyncio as aioredis

redis_client = aioredis.Redis(host="localhost", port=6379, db=0)

async def get_cache():
    return redis_client

async def cache_task(task):
    return {
        "id": task.id,
        "title": task.title,
        "isCompleted": task.isCompleted,
        "created_at": task.created_at.isoformat(),
    }