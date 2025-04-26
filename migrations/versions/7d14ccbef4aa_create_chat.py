"""create chat

Revision ID: 7d14ccbef4aa
Revises: 9bd276c4d92b
Create Date: 2025-04-23 18:20:25.220221

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

import sqlmodel

# revision identifiers, used by Alembic.
revision: str = '7d14ccbef4aa'
down_revision: Union[str, None] = '9bd276c4d92b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
