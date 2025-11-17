"""create posts table

Revision ID: 1a3c05cface2
Revises: b8c94182471b
Create Date: 2025-11-16 12:08:35.317910

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1a3c05cface2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'posts',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('title', sa.String(), nullable=False),
    )
    pass


def downgrade():
    op.drop_table('posts')
    pass
