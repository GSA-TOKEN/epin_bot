# keyboards.py

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("🛍 Browse Products", callback_data='browse')],
        [InlineKeyboardButton("📦 My Orders", callback_data='orders')],
        [InlineKeyboardButton("❓ Help", callback_data='help')]
    ]
    return InlineKeyboardMarkup(keyboard)

def category_keyboard():
    keyboard = [
        [InlineKeyboardButton("💳 E-Pins", callback_data='category_epins')],
        [InlineKeyboardButton("🎮 Game Codes", callback_data='category_games')],
        [InlineKeyboardButton("🎁 Special Offers", callback_data='category_special')],
        [InlineKeyboardButton("⬅️ Back", callback_data='start')]
    ]
    return InlineKeyboardMarkup(keyboard)

def epins_category_keyboard():
    keyboard = [
        [InlineKeyboardButton("Netflix Codes", callback_data='product_netflix')],
        [InlineKeyboardButton("Riot Games Codes", callback_data='product_riot')],
        [InlineKeyboardButton("Milli Piyango", callback_data='product_milli')],
        [InlineKeyboardButton("PlayStation Codes", callback_data='product_ps')],
        [InlineKeyboardButton("Razer Gold", callback_data='product_razer')],
        [InlineKeyboardButton("PUBG", callback_data='product_pubg')],
        [InlineKeyboardButton("⬅️ Back", callback_data='browse')]
    ]
    return InlineKeyboardMarkup(keyboard)

def games_category_keyboard():
    keyboard = [
        [InlineKeyboardButton("Steam Games", callback_data='product_steam')],
        [InlineKeyboardButton("Xbox Games", callback_data='product_xbox')],
        [InlineKeyboardButton("PlayStation Games", callback_data='product_psn')],
        [InlineKeyboardButton("⬅️ Back", callback_data='browse')]
    ]
    return InlineKeyboardMarkup(keyboard)

def special_offers_keyboard():
    keyboard = [
        [InlineKeyboardButton("Weekly Deals", callback_data='product_weekly')],
        [InlineKeyboardButton("Flash Sales", callback_data='product_flash')],
        [InlineKeyboardButton("Bundle Offers", callback_data='product_bundle')],
        [InlineKeyboardButton("⬅️ Back", callback_data='browse')]
    ]
    return InlineKeyboardMarkup(keyboard)

def product_keyboard(product_type):
    keyboards = {
        'netflix': [
            [InlineKeyboardButton("$10 Netflix Gift Card", callback_data='buy_netflix_10')],
            [InlineKeyboardButton("$25 Netflix Gift Card", callback_data='buy_netflix_25')],
            [InlineKeyboardButton("⬅️ Back", callback_data='category_epins')]
        ],
        'riot': [
            [InlineKeyboardButton("1000 Riot Points", callback_data='buy_riot_1000')],
            [InlineKeyboardButton("2000 Riot Points", callback_data='buy_riot_2000')],
            [InlineKeyboardButton("⬅️ Back", callback_data='category_epins')]
        ],
        'pubg': [
            [InlineKeyboardButton("600 UC", callback_data='buy_pubg_600')],
            [InlineKeyboardButton("1500 UC", callback_data='buy_pubg_1500')],
            [InlineKeyboardButton("⬅️ Back", callback_data='category_epins')]
        ],
        'ps': [
            [InlineKeyboardButton("$10 PlayStation Card", callback_data='buy_ps_10')],
            [InlineKeyboardButton("$20 PlayStation Card", callback_data='buy_ps_20')],
            [InlineKeyboardButton("⬅️ Back", callback_data='category_epins')]
        ],
        'razer': [
            [InlineKeyboardButton("$10 Razer Gold", callback_data='buy_razer_10')],
            [InlineKeyboardButton("$25 Razer Gold", callback_data='buy_razer_25')],
            [InlineKeyboardButton("⬅️ Back", callback_data='category_epins')]
        ],
        'milli': [
            [InlineKeyboardButton("1 Adet Milli Piyango", callback_data='buy_milli_1')],
            [InlineKeyboardButton("5 Adet Milli Piyango", callback_data='buy_milli_5')],
            [InlineKeyboardButton("⬅️ Back", callback_data='category_epins')]
        ],
        'steam': [
            [InlineKeyboardButton("$20 Steam Wallet", callback_data='buy_steam_20')],
            [InlineKeyboardButton("$50 Steam Wallet", callback_data='buy_steam_50')],
            [InlineKeyboardButton("⬅️ Back", callback_data='category_games')]
        ],
        'xbox': [
            [InlineKeyboardButton("$25 Xbox Gift Card", callback_data='buy_xbox_25')],
            [InlineKeyboardButton("$50 Xbox Gift Card", callback_data='buy_xbox_50')],
            [InlineKeyboardButton("⬅️ Back", callback_data='category_games')]
        ],
        'weekly': [
            [InlineKeyboardButton("30% Off Bundle", callback_data='buy_weekly_30')],
            [InlineKeyboardButton("50% Off Bundle", callback_data='buy_weekly_50')],
            [InlineKeyboardButton("⬅️ Back", callback_data='category_special')]
        ]
    }
    return InlineKeyboardMarkup(keyboards.get(product_type, []))

def quantity_keyboard(product_type):
    keyboard = [
        [InlineKeyboardButton("1", callback_data='qty_1'),
         InlineKeyboardButton("2", callback_data='qty_2'),
         InlineKeyboardButton("3", callback_data='qty_3')],
        [InlineKeyboardButton("4", callback_data='qty_4'),
         InlineKeyboardButton("5", callback_data='qty_5'),
         InlineKeyboardButton("6", callback_data='qty_6')],
        [InlineKeyboardButton("🛒 Add to Cart", callback_data='confirm_purchase')],
        [InlineKeyboardButton("⬅️ Back", callback_data=f'product_{product_type}')]
    ]
    return InlineKeyboardMarkup(keyboard)

def payment_methods_keyboard(product_type, amount):
    keyboard = [
        [InlineKeyboardButton("💳 Credit Card", callback_data='pay_card')],
        [InlineKeyboardButton("₿ Cryptocurrency", callback_data='pay_crypto')],
        [InlineKeyboardButton("💰 Balance", callback_data='pay_balance')],
        [InlineKeyboardButton("⬅️ Back", callback_data=f'buy_{product_type}_{amount}')]
    ]
    return InlineKeyboardMarkup(keyboard)

def orders_keyboard():
    keyboard = [
        [InlineKeyboardButton("View Code", callback_data='view_code_1')],
        [InlineKeyboardButton("⬅️ Back to Home", callback_data='start')]
    ]
    return InlineKeyboardMarkup(keyboard)

def code_view_keyboard():
    keyboard = [
        [InlineKeyboardButton("📋 Copy Code", callback_data='copy_code')],
        [InlineKeyboardButton("⬅️ Back to Orders", callback_data='orders')]
    ]
    return InlineKeyboardMarkup(keyboard)
