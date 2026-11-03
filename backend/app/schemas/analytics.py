from typing import List, Optional, Dict, Any
from pydantic import BaseModel

class AnalyticsSummaryResponse(BaseModel):
    total_revenue_usd: float
    captured_transactions_count: int
    active_entitlements_count: int
    unique_agents_count: int
    conversion_rate_pct: float
    total_usage_events: int

class TransactionItemResponse(BaseModel):
    id: str
    paypal_order_id: str
    paypal_capture_id: str
    amount: float
    currency: str
    status: str
    resource_title: str
    resource_slug: str
    captured_at: str

class PaginatedTransactionsResponse(BaseModel):
    total: int
    items: List[TransactionItemResponse]

class UsageItemResponse(BaseModel):
    id: str
    resource_slug: str
    event_type: str
    units: int
    created_at: str

class PaginatedUsageResponse(BaseModel):
    total: int
    items: List[UsageItemResponse]
