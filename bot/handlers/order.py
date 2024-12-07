# handlers/order_handlers.py

from telegram import Update
from telegram.ext import ContextTypes
from keyboards import orders_keyboard
from config import MAIN_MENU
from aiohttp import ClientSession
from config.settings import API_BASE_URL
import logging

async def show_orders(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """My Orders handler"""
    query = update.callback_query
    await query.answer()

    try:
        async with ClientSession() as session:
            async with session.get(
                f"{API_BASE_URL}/orders/user/{update.effective_user.id}"
            ) as response:
                if response.status == 200:
                    orders = await response.json()
                    
                    if not orders:
                        await query.edit_message_text(
                            "You don't have any orders yet.",
                            reply_markup=orders_keyboard()
                        )
                        return MAIN_MENU
                    
                    # Format orders message
                    orders_text = "Your Orders:\n\n"
                    for order in orders:
                        payment_amount = f"{order['amount_ton']:.2f} TON" if order['payment_method'] == 'ton' else f"${order['amount_usd']:.2f}"
                        orders_text += (
                            f"#{order['id']} - {order['product_type']}\n"
                            f"Amount: {payment_amount}\n"
                            f"Quantity: {order['quantity']}\n"
                            f"Status: {order['payment_status'].title()}\n"
                            f"Date: {order['created_at']}\n\n"
                        )
                    
                    await query.edit_message_text(
                        text=orders_text,
                        reply_markup=orders_keyboard()
                    )
                    return MAIN_MENU
                    
    except Exception as e:
        logging.error(f"Error fetching orders: {e}")
        await query.edit_message_text(
            "Error fetching orders. Please try again.",
            reply_markup=orders_keyboard()
        )
    
    return MAIN_MENU
