# E-Pin Shop

Welcome to the E-Pin Shop, a digital marketplace for gift cards and game currencies, powered by a FastAPI backend and a Telegram bot interface.

## Project Overview

The E-Pin Shop is composed of two primary components:

1. **FastAPI Backend**: Manages database operations, user management, and business logic.
2. **Telegram Bot**: Serves as the user interface for browsing and purchasing digital products.

## Technology Stack

- **Backend Technologies:**
  - **FastAPI**: Web framework for building APIs.
  - **SQLAlchemy**: Object-Relational Mapping (ORM) tool.
  - **Alembic**: Database migration tool.
  - **Supabase**: Database service.
  - **Pydantic**: Data validation and settings management.

- **Bot Technologies:**
  - **python-telegram-bot**: Library for building Telegram bots.
  - **Python asyncio**: Asynchronous programming support.
  - **State Management**: Manages bot states and transitions.
  - **Message Templates**: Predefined message formats for user interaction.

## Quick Start Guide

Follow these steps to set up and run the E-Pin Shop:

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

   Create `.env` files in both `/bot` and `/backend` directories with the following content:

   **Backend `.env`:**
   ```plaintext
   # PostgreSQL Configuration
   POSTGRES_SERVER=your-server
   POSTGRES_USER=your-user
   POSTGRES_PASSWORD=your-password
   POSTGRES_PORT=your-port
   POSTGRES_DB=your-db
   DATABASE_URL=your-url

   # Security Settings
   SECRET_KEY=your-secret-key
   ACCESS_TOKEN_EXPIRE_MINUTES=30

   # Supabase Configuration
   SUPABASE_URL=your-url
   SUPABASE_KEY=your-key
   ```

   **Bot `.env`:**
   ```plaintext
   BOT_TOKEN=your-telegram-bot-token
   LOG_LEVEL=DEBUG  # Use INFO for production
   ```

5. **Launch the Applications:**

   - **Backend**: Open a terminal and run:
     ```bash
     cd backend
     uvicorn main:app --reload
     ```

   - **Bot**: Open another terminal and run:
     ```bash
     cd bot
     python main.py
     ```

## Documentation

- Access the Backend API documentation at: [http://localhost:8000/docs](http://localhost:8000/docs)
- For detailed setup instructions, refer to:
  - [Backend README](backend/README.md)
  - [Bot README](bot/README.md)

## Project Structure
