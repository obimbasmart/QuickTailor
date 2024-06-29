"""add: otp attr to user/tailor

Revision ID: 050c4248cc90
Revises: c566990de72d
Create Date: 2024-06-29 15:49:09.981222

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '050c4248cc90'
down_revision = 'c566990de72d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tailors', schema=None) as batch_op:
        batch_op.add_column(sa.Column('otp', sa.Integer(), nullable=True))

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('otp', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('otp')

    with op.batch_alter_table('tailors', schema=None) as batch_op:
        batch_op.drop_column('otp')

    # ### end Alembic commands ###
