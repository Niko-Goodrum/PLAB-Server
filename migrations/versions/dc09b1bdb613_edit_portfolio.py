"""edit portfolio

Revision ID: dc09b1bdb613
Revises: bdaa4ae0a3d6
Create Date: 2025-05-31 21:44:48.953403

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

import sqlmodel

# revision identifiers, used by Alembic.
revision: str = 'dc09b1bdb613'
down_revision: Union[str, None] = 'bdaa4ae0a3d6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'portfolio', ['user_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'portfolio', type_='unique')
    # ### end Alembic commands ###
