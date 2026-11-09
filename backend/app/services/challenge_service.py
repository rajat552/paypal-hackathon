from datetime import UTC, datetime, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.config import settings
from backend.app.core.exceptions import InvalidChallengeException
from backend.app.core.security import generate_challenge_id
from backend.app.models.entities import Offer, PaymentChallenge, Resource


class ChallengeService:
    async def create_challenge(
        self,
        session: AsyncSession,
        resource: Resource,
        offer: Offer,
        agent_id: str | None = None
    ) -> PaymentChallenge:
        challenge_id = generate_challenge_id()
        expires_at = datetime.now(UTC) + timedelta(minutes=settings.PAYMENT_CHALLENGE_TTL_MINUTES)
        
        challenge = PaymentChallenge(
            id=challenge_id,
            agent_id=agent_id,
            resource_id=resource.id,
            offer_id=offer.id,
            amount=offer.price_amount,
            currency=offer.currency,
            scope_json=offer.scope_json,
            expires_at=expires_at,
            status="PENDING"
        )
        session.add(challenge)
        await session.commit()
        await session.refresh(challenge)
        return challenge

    async def get_challenge(
        self,
        session: AsyncSession,
        challenge_id: str
    ) -> PaymentChallenge | None:
        stmt = select(PaymentChallenge).where(PaymentChallenge.id == challenge_id)
        result = await session.execute(stmt)
        return result.scalars().first()

    async def get_and_validate_challenge(
        self,
        session: AsyncSession,
        challenge_id: str
    ) -> PaymentChallenge:
        stmt = select(PaymentChallenge).where(PaymentChallenge.id == challenge_id)
        result = await session.execute(stmt)
        challenge = result.scalars().first()
        
        if not challenge:
            raise InvalidChallengeException("Challenge ID does not exist.")
        
        if challenge.status != "PENDING":
            raise InvalidChallengeException(f"Challenge already {challenge.status.lower()} (single-use replay violation).")
        
        now = datetime.now(UTC)
        # Ensure timezone-aware comparison
        expires_at = challenge.expires_at
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=UTC)
            
        if now > expires_at:
            challenge.status = "EXPIRED"
            await session.commit()
            raise InvalidChallengeException("Challenge has expired.")
            
        return challenge

    async def consume_challenge(self, session: AsyncSession, challenge: PaymentChallenge):
        challenge.status = "CONSUMED"
        await session.commit()

challenge_service = ChallengeService()
