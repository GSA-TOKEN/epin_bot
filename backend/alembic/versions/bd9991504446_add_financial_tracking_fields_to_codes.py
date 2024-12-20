"""add financial tracking fields to codes

Revision ID: bd9991504446
Revises: 35a413755659
Create Date: 2024-11-24 04:00:36.340733

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bd9991504446'
down_revision: Union[str, None] = '35a413755659'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('codes', sa.Column('purchase_date', sa.DateTime(), nullable=True))
    op.add_column('codes', sa.Column('purchase_cost', sa.Numeric(precision=10, scale=2), nullable=False))
    op.add_column('codes', sa.Column('sale_price', sa.Numeric(precision=10, scale=2), nullable=True))
    op.add_column('codes', sa.Column('gross_profit', sa.Numeric(precision=10, scale=2), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('codes', 'gross_profit')
    op.drop_column('codes', 'sale_price')
    op.drop_column('codes', 'purchase_cost')
    op.drop_column('codes', 'purchase_date')
    # ### end Alembic commands ###
