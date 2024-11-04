"""update posts table

Revision ID: 973c40fed47a
Revises: bbfc62380431
Create Date: 2024-11-04 16:41:29.211038

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "973c40fed47a"
down_revision: Union[str, None] = "bbfc62380431"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "posts",
        sa.Column("published", sa.Boolean(), server_default="TRUE", nullable=False),
    )
    pass


def downgrade() -> None:
    op.drop_column("posts", "published")
    pass
