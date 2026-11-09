import json
import uuid

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.config import settings
from backend.app.db.session import get_db
from backend.app.models.entities import (
    AuditLog,
    Entitlement,
    Offer,
    PaymentSession,
    Resource,
    Transaction,
    WebhookEvent,
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

@router.get("/api/v1/payment-sessions/{session_id}/check-approval")
async def check_payment_session_approval(session_id: str, session: AsyncSession = Depends(get_db)):
    """Check live approval status of a PayPal order before attempting capture."""
    stmt = select(PaymentSession).where(PaymentSession.id == session_id)
    res = await session.execute(stmt)
    ps = res.scalars().first()
    if not ps:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment session not found")

    order_info = await paypal_gateway.get_order(ps.paypal_order_id)
    order_status = order_info.get("status", "UNKNOWN")
    return {
        "session_id": ps.id,
        "paypal_order_id": ps.paypal_order_id,
        "paypal_status": order_status,
        "is_approved": order_status in ("APPROVED", "COMPLETED")
    }

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

    # 1. Idempotency check: if session already captured, return existing active entitlement
    if ps.status == "CAPTURED":
        challenge = await challenge_service.get_challenge(session, ps.challenge_id)
        if not challenge:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment challenge not found")

        stmt_offer = select(Offer).where(Offer.id == challenge.offer_id)
        res_offer = await session.execute(stmt_offer)
        offer = res_offer.scalars().first()

        stmt_res = select(Resource).where(Resource.id == challenge.resource_id)
        res_resource = await session.execute(stmt_res)
        resource = res_resource.scalars().first()

        stmt_tx = select(Transaction).where(Transaction.payment_session_id == ps.id)
        res_tx = await session.execute(stmt_tx)
        tx = res_tx.scalars().first()

        stmt_ent = select(Entitlement).where(
            Entitlement.resource_id == challenge.resource_id,
            Entitlement.offer_id == challenge.offer_id,
            Entitlement.status == "ACTIVE"
        ).order_by(Entitlement.starts_at.desc())
        res_ent = await session.execute(stmt_ent)
        existing_ent = res_ent.scalars().first()

        return CaptureResponse(
            status="CAPTURED",
            payment_session_id=ps.id,
            paypal_order_id=ps.paypal_order_id,
            paypal_capture_id=tx.paypal_capture_id if tx else f"CAP-{ps.paypal_order_id}",
            access_token="[SESSION_ALREADY_CAPTURED_RETAIN_EXISTING_TOKEN]",
            expires_at=existing_ent.expires_at.isoformat() if existing_ent else challenge.expires_at.isoformat(),
            resource_slug=resource.slug if resource else "unknown",
            scope=json.loads(offer.scope_json) if offer else {"access": "read"}
        )

    # Retrieve and validate challenge to get resource & offer
    challenge = await challenge_service.get_and_validate_challenge(session, ps.challenge_id)
    
    # Retrieve offer
    stmt_offer = select(Offer).where(Offer.id == challenge.offer_id)
    res_offer = await session.execute(stmt_offer)
    offer = res_offer.scalars().first()

    # Retrieve resource
    stmt_res = select(Resource).where(Resource.id == challenge.resource_id)
    res_resource = await session.execute(stmt_res)
    resource = res_resource.scalars().first()

    # 2. Capture PayPal Sandbox Order on server
    simulate_approval = bool(payload and payload.simulate_buyer_approval)
    if simulate_approval:
        if paypal_gateway.is_configured and settings.APP_ENV != "testing":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Simulated approval is disabled. Real PayPal Sandbox credentials are active — complete buyer approval at PayPal Sandbox."
            )
        simulated_capture_id = f"CAP-SANDBOX-AUTH-{uuid.uuid4().hex[:8].upper()}"
        capture_data = {
            "id": ps.paypal_order_id,
            "status": "COMPLETED",
            "capture_id": simulated_capture_id,
            "raw_response": {
                "status": "COMPLETED",
                "id": ps.paypal_order_id,
                "capture_id": simulated_capture_id,
                "environment": "paypal_sandbox_simulated_buyer",
                "simulated_buyer": True,
            }
        }
    else:
        capture_data = await paypal_gateway.capture_order(ps.paypal_order_id)
        if capture_data.get("status") != "COMPLETED":
            ps.status = "FAILED"
            await session.commit()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="PayPal capture was not completed")

    capture_id = capture_data.get("capture_id", f"CAP-{ps.paypal_order_id}")

    # 3. Check for existing Transaction (idempotent against concurrent/replayed captures)
    stmt_existing_tx = select(Transaction).where(Transaction.paypal_capture_id == capture_id)
    res_existing_tx = await session.execute(stmt_existing_tx)
    existing_tx = res_existing_tx.scalars().first()

    if existing_tx:
        # A transaction already exists for this capture! Do NOT issue another entitlement.
        ps.status = "CAPTURED"
        await session.commit()

        stmt_ent = select(Entitlement).where(
            Entitlement.resource_id == challenge.resource_id,
            Entitlement.offer_id == challenge.offer_id,
            Entitlement.status == "ACTIVE"
        ).order_by(Entitlement.starts_at.desc())
        res_ent = await session.execute(stmt_ent)
        existing_ent = res_ent.scalars().first()

        return CaptureResponse(
            status="CAPTURED",
            payment_session_id=ps.id,
            paypal_order_id=ps.paypal_order_id,
            paypal_capture_id=capture_id,
            access_token="[SESSION_ALREADY_CAPTURED_RETAIN_EXISTING_TOKEN]",
            expires_at=existing_ent.expires_at.isoformat() if existing_ent else challenge.expires_at.isoformat(),
            resource_slug=resource.slug if resource else "unknown",
            scope=json.loads(offer.scope_json) if offer else {"access": "read"}
        )

    # 4. Durable transaction persistence BEFORE entitlement issuance
    tx = Transaction(
        payment_session_id=ps.id,
        paypal_order_id=ps.paypal_order_id,
        paypal_capture_id=capture_id,
        gross_amount=ps.amount,
        currency=ps.currency,
        payment_status="COMPLETED",
        raw_summary_json=json.dumps(capture_data.get("raw_response", {}))
    )
    session.add(tx)

    try:
        # Enforce database unique constraint on paypal_capture_id and test DB durability
        await session.flush()
    except IntegrityError:
        # A concurrent request committed the transaction first
        await session.rollback()
        stmt_ent = select(Entitlement).where(
            Entitlement.resource_id == challenge.resource_id,
            Entitlement.offer_id == challenge.offer_id,
            Entitlement.status == "ACTIVE"
        ).order_by(Entitlement.starts_at.desc())
        res_ent = await session.execute(stmt_ent)
        existing_ent = res_ent.scalars().first()

        return CaptureResponse(
            status="CAPTURED",
            payment_session_id=ps.id,
            paypal_order_id=ps.paypal_order_id,
            paypal_capture_id=capture_id,
            access_token="[SESSION_ALREADY_CAPTURED_RETAIN_EXISTING_TOKEN]",
            expires_at=existing_ent.expires_at.isoformat() if existing_ent else challenge.expires_at.isoformat(),
            resource_slug=resource.slug if resource else "unknown",
            scope=json.loads(offer.scope_json) if offer else {"access": "read"}
        )
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to record payment transaction in database: {e!s}. Entitlement was not issued."
        ) from e

    # 5. Issue Entitlement ONLY AFTER durable transaction persistence
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

    # 6. Mark PaymentSession CAPTURED and consume challenge
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

# --- PayPal Webhook Notification Endpoint ---
@router.post("/api/v1/payments/webhook")
async def paypal_webhook_handler(
    request: Request,
    session: AsyncSession = Depends(get_db)
):
    """Handle incoming asynchronous PayPal webhook events with signature verification & reconciliation."""
    try:
        body = await request.json()
    except Exception:  # noqa: BLE001
        body = {}

    headers = dict(request.headers)
    event_type = body.get("event_type", "UNKNOWN")
    event_id = body.get("id", "evt_unknown")
    resource_data = body.get("resource", {})

    # 1. Verify PayPal webhook signature
    is_valid_sig = await paypal_gateway.verify_webhook_signature(headers, body)
    if not is_valid_sig:
        log_mongo_audit_event("PAYPAL_WEBHOOK_REJECTED", {
            "event_id": event_id,
            "event_type": event_type,
            "reason": "Invalid or missing PayPal webhook signature"
        })
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="PayPal webhook signature verification failed."
        )

    # 2. Database-enforced idempotency: record WebhookEvent with unique event_id
    webhook_event_record = WebhookEvent(
        event_id=event_id,
        event_type=event_type,
        resource_id=resource_data.get("id"),
        summary=body.get("summary", ""),
        status="PROCESSED",
        payload_json=json.dumps(body)
    )
    session.add(webhook_event_record)

    try:
        # 3. Reconcile transaction or payment session state atomically
        reconciled_session_id = None
        if event_type == "CHECKOUT.ORDER.APPROVED":
            order_id = resource_data.get("id")
            if order_id:
                stmt_ps = select(PaymentSession).where(PaymentSession.paypal_order_id == order_id)
                ps_res = await session.execute(stmt_ps)
                ps = ps_res.scalars().first()
                if ps and ps.status == "CREATED":
                    ps.status = "APPROVED"
                    reconciled_session_id = ps.id

        elif event_type == "PAYMENT.CAPTURE.COMPLETED":
            custom_id = resource_data.get("custom_id")
            if custom_id:
                stmt_ps = select(PaymentSession).where(PaymentSession.id == custom_id)
                ps_res = await session.execute(stmt_ps)
                ps = ps_res.scalars().first()
                if ps:
                    reconciled_session_id = ps.id

        # 4. Record audit log
        audit = AuditLog(
            actor_type="paypal_webhook",
            actor_id=headers.get("paypal-transmission-id", "webhook_transmission"),
            action="PAYPAL_WEBHOOK_PROCESSED",
            entity_type="webhook_event",
            entity_id=event_id,
            metadata_json=json.dumps({
                "event_type": event_type,
                "summary": body.get("summary", ""),
                "reconciled_session_id": reconciled_session_id
            })
        )
        session.add(audit)

        # Commit WebhookEvent + state mutations + audit log atomically
        await session.commit()

    except IntegrityError:
        # Database UNIQUE constraint on webhook_events.event_id triggered!
        # Revert any staged session mutations completely
        await session.rollback()
        return {
            "status": "already_processed",
            "event_type": event_type,
            "event_id": event_id
        }

    log_mongo_audit_event("PAYPAL_WEBHOOK_PROCESSED", {
        "event_id": event_id,
        "event_type": event_type,
        "summary": body.get("summary", ""),
        "resource_id": resource_data.get("id"),
        "resource_status": resource_data.get("status"),
        "reconciled_session_id": reconciled_session_id
    })

    return {
        "status": "received",
        "verified": True,
        "event_type": event_type,
        "event_id": event_id
    }


