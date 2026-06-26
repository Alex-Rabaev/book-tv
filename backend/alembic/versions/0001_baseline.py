"""baseline (no domain tables yet)

Revision ID: 0001_baseline
Revises:
Create Date: 2026-06-27

Domain tables (users, saved_images) are introduced by later stories (1.2, 4.1).
This baseline establishes the migration chain only.
"""
from typing import Sequence, Union

revision: str = "0001_baseline"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
