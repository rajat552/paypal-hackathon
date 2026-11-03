# PayMesh AI API Reference

**Tagline**: A Trust & Payment Infrastructure for Autonomous AI Commerce  
**Base URL**: `/api/v1`

## Authentication & Authorization
- **Public endpoints**: No authorization required.
- **Publisher/Merchant endpoints**: Protected by API key or Bearer authentication header.
- **Protected resource content**: Requires `Authorization: Bearer <pm_live_token>` header. Missing or invalid tokens return HTTP `402 Payment Required` containing a PayMesh L402 challenge.

---

## 1. Health & Status
- **`GET /health`**
  - **Response 200**: `{ "status": "ok", "app": "PayMesh AI — A Trust & Payment Infrastructure for Autonomous AI Commerce", "timestamp": "...", "database": "connected" }`

---

## 2. Resource Catalogue
- **`GET /api/v1/catalogue`**
  - Returns list of active public resources with publisher info, category, and available access offers.
- **`GET /api/v1/resources/{slug}`**
  - Returns metadata for a specific resource.
- **`GET /api/v1/resources/{slug}/content`**
  - With valid Bearer token (`pm_live_...`): returns protected structured data payload (200 OK).
  - Without token: returns HTTP 402 with PayMesh L402 challenge body.

---

## 3. Payment Sessions & PayPal Sandbox
- **`POST /api/v1/payment-sessions`**
  - **Body**: `{ "challenge_id": "uuid", "offer_id": "uuid", "agent_id": "uuid", "buyer_confirmed": true }`
  - Validates challenge and offer, checks policy limits, creates PayPal Sandbox order with `intent: CAPTURE`, and returns `{ "session_id": "...", "paypal_order_id": "...", "approval_url": "..." }`.
- **`GET /api/v1/payment-sessions/{session_id}`**
  - Returns current status of the payment session (`PENDING`, `APPROVED`, `CAPTURED`, `EXPIRED`, `FAILED`).
- **`POST /api/v1/payment-sessions/{session_id}/capture`**
  - Captures the approved PayPal order on the server, verifies `COMPLETED` status, creates transaction record, and issues new Bearer access token (`pm_live_...`).
  - **Response 200**: `{ "status": "CAPTURED", "access_token": "pm_live_...", "expires_at": "...", "resource_slug": "..." }`

---

## 4. AI Agent & MCP (Model Context Protocol)
- **`POST /api/v1/agent/runs`**
  - Starts or executes an agent task with budget constraint.
- **`POST /api/v1/agent/policy/evaluate`**
  - Runs deterministic policy evaluation against budget, currency, publisher, and offer.
- **`POST /api/v1/agent/tools/{tool_name}`**
  - Directly executes an MCP tool (`paymesh.discover_resources`, `paymesh.get_offer`, `paymesh.request_challenge`, `paymesh.evaluate_purchase`, `paymesh.fetch_resource`).
- **`GET /api/v1/agent/mcp/manifest`**
  - Returns standard Model Context Protocol server tool definitions.

---

## 5. Publisher & Financial Analytics (AG Grid)
- **`POST /api/v1/publisher/resources`**
  - Creates a new data resource.
- **`POST /api/v1/publisher/resources/{id}/offers`**
  - Adds a pricing offer for a resource.
- **`GET /api/v1/publisher/analytics/summary`**
  - Returns KPI metrics (total revenue, captured orders, conversion rate, unique agents).
- **`GET /api/v1/publisher/analytics/transactions`**
  - Returns paginated, filterable transactions designed for AG Grid.
- **`GET /api/v1/publisher/analytics/usage`**
  - Returns usage events by resource and time window.
