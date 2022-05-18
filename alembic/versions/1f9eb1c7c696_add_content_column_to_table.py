"""add content column to table

Revision ID: 1f9eb1c7c696
Revises: dd1ef5b43c8e
Create Date: 2022-05-18 16:35:21.196670

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1f9eb1c7c696'
down_revision = 'dd1ef5b43c8e'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('content', sa.String(),nullable = False))
    pass


def downgrade():
    op.drop_column('posts','content')
    pass
