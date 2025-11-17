"""add forgein_key_post_table

Revision ID: 159ecf14a6c0
Revises: 5cb6a1872629
Create Date: 2025-11-16 12:36:12.990573

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '159ecf14a6c0'
down_revision = '5cb6a1872629'
branch_labels = None
depends_on = None



def upgrade():
    op.add_column('posts', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table="posts", referent_table="users", local_cols=[
                          'user_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts', 'user_id')
    pass