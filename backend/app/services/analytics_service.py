import json
from typing import Any

from sqlalchemy import desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models.entities import (
    Entitlement,
    PaymentChallenge,
    PaymentSession,
    Resource,
    Transaction,
    UsageEvent,
)


class AnalyticsService:
    async def get_summary(self, session: AsyncSession) -> dict[str, Any]:
        # Total revenue
        rev_stmt = select(func.coalesce(func.sum(Transaction.gross_amount), 0.0))
        rev_res = await session.execute(rev_stmt)
        total_revenue = float(rev_res.scalar() or 0.0)

        # Total captured transactions
        tx_stmt = select(func.count(Transaction.id))
        tx_res = await session.execute(tx_stmt)
        tx_count = int(tx_res.scalar() or 0)

        # Total active entitlements
        ent_stmt = select(func.count(Entitlement.id)).where(Entitlement.status == "ACTIVE")
        ent_res = await session.execute(ent_stmt)
        ent_count = int(ent_res.scalar() or 0)

        # Unique agents
        agent_stmt = select(func.count(func.distinct(Entitlement.agent_id)))
        agent_res = await session.execute(agent_stmt)
        agent_count = int(agent_res.scalar() or 0)

        # Payment sessions count for conversion
        sess_stmt = select(func.count(PaymentSession.id))
        sess_res = await session.execute(sess_stmt)
        sess_count = int(sess_res.scalar() or 0)
        conversion_rate = (tx_count / sess_count * 100.0) if sess_count > 0 else 100.0

        # Total usage events
        usage_stmt = select(func.count(UsageEvent.id))
        usage_res = await session.execute(usage_stmt)
        usage_count = int(usage_res.scalar() or 0)

        return {
            "total_revenue_usd": round(total_revenue, 2),
            "captured_transactions_count": tx_count,
            "active_entitlements_count": ent_count,
            "unique_agents_count": agent_count,
            "conversion_rate_pct": round(conversion_rate, 1),
            "total_usage_events": usage_count
        }

    async def get_transactions(
        self,
        session: AsyncSession,
        limit: int = 50,
        offset: int = 0
    ) -> list[dict[str, Any]]:
        stmt = (
            select(Transaction, PaymentSession, Resource)
            .join(PaymentSession, Transaction.payment_session_id == PaymentSession.id)
            .outerjoin(PaymentChallenge, PaymentSession.challenge_id == PaymentChallenge.id)
            .outerjoin(Resource, PaymentChallenge.resource_id == Resource.id)
            .order_by(desc(Transaction.captured_at))
            .limit(limit)
            .offset(offset)
        )
        result = await session.execute(stmt)
        rows = result.all()
        
        items = []
        for tx, _sess, res in rows:
            is_sim = False
            try:
                raw = json.loads(tx.raw_summary_json) if tx.raw_summary_json else {}
                is_sim = bool(raw.get("simulated", False)) or "SIM" in tx.paypal_order_id or "SANDBOX" in tx.paypal_order_id
            except (json.JSONDecodeError, TypeError, KeyError):
                is_sim = False

            env_tag = "simulated_sandbox" if is_sim else "live_sandbox"
            env_lbl = "Sandbox Simulation (Dry-Run)" if is_sim else "PayPal Sandbox (Live Verified)"

            items.append({
                "id": tx.id,
                "paypal_order_id": tx.paypal_order_id,
                "paypal_capture_id": tx.paypal_capture_id,
                "amount": float(tx.gross_amount),
                "currency": tx.currency,
                "status": tx.payment_status,
                "environment": env_tag,
                "environment_label": env_lbl,
                "resource_title": res.title if res else "Product Intelligence Report",
                "resource_slug": res.slug if res else "product-intelligence-report",
                "captured_at": tx.captured_at.isoformat()
            })
        return items

    async def get_usage_events(
        self,
        session: AsyncSession,
        limit: int = 50,
        offset: int = 0
    ) -> list[dict[str, Any]]:
        stmt = (
            select(UsageEvent)
            .order_by(desc(UsageEvent.created_at))
            .limit(limit)
            .offset(offset)
        )
        result = await session.execute(stmt)
        events = result.scalars().all()
        return [
            {
                "id": ev.id,
                "resource_slug": ev.resource_id,
                "event_type": ev.event_type,
                "units": ev.units,
                "created_at": ev.created_at.isoformat()
            }
            for ev in events
        ]

analytics_service = AnalyticsService()
