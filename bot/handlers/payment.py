from telegram import Update
from telegram.ext import ContextTypes
from keyboards import payment_methods_keyboard, orders_keyboard
from messages import ORDER_SUCCESS_MESSAGE
from config import ORDER_CONFIRMATION, PAYMENT_SELECTION, MAIN_MENU
from .unlimit import handle_unlimit_payment

async def handle_payment(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle payment selection"""
    query = update.callback_query
    await query.answer()

    if query.data.startswith('qty_'):
        quantity = int(query.data.split('_')[1])
        context.user_data['quantity'] = quantity

        product = context.user_data.get('selected_product', {})
        product_type = product.get('type')
        amount = product.get('amount')

        await query.edit_message_text(
            text=f"Order Summary:\n"
                 f"Product: {product_type.title()} {amount}\n"
                 f"Quantity: {quantity}\n\n"
                 f"Please select your payment method:",
            reply_markup=payment_methods_keyboard(product_type, amount)
        )
        return ORDER_CONFIRMATION

    return PAYMENT_SELECTION

async def handle_order_confirmation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle order confirmation"""
    query = update.callback_query
    await query.answer()

    if query.data == 'pay_unlimit':
        return await handle_unlimit_payment(update, context)
    elif query.data.startswith('pay_'):
        payment_method = query.data.split('_')[1]
        product = context.user_data.get('selected_product', {})
        quantity = context.user_data.get('quantity', 1)

        await query.edit_message_text(
            text=ORDER_SUCCESS_MESSAGE(product['type'], product['amount'], quantity, payment_method),
            reply_markup=orders_keyboard()
        )
        return MAIN_MENU

    return ORDER_CONFIRMATION
