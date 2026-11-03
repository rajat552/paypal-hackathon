import json
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.db.session import get_db
from backend.app.services.resource_service import resource_service
from backend.app.schemas.catalogue import CatalogueResponse, ResourcePublic, OfferPublic

router = APIRouter(prefix="/catalogue", tags=["Catalogue"])

@router.get("", response_model=CatalogueResponse)
async def get_catalogue(session: AsyncSession = Depends(get_db)):
    resources = await resource_service.get_catalogue(session)
    public_list = []
    for r in resources:
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
            for o in r.offers if o.active
        ]
        public_list.append(
            ResourcePublic(
                id=r.id,
                slug=r.slug,
                title=r.title,
                description=r.description,
                resource_type=r.resource_type,
                provider=r.provider,
                publisher_name=r.publisher.email if r.publisher else "PayMesh AI Verified Publisher",
                offers=offers
            )
        )
    return CatalogueResponse(total=len(public_list), resources=public_list)

