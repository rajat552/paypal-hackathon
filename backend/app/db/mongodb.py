import logging
from typing import Any
import certifi
from pymongo import MongoClient

from backend.app.core.config import settings

logger = logging.getLogger(__name__)

_mongo_client: MongoClient | None = None


def get_mongo_client() -> MongoClient | None:
    """Return a singleton MongoClient instance if MONGODB_URI is configured."""
    global _mongo_client
    if not settings.MONGODB_URI:
        return None
    if _mongo_client is None:
        try:
            _mongo_client = MongoClient(
                settings.MONGODB_URI,
                tlsCAFile=certifi.where(),
                serverSelectionTimeoutMS=4000,
                connectTimeoutMS=4000
            )
        except Exception as e:
            logger.warning(f"Failed to initialize MongoDB client: {e}")
            return None
    return _mongo_client


def check_mongo_health() -> dict[str, Any]:
    """Verify MongoDB connectivity and return cluster information."""
    if not settings.MONGODB_URI:
        return {"status": "unconfigured"}
    try:
        client = get_mongo_client()
        if client is None:
            return {"status": "unconfigured"}
        info = client.server_info()
        db = client.get_default_database()
        db_name = db.name if db is not None else "unknown"
        return {
            "status": "connected",
            "server_version": info.get("version"),
            "database": db_name,
        }
    except Exception as e:
        logger.warning(f"MongoDB health check failed: {e}")
        return {"status": "unreachable", "error": str(e)}


def log_mongo_audit_event(event_type: str, details: dict[str, Any]) -> bool:
    """Record an audit or transaction event into MongoDB Atlas collection."""
    try:
        client = get_mongo_client()
        if client is None:
            return False
        db = client.get_default_database()
        if db is None:
            return False
        collection = db["auditevents"]
        doc = {
            "event_type": event_type,
            "details": details,
            "source": "paymesh-ai",
            "cluster": "atlas-cohesora"
        }
        collection.insert_one(doc)
        return True
    except Exception as e:
        logger.warning(f"MongoDB audit log insert skipped: {e}")
        return False
