#!/bin/bash

# MoMo SMS Analytics API Test Script
# This script tests all CRUD endpoints and authentication

BASE_URL="http://localhost:8000"
ADMIN_USER="admin"
ADMIN_PASS="admin123"
USER_USER="user"
USER_PASS="user123"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "=========================================="
echo "MoMo SMS Analytics API Test Suite"
echo "=========================================="
echo ""

# Test 1: Authentication - Success
echo -e "${YELLOW}Test 1: Authentication Success${NC}"
echo "Testing valid credentials..."
RESPONSE=$(curl -s -w "\n%{http_code}" -u $ADMIN_USER:$ADMIN_PASS $BASE_URL/transactions)
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" == "200" ]; then
    echo -e "${GREEN}✓ PASS${NC} - Authentication successful (200 OK)"
else
    echo -e "${RED}✗ FAIL${NC} - Expected 200, got $HTTP_CODE"
fi
echo ""

# Test 2: Authentication - Failure
echo -e "${YELLOW}Test 2: Authentication Failure${NC}"
echo "Testing invalid credentials..."
RESPONSE=$(curl -s -w "\n%{http_code}" -u wrong:wrong $BASE_URL/transactions)
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)

if [ "$HTTP_CODE" == "401" ]; then
    echo -e "${GREEN}✓ PASS${NC} - Authentication failed correctly (401 Unauthorized)"
else
    echo -e "${RED}✗ FAIL${NC} - Expected 401, got $HTTP_CODE"
fi
echo ""

# Test 3: GET /transactions - List All
echo -e "${YELLOW}Test 3: GET /transactions (List All)${NC}"
RESPONSE=$(curl -s -w "\n%{http_code}" -u $ADMIN_USER:$ADMIN_PASS $BASE_URL/transactions)
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" == "200" ]; then
    COUNT=$(echo "$BODY" | grep -o '"count":[0-9]*' | grep -o '[0-9]*')
    echo -e "${GREEN}✓ PASS${NC} - Retrieved all transactions (200 OK)"
    echo "  Transaction count: $COUNT"
else
    echo -e "${RED}✗ FAIL${NC} - Expected 200, got $HTTP_CODE"
fi
echo ""

# Test 4: GET /transactions/{id} - Get Single Transaction
echo -e "${YELLOW}Test 4: GET /transactions/{id} (Get Single)${NC}"
TRANSACTION_ID="76662021700"
RESPONSE=$(curl -s -w "\n%{http_code}" -u $ADMIN_USER:$ADMIN_PASS $BASE_URL/transactions/$TRANSACTION_ID)
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" == "200" ]; then
    echo -e "${GREEN}✓ PASS${NC} - Retrieved transaction $TRANSACTION_ID (200 OK)"
    echo "$BODY" | python3 -m json.tool | head -10
elif [ "$HTTP_CODE" == "404" ]; then
    echo -e "${YELLOW}⚠ SKIP${NC} - Transaction $TRANSACTION_ID not found (may not exist in data)"
else
    echo -e "${RED}✗ FAIL${NC} - Expected 200 or 404, got $HTTP_CODE"
fi
echo ""

# Test 5: GET /transactions/{id} - Not Found
echo -e "${YELLOW}Test 5: GET /transactions/{id} (Not Found)${NC}"
RESPONSE=$(curl -s -w "\n%{http_code}" -u $ADMIN_USER:$ADMIN_PASS $BASE_URL/transactions/NONEXISTENT123)
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" == "404" ]; then
    echo -e "${GREEN}✓ PASS${NC} - Correctly returned 404 for non-existent transaction"
else
    echo -e "${RED}✗ FAIL${NC} - Expected 404, got $HTTP_CODE"
fi
echo ""

# Test 6: POST /transactions - Create New
echo -e "${YELLOW}Test 6: POST /transactions (Create)${NC}"
NEW_TX_ID="TEST_$(date +%s)"
JSON_DATA="{
  \"parsed_transaction\": {
    \"transaction_id\": \"$NEW_TX_ID\",
    \"amount\": \"5000\",
    \"transaction_type\": \"payment\",
    \"sender\": \"Test User\",
    \"recipient\": \"Jane Smith\",
    \"new_balance\": \"10000\",
    \"fee\": \"0\",
    \"transaction_date\": \"$(date '+%Y-%m-%d %H:%M:%S')\"
  },
  \"raw_body\": \"Test transaction created via API\"
}"

RESPONSE=$(curl -s -w "\n%{http_code}" -X POST \
  -u $ADMIN_USER:$ADMIN_PASS \
  -H "Content-Type: application/json" \
  -d "$JSON_DATA" \
  $BASE_URL/transactions)
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" == "201" ]; then
    echo -e "${GREEN}✓ PASS${NC} - Created transaction $NEW_TX_ID (201 Created)"
    CREATED_ID=$NEW_TX_ID
else
    echo -e "${RED}✗ FAIL${NC} - Expected 201, got $HTTP_CODE"
    echo "$BODY"
    CREATED_ID=""
fi
echo ""

# Test 7: PUT /transactions/{id} - Update
if [ -n "$CREATED_ID" ]; then
    echo -e "${YELLOW}Test 7: PUT /transactions/{id} (Update)${NC}"
    UPDATE_DATA="{
      \"parsed_transaction\": {
        \"amount\": \"6000\",
        \"new_balance\": \"11000\"
      }
    }"
    
    RESPONSE=$(curl -s -w "\n%{http_code}" -X PUT \
      -u $ADMIN_USER:$ADMIN_PASS \
      -H "Content-Type: application/json" \
      -d "$UPDATE_DATA" \
      $BASE_URL/transactions/$CREATED_ID)
    HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
    BODY=$(echo "$RESPONSE" | sed '$d')
    
    if [ "$HTTP_CODE" == "200" ]; then
        echo -e "${GREEN}✓ PASS${NC} - Updated transaction $CREATED_ID (200 OK)"
    else
        echo -e "${RED}✗ FAIL${NC} - Expected 200, got $HTTP_CODE"
    fi
    echo ""
fi

# Test 8: DELETE /transactions/{id} - Delete
if [ -n "$CREATED_ID" ]; then
    echo -e "${YELLOW}Test 8: DELETE /transactions/{id} (Delete)${NC}"
    RESPONSE=$(curl -s -w "\n%{http_code}" -X DELETE \
      -u $ADMIN_USER:$ADMIN_PASS \
      $BASE_URL/transactions/$CREATED_ID)
    HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
    BODY=$(echo "$RESPONSE" | sed '$d')
    
    if [ "$HTTP_CODE" == "200" ]; then
        echo -e "${GREEN}✓ PASS${NC} - Deleted transaction $CREATED_ID (200 OK)"
    else
        echo -e "${RED}✗ FAIL${NC} - Expected 200, got $HTTP_CODE"
    fi
    echo ""
fi

# Test 9: POST /transactions - Duplicate (Conflict)
echo -e "${YELLOW}Test 9: POST /transactions (Duplicate - Conflict)${NC}"
# First create
curl -s -X POST -u $ADMIN_USER:$ADMIN_PASS \
  -H "Content-Type: application/json" \
  -d "$JSON_DATA" \
  $BASE_URL/transactions > /dev/null

# Try to create again
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST \
  -u $ADMIN_USER:$ADMIN_PASS \
  -H "Content-Type: application/json" \
  -d "$JSON_DATA" \
  $BASE_URL/transactions)
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)

if [ "$HTTP_CODE" == "409" ]; then
    echo -e "${GREEN}✓ PASS${NC} - Correctly returned 409 Conflict for duplicate"
else
    echo -e "${RED}✗ FAIL${NC} - Expected 409, got $HTTP_CODE"
fi
echo ""

echo "=========================================="
echo "Test Suite Complete"
echo "=========================================="
echo ""
echo "Note: Make sure the API server is running:"
echo "  python3 api/server.py"
echo ""
