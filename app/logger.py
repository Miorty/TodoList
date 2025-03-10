import logging
import time
from fastapi import Request
from redis import asyncio as aioredis
import json

redis_logging = aioredis.Redis(host="localhost", port=6379, db=1)

# Настройка логирования в файл
logging.basicConfig(level=logging.INFO, filename="py_log.log")

async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time

    log_entry = f"Request: {request.method} {request.url} - {duration:.3f} sec\n"

    # Вывод в консоль
    print(log_entry)

    logging.info(log_entry)

    # Формирование JSON-объекта лога
    log_entry = {
        "method": request.method,
        "url": str(request.url),
        "duration": round(duration, 4),
        "status_code": response.status_code,
    }

    # Сохраняем в Redis (добавляем запись в список logs)
    #await redis_logging.lpush("http_logs", json.dumps(log_entry))


    return response
