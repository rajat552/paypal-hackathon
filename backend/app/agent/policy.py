from typing import Tuple, Optional
from backend.app.models.entities import Offer

class PolicyEngine:
    @staticmethod
    def evaluate(
        offer: Offer,
        budget_limit: float,
        currency: str = "USD"
    ) -> Tuple[bool, str]:
        """Deterministic policy validation. LLM cannot override this rule."""
        if not offer.active:
            return False, "Offer is currently inactive."

        if offer.currency.upper() != currency.upper():
            return False, f"Currency mismatch: offer requires {offer.currency}, buyer specified {currency}."

        offer_amount = float(offer.price_amount)
        if offer_amount > budget_limit:
            return False, f"Price exceeds buyer budget limit: ${offer_amount:.2f} > max budget ${budget_limit:.2f}."

        if offer_amount <= 0:
            return False, "Invalid price amount."

        return True, f"Policy passed: ${offer_amount:.2f} is within budget limit of ${budget_limit:.2f}."

policy_engine = PolicyEngine()

