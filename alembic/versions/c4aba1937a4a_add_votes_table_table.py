"""add votes table table

Revision ID: c4aba1937a4a
Revises: 973c40fed47a
Create Date: 2024-11-04 16:50:45.730810

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'c4aba1937a4a'
down_revision: Union[str, None] = '973c40fed47a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('votes',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'post_id')
    )
    op.create_index(op.f('ix_votes_post_id'), 'votes', ['post_id'], unique=False)
    op.create_index(op.f('ix_votes_user_id'), 'votes', ['user_id'], unique=False)
    op.alter_column('posts', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               type_=sa.TIMESTAMP(timezone=True),
               existing_nullable=False,
               existing_server_default=sa.text('now()'))
    op.create_index(op.f('ix_posts_content'), 'posts', ['content'], unique=False)
    op.create_index(op.f('ix_posts_created_at'), 'posts', ['created_at'], unique=False)
    op.create_index(op.f('ix_posts_id'), 'posts', ['id'], unique=False)
    op.create_index(op.f('ix_posts_owner_id'), 'posts', ['owner_id'], unique=False)
    op.alter_column('users', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               type_=sa.TIMESTAMP(timezone=True),
               existing_nullable=False,
               existing_server_default=sa.text('now()'))
    op.drop_constraint('users_email_key', 'users', type_='unique')
    op.create_index(op.f('ix_users_created_at'), 'users', ['created_at'], unique=False)
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.drop_column('users', 'updated_at')
    op.drop_column('users', 'is_active')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('is_active', sa.BOOLEAN(), server_default=sa.text('true'), autoincrement=False, nullable=False))
    op.add_column('users', sa.Column('updated_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=False))
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_index(op.f('ix_users_created_at'), table_name='users')
    op.create_unique_constraint('users_email_key', 'users', ['email'])
    op.alter_column('users', 'created_at',
               existing_type=sa.TIMESTAMP(timezone=True),
               type_=postgresql.TIMESTAMP(),
               existing_nullable=False,
               existing_server_default=sa.text('now()'))
    op.drop_index(op.f('ix_posts_owner_id'), table_name='posts')
    op.drop_index(op.f('ix_posts_id'), table_name='posts')
    op.drop_index(op.f('ix_posts_created_at'), table_name='posts')
    op.drop_index(op.f('ix_posts_content'), table_name='posts')
    op.alter_column('posts', 'created_at',
               existing_type=sa.TIMESTAMP(timezone=True),
               type_=postgresql.TIMESTAMP(),
               existing_nullable=False,
               existing_server_default=sa.text('now()'))
    op.drop_index(op.f('ix_votes_user_id'), table_name='votes')
    op.drop_index(op.f('ix_votes_post_id'), table_name='votes')
    op.drop_table('votes')
    # ### end Alembic commands ###
