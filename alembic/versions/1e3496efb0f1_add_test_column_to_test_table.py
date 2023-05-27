"""add test_column to test_table

Revision ID: 1e3496efb0f1
Revises: 903ec7399a5e
Create Date: 2023-05-27 17:48:21.727926

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1e3496efb0f1'
down_revision = '903ec7399a5e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('test_table', sa.Column('test_column', sa.String, nullable=True))


def downgrade() -> None:
    op.drop_column('test_table', 'test_column')
