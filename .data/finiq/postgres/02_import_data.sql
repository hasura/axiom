-- =====================================================
-- FinIQ - Financial Intelligence & Quality Platform
-- Database: fin_recon
-- Purpose: Import CSV data into PostgreSQL database
-- Version: 2.0 (with Merchants & Enhanced Analytics)
-- =====================================================

-- This script assumes CSV files are in /docker-entrypoint-initdb.d/demo_data/
-- For Docker, mount your demo_data directory to this path

-- =====================================================
-- Import Issuers
-- =====================================================

\echo 'Importing issuers...'

COPY issuers (
    issuer_id,
    issuer_name,
    issuer_country,
    primary_currency,
    created_at
)
FROM '/docker-entrypoint-initdb.d/demo_data/issuers.csv'
DELIMITER ','
CSV HEADER;

\echo 'Issuers imported successfully'

-- =====================================================
-- Import Acquirers
-- =====================================================

\echo 'Importing acquirers...'

COPY acquirers (
    acquirer_id,
    acquirer_name,
    acquirer_country,
    primary_currency,
    created_at
)
FROM '/docker-entrypoint-initdb.d/demo_data/acquirers.csv'
DELIMITER ','
CSV HEADER;

\echo 'Acquirers imported successfully'

-- =====================================================
-- Import Merchants
-- =====================================================

\echo 'Importing merchants...'

COPY merchants (
    merchant_id,
    merchant_name,
    merchant_category_code,
    merchant_category_name,
    merchant_country,
    acquirer_id,
    annual_volume,
    risk_level,
    created_at
)
FROM '/docker-entrypoint-initdb.d/demo_data/merchants.csv'
DELIMITER ','
CSV HEADER;

\echo 'Merchants imported successfully'

-- =====================================================
-- Import Authorization Transactions
-- =====================================================

\echo 'Importing authorization transactions...'

COPY auth_transactions (
    transaction_id,
    issuer_id,
    acquirer_id,
    merchant_id,
    transaction_amount,
    transaction_date,
    transaction_timestamp,
    transaction_type,
    issuer_currency,
    acquirer_currency,
    transaction_code,
    card_last_four,
    authorization_status,
    created_at
)
FROM '/docker-entrypoint-initdb.d/demo_data/auth_transactions.csv'
DELIMITER ','
CSV HEADER
NULL '';

\echo 'Authorization transactions imported successfully'

-- =====================================================
-- Import Settlement Transactions
-- =====================================================

\echo 'Importing settlement transactions...'

COPY settlement_transactions (
    transaction_id,
    auth_transaction_id,
    issuer_id,
    acquirer_id,
    merchant_id,
    transaction_amount,
    transaction_date,
    transaction_type,
    issuer_currency,
    acquirer_currency,
    acquirer_settlement_amount,
    issuer_settlement_amount,
    acquirer_settlement_date,
    issuer_settlement_date,
    transaction_settlement_date,
    settlement_status,
    interchange_fee,
    network_fee,
    created_at
)
FROM '/docker-entrypoint-initdb.d/demo_data/settlement_transactions.csv'
DELIMITER ','
CSV HEADER;

\echo 'Settlement transactions imported successfully'

-- =====================================================
-- Verify Data Import
-- =====================================================

\echo ''
\echo '====================================================='
\echo 'Data Import Summary'
\echo '====================================================='

SELECT 'Issuers' as table_name, COUNT(*) as record_count FROM issuers
UNION ALL
SELECT 'Acquirers', COUNT(*) FROM acquirers
UNION ALL
SELECT 'Merchants', COUNT(*) FROM merchants
UNION ALL
SELECT 'Auth Transactions', COUNT(*) FROM auth_transactions
UNION ALL
SELECT 'Settlement Transactions', COUNT(*) FROM settlement_transactions;

\echo ''
\echo 'Merchant Category Distribution:'
SELECT
    merchant_category_name,
    COUNT(*) as merchant_count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1) as percentage
FROM merchants
GROUP BY merchant_category_name
ORDER BY merchant_count DESC
LIMIT 10;

\echo ''
\echo 'Merchant Risk Level Distribution:'
SELECT
    risk_level,
    COUNT(*) as merchant_count,
    ROUND(AVG(annual_volume)::numeric, 2) as avg_annual_volume
FROM merchants
GROUP BY risk_level
ORDER BY
    CASE risk_level
        WHEN 'LOW' THEN 1
        WHEN 'MEDIUM' THEN 2
        WHEN 'HIGH' THEN 3
    END;

\echo ''
\echo 'Transaction Volume by Month (Last 12 Months):'
SELECT
    TO_CHAR(transaction_date, 'YYYY-MM') as month,
    COUNT(*) as auth_count,
    ROUND(SUM(transaction_amount)::numeric, 2) as total_auth_amount,
    ROUND(AVG(transaction_amount)::numeric, 2) as avg_transaction_amount
FROM auth_transactions
GROUP BY TO_CHAR(transaction_date, 'YYYY-MM')
ORDER BY month DESC
LIMIT 12;

\echo ''
\echo 'Data import complete!'
\echo '====================================================='
\echo ''

-- =====================================================
-- Sample PromptQL Queries Documentation
-- =====================================================

\echo 'Sample PromptQL Natural Language Queries:'
\echo ''
\echo '=== Basic Transaction Queries ==='
\echo '  "Show me all transactions from last week"'
\echo '  "What are the declined transactions today?"'
\echo '  "Find all transactions over $5000"'
\echo ''
\echo '=== Merchant Analysis ==='
\echo '  "Which merchants have the highest settlement variance?"'
\echo '  "Show me top 10 merchants by transaction volume"'
\echo '  "What restaurants had settlement issues this month?"'
\echo '  "Compare gas stations vs grocery stores settlement rates"'
\echo ''
\echo '=== Settlement Analysis ==='
\echo '  "Find settlements with variance greater than 2%"'
\echo '  "Show unsettled transactions over $1000"'
\echo '  "Which transactions took more than 3 days to settle?"'
\echo '  "Calculate settlement success rate by merchant category"'
\echo ''
\echo '=== Missing Data Analysis ==='
\echo '  "How many transactions are missing transaction codes?"'
\echo '  "Show auth transactions without response codes from yesterday"'
\echo '  "What percentage of restaurant transactions have missing codes?"'
\echo ''
\echo '=== Financial Analysis ==='
\echo '  "Calculate total interchange fees by issuer"'
\echo '  "What is the average transaction amount for hotels?"'
\echo '  "Show merchant categories ranked by total volume"'
\echo '  "Compare network fees across different merchant types"'
\echo ''
\echo '=== Risk & Compliance ==='
\echo '  "Identify high-risk merchants with settlement problems"'
\echo '  "Show merchants with above-average variance rates"'
\echo '  "Find patterns in settlement mismatches by merchant category"'
\echo '  "Which acquirers have the most high-variance settlements?"'
\echo ''
\echo '=== Temporal Analysis ==='
\echo '  "Compare Q1 vs Q2 transaction volumes"'
\echo '  "Show settlement trends by day of week"'
\echo '  "What is the average time to settlement by merchant type?"'
\echo '  "Analyze transaction patterns during peak hours"'
\echo ''
\echo '=== Executive Summaries ==='
\echo '  "Give me a summary of last month transactions"'
\echo '  "Show merchant performance dashboard metrics"'
\echo '  "Calculate key settlement KPIs for this quarter"'
\echo '  "What are the top issues affecting settlement rates?"'
\echo ''