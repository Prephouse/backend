"""converted confidence to a floating number

Revision ID: 9df6f94ffc11
Revises: 24003bd80de5
Create Date: 2022-03-08 05:24:07.783039

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9df6f94ffc11'
down_revision = '24003bd80de5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('feedback', 'confidence',
               existing_type=sa.INTEGER(),
               type_=sa.Numeric(precision=10, scale=9),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('feedback', 'confidence',
               existing_type=sa.Numeric(precision=10, scale=9),
               type_=sa.INTEGER(),
               existing_nullable=True)
    # ### end Alembic commands ###
