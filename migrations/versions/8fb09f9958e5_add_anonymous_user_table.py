"""add: anonymous_user table

Revision ID: 8fb09f9958e5
Revises: 8e0da6305668
Create Date: 2024-07-04 03:49:41.627048

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8fb09f9958e5'
down_revision = '8e0da6305668'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('anonymous_users',
    sa.Column('ip', sa.String(length=128), nullable=True),
    sa.Column('data', sa.JSON(), nullable=True),
    sa.Column('id', sa.String(length=60), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('anonymous_users')
    # ### end Alembic commands ###