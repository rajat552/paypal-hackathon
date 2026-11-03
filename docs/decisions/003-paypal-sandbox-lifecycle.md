# ADR 003: PayPal Sandbox Lifecycle and Capture Verification

## Status
Accepted

## Context
Payment operations must be robust, secure, and verifiable against PayPal Sandbox APIs. The backend must be the sole authority on payment state.

## Decisions
1. **OAuth 2.0 Client Credentials**:
   - The server authenticates against `https://api-m.sandbox.paypal.com/v1/oauth2/token` using HTTP Basic Auth (`PAYPAL_CLIENT_ID` and `PAYPAL_CLIENT_SECRET`).
   - Access tokens are cached in memory with proactive refresh 60 seconds before expiry.
2. **Order Creation (`intent: CAPTURE`)**:
   - The order creation payload is constructed purely from server-resolved database offer details.
   - Idempotency is enforced via `PayPal-Request-Id` and persisted `payment_sessions`.
   - Returns the PayPal approval URL (`approve` rel link) to the client.
3. **Capture & Server-Side Verification**:
   - After buyer approval in PayPal Sandbox, the client triggers the backend capture endpoint.
   - The backend makes the POST request to `/v2/checkout/orders/{id}/capture` using server OAuth credentials.
   - The capture response is strictly validated: status must be `COMPLETED`, currency and amount must match the recorded offer, and the captured order ID must match the internal session.
   - Upon verification, a `transactions` record and an `entitlements` record are created atomically.
   - Duplicate capture requests are idempotent and return the existing verified result.
