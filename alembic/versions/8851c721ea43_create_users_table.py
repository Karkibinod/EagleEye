"""create_users_table

Revision ID: 8851c721ea43
Revises: 9f975aa2a833
Create Date: 2025-11-24 13:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8851c721ea43'
down_revision: Union[str, Sequence[str], None] = '9f975aa2a833'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create users table (enum will be created automatically by SQLAlchemy if needed)
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('role', sa.Enum('STUDENT', 'FACULTY', 'STAFF', 'VISITOR',
                  'ADMIN', name='userrole', create_type=False), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_user_id'),
                    'users', ['user_id'], unique=True)
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)

    # Create preferences table
    op.create_table(
        'preferences',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('accessibility_mode_enabled', sa.Boolean(), nullable=False),
        sa.Column('notifications_enabled', sa.Boolean(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id')
    )


def downgrade() -> None:
    op.drop_table('preferences')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_index(op.f('ix_users_user_id'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
    op.execute("DROP TYPE IF EXISTS userrole")
