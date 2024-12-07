from aiohttp import ClientSession
from config.settings import API_BASE_URL
import logging
from decimal import Decimal
from typing import Optional

# Set up logger
logger = logging.getLogger(__name__)

async def create_order(
    user_id: int,
    product_type: str,
    product_amount: str,
    quantity: int,
    payment_method: str,
    payment_id: str,
    amount_ton: float,
    amount_usd: float,
    status: str
) -> Optional[int]:
    """Create order in database"""
    try:
        async with ClientSession() as session:
            data = {
                "user_id": user_id,
                "product_type": product_type,
                "product_amount": product_amount,
                "quantity": quantity,
                "payment_method": payment_method,
                "payment_id": payment_id,
                "amount_ton": amount_ton,
                "amount_usd": amount_usd,
                "status": status
            }
            async with session.post(f"{API_BASE_URL}/orders", json=data) as response:
                if response.status != 200:
                    logger.error(f"Failed to create order. Status: {response.status}")
                    response_text = await response.text()
                    logger.error(f"Response: {response_text}")
                    return None
                result = await response.json()
                logger.info(f"Order created successfully: {result}")
                return result.get("order_id")
    except Exception as e:
        logger.error(f"Error creating order: {e}")
        return None

async def update_order_status(order_id: int, status: str) -> bool:
    async with ClientSession() as session:
        async with session.patch(f"{API_BASE_URL}/orders/{order_id}", json={
            "status": status
        }) as response:
            return response.status == 200

async def get_order(order_id: int) -> dict:
    async with ClientSession() as session:
        async with session.get(f"{API_BASE_URL}/orders/{order_id}") as response:
            if response.status == 200:
                return await response.json()
            return None

async def get_product_codes(product_type: str, product_amount: str, quantity: int) -> list:
    """Get available product codes from the database"""
    async with ClientSession() as session:
        async with session.get(
            f"{API_BASE_URL}/codes/available",
            params={
                "product_type": product_type,
                "product_amount": product_amount,
                "quantity": quantity
            }
        ) as response:
            if response.status == 200:
                data = await response.json()
                return data.get('codes', [])
            logging.error(f"Failed to get product codes: {response.status}")
            return [] 

async def register_user(user_id: int, username: str = None, first_name: str = None, last_name: str = None) -> bool:
    """Register user in the database"""
    try:
        async with ClientSession() as session:
            data = {
                "telegram_user_id": str(user_id),
                "username": username,
                "first_name": first_name,
                "last_name": last_name,
                "email": f"{user_id}@telegram.user"  # Required by current schema
            }
            async with session.post(f"{API_BASE_URL}/users", json=data) as response:
                if response.status != 200:
                    logger.error(f"Failed to register user. Status: {response.status}")
                    response_text = await response.text()
                    logger.error(f"Response: {response_text}")
                    return False
                return True
    except Exception as e:
        logger.error(f"Error registering user: {e}")
        return False 