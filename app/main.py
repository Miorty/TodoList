from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.databaseTD import engine
from app.logger import log_requests
from app.models import Base
from app.router_tasks import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()

app = FastAPI(lifespan=lifespan)

app.include_router(router)

app.middleware("http")(log_requests)

# app = FastAPI()
#
# app.include_router(router)
#
# app.middleware("http")(log_requests)
#
# @app.on_event("startup")
# async def startup():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)