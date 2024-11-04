"""add created_at column

Revision ID: 18ec9b8110f1
Revises: 3d0aac803874
Create Date: 2024-11-04 16:02:02.706922

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "18ec9b8110f1"
down_revision: Union[str, None] = "3d0aac803874"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "posts",
        sa.Column(
            "created_at",
            sa.TIMESTAMP(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )
    # sa.Index("ix_posts_content", "content"),
    # sa.Index("ix_posts_published", "published"),
    # sa.Index("ix_posts_title", "title"),
    pass


def downgrade() -> None:
    op.drop_column("posts", "created_at")
    pass
