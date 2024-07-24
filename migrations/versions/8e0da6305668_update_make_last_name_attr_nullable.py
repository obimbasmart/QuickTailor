"""update: make last_name attr nullable

Revision ID: 8e0da6305668
Revises: 050c4248cc90
Create Date: 2024-06-29 18:37:09.345914

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '8e0da6305668'
down_revision = '050c4248cc90'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tailors', schema=None) as batch_op:
        batch_op.alter_column('last_name',
               existing_type=mysql.VARCHAR(length=128),
               nullable=True)

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('last_name',
               existing_type=mysql.VARCHAR(length=128),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('last_name',
               existing_type=mysql.VARCHAR(length=128),
               nullable=False)

    with op.batch_alter_table('tailors', schema=None) as batch_op:
        batch_op.alter_column('last_name',
               existing_type=mysql.VARCHAR(length=128),
               nullable=False)

    # ### end Alembic commands ###
