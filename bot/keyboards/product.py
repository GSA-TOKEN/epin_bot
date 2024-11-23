from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from typing import Dict, List

def product_keyboard(product_type: str) -> InlineKeyboardMarkup:
    product_options: Dict[str, List[List[str]]] = {
        'netflix': [['$10', '$25', '$50'], ['$75', '$100']],
        'riot': [['1380', '3500', '5600'], ['7200', '11000']],
        'pubg': [['60', '300', '600'], ['1500', '3000']],
        'ps': [['$10', '$20', '$50'], ['$75', '$100']],
        'razer': [['$10', '$20', '$50'], ['$75', '$100']],
        'milli': [['1', '2', '5'], ['10', '20']]
    }
    
    keyboard = []
    for row in product_options.get(product_type, []):
        keyboard.append([
            InlineKeyboardButton(
                f"{amount}", 
                callback_data=f'buy_{product_type}_{amount}'
            ) for amount in row
        ])
    
    keyboard.append([InlineKeyboardButton("⬅️ Back", callback_data='category_epins')])
    return InlineKeyboardMarkup(keyboard)
