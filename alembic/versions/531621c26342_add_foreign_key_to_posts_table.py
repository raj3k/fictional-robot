"""add foreign-key to posts table

Revision ID: 531621c26342
Revises: a6c5590acd3c
Create Date: 2022-12-03 20:34:24.006268

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '531621c26342'
down_revision = 'a6c5590acd3c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table="posts", referent_table="users", local_cols=[
        'owner_id'], remote_cols=['id'], ondelete="CASCADE")


def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
