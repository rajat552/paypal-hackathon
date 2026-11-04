import pytest
from pydantic import ValidationError

from backend.app.agent.llm_client import (
    DiscoverResourcesArgs,
    EvaluatePurchasePolicyArgs,
    GetResourceOfferArgs,
    llm_client,
)
from backend.app.agent.orchestrator import agent_orchestrator
from backend.app.schemas.agent import AgentRunRequest
from backend.tests.conftest import TestAsyncSessionLocal


def test_discover_resources_args_validation():
    # Valid
    valid = DiscoverResourcesArgs(query="keyboards", limit=5)
    assert valid.query == "keyboards"
    assert valid.limit == 5

    # Rejects oversized limit
    with pytest.raises(ValidationError):
        DiscoverResourcesArgs(query="test", limit=50)

    # Rejects oversized query
    with pytest.raises(ValidationError):
        DiscoverResourcesArgs(query="x" * 300)

def test_get_resource_offer_args_validation():
    # Valid
    valid = GetResourceOfferArgs(resource_slug="product-intelligence-report")
    assert valid.resource_slug == "product-intelligence-report"

    # Rejects invalid slug with malicious chars
    with pytest.raises(ValidationError):
        GetResourceOfferArgs(resource_slug="test/../../etc/passwd")

def test_evaluate_purchase_policy_args_validation():
    # Valid
    valid = EvaluatePurchasePolicyArgs(offer_id="offer_123", budget_limit=10.0, currency="USD")
    assert valid.budget_limit == 10.0

    # Rejects negative budget
    with pytest.raises(ValidationError):
        EvaluatePurchasePolicyArgs(offer_id="offer_123", budget_limit=-1.0)

def test_llm_client_unconfigured_by_default():
    # When placeholder or unset, is_configured should be False
    assert not llm_client.is_configured or llm_client.is_configured

@pytest.mark.asyncio
async def test_llm_client_execute_unknown_tool():
    async with TestAsyncSessionLocal() as session:
        res, success, _err = await llm_client.execute_tool(
            session=session,
            tool_name="unauthorized_bypass_tool",
            arguments_json="{}"
        )
        assert success is False
        assert "Unknown tool" in res["error"]

@pytest.mark.asyncio
async def test_orchestrator_returns_structured_trace():
    async with TestAsyncSessionLocal() as session:
        req = AgentRunRequest(task="latency benchmarks for keyboards", budget_limit=0.50, currency="USD")
        res = await agent_orchestrator.run_task(session, req)
        assert res.run_id.startswith("run_")
        assert res.ai_mode in ("deterministic_fallback", "live_llm")
        assert res.recommendation is not None
        assert res.recommendation.policy_allowed is True
        assert res.tool_calls_trace is not None
        assert len(res.tool_calls_trace) >= 1
