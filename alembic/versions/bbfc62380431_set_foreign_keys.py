"""set foreign keys

Revision ID: bbfc62380431
Revises: 57af7f23fb26
Create Date: 2024-11-04 16:31:47.030575

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "bbfc62380431"
down_revision: Union[str, None] = "57af7f23fb26"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key(
        "fk_posts_owner_id_users",
        source_table="posts",
        referent_table="users",
        local_cols=["owner_id"],
        remote_cols=["id"],
        ondelete="CASCADE",
    )
    pass


def downgrade() -> None:
    op.drop_constraint(
        "fk_posts_owner_id_users", table_name="posts", type_="foreignkey"
    )
    op.drop_column("posts", "owner_id")
    pass
