import uuid
import time
import httpx
from datetime import datetime, timezone
from typing import Dict, Any, Optional, Tuple
from backend.app.core.config import settings
from backend.app.core.logging import logger
from backend.app.core.exceptions import PayPalApiException

class PayPalGateway:
    def __init__(self):
        self._access_token: Optional[str] = None
        self._token_expires_at: float = 0.0

    @property
    def is_configured(self) -> bool:
        return (
            bool(settings.PAYPAL_CLIENT_ID)
            and settings.PAYPAL_CLIENT_ID != "replace-with-sandbox-client-id"
            and settings.PAYPAL_CLIENT_ID != "sandbox_client_id_placeholder"
            and bool(settings.PAYPAL_CLIENT_SECRET)
            and settings.PAYPAL_CLIENT_SECRET != "replace-with-sandbox-client-secret"
            and settings.PAYPAL_CLIENT_SECRET != "sandbox_client_secret_placeholder"
        )

    async def get_access_token(self) -> str:
        """Fetch and cache OAuth 2.0 bearer token using client credentials."""
        now = time.time()
        if self._access_token and now < (self._token_expires_at - 60):
            return self._access_token

        if not self.is_configured:
            # Deterministic sandbox mock token for unit tests/dry-runs
            self._access_token = f"sandbox_simulated_token_{uuid.uuid4().hex[:8]}"
            self._token_expires_at = now + 3600
            return self._access_token

        auth_url = f"{settings.paypal_base_url}/v1/oauth2/token"
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                resp = await client.post(
                    auth_url,
                    auth=(settings.PAYPAL_CLIENT_ID, settings.PAYPAL_CLIENT_SECRET),
                    data={"grant_type": "client_credentials"},
                    headers={"Accept": "application/json", "Accept-Language": "en_US"}
                )
                if resp.status_code != 200:
                    raise PayPalApiException(f"Failed to obtain OAuth token from PayPal: {resp.text}")
                
                data = resp.json()
                self._access_token = data["access_token"]
                expires_in = data.get("expires_in", 32400)
                self._token_expires_at = now + expires_in
                logger.info("Successfully fetched fresh PayPal Sandbox OAuth access token.")
                return self._access_token
        except Exception as e:
            if isinstance(e, PayPalApiException):
                raise
            raise PayPalApiException(f"Network error during PayPal OAuth: {str(e)}")

    async def create_order(
        self,
        amount: float,
        currency: str,
        session_id: str,
        return_url: Optional[str] = None,
        cancel_url: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a PayPal Sandbox order with intent: CAPTURE."""
        ret_url = return_url or f"{settings.FRONTEND_URL}/checkout/success?session_id={session_id}"
        cnc_url = cancel_url or f"{settings.FRONTEND_URL}/checkout/cancel?session_id={session_id}"
        formatted_amount = f"{amount:.2f}"

        if not self.is_configured:
            # Deterministic sandbox simulation mode
            simulated_order_id = f"ORDER-SANDBOX-{uuid.uuid4().hex[:8].upper()}"
            simulated_approval_url = f"https://www.sandbox.paypal.com/checkoutnow?token={simulated_order_id}"
            logger.info(f"[SIMULATED SANDBOX] Created PayPal order {simulated_order_id} for amount ${formatted_amount} {currency}")
            return {
                "id": simulated_order_id,
                "status": "CREATED",
                "approval_url": simulated_approval_url
            }

        token = await self.get_access_token()
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
            "PayPal-Request-Id": str(uuid.uuid4())
        }

        payload = {
            "intent": "CAPTURE",
            "purchase_units": [
                {
                    "reference_id": session_id,
                    "description": "PayMesh AI Machine-Readable Data Entitlement",
                    "custom_id": session_id,
                    "amount": {
                        "currency_code": currency,
                        "value": formatted_amount
                    }
                }
            ],
            "application_context": {
                "brand_name": "PayMesh AI Commerce",
                "landing_page": "NO_PREFERENCE",
                "user_action": "PAY_NOW",
                "return_url": ret_url,
                "cancel_url": cnc_url
            }
        }

        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.post(
                f"{settings.paypal_base_url}/v2/checkout/orders",
                headers=headers,
                json=payload
            )
            if resp.status_code not in (200, 201):
                logger.error(f"PayPal order creation failed: {resp.text}")
                raise PayPalApiException(f"PayPal order creation failed: {resp.text}")

            data = resp.json()
            approval_url = None
            for link in data.get("links", []):
                if link.get("rel") == "approve":
                    approval_url = link.get("href")
                    break

            if not approval_url:
                approval_url = f"https://www.sandbox.paypal.com/checkoutnow?token={data['id']}"

            return {
                "id": data["id"],
                "status": data["status"],
                "approval_url": approval_url
            }

    async def capture_order(self, paypal_order_id: str) -> Dict[str, Any]:
        """Capture an approved PayPal order and verify COMPLETED status."""
        if not self.is_configured:
            # Deterministic sandbox simulation mode
            simulated_capture_id = f"CAP-SANDBOX-{uuid.uuid4().hex[:8].upper()}"
            logger.info(f"[SIMULATED SANDBOX] Captured PayPal order {paypal_order_id} with capture ID {simulated_capture_id}")
            return {
                "id": paypal_order_id,
                "status": "COMPLETED",
                "capture_id": simulated_capture_id,
                "raw_response": {"status": "COMPLETED", "capture_id": simulated_capture_id, "simulated": True}
            }

        token = await self.get_access_token()
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
            "PayPal-Request-Id": str(uuid.uuid4())
        }

        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.post(
                f"{settings.paypal_base_url}/v2/checkout/orders/{paypal_order_id}/capture",
                headers=headers
            )
            if resp.status_code not in (200, 201):
                logger.error(f"PayPal order capture failed for order {paypal_order_id}: {resp.text}")
                raise PayPalApiException(f"PayPal order capture failed: {resp.text}")

            data = resp.json()
            order_status = data.get("status")
            if order_status != "COMPLETED":
                raise PayPalApiException(f"Order status is not COMPLETED (status: {order_status})")

            # Extract capture ID from purchase units
            capture_id = None
            purchase_units = data.get("purchase_units", [])
            if purchase_units:
                payments = purchase_units[0].get("payments", {})
                captures = payments.get("captures", [])
                if captures:
                    capture_id = captures[0].get("id")

            if not capture_id:
                capture_id = f"CAP-{paypal_order_id}"

            return {
                "id": paypal_order_id,
                "status": order_status,
                "capture_id": capture_id,
                "raw_response": data
            }

paypal_gateway = PayPalGateway()
