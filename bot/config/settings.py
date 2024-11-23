import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot settings
BOT_TOKEN = os.getenv('BOT_TOKEN')
SUPPORT_ADMIN = "@support_admin"

# Logging settings
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
