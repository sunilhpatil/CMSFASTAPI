"""add content column to posts

Revision ID: 799e1ae65539
Revises: 1f03ab000fae
Create Date: 2023-02-18 00:10:02.769817

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '799e1ae65539'
down_revision = '1f03ab000fae'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable = False))
    pass


def downgrade() -> None:
    op.drop_column('post', 'content')
    pass
