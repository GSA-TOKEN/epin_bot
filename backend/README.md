# E-Pin Shop API

Welcome to the FastAPI backend for the E-Pin Shop application. This guide will help you set up and run the application efficiently.

## Quick Start Guide

### 1. Environment Setup

- **Create a Virtual Environment:**
  ```bash
  python -m venv venv
  source venv/bin/activate  # For Windows: venv\Scripts\activate
  ```

- **Install Dependencies:**
  ```bash
  pip install -r requirements.txt
  ```

### 2. Configuration

- **Edit the `.env` file:**
  Ensure you provide your database credentials and other necessary configurations.

### 3. Database Initialization

- **Run Database Migrations:**
  ```bash
  alembic upgrade head
  ```

### 4. Start Development Server

- **Launch the Server:**
  ```bash
  uvicorn main:app --reload
  ```

## Database Migrations

Manage your database schema changes with Alembic:

- **Create a New Migration:**
  ```bash
  alembic revision --autogenerate -m "description"
  ```

- **Upgrade to Latest Version:**
  ```bash
  alembic upgrade head
  ```

- **Downgrade One Version:**
  ```bash
  alembic downgrade -1
  ```

- **Check Current Version:**
  ```bash
  alembic current
  ```

## API Documentation

Access the API documentation and base URL:

- **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **API Base URL:** [http://localhost:8000/api/v1](http://localhost:8000/api/v1)
