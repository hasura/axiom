-- =====================================================
-- FinIQ - Financial Intelligence & Quality Platform
-- Database: fin_recon
-- Purpose: Transaction Reconciliation & Analytics Demo
-- Version: 2.0 (with Merchants & Enhanced Analytics)
-- =====================================================

-- Drop existing tables if they exist (for clean runs)
DROP TABLE IF EXISTS settlement_transactions CASCADE;
DROP TABLE IF EXISTS auth_transactions CASCADE;
DROP TABLE IF EXISTS merchants CASCADE;
DROP TABLE IF EXISTS issuers CASCADE;
DROP TABLE IF EXISTS acquirers CASCADE;

-- =====================================================
-- Reference Tables
-- =====================================================

-- Issuers: Financial institutions that issue cards
CREATE TABLE issuers (
    issuer_id VARCHAR(20) PRIMARY KEY,
    issuer_name VARCHAR(255) NOT NULL,
    issuer_country VARCHAR(3) DEFAULT 'USA',
    primary_currency VARCHAR(3) DEFAULT 'USD',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_issuers_name ON issuers(issuer_name);

-- Acquirers: Merchants' financial institutions
CREATE TABLE acquirers (
    acquirer_id VARCHAR(20) PRIMARY KEY,
    acquirer_name VARCHAR(255) NOT NULL,
    acquirer_country VARCHAR(3) DEFAULT 'USA',
    primary_currency VARCHAR(3) DEFAULT 'USD',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_acquirers_name ON acquirers(acquirer_name);

-- Merchants: Business entities accepting card payments
CREATE TABLE merchants (
    merchant_id VARCHAR(20) PRIMARY KEY,
    merchant_name VARCHAR(255) NOT NULL,
    merchant_category_code VARCHAR(4) NOT NULL,  -- ISO 18245 MCC
    merchant_category_name VARCHAR(50) NOT NULL,
    merchant_country VARCHAR(3) DEFAULT 'USA',
    acquirer_id VARCHAR(20),
    annual_volume NUMERIC(15, 2),
    risk_level VARCHAR(20) DEFAULT 'LOW',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign key constraint
    CONSTRAINT fk_merchant_acquirer FOREIGN KEY (acquirer_id) 
        REFERENCES acquirers(acquirer_id) ON DELETE SET NULL
);

CREATE INDEX idx_merchants_name ON merchants(merchant_name);
CREATE INDEX idx_merchants_category ON merchants(merchant_category_code);
CREATE INDEX idx_merchants_acquirer ON merchants(acquirer_id);
CREATE INDEX idx_merchants_risk ON merchants(risk_level);

-- =====================================================
-- Authorization Transactions
-- =====================================================

CREATE TABLE auth_transactions (
    transaction_id VARCHAR(50) PRIMARY KEY,
    issuer_id VARCHAR(20) NOT NULL,
    acquirer_id VARCHAR(20) NOT NULL,
    merchant_id VARCHAR(20) NOT NULL,
    transaction_amount NUMERIC(15, 2) NOT NULL CHECK (transaction_amount >= 0),
    transaction_date DATE NOT NULL,
    transaction_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    transaction_type VARCHAR(50) NOT NULL,
    issuer_currency VARCHAR(3) DEFAULT 'USD',
    acquirer_currency VARCHAR(3) DEFAULT 'USD',
    transaction_code VARCHAR(10),
    card_last_four VARCHAR(4),
    authorization_status VARCHAR(20) DEFAULT 'APPROVED',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Optional: Audit fields (uncomment if needed for governance demo)
    -- last_updated_by VARCHAR(50) DEFAULT 'SYSTEM',
    -- last_updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign key constraints
    CONSTRAINT fk_auth_issuer FOREIGN KEY (issuer_id) 
        REFERENCES issuers(issuer_id) ON DELETE RESTRICT,
    CONSTRAINT fk_auth_acquirer FOREIGN KEY (acquirer_id) 
        REFERENCES acquirers(acquirer_id) ON DELETE RESTRICT,
    CONSTRAINT fk_auth_merchant FOREIGN KEY (merchant_id) 
        REFERENCES merchants(merchant_id) ON DELETE RESTRICT,
    
    -- Business rule constraints
    CONSTRAINT chk_auth_date CHECK (transaction_date <= CURRENT_DATE),
    CONSTRAINT chk_transaction_code CHECK (
        transaction_code IS NULL OR 
        transaction_code IN ('000', '100', '101', '102')
    )
);

-- Indexes for query performance
CREATE INDEX idx_auth_issuer ON auth_transactions(issuer_id);
CREATE INDEX idx_auth_acquirer ON auth_transactions(acquirer_id);
CREATE INDEX idx_auth_merchant ON auth_transactions(merchant_id);
CREATE INDEX idx_auth_date ON auth_transactions(transaction_date);
CREATE INDEX idx_auth_timestamp ON auth_transactions(transaction_timestamp);
CREATE INDEX idx_auth_code ON auth_transactions(transaction_code);
CREATE INDEX idx_auth_type ON auth_transactions(transaction_type);
CREATE INDEX idx_auth_amount ON auth_transactions(transaction_amount);
CREATE INDEX idx_auth_status ON auth_transactions(authorization_status);

-- =====================================================
-- Settlement Transactions
-- =====================================================

CREATE TABLE settlement_transactions (
    transaction_id VARCHAR(50) PRIMARY KEY,
    auth_transaction_id VARCHAR(50) NOT NULL,
    issuer_id VARCHAR(20) NOT NULL,
    acquirer_id VARCHAR(20) NOT NULL,
    merchant_id VARCHAR(20) NOT NULL,
    transaction_amount NUMERIC(15, 2) NOT NULL CHECK (transaction_amount >= 0),
    transaction_date DATE NOT NULL,
    transaction_type VARCHAR(50) NOT NULL,
    issuer_currency VARCHAR(3) DEFAULT 'USD',
    acquirer_currency VARCHAR(3) DEFAULT 'USD',
    acquirer_settlement_amount NUMERIC(15, 2) NOT NULL,
    issuer_settlement_amount NUMERIC(15, 2) NOT NULL,
    acquirer_settlement_date DATE NOT NULL,
    issuer_settlement_date DATE NOT NULL,
    transaction_settlement_date DATE NOT NULL,
    settlement_status VARCHAR(20) DEFAULT 'SETTLED',
    settlement_delta_pct NUMERIC(8,2),
    interchange_fee NUMERIC(15, 2) DEFAULT 0.00,
    network_fee NUMERIC(15, 2) DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Optional: Audit fields (uncomment if needed for governance demo)
    -- reconciled BOOLEAN DEFAULT FALSE,
    -- reconciled_by VARCHAR(50),
    -- reconciled_at TIMESTAMP,
    -- last_updated_by VARCHAR(50) DEFAULT 'SYSTEM',
    
    -- Foreign key constraints
    CONSTRAINT fk_settlement_auth FOREIGN KEY (auth_transaction_id) 
        REFERENCES auth_transactions(transaction_id) ON DELETE RESTRICT,
    CONSTRAINT fk_settlement_issuer FOREIGN KEY (issuer_id) 
        REFERENCES issuers(issuer_id) ON DELETE RESTRICT,
    CONSTRAINT fk_settlement_acquirer FOREIGN KEY (acquirer_id) 
        REFERENCES acquirers(acquirer_id) ON DELETE RESTRICT,
    CONSTRAINT fk_settlement_merchant FOREIGN KEY (merchant_id) 
        REFERENCES merchants(merchant_id) ON DELETE RESTRICT,
    
    -- Business rule constraints
    CONSTRAINT chk_settlement_dates CHECK (
        transaction_settlement_date >= transaction_date AND
        acquirer_settlement_date >= transaction_date AND
        issuer_settlement_date >= transaction_date
    ),
    CONSTRAINT chk_settlement_amounts CHECK (
        acquirer_settlement_amount > 0 AND
        issuer_settlement_amount > 0
    )
);

-- Indexes for query performance
CREATE INDEX idx_settlement_auth ON settlement_transactions(auth_transaction_id);
CREATE INDEX idx_settlement_issuer ON settlement_transactions(issuer_id);
CREATE INDEX idx_settlement_acquirer ON settlement_transactions(acquirer_id);
CREATE INDEX idx_settlement_merchant ON settlement_transactions(merchant_id);
CREATE INDEX idx_settlement_date ON settlement_transactions(transaction_date);
CREATE INDEX idx_settlement_status ON settlement_transactions(settlement_status);
CREATE INDEX idx_settlement_trans_date ON settlement_transactions(transaction_settlement_date);
CREATE INDEX idx_settlement_delta ON settlement_transactions(settlement_delta_pct);

-- =====================================================
-- Core Tables Complete - No Views Created
-- =====================================================
-- All necessary data can be queried directly from the base tables:
-- - auth_transactions
-- - settlement_transactions
-- - merchants
-- - issuers
-- - acquirers


-- =====================================================
-- Comments for Documentation
-- =====================================================

COMMENT ON TABLE auth_transactions IS 'FinIQ: Authorization transactions representing initial card transaction requests';
COMMENT ON TABLE settlement_transactions IS 'FinIQ: Settlement transactions representing final cleared payments';
COMMENT ON TABLE merchants IS 'FinIQ: Merchants accepting card payments';
COMMENT ON COLUMN auth_transactions.transaction_code IS 'Transaction response code: 000=approved, 100=decline, 101=pickup, 102=refer';
COMMENT ON COLUMN settlement_transactions.interchange_fee IS 'Fee charged by issuer to acquirer';
COMMENT ON COLUMN settlement_transactions.network_fee IS 'Fee charged by card network (Amex/Visa/MC)';
COMMENT ON COLUMN settlement_transactions.settlement_delta_pct IS 'Percentage variance between auth and settlement amounts (calculated)';
COMMENT ON COLUMN merchants.merchant_category_code IS 'ISO 18245 Merchant Category Code (MCC)';
COMMENT ON COLUMN merchants.risk_level IS 'Merchant risk classification: LOW, MEDIUM, HIGH';

-- Grant permissions (adjust as needed for your environment)
-- GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO finiq_app_user;
-- GRANT SELECT ON ALL SEQUENCES IN SCHEMA public TO finiq_app_user;