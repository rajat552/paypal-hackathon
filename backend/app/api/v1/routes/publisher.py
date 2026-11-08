import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db.session import get_db
from backend.app.models.entities import Offer, Resource, User
from backend.app.schemas.publisher import (
    OfferCreateRequest,
    OfferResponse,
    ResourceCreateRequest,
    ResourceResponse,
)

router = APIRouter(prefix="/publisher", tags=["Publisher"])

@router.post("/resources", response_model=ResourceResponse)
async def create_publisher_resource(
    request: ResourceCreateRequest,
    session: AsyncSession = Depends(get_db)
):
    # Check if slug exists
    stmt = select(Resource).where(Resource.slug == request.slug)
    res = await session.execute(stmt)
    if res.scalars().first():
        raise HTTPException(status_code=400, detail="Resource slug already exists")

    # Get or create default publisher user
    user_stmt = select(User).where(User.role == "publisher")
    user_res = await session.execute(user_stmt)
    publisher = user_res.scalars().first()
    if not publisher:
        publisher = User(
            email="publisher@paymesh.ai",
            password_hash="system_managed",
            role="publisher"
        )
        session.add(publisher)
        await session.commit()
        await session.refresh(publisher)

    resource = Resource(
        publisher_id=publisher.id,
        slug=request.slug,
        title=request.title,
        description=request.description,
        resource_type=request.resource_type,
        provider=request.provider,
        metadata_json=json.dumps(request.metadata)
    )
    session.add(resource)
    await session.commit()
    await session.refresh(resource)

    return ResourceResponse(
        id=resource.id,
        slug=resource.slug,
        title=resource.title,
        description=resource.description,
        resource_type=resource.resource_type,
        provider=resource.provider,
        status=resource.status,
        created_at=resource.created_at.isoformat()
    )

@router.post("/resources/{resource_id}/offers", response_model=OfferResponse)
async def create_resource_offer(
    resource_id: str,
    request: OfferCreateRequest,
    session: AsyncSession = Depends(get_db)
):
    stmt = select(Resource).where(Resource.id == resource_id)
    res = await session.execute(stmt)
    resource = res.scalars().first()
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")

    # Authoritative ownership validation to prevent cross-tenant IDOR
    user_stmt = select(User).where(User.role == "publisher")
    user_res = await session.execute(user_stmt)
    publisher = user_res.scalars().first()
    if publisher and resource.publisher_id != publisher.id:
        raise HTTPException(status_code=403, detail="Forbidden: You do not have permission to attach offers to this resource.")

    if request.currency.upper() not in {"USD", "EUR", "GBP"}:
        raise HTTPException(status_code=400, detail=f"Currency '{request.currency}' is not allowed. Must be USD, EUR, or GBP.")

    offer = Offer(
        resource_id=resource.id,
        offer_code=request.offer_code,
        title=request.title,
        description=request.description,
        price_amount=request.price_amount,
        currency=request.currency,
        pricing_model=request.pricing_model,
        duration_seconds=request.duration_seconds,
        scope_json=json.dumps(request.scope)
    )
    session.add(offer)
    await session.commit()
    await session.refresh(offer)

    return OfferResponse(
        id=offer.id,
        resource_id=offer.resource_id,
        offer_code=offer.offer_code,
        title=offer.title,
        description=offer.description,
        price_amount=float(offer.price_amount),
        currency=offer.currency,
        pricing_model=offer.pricing_model,
        duration_seconds=offer.duration_seconds,
        active=offer.active
    )

