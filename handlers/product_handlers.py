# handlers/product_handlers.py

from telegram import Update
from telegram.ext import ContextTypes
from keyboards import product_keyboard, quantity_keyboard
from messages import PRODUCT_MESSAGES
from config import QUANTITY_INPUT, PAYMENT_SELECTION

async def show_products(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Product listing handler"""
    query = update.callback_query
    await query.answer()

    product_type = query.data.split('_')[1]

    reply_markup = product_keyboard(product_type)

    message = PRODUCT_MESSAGES.get(product_type, "Select a product:")

    await query.edit_message_text(
        text=message,
        reply_markup=reply_markup
    )
    return QUANTITY_INPUT

async def handle_quantity(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle product quantity selection"""
    query = update.callback_query
    await query.answer()

    _, product_type, amount = query.data.split('_')

    context.user_data['selected_product'] = {
        'type': product_type,
        'amount': amount
    }

    product_names = {
        'netflix': f"${amount} Netflix Gift Card",
        'riot': f"{amount} Riot Points",
        'pubg': f"{amount} UC",
        'ps': f"${amount} PlayStation Card",
        'razer': f"${amount} Razer Gold",
        'milli': f"{amount} Adet Milli Piyango"
    }

    product_name = product_names.get(product_type, "Selected product")

    await query.edit_message_text(
        text=f"Selected: {product_name}\n\n"
             f"Please select quantity or add to cart:",
        reply_markup=quantity_keyboard(product_type)
    )
    return PAYMENT_SELECTION
