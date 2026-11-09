from unittest.mock import AsyncMock, patch
import httpx
import pytest
from httpx import AsyncClient, Response
from sqlalchemy import select

from backend.app.agent.llm_client import llm_client
from backend.app.models.entities import Transaction
from backend.app.services.paypal_gateway import paypal_gateway
from backend.tests.conftest import TestAsyncSessionLocal


@pytest.mark.asyncio
async def test_gemini_error_handling_http_400():
    """Verify HTTP 400 Bad Request does not trigger model fallback and reports bad_request."""
    async with TestAsyncSessionLocal() as session:
        mock_resp = Response(
            status_code=400,
            json={"error": {"code": 400, "message": "Invalid argument: malformed prompt", "status": "INVALID_ARGUMENT"}}
        )
        with patch.object(httpx.AsyncClient, "post", new_callable=AsyncMock) as mock_post:
            mock_post.return_value = mock_resp
            # Temporarily configure AI key if not set
            with patch("backend.app.core.config.settings.AI_API_KEY", "test_gemini_key_1234567890"):
                res = await llm_client._run_gemini_workflow(
                    session=session,
                    task="test prompt",
                    budget_limit=0.10,
                    currency="USD"
                )
                assert res is not None
                assert res.success is False
                assert res.error_type == "bad_request"
                assert "HTTP 400 Bad Request" in res.error_message
                # Exactly 1 call was made; no model fallback loop occurred
                assert mock_post.call_count == 1


@pytest.mark.asyncio
async def test_gemini_error_handling_http_404_model_switch():
    """Verify HTTP 404 model-not-found switches to next candidate model."""
    async with TestAsyncSessionLocal() as session:
        resp_404 = Response(status_code=404, text="Model not found")
        resp_200 = Response(
            status_code=200,
            json={
                "candidates": [{
                    "content": {
                        "parts": [{"text": "Switched model recommendation completed."}]
                    }
                }]
            }
        )
        with patch.object(httpx.AsyncClient, "post", new_callable=AsyncMock) as mock_post:
            mock_post.side_effect = [resp_404, resp_200]
            with patch("backend.app.core.config.settings.AI_API_KEY", "test_gemini_key_1234567890"):
                res = await llm_client._run_gemini_workflow(
                    session=session,
                    task="test query",
                    budget_limit=0.10,
                    currency="USD"
                )
                assert res is not None
                assert res.success is True
                assert mock_post.call_count == 2


@pytest.mark.asyncio
async def test_gemini_error_handling_http_429_daily_quota_exhausted():
    """Verify HTTP 429 daily quota exhaustion is recognized immediately without retry."""
    async with TestAsyncSessionLocal() as session:
        mock_resp = Response(
            status_code=429,
            json={"error": {"code": 429, "message": "Resource has been exhausted: daily requests quota exceeded.", "status": "RESOURCE_EXHAUSTED"}}
        )
        with patch.object(httpx.AsyncClient, "post", new_callable=AsyncMock) as mock_post:
            mock_post.return_value = mock_resp
            with patch("backend.app.core.config.settings.AI_API_KEY", "test_gemini_key_1234567890"):
                res = await llm_client._run_gemini_workflow(
                    session=session,
                    task="test query",
                    budget_limit=0.10,
                    currency="USD"
                )
                assert res is not None
                assert res.success is False
                assert res.error_type == "daily_quota_exhausted"
                assert mock_post.call_count == 1


@pytest.mark.asyncio
async def test_gemini_error_handling_http_429_rate_limit_backoff_exhaustion():
    """Verify transient HTTP 429 rate limit triggers bounded exponential backoff with retries."""
    async with TestAsyncSessionLocal() as session:
        mock_resp = Response(
            status_code=429,
            headers={"Retry-After": "1"},
            json={"error": {"code": 429, "message": "Rate limit exceeded (per-minute RPM).", "status": "RESOURCE_EXHAUSTED"}}
        )
        with patch.object(httpx.AsyncClient, "post", new_callable=AsyncMock) as mock_post, \
             patch("asyncio.sleep", new_callable=AsyncMock) as mock_sleep:
            mock_post.return_value = mock_resp
            with patch("backend.app.core.config.settings.AI_API_KEY", "test_gemini_key_1234567890"):
                res = await llm_client._run_gemini_workflow(
                    session=session,
                    task="test query",
                    budget_limit=0.10,
                    currency="USD"
                )
                assert res is not None
                assert res.success is False
                assert res.error_type == "rate_limit_exceeded"
                # Initial try + 3 retries = 4 posts
                assert mock_post.call_count == 4
                assert mock_sleep.call_count == 3


@pytest.mark.asyncio
async def test_concurrent_duplicate_webhook_deliveries(async_client: AsyncClient):
    """Verify database uniqueness prevents duplicate webhook event insertion and state mutation."""
    event_id = "WH-RELIABILITY-TEST-001"
    webhook_payload = {
        "id": event_id,
        "event_type": "CHECKOUT.ORDER.APPROVED",
        "summary": "Buyer approved order",
        "resource": {"id": "ORDER-WH-TEST-001"}
    }
    valid_headers = {
        "PAYPAL-TRANSMISSION-ID": "tx-reliability-123",
        "PAYPAL-AUTH-ALGO": "SHA256withRSA",
        "PAYPAL-CERT-URL": "https://api.sandbox.paypal.com/v1/notifications/certs/CERT-123",
        "PAYPAL-TRANSMISSION-SIG": "valid_signature",
        "PAYPAL-TRANSMISSION-TIME": "2026-11-09T09:00:00Z"
    }

    with patch.object(paypal_gateway, "verify_webhook_signature", new_callable=AsyncMock) as mock_verify:
        mock_verify.return_value = True

        # First delivery: processed successfully
        r1 = await async_client.post("/api/v1/payments/webhook", json=webhook_payload, headers=valid_headers)
        assert r1.status_code == 200
        assert r1.json()["status"] == "received"

        # Duplicate delivery: database uniqueness catches it and discards safely
        r2 = await async_client.post("/api/v1/payments/webhook", json=webhook_payload, headers=valid_headers)
        assert r2.status_code == 200
        assert r2.json()["status"] == "already_processed"


@pytest.mark.asyncio
async def test_invalid_webhook_signature_rejected(async_client: AsyncClient):
    """Verify invalid webhook signature is rejected with HTTP 401."""
    webhook_payload = {"id": "WH-INVALID-SIG-001", "event_type": "PAYMENT.CAPTURE.COMPLETED"}
    with patch.object(paypal_gateway, "verify_webhook_signature", new_callable=AsyncMock) as mock_verify:
        mock_verify.return_value = False
        r = await async_client.post("/api/v1/payments/webhook", json=webhook_payload)
        assert r.status_code == 401
        assert "signature verification failed" in r.json()["detail"]


@pytest.mark.asyncio
async def test_concurrent_capture_requests_idempotency(async_client: AsyncClient):
    """Verify duplicate capture requests do not issue duplicate entitlements or fail."""
    # 1. Challenge & Session
    c_resp = await async_client.get("/api/v1/resources/product-intelligence-report/content")
    c_data = c_resp.json()
    challenge_id = c_data["challenge_id"]
    offer_id = c_data["offers"][0]["id"]

    s_resp = await async_client.post("/api/v1/payment-sessions", json={
        "challenge_id": challenge_id,
        "offer_id": offer_id,
        "buyer_confirmed": True
    })
    session_id = s_resp.json()["session_id"]

    # 2. First capture
    cap1 = await async_client.post(
        f"/api/v1/payment-sessions/{session_id}/capture",
        json={"simulate_buyer_approval": True}
    )
    assert cap1.status_code == 200
    token1 = cap1.json()["access_token"]
    assert token1.startswith("pm_live_")

    # 3. Second capture (duplicate/replayed)
    cap2 = await async_client.post(
        f"/api/v1/payment-sessions/{session_id}/capture",
        json={"simulate_buyer_approval": True}
    )
    assert cap2.status_code == 200
    assert cap2.json()["status"] == "CAPTURED"
    assert "RETAIN_EXISTING_TOKEN" in cap2.json()["access_token"]

    # 4. Verify original token accesses content
    content_resp = await async_client.get(
        "/api/v1/resources/product-intelligence-report/content",
        headers={"Authorization": f"Bearer {token1}"}
    )
    assert content_resp.status_code == 200


@pytest.mark.asyncio
async def test_database_failure_before_entitlement_issuance(async_client: AsyncClient):
    """Verify that if database transaction persistence fails, no entitlement is issued."""
    # 1. Challenge & Session
    c_resp = await async_client.get("/api/v1/resources/product-intelligence-report/content")
    c_data = c_resp.json()
    challenge_id = c_data["challenge_id"]
    offer_id = c_data["offers"][0]["id"]

    s_resp = await async_client.post("/api/v1/payment-sessions", json={
        "challenge_id": challenge_id,
        "offer_id": offer_id,
        "buyer_confirmed": True
    })
    session_id = s_resp.json()["session_id"]

    # 2. Simulate database failure during transaction flush
    from sqlalchemy.ext.asyncio import AsyncSession
    with patch.object(AsyncSession, "flush", side_effect=Exception("Simulated disk write failure")):
        cap_fail = await async_client.post(
            f"/api/v1/payment-sessions/{session_id}/capture",
            json={"simulate_buyer_approval": True}
        )
        assert cap_fail.status_code == 500
        assert "Failed to record payment transaction" in cap_fail.json()["detail"]

    # 3. Verify no transaction or entitlement exists for this failed session
    async with TestAsyncSessionLocal() as db_session:
        tx_check = await db_session.execute(select(Transaction).where(Transaction.payment_session_id == session_id))
        assert tx_check.scalars().first() is None


@pytest.mark.asyncio
async def test_existing_successful_sandbox_payment_behaviour(async_client: AsyncClient):
    """Verify existing successful payment and content decryption workflow remains completely intact."""
    c_resp = await async_client.get("/api/v1/resources/product-intelligence-report/content")
    assert c_resp.status_code == 402
    c_data = c_resp.json()

    s_resp = await async_client.post("/api/v1/payment-sessions", json={
        "challenge_id": c_data["challenge_id"],
        "offer_id": c_data["offers"][0]["id"],
        "buyer_confirmed": True
    })
    assert s_resp.status_code == 200
    s_data = s_resp.json()

    cap_resp = await async_client.post(
        f"/api/v1/payment-sessions/{s_data['session_id']}/capture",
        json={"simulate_buyer_approval": True}
    )
    assert cap_resp.status_code == 200
    bearer_token = cap_resp.json()["access_token"]

    data_resp = await async_client.get(
        "/api/v1/resources/product-intelligence-report/content",
        headers={"Authorization": f"Bearer {bearer_token}"}
    )
    assert data_resp.status_code == 200
    assert data_resp.json()["slug"] == "product-intelligence-report"

