# MoMo SMS Analytics Dashboard

## Project Description
This project processes MoMo SMS data in XML format, cleans and categorizes the transactions, stores them in a relational database (SQLite), and provides a simple frontend dashboard to analyze and visualize the data.

## Team Members
- Erin Leyian
- Kenny Gael Ishimwe Gatete
- Belyse INTWAZA

## High-Level System Architecture
Architecture diagram:
https://drive.google.com/file/d/1LdLmCNTx0AVMPfHcpYz2l_qiHtIG0kzN/view?usp=gmail

Flow (high level):
- XML input (MoMo SMS) → ETL pipeline (parse, clean, categorize)
- Store transactions in SQLite database
- Export aggregated analytics to JSON
- Frontend dashboard reads JSON and visualizes insights

## Scrum Board
https://github.com/users/erin-leyian/projects/1/views/1

## Team Task Sheet
https://docs.google.com/spreadsheets/d/1QJqkAyxRMrB263eiSfwBkgEmQOp3IDE967a9dt-lmQw/edit?gid=0#gid=0

## Database Design

### Database Schema
The system uses MySQL database (`momo_sms_analytics`) with the following tables:

- **users**: Stores user information (name, phone, balance)
- **transaction_types**: Lookup table for transaction categories (Payment, Received, Deposit, etc.)
- **transactions**: Main transaction records with sender, receiver, amount, date, and status
- **promotions**: Stores promotional offers (e.g., BivaMoMotima campaign)
- **user_promos**: Junction table for many-to-many relationship between users and promotions
- **system_logs**: Tracks ETL processing logs linked to transactions

### Key Relationships
- Users can send/receive multiple transactions (1:M)
- Each transaction has one type (1:M with transaction_types)
- Users can have multiple promotions (M:M via user_promos)
- Transactions can have multiple log entries (1:M with system_logs)

### Database Files
- `database/database_setup.sql`: Complete DDL script to create all tables
- `database/sample_data.sql`: Sample data for testing (5+ records per table)
- `database/test_queries.sql`: CRUD operation examples and test queries

### Setup Instructions

**Option A — Quick local setup (recommended, SQLite)**

1. No external DB required — the FastAPI app uses SQLite by default.
2. From the repository root, create and activate a virtual environment (optional but recommended):
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r api/requirements.txt
   ```
3. Start the API (this will auto-create the SQLite DB file `momo_auth.db` in the `api/` folder):
   ```bash
   cd api
   python3 main.py
   # or using uvicorn:
   # uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```
4. Open API docs at `http://localhost:8000/docs` to explore endpoints.

**Option B — MySQL (use the provided SQL scripts)**

1. The project includes MySQL DDL and sample data under `Venture-momo-sms-analytics/database/`.
2. Create the database and load sample data (run these from the repo root or provide full paths):
   ```bash
   mysql -u root -p < Venture-momo-sms-analytics/database/database_setup.sql
   mysql -u root -p momo_sms_analytics < Venture-momo-sms-analytics/database/sample_data.sql
   ```
3. Update `api/config/database.py` to use your MySQL connection, for example:
   ```py
   DATABASE_URL = "mysql+pymysql://user:password@localhost/momo_sms_analytics"
   ```
   and install the MySQL driver: `pip install pymysql`.
4. Start the API as above.


### Documentation
For detailed database documentation including sample queries with screenshots and constraint testing, please refer to the Database Design Document PDF located in the `docs/db_design_document` folder. The document contains comprehensive examples of database functionality, unique rules implementation, and query results with visual demonstrations.

## REST API

### Overview
The MoMo SMS Analytics API provides RESTful endpoints to manage and query mobile money transaction data. The API uses Basic Authentication and supports full CRUD operations.

### Quick Start

1. **Start the API Server (two options):**

   - **Option A — FastAPI (recommended, uses SQLite by default)**
     ```bash
     # Optional: create and activate a virtualenv
     python3 -m venv .venv
     source .venv/bin/activate
     pip install -r api/requirements.txt

     # From the api/ folder, start the server (auto-creates SQLite DB 'momo_auth.db')
     cd api
     python3 main.py
     # or using uvicorn:
     # uvicorn main:app --reload --host 0.0.0.0 --port 8000
     ```
     API docs: `http://localhost:8000/docs`

   - **Option B — Simple JSON file server (quick demo)**
     ```bash
     python3 api/server.py
     ```
     This server serves transactions from `api/dsa/momo_transactions.json` and listens on `http://localhost:8000`.

2. **Testing the API**

   - There is no shipped automated API test script in this repository. You can test manually with curl:
     ```bash
     curl -u admin:admin123 http://localhost:8000/transactions
     ```
   - For FastAPI, add pytest-based tests and run them with `pytest` (recommended for automated testing).

### Authentication

The API uses Basic Authentication. Credentials:
- **Username:** `admin` / **Password:** `admin123`
- **Username:** `user` / **Password:** `user123`

**Example:**
```bash
curl -u admin:admin123 http://localhost:8000/transactions
```

### API Endpoints

- `GET /transactions` - Get all transactions
- `GET /transactions/{id}` - Get a specific transaction
- `POST /transactions` - Create a new transaction
- `PUT /transactions/{id}` - Update a transaction
- `DELETE /transactions/{id}` - Delete a transaction

### Documentation

For complete API documentation including request/response examples, error codes, and security considerations, see [`docs/api_docs.md`](docs/api_docs.md).

### Testing

Automated test scripts are available in `tests/api_tests.sh`. The script tests:
- Authentication (success and failure)
- All CRUD operations
- Error handling (404, 409, etc.)

To run tests:
```bash
# Make sure server is running first
python3 api/server.py

# In another terminal, run tests
./tests/api_tests.sh
```

## Planned Project Structure

```
├── README.md
├── .env.example
├── requirements.txt
├── index.html
├── database/
│   ├── database_setup.sql
│   ├── sample_data.sql
│   └── test_queries.sql
├── web/
│   ├── styles.css
│   ├── chart_handler.js
│   └── assets/
├── data/
│   ├── raw/
│   ├── processed/
│   ├── db.sqlite3
│   └── logs/
├── etl/
├── api/
├── scripts/
└── tests/

