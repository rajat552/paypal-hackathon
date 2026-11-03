import json
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.app.models.entities import Resource, Offer, User
from backend.app.services.channel3_client import channel3_client

class ResourceService:
    async def get_catalogue(self, session: AsyncSession) -> List[Resource]:
        stmt = (
            select(Resource)
            .where(Resource.status == "active")
            .options(selectinload(Resource.offers), selectinload(Resource.publisher))
            .order_by(Resource.created_at.desc())
        )
        result = await session.execute(stmt)
        return list(result.scalars().all())

    async def get_by_slug(self, session: AsyncSession, slug: str) -> Optional[Resource]:
        stmt = (
            select(Resource)
            .where(Resource.slug == slug)
            .options(selectinload(Resource.offers), selectinload(Resource.publisher))
        )
        result = await session.execute(stmt)
        return result.scalars().first()

    async def get_resource_content(self, session: AsyncSession, resource: Resource) -> Dict[str, Any]:
        """Fetch protected structured dataset payload for verified access."""
        if resource.resource_type == "product_intelligence":
            product_data = await channel3_client.search_products(query="mechanical keyboards", limit=10)
            return {
                "resource_id": resource.id,
                "slug": resource.slug,
                "title": resource.title,
                "provider": resource.provider,
                "retrieved_at": datetime.now(timezone.utc).isoformat(),
                "dataset_type": "deep_hardware_benchmark_comparison",
                "attribution": product_data["source_attribution"],
                "data": {
                    "total_analyzed": len(product_data["items"]),
                    "benchmarks": product_data["items"],
                    "market_insights": {
                        "recommendation": "Wooting 60HE+ leads in ultra-low input latency (0.1ms Hall Effect), while Keychron Q1 Pro offers the most versatile build quality and wireless endurance.",
                        "budget_pick": "Rainy75 Aluminum ($99) delivers exceptional value with CNC chassis and pre-lubed HMX switches."
                    }
                }
            }
        else:
            # Fallback / News dataset for legacy compatibility
            return {
                "resource_id": resource.id,
                "slug": resource.slug,
                "title": resource.title,
                "retrieved_at": datetime.now(timezone.utc).isoformat(),
                "news": [
                    {
                        "headline": "Autonomous Agents Adopt PayMesh AI Machine-Readable L402 Commerce",
                        "summary": "Publishers globally are unlocking programmatic revenue through PayPal Sandbox and PayMesh AI gateways.",
                        "category": "technology"
                    }
                ]
            }

resource_service = ResourceService()
