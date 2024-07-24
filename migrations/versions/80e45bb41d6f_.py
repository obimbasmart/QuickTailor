"""empty message

Revision ID: 80e45bb41d6f
Revises: c383deafb87e
Create Date: 2024-06-14 02:04:20.942452

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '80e45bb41d6f'
down_revision = 'c383deafb87e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tailors',
    sa.Column('first_name', sa.String(length=128), nullable=False),
    sa.Column('last_name', sa.String(length=128), nullable=False),
    sa.Column('email', sa.String(length=128), nullable=False),
    sa.Column('password_hash', sa.TEXT(), nullable=False),
    sa.Column('phone_no', sa.String(length=128), nullable=False),
    sa.Column('business_name', sa.String(length=128), nullable=True),
    sa.Column('cac_number', sa.String(length=128), nullable=True),
    sa.Column('about', sa.String(length=1024), nullable=True),
    sa.Column('state', sa.String(length=128), nullable=True),
    sa.Column('city', sa.String(length=128), nullable=True),
    sa.Column('street', sa.String(length=128), nullable=True),
    sa.Column('is_available', sa.Boolean(), nullable=True),
    sa.Column('no_of_completed_jobs', sa.Integer(), nullable=False),
    sa.Column('reputation', sa.Integer(), nullable=True),
    sa.Column('photo_url', sa.String(length=2048), nullable=True),
    sa.Column('bank_name', sa.String(length=128), nullable=True),
    sa.Column('account_number', sa.Integer(), nullable=True),
    sa.Column('account_name', sa.String(length=128), nullable=True),
    sa.Column('reset_token', sa.String(length=128), nullable=True),
    sa.Column('reset_token_expires', sa.DateTime(), nullable=True),
    sa.Column('id', sa.String(length=60), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('first_name', sa.String(length=128), nullable=False),
    sa.Column('last_name', sa.String(length=128), nullable=False),
    sa.Column('email', sa.String(length=128), nullable=False),
    sa.Column('password_hash', sa.TEXT(), nullable=False),
    sa.Column('phone_no', sa.String(length=128), nullable=False),
    sa.Column('measurements', sa.JSON(), nullable=True),
    sa.Column('reset_token', sa.String(length=128), nullable=True),
    sa.Column('reset_token_expires', sa.DateTime(), nullable=True),
    sa.Column('id', sa.String(length=60), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('products',
    sa.Column('tailor_id', sa.String(length=128), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('description', sa.String(length=350), nullable=True),
    sa.Column('price', sa.String(length=128), nullable=False),
    sa.Column('images', sa.JSON(), nullable=True),
    sa.Column('estimated_tc', sa.Integer(), nullable=False),
    sa.Column('material', sa.String(length=128), nullable=True),
    sa.Column('on_draft', sa.Boolean(), nullable=False),
    sa.Column('customization_tokens', sa.JSON(), nullable=True),
    sa.Column('id', sa.String(length=60), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['tailor_id'], ['tailors.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('carts',
    sa.Column('product_id', sa.String(length=128), nullable=False),
    sa.Column('user_id', sa.String(length=128), nullable=False),
    sa.Column('measurements', sa.JSON(), nullable=False),
    sa.Column('cusomization_value', sa.String(length=128), nullable=True),
    sa.Column('id', sa.String(length=60), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('orders',
    sa.Column('product_id', sa.String(length=128), nullable=False),
    sa.Column('user_id', sa.String(length=128), nullable=False),
    sa.Column('order_status', sa.Enum('PENDING', 'COMFIRMED', 'COMPLETED', 'IN_PRGRESS', 'DELIVERED', name='orderStatus'), nullable=False),
    sa.Column('order_progress', sa.Enum('AWAITING_COMFIRMATION', 'MATERIAL_SOURCING', 'CUTTING', 'SEWING', 'IRONING', 'PACKAGING', name='orderProgress'), nullable=False),
    sa.Column('measurements', sa.JSON(), nullable=False),
    sa.Column('id', sa.String(length=60), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('orders')
    op.drop_table('carts')
    op.drop_table('products')
    op.drop_table('users')
    op.drop_table('tailors')
    # ### end Alembic commands ###