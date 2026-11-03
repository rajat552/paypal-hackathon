from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class OfferPublic(BaseModel):
    id: str
    offer_code: str
    title: str
    description: str
    amount: float
    currency: str
    pricing_model: str
    duration_seconds: int
    scope: Dict[str, Any]

class ResourcePublic(BaseModel):
    id: str
    slug: str
    title: str
    description: str
    resource_type: str
    provider: str
    publisher_name: Optional[str] = "PayMesh AI Verified Publisher"
    offers: List[OfferPublic] = []

class CatalogueResponse(BaseModel):
    total: int
    resources: List[ResourcePublic]
