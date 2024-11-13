# handlers/menu_handlers.py

from telegram import Update
from telegram.ext import ContextTypes
from keyboards import category_keyboard
from config import CATEGORY_SELECTION

async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Main menu handler"""
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        text="Choose a category to start shopping:",
        reply_markup=category_keyboard()
    )
    return CATEGORY_SELECTION
