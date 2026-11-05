from datetime import UTC, datetime, timedelta
from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.agent.orchestrator import agent_orchestrator
from backend.app.agent.policy import policy_engine
from backend.app.agent.tools import agent_tools
from backend.app.db.session import get_db
from backend.app.mcp.server import mcp_server
from backend.app.models.entities import Transaction
from backend.app.schemas.agent import (
    AgentRunRequest,
    AgentRunResponse,
    PolicyConfigResponse,
    PolicyConfigUpdateRequest,
    PolicyEvaluateRequest,
    PolicyEvaluateResponse,
    ToolExecutionResponse,
)

router = APIRouter(prefix="/agent", tags=["Agent & MCP"])

@router.post("/runs", response_model=AgentRunResponse)
async def run_agent_task(
    request: AgentRunRequest,
    session: AsyncSession = Depends(get_db)
):
    return await agent_orchestrator.run_task(session, request)

@router.post("/policy/evaluate", response_model=PolicyEvaluateResponse)
async def evaluate_policy(
    request: PolicyEvaluateRequest,
    session: AsyncSession = Depends(get_db)
):
    result = await agent_tools.evaluate_purchase_policy(
        session=session,
        offer_id=request.offer_id,
        budget_limit=request.budget_limit,
        currency=request.currency
    )
    return PolicyEvaluateResponse(**result)

@router.get("/policy/config", response_model=PolicyConfigResponse)
async def get_policy_config(session: AsyncSession = Depends(get_db)):
    """Retrieve active deterministic spending policy limits and 24-hour utilized budget."""
    cutoff = datetime.now(UTC) - timedelta(hours=24)
    stmt = select(func.coalesce(func.sum(Transaction.gross_amount), 0.0)).where(
        Transaction.captured_at >= cutoff,
        Transaction.payment_status == "COMPLETED"
    )
    res = await session.execute(stmt)
    rolling_spent = float(res.scalar() or 0.0)

    daily_cap = float(policy_engine.daily_cap)
    pct = min(100, round((rolling_spent / daily_cap * 100))) if daily_cap > 0 else 0

    return PolicyConfigResponse(
        max_per_transaction=policy_engine.max_single_tx_limit,
        daily_cap=daily_cap,
        allowed_currencies=sorted(policy_engine.allowed_currencies),
        auto_approve_under=policy_engine.auto_approve_under,
        enforce_prompt_sanitization=policy_engine.enforce_prompt_sanitization,
        strict_scope_check=policy_engine.strict_scope_check,
        current_utilized_24h=round(rolling_spent, 2),
        utilized_pct=pct
    )

@router.put("/policy/config", response_model=PolicyConfigResponse)
async def update_policy_config(
    request: PolicyConfigUpdateRequest,
    session: AsyncSession = Depends(get_db)
):
    """Update active deterministic spending policy parameters in server memory."""
    policy_engine.max_single_tx_limit = float(request.max_per_transaction)
    policy_engine.daily_cap = float(request.daily_cap)
    policy_engine.allowed_currencies = {c.upper().strip() for c in request.allowed_currencies if c.strip()}
    policy_engine.auto_approve_under = float(request.auto_approve_under)
    policy_engine.enforce_prompt_sanitization = bool(request.enforce_prompt_sanitization)
    policy_engine.strict_scope_check = bool(request.strict_scope_check)

    return await get_policy_config(session)

@router.post("/tools/{tool_name}", response_model=ToolExecutionResponse)
async def execute_tool(
    tool_name: str,
    payload: dict[str, Any],
    session: AsyncSession = Depends(get_db)
):
    try:
        res = await mcp_server.execute_tool(session, tool_name, payload)
        return ToolExecutionResponse(tool_name=tool_name, success=True, result=res)
    except Exception as e:  # noqa: BLE001
        return ToolExecutionResponse(tool_name=tool_name, success=False, result=None, error=str(e))

@router.get("/mcp/manifest")
async def get_mcp_manifest():
    return mcp_server.get_manifest()

@router.post("/mcp/call")
async def call_mcp_tool(
    payload: dict[str, Any],
    session: AsyncSession = Depends(get_db)
):
    tool_name = payload.get("tool_name", "")
    arguments = payload.get("arguments", {})
    return await mcp_server.execute_tool(session, tool_name, arguments)
