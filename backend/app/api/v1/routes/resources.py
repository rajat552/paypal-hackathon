import json
import uuid
from typing import Optional
from fastapi import APIRouter, Depends, Header, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db.session import get_db
from backend.app.core.config import settings
from backend.app.services.resource_service import resource_service
from backend.app.services.challenge_service import challenge_service
from backend.app.services.entitlement_service import entitlement_service
from backend.app.schemas.catalogue import ResourcePublic, OfferPublic

router = APIRouter(prefix="/resources", tags=["Resources"])

def extract_bearer_token(authorization: Optional[str] = Header(None)) -> Optional[str]:
    if authorization:
        parts = authorization.split()
        if len(parts) == 2 and parts[0].lower() == "bearer":
            return parts[1]
    return None

@router.get("/{slug}")
async def get_resource_details(slug: str, session: AsyncSession = Depends(get_db)):
    resource = await resource_service.get_by_slug(session, slug)
    if not resource:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")
    
    offers = [
        OfferPublic(
            id=o.id,
            offer_code=o.offer_code,
            title=o.title,
            description=o.description,
            amount=float(o.price_amount),
            currency=o.currency,
            pricing_model=o.pricing_model,
            duration_seconds=o.duration_seconds,
            scope=json.loads(o.scope_json) if isinstance(o.scope_json, str) else o.scope_json
        )
        for o in resource.offers if o.active
    ]
    return ResourcePublic(
        id=resource.id,
        slug=resource.slug,
        title=resource.title,
        description=resource.description,
        resource_type=resource.resource_type,
        provider=resource.provider,
        publisher_name=resource.publisher.email if resource.publisher else "PayMesh AI Verified Publisher",
        offers=offers
    )

@router.get("/{slug}/content")
async def get_resource_content(
    slug: str,
    authorization: Optional[str] = Header(None),
    session: AsyncSession = Depends(get_db)
):
    resource = await resource_service.get_by_slug(session, slug)
    if not resource:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")

    bearer_token = extract_bearer_token(authorization)
    
    # 1. Validate entitlement if bearer token provided
    if bearer_token:
        entitlement = await entitlement_service.validate_bearer_token(session, bearer_token, resource.id)
        if entitlement:
            # Token is valid and authorized!
            content_payload = await resource_service.get_resource_content(session, resource)
            return JSONResponse(status_code=status.HTTP_200_OK, content=content_payload)

    # 2. If token missing or invalid, generate HTTP 402 challenge
    active_offers = [o for o in resource.offers if o.active]
    if not active_offers:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Resource has no active offers")

    selected_offer = active_offers[0]
    challenge = await challenge_service.create_challenge(session, resource, selected_offer)

    # Build L402 challenge body
    correlation_id = str(uuid.uuid4())
    payment_endpoint = f"{settings.APP_BASE_URL}/api/v1/payment-sessions"

    challenge_body = {
        "protocol": "paymesh-l402",
        "protocol_version": "1.0",
        "status": 402,
        "challenge_id": challenge.id,
        "resource": {
            "id": resource.id,
            "slug": resource.slug,
            "title": resource.title
        },
        "offers": [
            {
                "id": o.id,
                "offer_code": o.offer_code,
                "title": o.title,
                "description": o.description,
                "amount": float(o.price_amount),
                "currency": o.currency,
                "pricing_model": o.pricing_model,
                "duration_seconds": o.duration_seconds,
                "scope": json.loads(o.scope_json) if isinstance(o.scope_json, str) else o.scope_json,
                "payment_method": "paypal"
            }
            for o in active_offers
        ],
        "payment_endpoint": payment_endpoint,
        "expires_at": challenge.expires_at.isoformat(),
        "correlation_id": correlation_id
    }

    return JSONResponse(status_code=status.HTTP_402_PAYMENT_REQUIRED, content=challenge_body)

