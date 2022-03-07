"""add_text_feedback

Revision ID: 24003bd80de5
Revises: 0d3fe2ab5de9
Create Date: 2022-03-05 21:57:02.097456

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '24003bd80de5'
down_revision = '0d3fe2ab5de9'
branch_labels = None
depends_on = None


def upgrade():
    with op.get_context().autocommit_block():
        op.execute("ALTER TYPE feedbackcategory ADD VALUE 'TEXTUAL_SUMMARY'")


def downgrade():
    pass
