"""add content column to post table

Revision ID: 40a544b3457a
Revises: 71ddb27bac33
Create Date: 2022-11-22 15:06:19.931579

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '40a544b3457a'
down_revision = '71ddb27bac33'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts",sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade():
    op.drop_column("posts","content")
    pass
