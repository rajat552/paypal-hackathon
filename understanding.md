# PayMesh AI — Complete Technical Architecture & System Documentation

> **Document Version:** 2.1.0  
> **Last Verified:** November 2026  
> **Project:** PayMesh AI — Trust & Payment Infrastructure for Autonomous AI Commerce  
> **Hackathon Track:** PayPal AI Hackathon 2026  
> **Live Deployments:**  
> - **Frontend (Vercel):** [https://paypal-hackathon-mu.vercel.app/](https://paypal-hackathon-mu.vercel.app/)  
> - **Backend API (Render):** [https://paypal-hackathon-s0gq.onrender.com](https://paypal-hackathon-s0gq.onrender.com)  
> - **API Diagnostics:** [https://paypal-hackathon-s0gq.onrender.com/health](https://paypal-hackathon-s0gq.onrender.com/health)  
> - **PayPal Webhook ID:** `70X74465B0704404B`  
> - **MongoDB Atlas Cluster:** `cluster0.mfzju4v.mongodb.net/cohesora` (v8.0.37)  

---

## Table of Contents

1. [Executive Summary & Purpose](#1-executive-summary--purpose)
2. [Complete Directory & File Architecture](#2-complete-directory--file-architecture)
3. [Technology Stack & System Topology](#3-technology-stack--system-topology)
4. [Database Models, Schema & Entity Relationships](#4-database-models-schema--entity-relationships)
5. [Complete Frontend Component & Page Architecture](#5-complete-frontend-component--page-architecture)
6. [Interactive Elements & Button Action Catalog](#6-interactive-elements--button-action-catalog)
7. [Comprehensive Backend API Specification](#7-comprehensive-backend-api-specification)
8. [The PayMesh L402 Protocol Specification](#8-the-paymesh-l402-protocol-specification)
9. [Deterministic Spending Policy Engine](#9-deterministic-spending-policy-engine)
10. [PayPal Orders v2 & Webhook Lifecycle](#10-paypal-orders-v2--webhook-lifecycle)
11. [AI Reasoning & Model Context Protocol (MCP)](#11-ai-reasoning--model-context-protocol-mcp)
12. [Dual-Persistence & MongoDB Atlas Cloud Integration](#12-dual-persistence--mongodb-atlas-cloud-integration)
13. [Security, Cryptography & Invariant Guarantees](#13-security-cryptography--invariant-guarantees)
14. [Sponsor & External Integrations](#14-sponsor--external-integrations)
15. [End-to-End User Journeys](#15-end-to-end-user-journeys)
16. [Installation, Environment & Execution Runbook](#16-installation-environment--execution-runbook)
17. [Testing, Quality Assurance & Verification Results](#17-testing-quality-assurance--verification-results)
18. [Project Status & Production Roadmap](#18-project-status--production-roadmap)

---

## 1. Executive Summary & Purpose

### 1.1 The Core Problem
The software industry is transitioning from human-operated web browsers to autonomous software agents capable of executing multi-step research, market comparison, dataset procurement, and API orchestration. 

However, current payment and financial rails are completely incompatible with autonomous AI agents:
1. **The Prompt-Injection & Credential Danger:** Exposing static corporate credit cards, bank accounts, or unrestricted API tokens to an LLM creates catastrophic financial risk. Prompt injections, hallucinations, or runaway execution loops can drain funds or exfiltrate private credentials.
2. **Human-Centric Payment Barriers:** Traditional payment gateways rely on 3D Secure, captchas, cookie-based sessions, and visual browser redirects that crash autonomous headless agents.
3. **The Data Monetization Impasse:** Content creators and data publishers struggle to monetize proprietary APIs for AI crawlers without either blocking legitimate agents entirely or allowing them to scrape content without compensation.

### 1.2 The Solution: PayMesh AI
**PayMesh AI** establishes a standardized, enterprise-grade trust and settlement mesh for autonomous AI commerce. It connects four core primitives:

```
[Buyer / Autonomous Agent]
       │
       ▼
 [L402 Protocol Challenge (HTTP 402)]
       │
       ▼
[Deterministic Spending Policy Engine]  <--- Server-enforced financial limits
       │
       ▼
[PayPal Developer Sandbox (Orders v2 + Webhooks)] <--- Real programmable payment settlement
       │
       ▼
[Cryptographic Bearer Token (HMAC-SHA256)]
       │
       ▼
[Decrypted Data / Verified Channel3 Product Intelligence]
```

- **Machine-Readable Paywalls (L402):** Programmatic clients attempting to access monetized resources receive structured JSON challenges with pre-negotiated pricing offers, expiration timestamps, and settlement endpoints.
- **Deterministic Trust Engine:** The AI model is strictly prohibited from authorizing payments or changing prices. Spending limits (per-transaction ceilings, 24-hour rolling quotas) run deterministically on the server.
- **Genuine PayPal Settlement:** Full Orders v2 lifecycle—OAuth 2.0 client credentials, purchase unit creation, approval link delegation, server-side capture verification, and real-time webhook ingestion.
- **Dual Persistence:** High-speed relational session handling via SQLAlchemy 2.0 (PostgreSQL/SQLite) paired with immutable audit event logging on **MongoDB Atlas** (`cohesora` cluster).
- **Model Context Protocol (MCP):** Anthropic-compliant tool server allowing agents like Claude Desktop to discover and purchase datasets natively.

---

## 2. Complete Directory & File Architecture

```text
paypal-hackathon/
├── .env                                # Local environment secrets (Git-ignored)
├── .env.example                        # Documented environment template with placeholders
├── .gitignore                          # Exhaustive exclusion rules for builds, secrets & caches
├── docker-compose.yml                  # Multi-container local orchestration (Backend + Postgres)
├── pyproject.toml                      # Modern Python packaging and Pytest tool configuration
├── README.md                           # Master repository showcase with screenshots & verified badges
├── render.yaml                         # Production Render 1-click cloud Blueprint specification
├── requirements.txt                    # Pinned Python backend dependencies
├── vercel.json                         # Root Vercel deployment with API rewrite proxies
├── understanding.md                    # Comprehensive master technical documentation (This file)
│
├── backend/                            # FastAPI Application Root
│   ├── Dockerfile                      # Production container image definition
│   ├── requirements.txt                # Backend package manifest
│   ├── app/
│   │   ├── main.py                     # Application entry point, lifespan, CORS & static mounts
│   │   ├── agent/                      # AI Agent Core Engine
│   │   │   ├── llm_client.py           # Multi-provider client (Google Gemini 2.5, OpenAI, Claude)
│   │   │   ├── orchestrator.py         # Autonomous discovery, challenge & policy workflow
│   │   │   ├── policy.py               # Deterministic spending limits & rolling 24h budget engine
│   │   │   └── tools.py                # Tool registry for catalogue, challenge, and payments
│   │   ├── api/v1/routes/              # REST API Route Controllers
│   │   │   ├── __init__.py             # Unified API router mounting all sub-routes
│   │   │   ├── agent.py                # Agent runs, policy evaluation, policy config & MCP routes
│   │   │   ├── analytics.py            # Publisher KPI summaries, transactions & usage endpoints
│   │   │   ├── catalogue.py            # Public dataset marketplace & pricing offer registry
│   │   │   ├── health.py               # Health probe reporting SQLite/Postgres & MongoDB status
│   │   │   ├── payments.py             # Payment sessions, PayPal capture & Webhook listener
│   │   │   ├── publisher.py            # Merchant resource publishing & pricing offer creation
│   │   │   └── resources.py            # Resource details & HTTP 402 L402 paywall content gates
│   │   ├── core/                       # Core Infrastructure
│   │   │   ├── config.py               # Pydantic v2 Settings (env parsing, PayPal URLs, DB URLs)
│   │   │   ├── exceptions.py           # Domain exceptions (PayMeshException, PolicyViolation, etc.)
│   │   │   ├── logging.py              # Structured application logger with formatting
│   │   │   └── security.py             # Cryptographic hashing (HMAC-SHA256), passwords & tokens
│   │   ├── db/                         # Database Access Layer
│   │   │   ├── base.py                 # SQLAlchemy DeclarativeBase metadata
│   │   │   ├── mongodb.py              # MongoDB Atlas client with certifi TLS & audit logger
│   │   │   └── session.py              # Async engine, sessionmaker & lifespan table init
│   │   ├── mcp/                        # Model Context Protocol Standard
│   │   │   └── server.py               # Anthropic MCP manifest generator & tool dispatcher
│   │   ├── models/                     # Relational ORM Entities
│   │   │   └── entities.py             # User, Resource, Offer, Challenge, Session, Transaction, etc.
│   │   ├── schemas/                    # Pydantic v2 Data Transfer Objects (DTOs)
│   │   │   ├── agent.py                # Agent run, recommendation, policy config & MCP schemas
│   │   │   ├── analytics.py            # KPI metrics, paginated transaction & usage schemas
│   │   │   ├── catalogue.py            # Public resource and offer presentation schemas
│   │   │   ├── payment.py              # Session creation, status, and capture response schemas
│   │   │   └── publisher.py            # Resource creation & offer specification schemas
│   │   ├── scripts/                    # Database Seeding & Setup
│   │   │   └── seed_demo.py            # Seeds default publisher, Channel3 keyboards & news datasets
│   │   ├── services/                   # Business Logic Domain Services
│   │   │   ├── analytics_service.py    # Revenue sums, conversion metrics & transaction history
│   │   │   ├── challenge_service.py    # L402 challenge creation, validation, consumption & expiry
│   │   │   ├── channel3_client.py      # Channel3 Product Data API client with latency fixtures
│   │   │   ├── entitlement_service.py  # Cryptographic Bearer token issuance & hash verification
│   │   │   ├── paypal_gateway.py       # PayPal Sandbox OAuth, Orders v2 creation, capture & fallback
│   │   │   └── resource_service.py     # Catalogue queries, slug lookup & protected content assembly
│   │   └── templates/                  # Static HTML Fallbacks
│   │       └── portal.html             # Standalone fallback testing portal
│   └── tests/                          # Automated Pytest Suite (28 passing tests)
│       ├── conftest.py                 # Async HTTP client, in-memory SQLite fixtures & mock session
│       ├── integration/                # Integration Tests
│       │   └── test_api_endpoints.py   # Health, Catalogue, L402 402, Capture, MCP, Webhook & Policy
│       └── unit/                       # Unit Tests
│           ├── test_ai_agent.py        # Tool argument validation, orchestrator traces & LLM mock
│           ├── test_config_and_security.py # Settings parsing, HMAC token hashing & passwords
│           └── test_policy.py          # Deterministic budget, currency match & ceiling limits
│
├── frontend/                           # React 18 + Vite + Tailwind CSS Frontend
│   ├── package.json                    # Dependencies (React 18, Vite 6, AG Grid 32, Lucide React)
│   ├── tailwind.config.js              # Neo-tech theme tokens, blueprint grids & brutalist shadows
│   ├── tsconfig.json                   # Strict TypeScript compiler configuration
│   ├── vercel.json                     # Frontend Vercel rewrites to Render backend
│   ├── vite.config.ts                  # Vite build settings & local API proxy configuration
│   └── src/
│       ├── App.tsx                     # Main layout shell, tab navigation & developer footer
│       ├── index.css                   # Neo-tech styling utilities, blueprint grid & AG Grid CSS
│       ├── main.tsx                    # React DOM entry point
│       └── components/                 # View Modules
│           ├── AgentWorkspace.tsx      # AI agent command center, L402 terminal & PayPal modal
│           ├── AnalyticsView.tsx       # AG Grid financial ledger with sorting, filtering & CSV export
│           ├── CatalogueView.tsx       # Data product marketplace, category chips & agent dispatch
│           ├── Navbar.tsx              # Navigation bar, PayPal Sandbox pill & OpenAPI links
│           ├── PolicyManager.tsx       # Dynamic spending policy control plane & 24h budget meter
│           └── PublisherConsole.tsx    # Merchant publishing studio with live card preview
│
├── remotion/                           # Programmatic React Video Pitch Engine
│   ├── package.json                    # Remotion CLI and core dependencies
│   ├── remotion.config.ts              # Video render configuration (1080p, 30fps)
│   ├── src/
│   │   ├── index.ts                    # Remotion bundle entry point
│   │   ├── PayMeshDemo.tsx             # 60-second primary pitch video composition
│   │   ├── PayMeshTeaser.tsx           # 15-second high-energy teaser composition
│   │   ├── Root.tsx                    # Remotion composition registration root
│   │   ├── types.ts                    # Shared animation and slide types
│   │   ├── components/                 # Reusable video components (HeaderBadge, NeoCard)
│   │   └── scenes/                     # Intro, Problem, Solution, Architecture, Showcase, Outro
│   └── out/                            # Rendered artifacts
│       └── paymesh-demo.mp4            # Full 1080p demo render (26 MB, 1800 frames)
│
├── docs/                               # Architecture Documentation & Visual Assets
│   ├── api-reference.md                # Markdown API endpoint reference
│   ├── baseline-audit.md               # Early project architecture audit
│   ├── BASELINE_FUNCTIONALITY_REPORT.md# Baseline functionality checklist
│   ├── demo-script.md                  # Video voiceover and demonstration transcript
│   ├── FRONTEND_AUDIT.md               # Frontend UI/UX audit report
│   ├── security.md                     # Security architecture & threat analysis
│   ├── assets/screenshots/             # 7 genuine application screenshots used in README
│   └── decisions/                      # Architecture Decision Records (ADR 001, 002, 003)
│
├── scripts/                            # Verification & Automation Scripts
│   ├── capture_screenshots.py          # Playwright headless browser screenshot capture script
│   ├── smoke_test.py                   # 7-step automated end-to-end integration smoke test
│   └── test_mongo.py                   # MongoDB Atlas TLS connectivity & audit event test
│
└── client/                             # CLI Programmatic Client
    └── main.py                         # Command-line bot for automated L402 purchases
```

---

## 3. Technology Stack & System Topology

### 3.1 Technology Matrix

| Component | Technology | Version | Purpose in PayMesh AI |
| :--- | :--- | :--- | :--- |
| **Backend Framework** | FastAPI | 0.115+ | Asynchronous REST gateway, L402 paywall middleware, dependency injection |
| **ASGI Server** | Uvicorn | 0.34+ | High-throughput asynchronous HTTP/1.1 server |
| **Relational ORM** | SQLAlchemy | 2.0.38+ | Async entity management, connection pooling, and transactional integrity |
| **Database Engines** | SQLite / PostgreSQL | 3.x / 16.x | Session state, catalogue records, challenges, entitlements |
| **NoSQL Database** | MongoDB Atlas | 8.0.37 | Cloud audit ledger (`auditevents`) and persistent document storage |
| **Payment Settlement** | PayPal Developer Platform | Orders v2 | OAuth 2.0 client token, purchase units, server capture, Webhooks |
| **AI Inference** | Google Gemini | 2.5 Flash | Intent interpretation, dataset selection, hardware intelligence synthesis |
| **Fallback AI Engine** | OpenAI / Anthropic | SDK 1.5+ | GPT-4o-mini and Claude 3.5 Sonnet support |
| **Agent Protocol** | Anthropic MCP | 1.0 | Model Context Protocol server manifest and tool execution |
| **Frontend Framework** | React | 18.3.1 | Component-driven reactive user interface |
| **Frontend Build Tool** | Vite | 6.0.1 | High-speed ESM development server and Rollup production bundler |
| **Styling & Theme** | Tailwind CSS | 3.4.15 | Custom Neo-Tech aesthetic with brutalist drop shadows and blueprint grid |
| **Data Grid** | AG Grid Community | 32.3.3 | Enterprise financial settlement table with sorting, filtering, CSV export |
| **Iconography** | Lucide React | 0.460+ | Modern vector icons |
| **Video Engine** | Remotion | 4.0.250+ | Code-driven React video rendering for 1080p demo MP4 |
| **Testing** | Pytest + AsyncIO | 9.0.3 | 28 automated unit and integration tests |

### 3.2 High-Level System Architecture Diagram

```mermaid
flowchart TD
    subgraph ClientLayer ["Client & Interface Layer"]
        BrowserUI["React 18 SPA (Vercel)"]
        CLIBot["Python CLI Bot (client/main.py)"]
        MCPAgent["Anthropic MCP Agent (Claude Desktop)"]
    end

    subgraph GatewayLayer ["PayMesh AI API Gateway (Render Cloud)"]
        FastAPIApp["FastAPI ASGI Server (:8000)"]
        CORSMiddleware["Strict CORS & Security Headers"]
        L402Paywall["L402 Challenge Middleware"]
    end

    subgraph IntelligenceLayer ["Autonomous Intelligence & Policy Layer"]
        GeminiClient["Google Gemini 2.5 Flash Engine"]
        Orchestrator["Agent Orchestrator"]
        PolicyEngine["Deterministic Spending Engine"]
        MCPServer["Model Context Protocol Server"]
    end

    subgraph SettlementLayer ["Payment & Settlement Layer"]
        PayPalGateway["PayPal Gateway Service"]
        PayPalSandbox["PayPal Sandbox Orders v2 API"]
        PayPalWebhooks["PayPal Webhook Receiver (/api/v1/payments/webhook)"]
    end

    subgraph StorageLayer ["Persistence & Audit Infrastructure"]
        SQLAlchemyAsync["SQLAlchemy 2.0 Async Session"]
        RelationalDB[("PostgreSQL / SQLite")]
        MongoDBAtlas[("MongoDB Atlas Cloud ('cohesora')")]
    end

    subgraph DataProviderLayer ["Data & Sponsor Registries"]
        Channel3Client["Channel3 Hardware Latency API"]
        MarketplaceCatalogue["Data Product Catalogue"]
    end

    BrowserUI -->|HTTP / JSON| FastAPIApp
    CLIBot -->|HTTP / JSON| FastAPIApp
    MCPAgent -->|MCP JSON-RPC| FastAPIApp

    FastAPIApp --> CORSMiddleware
    CORSMiddleware --> L402Paywall

    L402Paywall --> Orchestrator
    Orchestrator --> GeminiClient
    Orchestrator --> MCPServer
    Orchestrator --> PolicyEngine

    PolicyEngine -->|Evaluates limits against| SQLAlchemyAsync
    Orchestrator -->|Triggers payment| PayPalGateway

    PayPalGateway -->|OAuth & Orders v2| PayPalSandbox
    PayPalSandbox -->|Webhook Events| PayPalWebhooks
    PayPalWebhooks -->|Mirror audit record| MongoDBAtlas

    SQLAlchemyAsync --> RelationalDB
    FastAPIApp --> MongoDBAtlas

    Orchestrator --> Channel3Client
    Orchestrator --> MarketplaceCatalogue
```

---

## 4. Database Models, Schema & Entity Relationships

PayMesh AI uses **SQLAlchemy 2.0 DeclarativeBase** with `mapped_column` syntax and UUID primary keys.

### 4.1 Relational Entities

1. **`User` (`users` table):**
   - Stores user identities, email addresses, hashed passwords, and system roles (`admin`, `publisher`, `buyer`).
2. **`Resource` (`resources` table):**
   - Represents a monetized dataset or API. Holds `slug` (unique identifier), `title`, `description`, `resource_type`, `provider` (e.g. `channel3`), `status` (`active`/`inactive`), and `metadata_json`.
   - ForeignKey to `User` (`publisher_id`).
3. **`Offer` (`offers` table):**
   - The authoritative pricing contracts for a resource. Holds `offer_code`, `price_amount` (Decimal), `currency` (`USD`, `EUR`, `GBP`), `pricing_model` (`one_time`, `subscription`), `duration_seconds`, `active` flag, and `scope_json`.
   - ForeignKey to `Resource` (`resource_id`).
4. **`PaymentChallenge` (`payment_challenges` table):**
   - An ephemeral cryptographic challenge issued when an unauthenticated request triggers HTTP 402. Holds `id` (`chl_<hex>`), `status` (`PENDING`, `CONSUMED`, `EXPIRED`), `expires_at`, and links to `Resource` and `Offer`.
5. **`PaymentSession` (`payment_sessions` table):**
   - Represents an initiated checkout flow. Stores `session_id` (UUID), `paypal_order_id`, `amount`, `currency`, `status` (`CREATED`, `CAPTURED`, `FAILED`), and `agent_id`.
   - ForeignKey to `PaymentChallenge` (`challenge_id`).
6. **`Transaction` (`transactions` table):**
   - Immutable financial settlement record created upon successful capture. Stores `paypal_order_id`, `paypal_capture_id`, `gross_amount`, `currency`, `payment_status` (`COMPLETED`), `captured_at`, and raw capture response JSON.
   - ForeignKey to `PaymentSession` (`payment_session_id`).
7. **`Entitlement` (`entitlements` table):**
   - Proof of purchase. Stores `agent_id`, `token_hash` (HMAC-SHA256 salted hash of the Bearer token), `status` (`ACTIVE`, `EXPIRED`, `REVOKED`), `expires_at`, and `scope_json`.
   - ForeignKeys to `Resource` and `Offer`.
8. **`UsageEvent` (`usage_events` table):**
   - High-throughput operational metric tracking every API request, data fetch, and token validation.
9. **`AuditLog` (`audit_logs` table):**
   - Relational audit trace logging actor actions, entity mutations, and metadata.
10. **`PolicySetting` (`policy_settings` table):**
    - Database-persisted spending policy rules (`max_per_transaction`, `daily_cap`, `allowed_currencies_json`, `auto_approve_under`, `enforce_prompt_sanitization`, `strict_scope_check`, `updated_at`). Ensures spending limits survive server restarts and scale consistently.

### 4.2 Entity-Relationship Diagram (ERD)

```mermaid
erDiagram
    User ||--o{ Resource : "publishes"
    Resource ||--|{ Offer : "contains pricing tiers"
    Resource ||--o{ PaymentChallenge : "protected by"
    Offer ||--o{ PaymentChallenge : "defines price in"
    PaymentChallenge ||--o| PaymentSession : "settled via"
    PaymentSession ||--o| Transaction : "captured into"
    PaymentSession ||--o| Entitlement : "issues"
    Offer ||--o{ Entitlement : "grants scope"
    Resource ||--o{ Entitlement : "authorizes"
    Resource ||--o{ UsageEvent : "tracks queries"
```

---

## 5. Complete Frontend Component & Page Architecture

The frontend is an ultra-responsive, single-page application built on **React 18** with **Vite 6** and **Tailwind CSS**.

### 5.1 `App.tsx` (Root Application Shell)
- **Role:** Main container managing navigation state (`activeTab`), cross-view context handoff, and the developer ecosystem footer.
- **State Managed:**
  - `activeTab`: String identifying the visible view (`workspace`, `policy`, `catalogue`, `analytics`, `publisher`).
  - `targetResourceSlug`: String tracking dataset slug passed from the Catalogue to the Agent Workspace.
- **Header:** Mounts `<Navbar />` with sticky positioning.
- **Footer:** Renders developer links to GitHub repo, Swagger `/docs`, MCP manifest, and PayPal Developer Sandbox.

### 5.2 `Navbar.tsx` (Top Navigation & Status Bar)
- **Brand Logo:** Neo-tech isometric "PM" badge with live pulse indicator. Clicking returns to `workspace`.
- **Navigation Tabs:** Desktop pill tabs with icons for each view. Active tabs receive brutalist yellow fill and black border.
- **Status Badges:** Displays live green `PayPal Sandbox Orders v2` status pill and link to Swagger `/docs`.
- **Mobile Menu:** Collapsible animated drawer for mobile screens.

### 5.3 `AgentWorkspace.tsx` (AI Commerce Mission Control)
- **Task Form:** Natural language prompt input with research goals.
- **Quick Goal Chips:** One-click presets:
  - *Wooting vs Keychron* (Hardware latency benchmarks)
  - *Rapid Trigger Switches* (Gaming actuator profiles)
  - *Budget Hall Effect* (Price-to-performance matrix)
- **Spending Policy Limit:** Number input defining maximum buyer allowance (e.g. `$0.10 USD`).
- **Dispatch Button:** Initiates autonomous agent run via `POST /api/v1/agent/runs`.
- **Protocol Terminal:** Real-time log inspector streaming timestamped events (`INFO`, `L402`, `SUCCESS`, `ERROR`). Includes "Copy Log" and "Clear" utilities.
- **Recommendation & Challenge Card:** Displays discovered resource title, verified offer price, policy clearance, and "Authorize Payment" button.
- **PayPal Checkout Modal:** Modal presenting purchase unit breakdown, PayPal Sandbox branding, and the "Confirm & Capture with PayPal" action.
- **Unlocked Intelligence Panel:** Displays decrypted Channel3 product specifications, switch latencies, market insights, and the cryptographic Bearer token with one-click clipboard copy.

### 5.4 `PolicyManager.tsx` (Deterministic Spending Guardrails)
- **Real-Time Budget Meter:** Progress bar dynamically querying `GET /api/v1/agent/policy/config` and calculating genuine 24-hour expenditure against the rolling cap.
- **Controls Form:**
  - *Max Spend Per Transaction:* Hard ceiling on single purchases.
  - *Cumulative Daily Cap:* 24-hour rolling budget ceiling.
  - *Prompt-Injection Sanitization Toggle:* Forces untrusted payload wrapping.
  - *Strict Scope Check Toggle:* Binds Bearer token to specific resource.
- **Save Action:** Sends `PUT /api/v1/agent/policy/config` to update server policy parameters in runtime.

### 5.5 `CatalogueView.tsx` (Data Product Registry)
- **Search Bar:** Real-time filtering across dataset titles, slugs, descriptions, and providers.
- **Category Chips:** Filters resources by provider: *All Products*, *Channel3 Hardware*, *News Feeds*.
- **Dataset Cards:** Displays provider badges, resource slugs, pricing offers (price, currency, model, duration), and publisher attribution.
- **Actions:**
  - *HTTP 402 Link:* Opens raw challenge URL in a new tab for manual inspection.
  - *Dispatch Agent Button:* Switches to `workspace` tab and pre-fills task input with the selected dataset.

### 5.6 `AnalyticsView.tsx` (AG Grid Financial Ledger)
- **KPI Summary Cards:**
  - Total Captured Revenue ($ USD)
  - Completed Transactions Count
  - Active Entitlements Count
  - Unique Agent Identities
  - Conversion Rate Percentage
- **AG Grid Table:** Full-featured grid with custom cell renderers for Captured Date, Resource Title, Environment, PayPal Order ID, Capture ID, Gross Amount, and Status.
- **Actions:**
  - *Export CSV:* Downloads current ledger rows as `paymesh_ledger_<date>.csv`.
  - *Refresh:* Re-fetches `/publisher/analytics/summary` and `/publisher/analytics/transactions`.

### 5.7 `PublisherConsole.tsx` (Merchant Publishing Studio)
- **Resource Details Form:** Title input, Auto-Slug generator (`handleAutoSlug`), provider dropdown, and description.
- **Pricing Offer Builder:** Offer code, offer label, price (USD), duration (seconds), and pricing model.
- **Live Preview Card:** Real-time visual mockup showing how the resource will appear to AI agents.
- **Submission:** Submits resource and offer to backend, displays success banner with direct link to view in Catalogue.

---

## 6. Interactive Elements & Button Action Catalog

| Component | UI Element / Button | Trigger Event | Expected Action | Backend API Called | State Updated |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`Navbar`** | Logo / Title | `onClick` | Navigates to workspace tab | None | `activeTab = 'workspace'` |
| **`Navbar`** | Navigation Tabs (5 tabs) | `onClick` | Switches active view | None | `activeTab = <id>` |
| **`Navbar`** | Mobile Menu Toggle | `onClick` | Toggles mobile drawer | None | `mobileMenuOpen = !open` |
| **`Navbar`** | API Docs Link | `onClick` | Opens Swagger UI in new tab | None (Browser nav) | None |
| **`AgentWorkspace`** | Quick Goal Chip (Wooting) | `onClick` | Pre-fills task and budget | None | `task = ...`, `budget = 0.10` |
| **`AgentWorkspace`** | Quick Goal Chip (Actuation) | `onClick` | Pre-fills task and budget | None | `task = ...`, `budget = 0.15` |
| **`AgentWorkspace`** | Quick Goal Chip (Budget) | `onClick` | Pre-fills task and budget | None | `task = ...`, `budget = 0.08` |
| **`AgentWorkspace`** | "Dispatch Agent" Button | `onClick` | Initiates autonomous run | `POST /api/v1/agent/runs` | `status = 'DISCOVERING' -> 'AWAITING_APPROVAL'` |
| **`AgentWorkspace`** | "Authorize Payment" Button | `onClick` | Opens PayPal checkout modal | None | `showCheckoutModal = true` |
| **`AgentWorkspace`** | "Reject & Abort" Button | `onClick` | Cancels pending transaction | None | `status = 'IDLE'` |
| **`AgentWorkspace`** | "Confirm & Capture with PayPal" | `onClick` | Executes PayPal Order capture & unlocks content | `POST /api/v1/payment-sessions`<br>`POST /.../capture`<br>`GET /.../content` | `status = 'PAYING' -> 'COMPLETED'`, `bearerToken`, `unlockedData` |
| **`AgentWorkspace`** | Modal "Cancel" Button | `onClick` | Closes modal | None | `showCheckoutModal = false` |
| **`AgentWorkspace`** | "Copy Token" Button | `onClick` | Copies Bearer token to clipboard | None (Clipboard API) | `copiedToken = true` |
| **`AgentWorkspace`** | "Copy Audit Trace" Button | `onClick` | Copies terminal log to clipboard | None (Clipboard API) | `copiedLog = true` |
| **`AgentWorkspace`** | "Clear Terminal" Button | `onClick` | Clears all log entries | None | `logs = []` |
| **`PolicyManager`** | Budget Refresh Button | `onClick` | Re-fetches 24h spend metrics | `GET /api/v1/agent/policy/config` | `currentUtilized`, `utilizedPct` |
| **`PolicyManager`** | "Update Policy Rules" Button | `onSubmit` | Persists spending limits | `PUT /api/v1/agent/policy/config` | `saved = true`, updates engine |
| **`CatalogueView`** | Category Filter Chips | `onClick` | Filters list by provider | None | `selectedCategory = <id>` |
| **`CatalogueView`** | Search Input Clear (X) | `onClick` | Clears search input | None | `searchTerm = ''` |
| **`CatalogueView`** | Catalogue Refresh Button | `onClick` | Re-fetches marketplace items | `GET /api/v1/catalogue` | `resources = [...]` |
| **`CatalogueView`** | "HTTP 402" Link | `onClick` | Opens raw challenge endpoint | Browser GET | None |
| **`CatalogueView`** | "Dispatch Agent" Button | `onClick` | Sends slug to workspace | None | `targetResourceSlug = slug`, `activeTab = 'workspace'` |
| **`AnalyticsView`** | "Export CSV" Button | `onClick` | Generates & downloads CSV | None (Browser Blob) | `exported = true` |
| **`AnalyticsView`** | Analytics Refresh Button | `onClick` | Refreshes KPI and ledger | `GET /publisher/analytics/summary`<br>`GET /publisher/analytics/transactions` | `summary`, `transactions` |
| **`PublisherConsole`**| "Auto Slug" Button | `onClick` | Formats title into valid slug | None | `slug = formatted` |
| **`PublisherConsole`**| "Publish Data Product" Button| `onSubmit` | Creates resource & offer | `POST /api/v1/publisher/resources`<br>`POST /.../offers` | `message = success`, resets form |
| **`PublisherConsole`**| "View in Catalogue" Link | `onClick` | Navigates to catalogue view | None | `activeTab = 'catalogue'` |

---

## 7. Comprehensive Backend API Specification

Interactive OpenAPI documentation is hosted at:  
👉 **`https://paypal-hackathon-s0gq.onrender.com/docs`** (or `http://localhost:8000/docs` locally).

### 7.1 Endpoints Summary

| Method | Path | Summary | Auth Required |
| :---: | :--- | :--- | :---: |
| `GET` | `/health` | System health probe, database check, MongoDB Atlas info | Public |
| `GET` | `/api/v1/catalogue` | Returns all active resources and pre-negotiated offers | Public |
| `GET` | `/api/v1/resources/{slug}` | Returns public metadata and pricing tiers for a slug | Public |
| `GET` | `/api/v1/resources/{slug}/content` | Protected data gate: returns 402 challenge or unlocked content | Bearer Token |
| `POST` | `/api/v1/payment-sessions` | Initiates PayPal Sandbox Orders v2 checkout | Public |
| `GET` | `/api/v1/payment-sessions/{id}` | Polls payment session status | Public |
| `POST` | `/api/v1/payment-sessions/{id}/capture` | Server-side capture of PayPal Order & Bearer token issuance | Public |
| `POST` | `/api/v1/payments/webhook` | Receives asynchronous PayPal Sandbox webhook events | Public |
| `POST` | `/api/v1/agent/runs` | Multi-step agent workflow: discovery, challenge, policy check | Public |
| `POST` | `/api/v1/agent/policy/evaluate` | Evaluates single-offer policy constraints | Public |
| `GET` | `/api/v1/agent/policy/config` | Retrieves active spending limits and 24h utilized budget | Public |
| `PUT` | `/api/v1/agent/policy/config` | Updates deterministic spending limits in server memory | Public |
| `POST` | `/api/v1/agent/tools/{tool_name}` | Direct execution of registered agent tools | Public |
| `GET` | `/api/v1/agent/mcp/manifest` | Anthropic Model Context Protocol server manifest | Public |
| `POST` | `/api/v1/agent/mcp/call` | Executes tool via Model Context Protocol JSON-RPC | Public |
| `POST` | `/api/v1/publisher/resources` | Registers a new dataset and provider | Public |
| `POST` | `/api/v1/publisher/resources/{id}/offers` | Creates pricing tiers for a resource | Public |
| `GET` | `/api/v1/publisher/analytics/summary` | Real-time publisher revenue, conversion, and orders | Public |
| `GET` | `/api/v1/publisher/analytics/transactions`| Paginated ledger of captured PayPal transactions | Public |
| `GET` | `/api/v1/publisher/analytics/usage` | Paginated log of API usage events | Public |

---

## 8. The PayMesh L402 Protocol Specification

The **PayMesh L402 Protocol** standardizes machine-to-machine payment negotiation over standard HTTP error semantics.

### 8.1 The HTTP 402 Challenge Envelope
When an agent sends `GET /api/v1/resources/{slug}/content` without an `Authorization` header, the server returns status `402 Payment Required` with a structured payload:

```json
{
  "protocol": "paymesh-l402",
  "protocol_version": "1.0",
  "status": 402,
  "challenge_id": "chl_ebf3ca705752e1bedc35e9b71d7d547f",
  "resource": {
    "id": "res_8df72c1a93b4",
    "slug": "channel3-mechanical-keyboards",
    "title": "Channel3 Keyboard Latency Intelligence"
  },
  "offers": [
    {
      "id": "off_3b8a1c9e74d2",
      "offer_code": "channel3_single_query",
      "title": "Single Query Access",
      "description": "Access full switch latency benchmarks",
      "amount": 0.05,
      "currency": "USD",
      "pricing_model": "one_time",
      "duration_seconds": 3600,
      "scope": { "access": "read", "dataset": "channel3-mechanical-keyboards" },
      "payment_method": "paypal"
    }
  ],
  "payment_endpoint": "http://localhost:8000/api/v1/payment-sessions",
  "expires_at": "2026-11-05T15:27:40.662592+00:00",
  "correlation_id": "74944790-e388-41ae-89b0-340010bdb861"
}
```

### 8.2 Cryptographic Challenge Invariants
1. **Challenge Lifespan:** Challenges expire after 10 minutes (`PAYMENT_CHALLENGE_TTL_MINUTES = 10`).
2. **One-Time Consumption:** Once captured, a challenge enters `CONSUMED` state. Retrying a consumed challenge returns `400 Bad Request`.
3. **Price Binding:** The amount in `offers[0].amount` is read directly from the database; prompt parameters cannot alter this value.

---

## 9. Deterministic Spending Policy Engine

Large Language Models are probabilistic and susceptible to prompt injection. If an agent is granted financial authority, malicious input could instruct it to pay arbitrary sums to attacker accounts.

PayMesh AI solves this by decoupling intent interpretation from payment authorization:

### 9.1 Policy Rules Enforced in `PolicyEngine`
1. **Hard Ceiling Per Transaction:** Any offer exceeding `max_single_tx_limit` (default `$25.00`, configurable in UI down to `$0.50`) is rejected before payment initiation.
2. **Rolling 24-Hour Cumulative Quota:** The engine calculates total settled spend in the last 24 hours:
   $$\text{Current Spend} + \text{Offer Amount} \le \text{Daily Cap}$$
3. **Currency Invariant Check:** Only pre-approved currencies (`USD`, `EUR`, `GBP`) are permitted.
4. **Offer Active State Check:** Inactive or deleted offers are rejected immediately.
5. **Prompt-Injection Sanitization:** Data returned from external publishers is treated as untrusted strings and cannot execute system-level commands.

---

## 10. PayPal Orders v2 & Webhook Lifecycle

PayMesh AI connects to the **PayPal Developer Sandbox** (`api-m.sandbox.paypal.com`):

```mermaid
sequenceDiagram
    autonumber
    participant Agent as Autonomous AI Agent
    participant Gateway as PayMesh AI Gateway
    participant PayPal as PayPal Sandbox API
    participant Mongo as MongoDB Atlas Cloud

    Agent->>Gateway: POST /api/v1/payment-sessions (challenge_id, offer_id)
    Gateway->>PayPal: POST /v1/oauth2/token (Client ID + Secret)
    PayPal-->>Gateway: Access Token (expires_in: 32400)
    Gateway->>PayPal: POST /v2/checkout/orders (intent: CAPTURE, amount: $0.05)
    PayPal-->>Gateway: Order Created (ID: 2M942495GD6205744)
    Gateway-->>Agent: Returns session_id & approval_url

    Agent->>Gateway: POST /api/v1/payment-sessions/{id}/capture
    Gateway->>PayPal: POST /v2/checkout/orders/{id}/capture
    PayPal-->>Gateway: Status: COMPLETED (Capture ID: CAP-2M942495)
    
    Gateway->>Gateway: Mint Bearer Token (pm_live_...) & Store HMAC Hash
    Gateway->>Mongo: Insert Audit Event (auditevents: PAYPAL_CAPTURE_SUCCESS)
    Gateway-->>Agent: Returns Bearer Token

    PayPal-->>Gateway: POST /api/v1/payments/webhook (Event: PAYMENT.CAPTURE.COMPLETED)
    Gateway->>Mongo: Insert Webhook Event (auditevents: PAYPAL_WEBHOOK_RECEIVED)
    Gateway-->>PayPal: HTTP 200 OK
```

### 10.1 Webhook Verification & Lifecycle Security
- **Registered Webhook ID:** `70X74465B0704404B`
- **Endpoint:** `https://paypal-hackathon-s0gq.onrender.com/api/v1/payments/webhook`
- **Events Tracked:** All Events (specifically `PAYMENT.CAPTURE.COMPLETED`, `CHECKOUT.ORDER.APPROVED`)
- **Cryptographic Signature Verification:** Every incoming request is verified via PayPal's `/v1/notifications/verify-webhook-signature` endpoint:
  - Validates `PAYPAL-AUTH-ALGO`, `PAYPAL-CERT-URL`, `PAYPAL-TRANSMISSION-ID`, `PAYPAL-TRANSMISSION-SIG`, and `PAYPAL-TRANSMISSION-TIME`.
  - Rejects untrusted, spoofed, or unauthenticated HTTP requests with `401 Unauthorized`.
- **Idempotency & Replay Protection:** Webhook event IDs are deduplicated against the relational `AuditLog` table. Replayed events return `200 OK` with status `already_processed` without duplicate side-effects.
- **State Reconciliation:** Upon receiving `CHECKOUT.ORDER.APPROVED` or `PAYMENT.CAPTURE.COMPLETED`, the handler reconciles and updates the associated `PaymentSession` state in both SQLite/Postgres and MongoDB Atlas.

---

## 11. AI Reasoning & Model Context Protocol (MCP)

### 11.1 Google Gemini AI Engine
- **Primary Model:** `gemini-2.5-flash` (with automated `gemini-1.5-flash` fallback).
- **Architecture:** Pure asynchronous REST tool-calling loop using Google Generative Language API (`/v1beta/models/{model}:generateContent`).
- **Function Declarations:**
  1. `discover_resources`: Typed arguments (`query`, `limit`), searches verified publisher catalog.
  2. `get_resource_offer`: Retrieves authoritative database price and scope for a resource slug.
  3. `evaluate_purchase_policy`: Evaluates candidate offers against deterministic financial guardrails.
- **Safety Invariant:** The model cannot create orders, execute captures, or modify policy limits; it acts purely as an intelligent procurement advisor.

### 11.2 Model Context Protocol (MCP) Server
PayMesh AI exposes an Anthropic MCP server at `/api/v1/agent/mcp/manifest` exposing standardized tools:
1. `discover_resources`: Programmatically searches marketplace datasets by keyword or provider.
2. `get_resource_offer`: Retrieves active pricing offers for a dataset.
3. `evaluate_purchase_policy`: Evaluates whether a proposed purchase satisfies deterministic financial constraints.

---

## 12. Dual-Persistence & MongoDB Atlas Cloud Integration

PayMesh AI implements a dual-persistence strategy:
1. **Relational Core (SQLAlchemy + SQLite/Postgres):** Handles ACID-compliant checkout sessions, entitlement lifecycles, and relational constraints.
2. **MongoDB Atlas Cloud (`cohesora` Cluster):** Provides an immutable, append-only document repository for audit logs and webhook receipts.

### 12.1 MongoDB Collections
- **`auditevents`**: Stores every capture event, webhook notification, and agent action with timestamp, cluster identifier, and raw payload.

---

## 13. Security, Cryptography & Invariant Guarantees

1. **Token Hashing:** Bearer tokens (`pm_live_<base64>`) are never stored in plain text. The database only stores `token_hash = hmac_sha256(SECRET_KEY, raw_token)`.
2. **Challenge Isolation:** Challenge IDs, PayPal Order IDs, and Bearer Tokens are cryptographically decoupled. Knowing a PayPal Order ID grants no access to data.
3. **Security Headers:** Every response carries:
   - `X-Content-Type-Options: nosniff`
   - `X-Frame-Options: SAMEORIGIN`
   - `Referrer-Policy: strict-origin-when-cross-origin`
   - `Permissions-Policy: geolocation=(), camera=(), microphone=()`
4. **CORS Isolation:** Strict explicit origins allowed without wildcards, with regex support for `https://.*\.vercel\.app`.

---

## 14. Sponsor & External Integrations

| Sponsor / Service | Integration Point | Implementation Detail |
| :--- | :--- | :--- |
| **PayPal** | Orders v2 & Webhooks | Server-side OAuth 2.0, order creation, capture, and webhook handler |
| **Google Gemini** | AI Reasoning | `gemini-2.5-flash` client for autonomous task formulation |
| **MongoDB Atlas** | Audit Cloud | Managed cluster `cluster0.mfzju4v.mongodb.net/cohesora` for audit events |
| **AG Grid** | Financial Table | AG Grid Community v32 with sorting, filtering, and CSV export |
| **Channel3** | Product Data | Hardware latency benchmarks, switch profiles, and retail links |
| **Render** | Backend Hosting | `render.yaml` Blueprint with automated Postgres provisioning |
| **Vercel** | Frontend Hosting | Vite SPA hosting with automated API rewrite proxies |
| **Remotion** | Pitch Video | Programmatic React video compositions in `remotion/` |

---

## 15. End-to-End User Journeys

### 15.1 The Autonomous Buyer Agent Journey
1. **Initiation:** User enters `"Find mechanical keyboards with ultra-low latency"` in the Agent Workspace.
2. **Discovery:** Agent calls `/api/v1/catalogue` and selects `channel3-mechanical-keyboards`.
3. **Paywall Hit:** Agent attempts to fetch content, receiving `HTTP 402` with challenge `chl_...`.
4. **Policy Clearance:** Policy engine verifies `$0.05` is within budget.
5. **Checkout:** Agent creates PayPal Order `2M942495...` and requests human approval.
6. **Capture:** Upon approval, server captures order and mints Bearer token `pm_live_...`.
7. **Unlock:** Agent exchanges Bearer token for hardware benchmarks and displays comparison.

### 15.2 The Data Publisher Journey
1. **Creation:** Publisher enters title, description, and price in Merchant Studio.
2. **Publication:** Server registers resource and creates pricing offer.
3. **Monetization:** Resource is immediately protected by L402 and listed in Catalogue.
4. **Auditing:** Purchases appear in AG Grid financial ledger with revenue tracking.

---

## 16. Installation, Environment & Execution Runbook

### 16.1 Prerequisites
- Python 3.11, 3.12, or 3.13
- Node.js 18+ and npm 9+
- PayPal Developer Account (Sandbox Client ID & Secret)

### 16.2 Environment Setup (`.env`)
```env
APP_ENV=development
APP_BASE_URL=http://localhost:8000
FRONTEND_URL=http://localhost:3000
SECRET_KEY=paymesh-ai-development-secret-key-32-chars-min
ACCESS_TOKEN_TTL_MINUTES=60
PAYMENT_CHALLENGE_TTL_MINUTES=10
LOG_LEVEL=INFO

DATABASE_URL=sqlite+aiosqlite:///./paymesh.db

PAYPAL_ENVIRONMENT=sandbox
PAYPAL_CLIENT_ID=your-paypal-sandbox-client-id
PAYPAL_CLIENT_SECRET=your-paypal-sandbox-client-secret
PAYPAL_WEBHOOK_ID=70X74465B0704404B

AI_PROVIDER=gemini
AI_API_KEY=your-gemini-api-key
AI_MODEL=gemini-2.5-flash

CHANNEL3_API_KEY=your-channel3-key

MONGODB_URI=mongodb+srv://user:pass@cluster0.mfzju4v.mongodb.net/cohesora?retryWrites=true&w=majority
MONGODB_AI_ENDPOINT=https://ai.mongodb.com
MONGODB_MODEL_API_KEY=your-mongodb-model-api-key

NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_PAYPAL_CLIENT_ID=your-paypal-sandbox-client-id
```

### 16.3 Step-by-Step Execution
```bash
# 1. Install backend dependencies
pip install -r requirements.txt

# 2. Install frontend dependencies & build
cd frontend
npm install
npm run build
cd ..

# 3. Start backend server (Terminal 1)
python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000

# 4. Start frontend development server (Terminal 2)
npm --prefix frontend run dev
```

---

## 17. Testing, Quality Assurance & Verification Results

### 17.1 Pytest Suite Execution (28/28 Passing)
```bash
python -m pytest backend/tests -v
```

```text
============================= test session starts =============================
platform win32 -- Python 3.13.1, pytest-9.0.3, pluggy-1.6.0
collected 28 items

backend/tests/integration/test_api_endpoints.py::test_health_endpoint PASSED              [  3%]
backend/tests/integration/test_api_endpoints.py::test_catalogue_endpoint PASSED           [  7%]
backend/tests/integration/test_api_endpoints.py::test_protected_resource_returns_402_challenge PASSED [ 10%]
backend/tests/integration/test_api_endpoints.py::test_full_payment_capture_and_retrieval_flow PASSED [ 14%]
backend/tests/integration/test_api_endpoints.py::test_agent_run_orchestration PASSED      [ 17%]
backend/tests/integration/test_api_endpoints.py::test_mcp_manifest_and_tool_execution PASSED [ 21%]
backend/tests/integration/test_api_endpoints.py::test_legacy_bot_l402_and_payment_flow PASSED [ 25%]
backend/tests/integration/test_api_endpoints.py::test_security_headers_enforced PASSED   [ 28%]
backend/tests/integration/test_api_endpoints.py::test_publisher_validation_rejects_invalid_currency PASSED [ 32%]
backend/tests/integration/test_api_endpoints.py::test_agent_orchestration_returns_ai_metadata PASSED [ 35%]
backend/tests/integration/test_api_endpoints.py::test_paypal_webhook_handler PASSED      [ 39%]
backend/tests/integration/test_api_endpoints.py::test_policy_config_get_and_update PASSED [ 42%]
backend/tests/unit/test_ai_agent.py::test_discover_resources_args_validation PASSED       [ 46%]
backend/tests/unit/test_ai_agent.py::test_get_resource_offer_args_validation PASSED       [ 50%]
backend/tests/unit/test_ai_agent.py::test_evaluate_purchase_policy_args_validation PASSED [ 53%]
backend/tests/unit/test_ai_agent.py::test_llm_client_unconfigured_by_default PASSED      [ 57%]
backend/tests/unit/test_ai_agent.py::test_llm_client_execute_unknown_tool PASSED         [ 60%]
backend/tests/unit/test_ai_agent.py::test_orchestrator_returns_structured_trace PASSED   [ 64%]
backend/tests/unit/test_config_and_security.py::test_settings_properties PASSED          [ 67%]
backend/tests/unit/test_config_and_security.py::test_token_hashing_and_verification PASSED [ 71%]
backend/tests/unit/test_config_and_security.py::test_challenge_id_format PASSED          [ 75%]
backend/tests/unit/test_config_and_security.py::test_password_hashing PASSED             [ 78%]
backend/tests/unit/test_policy.py::test_policy_within_budget PASSED                       [ 82%]
backend/tests/unit/test_policy.py::test_policy_exceeds_budget PASSED                      [ 85%]
backend/tests/unit/test_policy.py::test_policy_currency_mismatch PASSED                  [ 89%]
backend/tests/unit/test_policy.py::test_policy_inactive_offer PASSED                      [ 92%]
backend/tests/unit/test_policy.py::test_policy_disallowed_currency PASSED                 [ 96%]
backend/tests/unit/test_policy.py::test_policy_exceeds_platform_ceiling PASSED            [100%]

============================= 28 passed in 45.73s =============================
```

### 17.2 End-to-End Smoke Test Execution (7/7 Steps Passing)
```bash
python scripts/smoke_test.py http://localhost:8000
```
- Step 1: `/health` -> PASS (Database connected, MongoDB Atlas connected)
- Step 2: `/api/v1/catalogue` -> PASS (Discovered resources)
- Step 3: `HTTP 402 Challenge` -> PASS (L402 challenge generated)
- Step 4: `/api/v1/payment-sessions` -> PASS (PayPal Sandbox Order created)
- Step 5: `/capture` -> PASS (Captured & Bearer token issued)
- Step 6: Authenticated retrieval -> PASS (Decrypted intelligence returned)
- Step 7: `/publisher/analytics/summary` -> PASS (Revenue updated)

---

## 18. Project Status & Production Roadmap

### 18.1 Implemented & Verified Capabilities
- [x] L402 HTTP 402 Challenge Envelope engine.
- [x] PayPal Orders v2 Sandbox OAuth, Order creation, and capture.
- [x] Asynchronous PayPal Webhook notification handler (`70X74465B0704404B`).
- [x] Deterministic spending policy engine with dynamic runtime update API.
- [x] MongoDB Atlas audit event mirroring (`auditevents` collection).
- [x] Google Gemini 2.5 Flash live inference integration.
- [x] AG Grid Community v32 financial settlement ledger with CSV export.
- [x] Model Context Protocol (MCP) tool manifest server.
- [x] Channel3 Product Intelligence client integration.
- [x] Remotion 1080p programmatic video pitch render.
- [x] Vercel frontend & Render backend live cloud deployment.

### 18.2 Future Roadmap
- [ ] Multi-currency FX auto-hedging via PayPal Conversion APIs.
- [ ] Decentralized DID (Decentralized Identity) credentials for autonomous multi-agent swarms.
- [ ] Hardware Secure Enclave (HSM) signing for enterprise procurement keys.

