# ADR 001: Architecture, Stack, and Data Commerce Gateway

## Status
Accepted

## Context
PayMesh AI requires an enterprise-ready architecture that connects AI autonomous agents with publisher monetisation through PayPal Sandbox, providing deterministic pricing, verifiable entitlements, and machine-readable L402 protocol challenges.

## Decisions
1. **Backend Framework**: FastAPI with Python 3.11+. Asynchronous request handling, OpenAPI 3.1 generation, and native Pydantic v2 schemas.
2. **Database & ORM**: PostgreSQL with SQLAlchemy 2 (async + sync sessions) and Alembic migrations. SQLite support is provided for zero-dependency local verification.
3. **Frontend Architecture**: React 18 / Tailwind CSS single-page / modular architecture with AG Grid for publisher analytics and responsive UI for AI buyer agent workspace.
4. **PayPal Gateway**: Direct PayPal Sandbox Orders v2 REST client supporting OAuth 2.0 token caching, Order creation (`intent: CAPTURE`), buyer approval redirection, server-side capture verification, and idempotent transaction recording.
5. **AI Orchestration & MCP**: AI Agent engine with deterministic tool calls (`paymesh.discover_resources`, `paymesh.get_offer`, `paymesh.request_challenge`, `paymesh.evaluate_purchase`, `paymesh.fetch_resource`) and Model Context Protocol (MCP) server endpoints.
6. **Data Provider**: Channel3 API integration for normalised retail product intelligence, complete with provider attribution and source links.
