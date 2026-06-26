"""users table

Revision ID: 0002_users
Revises: 0001_baseline
Create Date: 2026-06-27

Adds the `users` table (Story 1.2). Only identity/auth columns; avatar_path (1.5)
and generations_* (3.2) are added by their own migrations.
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0002_users"
down_revision: Union[str, None] = "0001_baseline"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("nickname", sa.String(length=50), nullable=False),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("date_of_birth", sa.Date(), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email", name="uq_users_email"),
        sa.UniqueConstraint("nickname", name="uq_users_nickname"),
    )
    op.create_index("ix_users_email", "users", ["email"])
    op.create_index("ix_users_nickname", "users", ["nickname"])


def downgrade() -> None:
    op.drop_index("ix_users_nickname", table_name="users")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")
