"""create posts table

Revision ID: 9fd0360d5d7f
Revises: 
Create Date: 2025-07-30 16:22:00.693885

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9fd0360d5d7f'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('vlans', sa.Column('vlan_id', sa.Integer(), nullable = False , primary_key = True),
                    sa.Column('name', sa.String(), nullable= False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('vlans')
    pass
