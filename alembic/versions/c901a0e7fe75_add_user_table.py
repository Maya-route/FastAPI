"""add user table

Revision ID: c901a0e7fe75
Revises: f7e7697d2cdd
Create Date: 2025-07-30 18:32:25.997122

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c901a0e7fe75'
down_revision: Union[str, Sequence[str], None] = 'f7e7697d2cdd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    
    op.create_table('users' , sa.Column('user_id' , sa.Integer(), nullable=False ),
                                sa.Column('email' , sa.String(), nullable= False ),
                                sa.Column('password' , sa.String(), nullable=False),
                                sa.Column('created_at' , sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
                                sa.PrimaryKeyConstraint('user_id'),
                                sa.UniqueConstraint('email'))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('users')
    pass
