"""add: product_id to Review class

Revision ID: b1ead3cdf61a
Revises: 960ca930c1c3
Create Date: 2024-06-20 15:51:45.601803

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b1ead3cdf61a'
down_revision = '960ca930c1c3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('reviews', schema=None) as batch_op:
        batch_op.add_column(sa.Column('product_id', sa.String(length=128), nullable=False))
        batch_op.create_foreign_key(None, 'products', ['product_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('reviews', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('product_id')

    # ### end Alembic commands ###
