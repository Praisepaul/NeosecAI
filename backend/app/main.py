from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.config.settings import settings
from app.core.database import ensure_indexes, verify_connection
from app.core.logger import logger

app = FastAPI(title="NeoSOC AI API", version="1.0.0")

app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    logger.info("Starting NeoSOC AI API")
    verify_connection()
    ensure_indexes()


@app.get("/")
def root():
    return {"status": "running", "application": "NeoSOC AI"}
