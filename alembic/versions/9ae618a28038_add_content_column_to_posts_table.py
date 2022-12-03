"""add content column to posts table

Revision ID: 9ae618a28038
Revises: 4f7eb9e08b3b
Create Date: 2022-12-03 20:18:11.067046

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9ae618a28038'
down_revision = '4f7eb9e08b3b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column("posts", "content")
