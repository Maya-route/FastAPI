"""create column description

Revision ID: f7e7697d2cdd
Revises: 9fd0360d5d7f
Create Date: 2025-07-30 18:12:54.469425

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f7e7697d2cdd'
down_revision: Union[str, Sequence[str], None] = '9fd0360d5d7f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    
    op.add_column('vlans', sa.Column('description', sa.String(), nullable= True , server_default= 'in_use'))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('vlans', 'description')
    pass
