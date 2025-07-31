"""add  foreign_key to posts table

Revision ID: 46729ea06517
Revises: c901a0e7fe75
Create Date: 2025-07-30 18:50:13.631121

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '46729ea06517'
down_revision: Union[str, Sequence[str], None] = 'c901a0e7fe75'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('vlans' , sa.Column('owner_id' , sa.Integer() ,nullable=False))
    op.create_foreign_key('post_users_fkey', source_table='vlans' , referent_table='users' , 
                          local_cols= ['owner_id'] , remote_cols=['user_id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('post_users_fkey' , table_name='vlans')
    op.drop_column('vlans', 'owner_id')
    pass
