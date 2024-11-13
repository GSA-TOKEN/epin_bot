# handlers/order_handlers.py

from telegram import Update
from telegram.ext import ContextTypes
from keyboards import orders_keyboard
from config import MAIN_MENU

async def show_orders(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """My Orders handler"""
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        text="Your Orders:\n\n"
             "1. $10 Netflix Gift Card\n"
             "Purchased on: July 5, 2024\n"
             "Quantity: 1\n"
             "Status: Ready for delivery",
        reply_markup=orders_keyboard()
    )
    return MAIN_MENU
