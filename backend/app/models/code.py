from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from app.db.base import Base
import datetime

class Code(Base):
    __tablename__ = "codes"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    code = Column(String, nullable=False)
    purchase_date = Column(DateTime, default=datetime.datetime.utcnow)
    purchase_cost = Column(Numeric(10, 2), nullable=True)
    sale_price = Column(Numeric(10, 2), nullable=True)
    gross_profit = Column(Numeric(10, 2), nullable=True)
    is_sold = Column(Boolean, default=False)
    sold_at = Column(DateTime, nullable=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.datetime.utcnow)

    product = relationship("Product", back_populates="codes")
    order = relationship("Order", back_populates="codes")