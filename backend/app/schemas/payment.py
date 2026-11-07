from typing import Any

from pydantic import BaseModel, Field


class PaymentSessionCreateRequest(BaseModel):
    challenge_id: str
    offer_id: str
    agent_id: str | None = None
    buyer_confirmed: bool = Field(..., description="Explicit buyer confirmation is mandatory")

class PaymentSessionResponse(BaseModel):
    session_id: str
    challenge_id: str
    paypal_order_id: str
    approval_url: str
    amount: float
    currency: str
    status: str

class PaymentSessionStatusResponse(BaseModel):
    session_id: str
    paypal_order_id: str
    status: str
    amount: float
    currency: str
    created_at: str

class CaptureRequest(BaseModel):
    paypal_order_id: str | None = None
    simulate_buyer_approval: bool = False

class CaptureResponse(BaseModel):
    status: str
    payment_session_id: str
    paypal_order_id: str
    paypal_capture_id: str
    access_token: str
    token_type: str = "Bearer"
    expires_at: str
    resource_slug: str
    scope: dict[str, Any]
