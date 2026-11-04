from datetime import UTC, datetime

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db.session import get_db

router = APIRouter(tags=["Health"])

@router.get("/health")
async def health_check(session: AsyncSession = Depends(get_db)):
    db_status = "connected"
    try:
        await session.execute(text("SELECT 1"))
    except Exception as e:  # noqa: BLE001
        db_status = f"unhealthy: {e!s}"

    return {
        "status": "ok" if db_status == "connected" else "degraded",
        "app": "PayMesh AI — A Trust & Payment Infrastructure for Autonomous AI Commerce",
        "version": "2.0.0",
        "timestamp": datetime.now(UTC).isoformat(),
        "database": db_status
    }

