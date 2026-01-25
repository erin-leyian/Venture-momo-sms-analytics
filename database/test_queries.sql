-- Test queries for database
USE momo_sms_analytics;

-- INSERT examples
INSERT INTO transaction_types (type_name) VALUES ('Refund');

INSERT INTO users (name, phone, balance) VALUES ('Test User', '250799999999', 5000.00);

INSERT INTO transactions (transaction_id, sender_id, receiver_id, type_id, amount, transaction_date, status)
VALUES (
    'TEST123456',
    (SELECT user_id FROM users WHERE phone = '250799999999'),
    (SELECT user_id FROM users WHERE phone = '250791666666'),
    (SELECT type_id FROM transaction_types WHERE type_name = 'Payment'),
    5000.00,
    NOW(),
    'Completed'
);

-- SELECT examples
-- Get all transactions with user names and type
SELECT 
    t.transaction_id,
    t.amount,
    t.transaction_date,
    t.status,
    sender.name AS sender_name,
    receiver.name AS receiver_name,
    tt.type_name
FROM transactions t
LEFT JOIN users sender ON t.sender_id = sender.user_id
LEFT JOIN users receiver ON t.receiver_id = receiver.user_id
INNER JOIN transaction_types tt ON t.type_id = tt.type_id
ORDER BY t.transaction_date DESC;

-- Get transaction summary by type
SELECT 
    tt.type_name,
    COUNT(*) AS transaction_count,
    SUM(t.amount) AS total_amount
FROM transactions t
INNER JOIN transaction_types tt ON t.type_id = tt.type_id
GROUP BY tt.type_id, tt.type_name
ORDER BY total_amount DESC;

-- Get user transaction history
SELECT 
    u.name,
    u.phone,
    u.balance,
    COUNT(DISTINCT CASE WHEN t.sender_id = u.user_id THEN t.transaction_id END) AS sent_count,
    COUNT(DISTINCT CASE WHEN t.receiver_id = u.user_id THEN t.transaction_id END) AS received_count
FROM users u
LEFT JOIN transactions t ON (t.sender_id = u.user_id OR t.receiver_id = u.user_id)
GROUP BY u.user_id, u.name, u.phone, u.balance
ORDER BY u.name;

-- Get users with promotions
SELECT 
    u.name,
    u.phone,
    p.promo_name,
    up.join_date,
    up.status,
    up.redeemed
FROM users u
INNER JOIN user_promos up ON u.user_id = up.user_id
INNER JOIN promotions p ON up.promo_id = p.promo_id
ORDER BY u.name;

-- Get system logs for a transaction
SELECT 
    sl.log_id,
    sl.transaction_id,
    sl.event_description,
    sl.timestamp
FROM system_logs sl
WHERE sl.transaction_id = '76662021700'
ORDER BY sl.timestamp;

-- UPDATE examples
UPDATE users 
SET balance = balance + 1000.00
WHERE user_id = 1;

UPDATE transactions 
SET status = 'Pending'
WHERE transaction_id = 'TEST123456';

UPDATE user_promos 
SET redeemed = TRUE, status = 'Used'
WHERE user_id = 1 AND promo_id = 1;

-- DELETE examples
DELETE FROM transactions WHERE transaction_id = 'TEST123456';

DELETE FROM system_logs WHERE timestamp < DATE_SUB(NOW(), INTERVAL 30 DAY);

-- Some analytics queries
-- Monthly transaction summary
SELECT 
    YEAR(transaction_date) AS year,
    MONTH(transaction_date) AS month,
    COUNT(*) AS transaction_count,
    SUM(amount) AS total_amount
FROM transactions
GROUP BY YEAR(transaction_date), MONTH(transaction_date)
ORDER BY year DESC, month DESC;

-- Top users by transaction count
SELECT 
    u.name,
    u.phone,
    COUNT(t.transaction_id) AS total_transactions,
    SUM(CASE WHEN t.sender_id = u.user_id THEN t.amount ELSE 0 END) AS total_sent,
    SUM(CASE WHEN t.receiver_id = u.user_id THEN t.amount ELSE 0 END) AS total_received
FROM users u
LEFT JOIN transactions t ON (t.sender_id = u.user_id OR t.receiver_id = u.user_id)
GROUP BY u.user_id, u.name, u.phone
ORDER BY total_transactions DESC
LIMIT 10;

-- Promotion usage statistics
SELECT 
    p.promo_name,
    COUNT(up.user_id) AS users_count,
    SUM(CASE WHEN up.redeemed = TRUE THEN 1 ELSE 0 END) AS redeemed_count
FROM promotions p
LEFT JOIN user_promos up ON p.promo_id = up.promo_id
GROUP BY p.promo_id, p.promo_name
ORDER BY users_count DESC;
