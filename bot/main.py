from telegram import Update
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, ConversationHandler
)
from config.settings import BOT_TOKEN, LOG_LEVEL
from config.states import (
    MAIN_MENU, CATEGORY_SELECTION, PRODUCT_SELECTION, 
    QUANTITY_INPUT, PAYMENT_SELECTION, ORDER_CONFIRMATION
)
from handlers import (
    start, help_menu, main_menu, show_categories, show_products, 
    show_orders, handle_quantity, handle_payment, handle_order_confirmation, 
    view_code, copy_code, help_command, cancel, return_to_menu
)
import logging

def main():
    """Start the bot."""
    # Configure logging
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=getattr(logging, LOG_LEVEL)
    )

    # Build application
    application = Application.builder().token(BOT_TOKEN).build()

    # Add conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            MAIN_MENU: [
                CallbackQueryHandler(main_menu, pattern="^browse$"),
                CallbackQueryHandler(show_orders, pattern="^orders$"),
                CallbackQueryHandler(help_menu, pattern="^help$"),
                CallbackQueryHandler(return_to_menu, pattern="^start$"),
                CallbackQueryHandler(view_code, pattern="^view_code"),
                CallbackQueryHandler(copy_code, pattern="^copy_code")
            ],
            CATEGORY_SELECTION: [
                CallbackQueryHandler(show_categories, pattern="^category_"),
                CallbackQueryHandler(return_to_menu, pattern="^start$")
            ],
            PRODUCT_SELECTION: [
                CallbackQueryHandler(show_products, pattern="^product_"),
                CallbackQueryHandler(main_menu, pattern="^browse$")
            ],
            QUANTITY_INPUT: [
                CallbackQueryHandler(show_categories, pattern="^category_"),
                CallbackQueryHandler(handle_quantity, pattern="^buy_"),
                CallbackQueryHandler(show_products, pattern="^product_")
            ],
            PAYMENT_SELECTION: [
                CallbackQueryHandler(handle_payment, pattern="^qty_"),
                CallbackQueryHandler(handle_quantity, pattern="^buy_"),
                CallbackQueryHandler(handle_payment, pattern="^confirm_purchase$")
            ],
            ORDER_CONFIRMATION: [
                CallbackQueryHandler(handle_order_confirmation, pattern="^pay_"),
                CallbackQueryHandler(handle_quantity, pattern="^buy_")
            ]
        },
        fallbacks=[
            CommandHandler("start", start),
            CommandHandler("help", help_command),
            CommandHandler("cancel", cancel)
        ],
    )

    application.add_handler(conv_handler)

    # Start the Bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
