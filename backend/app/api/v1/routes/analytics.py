from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db.session import get_db
from backend.app.schemas.analytics import (
    AnalyticsSummaryResponse,
    PaginatedTransactionsResponse,
    PaginatedUsageResponse,
    TransactionItemResponse,
    UsageItemResponse,
)
from backend.app.services.analytics_service import analytics_service

router = APIRouter(prefix="/publisher/analytics", tags=["Publisher Analytics"])

@router.get("/summary", response_model=AnalyticsSummaryResponse)
async def get_analytics_summary(session: AsyncSession = Depends(get_db)):
    summary = await analytics_service.get_summary(session)
    return AnalyticsSummaryResponse(**summary)

@router.get("/transactions", response_model=PaginatedTransactionsResponse)
async def get_transactions(
    limit: int = 50,
    offset: int = 0,
    session: AsyncSession = Depends(get_db)
):
    items = await analytics_service.get_transactions(session, limit=limit, offset=offset)
    return PaginatedTransactionsResponse(
        total=len(items),
        items=[TransactionItemResponse(**item) for item in items]
    )

@router.get("/usage", response_model=PaginatedUsageResponse)
async def get_usage(
    limit: int = 50,
    offset: int = 0,
    session: AsyncSession = Depends(get_db)
):
    items = await analytics_service.get_usage_events(session, limit=limit, offset=offset)
    return PaginatedUsageResponse(
        total=len(items),
        items=[UsageItemResponse(**item) for item in items]
    )

