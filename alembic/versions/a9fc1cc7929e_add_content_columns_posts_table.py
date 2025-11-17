"""add_content_columns_posts_table

Revision ID: a9fc1cc7929e
Revises: 1a3c05cface2
Create Date: 2025-11-16 12:24:22.793379

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a9fc1cc7929e'
down_revision = '1a3c05cface2'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
