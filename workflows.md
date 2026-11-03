# CrawlerPal 2.0 — Agentic Data Commerce Gateway

> **Engineering execution plan for the PayPal AI Hackathon 2026**  
> **Document type:** Product, architecture, implementation, verification, deployment, and submission workflow  
> **Baseline:** `positiveblue/CrawlerPal` plus the supplied `detailed.md` project brief  
> **Prepared:** 2 November 2026  
> **Target submission deadline:** 13 November 2026, 1:30 AM IST (equivalent to 12 November 2026, 12:00 PM Pacific Time, as displayed in the official Devpost rules)

---

## 0. How to Execute This Document

This file is the implementation contract for the project. It is not a claim that the changes described below have already been implemented. Work through the phases in order, keep the repository runnable after every phase, and do not mark a phase complete until its acceptance criteria have been demonstrated.

### Engineering rules

1. **Audit before editing.** Inspect the actual repository, dependencies, route behaviour, environment variables, assets, and Git history before changing or deleting anything.
2. **Preserve working behaviour until replacement is verified.** Migrate one vertical slice at a time. Do not remove the existing CLI or server until the new equivalent path passes its tests.
3. **No mock success.** A successful payment must be backed by a PayPal Sandbox order that has been approved and captured, then independently verified by the server. A UI animation or a fabricated `COMPLETED` response is not a payment integration.
4. **The LLM is not the payment authority.** AI can interpret the request, recommend a resource, and explain an offer. Deterministic backend policy and explicit buyer approval govern spending, order creation, capture, and entitlement issuance.
5. **One source of truth for money.** Prices, currency, scope, limits, and product IDs are resolved by the backend from persisted records. Never trust a client- or LLM-supplied amount.
6. **Use sponsor technology in a real user journey.** A sponsor logo, a README mention, or an unused dependency does not count as meaningful integration.
7. **Verify before committing.** Each implementation step must include the relevant automated checks and at least one manual end-to-end check where appropriate.
8. **Commit in small, reversible units.** Use feature branches and descriptive commits. Do not push secrets, generated databases, local credentials, or private user data.
9. **Do not invent repository facts.** If the code differs from this audit, update this document and the implementation plan based on the code that is actually present.
10. **Keep a deadline buffer.** Feature work must stop early enough to test the deployed build, record the video, and submit to Devpost before the deadline.

---

## 1. Hackathon Requirements and Product Strategy

### 1.1 Challenge requirements

The project is being updated for **PayPal AI Hackathon 2026 — “Build what’s next with PayPal and AI.”** The core requirement is a functional application that meaningfully integrates:

- At least one PayPal Developer Platform technology, API, SDK, or product, using the PayPal Sandbox for the hackathon prototype.
- An AI model, tool, agent framework, or AI platform that contributes to the actual user experience or application functionality.
- A working prototype or proof of concept. A static design, slide deck, or non-functional mockup is not sufficient.
- A public source-code repository with all code, assets, configuration templates, and run instructions required to operate the project.
- An open-source licence file in the public repository. The rights to every reused source file and asset must be clear.
- A functional demo, supplied as either a hosted application or complete, reproducible local setup instructions.
- A public YouTube demo video under three minutes, linked in the Devpost submission.
- A text description that clearly explains the problem, intended audience, product workflow, and technology use.

The judging criteria supplied on Devpost are:
- Technological Implementation
- Design
- Potential Impact
- Innovation / Idea
- Presentation

---

## 2. Baseline Audit: What CrawlerPal Already Has and What Must Change
(See detailed tasks in Section 13)

---

## 3. Target User Journeys and Functional Scope
- Publisher Console
- AI Buyer Workspace
- L402 Access Control & Entitlement
- PayPal Sandbox Orders v2 Lifecycle

---

## 4. Target Architecture & Components
- Frontend: Next.js / React + TypeScript + Tailwind CSS + AG Grid
- Backend: FastAPI, SQLAlchemy 2, Alembic, Pydantic v2
- PayPal Sandbox API Client & Gateway
- AI Agent & MCP Server (Model Context Protocol)
- Channel3 Product Data Client

---

## 5. Detailed 10 Phases
Phase 1: Repository Forensics, Ownership, and Baseline Stabilisation
Phase 2: Product Definition, UX, and Technical Contracts
Phase 3: Backend Foundation, Database, and Configuration
Phase 4: Resource Catalogue and Channel3 Product-Data Integration
Phase 5: L402 Challenge, Protected Resources, and Entitlements
Phase 6: PayPal Sandbox Checkout and Transaction Ledger
Phase 7: AI Agent, Policy Engine, and MCP
Phase 8: Frontend Product Experience and AG Grid Analytics
Phase 9: Quality Assurance, Security, CI, and Render Deployment
Phase 10: Release Hardening, Documentation, Demo, and Devpost Submission
