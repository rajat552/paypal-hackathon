import json
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.agent.policy import policy_engine
from backend.app.models.entities import Offer
from backend.app.services.challenge_service import challenge_service
from backend.app.services.entitlement_service import entitlement_service
from backend.app.services.resource_service import resource_service


class AgentTools:
    @staticmethod
    async def discover_resources(session: AsyncSession, query: str = "", limit: int = 5) -> dict[str, Any]:
        """Search public resource catalog without exposing protected data."""
        resources = await resource_service.get_catalogue(session)
        q = query.lower().strip()
        q_terms = [t for t in q.split() if len(t) > 2]
        matched = []
        for r in resources:
            text = f"{r.title} {r.description} {r.slug}".lower()
            if not q or not q_terms or any(term in text for term in q_terms):
                matched.append({
                    "id": r.id,
                    "slug": r.slug,
                    "title": r.title,
                    "description": r.description,
                    "provider": r.provider,
                    "offers": [
                        {
                            "id": o.id,
                            "offer_code": o.offer_code,
                            "title": o.title,
                            "amount": float(o.price_amount),
                            "currency": o.currency,
                            "pricing_model": o.pricing_model,
                            "duration_seconds": o.duration_seconds
                        }
                        for o in r.offers if o.active
                    ]
                })
        return {"resources": matched[:limit], "count": len(matched[:limit])}

    @staticmethod
    async def get_resource_offer(session: AsyncSession, resource_slug: str) -> dict[str, Any]:
        """Fetch server-owned offer details for a specific resource."""
        resource = await resource_service.get_by_slug(session, resource_slug)
        if not resource:
            return {"error": "Resource not found"}
        
        active_offers = [o for o in resource.offers if o.active]
        if not active_offers:
            return {"error": "No active offers found for resource"}
        
        primary = active_offers[0]
        return {
            "resource_id": resource.id,
            "resource_slug": resource.slug,
            "resource_title": resource.title,
            "offer_id": primary.id,
            "offer_code": primary.offer_code,
            "amount": float(primary.price_amount),
            "currency": primary.currency,
            "duration_seconds": primary.duration_seconds,
            "scope": json.loads(primary.scope_json) if isinstance(primary.scope_json, str) else primary.scope_json
        }

    @staticmethod
    async def request_access_challenge(
        session: AsyncSession,
        resource_slug: str,
        offer_id: str | None = None
    ) -> dict[str, Any]:
        """Request protected access to receive an authoritative L402 challenge."""
        resource = await resource_service.get_by_slug(session, resource_slug)
        if not resource:
            return {"error": "Resource not found"}

        active_offers = [o for o in resource.offers if o.active]
        selected_offer = None
        if offer_id:
            for o in active_offers:
                if o.id == offer_id or o.offer_code == offer_id:
                    selected_offer = o
                    break
        if not selected_offer and active_offers:
            selected_offer = active_offers[0]

        if not selected_offer:
            return {"error": "No offer available for this resource"}

        challenge = await challenge_service.create_challenge(session, resource, selected_offer)
        return {
            "status": 402,
            "protocol": "paymesh-l402",
            "compatibility_protocol": "crawlerpal-l402",
            "challenge_id": challenge.id,
            "resource_slug": resource.slug,
            "offer_id": selected_offer.id,
            "amount": float(selected_offer.price_amount),
            "currency": selected_offer.currency,
            "expires_at": challenge.expires_at.isoformat(),
            "payment_endpoint": "/api/v1/payment-sessions"
        }

    @staticmethod
    async def evaluate_purchase_policy(
        session: AsyncSession,
        offer_id: str,
        budget_limit: float,
        currency: str = "USD"
    ) -> dict[str, Any]:
        """Execute deterministic budget policy check."""
        stmt = select(Offer).where(Offer.id == offer_id)
        res = await session.execute(stmt)
        offer = res.scalars().first()
        if not offer:
            return {"allowed": False, "reason": "Offer ID not found"}

        allowed, reason, metrics = await policy_engine.evaluate_with_rolling_budget(
            session=session,
            offer=offer,
            budget_limit=budget_limit,
            currency=currency
        )
        return {
            "allowed": allowed,
            "offer_id": offer.id,
            "amount": float(offer.price_amount),
            "currency": offer.currency,
            "budget_limit": budget_limit,
            "reason": reason,
            "policy_metrics": metrics
        }

    @staticmethod
    async def fetch_entitled_resource(
        session: AsyncSession,
        resource_slug: str,
        bearer_token: str
    ) -> dict[str, Any]:
        """Retrieve protected content with verified entitlement token."""
        resource = await resource_service.get_by_slug(session, resource_slug)
        if not resource:
            return {"error": "Resource not found"}

        entitlement = await entitlement_service.validate_bearer_token(session, bearer_token, resource.id)
        if not entitlement:
            return {"status": 402, "error": "Entitlement token is invalid, expired, or revoked"}

        content = await resource_service.get_resource_content(session, resource)
        return {"status": 200, "content": content}

    @staticmethod
    def summarise_resource(retrieved_data: dict[str, Any]) -> str:
        """Summarise protected dataset without hallucinating external facts."""
        content = retrieved_data.get("content", {})
        data_block = content.get("data", {})
        benchmarks = data_block.get("benchmarks", [])
        insights = data_block.get("market_insights", {})

        summary_lines = [
            f"### Research Brief: {content.get('title', 'Hardware Market Intelligence')}",
            f"**Attribution**: {content.get('attribution', 'Channel3 Real-Time Commerce')}",
            "",
            "#### Curated Benchmarks:"
        ]
        for item in benchmarks:
            summary_lines.append(
                f"- **{item['title']}** (${item['price']} {item['currency']}): Latency {item.get('latency_ms')}ms, Switch: {item.get('switch_type')}. [View Product]({item.get('source_url')})"
            )
        summary_lines.append("")
        summary_lines.append(f"**Top Recommendation**: {insights.get('recommendation', 'Verified dataset insights available.')}")
        summary_lines.append(f"**Value Pick**: {insights.get('budget_pick', 'See product table for lowest price.')}")
        return "\n".join(summary_lines)

agent_tools = AgentTools()
