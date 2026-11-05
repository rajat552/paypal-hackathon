from typing import Any

from fastapi import HTTPException, status


class PayMeshException(Exception):
    def __init__(self, message: str, code: str = "INTERNAL_ERROR", details: Any | None = None):
        super().__init__(message)
        self.message = message
        self.code = code
        self.details = details

# Backwards-compatibility alias for legacy code
CrawlerPalException = PayMeshException

class PaymentRequiredException(HTTPException):
    def __init__(self, challenge_payload: dict):
        super().__init__(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail=challenge_payload
        )

class PolicyViolationException(PayMeshException):
    def __init__(self, reason: str, details: Any | None = None):
        super().__init__(message=f"Purchase policy violation: {reason}", code="POLICY_VIOLATION", details=details)

class InvalidChallengeException(PayMeshException):
    def __init__(self, reason: str):
        super().__init__(message=f"Invalid or expired challenge: {reason}", code="INVALID_CHALLENGE")

class PayPalApiException(PayMeshException):
    def __init__(self, message: str, details: Any | None = None):
        super().__init__(message=f"PayPal API error: {message}", code="PAYPAL_API_ERROR", details=details)

