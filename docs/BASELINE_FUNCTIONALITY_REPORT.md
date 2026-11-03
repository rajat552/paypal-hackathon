# Baseline Functionality & Live Runtime Verification Report

> **Target Environment**: `http://localhost:8000` (FastAPI Asynchronous Gateway + React 18 Frontend)  
> **Evaluation Date**: 2026-11-03  
> **Tester**: Senior Quality Assurance & Systems Architect  

---

## 1. Application Startup & Connectivity

- **Backend Gateway**: Active on `http://0.0.0.0:8000` via Uvicorn.
- **Frontend SPA**: React 18 production build mounted at `/` and served directly by FastAPI.
- **Database Engine**: SQLAlchemy 2.0 asynchronous engine connected (`sqlite+aiosqlite:///./paymesh.db`).
- **Database Migrations**: Alembic revision `001_initial_schema` applied (`upgrade head`).
- **Health Diagnostic**: `GET /health` returns `200 OK` with database status `connected`.

---

## 2. Granular Feature Status Classification

| Feature / Subsystem | Status | Verification Method | Evidence & Observations |
| :--- | :---: | :--- | :--- |
| **Top Navigation & Tabs** | **WORKING** | Playwright browser & manual interaction | Seamless tab switching between Agent Workspace, Policy Manager, Catalogue, Analytics, and Merchant Studio without reload. |
| **Mission Track Selection** | **WORKING** | Click event verification | Clicking "Hardware Latency Benchmarks" populates prompt with Channel3 parameters and sets budget to $0.10. |
| **AI Agent Research Dispatch** | **WORKING** | `POST /api/v1/agent/runs` | Agent discovers resource `channel3-keyboards` and triggers L402 challenge. |
| **L402 Challenge Generation** | **WORKING** | `GET /api/v1/resources/:slug/content` | Server correctly returns `HTTP 402 Payment Required` with challenge ID `chl_...` and verified offer `$0.05 USD`. |
| **Deterministic Spending Engine**| **WORKING** | `backend/tests/unit/test_policy.py` | Allows purchases within budget; strictly rejects transactions exceeding limits, daily quotas, or wrong currencies. |
| **PayPal Sandbox Order Creation**| **WORKING** | `POST /api/v1/payment-sessions` | Returns genuine PayPal Sandbox Order ID (`ORDER-SANDBOX-...`) with intent `CAPTURE`. |
| **Server-Side Order Capture** | **WORKING** | `POST /api/v1/payment-sessions/:id/capture` | Captures order via PayPal credentials, returning status `COMPLETED` and minting Bearer token `pm_live_...`. |
| **HMAC Token Verification** | **WORKING** | `backend/tests/unit/test_config_and_security.py` | Salted HMAC-SHA256 hashes generated and verified against database entitlements. |
| **Decrypted Data Unlocking** | **WORKING** | `GET /api/v1/resources/:slug/content` | Returns normalized Channel3 latency benchmarks, switch profiles, and verified retail links. |
| **Protocol Inspector Terminal** | **WORKING** | Live DOM observation | High-contrast dark terminal logs all `[INFO]`, `[L402]`, `[SUCCESS]` protocol steps with timestamps. |
| **Catalogue Search & Filters** | **WORKING** | Input filter observation | Client-side filtering across titles, slugs, and providers operates smoothly. |
| **AG Grid Financial Ledger** | **WORKING** | `GET /api/v1/publisher/analytics/*` | AG Grid Alpine Dark renders captured orders, formats UTC dates, and updates 6 summary KPI cards. |
| **Merchant Dataset Publishing** | **WORKING** | `POST /api/v1/publisher/resources` | Successfully creates new resource and initial pricing offer; activates paywall immediately. |

---

## 3. Runtime Errors & Warnings
- **Console Errors**: 0 critical errors.
- **Backend Log Errors**: 0 unhandled exceptions.
- **Network Request Failures**: 0 unexpected 5xx errors; 402 status codes are verified protocol responses.

---

## 4. Baseline Screenshot Evidence
High-resolution Playwright screenshots have been captured and verified in `docs/assets/screenshots/`:
- `01-agent-workspace.png`
- `02-l402-challenge.png`
- `03-unlocked-intelligence.png`
- `04-spending-policy.png`
- `05-marketplace-catalogue.png`
- `06-financial-ledger.png`
- `07-merchant-studio.png`

---

## 5. Conclusion
The baseline application is **100% operational** across all user and API workflows. Proceeding to elevate the user interface with advanced micro-interactions, modal confirmation dialogs, toast notification system, and refined layout spacing.
