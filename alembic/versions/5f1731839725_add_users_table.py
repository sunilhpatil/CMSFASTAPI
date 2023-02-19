"""add users table

Revision ID: 5f1731839725
Revises: 799e1ae65539
Create Date: 2023-02-18 00:35:07.522926

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5f1731839725'
down_revision = '799e1ae65539'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable = False, primary_key=True),
                    sa.Column('email', sa.String(),nullable = False),
                    sa.Column('password', sa.String(), nullable= False),
                    sa.Column('created_at',sa.TIMESTAMP(timezone=True), server_default= sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
