"""empty message

Revision ID: 457a6bd40ecb
Revises: 57f17233f3e1
Create Date: 2022-02-09 23:24:09.409878

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '457a6bd40ecb'
down_revision = '57f17233f3e1'
branch_labels = None
depends_on = None


def upgrade():
    with op.get_context().autocommit_block():
        op.execute("ALTER TYPE feedbackcategory ADD VALUE 'FILLER_WORD'")


def downgrade():
    pass
