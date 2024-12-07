from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.models import Order, OrderItem, User, Product
from app.schemas.order import OrderCreate
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/", response_model=dict)
async def create_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db)
):
    """
    Creates an order with its associated order item.
    """
    logger.info(f"Received order request: user_id={order_data.user_id}, product={order_data.product_type}")
    try:
        # 1. Find user by telegram_user_id
        user = db.query(User).filter(User.telegram_user_id == str(order_data.user_id)).first()
        if not user:
            logger.error(f"User not found: {order_data.user_id}")
            raise HTTPException(status_code=404, detail="User not found")

        # 2. Find product
        product = db.query(Product).filter(
            Product.name == order_data.product_type,
            Product.price == Decimal(order_data.product_amount.replace('$', ''))
        ).first()
        
        if not product:
            logger.error(f"Product not found: {order_data.product_type} - {order_data.product_amount}")
            raise HTTPException(status_code=404, detail="Product not found")

        # 3. Create main order record
        order = Order(
            user_id=user.id,
            total_amount=Decimal(str(order_data.amount_usd)),
            payment_method=order_data.payment_method,
            payment_status=order_data.status
        )
        db.add(order)
        db.flush()

        # 4. Create order item record
        order_item = OrderItem(
            order_id=order.id,
            product_id=product.id,
            quantity=order_data.quantity,
            unit_price=Decimal(str(order_data.amount_usd/order_data.quantity)),
            total_price=Decimal(str(order_data.amount_usd))
        )
        db.add(order_item)

        try:
            db.commit()
            logger.info(f"Order created successfully: Order ID {order.id}")
            return {
                "order_id": order.id,
                "order_item_id": order_item.id,
                "status": order_data.status,
                "total_amount": float(order.total_amount)
            }

        except Exception as e:
            logger.error(f"Database commit error: {e}")
            db.rollback()
            raise HTTPException(status_code=500, detail="Failed to create order records")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating order: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}") 

@router.get("/{order_id}", response_model=dict)
async def get_order(order_id: int, db: Session = Depends(get_db)):
    """Get order by ID"""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    return {
        "order_id": order.id,
        "status": order.payment_status,
        "total_amount": float(order.total_amount)
    }

@router.patch("/{order_id}", response_model=dict)
async def update_order_status(
    order_id: int, 
    status_update: dict,
    db: Session = Depends(get_db)
):
    """Update order status"""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    order.payment_status = status_update["status"]
    db.commit()
    
    return {
        "order_id": order.id,
        "status": order.payment_status
    } 