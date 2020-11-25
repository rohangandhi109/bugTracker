"""empty message

Revision ID: 3b7a8770dbb9
Revises: 5a571ba80234
Create Date: 2020-11-23 22:51:23.341784

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3b7a8770dbb9'
down_revision = '5a571ba80234'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('results', sa.Column('phone', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('results', 'phone')
    # ### end Alembic commands ###
