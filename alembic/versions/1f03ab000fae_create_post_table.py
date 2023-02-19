"""create post table

Revision ID: 1f03ab000fae
Revises: 
Create Date: 2023-02-17 01:25:07.115762

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1f03ab000fae'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts',sa.Column('id', sa.Integer, nullable = False),
                    sa.Column('title', sa.String, nullable = False)
                    )
    
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
