from typing import Dict, Any, List
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.agent.tools import agent_tools
from backend.app.services.challenge_service import challenge_service
from backend.app.services.paypal_gateway import paypal_gateway
from backend.app.models.entities import PaymentSession, Offer, PaymentChallenge
from backend.app.core.exceptions import InvalidChallengeException, PolicyViolationException
from backend.app.agent.policy import policy_engine
from sqlalchemy import select

MCP_TOOLS_MANIFEST: List[Dict[str, Any]] = [
    {
        "name": "paymesh.discover_resources",
        "description": "Search the public PayMesh AI resource catalog for datasets and APIs.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query keywords"},
                "limit": {"type": "integer", "default": 5}
            }
        }
    },
    {
        "name": "paymesh.get_offer",
        "description": "Get server-owned pricing offer details for a specific resource.",
        "input_schema": {
            "type": "object",
            "properties": {
                "resource_slug": {"type": "string", "description": "Resource slug identifier"}
            },
            "required": ["resource_slug"]
        }
    },
    {
        "name": "paymesh.request_challenge",
        "description": "Request protected resource to receive an authoritative L402 challenge.",
        "input_schema": {
            "type": "object",
            "properties": {
                "resource_slug": {"type": "string", "description": "Resource slug identifier"},
                "offer_id": {"type": "string", "description": "Optional offer ID"}
            },
            "required": ["resource_slug"]
        }
    },
    {
        "name": "paymesh.evaluate_purchase",
        "description": "Deterministic check verifying price against budget limits.",
        "input_schema": {
            "type": "object",
            "properties": {
                "offer_id": {"type": "string", "description": "Offer ID to evaluate"},
                "budget_limit": {"type": "number", "description": "Max budget limit"}
            },
            "required": ["offer_id", "budget_limit"]
        }
    },
    {
        "name": "paymesh.fetch_resource",
        "description": "Fetch protected content using a valid Bearer access token.",
        "input_schema": {
            "type": "object",
            "properties": {
                "resource_slug": {"type": "string"},
                "bearer_token": {"type": "string"}
            },
            "required": ["resource_slug", "bearer_token"]
        }
    }
]

class MCPServer:
    def get_manifest(self) -> Dict[str, Any]:
        return {
            "protocol": "mcp",
            "protocol_version": "2024-11-05",
            "server": {"name": "paymesh-ai-mcp-gateway", "version": "2.0.0"},
            "tools": MCP_TOOLS_MANIFEST
        }

    async def execute_tool(
        self,
        session: AsyncSession,
        tool_name: str,
        arguments: Dict[str, Any]
    ) -> Dict[str, Any]:
        # Support both paymesh.* and crawlerpal.* prefixes
        normalized = tool_name.replace("crawlerpal.", "paymesh.")
        
        if normalized == "paymesh.discover_resources":
            return await agent_tools.discover_resources(
                session,
                query=arguments.get("query", ""),
                limit=arguments.get("limit", 5)
            )
        elif normalized == "paymesh.get_offer":
            return await agent_tools.get_resource_offer(
                session,
                resource_slug=arguments.get("resource_slug", "")
            )
        elif normalized == "paymesh.request_challenge":
            return await agent_tools.request_access_challenge(
                session,
                resource_slug=arguments.get("resource_slug", ""),
                offer_id=arguments.get("offer_id")
            )
        elif normalized == "paymesh.evaluate_purchase":
            return await agent_tools.evaluate_purchase_policy(
                session,
                offer_id=arguments.get("offer_id", ""),
                budget_limit=float(arguments.get("budget_limit", 0.0))
            )
        elif normalized == "paymesh.fetch_resource":
            return await agent_tools.fetch_entitled_resource(
                session,
                resource_slug=arguments.get("resource_slug", ""),
                bearer_token=arguments.get("bearer_token", "")
            )
        else:
            return {"error": f"Unknown tool: {tool_name}"}

mcp_server = MCPServer()
