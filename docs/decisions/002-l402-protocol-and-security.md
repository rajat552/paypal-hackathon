# ADR 002: PayMesh L402 Protocol Specification and Token Security

## Status
Accepted

## Context
Autonomous agents requesting protected publisher resources must receive clear, machine-readable HTTP 402 Payment Required challenges that specify server-owned pricing, resource metadata, offer IDs, and payment endpoints.

## Decisions
1. **HTTP 402 Challenge Contract**:
   When an unauthorized client requests `/api/v1/resources/{slug}/content`, the server returns status 402 with:
   - `protocol`: "paymesh-l402"
   - `protocol_version`: "1.0"
   - `challenge_id`: Opaque persisted UUID (`chl_...`)
   - `resource`: `{ id, slug, title }`
   - `offers`: List of active server-owned offers with exact price, currency, duration, and scope
   - `payment_endpoint`: Canonical relative or absolute payment session creation URL
   - `expires_at`: ISO UTC timestamp (default TTL 10 minutes)
2. **Challenge Invariants**:
   - Every challenge is persisted in the database with status `PENDING`.
   - Single-use only: once consumed by order creation/capture, it transitions to `CONSUMED`.
   - Expired challenges are rejected immediately.
3. **Bearer Token Issuance**:
   - The bearer token is a separate cryptographically secure token (prefixed `pm_live_...`).
   - Only the HMAC-SHA256 hash is persisted in the `entitlements` table.
   - Tokens carry explicit scope, agent ID, resource ID, and expiry timestamp.
   - Tokens can be explicitly revoked by the publisher or system administrator.
