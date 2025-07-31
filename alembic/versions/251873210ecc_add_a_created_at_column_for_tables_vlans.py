"""add a created_at column for tables vlans

Revision ID: 251873210ecc
Revises: 46729ea06517
Create Date: 2025-07-30 19:08:06.693714

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '251873210ecc'
down_revision: Union[str, Sequence[str], None] = '46729ea06517'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('vlans' , sa.Column('created_at' , sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('vlans' , 'created_at')
    pass
