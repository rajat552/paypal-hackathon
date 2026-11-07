from unittest.mock import AsyncMock, patch
import pytest
from httpx import AsyncClient

from backend.app.services.paypal_gateway import paypal_gateway


@pytest.mark.asyncio
async def test_health_endpoint(async_client: AsyncClient):
    resp = await async_client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert "PayMesh AI" in data["app"]

@pytest.mark.asyncio
async def test_catalogue_endpoint(async_client: AsyncClient):
    resp = await async_client.get("/api/v1/catalogue")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] >= 1
    assert any(r["slug"] == "product-intelligence-report" for r in data["resources"])

@pytest.mark.asyncio
async def test_protected_resource_returns_402_challenge(async_client: AsyncClient):
    resp = await async_client.get("/api/v1/resources/product-intelligence-report/content")
    assert resp.status_code == 402
    data = resp.json()
    assert data["protocol"] == "paymesh-l402"
    assert "challenge_id" in data
    assert len(data["offers"]) >= 1
    assert data["offers"][0]["amount"] > 0
    assert data["offers"][0]["payment_method"] == "paypal"

@pytest.mark.asyncio
async def test_full_payment_capture_and_retrieval_flow(async_client: AsyncClient):
    # 1. Trigger 402 challenge
    c_resp = await async_client.get("/api/v1/resources/product-intelligence-report/content")
    assert c_resp.status_code == 402
    c_data = c_resp.json()
    challenge_id = c_data["challenge_id"]
    offer_id = c_data["offers"][0]["id"]

    # 2. Create Payment Session
    sess_payload = {
        "challenge_id": challenge_id,
        "offer_id": offer_id,
        "buyer_confirmed": True
    }
    s_resp = await async_client.post("/api/v1/payment-sessions", json=sess_payload)
    assert s_resp.status_code == 200
    s_data = s_resp.json()
    session_id = s_data["session_id"]
    assert "paypal_order_id" in s_data
    assert "approval_url" in s_data

    # 3a. Verify unapproved order capture fails honestly with 502
    unapproved_resp = await async_client.post(f"/api/v1/payment-sessions/{session_id}/capture", json={})
    assert unapproved_resp.status_code == 502
    assert "ORDER_NOT_APPROVED" in unapproved_resp.json().get("error", "") or "not been approved" in unapproved_resp.json().get("message", "")

    # 3b. Verify successful capture via controlled test fixture
    with patch.object(paypal_gateway, "capture_order", new_callable=AsyncMock) as mock_capture:
        mock_capture.return_value = {
            "id": s_data["paypal_order_id"],
            "status": "COMPLETED",
            "capture_id": "CAP-TEST-FIXTURE-12345",
            "raw_response": {"status": "COMPLETED", "fixture": True}
        }
        cap_resp = await async_client.post(f"/api/v1/payment-sessions/{session_id}/capture", json={})
        assert cap_resp.status_code == 200
        cap_data = cap_resp.json()
        assert cap_data["status"] == "CAPTURED"
        raw_token = cap_data["access_token"]
        assert raw_token.startswith("pm_live_")

    # 4. Fetch protected content with newly issued Bearer token
    headers = {"Authorization": f"Bearer {raw_token}"}
    p_resp = await async_client.get("/api/v1/resources/product-intelligence-report/content", headers=headers)
    assert p_resp.status_code == 200
    p_data = p_resp.json()
    assert p_data["slug"] == "product-intelligence-report"
    assert "benchmarks" in p_data["data"]
    assert len(p_data["data"]["benchmarks"]) >= 1

    # 5. Verify invalid token is rejected with 402
    bad_headers = {"Authorization": "Bearer pm_live_tampered_fake_token"}
    bad_resp = await async_client.get("/api/v1/resources/product-intelligence-report/content", headers=bad_headers)
    assert bad_resp.status_code == 402

@pytest.mark.asyncio
async def test_simulate_buyer_approval_instant_capture(async_client: AsyncClient):
    # 1. Challenge
    c_resp = await async_client.get("/api/v1/resources/product-intelligence-report/content")
    c_data = c_resp.json()
    challenge_id = c_data["challenge_id"]
    offer_id = c_data["offers"][0]["id"]

    # 2. Payment Session
    sess_payload = {
        "challenge_id": challenge_id,
        "offer_id": offer_id,
        "buyer_confirmed": True
    }
    s_resp = await async_client.post("/api/v1/payment-sessions", json=sess_payload)
    assert s_resp.status_code == 200
    session_id = s_resp.json()["session_id"]

    # 3. Simulate buyer approval capture without PayPal login
    cap_resp = await async_client.post(
        f"/api/v1/payment-sessions/{session_id}/capture",
        json={"simulate_buyer_approval": True}
    )
    assert cap_resp.status_code == 200
    cap_data = cap_resp.json()
    assert cap_data["status"] == "CAPTURED"
    assert cap_data["paypal_capture_id"].startswith("CAP-SANDBOX-AUTH-")
    assert cap_data["access_token"].startswith("pm_live_")

    # 4. Access content with newly issued token
    headers = {"Authorization": f"Bearer {cap_data['access_token']}"}
    p_resp = await async_client.get("/api/v1/resources/product-intelligence-report/content", headers=headers)
    assert p_resp.status_code == 200
    assert p_resp.json()["slug"] == "product-intelligence-report"

@pytest.mark.asyncio
async def test_agent_run_orchestration(async_client: AsyncClient):
    task_payload = {
        "task": "Find mechanical keyboards latency benchmarks",
        "budget_limit": 0.10,
        "currency": "USD"
    }
    resp = await async_client.post("/api/v1/agent/runs", json=task_payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "AWAITING_APPROVAL"
    assert data["recommendation"]["policy_allowed"] is True
    assert data["recommendation"]["amount"] <= 0.10

@pytest.mark.asyncio
async def test_mcp_manifest_and_tool_execution(async_client: AsyncClient):
    # Manifest
    m_resp = await async_client.get("/api/v1/agent/mcp/manifest")
    assert m_resp.status_code == 200
    manifest = m_resp.json()
    assert manifest["protocol"] == "mcp"
    assert len(manifest["tools"]) >= 4

    # Tool call
    tool_payload = {
        "tool_name": "paymesh.discover_resources",
        "arguments": {"query": "keyboard", "limit": 3}
    }
    t_resp = await async_client.post("/api/v1/agent/mcp/call", json=tool_payload)
    assert t_resp.status_code == 200
    t_data = t_resp.json()
    assert t_data["count"] >= 1

@pytest.mark.asyncio
async def test_legacy_bot_l402_and_payment_flow(async_client: AsyncClient):
    # Bot request without browser user-agent
    headers = {"User-Agent": "python-requests/2.31.0"}
    resp = await async_client.get("/", headers=headers)
    assert resp.status_code == 402
    data = resp.json()
    assert "payment_request_url" in data
    assert "payment_context_token" in data

    # Call legacy payment route with controlled test fixture for capture
    pay_payload = {
        "payment_context_token": data["payment_context_token"],
        "offer_id": "all_categories"
    }
    with patch.object(paypal_gateway, "capture_order", new_callable=AsyncMock) as mock_capture:
        mock_capture.return_value = {
            "id": "ORDER-LEGACY-MOCK",
            "status": "COMPLETED",
            "capture_id": "CAP-LEGACY-12345",
            "raw_response": {"status": "COMPLETED", "fixture": True}
        }
        p_resp = await async_client.post("/l402/payment-request", json=pay_payload)
        assert p_resp.status_code == 200
        p_data = p_resp.json()
        assert p_data["message"] == "Payment successful"
        bearer_token = p_data["bearer_token"]

    # Authenticated bot request
    auth_headers = {"User-Agent": "python-requests/2.31.0", "Authorization": f"Bearer {bearer_token}"}
    a_resp = await async_client.get("/", headers=auth_headers)
    assert a_resp.status_code == 200
    a_data = a_resp.json()
    assert a_data["status"] == "authenticated"

@pytest.mark.asyncio
async def test_security_headers_enforced(async_client: AsyncClient):
    resp = await async_client.get("/health")
    assert resp.status_code == 200
    assert resp.headers.get("x-content-type-options") == "nosniff"
    assert resp.headers.get("x-frame-options") == "SAMEORIGIN"
    assert "strict-origin-when-cross-origin" in resp.headers.get("referrer-policy", "")

@pytest.mark.asyncio
async def test_publisher_validation_rejects_invalid_currency(async_client: AsyncClient):
    # Retrieve catalogue to get valid resource ID
    cat_resp = await async_client.get("/api/v1/catalogue")
    res_id = cat_resp.json()["resources"][0]["id"]

    bad_payload = {
        "offer_code": "bad_curr_offer",
        "title": "Bad Currency Offer",
        "description": "Offering in unsupported cryptocurrency",
        "price_amount": 1.0,
        "currency": "BTC",
        "pricing_model": "one_time",
        "duration_seconds": 3600
    }
    resp = await async_client.post(f"/api/v1/publisher/resources/{res_id}/offers", json=bad_payload)
    assert resp.status_code == 400
    assert "not allowed" in resp.json()["detail"]

@pytest.mark.asyncio
async def test_agent_orchestration_returns_ai_metadata(async_client: AsyncClient):
    task_payload = {
        "task": "Find low latency mechanical keyboards",
        "budget_limit": 0.20,
        "currency": "USD"
    }
    resp = await async_client.post("/api/v1/agent/runs", json=task_payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["ai_mode"] in ("live_llm", "deterministic_fallback")
    assert data["tool_calls_trace"] is not None
    assert len(data["tool_calls_trace"]) >= 1

@pytest.mark.asyncio
async def test_paypal_webhook_handler(async_client: AsyncClient):
    webhook_payload = {
        "id": "WH-TEST-EVENT-001",
        "event_type": "PAYMENT.CAPTURE.COMPLETED",
        "summary": "Payment capture completed successfully",
        "resource": {
            "id": "CAP-TEST-12345",
            "status": "COMPLETED",
            "amount": {"value": "0.01", "currency_code": "USD"}
        }
    }
    valid_headers = {
        "PAYPAL-TRANSMISSION-ID": "tx-webhook-123",
        "PAYPAL-AUTH-ALGO": "SHA256withRSA",
        "PAYPAL-CERT-URL": "https://api.sandbox.paypal.com/v1/notifications/certs/CERT-123",
        "PAYPAL-TRANSMISSION-SIG": "mock_signature_data",
        "PAYPAL-TRANSMISSION-TIME": "2026-11-05T10:00:00Z"
    }

    # 1. Unauthenticated webhook without transmission headers is rejected
    unauth_resp = await async_client.post("/api/v1/payments/webhook", json=webhook_payload)
    assert unauth_resp.status_code == 401

    # 2. Verified webhook via controlled test fixture
    with patch.object(paypal_gateway, "verify_webhook_signature", new_callable=AsyncMock) as mock_verify:
        mock_verify.return_value = True
        resp = await async_client.post("/api/v1/payments/webhook", json=webhook_payload, headers=valid_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "received"
        assert data["event_type"] == "PAYMENT.CAPTURE.COMPLETED"

        # Test duplicate webhook idempotency
        dup_resp = await async_client.post("/api/v1/payments/webhook", json=webhook_payload, headers=valid_headers)
        assert dup_resp.status_code == 200
        dup_data = dup_resp.json()
        assert dup_data["status"] == "already_processed"

@pytest.mark.asyncio
async def test_policy_config_get_and_update(async_client: AsyncClient):
    # Test GET
    get_resp = await async_client.get("/api/v1/agent/policy/config")
    assert get_resp.status_code == 200
    cfg = get_resp.json()
    assert "max_per_transaction" in cfg
    assert "daily_cap" in cfg
    assert "current_utilized_24h" in cfg

    # Test PUT update
    update_payload = {
        "max_per_transaction": 1.25,
        "daily_cap": 10.00,
        "allowed_currencies": ["USD", "EUR"],
        "auto_approve_under": 0.05,
        "enforce_prompt_sanitization": True,
        "strict_scope_check": True
    }
    put_resp = await async_client.put("/api/v1/agent/policy/config", json=update_payload)
    assert put_resp.status_code == 200
    updated_cfg = put_resp.json()
    assert updated_cfg["max_per_transaction"] == 1.25
    assert updated_cfg["daily_cap"] == 10.00
    assert "USD" in updated_cfg["allowed_currencies"]
