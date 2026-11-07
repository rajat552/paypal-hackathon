import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.agent.llm_client import llm_client
from backend.app.agent.tools import agent_tools
from backend.app.schemas.agent import (
    AgentRecommendation,
    AgentRunRequest,
    AgentRunResponse,
)
from backend.app.services.resource_service import resource_service


class AgentOrchestrator:
    async def run_task(self, session: AsyncSession, request: AgentRunRequest) -> AgentRunResponse:
        run_id = f"run_{uuid.uuid4().hex[:12]}"

        # Direct / Target Resource mode (e.g. dispatched via Catalogue "Run Agent")
        target_slug = request.target_resource_slug
        if not target_slug:
            for term in request.task.replace("(", " ").replace(")", " ").split():
                clean_term = term.strip(":;,/").lower()
                if clean_term and len(clean_term) >= 2:
                    direct_res = await resource_service.get_by_slug(session, clean_term)
                    if direct_res:
                        target_slug = clean_term
                        break

        if target_slug:
            direct_resource = await resource_service.get_by_slug(session, target_slug)
            if direct_resource and direct_resource.offers:
                active_offers = [o for o in direct_resource.offers if o.active]
                if active_offers:
                    target_offer = active_offers[0]
                    policy_res = await agent_tools.evaluate_purchase_policy(
                        session=session,
                        offer_id=target_offer.id,
                        budget_limit=request.budget_limit,
                        currency=request.currency
                    )
                    challenge_res = await agent_tools.request_access_challenge(
                        session=session,
                        resource_slug=direct_resource.slug,
                        offer_id=target_offer.id
                    )
                    recommendation = AgentRecommendation(
                        resource_slug=direct_resource.slug,
                        resource_title=direct_resource.title,
                        offer_id=target_offer.id,
                        offer_title=target_offer.title,
                        amount=float(target_offer.price_amount),
                        currency=target_offer.currency,
                        explanation=f"Agent directly dispatched to procure verified catalogue resource '{direct_resource.title}'.",
                        scope_description="Read-only access to complete dataset and attributes",
                        policy_allowed=policy_res["allowed"],
                        policy_reason=policy_res["reason"]
                    )
                    status_text = "AWAITING_APPROVAL" if policy_res["allowed"] else "POLICY_REJECTED"
                    return AgentRunResponse(
                        run_id=run_id,
                        task=request.task,
                        budget_limit=request.budget_limit,
                        status=status_text,
                        ai_mode="direct_dispatch",
                        ai_provider="paymesh_gateway",
                        ai_model="catalogue_router",
                        interpreted_intent=f"Procure verified catalogue dataset: {direct_resource.title}",
                        comparison_reasoning=f"Direct 1-click catalogue dispatch targeted '{direct_resource.slug}' with ${target_offer.price_amount} USD offer.",
                        recommendation=recommendation,
                        challenge=challenge_res,
                        summary=f"Routed directly to {direct_resource.title} (${target_offer.price_amount} {target_offer.currency}). {policy_res['reason']}"
                    )

        # Attempt genuine LLM workflow if provider API key is configured
        llm_result = await llm_client.run_agent_workflow(
            session=session,
            task=request.task,
            budget_limit=request.budget_limit,
            currency=request.currency
        )

        if llm_result and llm_result.selected_resource_slug:
            # LLM autonomously discovered and recommended a verified resource
            res_slug = llm_result.selected_resource_slug
            resource = await resource_service.get_by_slug(session, res_slug)
            if resource and resource.offers:
                active_offers = [o for o in resource.offers if o.active]
                target_offer = None
                if llm_result.selected_offer_id:
                    for o in active_offers:
                        if o.id == llm_result.selected_offer_id:
                            target_offer = o
                            break
                if not target_offer and active_offers:
                    target_offer = active_offers[0]

                if target_offer:
                    # Enforce server-side policy check (LLM cannot bypass)
                    policy_res = await agent_tools.evaluate_purchase_policy(
                        session=session,
                        offer_id=target_offer.id,
                        budget_limit=request.budget_limit,
                        currency=request.currency
                    )

                    # Create L402 challenge
                    challenge_res = await agent_tools.request_access_challenge(
                        session=session,
                        resource_slug=resource.slug,
                        offer_id=target_offer.id
                    )

                    recommendation = AgentRecommendation(
                        resource_slug=resource.slug,
                        resource_title=resource.title,
                        offer_id=target_offer.id,
                        offer_title=target_offer.title,
                        amount=float(target_offer.price_amount),
                        currency=target_offer.currency,
                        explanation=llm_result.comparison_reasoning or f"AI analyzed catalogue for '{request.task}' and selected verified resource.",
                        scope_description="Read-only access to complete dataset and attributes",
                        policy_allowed=policy_res["allowed"],
                        policy_reason=policy_res["reason"]
                    )

                    status_text = "AWAITING_APPROVAL" if policy_res["allowed"] else "POLICY_REJECTED"

                    return AgentRunResponse(
                        run_id=run_id,
                        task=request.task,
                        budget_limit=request.budget_limit,
                        status=status_text,
                        ai_mode="live_llm",
                        ai_provider=llm_result.provider,
                        ai_model=llm_result.model,
                        interpreted_intent=llm_result.interpreted_intent,
                        comparison_reasoning=llm_result.comparison_reasoning,
                        tool_calls_trace=llm_result.tool_calls_trace,
                        recommendation=recommendation,
                        challenge=challenge_res,
                        summary=f"[AI Model: {llm_result.model}] Recommended {resource.title} (${target_offer.price_amount} {target_offer.currency}). {policy_res['reason']}"
                    )

        # Fallback / Deterministic Mode: Used when AI key is omitted or LLM failed
        discovery = await agent_tools.discover_resources(session, query=request.task, limit=3)
        resources = discovery.get("resources", [])

        if not resources:
            return AgentRunResponse(
                run_id=run_id,
                task=request.task,
                budget_limit=request.budget_limit,
                status="NO_RESOURCES_FOUND",
                ai_mode="deterministic_fallback",
                summary="No resources in the publisher catalogue matched your research query."
            )

        selected_res = resources[0]
        if not selected_res.get("offers"):
            return AgentRunResponse(
                run_id=run_id,
                task=request.task,
                budget_limit=request.budget_limit,
                status="NO_OFFERS",
                ai_mode="deterministic_fallback",
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
            ai_mode="deterministic_fallback",
            interpreted_intent=f"Catalog match for task: {request.task}",
            comparison_reasoning=f"Matched resource '{selected_res['title']}' via catalogue keywords.",
            tool_calls_trace=[
                {"tool": "discover_resources", "arguments": {"query": request.task, "limit": 3}, "success": True},
                {"tool": "evaluate_purchase_policy", "arguments": {"offer_id": selected_offer["id"], "budget_limit": request.budget_limit}, "success": True}
            ],
            recommendation=recommendation,
            challenge=challenge_res,
            summary=f"Agent recommended {selected_res['title']} at ${selected_offer['amount']:.2f} {selected_offer['currency']}. {policy_res['reason']}"
        )

agent_orchestrator = AgentOrchestrator()
