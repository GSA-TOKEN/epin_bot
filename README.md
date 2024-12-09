# E-Pin Shop

Welcome to the E-Pin Shop, a digital marketplace for gift cards and game currencies, powered by a FastAPI backend and a Telegram bot interface.

## Project Overview

The E-Pin Shop is composed of two primary components:

1. **FastAPI Backend**: Manages database operations, user management, and business logic.
2. **Telegram Bot**: Serves as the user interface for browsing and purchasing digital products.

## Technology Stack

- **Backend Technologies:**
  - **FastAPI**: Web framework for building APIs
  - **SQLAlchemy**: Object-Relational Mapping (ORM) tool
  - **Alembic**: Database migration tool
  - **Supabase**: Database service
  - **Pydantic**: Data validation and settings management

- **Bot Technologies:**
  - **python-telegram-bot**: Library for building Telegram bots
  - **Python asyncio**: Asynchronous programming support
  - **TON Payments**: Cryptocurrency payment integration
  - **State Management**: Manages bot states and transitions
  - **Message Templates**: Predefined message formats for user interaction

## Quick Start Guide

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/bartusisman/epin_bot
   cd epin-shop
   ```

2. **Set Up a Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # For Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r bot/requirements.txt -r backend/requirements.txt
   ```

4. **Configure Environment Variables:**

   Create `.env` files in both `/bot` and `/backend` directories:

   **Backend `.env**:**
   ```plaintext
   # PostgreSQL (Supabase)
   POSTGRES_USER=
   POSTGRES_PASSWORD
   POSTGRES_SERVER=
   POSTGRES_PORT=6543
   POSTGRES_DB=postgres
   DATABASE_URL=postgresql:

   # Security
   SECRET_KEY=your-secret-key
   ACCESS_TOKEN_EXPIRE_MINUTES=30

   # Admin Configuration
   ADMIN_TELEGRAM_ID=your_admin_telegram_id
   ```

   **Bot `.env**:**
   ```plaintext
   BOT_TOKEN=
   LOG_LEVEL=DEBUG
   ADMIN_TELEGRAM_ID=
   API_BASE_URL=http://localhost:8000/api
   SUPPORT_ADMIN=@support_admin
   
   # Payment Configuration
   UNLIMIT_PROVIDER_TOKEN=
   TON_WALLET_ADDRES
   TON_TESTNET=true
   TON_API_KEY
   ```

5. **Launch the Applications:**

   Start Backend:
   ```bash
   cd backend
   uvicorn main:app --reload
   ```

   Start Bot:
   ```bash
   cd bot
   python main.py
   ```

## Documentation

- Backend API documentation: [http://localhost:8000/docs](http://localhost:8000/docs)
- Detailed setup instructions:
  - [Backend README](backend/README.md)
  - [Bot README](bot/README.md)

## Security Notes

- Never commit `.env` files to version control
- Keep your TON wallet private key secure
- Regularly rotate API keys and tokens

## Project Structure
