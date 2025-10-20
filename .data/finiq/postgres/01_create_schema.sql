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
    interchange_fee NUMERIC(15, 2) DEFAULT 0.00,
    network_fee NUMERIC(15, 2) DEFAULT 0.00,
    
    -- Computed column for settlement variance percentage
    settlement_delta_pct NUMERIC(8,2) GENERATED ALWAYS AS (
        CASE WHEN transaction_amount > 0 THEN
            ROUND(ABS(acquirer_settlement_amount - transaction_amount) / transaction_amount * 100, 2)
        ELSE NULL END
    ) STORED,
    
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
-- Analytical Views
-- =====================================================

-- View: Authorization with Settlement Status
CREATE OR REPLACE VIEW v_auth_settlement_status AS
SELECT 
    a.transaction_id,
    a.transaction_date,
    a.transaction_timestamp,
    a.transaction_amount,
    a.transaction_type,
    a.transaction_code,
    a.issuer_id,
    a.acquirer_id,
    a.merchant_id,
    m.merchant_name,
    m.merchant_category_code,
    m.merchant_category_name,
    s.transaction_id AS settlement_id,
    s.transaction_settlement_date,
    s.acquirer_settlement_amount,
    s.issuer_settlement_amount,
    s.settlement_delta_pct,
    CASE 
        WHEN s.transaction_id IS NULL THEN 'UNSETTLED'
        ELSE s.settlement_status
    END AS settlement_status,
    CASE 
        WHEN s.transaction_id IS NOT NULL 
        THEN s.transaction_settlement_date - a.transaction_date
        ELSE NULL
    END AS days_to_settle
FROM auth_transactions a
LEFT JOIN settlement_transactions s ON a.transaction_id = s.auth_transaction_id
LEFT JOIN merchants m ON a.merchant_id = m.merchant_id;

-- View: Missing Transaction Codes Analysis
CREATE OR REPLACE VIEW v_missing_transaction_codes AS
SELECT 
    COUNT(*) as total_transactions,
    COUNT(transaction_code) as with_code,
    COUNT(*) - COUNT(transaction_code) as missing_code,
    ROUND(100.0 * (COUNT(*) - COUNT(transaction_code)) / COUNT(*), 2) as missing_percentage
FROM auth_transactions;

-- View: Settlement Mismatch Analysis
CREATE OR REPLACE VIEW v_settlement_mismatches AS
SELECT 
    s.transaction_id,
    s.auth_transaction_id,
    s.merchant_id,
    m.merchant_name,
    m.merchant_category_name,
    a.transaction_amount as auth_amount,
    s.acquirer_settlement_amount,
    s.issuer_settlement_amount,
    s.settlement_delta_pct,
    ABS(a.transaction_amount - s.acquirer_settlement_amount) as amount_variance,
    CASE 
        WHEN s.settlement_delta_pct > 2 THEN 'HIGH_VARIANCE'
        WHEN s.settlement_delta_pct > 0.5 THEN 'MEDIUM_VARIANCE'
        ELSE 'LOW_VARIANCE'
    END AS variance_category
FROM settlement_transactions s
JOIN auth_transactions a ON s.auth_transaction_id = a.transaction_id
JOIN merchants m ON s.merchant_id = m.merchant_id
WHERE ABS(a.transaction_amount - s.acquirer_settlement_amount) > 0.01;

-- View: Merchant Performance Summary
CREATE OR REPLACE VIEW v_merchant_performance AS
SELECT 
    m.merchant_id,
    m.merchant_name,
    m.merchant_category_name,
    m.risk_level,
    COUNT(DISTINCT a.transaction_id) as total_auth_count,
    SUM(a.transaction_amount) as total_auth_volume,
    ROUND(AVG(a.transaction_amount)::numeric, 2) as avg_transaction_amount,
    COUNT(DISTINCT s.transaction_id) as settled_count,
    SUM(s.acquirer_settlement_amount) as total_settlement_volume,
    ROUND(100.0 * COUNT(DISTINCT s.transaction_id) / NULLIF(COUNT(DISTINCT a.transaction_id), 0), 2) as settlement_rate_pct,
    COUNT(DISTINCT s.transaction_id) FILTER (WHERE s.settlement_delta_pct > 2) as high_variance_count,
    ROUND(AVG(s.settlement_delta_pct)::numeric, 2) as avg_variance_pct
FROM merchants m
LEFT JOIN auth_transactions a ON m.merchant_id = a.merchant_id
LEFT JOIN settlement_transactions s ON a.transaction_id = s.auth_transaction_id
GROUP BY m.merchant_id, m.merchant_name, m.merchant_category_name, m.risk_level;

-- View: Top Merchants by Settlement Volume
CREATE OR REPLACE VIEW v_top_merchants_by_volume AS
SELECT 
    m.merchant_id,
    m.merchant_name,
    m.merchant_category_name,
    COUNT(DISTINCT s.transaction_id) as settlement_count,
    SUM(s.acquirer_settlement_amount) as total_settlement_volume,
    ROUND(AVG(s.settlement_delta_pct)::numeric, 2) as avg_variance_pct,
    RANK() OVER (ORDER BY SUM(s.acquirer_settlement_amount) DESC) as volume_rank
FROM merchants m
JOIN settlement_transactions s ON m.merchant_id = s.merchant_id
GROUP BY m.merchant_id, m.merchant_name, m.merchant_category_name
ORDER BY total_settlement_volume DESC;

-- View: Merchant Category Analysis
CREATE OR REPLACE VIEW v_category_analysis AS
SELECT
    m.merchant_category_code,
    m.merchant_category_name,
    COUNT(DISTINCT m.merchant_id) as merchant_count,
    COUNT(DISTINCT a.transaction_id) as transaction_count,
    SUM(a.transaction_amount) as total_volume,
    ROUND(AVG(a.transaction_amount)::numeric, 2) as avg_transaction_size,
    COUNT(DISTINCT s.transaction_id) FILTER (WHERE s.settlement_delta_pct > 2) as high_variance_count,
    ROUND(AVG(s.settlement_delta_pct)::numeric, 2) as avg_variance_pct
FROM merchants m
LEFT JOIN auth_transactions a ON m.merchant_id = a.merchant_id
LEFT JOIN settlement_transactions s ON a.transaction_id = s.auth_transaction_id
GROUP BY m.merchant_category_code, m.merchant_category_name
ORDER BY total_volume DESC;

-- View: Transaction Code Distribution Analysis
CREATE OR REPLACE VIEW v_transaction_code_analysis AS
SELECT
    COALESCE(transaction_code, 'NULL') as transaction_code,
    COUNT(*) as transaction_count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) as percentage,
    CASE
        WHEN transaction_code = '000' THEN 'Approved'
        WHEN transaction_code = '100' THEN 'Declined - General'
        WHEN transaction_code = '101' THEN 'Declined - Pick Up Card'
        WHEN transaction_code = '102' THEN 'Declined - Refer to Issuer'
        WHEN transaction_code IS NULL THEN 'System Error - Missing Code'
        ELSE 'Other'
    END as code_description
FROM auth_transactions
GROUP BY transaction_code
ORDER BY transaction_count DESC;

-- View: Decline Rate Analysis by Risk Level
CREATE OR REPLACE VIEW v_decline_rate_by_risk AS
SELECT
    m.risk_level,
    COUNT(DISTINCT a.transaction_id) as total_transactions,
    COUNT(DISTINCT a.transaction_id) FILTER (WHERE a.authorization_status = 'DECLINED') as declined_transactions,
    COUNT(DISTINCT a.transaction_id) FILTER (WHERE a.authorization_status = 'APPROVED') as approved_transactions,
    ROUND(100.0 * COUNT(DISTINCT a.transaction_id) FILTER (WHERE a.authorization_status = 'DECLINED') / COUNT(DISTINCT a.transaction_id), 2) as decline_rate_pct,
    ROUND(100.0 * COUNT(DISTINCT a.transaction_id) FILTER (WHERE a.authorization_status = 'APPROVED') / COUNT(DISTINCT a.transaction_id), 2) as approval_rate_pct
FROM merchants m
JOIN auth_transactions a ON m.merchant_id = a.merchant_id
GROUP BY m.risk_level
ORDER BY
    CASE m.risk_level
        WHEN 'LOW' THEN 1
        WHEN 'MEDIUM' THEN 2
        WHEN 'HIGH' THEN 3
    END;

-- View: Settlement Timeframe Distribution
CREATE OR REPLACE VIEW v_settlement_timeframe_analysis AS
SELECT
    days_to_settle,
    COUNT(*) as settlement_count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) as percentage,
    CASE
        WHEN days_to_settle = 0 THEN 'Same Day'
        WHEN days_to_settle = 1 THEN 'Next Day'
        WHEN days_to_settle BETWEEN 2 AND 3 THEN '2-3 Days'
        WHEN days_to_settle BETWEEN 4 AND 7 THEN '4-7 Days'
        WHEN days_to_settle > 7 THEN '>7 Days (Dispute Resolution)'
        ELSE 'Other'
    END as timeframe_category
FROM v_auth_settlement_status
WHERE settlement_status = 'SETTLED'
GROUP BY days_to_settle
ORDER BY days_to_settle;

-- View: Enhanced Settlement Variance Analysis
CREATE OR REPLACE VIEW v_enhanced_settlement_variance AS
WITH variance_ranges AS (
    SELECT
        s.transaction_id,
        s.auth_transaction_id,
        s.merchant_id,
        m.merchant_name,
        m.merchant_category_name,
        m.risk_level,
        a.transaction_amount as auth_amount,
        s.acquirer_settlement_amount,
        s.settlement_delta_pct,
        CASE
            WHEN s.settlement_delta_pct = 0 THEN 'No Change (0%)'
            WHEN s.settlement_delta_pct > 0 AND s.settlement_delta_pct <= 1.0 THEN '0-1% Variance'
            WHEN s.settlement_delta_pct > 1.0 AND s.settlement_delta_pct <= 2.0 THEN '1-2% Variance'
            WHEN s.settlement_delta_pct > 2.0 AND s.settlement_delta_pct <= 5.0 THEN '2-5% Variance'
            WHEN s.settlement_delta_pct > 5.0 THEN '>5% Variance'
            ELSE 'Other'
        END AS variance_category
    FROM settlement_transactions s
    JOIN auth_transactions a ON s.auth_transaction_id = a.transaction_id
    JOIN merchants m ON s.merchant_id = m.merchant_id
)
SELECT
    variance_category,
    COUNT(*) as transaction_count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) as percentage,
    ROUND(AVG(settlement_delta_pct)::numeric, 3) as avg_variance_pct,
    ROUND(MAX(settlement_delta_pct)::numeric, 3) as max_variance_pct,
    COUNT(*) FILTER (WHERE merchant_category_name IN ('HOTELS_MOTELS', 'GAS_STATIONS', 'AIRLINES', 'RESTAURANTS')) as high_variance_category_count
FROM variance_ranges
GROUP BY variance_category
ORDER BY
    CASE variance_category
        WHEN 'No Change (0%)' THEN 1
        WHEN '0-1% Variance' THEN 2
        WHEN '1-2% Variance' THEN 3
        WHEN '2-5% Variance' THEN 4
        WHEN '>5% Variance' THEN 5
        ELSE 6
    END;

-- =====================================================
-- Utility Functions
-- =====================================================

-- Function to get transaction summary by date range
CREATE OR REPLACE FUNCTION get_transaction_summary(
    start_date DATE,
    end_date DATE
)
RETURNS TABLE (
    total_auth_count BIGINT,
    total_auth_amount NUMERIC,
    total_settlement_count BIGINT,
    total_settlement_amount NUMERIC,
    unsettled_count BIGINT,
    avg_settlement_days NUMERIC,
    high_variance_count BIGINT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        COUNT(DISTINCT a.transaction_id)::BIGINT,
        SUM(a.transaction_amount),
        COUNT(DISTINCT s.transaction_id)::BIGINT,
        SUM(s.acquirer_settlement_amount),
        COUNT(DISTINCT a.transaction_id) FILTER (WHERE s.transaction_id IS NULL)::BIGINT,
        AVG(s.transaction_settlement_date - a.transaction_date),
        COUNT(DISTINCT s.transaction_id) FILTER (WHERE s.settlement_delta_pct > 2)::BIGINT
    FROM auth_transactions a
    LEFT JOIN settlement_transactions s ON a.transaction_id = s.auth_transaction_id
    WHERE a.transaction_date BETWEEN start_date AND end_date;
END;
$$ LANGUAGE plpgsql;

-- Function to get merchant risk analysis
CREATE OR REPLACE FUNCTION get_merchant_risk_analysis(
    merchant_id_param VARCHAR(20)
)
RETURNS TABLE (
    merchant_name VARCHAR(255),
    total_transactions BIGINT,
    total_volume NUMERIC,
    settlement_rate NUMERIC,
    avg_variance_pct NUMERIC,
    high_variance_count BIGINT,
    risk_score NUMERIC
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        m.merchant_name,
        COUNT(DISTINCT a.transaction_id)::BIGINT,
        SUM(a.transaction_amount),
        ROUND(100.0 * COUNT(DISTINCT s.transaction_id) / NULLIF(COUNT(DISTINCT a.transaction_id), 0), 2),
        ROUND(AVG(s.settlement_delta_pct)::numeric, 2),
        COUNT(DISTINCT s.transaction_id) FILTER (WHERE s.settlement_delta_pct > 2)::BIGINT,
        -- Risk score: weighted combination of variance and settlement issues
        ROUND((
            COALESCE(AVG(s.settlement_delta_pct), 0) * 10 +
            (100 - COALESCE(100.0 * COUNT(DISTINCT s.transaction_id) / NULLIF(COUNT(DISTINCT a.transaction_id), 0), 100)) * 0.5
        )::numeric, 2)
    FROM merchants m
    LEFT JOIN auth_transactions a ON m.merchant_id = a.merchant_id
    LEFT JOIN settlement_transactions s ON a.transaction_id = s.auth_transaction_id
    WHERE m.merchant_id = merchant_id_param
    GROUP BY m.merchant_name;
END;
$$ LANGUAGE plpgsql;

-- =====================================================
-- Comments for Documentation
-- =====================================================

COMMENT ON TABLE auth_transactions IS 'FinIQ: Authorization transactions representing initial card transaction requests';
COMMENT ON TABLE settlement_transactions IS 'FinIQ: Settlement transactions representing final cleared payments';
COMMENT ON TABLE merchants IS 'FinIQ: Merchants accepting card payments';
COMMENT ON COLUMN auth_transactions.transaction_code IS 'Transaction response code: 000=approved, 100=decline, 101=pickup, 102=refer';
COMMENT ON COLUMN settlement_transactions.interchange_fee IS 'Fee charged by issuer to acquirer';
COMMENT ON COLUMN settlement_transactions.network_fee IS 'Fee charged by card network (Amex/Visa/MC)';
COMMENT ON COLUMN settlement_transactions.settlement_delta_pct IS 'Percentage variance between auth and settlement amounts';
COMMENT ON COLUMN merchants.merchant_category_code IS 'ISO 18245 Merchant Category Code (MCC)';
COMMENT ON COLUMN merchants.risk_level IS 'Merchant risk classification: LOW, MEDIUM, HIGH';

-- Grant permissions (adjust as needed for your environment)
-- GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO finiq_app_user;
-- GRANT SELECT ON ALL SEQUENCES IN SCHEMA public TO finiq_app_user;