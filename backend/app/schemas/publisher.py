from typing import Any

from pydantic import BaseModel, Field


class ResourceCreateRequest(BaseModel):
    slug: str = Field(..., min_length=2, max_length=120, pattern=r"^[a-zA-Z0-9_\-]+$")
    title: str = Field(..., min_length=2, max_length=200)
    description: str = Field(..., min_length=5, max_length=2000)
    resource_type: str = Field("product_intelligence", max_length=64)
    provider: str = Field("channel3", max_length=64)
    metadata: dict[str, Any] = Field(default_factory=dict)

class OfferCreateRequest(BaseModel):
    offer_code: str = Field(..., min_length=2, max_length=64, pattern=r"^[a-zA-Z0-9_\-]+$")
    title: str = Field(..., min_length=2, max_length=200)
    description: str = Field(..., min_length=5, max_length=2000)
    price_amount: float = Field(..., gt=0.0, le=100.0, description="Price must be positive and within limits")
    currency: str = Field("USD", min_length=3, max_length=3)
    pricing_model: str = Field("one_time", max_length=32)
    duration_seconds: int = Field(3600, ge=60, le=2592000)
    scope: dict[str, Any] = Field(default_factory=lambda: {"access": "read"})

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
