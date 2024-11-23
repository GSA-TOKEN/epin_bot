# E-Pin Shop Telegram Bot

A comprehensive Telegram bot designed for purchasing digital gift cards and game currencies.

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

- **Edit the `.env` file:**

  **Required:**
  - `BOT_TOKEN=your_telegram_bot_token`

  **Optional (default is INFO):**
  - `LOG_LEVEL=DEBUG`  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL

### Project Structure

- **bot/**
  - `config/` - Configuration settings
  - `handlers/` - Telegram command/callback handlers
  - `messages/` - Message templates
  - `utils/` - Utility functions
  - `main.py` - Bot entry point

## Key Features

- Browse digital products
- Multi-step purchase process
- View order history
- Access support system
- Generate and deliver codes

## Command Overview

- `/start` - Initialize or restart the bot
- `/help` - Display help information
- `/cancel` - Cancel the current operation

## Logging Configuration

The bot utilizes Python's logging system with the following levels:

- `DEBUG`: Detailed information for debugging (development)
- `INFO`: General operational information (production default)
- `WARNING`: Unexpected but handled situations
- `ERROR`: Serious issues that need attention
- `CRITICAL`: Critical failures

**Configure logging in `.env`:**

- **Development:**
  - `LOG_LEVEL=DEBUG`
- **Production:**
  - `LOG_LEVEL=INFO`

## Message Templates

Message templates are located in `messages/templates.py`.

## Conversation Flow

The bot employs a ConversationHandler with states defined in `main.py`.

## Development Instructions

1. **Create a Test Bot:**
   - Use @BotFather to create a test bot.

2. **Enable Detailed Logs:**
   - Set `LOG_LEVEL=DEBUG` in `.env`.

3. **Run the Bot:**
   ```bash
   python main.py
   ```

## Production Deployment

1. **Set Logging Level:**
   - Ensure `LOG_LEVEL=INFO` is set in `.env`.

2. **Run with a Process Manager:**
   ```bash
   pm2 start main.py --name epin-bot
   ```
