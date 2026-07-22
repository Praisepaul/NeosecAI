from pymongo import MongoClient
from pymongo.errors import PyMongoError

from app.config.settings import settings
from app.core.logger import logger

client = MongoClient(
    settings.mongo_uri,
    serverSelectionTimeoutMS=settings.mongo_server_selection_timeout_ms,
    connectTimeoutMS=settings.mongo_connect_timeout_ms,
    socketTimeoutMS=settings.mongo_socket_timeout_ms,
    maxIdleTimeMS=settings.mongo_max_idle_time_ms,
    retryWrites=True,
    retryReads=True,
    tz_aware=True,
)

db = client[settings.database_name]


def verify_connection() -> None:
    """Fail fast on startup if MongoDB is unreachable, instead of
    discovering it on the first request."""

    try:
        client.admin.command("ping")
        logger.info(f"MongoDB connected -> database='{settings.database_name}'")

    except PyMongoError as error:
        logger.error(f"MongoDB connection failed: {error}")
        raise


def ensure_indexes() -> None:
    """Create required indexes. Idempotent - safe to call on every startup."""

    try:
        db.threats.create_index("cve", unique=True, name="uniq_cve")
        db.assets.create_index("hostname", unique=True, name="uniq_hostname")
        db.sync_state.create_index("collector", unique=True, name="uniq_collector")
        db.github_lookup_cache.create_index("cve", unique=True, name="uniq_cve_cache")

        logger.info("MongoDB indexes verified")

    except PyMongoError as error:
        logger.error(f"Failed to create MongoDB indexes: {error}")
        raise
