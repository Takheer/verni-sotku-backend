"""create users table

Revision ID: 1255e16258ad
Revises: 
Create Date: 2023-05-02 03:21:54.274592

"""
from alembic import op
import sqlalchemy as sa

from sqlalchemy.engine.reflection import Inspector

conn = op.get_bind()
inspector = Inspector.from_engine(conn)
tables = inspector.get_table_names()

# revision identifiers, used by Alembic.
revision = '1255e16258ad'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    if 'users' not in tables:
        op.create_table(
            'users',
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('uuid', sa.String(50), nullable=False),
            sa.Column('name', sa.Unicode(350), nullable=False),
            sa.Column('email', sa.String(350), nullable=False),
            sa.Column('registration_date', sa.TIMESTAMP, server_default=sa.text('CURRENT_TIMESTAMP')),
        )


def downgrade() -> None:
    op.drop_table('users')
