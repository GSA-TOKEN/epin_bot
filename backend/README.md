# E-Pin Shop API

FastAPI backend with cryptocurrency payment support.

## Quick Start Guide

### Environment Setup

1. **Create a Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

### Configuration

Create a `.env` file:

```plaintext
# PostgreSQL (Supabase)
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_SERVER=
POSTGRES_PORT=6543
POSTGRES_DB=postgres
DATABASE_URL=

# Security
SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Admin Configuration
ADMIN_TELEGRAM_ID=your_admin_telegram_id
```

### Database Management

1. **Run Migrations:**
   ```bash
   alembic upgrade head
   ```

2. **Create New Migration:**
   ```bash
   alembic revision --autogenerate -m "description"
   ```

### Start Development Server

```bash
uvicorn main:app --reload
```

## Key Features

- Cryptocurrency payment processing
- Concurrent order processing
- Automatic code assignment
- User management
- Product management

## API Documentation

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Security Measures

- API key authentication
- Session management
- SQL injection protection
- XSS prevention
