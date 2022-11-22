"""create post table

Revision ID: 88e900fe452c
Revises: 
Create Date: 2022-11-22 12:21:34.543954

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '88e900fe452c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts',sa.Column('id',sa.Integer(),nullable=False,primary_key=True),sa.Column("Title",sa.String(),nullable=False))
    pass


def downgrade():
    op.drop_table("posts")
    pass
