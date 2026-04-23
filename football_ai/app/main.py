from fastapi import FastAPI

from app.api.routes.games import router as games_router
from app.api.routes.health import router as health_router
from app.api.routes.ingest import router as ingest_router

app = FastAPI(title="Football AI Backend")
app.include_router(health_router)
app.include_router(ingest_router)
app.include_router(games_router)
