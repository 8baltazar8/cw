"""add test table

Revision ID: 903ec7399a5e
Revises:
Create Date: 2023-05-27 17:30:28.485254

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '903ec7399a5e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('test_table',
                    sa.Column('id', sa.Integer, primary_key=True, nullable=False),
                    sa.Column('meme_text', sa.Text, nullable=False),
                    sa.Column('category', sa.String, nullable=False),
                    sa.Column('rating', sa.Numeric, server_default='1'),
                    sa.Column('num_of_grades', sa.Integer, server_default='1'),
                    sa.Column('created_at', sa.sql.sqltypes.TIMESTAMP(timezone=True), nullable=False, server_default=sa.sql.expression.text('now()')))


def downgrade() -> None:
    op.drop_table('test_table')
