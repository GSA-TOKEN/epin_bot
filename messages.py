# messages.py

WELCOME_MESSAGE = (
    "Welcome to E-Pin Shop! 🎮\n\n"
    "Your destination for Netflix, Riot, Milli Piyango, PS, Razer Gold, and PUBG codes."
)

HELP_MESSAGE = "Need help with your purchase? Contact our support team!"

PRODUCT_MESSAGES = {
    'netflix': "Select a Netflix Gift Card:",
    'riot': "Select Riot Points amount:",
    'pubg': "Select PUBG UC amount:",
    'ps': "Select PlayStation Card value:",
    'razer': "Select Razer Gold value:",
    'milli': "Select Milli Piyango amount:",
}

ORDER_SUCCESS_MESSAGE = lambda product_type, amount, quantity, payment_method: (
    f"🎉 Order Successful!\n\n"
    f"Your order for {quantity}x {product_type.title()} {amount} "
    f"has been confirmed.\n\n"
    f"Payment method: {payment_method.title()}\n\n"
    f"You can view your code(s) in My Orders."
)
