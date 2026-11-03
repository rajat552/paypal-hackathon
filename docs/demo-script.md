# PayMesh AI Hackathon Demo Script (Under 3 Minutes)

**Product:** PayMesh AI — A Trust & Payment Infrastructure for Autonomous AI Commerce  
**Track:** PayPal AI Hackathon 2026

## Scenario: Autonomous Agent Product-Intelligence Acquisition via PayPal

1. **0:00 - 0:25: Problem & Architecture**
   - Introduce **PayMesh AI**: A Trust & Payment Infrastructure for Autonomous AI Commerce.
   - Show how content publishers and data providers can monetize datasets and APIs directly for AI agents via L402 instead of fighting or blocking them.
   - Highlight the Merchant Console and the AI Commerce Agent Workspace.

2. **0:25 - 0:55: Task Submission & Resource Discovery**
   - Buyer enters prompt: *"Compare high-performance mechanical keyboards with ultra-low latency under budget. Budget: $0.10."*
   - Agent invokes `paymesh.discover_resources` tool, queries Channel3 product intelligence, and identifies a curated benchmark dataset.
   - Agent attempts to retrieve full protected report.

3. **0:55 - 1:20: HTTP 402 PayMesh L402 Challenge & Deterministic Policy Check**
   - Server returns HTTP 402 with machine-readable PayMesh L402 challenge.
   - Agent parses offer: $0.05 USD for 1-hour verified access.
   - Deterministic policy engine checks budget ($0.05 <= $0.10 budget limit) and validates offer.
   - Agent presents recommendation and requires buyer confirmation.

4. **1:20 - 1:55: PayPal Sandbox Checkout & Server Capture**
   - Buyer confirms purchase.
   - Server initiates PayPal Sandbox Order with `intent: CAPTURE`.
   - Buyer clicks PayPal Sandbox Checkout button and completes approval.
   - Backend captures the order directly from PayPal API, verifies `COMPLETED` status, and issues a hashed Bearer token (`pm_live_...`).

5. **1:55 - 2:30: Unlocked Data & AI Summary**
   - Agent uses new Bearer token to fetch `/api/v1/resources/product-intelligence-report/content`.
   - Request succeeds (200 OK) with full Channel3 enriched product specs and attribution links.
   - AI synthesizes a concise buying decision table.

6. **2:30 - 2:55: Publisher Analytics & AG Grid**
   - Switch to Publisher Console Financial Ledger.
   - AG Grid displays real-time captured transaction with PayPal Order ID, gross revenue, timestamp, and usage event.
   - Wrap up highlighting PayPal developer ecosystem, MCP standard, Channel3, and AG Grid.
