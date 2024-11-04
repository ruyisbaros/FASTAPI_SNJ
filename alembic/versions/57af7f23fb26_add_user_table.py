"""add user table

Revision ID: 57af7f23fb26
Revises: 18ec9b8110f1
Create Date: 2024-11-04 16:19:13.971809

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "57af7f23fb26"
down_revision: Union[str, None] = "18ec9b8110f1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("email", sa.String(length=100), unique=True, nullable=False),
        sa.Column("password", sa.String(length=100), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.Column("is_active", sa.Boolean(), nullable=False, default=True),
    )
    pass


def downgrade() -> None:
    op.drop_table("users")
    pass
