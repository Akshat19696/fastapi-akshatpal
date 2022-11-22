"""add foreign_key to post table

Revision ID: 1a00fefbda32
Revises: 40a544b3457a
Create Date: 2022-11-22 15:17:51.048102

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1a00fefbda32'
down_revision = '40a544b3457a'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts",sa.Column("owner_id",sa.Integer(),nullable=False))
    op.create_foreign_key("posts_user_fk",source_table="posts",referent_table="users",local_cols=['owner_id'],remote_cols=["id"],ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint("post_user_fk",table_name="posts")
    op.drop_column("posts","owner_id")
    pass
