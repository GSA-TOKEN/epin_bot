# handlers/code_handlers.py

from telegram import Update
from telegram.ext import ContextTypes
from keyboards import code_view_keyboard
from utils import generate_code
from config import MAIN_MENU

async def view_code(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle code viewing"""
    query = update.callback_query
    await query.answer()

    code = generate_code()

    await query.edit_message_text(
        text=f"🎮 Your Code:\n\n"
             f"`{code}`\n\n"
             f"⚠️ Important:\n"
             f"• Keep this code secure\n"
             f"• Do not share with others\n"
             f"• Code can only be used once",
        reply_markup=code_view_keyboard(),
        parse_mode='MarkdownV2'
    )
    return MAIN_MENU

async def copy_code(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle code copying"""
    query = update.callback_query
    await query.answer("Code copied to clipboard!", show_alert=True)
    return MAIN_MENU
