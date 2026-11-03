from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field

class ResourceCreateRequest(BaseModel):
    slug: str
    title: str
    description: str
    resource_type: str = "product_intelligence"
    provider: str = "channel3"
    metadata: Dict[str, Any] = {}

class OfferCreateRequest(BaseModel):
    offer_code: str
    title: str
    description: str
    price_amount: float
    currency: str = "USD"
    pricing_model: str = "one_time"
    duration_seconds: int = 3600
    scope: Dict[str, Any] = {"access": "read"}

class ResourceResponse(BaseModel):
    id: str
    slug: str
    title: str
    description: str
    resource_type: str
    provider: str
    status: str
    created_at: str

class OfferResponse(BaseModel):
    id: str
    resource_id: str
    offer_code: str
    title: str
    description: str
    price_amount: float
    currency: str
    pricing_model: str
    duration_seconds: int
    active: bool
