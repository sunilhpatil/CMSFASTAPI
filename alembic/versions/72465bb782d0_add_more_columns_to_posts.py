"""add more columns to posts

Revision ID: 72465bb782d0
Revises: c5b19e668bec
Create Date: 2023-02-18 01:40:44.720960

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '72465bb782d0'
down_revision = 'c5b19e668bec'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(table_name='posts', column=sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'))
    op.add_column(table_name='posts', column=sa.Column('created_at',
                                                       sa.TIMESTAMP(timezone=True),nullable=False,
                                                         server_default = sa.text('now()') ))
    pass


def downgrade() -> None:
    op.drop_column(table_name='posts',column_name='published')
    op.drop_column(table_name='posts', column_name='created_at')
    pass
