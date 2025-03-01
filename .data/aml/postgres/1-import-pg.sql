-- Create tables for PostgreSQL
CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    account INT NOT NULL,
    dob DATE,
    nationality VARCHAR(50),
    address TEXT,
    risk_level VARCHAR(10),
    pep_status BOOLEAN,
    blacklisted BOOLEAN
);

CREATE TABLE financial_transfers (
    transaction_id INT PRIMARY KEY,
    time VARCHAR(5),
    date DATE,
    sender_account INT,
    receiver_account INT,
    amount DECIMAL(10, 2),
    payment_currency VARCHAR(5),
    received_currency VARCHAR(5),
    sender_bank_location VARCHAR(50),
    receiver_bank_location VARCHAR(50),
    payment_type VARCHAR(10),
    is_laundering BOOLEAN,
    laundering_type VARCHAR(20)
);

CREATE TABLE sars (
    sar_id INT PRIMARY KEY,
    customer_id INT,
    transaction_id INT,
    reason TEXT,
    status VARCHAR(10),
    filed_date TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (transaction_id) REFERENCES financial_transfers(transaction_id)
);

-- Copy data from CSV files
COPY customers FROM '/docker-entrypoint-initdb.d/customers.csv' DELIMITER ',' CSV HEADER;
COPY financial_transfers FROM '/docker-entrypoint-initdb.d/financial_transfers.csv' DELIMITER ',' CSV HEADER;
COPY sars FROM '/docker-entrypoint-initdb.d/sars.csv' DELIMITER ',' CSV HEADER;

-- Indexes for customers table
CREATE INDEX idx_customers_name ON customers(name);
CREATE INDEX idx_customers_account ON customers(account);
CREATE INDEX idx_customers_nationality ON customers(nationality);
CREATE INDEX idx_customers_risk_level ON customers(risk_level);
CREATE INDEX idx_customers_pep_status ON customers(pep_status);
CREATE INDEX idx_customers_blacklisted ON customers(blacklisted);

-- Indexes for financial_transfers table
CREATE INDEX idx_financial_transfers_date ON financial_transfers(date);
CREATE INDEX idx_financial_transfers_sender_account ON financial_transfers(sender_account);
CREATE INDEX idx_financial_transfers_receiver_account ON financial_transfers(receiver_account);
CREATE INDEX idx_financial_transfers_payment_type ON financial_transfers(payment_type);
CREATE INDEX idx_financial_transfers_amount ON financial_transfers(amount);
CREATE INDEX idx_financial_transfers_sender_location ON financial_transfers(sender_bank_location);
CREATE INDEX idx_financial_transfers_receiver_location ON financial_transfers(receiver_bank_location);
CREATE INDEX idx_financial_transfers_is_laundering ON financial_transfers(is_laundering);
CREATE INDEX idx_financial_transfers_laundering_type ON financial_transfers(laundering_type);

-- Indexes for SARs table
CREATE INDEX idx_sars_status ON sars(status);
CREATE INDEX idx_sars_filed_date ON sars(filed_date);