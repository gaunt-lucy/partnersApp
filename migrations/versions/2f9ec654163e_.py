"""empty message

Revision ID: 2f9ec654163e
Revises: 61d66f3243ef
Create Date: 2018-07-30 22:47:23.366284

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2f9ec654163e'
down_revision = '61d66f3243ef'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('report', sa.Column('visit_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'report', 'visit', ['visit_id'], ['id'])
    op.drop_column('report', 'visit')
    op.add_column('visit', sa.Column('status', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('visit', 'status')
    op.add_column('report', sa.Column('visit', sa.INTEGER(), nullable=True))
    op.drop_constraint(None, 'report', type_='foreignkey')
    op.drop_column('report', 'visit_id')
    # ### end Alembic commands ###
