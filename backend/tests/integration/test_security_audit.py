import pytest
from httpx import AsyncClient

from backend.app.models.entities import Resource, User
from backend.app.services.paypal_gateway import (
    PAYPAL_CERT_URL_REGEX,
    paypal_gateway,
)
from backend.tests.conftest import TestAsyncSessionLocal


@pytest.mark.asyncio
async def test_webhook_rejects_untrusted_cert_urls(async_client: AsyncClient):
    """Verify PayPal webhook handler rejects spoofed or non-PayPal certificate URLs (SSRF mitigation)."""
    malicious_cert_urls = [
        "http://169.254.169.254/latest/meta-data/",
        "https://attacker.com/certs/fake.pem",
        "http://localhost:8000/internal/cert",
        "ftp://api.paypal.com/cert",
        "https://api.paypal.com.evil.com/v1/notifications/certs/CERT-1",
        "javascript:alert(1)"
    ]

    webhook_payload = {
        "id": "WH-TEST-SSRF-001",
        "event_type": "PAYMENT.CAPTURE.COMPLETED",
        "summary": "Capture completed",
        "resource": {"id": "CAP-123", "status": "COMPLETED"}
    }

    for bad_url in malicious_cert_urls:
        headers = {
            "PAYPAL-TRANSMISSION-ID": "tx-ssrf-test",
            "PAYPAL-AUTH-ALGO": "SHA256withRSA",
            "PAYPAL-CERT-URL": bad_url,
            "PAYPAL-TRANSMISSION-SIG": "mock_sig",
            "PAYPAL-TRANSMISSION-TIME": "2026-11-08T12:00:00Z"
        }
        resp = await async_client.post("/api/v1/payments/webhook", json=webhook_payload, headers=headers)
        assert resp.status_code == 401, f"Failed to reject untrusted cert URL: {bad_url}"


def test_paypal_cert_url_regex():
    """Verify cert URL regex accepts only official PayPal certificate endpoints."""
    assert PAYPAL_CERT_URL_REGEX.match("https://api.paypal.com/v1/notifications/certs/CERT-360742354-12345")
    assert PAYPAL_CERT_URL_REGEX.match("https://api.sandbox.paypal.com/v1/notifications/certs/CERT-123")
    assert not PAYPAL_CERT_URL_REGEX.match("http://api.paypal.com/v1/notifications/certs/CERT-123")
    assert not PAYPAL_CERT_URL_REGEX.match("https://evil.paypal.com/v1/notifications/certs/CERT-123")
    assert not PAYPAL_CERT_URL_REGEX.match("https://api.paypal.com/other/path/cert")


def test_safe_redirect_url_validation():
    """Verify open-redirect defense: only trusted frontends and Vercel domains are allowed."""
    assert paypal_gateway._is_safe_redirect_url("http://localhost:3000/checkout/success")
    assert paypal_gateway._is_safe_redirect_url("https://paypal-hackathon-mu.vercel.app/checkout/success")
    assert paypal_gateway._is_safe_redirect_url("https://my-preview.vercel.app/checkout/cancel")
    assert not paypal_gateway._is_safe_redirect_url("https://evil-phishing-site.com/steal")
    assert not paypal_gateway._is_safe_redirect_url("javascript:stealData()")
    assert not paypal_gateway._is_safe_redirect_url("data:text/html,<html>")


@pytest.mark.asyncio
async def test_health_check_does_not_leak_exception(async_client: AsyncClient):
    """Verify health endpoint masks internal database or connection errors."""
    resp = await async_client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] in ("ok", "degraded")
    assert "error" not in data.get("mongodb", {})
    # Ensure no python traceback keywords appear
    assert "Traceback" not in resp.text
    assert "OperationalError" not in resp.text


@pytest.mark.asyncio
async def test_policy_config_bounds_enforced(async_client: AsyncClient):
    """Verify spending policy update rejects negative or astronomical limit values."""
    # Negative ceiling
    bad_payload_neg = {
        "max_per_transaction": -5.0,
        "daily_cap": 10.0,
        "allowed_currencies": ["USD"]
    }
    resp_neg = await async_client.put("/api/v1/agent/policy/config", json=bad_payload_neg)
    assert resp_neg.status_code == 422

    # Astronomical ceiling beyond safety limit
    bad_payload_huge = {
        "max_per_transaction": 999999.0,
        "daily_cap": 10.0,
        "allowed_currencies": ["USD"]
    }
    resp_huge = await async_client.put("/api/v1/agent/policy/config", json=bad_payload_huge)
    assert resp_huge.status_code == 422


@pytest.mark.asyncio
async def test_agent_run_task_length_enforced(async_client: AsyncClient):
    """Verify agent rejects empty tasks or tasks exceeding maximum length."""
    # Empty task
    resp_empty = await async_client.post("/api/v1/agent/runs", json={"task": "", "budget_limit": 1.0})
    assert resp_empty.status_code == 422

    # Oversized payload
    resp_huge = await async_client.post("/api/v1/agent/runs", json={"task": "A" * 1001, "budget_limit": 1.0})
    assert resp_huge.status_code == 422


@pytest.mark.asyncio
async def test_publisher_idor_prevention(async_client: AsyncClient):
    """Verify a publisher cannot attach offers to resources owned by another tenant/publisher."""
    async with TestAsyncSessionLocal() as db_session:
        # Create alien publisher
        alien_user = User(
            email="alien_publisher@external-domain.com",
            password_hash="system_managed",
            role="publisher"
        )
        db_session.add(alien_user)
        await db_session.commit()
        await db_session.refresh(alien_user)

        # Create alien resource
        alien_resource = Resource(
            publisher_id=alien_user.id,
            slug="alien-proprietary-dataset",
            title="Alien Proprietary Dataset",
            description="Confidential high-value dataset",
            resource_type="dataset",
            provider="alien_lab"
        )
        db_session.add(alien_resource)
        await db_session.commit()
        await db_session.refresh(alien_resource)

    # Attempt to attach an offer to the alien resource as the default publisher
    offer_payload = {
        "offer_code": "unauthorized_offer",
        "title": "Malicious Price Injection",
        "description": "Attempting cross-tenant offer attachment",
        "price_amount": 0.05,
        "currency": "USD",
        "pricing_model": "one_time",
        "duration_seconds": 3600
    }
    resp = await async_client.post(f"/api/v1/publisher/resources/{alien_resource.id}/offers", json=offer_payload)
    assert resp.status_code == 403
    assert "Forbidden" in resp.json()["detail"]
