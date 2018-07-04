"""empty message

Revision ID: 6bba61c26bcd
Revises: 5aa30c71ca70
Create Date: 2018-07-04 11:50:44.996761

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6bba61c26bcd'
down_revision = '5aa30c71ca70'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('partner', sa.Column('offname', sa.String(length=80), nullable=True))
    op.create_index(op.f('ix_partner_created_date'), 'partner', ['created_date'], unique=False)
    op.create_index(op.f('ix_partner_name'), 'partner', ['name'], unique=True)
    op.create_index(op.f('ix_partner_offname'), 'partner', ['offname'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_partner_offname'), table_name='partner')
    op.drop_index(op.f('ix_partner_name'), table_name='partner')
    op.drop_index(op.f('ix_partner_created_date'), table_name='partner')
    op.drop_column('partner', 'offname')
    # ### end Alembic commands ###
