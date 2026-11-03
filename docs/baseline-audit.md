# Baseline Audit: CrawlerPal 1.0 to CrawlerPal 2.0

## 1. Repository Forensics
- **Repository Baseline Commit SHA**: `2fa9b4a`
- **Origin Remote**: `https://github.com/rajat552/paypal-hackathon.git`
- **Upstream Reference**: `https://github.com/positiveblue/CrawlerPal.git`
- **Audit Date**: 2 November 2026

## 2. Tracked Files Inventory
- `server/main.py` (410 lines): Monolithic FastAPI application containing Faker news generator, HTML browser rendering, User-Agent bot detection, L402 402 response, and PayPal Orders v2 create endpoint.
- `client/main.py` (172 lines): Python CLI script using `requests` to test unauthenticated GET, 402 negotiation, POST payment, and authenticated GET with Bearer token.
- `requirements.txt`: Declared `fastapi`, `uvicorn[standard]`, `httpx`, `Faker`, `requests`. Missing `python-dotenv`, `sqlalchemy`, `alembic`, etc.
- `server/payments_db.json`: File-based JSON payment ledger.
- `landing.png`, `paypal-payments.jpg`: UI and terminal flow screenshots.
- `README.md`: Basic description of the legacy news-feed paywall.

## 3. Discovered Defects and Architectural Blockers
1. **Direct Access Token Import Dependency**: `server/main.py` requires `PAYPAL_ACCESS_TOKEN` in `.env` at startup. If missing, the app crashes. In reality, PayPal access tokens expire in 9 hours and must be dynamically fetched using Client ID + Secret via OAuth 2.0.
2. **Hardcoded Localhost in 402 Response**: The payment URL was hardcoded to `http://localhost:8000/l402/payment-request`. Remote agents or cloud deployments fail.
3. **Hardcoded Vault ID & Customer ID**: In `server/main.py`, the PayPal payload specifies a static `vault_id: 7m164080c5885500e` and `customer.id: jQBrFyQJTq`, which breaks general buyer checkouts.
4. **Order Create Conflated with Capture**: Legacy code calls Orders v2 Create and immediately checks `paypal_response_data.get('status') == 'COMPLETED'`. Orders v2 Create returns `CREATED`, requiring buyer approval, then capture.
5. **No Challenge Persistence**: `payment_context_token` was randomly generated on 402 but never persisted in a challenge database table.
6. **Token Reuse as Bearer Token**: The `payment_context_token` UUID was reused directly as the access token, exposing session identifiers.
7. **JSON File & Memory Store**: State stored in global dictionary and mirrored to `payments_db.json`, causing race conditions and lack of transactional guarantees.
8. **Insecure Authorization via User-Agent**: Routing relied on `is_browser(user_agent)`, which is trivially spoofable.
9. **Missing AI Agent & MCP**: No AI model orchestration, tool calling, or MCP endpoints existed.
10. **Hardcoded Pricing vs Brief Discrepancy**: Legacy used `$0.01` and `$0.05` while documentation mentioned `$1` and `$5`. Prices must be decimal database-driven entities.

## 4. Licensing and Attribution Decision
The legacy repository lacked an explicit `LICENSE` file. To ensure compliance with PayPal AI Hackathon rules:
- Codebase will be architected with clean, original, modular design.
- Reusable concepts from the original CrawlerPal proof-of-concept are acknowledged.
- An official MIT License is placed at repository root covering original implementation code.
