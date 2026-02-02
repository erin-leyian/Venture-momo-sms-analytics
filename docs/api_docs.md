# MoMo SMS Analytics API Documentation

## Overview

The MoMo SMS Analytics API provides RESTful endpoints to manage and query mobile money transaction data. The API uses Basic Authentication for security and supports full CRUD operations on transaction records.

**Base URL:** `http://localhost:8000`

**Authentication:** Basic Auth (username:password encoded in Base64)

---

## Authentication

All endpoints require Basic Authentication. Include the `Authorization` header with each request.

### Credentials

- **Username:** `admin` / **Password:** `admin123`
- **Username:** `user` / **Password:** `user123`

### How to Authenticate

Include the Authorization header in your requests:

```
Authorization: Basic YWRtaW46YWRtaW4xMjM=
```

Where `YWRtaW46YWRtaW4xMjM=` is the Base64 encoding of `admin:admin123`

### Authentication Failure

If authentication fails, you will receive:

**Status Code:** `401 Unauthorized`

**Response:**
```json
{
  "error": "Unauthorized"
}
```

---

## Endpoints

### 1. Get All Transactions

Retrieve a list of all transactions in the system.

**Endpoint:** `GET /transactions`

**Authentication:** Required

**Response:**

**Status Code:** `200 OK`

```json
{
  "transactions": [
    {
      "id": "76662021700",
      "parsed_transaction": {
        "transaction_id": "76662021700",
        "amount": "2000",
        "transaction_type": "receive",
        "sender": "Jane Smith",
        "recipient": null,
        "new_balance": "2000",
        "fee": "0",
        "transaction_date": "2024-05-10 16:30:51"
      },
      "raw_body": "You have received 2000 RWF from Jane Smith..."
    }
  ],
  "count": 1693
}
```

**Example Request (curl):**
```bash
curl -u admin:admin123 http://localhost:8000/transactions
```

---

### 2. Get Single Transaction

Retrieve a specific transaction by its ID.

**Endpoint:** `GET /transactions/{id}`

**Authentication:** Required

**Path Parameters:**
- `id` (string, required) - The transaction ID

**Response:**

**Status Code:** `200 OK`

```json
{
  "id": "76662021700",
  "parsed_transaction": {
    "transaction_id": "76662021700",
    "amount": "2000",
    "transaction_type": "receive",
    "sender": "Jane Smith",
    "recipient": null,
    "new_balance": "2000",
    "fee": "0",
    "transaction_date": "2024-05-10 16:30:51"
  },
  "raw_body": "You have received 2000 RWF from Jane Smith..."
}
```

**Error Response:**

**Status Code:** `404 Not Found`

```json
{
  "error": "Transaction not found"
}
```

**Example Request (curl):**
```bash
curl -u admin:admin123 http://localhost:8000/transactions/76662021700
```

---

### 3. Create Transaction

Create a new transaction record.

**Endpoint:** `POST /transactions`

**Authentication:** Required

**Request Body:**
```json
{
  "parsed_transaction": {
    "transaction_id": "NEW123456",
    "amount": "5000",
    "transaction_type": "payment",
    "sender": "John Doe",
    "recipient": "Jane Smith",
    "new_balance": "10000",
    "fee": "0",
    "transaction_date": "2024-05-20 10:00:00"
  },
  "raw_body": "Your payment of 5,000 RWF to Jane Smith..."
}
```

**Response:**

**Status Code:** `201 Created`

```json
{
  "message": "Created",
  "data": {
    "parsed_transaction": {
      "transaction_id": "NEW123456",
      "amount": "5000",
      ...
    }
  }
}
```

**Error Responses:**

**Status Code:** `400 Bad Request` - Missing JSON body or transaction_id
```json
{
  "error": "Missing JSON body"
}
```

**Status Code:** `409 Conflict` - Transaction already exists
```json
{
  "error": "Transaction already exists"
}
```

**Example Request (curl):**
```bash
curl -X POST -u admin:admin123 \
  -H "Content-Type: application/json" \
  -d '{
    "parsed_transaction": {
      "transaction_id": "NEW123456",
      "amount": "5000",
      "transaction_type": "payment",
      "sender": "John Doe",
      "recipient": "Jane Smith",
      "new_balance": "10000",
      "fee": "0",
      "transaction_date": "2024-05-20 10:00:00"
    },
    "raw_body": "Your payment of 5,000 RWF to Jane Smith..."
  }' \
  http://localhost:8000/transactions
```

---

### 4. Update Transaction

Update an existing transaction record.

**Endpoint:** `PUT /transactions/{id}`

**Authentication:** Required

**Path Parameters:**
- `id` (string, required) - The transaction ID to update

**Request Body:**
```json
{
  "parsed_transaction": {
    "amount": "6000",
    "new_balance": "11000"
  }
}
```

**Response:**

**Status Code:** `200 OK`

```json
{
  "message": "Updated",
  "data": {
    "id": "76662021700",
    "parsed_transaction": {
      "transaction_id": "76662021700",
      "amount": "6000",
      ...
    }
  }
}
```

**Error Responses:**

**Status Code:** `404 Not Found` - Transaction doesn't exist
```json
{
  "error": "Transaction not found"
}
```

**Status Code:** `400 Bad Request` - Missing JSON body
```json
{
  "error": "Missing JSON body"
}
```

**Example Request (curl):**
```bash
curl -X PUT -u admin:admin123 \
  -H "Content-Type: application/json" \
  -d '{
    "parsed_transaction": {
      "amount": "6000",
      "new_balance": "11000"
    }
  }' \
  http://localhost:8000/transactions/76662021700
```

---

### 5. Delete Transaction

Delete a transaction record.

**Endpoint:** `DELETE /transactions/{id}`

**Authentication:** Required

**Path Parameters:**
- `id` (string, required) - The transaction ID to delete

**Response:**

**Status Code:** `200 OK`

```json
{
  "message": "Deleted 76662021700"
}
```

**Error Response:**

**Status Code:** `404 Not Found`

```json
{
  "error": "Transaction not found"
}
```

**Example Request (curl):**
```bash
curl -X DELETE -u admin:admin123 http://localhost:8000/transactions/76662021700
```

---

## Error Codes

| Status Code | Description |
|------------|-------------|
| 200 | OK - Request successful |
| 201 | Created - Resource created successfully |
| 400 | Bad Request - Invalid request format or missing data |
| 401 | Unauthorized - Authentication required or invalid credentials |
| 404 | Not Found - Resource not found |
| 409 | Conflict - Resource already exists |

---

## Request/Response Format

- **Content-Type:** `application/json`
- **Accept:** `application/json`
- All request bodies must be valid JSON
- All responses are JSON formatted

---

## Rate Limiting

Currently, there are no rate limits implemented. However, for production use, rate limiting should be added.

---

## Security Considerations

### Basic Authentication Limitations

1. **Credentials in Plain Text:** Basic Auth sends credentials in Base64 encoding, which is easily decoded. Always use HTTPS in production.

2. **No Token Expiration:** Credentials don't expire. Implement token-based authentication for better security.

3. **No Role-Based Access Control:** All authenticated users have the same permissions. Consider implementing role-based access control (RBAC).

4. **No Password Hashing:** Passwords are stored in plain text in the server code. Use proper password hashing (bcrypt, argon2) in production.

### Recommendations for Production

- Use HTTPS/TLS encryption
- Implement JWT or OAuth2 token-based authentication
- Add rate limiting
- Implement proper password hashing
- Add request logging and monitoring
- Use environment variables for credentials
- Implement role-based access control

---

## Testing

See `tests/api_tests.sh` for automated test scripts and examples.

---

## Support

For issues or questions, please refer to the main README.md or contact the development team.
