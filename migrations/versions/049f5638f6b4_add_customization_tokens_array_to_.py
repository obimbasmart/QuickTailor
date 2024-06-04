"""add: customization_tokens array to product table

Revision ID: 049f5638f6b4
Revises: 0f4544d9896b
Create Date: 2024-06-02 12:25:59.285317

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '049f5638f6b4'
down_revision = '0f4544d9896b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.add_column(sa.Column('customization_tokens', sa.JSON(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.drop_column('customization_tokens')

    # ### end Alembic commands ###