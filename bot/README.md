# E-Pin Shop Telegram Bot

A comprehensive Telegram bot for purchasing digital gift cards and game currencies with cryptocurrency support.

## Quick Start Guide

### Environment Setup

1. **Create a Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # For Windows: venv\Scripts\activate
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Configuration

Create a `.env` file with the following:

```plaintext
# Bot Configuration
BOT_TOKEN=
LOG_LEVEL=DEBUG
ADMIN_TELEGRAM_ID=
API_BASE_URL=http://localhost:8000/api
SUPPORT_ADMIN=@support_admin

# Payment Configuration
UNLIMIT_PROVIDER_TOKEN=
TON_WALLET_ADDRESS=
TON_TESTNET=true
TON_API_KEY=
```

### Project Structure

- **bot/**
  - `config/` - Configuration settings
  - `handlers/` - Telegram command/callback handlers
  - `messages/` - Message templates
  - `utils/` - Utility functions
  - `ton/` - TON blockchain integration
  - `main.py` - Bot entry point

## Key Features

- Browse digital products
- Cryptocurrency payments (TON)
- Multi-step purchase process
- Order history
- Support system
- Automatic code delivery

## Payment Methods

- TON Cryptocurrency
- Support for both mainnet and testnet
- Automatic payment verification

## Development Instructions

1. **Create Test Wallets:**
   - Set up TON testnet wallet
   - Configure test payment provider

2. **Enable Debug Mode:**
   - Set `LOG_LEVEL=DEBUG`
   - Set `TON_TESTNET=true`

3. **Run the Bot:**
   ```bash
   python main.py
   ```

## Production Deployment

1. **Configure Production Settings:**
   ```plaintext
   LOG_LEVEL=INFO
   TON_TESTNET=false
   ```

2. **Run with Process Manager:**
   ```bash
   pm2 start main.py --name epin-bot
   ```

## Security Considerations

- Secure storage of wallet keys
- Regular monitoring of transactions
- Proper session management
