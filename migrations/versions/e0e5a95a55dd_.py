"""empty message

Revision ID: e0e5a95a55dd
Revises: e44eb63bda32
Create Date: 2018-08-21 23:06:15.691587

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e0e5a95a55dd'
down_revision = 'e44eb63bda32'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'partner', 'country', ['country'], ['iso'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'partner', type_='foreignkey')
    # ### end Alembic commands ###