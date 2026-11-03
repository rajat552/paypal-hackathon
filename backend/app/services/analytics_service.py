from typing import Dict, Any, List
from sqlalchemy import select, func, desc
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.models.entities import Transaction, Entitlement, UsageEvent, PaymentSession, Resource

class AnalyticsService:
    async def get_summary(self, session: AsyncSession) -> Dict[str, Any]:
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
    ) -> List[Dict[str, Any]]:
        stmt = (
            select(Transaction, PaymentSession, Resource)
            .join(PaymentSession, Transaction.payment_session_id == PaymentSession.id)
            .join(Resource, Resource.id != None) # simplified join
            .order_by(desc(Transaction.captured_at))
            .limit(limit)
            .offset(offset)
        )
        result = await session.execute(stmt)
        rows = result.all()
        
        items = []
        for tx, sess, res in rows:
            items.append({
                "id": tx.id,
                "paypal_order_id": tx.paypal_order_id,
                "paypal_capture_id": tx.paypal_capture_id,
                "amount": float(tx.gross_amount),
                "currency": tx.currency,
                "status": tx.payment_status,
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
    ) -> List[Dict[str, Any]]:
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
