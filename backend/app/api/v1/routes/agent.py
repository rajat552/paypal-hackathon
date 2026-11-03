from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db.session import get_db
from backend.app.schemas.agent import (
    AgentRunRequest, AgentRunResponse,
    PolicyEvaluateRequest, PolicyEvaluateResponse,
    ToolExecutionRequest, ToolExecutionResponse
)
from backend.app.agent.orchestrator import agent_orchestrator
from backend.app.agent.tools import agent_tools
from backend.app.mcp.server import mcp_server

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

@router.post("/tools/{tool_name}", response_model=ToolExecutionResponse)
async def execute_tool(
    tool_name: str,
    payload: Dict[str, Any],
    session: AsyncSession = Depends(get_db)
):
    try:
        res = await mcp_server.execute_tool(session, tool_name, payload)
        return ToolExecutionResponse(tool_name=tool_name, success=True, result=res)
    except Exception as e:
        return ToolExecutionResponse(tool_name=tool_name, success=False, result=None, error=str(e))

@router.get("/mcp/manifest")
async def get_mcp_manifest():
    return mcp_server.get_manifest()

@router.post("/mcp/call")
async def call_mcp_tool(
    payload: Dict[str, Any],
    session: AsyncSession = Depends(get_db)
):
    tool_name = payload.get("tool_name", "")
    arguments = payload.get("arguments", {})
    return await mcp_server.execute_tool(session, tool_name, arguments)

