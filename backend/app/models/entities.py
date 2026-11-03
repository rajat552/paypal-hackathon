import uuid
from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import (
    String, Text, Boolean, Integer, Numeric, DateTime, ForeignKey, Index
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.db.base import Base

def utc_now() -> datetime:
    return datetime.now(timezone.utc)

def generate_uuid() -> str:
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(32), default="publisher") # publisher, buyer, admin
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

    resources: Mapped[list["Resource"]] = relationship("Resource", back_populates="publisher")
    agents: Mapped[list["Agent"]] = relationship("Agent", back_populates="owner")

class Agent(Base):
    __tablename__ = "agents"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    owner_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    api_key_hash: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="active")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

    owner: Mapped["User"] = relationship("User", back_populates="agents")
    entitlements: Mapped[list["Entitlement"]] = relationship("Entitlement", back_populates="agent")

class Resource(Base):
    __tablename__ = "resources"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    publisher_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=False)
    slug: Mapped[str] = mapped_column(String(128), unique=True, index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    resource_type: Mapped[str] = mapped_column(String(64), default="product_intelligence") # news, product_intelligence, dataset
    provider: Mapped[str] = mapped_column(String(64), default="channel3") # channel3, crawlerpal_demo
    status: Mapped[str] = mapped_column(String(32), default="active")
    metadata_json: Mapped[str] = mapped_column(Text, default="{}")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

    publisher: Mapped["User"] = relationship("User", back_populates="resources")
    offers: Mapped[list["Offer"]] = relationship("Offer", back_populates="resource", cascade="all, delete-orphan")
    entitlements: Mapped[list["Entitlement"]] = relationship("Entitlement", back_populates="resource")

class Offer(Base):
    __tablename__ = "offers"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    resource_id: Mapped[str] = mapped_column(String(36), ForeignKey("resources.id"), nullable=False)
    offer_code: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    price_amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="USD", nullable=False)
    pricing_model: Mapped[str] = mapped_column(String(32), default="one_time") # one_time, subscription, pay_per_call
    scope_json: Mapped[str] = mapped_column(Text, default='{"access": "read"}')
    duration_seconds: Mapped[int] = mapped_column(Integer, default=3600) # 1 hour
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

    resource: Mapped["Resource"] = relationship("Resource", back_populates="offers")

class PaymentChallenge(Base):
    __tablename__ = "payment_challenges"

    id: Mapped[str] = mapped_column(String(64), primary_key=True) # e.g. chl_...
    agent_id: Mapped[Optional[str]] = mapped_column(String(36), nullable=True)
    resource_id: Mapped[str] = mapped_column(String(36), ForeignKey("resources.id"), nullable=False)
    offer_id: Mapped[str] = mapped_column(String(36), ForeignKey("offers.id"), nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="USD", nullable=False)
    scope_json: Mapped[str] = mapped_column(Text, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="PENDING") # PENDING, CONSUMED, EXPIRED
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

class PaymentSession(Base):
    __tablename__ = "payment_sessions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    challenge_id: Mapped[str] = mapped_column(String(64), ForeignKey("payment_challenges.id"), nullable=False)
    agent_id: Mapped[Optional[str]] = mapped_column(String(36), nullable=True)
    paypal_order_id: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    paypal_request_id: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    approval_url: Mapped[str] = mapped_column(Text, nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="USD", nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="CREATED") # CREATED, APPROVED, CAPTURED, FAILED, CANCELLED
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)

class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    payment_session_id: Mapped[str] = mapped_column(String(36), ForeignKey("payment_sessions.id"), nullable=False)
    paypal_order_id: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    paypal_capture_id: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    gross_amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="USD", nullable=False)
    payment_status: Mapped[str] = mapped_column(String(32), default="COMPLETED", nullable=False)
    payer_reference_hash: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    captured_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    raw_summary_json: Mapped[str] = mapped_column(Text, default="{}")

class Entitlement(Base):
    __tablename__ = "entitlements"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    agent_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("agents.id"), nullable=True)
    resource_id: Mapped[str] = mapped_column(String(36), ForeignKey("resources.id"), nullable=False)
    offer_id: Mapped[str] = mapped_column(String(36), ForeignKey("offers.id"), nullable=False)
    token_hash: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    scope_json: Mapped[str] = mapped_column(Text, nullable=False)
    starts_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    revoked_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[str] = mapped_column(String(32), default="ACTIVE") # ACTIVE, EXPIRED, REVOKED

    agent: Mapped[Optional["Agent"]] = relationship("Agent", back_populates="entitlements")
    resource: Mapped["Resource"] = relationship("Resource", back_populates="entitlements")

class UsageEvent(Base):
    __tablename__ = "usage_events"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    agent_id: Mapped[Optional[str]] = mapped_column(String(36), nullable=True)
    resource_id: Mapped[str] = mapped_column(String(36), nullable=False)
    entitlement_id: Mapped[str] = mapped_column(String(36), nullable=False)
    event_type: Mapped[str] = mapped_column(String(32), default="read_content")
    units: Mapped[int] = mapped_column(Integer, default=1)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    actor_type: Mapped[str] = mapped_column(String(32)) # system, agent, buyer, publisher
    actor_id: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    action: Mapped[str] = mapped_column(String(64), nullable=False)
    entity_type: Mapped[str] = mapped_column(String(64), nullable=False)
    entity_id: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    metadata_json: Mapped[str] = mapped_column(Text, default="{}")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

class ProductSnapshot(Base):
    __tablename__ = "product_snapshots"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    provider: Mapped[str] = mapped_column(String(32), default="channel3")
    provider_item_id: Mapped[str] = mapped_column(String(128), index=True, nullable=False)
    query_hash: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    payload_json: Mapped[str] = mapped_column(Text, nullable=False)
    fetched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
