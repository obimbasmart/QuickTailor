"""add: product_id to review class

Revision ID: 68a20862b7f5
Revises: f69992ac8129
Create Date: 2024-06-20 16:04:46.697550

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '68a20862b7f5'
down_revision = 'f69992ac8129'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('reviews',
    sa.Column('order_id', sa.String(length=128), nullable=False),
    sa.Column('product_id', sa.String(length=128), nullable=False),
    sa.Column('review', sa.String(length=1028), nullable=False),
    sa.Column('rating', sa.Integer(), nullable=False),
    sa.Column('id', sa.String(length=60), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('reviews')
    # ### end Alembic commands ###
