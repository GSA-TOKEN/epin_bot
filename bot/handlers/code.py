from telegram import Update
from telegram.ext import ContextTypes
import aiohttp
from config.settings import API_BASE_URL

async def view_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_BASE_URL}/codes/{context.user_data.get('code_id')}") as response:
            if response.status == 200:
                code_data = await response.json()
                await update.message.reply_text(f"Your code: {code_data['code']}")
            else:
                await update.message.reply_text("Failed to retrieve code")

async def copy_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_BASE_URL}/codes/{context.user_data.get('code_id')}") as response:
            if response.status == 200:
                code_data = await response.json()
                await update.message.reply_text(
                    f"Code copied: {code_data['code']}\n"
                    "You can now paste it in your game/application"
                )
            else:
                await update.message.reply_text("Failed to retrieve code")
