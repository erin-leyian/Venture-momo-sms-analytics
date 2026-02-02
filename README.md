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
1. Create database: `mysql -u root -p < database/database_setup.sql`
2. Load sample data: `mysql -u root -p momo_sms_analytics < database/sample_data.sql`
3. Run test queries: `mysql -u root -p momo_sms_analytics < database/test_queries.sql`

### Documentation
For detailed database documentation including sample queries with screenshots and constraint testing, please refer to the Database Design Document PDF located in the `docs/db_design_document` folder. The document contains comprehensive examples of database functionality, unique rules implementation, and query results with visual demonstrations.

## REST API

### Overview
The MoMo SMS Analytics API provides RESTful endpoints to manage and query mobile money transaction data. The API uses Basic Authentication and supports full CRUD operations.

### Quick Start

1. **Start the API Server:**
   ```bash
   python3 api/server.py
   ```
   The server will start on `http://localhost:8000`

2. **Test the API:**
   ```bash
   # Run automated tests
   ./tests/api_tests.sh
   
   # Or test manually with curl
   curl -u admin:admin123 http://localhost:8000/transactions
   ```

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
```
