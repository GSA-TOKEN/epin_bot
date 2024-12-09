from telegram import Update
from telegram.ext import ContextTypes
from config.settings import ADMIN_TELEGRAM_ID
import csv
import io
import aiohttp
from config.settings import API_BASE_URL

def is_admin(user_id: int) -> bool:
    """Check if user is an admin"""
    admin_ids = [int(id.strip()) for id in ADMIN_TELEGRAM_ID.split(',')]
    return user_id in admin_ids

async def admin_upload(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("⛔️ This command is only available for administrators.")
        return

    await update.message.reply_text(
        "📤 Please upload a CSV file with the following columns:\n"
        "- product_name\n"
        "- price\n"
        "- pin_code\n\n"
        "Example format:\n"
        "product_name,price,pin_code\n"
        "Game Card A,9.99,ABC123XYZ"
    )

async def handle_csv_upload(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("⛔️ Not authorized")
        return

    if not update.message.document or not update.message.document.file_name.endswith('.csv'):
        await update.message.reply_text("❌ Please upload a CSV file")
        return

    try:
        file = await context.bot.get_file(update.message.document.file_id)
        file_content = await file.download_as_bytearray()
        
        # Validate CSV format
        csv_text = file_content.decode('utf-8')
        csv_file = io.StringIO(csv_text)
        csv_reader = csv.DictReader(csv_file)
        
        required_columns = {'product_name', 'price', 'pin_code'}
        headers = set(next(csv_reader).keys())
        
        if not required_columns.issubset(headers):
            await update.message.reply_text(
                "❌ Invalid CSV format. Required columns:\n"
                "- product_name\n"
                "- price\n"
                "- pin_code"
            )
            return

        # Send to API
        async with aiohttp.ClientSession() as session:
            form_data = aiohttp.FormData()
            form_data.add_field('file', 
                               file_content,
                               filename='upload.csv',
                               content_type='text/csv')
            
            async with session.post(
                f"{API_BASE_URL}/admin/upload-pins",
                data=form_data,
                headers={'telegram_user_id': str(update.effective_user.id)}
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    await update.message.reply_text(
                        f"✅ Upload successful!\n"
                        f"Products created: {result['products_created']}\n"
                        f"Pins uploaded: {result['pins_created']}"
                    )
                else:
                    error_text = await response.text()
                    await update.message.reply_text(f"❌ Upload failed: {error_text}")

    except Exception as e:
        await update.message.reply_text(f"❌ Error processing file: {str(e)}") 