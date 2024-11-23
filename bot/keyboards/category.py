from telegram import InlineKeyboardButton, InlineKeyboardMarkup

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
        [InlineKeyboardButton("Epic Games", callback_data='product_epic')],
        [InlineKeyboardButton("Origin Games", callback_data='product_origin')],
        [InlineKeyboardButton("⬅️ Back", callback_data='browse')]
    ]
    return InlineKeyboardMarkup(keyboard)

def special_offers_keyboard():
    keyboard = [
        [InlineKeyboardButton("Daily Deals", callback_data='product_daily')],
        [InlineKeyboardButton("Bundle Offers", callback_data='product_bundle')],
        [InlineKeyboardButton("Flash Sales", callback_data='product_flash')],
        [InlineKeyboardButton("⬅️ Back", callback_data='browse')]
    ]
    return InlineKeyboardMarkup(keyboard)
