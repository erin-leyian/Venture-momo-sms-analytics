-- Sample data for testing
USE momo_sms_analytics;

-- Insert transaction types
INSERT INTO transaction_types (type_name) VALUES
('Payment'),
('Received'),
('Bank Deposit'),
('Withdrawal'),
('Transfer'),
('Airtime'),
('Cash Power');

-- Insert users
INSERT INTO users (name, phone, balance) VALUES
('Jane Smith', '250791666666', 2000.00),
('Samuel Carter', '250788999999', 1500.00),
('Robert Brown', '250790777777', 3000.00),
('Alex Doe', '250789888888', 1000.00),
('Linda Green', '250788110381', 2500.00),
('MTN MobileMoney', '250795963036', 0.00);

-- Insert promotions
INSERT INTO promotions (promo_name, discount_rate) VALUES
('BivaMoMotima', 10.00),
('Welcome Bonus', 5.00),
('Loyalty Program', 15.00),
('Holiday Special', 20.00),
('Referral Bonus', 25.00);

-- Insert transactions
INSERT INTO transactions (transaction_id, sender_id, receiver_id, type_id, amount, transaction_date, status) VALUES
('76662021700', 
    (SELECT user_id FROM users WHERE phone = '250791666666'),
    (SELECT user_id FROM users WHERE phone = '250788110381'),
    (SELECT type_id FROM transaction_types WHERE type_name = 'Received'),
    2000.00,
    '2024-05-10 16:30:51',
    'Completed'
),
('73214484437',
    (SELECT user_id FROM users WHERE phone = '250788110381'),
    (SELECT user_id FROM users WHERE phone = '250791666666'),
    (SELECT type_id FROM transaction_types WHERE type_name = 'Payment'),
    1000.00,
    '2024-05-10 16:31:39',
    'Completed'
),
('51732411227',
    (SELECT user_id FROM users WHERE phone = '250788110381'),
    (SELECT user_id FROM users WHERE phone = '250788999999'),
    (SELECT type_id FROM transaction_types WHERE type_name = 'Payment'),
    600.00,
    '2024-05-10 21:32:32',
    'Completed'
),
('43668074924',
    (SELECT user_id FROM users WHERE phone = '250788999999'),
    (SELECT user_id FROM users WHERE phone = '250788110381'),
    (SELECT type_id FROM transaction_types WHERE type_name = 'Received'),
    25000.00,
    '2024-05-14 20:57:36',
    'Completed'
),
('14098463509',
    (SELECT user_id FROM users WHERE phone = '250788110381'),
    (SELECT user_id FROM users WHERE phone = '250790777777'),
    (SELECT type_id FROM transaction_types WHERE type_name = 'Withdrawal'),
    20000.00,
    '2024-05-26 02:10:27',
    'Completed'
),
('14103506143',
    (SELECT user_id FROM users WHERE phone = '250788110381'),
    NULL,
    (SELECT type_id FROM transaction_types WHERE type_name = 'Cash Power'),
    4000.00,
    '2024-05-26 13:31:00',
    'Completed'
),
('DEP001',
    NULL,
    (SELECT user_id FROM users WHERE phone = '250788110381'),
    (SELECT type_id FROM transaction_types WHERE type_name = 'Bank Deposit'),
    5000.00,
    '2024-05-11 18:43:49',
    'Completed'
);

-- Insert user promotions (junction table)
INSERT INTO user_promos (user_id, promo_id, join_date, status, redeemed) VALUES
(
    (SELECT user_id FROM users WHERE phone = '250788110381'),
    (SELECT promo_id FROM promotions WHERE promo_name = 'BivaMoMotima'),
    '2024-05-10 10:00:00',
    'Active',
    FALSE
),
(
    (SELECT user_id FROM users WHERE phone = '250791666666'),
    (SELECT promo_id FROM promotions WHERE promo_name = 'Welcome Bonus'),
    '2024-05-10 08:00:00',
    'Active',
    TRUE
),
(
    (SELECT user_id FROM users WHERE phone = '250788999999'),
    (SELECT promo_id FROM promotions WHERE promo_name = 'Loyalty Program'),
    '2024-05-12 12:00:00',
    'Active',
    FALSE
),
(
    (SELECT user_id FROM users WHERE phone = '250790777777'),
    (SELECT promo_id FROM promotions WHERE promo_name = 'Holiday Special'),
    '2024-05-15 14:00:00',
    'Expired',
    TRUE
),
(
    (SELECT user_id FROM users WHERE phone = '250789888888'),
    (SELECT promo_id FROM promotions WHERE promo_name = 'Referral Bonus'),
    '2024-05-20 16:00:00',
    'Active',
    FALSE
);

-- Insert system logs
INSERT INTO system_logs (transaction_id, event_description, timestamp) VALUES
('76662021700', 'Transaction processed successfully', '2024-05-10 16:30:52'),
('73214484437', 'Payment completed', '2024-05-10 16:31:40'),
('51732411227', 'Transaction verified', '2024-05-10 21:32:33'),
('43668074924', 'Money received notification sent', '2024-05-14 20:57:37'),
('14098463509', 'Withdrawal processed via agent', '2024-05-26 02:10:28'),
('14103506143', 'Cash power token generated', '2024-05-26 13:31:01'),
('DEP001', 'Bank deposit confirmed', '2024-05-11 18:43:50'),
('76662021700', 'SMS notification sent to receiver', '2024-05-10 16:30:53'),
('73214484437', 'Balance updated', '2024-05-10 16:31:41'),
('51732411227', 'Transaction logged in system', '2024-05-10 21:32:34');
