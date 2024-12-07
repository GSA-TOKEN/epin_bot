"""simplify_order_and_code_tables

Revision ID: 654f1d97ff8d
Revises: bd9991504446
Create Date: 2024-12-07 22:38:17.891297

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '654f1d97ff8d'
down_revision: Union[str, None] = 'bd9991504446'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Drop foreign key constraints first
    op.drop_constraint('codes_order_item_id_fkey', 'codes', type_='foreignkey')
    op.drop_constraint('codes_product_id_fkey', 'codes', type_='foreignkey')
    op.drop_constraint('order_items_order_id_fkey', 'order_items', type_='foreignkey')
    op.drop_constraint('order_items_product_id_fkey', 'order_items', type_='foreignkey')

    # Drop order_items table and products table
    op.drop_table('order_items')
    op.drop_table('products')

    # Modify codes table
    op.drop_column('codes', 'order_item_id')
    op.drop_column('codes', 'product_id')
    op.add_column('codes', sa.Column('order_id', sa.Integer(), nullable=True))
    op.add_column('codes', sa.Column('product_type', sa.String(), nullable=True))
    
    # Create foreign key for codes.order_id
    op.create_foreign_key('fk_codes_orders', 'codes', 'orders', ['order_id'], ['id'])

    # Modify orders table
    op.add_column('orders', sa.Column('product_type', sa.String(), nullable=True))
    op.add_column('orders', sa.Column('quantity', sa.Integer(), nullable=True))
    op.add_column('orders', sa.Column('payment_id', sa.String(), nullable=True))
    op.add_column('orders', sa.Column('amount_ton', sa.Numeric(precision=18, scale=9), nullable=True))
    op.add_column('orders', sa.Column('amount_usd', sa.Numeric(precision=10, scale=2), nullable=True))
    
    # Drop old column from orders
    op.drop_column('orders', 'total_amount')
    
    # Make new columns non-nullable after data migration
    op.alter_column('orders', 'product_type', nullable=False)
    op.alter_column('orders', 'quantity', nullable=False)
    op.alter_column('orders', 'payment_id', nullable=False)
    op.alter_column('orders', 'amount_ton', nullable=False)
    op.alter_column('orders', 'amount_usd', nullable=False)
    op.alter_column('codes', 'product_type', nullable=False)


def downgrade() -> None:
    pass
