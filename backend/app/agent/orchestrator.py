import uuid
from typing import Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.agent.tools import agent_tools
from backend.app.schemas.agent import AgentRunRequest, AgentRunResponse, AgentRecommendation

class AgentOrchestrator:
    async def run_task(self, session: AsyncSession, request: AgentRunRequest) -> AgentRunResponse:
        run_id = f"run_{uuid.uuid4().hex[:12]}"
        
        # 1. Discover relevant resources based on task keywords
        discovery = await agent_tools.discover_resources(session, query=request.task, limit=3)
        resources = discovery.get("resources", [])
        
        if not resources:
            return AgentRunResponse(
                run_id=run_id,
                task=request.task,
                budget_limit=request.budget_limit,
                status="NO_RESOURCES_FOUND",
                summary="No resources in the publisher catalogue matched your research query."
            )

        # Select most relevant resource
        selected_res = resources[0]
        if not selected_res.get("offers"):
            return AgentRunResponse(
                run_id=run_id,
                task=request.task,
                budget_limit=request.budget_limit,
                status="NO_OFFERS",
                summary=f"Resource '{selected_res['title']}' has no active pricing offers."
            )

        selected_offer = selected_res["offers"][0]
        
        # 2. Deterministic policy check against buyer's budget limit
        policy_res = await agent_tools.evaluate_purchase_policy(
            session=session,
            offer_id=selected_offer["id"],
            budget_limit=request.budget_limit,
            currency=request.currency
        )

        # 3. Create L402 challenge
        challenge_res = await agent_tools.request_access_challenge(
            session=session,
            resource_slug=selected_res["slug"],
            offer_id=selected_offer["id"]
        )

        recommendation = AgentRecommendation(
            resource_slug=selected_res["slug"],
            resource_title=selected_res["title"],
            offer_id=selected_offer["id"],
            offer_title=selected_offer["title"],
            amount=selected_offer["amount"],
            currency=selected_offer["currency"],
            explanation=f"Identified verified benchmark dataset for '{request.task}'. Requires verified 1-hour micro-access.",
            scope_description="Read-only access to complete benchmark dataset and Channel3 source attributes",
            policy_allowed=policy_res["allowed"],
            policy_reason=policy_res["reason"]
        )

        status_text = "AWAITING_APPROVAL" if policy_res["allowed"] else "POLICY_REJECTED"

        return AgentRunResponse(
            run_id=run_id,
            task=request.task,
            budget_limit=request.budget_limit,
            status=status_text,
            recommendation=recommendation,
            challenge=challenge_res,
            summary=f"Agent recommended {selected_res['title']} at ${selected_offer['amount']:.2f} {selected_offer['currency']}. {policy_res['reason']}"
        )

agent_orchestrator = AgentOrchestrator()

