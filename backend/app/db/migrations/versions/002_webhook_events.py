"""add webhook_events table

Revision ID: 002_webhook_events
Revises: 001_initial_schema
Create Date: 2026-11-09 09:10:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = '002_webhook_events'
down_revision = '001_initial_schema'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        'webhook_events',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('event_id', sa.String(length=128), nullable=False, unique=True),
        sa.Column('event_type', sa.String(length=64), nullable=False),
        sa.Column('resource_id', sa.String(length=64), nullable=True),
        sa.Column('summary', sa.String(length=255), nullable=True),
        sa.Column('status', sa.String(length=32), server_default='PROCESSED', nullable=False),
        sa.Column('payload_json', sa.Text(), server_default='{}'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False)
    )
    op.create_index(op.f('ix_webhook_events_event_id'), 'webhook_events', ['event_id'], unique=True)

def downgrade() -> None:
    op.drop_index(op.f('ix_webhook_events_event_id'), table_name='webhook_events')
    op.drop_table('webhook_events')

