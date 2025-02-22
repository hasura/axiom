CREATE DATABASE aml;

\c aml;

CREATE TABLE IF NOT EXISTS saml_d (
    time TIME,
    date DATE,
    sender_account BIGINT,
    receiver_account BIGINT,
    amount DECIMAL(15,2),
    payment_currency VARCHAR(20),
    received_currency VARCHAR(20),
    sender_bank_location VARCHAR(50),
    receiver_bank_location VARCHAR(50),
    payment_type VARCHAR(50),
    is_laundering BOOLEAN,
    laundering_type VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS customers (
    customer_id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    account BIGINT UNIQUE NOT NULL,
    dob DATE NOT NULL,
    nationality VARCHAR(100),
    risk_level VARCHAR(10) CHECK (risk_level IN ('low', 'medium', 'high')),
    pep_status BOOLEAN DEFAULT FALSE,
    blacklisted BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS sars (
    sar_id BIGSERIAL PRIMARY KEY,
    customer_id BIGINT REFERENCES customers(customer_id) ON DELETE CASCADE,
    transaction_id BIGINT NOT NULL,
    reason TEXT NOT NULL,
    status VARCHAR(10) CHECK (status IN ('pending', 'filed', 'dismissed')) DEFAULT 'pending',
    filed_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_customers_nationality ON customers(nationality);
CREATE INDEX idx_sars_customer_id ON sars(customer_id);
CREATE INDEX idx_sars_transaction_id ON sars(transaction_id);
CREATE INDEX idx_saml_d_sender_account ON saml_d(sender_account);
CREATE INDEX idx_saml_d_receiver_account ON saml_d(receiver_account);
CREATE INDEX idx_saml_d_date ON saml_d(date);
CREATE INDEX idx_saml_d_payment_type ON saml_d(payment_type);
CREATE INDEX idx_saml_d_is_laundering ON saml_d(is_laundering);

COPY customers FROM '/docker-entrypoint-initdb.d/customers.csv' DELIMITER ',' CSV HEADER;
COPY sars FROM '/docker-entrypoint-initdb.d/sars.csv' DELIMITER ',' CSV HEADER;
COPY saml_d FROM '/docker-entrypoint-initdb.d/SAML-D.csv' DELIMITER ',' CSV HEADER;
