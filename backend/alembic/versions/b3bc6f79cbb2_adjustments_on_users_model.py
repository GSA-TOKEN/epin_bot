"""adjustments on users model

Revision ID: b3bc6f79cbb2
Revises: bd9991504446
Create Date: 2024-11-24 14:17:48.906065

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b3bc6f79cbb2'
down_revision: Union[str, None] = 'bd9991504446'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
