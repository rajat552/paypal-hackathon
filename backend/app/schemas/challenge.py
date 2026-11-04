from typing import Any

from pydantic import BaseModel


class ChallengeOfferItem(BaseModel):
    id: str
    offer_code: str
    title: str
    description: str
    amount: float
    currency: str
    pricing_model: str
    duration_seconds: int
    scope: dict[str, Any]
    payment_method: str = "paypal"

class L402ChallengeResponse(BaseModel):
    protocol: str = "paymesh-l402"
    protocol_version: str = "1.0"
    status: int = 402
    challenge_id: str
    resource: dict[str, str]
    offers: list[ChallengeOfferItem]
    payment_endpoint: str
    expires_at: str
    correlation_id: str
