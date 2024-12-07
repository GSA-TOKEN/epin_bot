# handlers/start_handlers.py

from telegram import Update
from telegram.ext import ContextTypes
from keyboards import main_menu_keyboard
from messages import WELCOME_MESSAGE, HELP_MESSAGE
from config import MAIN_MENU
from utils.db import register_user
import logging

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Welcome screen handler"""
    user = update.effective_user
    
    # Register user
    success = await register_user(
        user_id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name
    )
    
    if not success:
        logger.error(f"Failed to register user {user.id}")
    
    await update.message.reply_text(
        WELCOME_MESSAGE,
        reply_markup=main_menu_keyboard()
    )
    return MAIN_MENU

async def help_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Help menu handler"""
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        text=HELP_MESSAGE,
        reply_markup=main_menu_keyboard()
    )
    return MAIN_MENU

async def return_to_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Return to main menu handler"""
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text(
        text=WELCOME_MESSAGE,
        reply_markup=main_menu_keyboard()
    )
    return MAIN_MENU
