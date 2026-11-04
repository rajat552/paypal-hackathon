from datetime import UTC, datetime, timedelta
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models.entities import Offer, Transaction

ALLOWED_CURRENCIES = {"USD", "EUR", "GBP"}
DEFAULT_DAILY_CAP = 50.0
MAX_SINGLE_TX_LIMIT = 25.0

class PolicyEngine:
    @staticmethod
    def evaluate(
        offer: Offer,
        budget_limit: float,
        currency: str = "USD"
    ) -> tuple[bool, str]:
        """Deterministic policy validation for single-transaction rules."""
        if not offer.active:
            return False, "Offer is currently inactive."

        curr_upper = currency.upper().strip()
        offer_curr_upper = offer.currency.upper().strip()

        if offer_curr_upper not in ALLOWED_CURRENCIES:
            return False, f"Offer currency '{offer.currency}' is not in allowed currency policy list: {sorted(ALLOWED_CURRENCIES)}."

        if curr_upper != offer_curr_upper:
            return False, f"Currency mismatch: offer requires {offer.currency}, buyer specified {currency}."

        offer_amount = float(offer.price_amount)
        if offer_amount <= 0:
            return False, "Invalid price amount: price must be greater than zero."

        if offer_amount > MAX_SINGLE_TX_LIMIT:
            return False, f"Price ${offer_amount:.2f} exceeds absolute platform safety ceiling of ${MAX_SINGLE_TX_LIMIT:.2f}."

        if offer_amount > budget_limit:
            return False, f"Price exceeds buyer budget limit: ${offer_amount:.2f} > max budget ${budget_limit:.2f}."

        return True, f"Policy passed: ${offer_amount:.2f} is within budget limit of ${budget_limit:.2f}."

    @staticmethod
    async def evaluate_with_rolling_budget(
        session: AsyncSession,
        offer: Offer,
        budget_limit: float,
        currency: str = "USD",
        daily_cap: float = DEFAULT_DAILY_CAP
    ) -> tuple[bool, str, dict[str, Any]]:
        """Evaluate spending policy including 24-hour rolling cumulative spend."""
        allowed, reason = PolicyEngine.evaluate(offer, budget_limit, currency)
        if not allowed:
            return False, reason, {"rolling_spent": 0.0, "daily_cap": daily_cap}

        # Calculate total settled spend in the last 24 hours
        cutoff = datetime.now(UTC) - timedelta(hours=24)
        stmt = select(func.sum(Transaction.gross_amount)).where(
            Transaction.captured_at >= cutoff,
            Transaction.payment_status == "COMPLETED"
        )
        res = await session.execute(stmt)
        rolling_spent_dec = res.scalar() or 0.0
        rolling_spent = float(rolling_spent_dec)

        offer_amount = float(offer.price_amount)
        projected_spend = rolling_spent + offer_amount

        if projected_spend > daily_cap:
            msg = (
                f"Rolling 24-hour budget exceeded: current spend ${rolling_spent:.2f} + ${offer_amount:.2f} "
                f"would exceed 24h cap of ${daily_cap:.2f}."
            )
            return False, msg, {"rolling_spent": rolling_spent, "daily_cap": daily_cap, "projected_spend": projected_spend}

        return True, reason, {
            "rolling_spent": rolling_spent,
            "daily_cap": daily_cap,
            "projected_spend": projected_spend,
            "remaining_allowance": daily_cap - projected_spend
        }

policy_engine = PolicyEngine()
