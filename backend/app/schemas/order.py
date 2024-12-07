from pydantic import BaseModel, Field
from decimal import Decimal

class OrderCreate(BaseModel):
    user_id: int
    product_type: str
    product_amount: str
    quantity: int
    payment_method: str
    payment_id: str
    amount_ton: float
    amount_usd: float
    status: str = Field(default="pending") 