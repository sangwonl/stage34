"""create user table

Revision ID: 3cc47c8d8c2c
Revises: 
Create Date: 2016-08-09 13:20:48.644215

"""

# revision identifiers, used by Alembic.
revision = '3cc47c8d8c2c'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('email', sa.String(128)),
        sa.Column('password', sa.String(128)),
        sa.Column('jwt', sa.String(512)),


def downgrade():
    op.drop_table('users')
