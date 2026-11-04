from typing import Any

from pydantic import BaseModel


class OfferPublic(BaseModel):
    id: str
    offer_code: str
    title: str
    description: str
    amount: float
    currency: str
    pricing_model: str
    duration_seconds: int
    scope: dict[str, Any]

class ResourcePublic(BaseModel):
    id: str
    slug: str
    title: str
    description: str
    resource_type: str
    provider: str
    publisher_name: str | None = "PayMesh AI Verified Publisher"
    offers: list[OfferPublic] = []

class CatalogueResponse(BaseModel):
    total: int
    resources: list[ResourcePublic]
