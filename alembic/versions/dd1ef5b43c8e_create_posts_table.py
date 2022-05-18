"""create posts table

Revision ID: dd1ef5b43c8e
Revises: 
Create Date: 2022-05-18 16:15:25.547437

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dd1ef5b43c8e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts',sa.Column('id',sa.Integer(),nullable = False,primary_key= True),
                    sa.Column('title',sa.String(),nullable= False))
    pass


def downgrade():
    op.drop_table('posts')
    pass
