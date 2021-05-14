"""empty message

Revision ID: 3c6d57f093d1
Revises: 8c8428ca5710
Create Date: 2021-05-14 05:10:10.773833

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3c6d57f093d1'
down_revision = '8c8428ca5710'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('questionset', sa.Column('module', sa.String(length=64), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('questionset', 'module')
    # ### end Alembic commands ###
