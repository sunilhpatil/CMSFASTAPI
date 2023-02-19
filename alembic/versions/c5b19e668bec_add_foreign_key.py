"""add foreign key

Revision ID: c5b19e668bec
Revises: 5f1731839725
Create Date: 2023-02-18 01:24:02.198757

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c5b19e668bec'
down_revision = '5f1731839725'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable= False))
    op.create_foreign_key('posts_users_fk',source_table='posts', referent_table='users',
                          local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint(constraint_name='posts_users_fk',table_name='posts')
    op.drop_column(table_name='posts', column_name='owner_id')
    pass
