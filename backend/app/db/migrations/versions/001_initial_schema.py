"""Initial schema migration for PayMesh AI

Revision ID: 001_initial_schema
Revises: 
Create Date: 2026-11-02 00:00:00.000000

"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = '001_initial_schema'
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

def upgrade() -> None:
    # users
    op.create_table(
        'users',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('email', sa.String(length=255), nullable=False, unique=True),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('role', sa.String(length=32), server_default='publisher'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False)
    )

    # agents
    op.create_table(
        'agents',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('owner_id', sa.String(length=36), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('name', sa.String(length=128), nullable=False),
        sa.Column('api_key_hash', sa.String(length=64), nullable=False, index=True),
        sa.Column('status', sa.String(length=32), server_default='active'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False)
    )

    # resources
    op.create_table(
        'resources',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('publisher_id', sa.String(length=36), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('slug', sa.String(length=128), nullable=False, unique=True, index=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('resource_type', sa.String(length=64), server_default='product_intelligence'),
        sa.Column('provider', sa.String(length=64), server_default='channel3'),
        sa.Column('status', sa.String(length=32), server_default='active'),
        sa.Column('metadata_json', sa.Text(), server_default='{}'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False)
    )

    # offers
    op.create_table(
        'offers',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('resource_id', sa.String(length=36), sa.ForeignKey('resources.id'), nullable=False),
        sa.Column('offer_code', sa.String(length=64), nullable=False, index=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('price_amount', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('currency', sa.String(length=3), server_default='USD', nullable=False),
        sa.Column('pricing_model', sa.String(length=32), server_default='one_time'),
        sa.Column('scope_json', sa.Text(), server_default='{"access": "read"}'),
        sa.Column('duration_seconds', sa.Integer(), server_default='3600'),
        sa.Column('active', sa.Boolean(), server_default='1'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False)
    )

    # payment_challenges
    op.create_table(
        'payment_challenges',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('agent_id', sa.String(length=36), nullable=True),
        sa.Column('resource_id', sa.String(length=36), sa.ForeignKey('resources.id'), nullable=False),
        sa.Column('offer_id', sa.String(length=36), sa.ForeignKey('offers.id'), nullable=False),
        sa.Column('amount', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('currency', sa.String(length=3), server_default='USD', nullable=False),
        sa.Column('scope_json', sa.Text(), nullable=False),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('status', sa.String(length=32), server_default='PENDING'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False)
    )

    # payment_sessions
    op.create_table(
        'payment_sessions',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('challenge_id', sa.String(length=64), sa.ForeignKey('payment_challenges.id'), nullable=False),
        sa.Column('agent_id', sa.String(length=36), nullable=True),
        sa.Column('paypal_order_id', sa.String(length=64), nullable=False, unique=True, index=True),
        sa.Column('paypal_request_id', sa.String(length=64), nullable=False, unique=True),
        sa.Column('approval_url', sa.Text(), nullable=False),
        sa.Column('amount', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('currency', sa.String(length=3), server_default='USD', nullable=False),
        sa.Column('status', sa.String(length=32), server_default='CREATED'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False)
    )

    # transactions
    op.create_table(
        'transactions',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('payment_session_id', sa.String(length=36), sa.ForeignKey('payment_sessions.id'), nullable=False),
        sa.Column('paypal_order_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('paypal_capture_id', sa.String(length=64), nullable=False, unique=True, index=True),
        sa.Column('gross_amount', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('currency', sa.String(length=3), server_default='USD', nullable=False),
        sa.Column('payment_status', sa.String(length=32), server_default='COMPLETED', nullable=False),
        sa.Column('payer_reference_hash', sa.String(length=64), nullable=True),
        sa.Column('captured_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('raw_summary_json', sa.Text(), server_default='{}')
    )

    # entitlements
    op.create_table(
        'entitlements',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('agent_id', sa.String(length=36), sa.ForeignKey('agents.id'), nullable=True),
        sa.Column('resource_id', sa.String(length=36), sa.ForeignKey('resources.id'), nullable=False),
        sa.Column('offer_id', sa.String(length=36), sa.ForeignKey('offers.id'), nullable=False),
        sa.Column('token_hash', sa.String(length=64), nullable=False, unique=True, index=True),
        sa.Column('scope_json', sa.Text(), nullable=False),
        sa.Column('starts_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('revoked_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('status', sa.String(length=32), server_default='ACTIVE')
    )

    # usage_events
    op.create_table(
        'usage_events',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('agent_id', sa.String(length=36), nullable=True),
        sa.Column('resource_id', sa.String(length=36), nullable=False),
        sa.Column('entitlement_id', sa.String(length=36), nullable=False),
        sa.Column('event_type', sa.String(length=32), server_default='read_content'),
        sa.Column('units', sa.Integer(), server_default='1'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False)
    )

    # audit_logs
    op.create_table(
        'audit_logs',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('actor_type', sa.String(length=32), nullable=False),
        sa.Column('actor_id', sa.String(length=64), nullable=True),
        sa.Column('action', sa.String(length=64), nullable=False),
        sa.Column('entity_type', sa.String(length=64), nullable=False),
        sa.Column('entity_id', sa.String(length=64), nullable=True),
        sa.Column('metadata_json', sa.Text(), server_default='{}'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False)
    )

    # product_snapshots
    op.create_table(
        'product_snapshots',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('provider', sa.String(length=32), server_default='channel3'),
        sa.Column('provider_item_id', sa.String(length=128), nullable=False, index=True),
        sa.Column('query_hash', sa.String(length=64), nullable=False, index=True),
        sa.Column('payload_json', sa.Text(), nullable=False),
        sa.Column('fetched_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False)
    )

def downgrade() -> None:
    op.drop_table('product_snapshots')
    op.drop_table('audit_logs')
    op.drop_table('usage_events')
    op.drop_table('entitlements')
    op.drop_table('transactions')
    op.drop_table('payment_sessions')
    op.drop_table('payment_challenges')
    op.drop_table('offers')
    op.drop_table('resources')
    op.drop_table('agents')
    op.drop_table('users')

