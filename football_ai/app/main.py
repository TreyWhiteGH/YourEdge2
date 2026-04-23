from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes.games import router as games_router
from app.api.routes.health import router as health_router
from app.api.routes.ingest import client as ingest_client
from app.api.routes.ingest import router as ingest_router


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    try:
        yield
    finally:
        ingest_client.close()


app = FastAPI(title="Football AI Backend", lifespan=lifespan)
app.include_router(health_router)
app.include_router(ingest_router)
app.include_router(games_router)
