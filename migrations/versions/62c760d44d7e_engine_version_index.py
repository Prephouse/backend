"""engine_version_index

Revision ID: 62c760d44d7e
Revises: 9df6f94ffc11
Create Date: 2022-03-09 18:47:54.589932

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '62c760d44d7e'
down_revision = '9df6f94ffc11'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_engine_version'), 'engine', ['version'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_engine_version'), table_name='engine')
    # ### end Alembic commands ###
