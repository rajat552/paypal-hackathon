import json
from datetime import datetime, timezone, timedelta
from typing import Optional, Dict, Any, Tuple
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.config import settings
from backend.app.core.security import generate_secure_bearer_token, hash_token
from backend.app.models.entities import Entitlement, UsageEvent, Resource, Offer

class EntitlementService:
    async def issue_entitlement(
        self,
        session: AsyncSession,
        resource_id: str,
        offer_id: str,
        scope_json: str,
        duration_seconds: int,
        agent_id: Optional[str] = None
    ) -> Tuple[Entitlement, str]:
        """Issue a new entitlement and return (entitlement_record, raw_secret_bearer_token)."""
        raw_token = generate_secure_bearer_token()
        token_hash = hash_token(raw_token)
        
        now = datetime.now(timezone.utc)
        expires_at = now + timedelta(seconds=duration_seconds)
        
        entitlement = Entitlement(
            agent_id=agent_id,
            resource_id=resource_id,
            offer_id=offer_id,
            token_hash=token_hash,
            scope_json=scope_json,
            starts_at=now,
            expires_at=expires_at,
            status="ACTIVE"
        )
        session.add(entitlement)
        await session.commit()
        await session.refresh(entitlement)
        return entitlement, raw_token

    async def validate_bearer_token(
        self,
        session: AsyncSession,
        raw_token: str,
        resource_id: str
    ) -> Optional[Entitlement]:
        """Verify token hash, expiry, active status, and resource scoping."""
        if not raw_token or not (raw_token.startswith("pm_live_") or raw_token.startswith("cp_live_")):
            return None
            
        token_hash = hash_token(raw_token)
        stmt = (
            select(Entitlement)
            .where(
                Entitlement.token_hash == token_hash,
                Entitlement.resource_id == resource_id
            )
        )
        result = await session.execute(stmt)
        entitlement = result.scalars().first()
        
        if not entitlement or entitlement.status != "ACTIVE":
            return None
            
        now = datetime.now(timezone.utc)
        expires_at = entitlement.expires_at
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)
            
        if now > expires_at:
            entitlement.status = "EXPIRED"
            await session.commit()
            return None
            
        # Record usage event
        usage = UsageEvent(
            agent_id=entitlement.agent_id,
            resource_id=resource_id,
            entitlement_id=entitlement.id,
            event_type="read_content",
            units=1
        )
        session.add(usage)
        await session.commit()
        
        return entitlement

entitlement_service = EntitlementService()
