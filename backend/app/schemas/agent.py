from typing import Any

from pydantic import BaseModel, Field


class PolicyEvaluateRequest(BaseModel):
    offer_id: str
    budget_limit: float
    currency: str = "USD"
    agent_id: str | None = None

class PolicyEvaluateResponse(BaseModel):
    allowed: bool
    offer_id: str
    amount: float
    currency: str
    budget_limit: float
    reason: str

class PolicyConfigResponse(BaseModel):
    max_per_transaction: float
    daily_cap: float
    allowed_currencies: list[str]
    auto_approve_under: float
    enforce_prompt_sanitization: bool
    strict_scope_check: bool
    current_utilized_24h: float
    utilized_pct: int

class PolicyConfigUpdateRequest(BaseModel):
    max_per_transaction: float = Field(0.50, gt=0.0, le=500.0, description="Max single transaction ceiling")
    daily_cap: float = Field(5.00, gt=0.0, le=5000.0, description="24-hour cumulative spending cap")
    allowed_currencies: list[str] = ["USD"]
    auto_approve_under: float = Field(0.0, ge=0.0, le=50.0, description="Auto-approve threshold")
    enforce_prompt_sanitization: bool = True
    strict_scope_check: bool = True

class AgentRunRequest(BaseModel):
    task: str = Field(..., min_length=2, max_length=1000, description="Natural language search or data research request")
    budget_limit: float = Field(0.10, gt=0.0, le=500.0, description="Maximum amount the buyer is willing to spend")
    currency: str = "USD"
    auto_approve_under_budget: bool = False
    target_resource_slug: str | None = None

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
    ai_mode: str = "deterministic_fallback" # "live_llm" or "deterministic_fallback"
    ai_provider: str | None = None
    ai_model: str | None = None
    interpreted_intent: str | None = None
    comparison_reasoning: str | None = None
    tool_calls_trace: list[dict[str, Any]] | None = None
    recommendation: AgentRecommendation | None = None
    challenge: dict[str, Any] | None = None
    approval_url: str | None = None
    session_id: str | None = None
    summary: str | None = None
    data: dict[str, Any] | None = None

class ToolExecutionRequest(BaseModel):
    tool_name: str
    arguments: dict[str, Any] = {}

class ToolExecutionResponse(BaseModel):
    tool_name: str
    success: bool
    result: Any
    error: str | None = None
