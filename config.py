# config.py

import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
print(f"Current BOT_TOKEN: {BOT_TOKEN}")

# Logging setup
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Conversation states
MAIN_MENU, CATEGORY_SELECTION, PRODUCT_SELECTION, QUANTITY_INPUT, PAYMENT_SELECTION, ORDER_CONFIRMATION = range(6)
