from telegram import LabeledPrice, Update
from telegram.ext import ContextTypes
from config.settings import UNLIMIT_PROVIDER_TOKEN
from config import MAIN_MENU
import logging

async def handle_unlimit_payment(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle Unlimit payment processing"""
    query = update.callback_query
    await query.answer()

    product = context.user_data.get('selected_product', {})
    quantity = context.user_data.get('quantity', 1)
    
    try:
        # Convert price to Turkish Lira (1 USD = 30 TRY)
        # Remove '$' and convert to float
        price_in_usd = float(product.get('amount').replace('$', ''))
        
        # Convert to TRY (minimum amount is 50 kuruş)
        price_in_try = max(50, int(price_in_usd * 30 * 100))  # Convert to kuruş
        final_price = price_in_try * quantity
        
        # Ensure minimum amount requirement is met
        if final_price < 50:
            final_price = 50
            
        logging.info(f"Price calculation: USD {price_in_usd} -> TRY {final_price/100} (kuruş: {final_price})")

        chat_id = update.effective_chat.id
        title = f"{product.get('type', 'Product').title()} {product.get('amount', '')}"
        description = f"Quantity: {quantity} - Total: {final_price/100} TRY"
        payload = f"product_{product.get('type')}_{product.get('amount')}_{quantity}"
        currency = "TRY"
        prices = [LabeledPrice("Product", final_price)]

        await context.bot.send_invoice(
            chat_id=chat_id,
            title=title,
            description=description,
            payload=payload,
            provider_token=UNLIMIT_PROVIDER_TOKEN,
            currency=currency,
            prices=prices,
            need_name=True,
            need_phone_number=True,
            need_email=True,
            start_parameter="unlimit-payment"
        )
        logging.info("Invoice sent successfully")
        
    except ValueError as e:
        logging.error(f"Price calculation error: {e}")
        await query.edit_message_text("Invalid price format. Please try again.")
        return MAIN_MENU
    except Exception as e:
        logging.error(f"Payment error: {str(e)}")
        await query.edit_message_text(
            "Payment service error. Please try again later.\n"
            f"Error: {str(e)}"
        )
        return MAIN_MENU
    
    return MAIN_MENU

async def precheckout_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the pre-checkout callback"""
    query = update.pre_checkout_query
    
    try:
        await query.answer(ok=True)
    except Exception as e:
        logging.error(f"Error in pre-checkout: {e}")
        await query.answer(ok=False, error_message="Payment processing failed")

async def successful_payment_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle successful payment"""
    payment = update.message.successful_payment
    
    try:
        product_type, amount, quantity = payment.invoice_payload.split('_')[1:]
        await update.message.reply_text(
            f"Payment successful! 🎉\n\n"
            f"Product: {product_type.title()} {amount}\n"
            f"Quantity: {quantity}\n"
            f"Total Paid: {payment.total_amount / 100} {payment.currency}\n\n"
            f"Your code(s) will be delivered shortly."
        )
    except Exception as e:
        logging.error(f"Error processing successful payment: {e}")
        await update.message.reply_text("Payment received. Processing your order...")