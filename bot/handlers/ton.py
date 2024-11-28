from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from keyboards import category_keyboard, main_menu_keyboard
from config.settings import TON_WALLET_ADDRESS
from config import MAIN_MENU
import logging
import random
from utils.db import create_order, update_order_status, get_order, get_product_codes
import asyncio
from .command import cancel  # Import the existing cancel handler
from decimal import Decimal
from datetime import datetime, timedelta
from typing import Optional
from services.ton_service import TONService  
from services.exchange_service import get_ton_price

async def handle_ton_payment(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle TON cryptocurrency payment"""
    query = update.callback_query
    await query.answer()

    if not context.user_data.get('selected_product'):
        await query.edit_message_text(
            "❌ No product selected. Please start over.",
            reply_markup=main_menu_keyboard()
        )
        return MAIN_MENU

    product = context.user_data.get('selected_product', {})
    quantity = context.user_data.get('quantity', 1)
    
    try:
        # Get real-time TON price
        ton_rate = await get_ton_price()
        price_in_usd = Decimal(product.get('amount').replace('$', ''))
        price_in_ton = price_in_usd / ton_rate
        final_price = price_in_ton * Decimal(str(quantity))
        
        # Set payment expiration (30 minutes)
        payment_expiry = datetime.now() + timedelta(minutes=30)
        context.user_data['payment_expiry'] = payment_expiry
        
        # Generate unique payment ID
        payment_id = random.randint(100000, 999999)
        context.user_data['payment_id'] = payment_id
        
        payment_message = (
            f"💎 TON Payment Details\n\n"
            f"Product: {product.get('type').title()} {product.get('amount')}\n"
            f"Quantity: {quantity}\n"
            f"Total: {final_price:.2f} TON\n\n"
            f"Please send exactly {final_price:.2f} TON to:\n"
            f"`{TON_WALLET_ADDRESS}`\n\n"
            f"📝 Important: Include this code in payment comment:\n"
            f"`{payment_id}`"
        )
        
        # Add expiry time to message
        payment_message += f"\n\n⏰ Payment valid until: {payment_expiry.strftime('%H:%M:%S')}"
        
        # Multiple wallet options
        keyboard = [
            [
                InlineKeyboardButton(
                    "💳 Tonkeeper",
                    url=f"https://app.tonkeeper.com/transfer/{TON_WALLET_ADDRESS}?amount={int(final_price * Decimal('1e9'))}&text={payment_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    "💳 TonHub",
                    url=f"https://tonhub.com/transfer/{TON_WALLET_ADDRESS}?amount={int(final_price * Decimal('1e9'))}&text={payment_id}"
                )
            ],
            [InlineKeyboardButton("✅ I've Sent Payment", callback_data=f'check_ton_{payment_id}')],
            [InlineKeyboardButton("❌ Cancel", callback_data='cancel_payment')]
        ]
        
        await query.edit_message_text(
            text=payment_message,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
        
        logging.info(f"TON payment initiated: {payment_id} for {final_price} TON")
        
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

async def check_ton_payment(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Check TON payment status"""
    query = update.callback_query
    await query.answer()
    
    payment_id = query.data.split('_')[2]
    stored_payment_id = context.user_data.get('payment_id')
    product = context.user_data.get('selected_product', {})
    quantity = context.user_data.get('quantity', 1)
    
    if payment_id != str(stored_payment_id):
        await query.edit_message_text(
            "❌ Invalid payment verification request.",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("⬅️ Back to Menu", callback_data='menu')
            ]])
        )
        return MAIN_MENU
    
    try:
        # Calculate final amount in TON
        price_in_usd = Decimal(product.get('amount').replace('$', ''))
        price_in_ton = price_in_usd * Decimal('0.5')
        final_price = price_in_ton * Decimal(str(quantity))
        
        # Create pending order
        order_id = await create_order(
            user_id=update.effective_user.id,
            product_type=product.get('type'),
            product_amount=product.get('amount'),
            quantity=quantity,
            payment_method='ton',
            payment_id=payment_id,
            amount_ton=final_price,
            amount_usd=price_in_usd * quantity,
            status='pending'
        )
        
        if not order_id:
            raise Exception("Failed to create order")
        
        # Start payment verification task
        context.application.create_task(
            verify_ton_transaction(
                update=update,
                context=context,
                payment_id=payment_id,
                order_id=order_id,
                expected_amount=final_price
            )
        )
        
        await query.edit_message_text(
            "🔄 Payment verification in progress...\n\n"
            "We'll notify you once your payment is confirmed.\n"
            "This usually takes 1-2 minutes.",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("⬅️ Back to Menu", callback_data='menu')
            ]])
        )
        
    except Exception as e:
        logging.error(f"Error initiating payment verification: {e}")
        await query.edit_message_text(
            "❌ Error processing payment verification.\n"
            "Please try again or contact support.",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("⬅️ Back to Menu", callback_data='menu')
            ]])
        )
    
    return MAIN_MENU

async def verify_ton_transaction(update: Update, context: ContextTypes.DEFAULT_TYPE, 
                               payment_id: str, order_id: int, expected_amount: Decimal) -> None:
    """Background task to verify TON transaction"""
    ton_service = TONService()
    max_attempts = 18  # Extended to 3 minutes (18 * 10 seconds)
    
    try:
        for attempt in range(max_attempts):
            order = await get_order(order_id)
            if not order:
                logging.error(f"Order {order_id} not found")
                break
                
            # Check payment expiry
            payment_expiry = context.user_data.get('payment_expiry')
            if payment_expiry and datetime.now() > payment_expiry:
                await update_order_status(order_id, 'expired')
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="❌ Payment time expired.\nPlease start a new order."
                )
                return

            # Verify payment with transaction hash
            payment_data = await ton_service.verify_payment(payment_id, expected_amount)
            if payment_data and payment_data.get('verified'):
                tx_hash = payment_data.get('transaction_hash')
                
                # Update order with transaction hash
                await update_order_status(
                    order_id, 
                    'paid',
                    {'transaction_hash': tx_hash}
                )

                # Get product codes
                codes = await get_product_codes(
                    product_type=order['product_type'],
                    product_amount=order['product_amount'],
                    quantity=order['quantity']
                )
                
                if not codes:
                    await update_order_status(order_id, 'paid')
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"✅ Payment confirmed!\n\n"
                             f"Order ID: #{order_id}\n"
                             f"Your codes will be delivered shortly."
                    )
                    return
                
                # Update order and send codes
                await update_order_status(order_id, 'completed')
                codes_text = "\n".join([f"- `{code}`" for code in codes])
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=f"✅ Payment confirmed!\n\n"
                         f"Order ID: #{order_id}\n"
                         f"Product: {order['product_type'].title()} {order['product_amount']}\n"
                         f"Quantity: {order['quantity']}\n\n"
                         f"Your codes:\n{codes_text}",
                    parse_mode='Markdown'
                )
                return

            if attempt == max_attempts - 1:
                logging.warning(f"Payment verification timeout for order {order_id}")
            
            await asyncio.sleep(10)

        # Payment verification timeout
        await update_order_status(order_id, 'failed')
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="❌ Payment verification failed.\n\n"
                 "If you've sent the payment, please contact support with your Order ID:\n"
                 f"#{order_id}"
        )
        
    except Exception as e:
        logging.error(f"Error in TON transaction verification: {e}")
        await update_order_status(order_id, 'error')
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="❌ An error occurred during payment verification.\n"
                 "Please contact support with your Order ID:\n"
                 f"#{order_id}"
        )
