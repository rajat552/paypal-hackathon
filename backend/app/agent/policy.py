import json
from datetime import UTC, datetime, timedelta
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models.entities import Offer, PolicySetting, Transaction

DEFAULT_ALLOWED_CURRENCIES = {"USD", "EUR", "GBP"}
DEFAULT_DAILY_CAP = 50.0
DEFAULT_MAX_SINGLE_TX_LIMIT = 25.0


class PolicyEngine:
    def __init__(self):
        self.allowed_currencies: set[str] = set(DEFAULT_ALLOWED_CURRENCIES)
        self.daily_cap: float = 5.00
        self.max_single_tx_limit: float = DEFAULT_MAX_SINGLE_TX_LIMIT
        self.auto_approve_under: float = 0.00
        self.enforce_prompt_sanitization: bool = True
        self.strict_scope_check: bool = True

    async def sync_from_db(self, session: AsyncSession) -> PolicySetting:
        """Load persistent policy limits from database, seeding defaults if needed."""
        stmt = select(PolicySetting).where(PolicySetting.id == "global")
        res = await session.execute(stmt)
        record = res.scalars().first()

        if not record:
            record = PolicySetting(
                id="global",
                max_per_transaction=self.max_single_tx_limit,
                daily_cap=self.daily_cap,
                allowed_currencies_json=json.dumps(sorted(self.allowed_currencies)),
                auto_approve_under=self.auto_approve_under,
                enforce_prompt_sanitization=self.enforce_prompt_sanitization,
                strict_scope_check=self.strict_scope_check
            )
            session.add(record)
            await session.commit()
            await session.refresh(record)

        self.max_single_tx_limit = float(record.max_per_transaction)
        self.daily_cap = float(record.daily_cap)
        try:
            self.allowed_currencies = set(json.loads(record.allowed_currencies_json))
        except Exception:  # noqa: BLE001
            self.allowed_currencies = set(DEFAULT_ALLOWED_CURRENCIES)
        self.auto_approve_under = float(record.auto_approve_under)
        self.enforce_prompt_sanitization = bool(record.enforce_prompt_sanitization)
        self.strict_scope_check = bool(record.strict_scope_check)
        return record

    async def save_to_db(
        self,
        session: AsyncSession,
        max_per_transaction: float,
        daily_cap: float,
        allowed_currencies: list[str],
        auto_approve_under: float = 0.0,
        enforce_prompt_sanitization: bool = True,
        strict_scope_check: bool = True
    ) -> PolicySetting:
        """Persist updated spending policy configuration in the database."""
        stmt = select(PolicySetting).where(PolicySetting.id == "global")
        res = await session.execute(stmt)
        record = res.scalars().first()

        clean_currencies = sorted(list({c.upper().strip() for c in allowed_currencies if c.strip()}))
        if not record:
            record = PolicySetting(
                id="global",
                max_per_transaction=max_per_transaction,
                daily_cap=daily_cap,
                allowed_currencies_json=json.dumps(clean_currencies),
                auto_approve_under=auto_approve_under,
                enforce_prompt_sanitization=enforce_prompt_sanitization,
                strict_scope_check=strict_scope_check
            )
            session.add(record)
        else:
            record.max_per_transaction = max_per_transaction
            record.daily_cap = daily_cap
            record.allowed_currencies_json = json.dumps(clean_currencies)
            record.auto_approve_under = auto_approve_under
            record.enforce_prompt_sanitization = enforce_prompt_sanitization
            record.strict_scope_check = strict_scope_check

        await session.commit()
        await session.refresh(record)

        # Update in-memory state
        self.max_single_tx_limit = float(record.max_per_transaction)
        self.daily_cap = float(record.daily_cap)
        self.allowed_currencies = set(clean_currencies)
        self.auto_approve_under = float(record.auto_approve_under)
        self.enforce_prompt_sanitization = bool(record.enforce_prompt_sanitization)
        self.strict_scope_check = bool(record.strict_scope_check)
        return record

    def evaluate(
        self,
        offer: Offer,
        budget_limit: float,
        currency: str = "USD"
    ) -> tuple[bool, str]:
        """Deterministic policy validation for single-transaction rules."""
        if not offer.active:
            return False, "Offer is currently inactive."

        curr_upper = currency.upper().strip()
        offer_curr_upper = offer.currency.upper().strip()

        if offer_curr_upper not in self.allowed_currencies:
            return False, f"Offer currency '{offer.currency}' is not in allowed currency policy list: {sorted(self.allowed_currencies)}."

        if curr_upper != offer_curr_upper:
            return False, f"Currency mismatch: offer requires {offer.currency}, buyer specified {currency}."

        offer_amount = float(offer.price_amount)
        if offer_amount <= 0:
            return False, "Invalid price amount: price must be greater than zero."

        if offer_amount > self.max_single_tx_limit:
            return False, f"Price ${offer_amount:.2f} exceeds absolute platform safety ceiling of ${self.max_single_tx_limit:.2f}."

        if offer_amount > budget_limit:
            return False, f"Price exceeds buyer budget limit: ${offer_amount:.2f} > max budget ${budget_limit:.2f}."

        return True, f"Policy passed: ${offer_amount:.2f} is within budget limit of ${budget_limit:.2f}."

    async def evaluate_with_rolling_budget(
        self,
        session: AsyncSession,
        offer: Offer,
        budget_limit: float,
        currency: str = "USD",
        daily_cap: float | None = None
    ) -> tuple[bool, str, dict[str, Any]]:
        """Evaluate spending policy including 24-hour rolling cumulative spend."""
        # Ensure fresh policy limits from database
        try:
            await self.sync_from_db(session)
        except Exception:  # noqa: BLE001
            pass  # Fall back to in-memory defaults if table not yet initialized in early migration

        cap_to_use = daily_cap if daily_cap is not None else self.daily_cap
        allowed, reason = self.evaluate(offer, budget_limit, currency)
        if not allowed:
            return False, reason, {"rolling_spent": 0.0, "daily_cap": cap_to_use}

        # Calculate total settled spend in the last 24 hours
        cutoff = datetime.now(UTC) - timedelta(hours=24)
        stmt = select(func.coalesce(func.sum(Transaction.gross_amount), 0.0)).where(
            Transaction.captured_at >= cutoff,
            Transaction.payment_status == "COMPLETED"
        )
        res = await session.execute(stmt)
        rolling_spent_dec = res.scalar() or 0.0
        rolling_spent = float(rolling_spent_dec)

        offer_amount = float(offer.price_amount)
        projected_spend = rolling_spent + offer_amount

        if projected_spend > cap_to_use:
            msg = (
                f"Rolling 24-hour budget exceeded: current spend ${rolling_spent:.2f} + ${offer_amount:.2f} "
                f"would exceed 24h cap of ${cap_to_use:.2f}."
            )
            return False, msg, {"rolling_spent": rolling_spent, "daily_cap": cap_to_use, "projected_spend": projected_spend}

        return True, reason, {
            "rolling_spent": rolling_spent,
            "daily_cap": cap_to_use,
            "projected_spend": projected_spend,
            "remaining_allowance": cap_to_use - projected_spend
        }


policy_engine = PolicyEngine()
