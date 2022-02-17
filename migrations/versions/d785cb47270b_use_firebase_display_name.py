"""use firebase display name

Revision ID: d785cb47270b
Revises: 09a585955767
Create Date: 2022-02-06 18:13:32.892629

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd785cb47270b'
down_revision = '09a585955767'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('name', sa.String(), nullable=False))
    op.drop_column('user', 'last_name')
    op.drop_column('user', 'first_name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('first_name', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column('user', sa.Column('last_name', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_column('user', 'name')
    # ### end Alembic commands ###