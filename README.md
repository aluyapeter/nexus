# Nexus: Google OAuth2 & Paystack Integration

Nexus is a robust fintech backend demonstration built with **FastAPI**. It features secure Google authentication (OAuth2), idempotent payment processing with **Paystack**, and real-time transaction updates via cryptographic webhooks.

## 🚀 Features

* **Authentication:** Google OAuth2 (Authorization Code Flow) with HTTP-only Cookies.
* **Payments:** Paystack integration with idempotent transaction initiation.
* **Webhooks:** Secure signature verification (HMAC SHA512) for payment status updates.
* **Database:** PostgreSQL with SQLAlchemy ORM and Alembic migrations.
* **Testing:** Full integration testing suite using `pytest` and SQLite.
* **Frontend:** Minimalist dashboard for user interaction.

---

## 🛠️ Prerequisites

* Python 3.10+
* PostgreSQL (Local installation OR Docker)
* Paystack Account (Test Keys)
* Google Cloud Console Project (OAuth Credentials)

---

## 🔑 Environment Setup

Create a `.env` file in the root directory:

```ini
# Database
DATABASE_URL=postgresql://nexus_user:nexus_password@localhost:5432/nexus_db

# Google Auth
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_REDIRECT_URI=http://localhost:8000/auth/google/callback

# Paystack
PAYSTACK_SECRET_KEY=sk_test_your_paystack_secret

# Security
SECRET_KEY=your_random_secret_string
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ENVIRONMENT=development
```

## 🏃 Option A: Running Locally (No Docker)

If you prefer to run directly on your machine, follow these steps.

### 1. Database Setup
You must have PostgreSQL running locally.

```bash
# (Linux/WSL) Install Postgres
sudo apt update && sudo apt install postgresql postgresql-contrib

# Switch to postgres user
sudo -i -u postgres

# Create User and DB
psql -c "CREATE USER nexus_user WITH PASSWORD 'nexus_password';"
psql -c "CREATE DATABASE nexus_db OWNER nexus_user;"
exit
```

## 2. Install Dependencies
```bash

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install libraries
pip install -r requirements.txt
```

## 3. Run Migrations
Initialize the database tables.

```bash
alembic upgrade head
```

## 4. Start the Server

```bash
uvicorn app.main:app --reload
``` 
### Access the app at: http://localhost:8000/auth/google

## 🐳 Option B: Running with Docker (Recommended)
This method handles the database and application environment automatically.

Ensure Docker Desktop is running.

Build and run:

```bash
docker compose up --build
```
### Access the app at: http://localhost:8000/auth/google

## 🧪 Running Tests
Tests use an in-memory SQLite database, so they work without a running Postgres instance.

Local (with venv active):

```bash
pytest -v
```

Via Docker:
```bash
docker compose exec web pytest -v
```

## 📚 API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| **GET** | `/auth/google` | Initiates Google OAuth2 login flow. |
| **GET** | `/users/me` | Returns current user details (Requires Cookie). |
| **POST** | `/payments/paystack/initiate` | Starts a transaction. Body: `{"amount": 5000}` (Kobo). |
| **GET** | `/payments/{ref}/status` | Checks transaction status. |
| **POST** | `/payments/paystack/webhook` | Receives Paystack updates (Verifies Signature). |