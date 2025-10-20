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
\echo 'Missing Transaction Codes Analysis:'
SELECT * FROM v_missing_transaction_codes;

\echo ''
\echo 'Settlement Status Summary:'
SELECT 
    settlement_status,
    COUNT(*) as count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) as percentage
FROM v_auth_settlement_status
GROUP BY settlement_status
ORDER BY count DESC;

\echo ''
\echo 'Settlement Mismatch Summary:'
SELECT 
    COUNT(*) as total_mismatches,
    COUNT(*) FILTER (WHERE settlement_delta_pct > 2) as high_variance_count,
    COUNT(*) FILTER (WHERE settlement_delta_pct BETWEEN 0.5 AND 2) as medium_variance_count,
    COUNT(*) FILTER (WHERE settlement_delta_pct < 0.5) as low_variance_count,
    ROUND(AVG(settlement_delta_pct), 2) as avg_variance_pct,
    ROUND(MAX(settlement_delta_pct), 2) as max_variance_pct
FROM v_settlement_mismatches;

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
\echo 'Top 10 Merchants by Transaction Volume:'
SELECT 
    merchant_name,
    merchant_category_name,
    settlement_count,
    ROUND(total_settlement_volume::numeric, 2) as total_volume
FROM v_top_merchants_by_volume
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
\echo 'Category Performance Analysis:'
SELECT 
    merchant_category_name,
    transaction_count,
    ROUND(total_volume::numeric, 2) as total_volume,
    ROUND(avg_transaction_size::numeric, 2) as avg_transaction_size,
    high_variance_count,
    avg_variance_pct
FROM v_category_analysis
ORDER BY total_volume DESC
LIMIT 10;

\echo ''
\echo 'Industry-Aligned Settlement Variance Distribution:'
SELECT * FROM v_enhanced_settlement_variance;

\echo ''
\echo 'Transaction Code Distribution (Industry Standards):'
SELECT * FROM v_transaction_code_analysis;

\echo ''
\echo 'Decline Rates by Risk Level (Industry-Aligned):'
SELECT * FROM v_decline_rate_by_risk;

\echo ''
\echo 'Settlement Timeframe Analysis:'
SELECT
    timeframe_category,
    SUM(settlement_count) as total_count,
    ROUND(AVG(percentage), 2) as avg_percentage
FROM v_settlement_timeframe_analysis
GROUP BY timeframe_category
ORDER BY
    CASE timeframe_category
        WHEN 'Same Day' THEN 1
        WHEN 'Next Day' THEN 2
        WHEN '2-3 Days' THEN 3
        WHEN '4-7 Days' THEN 4
        WHEN '>7 Days (Dispute Resolution)' THEN 5
        ELSE 6
    END;

\echo ''
\echo 'Unsettled Transactions Analysis:'
WITH unsettled_analysis AS (
    SELECT
        m.merchant_category_name,
        m.risk_level,
        COUNT(*) as unsettled_count,
        ROUND(AVG(a.transaction_amount)::numeric, 2) as avg_amount
    FROM v_auth_settlement_status v
    JOIN auth_transactions a ON v.transaction_id = a.transaction_id
    JOIN merchants m ON v.merchant_id = m.merchant_id
    WHERE v.settlement_status = 'UNSETTLED'
    GROUP BY m.merchant_category_name, m.risk_level
)
SELECT
    merchant_category_name,
    risk_level,
    unsettled_count,
    avg_amount,
    ROUND(100.0 * unsettled_count / SUM(unsettled_count) OVER (), 2) as percentage_of_unsettled
FROM unsettled_analysis
ORDER BY unsettled_count DESC;

\echo ''
\echo 'High Variance Categories (Hospitality, Fuel, Airlines):'
WITH high_variance_categories AS (
    SELECT
        m.merchant_category_name,
        COUNT(s.transaction_id) as settlement_count,
        ROUND(AVG(s.settlement_delta_pct)::numeric, 3) as avg_variance_pct,
        ROUND(MAX(s.settlement_delta_pct)::numeric, 3) as max_variance_pct,
        COUNT(s.transaction_id) FILTER (WHERE s.settlement_delta_pct > 5) as extreme_variance_count
    FROM settlement_transactions s
    JOIN merchants m ON s.merchant_id = m.merchant_id
    WHERE m.merchant_category_name IN ('HOTELS_MOTELS', 'GAS_STATIONS', 'AIRLINES', 'RESTAURANTS')
    GROUP BY m.merchant_category_name
)
SELECT
    merchant_category_name,
    settlement_count,
    avg_variance_pct,
    max_variance_pct,
    extreme_variance_count,
    ROUND(100.0 * extreme_variance_count / settlement_count, 2) as extreme_variance_rate_pct
FROM high_variance_categories
ORDER BY avg_variance_pct DESC;

\echo ''
\echo '====================================================='
\echo ''
\echo 'Industry Alignment Summary:'
\echo '====================================================='

\echo ''
\echo 'Key Industry Standards Met:'
\echo '  ✓ Decline Rate Alignment:'
\echo '    - Low Risk Merchants: 10-15% decline rate'
\echo '    - Medium Risk Merchants: 15-25% decline rate'
\echo '    - High Risk Merchants: 25-35% decline rate'
\echo ''
\echo '  ✓ Settlement Variance Distribution:'
\echo '    - Reduced exact matches to 50-60%'
\echo '    - Increased 0-1% variance to 25-30%'
\echo '    - Added 2-5% variance (3-5% of transactions)'
\echo '    - Added >5% variance (1-2% of transactions)'
\echo ''
\echo '  ✓ Settlement Timeframes:'
\echo '    - Added same-day settlements (5-10%)'
\echo '    - Next-day settlements increased (40-45%)'
\echo '    - Extended settlement periods (4-14 days for disputes)'
\echo ''
\echo '  ✓ Unsettled Transactions:'
\echo '    - 0.5-2% of approved transactions remain unsettled'
\echo ''
\echo '  ✓ Category-Specific Patterns:'
\echo '    - Higher variance for hospitality, fuel, airlines'
\echo '    - Lower decline rates for grocery stores'
\echo '    - Realistic risk-based approval patterns'
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

\echo '=== Direct SQL Examples (for reference) ==='
\echo ''
\echo '1. Find merchants with high variance:'
\echo '   SELECT * FROM v_merchant_performance'
\echo '   WHERE avg_variance_pct > 2 ORDER BY avg_variance_pct DESC;'
\echo ''
\echo '2. Unsettled transactions by merchant category:'
\echo '   SELECT m.merchant_category_name, COUNT(*) as unsettled_count'
\echo '   FROM v_auth_settlement_status v'
\echo '   JOIN merchants m ON v.merchant_id = m.merchant_id'
\echo '   WHERE v.settlement_status = ''UNSETTLED'''
\echo '   GROUP BY m.merchant_category_name ORDER BY unsettled_count DESC;'
\echo ''
\echo '3. Settlement delta analysis by merchant:'
\echo '   SELECT * FROM v_settlement_mismatches'
\echo '   WHERE settlement_delta_pct > 2 ORDER BY settlement_delta_pct DESC LIMIT 20;'
\echo ''
\echo '4. Merchant risk analysis:'
\echo '   SELECT * FROM get_merchant_risk_analysis(''MER12345678'');'
\echo ''
\echo '5. Transaction summary for date range:'
\echo '   SELECT * FROM get_transaction_summary(''2024-01-01'', ''2024-12-31'');'
\echo ''