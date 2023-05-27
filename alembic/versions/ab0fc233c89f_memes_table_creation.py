"""memes table creation

Revision ID: ab0fc233c89f
Revises: 1e3496efb0f1
Create Date: 2023-05-27 18:04:09.505036

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ab0fc233c89f'
down_revision = '1e3496efb0f1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('memes',
                    sa.Column('id', sa.Integer, primary_key=True, nullable=False),
                    sa.Column('meme_text', sa.Text, nullable=False),
                    sa.Column('category', sa.String, nullable=False),
                    sa.Column('rating', sa.Numeric, server_default='1'),
                    sa.Column('num_of_grades', sa.Integer, server_default='1'),
                    sa.Column('created_at', sa.sql.sqltypes.TIMESTAMP(timezone=True), nullable=False, server_default=sa.sql.expression.text('now()')))


def downgrade() -> None:
    op.drop_table('memes')
