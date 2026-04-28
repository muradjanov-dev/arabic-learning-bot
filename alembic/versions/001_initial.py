"""Initial schema

Revision ID: 001
Revises:
Create Date: 2026-01-01
"""
from alembic import op
import sqlalchemy as sa

revision = "001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Tables are auto-created by SQLAlchemy on startup.
    # This migration is a no-op placeholder for Alembic tracking.
    pass


def downgrade() -> None:
    pass
