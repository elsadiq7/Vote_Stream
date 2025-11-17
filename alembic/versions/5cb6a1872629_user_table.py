"""user_table

Revision ID: 5cb6a1872629
Revises: a9fc1cc7929e
Create Date: 2025-11-16 12:30:38.249919

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5cb6a1872629'
down_revision = 'a9fc1cc7929e'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('email', sa.String(), nullable=False, unique=True),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()'))
    )   
    pass


def downgrade():
    op.drop_table('users')
    pass
