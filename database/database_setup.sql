-- MoMo SMS Analytics Database
-- Created for Week 2 Assignment

CREATE DATABASE IF NOT EXISTS momo_sms_analytics;

USE momo_sms_analytics;

-- Users table (primary table)
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique user identifier',
    name VARCHAR(100) COMMENT 'User full name',
    phone VARCHAR(20) UNIQUE COMMENT 'User phone number',
    balance DECIMAL(15, 2) DEFAULT 0.00 COMMENT 'Current account balance'
);

-- Transaction Types table (lookup table)
CREATE TABLE transaction_types (
    type_id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique type identifier',
    type_name VARCHAR(50) NOT NULL COMMENT 'Name of transaction type'
);

-- Promotions table
CREATE TABLE promotions (
    promo_id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique promotion identifier',
    promo_name VARCHAR(100) NOT NULL COMMENT 'Name of promotion',
    discount_rate DECIMAL(15, 2) COMMENT 'Discount percentage'
);

-- Transactions table (primary table)
CREATE TABLE transactions (
    transaction_id VARCHAR(50) PRIMARY KEY COMMENT 'Unique transaction ID from SMS',
    sender_id INT COMMENT 'User who sent money',
    receiver_id INT COMMENT 'User who received money',
    type_id INT NOT NULL COMMENT 'Type of transaction',
    amount DECIMAL(15, 2) NOT NULL COMMENT 'Transaction amount in RWF',
    transaction_date DATETIME NOT NULL COMMENT 'Date and time of transaction',
    status VARCHAR(20) COMMENT 'Transaction status',
    
    FOREIGN KEY (sender_id) REFERENCES users(user_id),
    FOREIGN KEY (receiver_id) REFERENCES users(user_id),
    FOREIGN KEY (type_id) REFERENCES transaction_types(type_id),
    
    CHECK (amount >= 0),
    
    INDEX idx_transaction_date (transaction_date),
    INDEX idx_type_id (type_id),
    INDEX idx_sender_id (sender_id),
    INDEX idx_receiver_id (receiver_id)
);

-- User_Promos junction table (many-to-many)
CREATE TABLE user_promos (
    user_id INT COMMENT 'User who has the promotion',
    promo_id INT COMMENT 'Promotion ID',
    join_date DATETIME COMMENT 'Date user joined promotion',
    status VARCHAR(20) COMMENT 'Promotion status',
    redeemed BOOLEAN DEFAULT FALSE COMMENT 'Whether promotion was redeemed',
    
    PRIMARY KEY (user_id, promo_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (promo_id) REFERENCES promotions(promo_id)
);

-- System Logs table
CREATE TABLE system_logs (
    log_id BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique log identifier',
    transaction_id VARCHAR(50) COMMENT 'Related transaction ID',
    event_description VARCHAR(255) COMMENT 'Description of logged event',
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT 'When event occurred',
    
    FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id),
    
    INDEX idx_transaction_id (transaction_id),
    INDEX idx_timestamp (timestamp)
);
