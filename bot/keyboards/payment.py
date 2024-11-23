from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from typing import List

def payment_methods_keyboard(product_type: str, amount: str) -> InlineKeyboardMarkup:
    keyboard: List[List[InlineKeyboardButton]] = [
        [InlineKeyboardButton("💳 Credit Card", callback_data='pay_card')],
        [InlineKeyboardButton("₿ Cryptocurrency", callback_data='pay_crypto')],
        [InlineKeyboardButton("💰 Balance", callback_data='pay_balance')],
        [InlineKeyboardButton("⬅️ Back", callback_data=f'buy_{product_type}_{amount}')]
    ]
    return InlineKeyboardMarkup(keyboard)

def quantity_keyboard(product_type: str) -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton("1", callback_data='qty_1'),
            InlineKeyboardButton("2", callback_data='qty_2'),
            InlineKeyboardButton("3", callback_data='qty_3')
        ],
        [
            InlineKeyboardButton("4", callback_data='qty_4'),
            InlineKeyboardButton("5", callback_data='qty_5'),
            InlineKeyboardButton("6", callback_data='qty_6')
        ],
        [InlineKeyboardButton("🛒 Add to Cart", callback_data='confirm_purchase')],
        [InlineKeyboardButton("⬅️ Back", callback_data=f'product_{product_type}')]
    ]
    return InlineKeyboardMarkup(keyboard)
