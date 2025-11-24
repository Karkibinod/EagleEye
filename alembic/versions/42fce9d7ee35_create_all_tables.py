"""create_all_tables

Revision ID: 42fce9d7ee35
Revises: c41474918153
Create Date: 2025-11-24 04:26:21.415801

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '42fce9d7ee35'
down_revision: Union[str, Sequence[str], None] = 'c41474918153'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
