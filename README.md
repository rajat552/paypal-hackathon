# PayMesh AI

<div align="center">

```text
  ██████╗  █████╗ ██╗   ██╗███╗   ███╗███████╗███████╗██╗  ██╗     █████╗ ██╗
  ██╔══██╗██╔══██╗╚██╗ ██╔╝████╗ ████║██╔════╝██╔════╝██║  ██║    ██╔══██╗██║
  ██████╔╝███████║ ╚████╔╝ ██╔████╔██║█████╗  ███████╗███████║    ███████║██║
  ██╔═══╝ ██╔══██║  ╚██╔╝  ██║╚██╔╝██║██╔══╝  ╚════██║██╔══██║    ██╔══██║██║
  ██║     ██║  ██║   ██║   ██║ ╚═╝ ██║███████╗███████║██║  ██║    ██║  ██║██║
  ╚═╝     ╚═╝  ╚═╝   ╚═╝   ╚═╝     ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝    ╚═╝  ╚═╝╚═╝
```

### A Trust & Payment Infrastructure for Autonomous AI Commerce
**Official Submission for the PayPal AI Hackathon 2026**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.12%20%7C%203.13-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/Frontend-React%2018%20%2B%20Vite-61DAFB.svg?logo=react&logoColor=black)](https://react.dev/)
[![PayPal](https://img.shields.io/badge/PayPal%20Sandbox-Orders%20v2%20%2B%20Webhooks-003087.svg?logo=paypal&logoColor=white)](https://developer.paypal.com)
[![Google Gemini](https://img.shields.io/badge/AI%20Engine-Gemini%202.5%20Flash-8E75C2.svg?logo=google&logoColor=white)](https://ai.google.dev/)
[![MongoDB Atlas](https://img.shields.io/badge/Database-MongoDB%20Atlas%208.0-47A248.svg?logo=mongodb&logoColor=white)](https://www.mongodb.com/atlas)
[![AG Grid](https://img.shields.io/badge/Financial%20Ledger-AG%20Grid%20v32-E0234E.svg?logo=aggrid&logoColor=white)](https://www.ag-grid.com)
[![Protocol](https://img.shields.io/badge/Protocol-L402%20HTTP%20402-F5A623.svg)](https://L402.org)
[![MCP Standard](https://img.shields.io/badge/Standard-Anthropic%20MCP-6366F1.svg)](https://modelcontextprotocol.io/)
[![Tests](https://img.shields.io/badge/Tests-29%20Passed%20%7C%20100%25-10B981.svg)](backend/tests/)

[Live Frontend](https://paypal-hackathon-mu.vercel.app/) • [API Backend Gateway](https://paypal-hackathon-s0gq.onrender.com) • [Interactive Swagger Docs](https://paypal-hackathon-s0gq.onrender.com/docs) • [Architecture](#4-how-it-works) • [Screenshots](#5-screenshots--visual-showcase) • [Quick Start](#9-installation--setup) • [Testing](#16-testing--verification)

</div>

---

## 1. Overview

### The Problem
Autonomous AI agents are shifting from passive conversational assistants into independent workers that gather real-time market data, procure pay-per-call APIs, and synthesize commercial intelligence. However, modern financial rails were built exclusively for humans:

1. **The Human-in-the-Loop Barrier**: Traditional checkouts demand browser session cookies, CAPTCHAs, redirect chains, and SMS 3D-Secure prompts that break programmatic machine execution.
2. **Critical Financial Security Risks**: Providing an LLM with unrestricted payment authority or static API keys creates severe vulnerabilities:
   - **Prompt Injection**: Malicious publisher payloads can trick the model into executing unauthorized purchases.
   - **Runaway Agent Loops**: Recursive orchestration errors can rapidly drain accounts.
   - **Credential Leakage**: Shared API keys passed into agent prompts are susceptible to context window leakage.
3. **The Data Provider Dilemma**: API publishers face web scrapers consuming compute without compensation, yet lack a lightweight, standardized micropayment protocol for legitimate AI agents.

### The Solution: PayMesh AI
**PayMesh AI** is an open-source trust and payment mesh connecting autonomous AI agents with paywalled datasets and APIs. Powered by the open **L402 protocol** and **PayPal Developer Sandbox (Orders v2 & Webhooks)**, PayMesh AI separates financial authorization from probabilistic model reasoning:

- **Standardized Machine-Readable Paywalls**: Returns authoritative `HTTP 402 Payment Required` envelopes with verified pricing offers and challenge IDs.
- **Deterministic Server-Enforced Spending Policies**: Hard per-transaction spending limits ($0.50 default) and 24-hour daily rolling caps ($5.00 default) are verified on the server before any payment order is generated. The AI model has zero authority to alter prices or initiate charges.
- **Genuine PayPal Orders v2 Settlement**: Complete OAuth 2.0 client credential acquisition, server-calculated purchase units, dual-mode approval (standard PayPal Sandbox account or instant test capture for evaluators), and server-side capture verification.
- **Cryptographic Token Isolation**: Challenge tokens, PayPal Order IDs, and Bearer access keys (`pm_live_...`) are strictly isolated. Tokens are saved exclusively as salted HMAC-SHA256 hashes.
- **Dual Persistence Architecture**: SQLAlchemy Async Engine (SQLite/PostgreSQL) for relational state paired with MongoDB Atlas (`cohesora` cluster) for immutable cloud audit logging.
- **Anthropic Model Context Protocol (MCP)**: Native server manifest at `/api/v1/agent/mcp/manifest` allowing Claude Desktop and MCP-compatible agents to discover, negotiate, and unlock datasets programmatically.

---

## 2. Live Deployments

| Component | Platform | URL | Status | Description |
| :--- | :--- | :--- | :--- | :--- |
| **Frontend** | Vercel (Edge CDN) | [paypal-hackathon-mu.vercel.app](https://paypal-hackathon-mu.vercel.app/) | Active | React 18 SPA with Neo-Brutalist design, mobile navigation, and guided tour |
| **API Backend** | Render Cloud | [paypal-hackathon-s0gq.onrender.com](https://paypal-hackathon-s0gq.onrender.com) | Active | FastAPI asynchronous gateway enforcing L402 challenges and PayPal capture |
| **System Health** | Render `/health` | [paypal-hackathon-s0gq.onrender.com/health](https://paypal-hackathon-s0gq.onrender.com/health) | 200 OK | Health diagnostic endpoint verifying database and MongoDB Atlas connectivity |
| **Swagger UI** | Render `/docs` | [paypal-hackathon-s0gq.onrender.com/docs](https://paypal-hackathon-s0gq.onrender.com/docs) | Active | Interactive OpenAPI 3.1 documentation for all 15 REST and agent endpoints |
| **MCP Server Manifest** | Render | [paypal-hackathon-s0gq.onrender.com/api/v1/agent/mcp/manifest](https://paypal-hackathon-s0gq.onrender.com/api/v1/agent/mcp/manifest) | Active | Machine-readable Anthropic Model Context Protocol catalog manifest |
| **PayPal Webhook** | PayPal Developer Portal | `https://paypal-hackathon-s0gq.onrender.com/api/v1/payments/webhook` | Registered | Webhook listener handling `PAYMENT.CAPTURE.COMPLETED` events |

---

## 3. Key Features

- **L402 HTTP 402 Paywall Protocol**: Standardized negotiation protocol returning machine-readable JSON envelopes containing offer details, expiration windows, and payment challenge tokens.
- **Deterministic Spending Guardrails**: Immutable server-side validation enforcing hard ceilings per transaction, 24-hour rolling quotas, and strict currency matching before any PayPal order is created.
- **PayPal Orders v2 Capture Flow**: Full server-side lifecycle using official PayPal REST APIs. Supports both standard Sandbox Buyer Account approval and an instant one-click test approval mode for evaluators without sandbox logins.
- **Asynchronous PayPal Webhook Processing**: Dedicated endpoint validating incoming webhook notifications, updating transaction states, and persisting immutable capture events in MongoDB Atlas.
- **Multi-Model AI Integration**: Powered by Google Gemini 2.5 Flash (`AI_PROVIDER=gemini`) for intent parsing and product synthesis, with support for OpenAI and Claude, as well as a zero-key deterministic procurement fallback.
- **Dual Persistence Architecture**: High-speed relational storage (SQLite locally, PostgreSQL in production) for resources, offers, and entitlements, paired with MongoDB Atlas cloud for audit trails.
- **Enterprise AG Grid Financial Ledger**: Real-time KPI cards (volume, order count, conversion rate, active tokens) and an interactive financial settlement ledger with sorting, filtering, and CSV export.
- **Self-Service Merchant Studio**: Publisher console for external data providers to register APIs, define custom pricing tiers ($0.01 - $0.50), and generate instant L402 paywalls.
- **15-Step Guided Onboarding Tour**: Integrated SVG spotlight walkthrough introducing users to the autonomous AI commerce lifecycle.
- **Custom Neo-Brutalist 404 Route Resolver**: Dedicated route error handling with protocol diagnostic traces, responsive layout, and history-aware fallback navigation.
- **Cross-Device Responsiveness**: Verified across 10 distinct viewports from 320px small mobile to 1920px widescreen desktop.

---

## 4. How It Works

### The Autonomous Commerce Lifecycle

```
[ User Request ]
       │ "Compare mechanical keyboard switch latencies under $0.10"
       ▼
[ AI Commerce Agent ] ───▶ Discovers /api/v1/catalogue
       │
       ▼
[ PayMesh L402 Gateway ] ───▶ Returns HTTP 402 + Challenge Token ($0.05 USD)
       │
       ▼
[ Deterministic Spending Engine ] ───▶ Verifies Price <= $0.10 & Daily Budget Intact
       │
       ▼
[ PayPal Sandbox Orders v2 ] ───▶ Creates Order & Verifies Server-Side Capture
       │
       ▼
[ Scoped Bearer Token ] ───▶ Hashed (HMAC-SHA256) & Returned to Agent
       │
       ▼
[ Unlocked Dataset ] ───▶ Decrypted Hardware Benchmarks + MongoDB Audit Record
```

### Complete Sequence Diagram

```mermaid
sequenceDiagram
    autonumber
    actor User as User / Supervisor
    participant Agent as AI Commerce Agent
    participant Gateway as PayMesh Gateway (FastAPI)
    participant Policy as Deterministic Spending Engine
    participant PayPal as PayPal Sandbox (Orders v2)
    participant Mongo as MongoDB Atlas (Audit Cloud)
    participant Provider as Protected API / Channel3

    User->>Agent: Submit research task with spending limit ($0.10 USD)
    Agent->>Gateway: GET /api/v1/catalogue (Discover resources)
    Gateway-->>Agent: Returns catalog with verified offer IDs
    
    Agent->>Gateway: GET /api/v1/resources/channel3-keyboards/content
    Gateway-->>Agent: HTTP 402 Payment Required (L402 Challenge Token)
    
    Agent->>Policy: Evaluate Challenge ($0.05 USD vs Budget $0.10 USD)
    Policy-->>Agent: Policy Approved (Price <= Ceiling, Daily Cap Intact)
    
    Agent->>Gateway: POST /api/v1/payment-sessions (Initiate Checkout)
    Gateway->>PayPal: POST /v2/checkout/orders (intent: CAPTURE)
    PayPal-->>Gateway: Order Created (ID: 2M942495GD6205744)
    Gateway-->>Agent: Returns session_id + PayPal approval details
    
    User->>Agent: Authorizes PayPal Sandbox payment
    Agent->>Gateway: POST /api/v1/payment-sessions/{id}/capture
    Gateway->>PayPal: POST /v2/checkout/orders/{id}/capture
    PayPal-->>Gateway: Capture COMPLETED (Capture ID: CAP-...)
    
    Gateway->>Mongo: Insert Audit Record (PAYPAL_CAPTURE_SUCCESS)
    Gateway->>Gateway: Mint Bearer Token (pm_live_...) & Store HMAC Hash
    Gateway-->>Agent: Returns Scoped Bearer Access Token
    
    Agent->>Gateway: GET /api/v1/resources/channel3-keyboards/content (Authorization: Bearer pm_live_...)
    Gateway->>Provider: Fetch Protected Intelligence Dataset
    Provider-->>Gateway: Benchmark Payload
    Gateway-->>Agent: HTTP 200 OK + Unlocked Data
    Agent-->>User: Structured Comparison & Direct Retail Links
```

---

## 5. Screenshots & Visual Showcase

### 1. AI Commerce Agent Studio & Live Protocol Inspector
Mission control where users enter autonomous research goals, set deterministic spending caps, dispatch multi-step agent runs, and inspect live L402 and MCP protocol frames.

![AI Commerce Agent Workspace](assets/screenshots/01-agent-workspace.png)

---

### 2. Machine-Readable L402 Challenge & PayPal Gateway Action
When an agent attempts to access protected endpoints without an entitlement, PayMesh AI issues an authoritative `HTTP 402 Payment Required` challenge. The agent's spending engine validates the pricing offer and initiates PayPal Sandbox checkout.

![L402 Challenge and PayPal Gateway](assets/screenshots/02-l402-challenge.png)

---

### 3. Decrypted Intelligence & Channel3 Product Data
Upon verified PayPal capture, a cryptographic Bearer token (`pm_live_...`) is minted, unlocking normalized Channel3 hardware latency benchmarks with verified retailer purchase links.

![Unlocked Channel3 Hardware Intelligence](assets/screenshots/03-unlocked-intelligence.png)

---

### 4. Deterministic Trust & Spending Policy Engine
Server-enforced guardrails that prevent probabilistic LLMs from runaway spending or falling victim to prompt-injection exploits.

![Deterministic Policy Manager](assets/screenshots/04-spending-policy.png)

---

### 5. API & Data Marketplace Catalogue
A machine-readable registry where data providers list intelligence feeds, benchmark datasets, and pricing tiers for programmatic discovery.

![API and Data Catalogue](assets/screenshots/05-marketplace-catalogue.png)

---

### 6. AG Grid Financial Settlement Ledger & KPI Analytics
Financial analytics tracking total capture volume, active entitlements, conversion rates, and immutable PayPal capture IDs with CSV export.

![AG Grid Financial Ledger](assets/screenshots/06-financial-ledger.png)

---

### 7. Merchant Publishing Studio
Self-service console enabling developers to publish datasets, configure custom micro-pricing tiers, and generate instant L402 paywalls.

![Merchant Studio](assets/screenshots/07-merchant-studio.png)

---

### 8. Interactive 15-Step Guided Onboarding Tour
High-contrast guided tour with SVG spotlight masking and tab-aware automatic navigation.

![Interactive Onboarding Tour](assets/screenshots/tour/00_url_click_tour_first.png)

---

### 9. Custom Neo-Brutalist 404 Route Resolver
Dedicated route error handling with protocol diagnostic traces, responsive layout, and history-aware fallback navigation.

![Custom 404 Page](assets/screenshots/404/01_404_desktop.png)

---

## 6. Technology Stack

| Layer | Technology | Purpose | Codebase Reference |
| :--- | :--- | :--- | :--- |
| **Backend Framework** | Python 3.11+ / FastAPI | Asynchronous REST gateway, L402 paywall middleware, and business logic | [`backend/app/main.py`](backend/app/main.py) |
| **Payment Gateway** | PayPal Orders v2 REST API | Sandbox payment creation, capture verification, and webhook notifications | [`backend/app/services/paypal_gateway.py`](backend/app/services/paypal_gateway.py) |
| **AI Inference** | Google Gemini 2.5 Flash | Autonomous intent parsing, tool execution, and product synthesis | [`backend/app/agent/llm_client.py`](backend/app/agent/llm_client.py) |
| **Audit Database** | MongoDB Atlas Cloud 8.0 | Multi-cloud immutable event repository (`auditevents` collection) with TLS verification | [`backend/app/db/mongodb.py`](backend/app/db/mongodb.py) |
| **Relational Database** | SQLAlchemy 2.0 (Async) | Manages resources, offers, challenges, payment sessions, and entitlements | [`backend/app/models/entities.py`](backend/app/models/entities.py) |
| **Schema Validation** | Pydantic v2 | Strict request/response validation and environment configuration parsing | [`backend/app/schemas/`](backend/app/schemas/) |
| **Frontend Framework** | React 18 + TypeScript + Vite | Client-side single-page application with hash-based routing and state persistence | [`frontend/src/`](frontend/src/) |
| **Styling & Design System** | Tailwind CSS (Neo-Brutalist) | Engineering blueprint grid, offset block shadows (`shadow-neo`), Space Grotesk fonts | [`frontend/tailwind.config.js`](frontend/tailwind.config.js) |
| **Financial Table** | AG Grid Community v32 | Financial ledger with multi-column sorting, filtering, and CSV export | [`frontend/src/components/AnalyticsView.tsx`](frontend/src/components/AnalyticsView.tsx) |
| **Agent Protocol** | Anthropic Model Context Protocol | Open tool integration standard exposed at `/api/v1/agent/mcp/manifest` | [`backend/app/mcp/server.py`](backend/app/mcp/server.py) |
| **External Integration** | Channel3 API Client | Hardware latency benchmarks and verified retailer purchase links | [`backend/app/services/channel3_client.py`](backend/app/services/channel3_client.py) |
| **Testing** | Pytest + Playwright | 29 automated backend tests and browser-based cross-device verification | [`backend/tests/`](backend/tests/) |

---

## 7. Architecture & Project Structure

```text
paypal-hackathon/
├── backend/                        # FastAPI asynchronous application
│   ├── app/
│   │   ├── agent/                  # AI agent orchestration, tools, and spending policy
│   │   │   ├── llm_client.py       # Google Gemini, OpenAI & Claude multi-model client
│   │   │   ├── orchestrator.py     # Multi-step discovery, challenge, and capture engine
│   │   │   ├── policy.py           # Deterministic spending limit guardrails
│   │   │   └── tools.py            # Agent tool definitions (catalogue, challenge, payment)
│   │   ├── api/v1/routes/          # REST API endpoints (Catalogue, Payments, MCP, Publisher, Webhook)
│   │   ├── core/                   # Application config, security, logging, exceptions
│   │   ├── db/                     # SQLAlchemy async engine, models, and MongoDB Atlas client
│   │   │   ├── mongodb.py          # MongoDB Atlas TLS connection & audit logger
│   │   │   └── session.py          # Async SQLAlchemy engine & table lifecycle initialization
│   │   ├── mcp/                    # Anthropic Model Context Protocol (MCP) server
│   │   ├── models/                 # Database entity models (Resource, Offer, Entitlement, etc.)
│   │   ├── schemas/                # Pydantic v2 validation models
│   │   ├── services/               # PayPal Orders v2 gateway, L402 challenge service, Channel3
│   │   └── main.py                 # FastAPI application root, lifespan, and CORS middleware
│   ├── tests/                      # Automated unit and integration test suite (29 passing tests)
│   │   ├── conftest.py             # Asynchronous test client and database fixtures
│   │   ├── integration/            # API, L402, PayPal, Webhook, and MCP integration tests
│   │   └── unit/                   # Policy engine, token hashing, and config unit tests
│   ├── Dockerfile                  # Production container definition
│   └── requirements.txt            # Python dependencies
├── frontend/                       # React 18 + Tailwind CSS + AG Grid application
│   ├── src/
│   │   ├── components/             # AgentWorkspace, PolicyManager, CatalogueView, AnalyticsView, etc.
│   │   │   ├── AgentWorkspace.tsx  # Interactive agent prompt submission & L402 challenge cards
│   │   │   ├── AnalyticsView.tsx   # AG Grid settlement ledger & financial KPIs
│   │   │   ├── CatalogueView.tsx   # Marketplace data product registry & search filters
│   │   │   ├── Navbar.tsx          # Dual-mode responsive navigation & mobile drawer
│   │   │   ├── NotFound.tsx        # Custom Neo-Brutalist 404 page with route diagnostics
│   │   │   ├── OnboardingTour.tsx  # 15-step interactive guided spotlight walkthrough
│   │   │   ├── PolicyManager.tsx   # Spending guardrails & 24h budget utilization gauge
│   │   │   └── PublisherConsole.tsx# Merchant studio for dataset monetization
│   │   ├── App.tsx                 # Main layout, routing resolver, and footer
│   │   ├── index.css               # Base styles, blueprint grid, and neo-tech utility classes
│   │   └── main.tsx                # React DOM entry point
│   ├── package.json                # Frontend package dependencies
│   ├── tailwind.config.js          # Neo-brutalist shadow tokens, palette, and fonts
│   ├── vercel.json                 # Vercel proxy rewrite configuration
│   └── vite.config.ts              # Vite dev server configuration and backend proxy
├── assets/screenshots/             # Authentic UI screenshots and responsive captures
├── scripts/                        # Automated verification tools
│   ├── audit_responsiveness.py     # Automated audit across 10 viewports and 5 modules
│   ├── smoke_test.py               # 7-step end-to-end integration smoke test
│   ├── verify_404.py               # Automated 404 route handling & fallback verification
│   ├── verify_cross_device.py      # Cross-device interaction & modal verification
│   └── verify_tour.py              # Automated 15-step onboarding tour verification
├── .env.example                    # Clean environment configuration template
├── docker-compose.yml              # Local multi-container development environment
├── render.yaml                     # Render cloud Blueprint configuration
└── vercel.json                     # Root Vercel deployment configuration
```

---

## 8. Prerequisites

- **Python**: Version `3.11`, `3.12`, or `3.13`.
- **Node.js**: Version `18.x` or higher (`npm 9+`).
- **PayPal Developer Account**: Sandbox Client ID and Secret from the [PayPal Developer Dashboard](https://developer.paypal.com).
- *(Optional)* **Google Gemini API Key**: For live LLM reasoning (falls back to deterministic heuristics if omitted).
- *(Optional)* **MongoDB Atlas URI**: For persistent cloud audit logging (uses relational database records if omitted).

---

## 9. Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/rajat552/paypal-hackathon.git
cd paypal-hackathon
```

### 2. Configure Environment Variables
Copy `.env.example` to `.env` and insert your credentials:
```bash
cp .env.example .env
```

### 3. Set Up Python Virtual Environment & Backend Dependencies
```bash
python -m venv .venv

# On Linux/macOS:
source .venv/bin/activate

# On Windows (PowerShell):
.\.venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

### 4. Install Frontend Dependencies
```bash
npm --prefix frontend install
```

### 5. Build Frontend (Production Bundle)
```bash
npm --prefix frontend run build
```

---

## 10. Environment Variables

| Variable Name | Purpose | Required | Safe Placeholder Example |
| :--- | :--- | :---: | :--- |
| `APP_ENV` | Application runtime environment (`development`, `production`) | No | `development` |
| `APP_BASE_URL` | Base URL of the backend API gateway | Yes | `http://127.0.0.1:8000` |
| `FRONTEND_URL` | Allowed origin for frontend CORS | Yes | `http://localhost:3000` |
| `SECRET_KEY` | HMAC secret key for hashing Bearer tokens and challenges | Yes | `min-32-chars-cryptographic-secret-key` |
| `DATABASE_URL` | SQLAlchemy relational database connection URL | Yes | `sqlite+aiosqlite:///./paymesh.db` |
| `PAYPAL_ENVIRONMENT` | PayPal operating environment (`sandbox` or `production`) | Yes | `sandbox` |
| `PAYPAL_CLIENT_ID` | PayPal REST API client identifier | Yes | `your-sandbox-client-id` |
| `PAYPAL_CLIENT_SECRET` | PayPal REST API client secret | Yes | `your-sandbox-client-secret` |
| `PAYPAL_WEBHOOK_ID` | Registered PayPal Webhook ID for signature verification | No | `optional-webhook-id` |
| `AI_PROVIDER` | Active LLM inference provider (`gemini`, `openai`, `anthropic`) | No | `gemini` |
| `AI_API_KEY` | API key for the chosen LLM provider | No | `optional-ai-api-key` |
| `AI_MODEL` | Model identifier string | No | `gemini-2.5-flash` |
| `MONGODB_URI` | MongoDB Atlas TLS connection string for audit logging | No | `mongodb+srv://user:pass@cluster.mongodb.net/dbname` |
| `CHANNEL3_API_KEY` | Channel3 Product Intelligence API key | No | `optional-channel3-key` |

---

## 11. Running the Application

### Option A: Run Backend and Frontend Simultaneously (Recommended for Development)

In **Terminal 1** (Backend):
```bash
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```

In **Terminal 2** (Frontend Dev Server):
```bash
npm --prefix frontend run dev
```

- **Frontend Application**: `http://localhost:3000`
- **Backend API Gateway**: `http://127.0.0.1:8000`
- **Interactive Swagger Documentation**: `http://127.0.0.1:8000/docs`
- **Health Check Endpoint**: `http://127.0.0.1:8000/health`

### Option B: Unified Production Server (FastAPI Serves Static Frontend)
After building the frontend via `npm --prefix frontend run build`, run:
```bash
python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
```
Navigate to `http://localhost:8000` to access the combined interface.

---

## 12. PayPal Sandbox Configuration

PayMesh AI connects directly to the official **PayPal Sandbox Orders v2 API**:

1. **Create a PayPal Developer Account**: Sign up at [developer.paypal.com](https://developer.paypal.com).
2. **Create a Sandbox REST App**:
   - Navigate to **Dashboard &rarr; Apps &amp; Credentials**.
   - Create an app under **Sandbox**.
   - Copy the generated `Client ID` and `Secret Key` into `.env` as `PAYPAL_CLIENT_ID` and `PAYPAL_CLIENT_SECRET`.
3. **Buyer Testing Credentials**:
   - In **Sandbox &rarr; Accounts**, note the pre-created Personal Buyer account credentials (`sb-buyer...@personal.example.com`).
4. **Approval & Capture Workflows**:
   - **Option 1 (Sandbox Buyer Login)**: Click **Sign In at PayPal Sandbox** to log in with sandbox buyer credentials and grant authorization.
   - **Option 2 (Instant Test Approval)**: Click **Instant Sandbox Test Approval** for immediate simulation of buyer approval directly through the server-side Orders v2 test flow (no login required for hackathon judges).
   - Once approved, the backend executes `POST /v2/checkout/orders/{id}/capture` to complete settlement and mint a Bearer access token.

> [!NOTE]
> All transactions are processed in the PayPal Sandbox test environment. No real funds or live credit cards are charged.

---

## 13. AI Configuration & Multi-Model Engine

PayMesh AI supports dynamic AI model inference for intent analysis and product synthesis:

- **Google Gemini 2.5 Flash (Primary)**:
  - Set `AI_PROVIDER=gemini`, `AI_MODEL=gemini-2.5-flash`, and provide your `AI_API_KEY`.
  - Used for intent extraction, benchmark comparisons, and structured market synthesis.
- **OpenAI & Claude Support**:
  - Set `AI_PROVIDER=openai` (e.g., `gpt-4o-mini`) or `AI_PROVIDER=anthropic` with the corresponding `AI_API_KEY`.
- **Deterministic Fallback (Zero-Key Execution)**:
  - If no `AI_API_KEY` is configured, PayMesh AI automatically runs in deterministic rule-based mode. The system executes catalogue discovery, evaluates spending limits, negotiates L402 paywalls, and processes PayPal Sandbox orders without requiring external AI credentials.

---

## 14. API Documentation

Complete interactive documentation with request/response schemas is available at `http://localhost:8000/docs` (or live at `https://paypal-hackathon-s0gq.onrender.com/docs`).

### Primary API Endpoints

| Method | Endpoint | Description | Auth Required |
| :---: | :--- | :--- | :---: |
| `GET` | `/health` | Real-time health diagnostic, database status, and MongoDB check | Public |
| `GET` | `/api/v1/catalogue` | Discover verified intelligence datasets, providers, and pricing offers | Public |
| `GET` | `/api/v1/resources/{slug}/content` | Retrieve protected content (returns `HTTP 402` without valid token) | Bearer Token |
| `POST` | `/api/v1/payment-sessions` | Create a PayPal Sandbox Orders v2 checkout session | Public |
| `POST` | `/api/v1/payment-sessions/{id}/capture` | Server-side capture and verification of an approved PayPal order | Public |
| `POST` | `/api/v1/payment-sessions/{id}/simulate-approval` | Simulate Sandbox buyer authorization for rapid evaluation | Public |
| `POST` | `/api/v1/payments/webhook` | Handle asynchronous PayPal webhook events (`PAYMENT.CAPTURE.COMPLETED`) | Public |
| `POST` | `/api/v1/agent/runs` | Multi-step agent orchestrator (discovery, challenge, and policy check) | Public |
| `GET` | `/api/v1/agent/policy/config` | Read current server-side spending guardrails and 24h budget metrics | Public |
| `PUT` | `/api/v1/agent/policy/config` | Update per-transaction limits, daily budgets, and security flags | Public |
| `GET` | `/api/v1/agent/mcp/manifest` | Anthropic Model Context Protocol (MCP) server manifest | Public |
| `POST` | `/api/v1/agent/mcp/tools/{tool_name}` | Execute MCP tools programmatically via standard JSON-RPC | Public |
| `POST` | `/api/v1/publisher/resources` | Register a new dataset product in the marketplace | Public |
| `POST` | `/api/v1/publisher/resources/{id}/offers` | Create custom pricing tiers and access durations | Public |
| `GET` | `/api/v1/publisher/analytics/summary` | Real-time financial KPI metrics (volume, order count, conversion) | Public |
| `GET` | `/api/v1/publisher/analytics/transactions` | Full settlement ledger of all captured PayPal transactions | Public |

---

## 15. Database & Data Storage

PayMesh AI utilizes a dual-database architecture:

1. **Transactional Relational Database (SQLAlchemy 2.0 Async Engine)**:
   - Default: `sqlite+aiosqlite:///./paymesh.db` (local development).
   - Production: PostgreSQL (Render Managed PostgreSQL).
   - **Core Entities**:
     - `Resource`: Monetized datasets and API endpoints (`slug`, `provider`, `resource_type`).
     - `Offer`: Pricing rules, currency, amounts ($0.01 - $0.50), and access durations.
     - `Challenge`: Authoritative L402 challenge tokens with 10-minute expiration.
     - `PaymentSession`: Tracks PayPal Order IDs, capture IDs, session state, and timestamps.
     - `Entitlement`: Issued access grants mapped to salted HMAC-SHA256 token hashes.
2. **Cloud Audit Ledger (MongoDB Atlas)**:
   - Dedicated `auditevents` collection on MongoDB Atlas (`cohesora` cluster).
   - Stores immutable audit events (`PAYPAL_CAPTURE_SUCCESS`, `ENTITLEMENT_ISSUED`, `WEBHOOK_RECEIVED`) with TLS certificate verification via `certifi`.

---

## 16. Testing & Verification

PayMesh AI includes an automated testing suite with **29 passing unit and integration tests**:

```bash
python -m pytest backend/tests/ -v
```

### Verified Test Results
```text
backend/tests/integration/test_api_endpoints.py::test_health_endpoint PASSED              [  3%]
backend/tests/integration/test_api_endpoints.py::test_catalogue_endpoint PASSED           [  6%]
backend/tests/integration/test_api_endpoints.py::test_protected_resource_returns_402_challenge PASSED [ 10%]
backend/tests/integration/test_api_endpoints.py::test_full_payment_capture_and_retrieval_flow PASSED [ 13%]
backend/tests/integration/test_api_endpoints.py::test_simulate_buyer_approval_instant_capture PASSED [ 17%]
backend/tests/integration/test_api_endpoints.py::test_agent_run_orchestration PASSED      [ 20%]
backend/tests/integration/test_api_endpoints.py::test_mcp_manifest_and_tool_execution PASSED [ 24%]
backend/tests/integration/test_api_endpoints.py::test_legacy_bot_l402_and_payment_flow PASSED [ 27%]
backend/tests/integration/test_api_endpoints.py::test_security_headers_enforced PASSED   [ 31%]
backend/tests/integration/test_api_endpoints.py::test_publisher_validation_rejects_invalid_currency PASSED [ 34%]
backend/tests/integration/test_api_endpoints.py::test_agent_orchestration_returns_ai_metadata PASSED [ 37%]
backend/tests/integration/test_api_endpoints.py::test_paypal_webhook_handler PASSED      [ 41%]
backend/tests/integration/test_api_endpoints.py::test_policy_config_get_and_update PASSED [ 44%]
backend/tests/unit/test_ai_agent.py::test_discover_resources_args_validation PASSED       [ 48%]
backend/tests/unit/test_ai_agent.py::test_get_resource_offer_args_validation PASSED       [ 51%]
backend/tests/unit/test_ai_agent.py::test_evaluate_purchase_policy_args_validation PASSED [ 55%]
backend/tests/unit/test_ai_agent.py::test_llm_client_unconfigured_by_default PASSED      [ 58%]
backend/tests/unit/test_ai_agent.py::test_llm_client_execute_unknown_tool PASSED         [ 62%]
backend/tests/unit/test_ai_agent.py::test_orchestrator_returns_structured_trace PASSED   [ 65%]
backend/tests/unit/test_config_and_security.py::test_settings_properties PASSED          [ 68%]
backend/tests/unit/test_config_and_security.py::test_token_hashing_and_verification PASSED [ 72%]
backend/tests/unit/test_config_and_security.py::test_challenge_id_format PASSED          [ 75%]
backend/tests/unit/test_config_and_security.py::test_password_hashing PASSED             [ 79%]
backend/tests/unit/test_policy.py::test_policy_within_budget PASSED                       [ 82%]
backend/tests/unit/test_policy.py::test_policy_exceeds_budget PASSED                      [ 86%]
backend/tests/unit/test_policy.py::test_policy_currency_mismatch PASSED                   [ 89%]
backend/tests/unit/test_policy.py::test_policy_inactive_offer PASSED                      [ 93%]
backend/tests/unit/test_policy.py::test_policy_disallowed_currency PASSED                 [ 96%]
backend/tests/unit/test_policy.py::test_policy_exceeds_platform_ceiling PASSED            [100%]

============================= 29 passed in 19.93s =============================
```

### Additional Verification Scripts

- **Frontend Compilation & Type Check**:
  ```bash
  npm --prefix frontend run build
  ```
- **Cross-Device & Responsive Verification**:
  ```bash
  python scripts/verify_cross_device.py
  ```
- **404 Route Handling & Fallback Verification**:
  ```bash
  python scripts/verify_404.py
  ```
- **Live Deployment Smoke Test**:
  ```bash
  python scripts/smoke_test.py https://paypal-hackathon-s0gq.onrender.com
  ```

---

## 17. Deployment Architecture

- **Backend (Render Web Service)**:
  - Configuration: Defined in [`render.yaml`](render.yaml).
  - Runtime: Python 3 with Uvicorn worker process.
  - Health check path: `/health`.
  - Start command: `python -m uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT`.
- **Frontend (Vercel Edge Network)**:
  - Configuration: Defined in [`vercel.json`](vercel.json).
  - Build command: `cd frontend && npm install && npm run build`.
  - Output directory: `frontend/dist`.
  - Rewrites `/api/:path*`, `/health`, and `/docs` to the Render gateway while routing SPA routes to `index.html`.

---

## 18. Security & Trust Invariants

1. **Zero-Hallucination Price Enforcement**: Pricing amounts are retrieved directly from the verified database offer record. The AI model has no capability to modify purchase unit amounts.
2. **Server-Side PayPal Verification**: Access tokens are minted only after the server verifies that `status == "COMPLETED"` from the PayPal Orders v2 capture API.
3. **Cryptographic HMAC-SHA256 Token Storage**: Bearer tokens are generated via `secrets.token_urlsafe(32)`. Only the salted HMAC-SHA256 hash is persisted; plaintext tokens are never stored.
4. **Strict Scope Binding**: Issued Bearer tokens are cryptographically bound to specific resource IDs and expire automatically after the allotted duration.
5. **Prompt-Injection Defense**: External payload attributes from marketplace providers are sanitized and validated against Pydantic schemas before being passed to LLM contexts.
6. **Hardened HTTP Response Headers**: All responses include `X-Content-Type-Options: nosniff`, `X-Frame-Options: SAMEORIGIN`, and strict referrer policies.

---

## 19. Known Limitations

- **PayPal Sandbox Only**: All payments are executed in the PayPal Sandbox environment and do not process real funds.
- **Micro-Payment Aggregation**: Transactions under $0.05 are demonstrated individually within Sandbox bounds; production micro-cent transactions would utilize batch settlement in live deployments.
- **External AI Providers**: Live LLM reasoning requires an active Google Gemini, OpenAI, or Anthropic API key; in the absence of an API key, the platform falls back to deterministic procurement heuristics.

---

## 20. License & Attributions

This project is open-source software licensed under the **[MIT License](LICENSE)**.

### Acknowledgements & Integrations
- **PayPal Developer Platform**: For PayPal Orders v2 Sandbox APIs and Webhook event infrastructure.
- **Google DeepMind / Gemini**: For `gemini-2.5-flash` powering autonomous intent interpretation and intelligence synthesis.
- **MongoDB Atlas**: For multi-cloud document storage and immutable audit logging.
- **AG Grid**: For enterprise financial data tables and analytics ledger.
- **Channel3**: For verified hardware latency benchmarks and retail product links.
- **Anthropic**: For the open Model Context Protocol (MCP) standard.
