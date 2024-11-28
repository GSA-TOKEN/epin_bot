from aiohttp import ClientSession
from config.settings import API_BASE_URL
import logging
from decimal import Decimal

async def create_order(user_id: int, product_type: str, product_amount: str,
                      quantity: int, payment_method: str, payment_id: str,
                      amount_ton: Decimal, amount_usd: Decimal, status: str) -> int:
    async with ClientSession() as session:
        async with session.post(f"{API_BASE_URL}/orders", json={
            "user_id": user_id,
            "product_type": product_type,
            "product_amount": product_amount,
            "quantity": quantity,
            "payment_method": payment_method,
            "payment_id": payment_id,
            "amount_ton": amount_ton,
            "amount_usd": amount_usd,
            "status": status
        }) as response:
            if response.status == 201:
                data = await response.json()
                return data.get('id')
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