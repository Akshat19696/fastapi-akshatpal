"""Add few columns to posts table 

Revision ID: 62a34ff3c976
Revises: 1a00fefbda32
Create Date: 2022-11-22 17:55:20.938337

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '62a34ff3c976'
down_revision = '1a00fefbda32'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts",sa.Column("publshed",sa.Boolean(),nullable=False,server_default="True"))
    op.add_column("posts",sa.Column("created_at",sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text("now()")))
    pass


def downgrade():
    op.drop_column("posts","published")
    op.drop_column("posts","created_at")
    pass
