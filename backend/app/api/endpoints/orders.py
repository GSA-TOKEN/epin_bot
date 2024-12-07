from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.models import Order, User, Code
from app.schemas.order import OrderCreate
from decimal import Decimal
import logging
import datetime

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/", response_model=dict)
async def create_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db)
):
    """
    Creates an order and assigns available codes to it.
    """
    logger.info(f"Received order request: user_id={order_data.user_id}, product={order_data.product_type}")
    try:
        # 1. Find user by telegram_user_id
        user = db.query(User).filter(User.telegram_user_id == str(order_data.user_id)).first()
        if not user:
            logger.error(f"User not found: {order_data.user_id}")
            raise HTTPException(status_code=404, detail="User not found")

        # 2. Find available codes for the product type
        available_codes = db.query(Code).join(Code.product).filter(
            Code.is_sold == False
        ).limit(order_data.quantity).all()

        if len(available_codes) < order_data.quantity:
            logger.error(f"Not enough codes available. Requested: {order_data.quantity}, Available: {len(available_codes)}")
            raise HTTPException(status_code=400, detail="Not enough codes available")

        # 3. Create order
        order = Order(
            user_id=user.id,
            product_type=order_data.product_type,
            quantity=order_data.quantity,
            payment_method=order_data.payment_method,
            payment_id=order_data.payment_id,
            payment_status=order_data.status,
            amount_ton=Decimal(str(order_data.amount_ton)),
            amount_usd=Decimal(str(order_data.amount_usd))
        )
        db.add(order)
        db.flush()  # Get order.id

        # 4. Assign codes to order
        for code in available_codes:
            code.order_id = order.id
            code.is_sold = True
            code.sold_at = datetime.datetime.utcnow()
            code.sale_price = Decimal(str(order_data.amount_usd / order_data.quantity))
            code.gross_profit = code.sale_price - code.purchase_cost if code.purchase_cost else None
            code.updated_at = datetime.datetime.utcnow()

        try:
            db.commit()
            logger.info(f"Order created successfully: Order ID {order.id}")
            return {
                "order_id": order.id,
                "status": order.payment_status,
                "amount_usd": float(order.amount_usd)
            }

        except Exception as e:
            logger.error(f"Database commit error: {e}")
            db.rollback()
            raise HTTPException(status_code=500, detail="Failed to create order")

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

@router.get("/{order_id}/codes", response_model=dict)
async def get_order_codes(
    order_id: int,
    db: Session = Depends(get_db)
):
    """Get codes associated with an order"""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
        
    codes = db.query(Code).filter(Code.order_id == order_id).all()
    return {
        "codes": [{
            "code": code.code,
            "sale_price": float(code.sale_price) if code.sale_price else None,
            "sold_at": code.sold_at.isoformat() if code.sold_at else None,
            "gross_profit": float(code.gross_profit) if code.gross_profit else None
        } for code in codes]
    } 