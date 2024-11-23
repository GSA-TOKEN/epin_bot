from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def orders_keyboard():
    keyboard = [
        [InlineKeyboardButton("View Code", callback_data='view_code_1')],
        [InlineKeyboardButton("⬅️ Back to Menu", callback_data='start')]
    ]
    return InlineKeyboardMarkup(keyboard)

def code_view_keyboard():
    keyboard = [
        [InlineKeyboardButton("📋 Copy Code", callback_data='copy_code')],
        [InlineKeyboardButton("⬅️ Back to Orders", callback_data='orders')]
    ]
    return InlineKeyboardMarkup(keyboard)
