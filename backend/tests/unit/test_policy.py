from backend.app.agent.policy import policy_engine
from backend.app.models.entities import Offer


def test_policy_within_budget():
    offer = Offer(
        id="test_offer",
        resource_id="test_res",
        offer_code="test_code",
        title="Test",
        description="Test",
        price_amount=0.05,
        currency="USD",
        active=True
    )
    allowed, reason = policy_engine.evaluate(offer, budget_limit=0.10, currency="USD")
    assert allowed is True
    assert "Policy passed" in reason

def test_policy_exceeds_budget():
    offer = Offer(
        id="test_offer",
        resource_id="test_res",
        offer_code="test_code",
        title="Test",
        description="Test",
        price_amount=0.50,
        currency="USD",
        active=True
    )
    allowed, reason = policy_engine.evaluate(offer, budget_limit=0.10, currency="USD")
    assert allowed is False
    assert "exceeds buyer budget" in reason

def test_policy_currency_mismatch():
    offer = Offer(
        id="test_offer",
        resource_id="test_res",
        offer_code="test_code",
        title="Test",
        description="Test",
        price_amount=0.05,
        currency="USD",
        active=True
    )
    allowed, reason = policy_engine.evaluate(offer, budget_limit=0.10, currency="EUR")
    assert allowed is False
    assert "Currency mismatch" in reason

def test_policy_inactive_offer():
    offer = Offer(
        id="test_offer",
        resource_id="test_res",
        offer_code="test_code",
        title="Test",
        description="Test",
        price_amount=0.05,
        currency="USD",
        active=False
    )
    allowed, reason = policy_engine.evaluate(offer, budget_limit=0.10, currency="USD")
    assert allowed is False
    assert "inactive" in reason

def test_policy_disallowed_currency():
    offer = Offer(
        id="test_offer",
        resource_id="test_res",
        offer_code="test_code",
        title="Test",
        description="Test",
        price_amount=0.05,
        currency="BTC",
        active=True
    )
    allowed, reason = policy_engine.evaluate(offer, budget_limit=0.10, currency="BTC")
    assert allowed is False
    assert "not in allowed currency" in reason

def test_policy_exceeds_platform_ceiling():
    offer = Offer(
        id="test_offer",
        resource_id="test_res",
        offer_code="test_code",
        title="Test",
        description="Test",
        price_amount=50.00,
        currency="USD",
        active=True
    )
    allowed, reason = policy_engine.evaluate(offer, budget_limit=100.00, currency="USD")
    assert allowed is False
    assert "safety ceiling" in reason
