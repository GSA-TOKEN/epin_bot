# handlers/category_handlers.py

from telegram import Update
from telegram.ext import ContextTypes
from keyboards import epins_category_keyboard, games_category_keyboard, special_offers_keyboard
from config import PRODUCT_SELECTION

async def show_categories(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Product categories handler"""
    query = update.callback_query
    await query.answer()

    category_type = query.data.split('_')[1]
    
    if category_type == 'epins':
        reply_markup = epins_category_keyboard()
        message = "Select an E-Pin category:"
    elif category_type == 'games':
        reply_markup = games_category_keyboard()
        message = "Select a game category:"
    elif category_type == 'special':
        reply_markup = special_offers_keyboard()
        message = "Check out our special offers:"
    else:
        reply_markup = None
        message = "Category not available"

    await query.edit_message_text(
        text=message,
        reply_markup=reply_markup
    )
    return PRODUCT_SELECTION
