from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from keyboards import main_menu_keyboard, orders_keyboard
from messages import HELP_MESSAGE
from config import MAIN_MENU

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show help information"""
    await update.message.reply_text(
        HELP_MESSAGE,
        reply_markup=main_menu_keyboard()
    )
    return MAIN_MENU

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancel current operation and return to main menu"""
    await update.message.reply_text(
        "Operation cancelled. Returning to main menu...",
        reply_markup=main_menu_keyboard()
    )
    return MAIN_MENU