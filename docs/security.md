# PayMesh AI Security & Access Control

## 1. Threat Model & Security Boundaries
- **No Client-Side Price Tampering**: Amounts, currency, publisher IDs, and entitlement durations are strictly resolved from server database records.
- **No LLM Payment Authority**: The AI model recommends resources and formats summaries; it has zero capability to capture payments or modify amounts.
- **Cryptographic Separation**: Challenge IDs (`chl_...`), PayPal Order IDs, and Bearer Tokens (`pm_live_...`) are distinct. Bearer tokens are cryptographically random strings with only HMAC-SHA256 hashes stored in the database.
- **Deterministic Policy Enforcement**: Evaluates spending limit, currency validity, offer expiration, and duplicate challenge status before initiating payment.
- **Redaction**: Access tokens, PayPal secret keys, and raw customer PII are redacted from structured logs.
- **SSRF & Data Injection Prevention**: Provider integrations use strict schemas, parameter validation, and avoid arbitrary URL fetching.
