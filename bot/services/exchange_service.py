import aiohttp
from decimal import Decimal
import logging

async def get_ton_price() -> Decimal:
    """Fetch current TON/USD price from an exchange"""
    try:
        async with aiohttp.ClientSession() as session:
            # Replace with your preferred crypto price API
            async with session.get('https://api.coingecko.com/api/v3/simple/price?ids=the-open-network&vs_currencies=usd') as response:
                data = await response.json()
                return Decimal(str(data['the-open-network']['usd']))
    except Exception as e:
        logging.error(f"Error fetching TON price: {e}")
        return Decimal('2.0')  # Fallback price 