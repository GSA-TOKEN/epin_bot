from sqlalchemy import Column, Integer, ForeignKey, Numeric, String, DateTime
from sqlalchemy.orm import relationship
from app.db.base import Base
import datetime

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Product details
    product_type = Column(String, nullable=False)  # e.g., "milli_1"
    quantity = Column(Integer, nullable=False)     # Number of codes ordered
    
    # Payment details
    payment_method = Column(String, nullable=False)
    payment_id = Column(String, nullable=False)
    payment_status = Column(String, nullable=False, default="pending")
    
    # Amount details
    amount_ton = Column(Numeric(18, 9), nullable=False)
    amount_usd = Column(Numeric(10, 2), nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="orders")
    codes = relationship("Code", back_populates="order") 