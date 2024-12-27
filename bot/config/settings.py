from os import getenv
from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = getenv("BOT_TOKEN")
ADMIN_TELEGRAM_ID = getenv("ADMIN_TELEGRAM_ID")
SUPPORT_ADMIN = getenv("SUPPORT_ADMIN")
API_BASE_URL = getenv("API_BASE_URL", "http://localhost:8000/api")
LOG_LEVEL = getenv("LOG_LEVEL", "INFO")
UNLIMIT_PROVIDER_TOKEN = getenv("UNLIMIT_PROVIDER_TOKEN")
TON_WALLET_ADDRESS = getenv('TON_WALLET_ADDRESS')
TON_TESTNET = getenv('TON_TESTNET').lower() == 'true'
TON_API_KEY = getenv('TON_API_KEY')

# WebApp Configuration
WEBAPP_URL = os.getenv('WEBAPP_URL', 'https://your-domain.com/webapp')