from pydantic import BaseModel, Field, validator
from decimal import Decimal

class PinCSVRow(BaseModel):
    product_name: str = Field(..., description="Name of the product")
    price: Decimal = Field(..., description="Price of the product", ge=0)
    pin_code: str = Field(..., description="The actual pin/code value")

    @validator('price')
    def validate_price(cls, v):
        if v <= 0:
            raise ValueError('Price must be greater than 0')
        return v 