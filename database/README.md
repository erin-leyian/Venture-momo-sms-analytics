# Database Documentation

## Overview
This is the MySQL database for storing MoMo SMS transaction data. It transforms hierarchical XML data into a normalized schema suitable for data processing. The database has 6 main tables.

## Database Info
- Database name: momo_sms_analytics
- Uses MySQL

## Tables

### 1. users
Primary table storing user information. Users can be both senders and recipients.

Columns:
- user_id (primary key)
- name
- phone (unique)
- balance

### 2. transaction_types
Lookup table for standardizing transaction activities like "Payment", "Received", "Bank deposits".

Columns:
- type_id (primary key)
- type_name

### 3. transactions
Primary table for storing transaction records. Links to users through sender_id and receiver_id.

Columns:
- transaction_id (primary key, VARCHAR)
- sender_id (foreign key to users)
- receiver_id (foreign key to users)
- type_id (foreign key to transaction_types)
- amount
- transaction_date
- status

### 4. promotions
Stores promotional offers like "BivaMoMotima" campaign.

Columns:
- promo_id (primary key)
- promo_name
- discount_rate

### 5. user_promos
Junction table for many-to-many relationship between users and promotions. Tracks promotion instances with status and join_date.

Columns:
- user_id (primary key, foreign key to users)
- promo_id (primary key, foreign key to promotions)
- join_date
- status
- redeemed

### 6. system_logs
Stores system logs linked to specific transactions for traceability.

Columns:
- log_id (primary key, BIGINT)
- transaction_id (foreign key to transactions)
- event_description
- timestamp

## Relationships

- Users to Transactions: 1-to-Many (users can send/receive multiple transactions)
- Transaction Types to Transactions: 1-to-Many (one type can have many transactions)
- Users to Promotions: Many-to-Many (resolved by user_promos junction table)
- Transactions to System Logs: 1-to-Many (one transaction can have multiple log entries)

## Constraints

### Unique Constraints
- phone must be unique in users
- transaction_id must be unique
- (user_id, promo_id) must be unique in user_promos

### Check Constraints
- amount must be >= 0

### Foreign Keys
- transactions.sender_id references users.user_id
- transactions.receiver_id references users.user_id
- transactions.type_id references transaction_types.type_id
- user_promos.user_id references users.user_id
- user_promos.promo_id references promotions.promo_id
- system_logs.transaction_id references transactions.transaction_id

## How to Use

### Setup
1. Run database_setup.sql to create tables
2. Run sample_data.sql to add test data
3. Run test_queries.sql to see example queries

### Example Queries

Get all transactions:
```sql
SELECT * FROM transactions;
```

Get transactions with user names and types:
```sql
SELECT 
    t.transaction_id,
    t.amount,
    sender.name AS sender_name,
    receiver.name AS receiver_name,
    tt.type_name
FROM transactions t
LEFT JOIN users sender ON t.sender_id = sender.user_id
LEFT JOIN users receiver ON t.receiver_id = receiver.user_id
INNER JOIN transaction_types tt ON t.type_id = tt.type_id;
```

Get users with their promotions:
```sql
SELECT 
    u.name,
    p.promo_name,
    up.status,
    up.redeemed
FROM users u
INNER JOIN user_promos up ON u.user_id = up.user_id
INNER JOIN promotions p ON up.promo_id = p.promo_id;
```
