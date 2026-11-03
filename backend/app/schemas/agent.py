from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field

class PolicyEvaluateRequest(BaseModel):
    offer_id: str
    budget_limit: float
    currency: str = "USD"
    agent_id: Optional[str] = None

class PolicyEvaluateResponse(BaseModel):
    allowed: bool
    offer_id: str
    amount: float
    currency: str
    budget_limit: float
    reason: str

class AgentRunRequest(BaseModel):
    task: str = Field(..., description="Natural language search or data research request")
    budget_limit: float = Field(0.10, description="Maximum amount the buyer is willing to spend")
    currency: str = "USD"
    auto_approve_under_budget: bool = False

class AgentRecommendation(BaseModel):
    resource_slug: str
    resource_title: str
    offer_id: str
    offer_title: str
    amount: float
    currency: str
    explanation: str
    scope_description: str
    policy_allowed: bool
    policy_reason: str

class AgentRunResponse(BaseModel):
    run_id: str
    task: str
    budget_limit: float
    status: str # DISCOVERED, CHALLENGED, AWAITING_APPROVAL, COMPLETED
    recommendation: Optional[AgentRecommendation] = None
    challenge: Optional[Dict[str, Any]] = None
    approval_url: Optional[str] = None
    session_id: Optional[str] = None
    summary: Optional[str] = None
    data: Optional[Dict[str, Any]] = None

class ToolExecutionRequest(BaseModel):
    tool_name: str
    arguments: Dict[str, Any] = {}

class ToolExecutionResponse(BaseModel):
    tool_name: str
    success: bool
    result: Any
    error: Optional[str] = None
