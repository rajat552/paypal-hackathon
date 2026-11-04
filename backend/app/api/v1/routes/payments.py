import json
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db.session import get_db
from backend.app.models.entities import (
    AuditLog,
    Offer,
    PaymentSession,
    Resource,
    Transaction,
)
from backend.app.schemas.payment import (
    CaptureRequest,
    CaptureResponse,
    PaymentSessionCreateRequest,
    PaymentSessionResponse,
    PaymentSessionStatusResponse,
)
from backend.app.services.challenge_service import challenge_service
from backend.app.services.entitlement_service import entitlement_service
from backend.app.services.paypal_gateway import paypal_gateway
from backend.app.db.mongodb import log_mongo_audit_event

router = APIRouter(tags=["Payments"])

@router.post("/api/v1/payment-sessions", response_model=PaymentSessionResponse)
async def create_payment_session(
    payload: PaymentSessionCreateRequest,
    session: AsyncSession = Depends(get_db)
):
    if not payload.buyer_confirmed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Buyer confirmation is required before initiating payment."
        )

    # 1. Validate challenge
    challenge = await challenge_service.get_and_validate_challenge(session, payload.challenge_id)

    # 2. Resolve offer authoritative price from database
    stmt = select(Offer).where(Offer.id == payload.offer_id)
    res = await session.execute(stmt)
    offer = res.scalars().first()
    if not offer or not offer.active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Selected offer is invalid or inactive")

    # Authoritative binding check: offer must match challenge
    if offer.id != challenge.offer_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Offer does not match the active challenge.")

    # 3. Create PayPal Sandbox Order
    session_id = str(uuid.uuid4())
    paypal_order = await paypal_gateway.create_order(
        amount=float(offer.price_amount),
        currency=offer.currency,
        session_id=session_id
    )

    # 4. Persist PaymentSession
    payment_session = PaymentSession(
        id=session_id,
        challenge_id=challenge.id,
        agent_id=payload.agent_id or challenge.agent_id,
        paypal_order_id=paypal_order["id"],
        paypal_request_id=str(uuid.uuid4()),
        approval_url=paypal_order["approval_url"],
        amount=offer.price_amount,
        currency=offer.currency,
        status="CREATED"
    )
    session.add(payment_session)
    await session.commit()
    await session.refresh(payment_session)

    return PaymentSessionResponse(
        session_id=payment_session.id,
        challenge_id=challenge.id,
        paypal_order_id=paypal_order["id"],
        approval_url=paypal_order["approval_url"],
        amount=float(payment_session.amount),
        currency=payment_session.currency,
        status=payment_session.status
    )

@router.get("/api/v1/payment-sessions/{session_id}", response_model=PaymentSessionStatusResponse)
async def get_payment_session_status(session_id: str, session: AsyncSession = Depends(get_db)):
    stmt = select(PaymentSession).where(PaymentSession.id == session_id)
    res = await session.execute(stmt)
    ps = res.scalars().first()
    if not ps:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment session not found")

    return PaymentSessionStatusResponse(
        session_id=ps.id,
        paypal_order_id=ps.paypal_order_id,
        status=ps.status,
        amount=float(ps.amount),
        currency=ps.currency,
        created_at=ps.created_at.isoformat()
    )

@router.post("/api/v1/payment-sessions/{session_id}/capture", response_model=CaptureResponse)
async def capture_payment_session(
    session_id: str,
    payload: CaptureRequest | None = None,
    session: AsyncSession = Depends(get_db)
):
    stmt = select(PaymentSession).where(PaymentSession.id == session_id)
    res = await session.execute(stmt)
    ps = res.scalars().first()
    if not ps:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment session not found")

    # Retrieve challenge to get resource & offer
    challenge = await challenge_service.get_and_validate_challenge(session, ps.challenge_id)
    
    # Retrieve offer
    stmt_offer = select(Offer).where(Offer.id == challenge.offer_id)
    res_offer = await session.execute(stmt_offer)
    offer = res_offer.scalars().first()

    # Retrieve resource
    stmt_res = select(Resource).where(Resource.id == challenge.resource_id)
    res_resource = await session.execute(stmt_res)
    resource = res_resource.scalars().first()

    # 1. Idempotency check: if already captured, return existing active entitlement
    if ps.status == "CAPTURED":
        # Already captured! Look up transaction
        stmt_tx = select(Transaction).where(Transaction.payment_session_id == ps.id)
        res_tx = await session.execute(stmt_tx)
        tx = res_tx.scalars().first()
        return CaptureResponse(
            status="CAPTURED",
            payment_session_id=ps.id,
            paypal_order_id=ps.paypal_order_id,
            paypal_capture_id=tx.paypal_capture_id if tx else "CAP-RECORDED",
            access_token="[SESSION_ALREADY_CAPTURED_RETAIN_EXISTING_TOKEN]",
            expires_at=challenge.expires_at.isoformat(),
            resource_slug=resource.slug if resource else "unknown",
            scope=json.loads(offer.scope_json) if offer else {"access": "read"}
        )

    # 2. Capture PayPal Sandbox Order on server
    capture_data = await paypal_gateway.capture_order(ps.paypal_order_id)
    if capture_data.get("status") != "COMPLETED":
        ps.status = "FAILED"
        await session.commit()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="PayPal capture was not completed")

    # 3. Create Transaction record
    tx = Transaction(
        payment_session_id=ps.id,
        paypal_order_id=ps.paypal_order_id,
        paypal_capture_id=capture_data.get("capture_id", f"CAP-{ps.paypal_order_id}"),
        gross_amount=ps.amount,
        currency=ps.currency,
        payment_status="COMPLETED",
        raw_summary_json=json.dumps(capture_data.get("raw_response", {}))
    )
    session.add(tx)

    # 4. Issue Entitlement and generate separate Bearer token
    duration = offer.duration_seconds if offer else 3600
    scope_str = offer.scope_json if offer else '{"access": "read"}'
    entitlement, raw_bearer_token = await entitlement_service.issue_entitlement(
        session=session,
        resource_id=challenge.resource_id,
        offer_id=challenge.offer_id,
        scope_json=scope_str,
        duration_seconds=duration,
        agent_id=ps.agent_id
    )

    # 5. Mark PaymentSession CAPTURED and consume challenge
    ps.status = "CAPTURED"
    await challenge_service.consume_challenge(session, challenge)

    audit = AuditLog(
        actor_type="buyer_agent",
        actor_id=ps.agent_id,
        action="PAYPAL_CAPTURE_SUCCESS",
        entity_type="transaction",
        entity_id=tx.id,
        metadata_json=json.dumps({"order_id": ps.paypal_order_id, "amount": float(ps.amount)})
    )
    session.add(audit)
    await session.commit()

    log_mongo_audit_event("PAYPAL_CAPTURE_SUCCESS", {
        "order_id": ps.paypal_order_id,
        "capture_id": tx.paypal_capture_id,
        "amount": float(ps.amount),
        "agent_id": ps.agent_id,
        "resource_slug": resource.slug if resource else "unknown"
    })

    return CaptureResponse(
        status="CAPTURED",
        payment_session_id=ps.id,
        paypal_order_id=ps.paypal_order_id,
        paypal_capture_id=tx.paypal_capture_id,
        access_token=raw_bearer_token,
        expires_at=entitlement.expires_at.isoformat(),
        resource_slug=resource.slug if resource else "unknown",
        scope=json.loads(scope_str)
    )

# --- Legacy Compatibility Route ---
@router.post("/l402/payment-request")
async def legacy_payment_request(payload: dict, session: AsyncSession = Depends(get_db)):
    """Maintain backward compatibility for legacy CLI client/main.py."""
    offer_code = payload.get("offer_id", "all_categories")
    
    # Map legacy offer to our database
    stmt = select(Offer).where(Offer.offer_code == offer_code)
    res = await session.execute(stmt)
    offer = res.scalars().first()
    if not offer:
        # Fallback to first available offer
        stmt = select(Offer).where(Offer.active.is_(True))
        res = await session.execute(stmt)
        offer = res.scalars().first()
        if not offer:
            raise HTTPException(status_code=400, detail="No active offer found")

    session_id = str(uuid.uuid4())
    paypal_order = await paypal_gateway.create_order(
        amount=float(offer.price_amount),
        currency=offer.currency,
        session_id=session_id
    )
    await paypal_gateway.capture_order(paypal_order["id"])

    # Issue entitlement
    _entitlement, raw_bearer_token = await entitlement_service.issue_entitlement(
        session=session,
        resource_id=offer.resource_id,
        offer_id=offer.id,
        scope_json=offer.scope_json,
        duration_seconds=offer.duration_seconds
    )

    return {
        "message": "Payment successful",
        "bearer_token": raw_bearer_token,
        "paypal_order_id": paypal_order["id"]
    }

