from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from keyboards import category_keyboard, main_menu_keyboard
from config.settings import TON_WALLET_ADDRESS
from config import MAIN_MENU
import logging
import random
from utils.db import create_order, update_order_status, get_order, get_product_codes, get_order_codes
import asyncio
from .command import cancel  # Import the existing cancel handler
from decimal import Decimal
from datetime import datetime, timedelta
from typing import Optional
from utils.logger import setup_logger
from exchange_service import get_ton_price
from ton_service import TONService

logger = setup_logger()

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
        
        logger.info(f"TON payment initiated: {payment_id} for {final_price} TON")
        
    except ValueError as e:
        logger.error(f"Price calculation error: {e}")
        await query.edit_message_text("Invalid price format. Please try again.")
        return MAIN_MENU
    except Exception as e:
        logger.error(f"Payment error: {str(e)}")
        await query.edit_message_text(
            "Payment service error. Please try again later.\n"
            f"Error: {str(e)}"
        )
        return MAIN_MENU
    
    return MAIN_MENU



async def check_ton_payment(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Check TON payment status"""
    try:
        logger.info("Starting check_ton_payment function")
        query = update.callback_query
        await query.answer()
        
        payment_id = query.data.split('_')[2]
        stored_payment_id = context.user_data.get('payment_id')
        product = context.user_data.get('selected_product', {})
        quantity = context.user_data.get('quantity', 1)
        
        logger.info(f"Payment check details:")
        logger.info(f"Payment ID: {payment_id}")
        logger.info(f"Stored Payment ID: {stored_payment_id}")
        logger.info(f"Product: {product}")
        logger.info(f"Quantity: {quantity}")
        
        if payment_id != str(stored_payment_id):
            logger.error(f"Payment ID mismatch: {payment_id} != {stored_payment_id}")
            await query.edit_message_text(
                "❌ Invalid payment verification request.",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("⬅️ Back to Menu", callback_data='menu')
                ]])
            )
            return MAIN_MENU
        
        # Get real-time TON price
        ton_rate = await get_ton_price()
        logger.info(f"Current TON rate: {ton_rate}")
        
        price_in_usd = Decimal(product.get('amount').replace('$', ''))
        price_in_ton = price_in_usd / ton_rate
        final_price = price_in_ton * Decimal(str(quantity))
        
        logger.info(f"Price calculations:")
        logger.info(f"Price in USD: ${price_in_usd}")
        logger.info(f"Price in TON: {price_in_ton}")
        logger.info(f"Final price: {final_price} TON")
        
        # Create pending order
        order_id = await create_order(
            user_id=update.effective_user.id,
            product_type=product.get('type'),
            quantity=quantity,
            payment_method='ton',
            payment_id=payment_id,
            amount_ton=float(final_price),
            amount_usd=float(price_in_usd * quantity),
            status='pending'
        )
        
        if not order_id:
            logger.error("Failed to create order in database")
            raise Exception("Failed to create order")
            
        logger.info(f"Created order with ID: {order_id}")
        
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
        logger.error(f"Error in check_ton_payment: {str(e)}", exc_info=True)
        await query.edit_message_text(
            "❌ Error processing payment verification.\n"
            "Please try again or contact support.",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("⬅️ Back to Menu", callback_data='menu')
            ]])
        )
        return MAIN_MENU
    
    return MAIN_MENU



async def verify_ton_transaction(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    payment_id: str,
    order_id: int,
    expected_amount: Decimal
) -> None:
    """Verify TON transaction and deliver codes if successful"""
    ton_service = TONService()
    attempt = 0
    max_attempts = 12  # 2 minutes (12 * 10 seconds)
    
    while attempt < max_attempts:
        try:
            # Check for payment using verify_payment instead of check_payment
            payment_result = await ton_service.verify_payment(
                payment_id=payment_id,
                expected_amount=expected_amount
            )
            
            if payment_result["verified"]:
                # Update order status
                await update_order_status(order_id, "completed")
                
                # Get codes for the order
                codes_response = await get_order_codes(order_id)
                
                if not codes_response:
                    logger.error(f"No codes found for order {order_id}")
                    raise Exception("No codes found for order")
                
                # Store codes in user_data for copy functionality
                context.user_data['order_codes'] = [code['code'] for code in codes_response]
                
                # Format codes message with copy buttons
                codes_message = "✅ Payment confirmed!\n\nHere are your codes:\n\n"
                keyboard = []
                
                for idx, code in enumerate(codes_response, 1):
                    codes_message += f"{idx}. `{code['code']}`\n"
                    keyboard.append([
                        InlineKeyboardButton(
                            f"📋 Copy Code #{idx}", 
                            callback_data=f'copy_code_{order_id}_{idx-1}'
                        )
                    ])
                
                codes_message += "\n📝 Save these codes safely!"
                
                # Add back to menu button
                keyboard.append([
                    InlineKeyboardButton("⬅️ Back to Menu", callback_data='menu')
                ])
                
                # Send codes to user
                await update.callback_query.edit_message_text(
                    text=codes_message,
                    parse_mode='Markdown',
                    reply_markup=InlineKeyboardMarkup(keyboard)
                )
                return
            
            # Payment not found yet
            attempt += 1
            await asyncio.sleep(10)
            
        except Exception as e:
            logger.error(f"Error in verify_ton_transaction: {e}", exc_info=True)
            attempt += 1
            await asyncio.sleep(10)
    
    # Verification failed after max attempts
    await update_order_status(order_id, "failed")
    await update.callback_query.edit_message_text(
        f"❌ Payment verification failed.\n\n"
        f"If you've sent the payment, please contact support with your Order ID: #{order_id}",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("⬅️ Back to Menu", callback_data='menu')
        ]])
    )

# Add new handler for copying individual codes
async def copy_code(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle copying individual codes"""
    query = update.callback_query
    
    try:
        # Parse callback data (format: copy_code_24_0)
        callback_parts = query.data.split('_')
        if len(callback_parts) != 4:
            raise ValueError("Invalid callback data format")
            
        order_id = callback_parts[2]
        code_index = int(callback_parts[3])
        
        # Get code from user_data
        codes = context.user_data.get('order_codes', [])
        if not codes or code_index >= len(codes):
            logger.error(f"Code not found: order_id={order_id}, index={code_index}")
            await query.answer("❌ Error: Code not found")
            return
            
        code = codes[code_index]
        
        # Send code in an easily copyable format
        await query.message.reply_text(
            "📋 Double tap the code below to copy:\n"
            "━━━━━━━━━━━━━━━━━━━━━\n"
            f"`{code}`\n"
            "━━━━━━━━━━━━━━━━━━━━━",
            parse_mode='Markdown'
        )
        
        # Notify user
        await query.answer("✨ Code ready to copy!")
        
    except Exception as e:
        logger.error(f"Error in copy_code: {e}")
        await query.answer("❌ Error retrieving code")
