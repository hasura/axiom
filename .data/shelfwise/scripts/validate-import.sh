#!/bin/bash
# Validate Nightly Import Results
# 
# This script checks if the nightly import completed successfully by:
# 1. Checking for data on expected dates
# 2. Verifying row counts are reasonable
# 3. Checking for gaps in the data
# 4. Validating data integrity

set -e

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SHELFWISE_HOME="$(dirname "$SCRIPT_DIR")"

# Load database credentials
if [ -f "$SHELFWISE_HOME/.env" ]; then
    source "$SHELFWISE_HOME/.env"
fi

echo "========================================="
echo "ShelfWise Nightly Import Validation"
echo "========================================="
echo ""

# 1. Check date range coverage
echo "1. Checking date range coverage..."
echo "-----------------------------------"
psql -c "
SELECT 
    MIN(date) as first_date,
    MAX(date) as last_date,
    COUNT(DISTINCT date) as total_days
FROM sales_daily;
"

# 2. Check for gaps in dates
echo ""
echo "2. Checking for gaps in dates..."
echo "-----------------------------------"
GAPS=$(psql -t -c "
WITH date_series AS (
    SELECT generate_series(
        (SELECT MIN(date) FROM sales_daily),
        (SELECT MAX(date) FROM sales_daily),
        '1 day'::interval
    )::date AS expected_date
),
actual_dates AS (
    SELECT DISTINCT date FROM sales_daily
)
SELECT COUNT(*) 
FROM date_series 
LEFT JOIN actual_dates ON date_series.expected_date = actual_dates.date
WHERE actual_dates.date IS NULL;
" | xargs)

if [ "$GAPS" -eq 0 ]; then
    echo "✓ No gaps found - continuous date coverage"
else
    echo "⚠ WARNING: Found $GAPS missing dates"
    psql -c "
    WITH date_series AS (
        SELECT generate_series(
            (SELECT MIN(date) FROM sales_daily),
            (SELECT MAX(date) FROM sales_daily),
            '1 day'::interval
        )::date AS expected_date
    ),
    actual_dates AS (
        SELECT DISTINCT date FROM sales_daily
    )
    SELECT date_series.expected_date as missing_date
    FROM date_series 
    LEFT JOIN actual_dates ON date_series.expected_date = actual_dates.date
    WHERE actual_dates.date IS NULL
    ORDER BY expected_date;
    "
fi

# 3. Check row counts per date (last 7 days)
echo ""
echo "3. Row counts for last 7 days..."
echo "-----------------------------------"
psql -c "
SELECT 
    date,
    (SELECT COUNT(*) FROM sales_daily WHERE date = s.date) as sales,
    (SELECT COUNT(*) FROM inventory_daily WHERE date = s.date) as inventory,
    (SELECT COUNT(*) FROM transactions WHERE date = s.date) as transactions,
    (SELECT COUNT(*) FROM transaction_line_items WHERE transaction_id IN 
        (SELECT transaction_id FROM transactions WHERE date = s.date)) as line_items
FROM (SELECT DISTINCT date FROM sales_daily ORDER BY date DESC LIMIT 7) s
ORDER BY date DESC;
"

# 4. Check for reasonable volumes
echo ""
echo "4. Checking data volumes (last date)..."
echo "-----------------------------------"
LAST_DATE=$(psql -t -c "SELECT MAX(date) FROM sales_daily;" | xargs)
echo "Last date with data: $LAST_DATE"
echo ""

psql -c "
SELECT 
    'sales_daily' as table_name,
    COUNT(*) as row_count,
    CASE 
        WHEN COUNT(*) BETWEEN 1000 AND 5000 THEN '✓ Normal'
        WHEN COUNT(*) > 0 THEN '⚠ Unusual'
        ELSE '✗ Empty'
    END as status
FROM sales_daily WHERE date = '$LAST_DATE'
UNION ALL
SELECT 
    'transactions',
    COUNT(*),
    CASE 
        WHEN COUNT(*) BETWEEN 5000 AND 15000 THEN '✓ Normal'
        WHEN COUNT(*) > 0 THEN '⚠ Unusual'
        ELSE '✗ Empty'
    END
FROM transactions WHERE date = '$LAST_DATE'
UNION ALL
SELECT 
    'transaction_line_items',
    COUNT(*),
    CASE 
        WHEN COUNT(*) BETWEEN 20000 AND 60000 THEN '✓ Normal'
        WHEN COUNT(*) > 0 THEN '⚠ Unusual'
        ELSE '✗ Empty'
    END
FROM transaction_line_items 
WHERE transaction_id IN (SELECT transaction_id FROM transactions WHERE date = '$LAST_DATE')
UNION ALL
SELECT 
    'delivery_assignments',
    COUNT(*),
    CASE 
        WHEN COUNT(*) BETWEEN 500 AND 2000 THEN '✓ Normal'
        WHEN COUNT(*) > 0 THEN '⚠ Unusual'
        ELSE '✗ Empty'
    END
FROM delivery_assignments 
WHERE transaction_id IN (SELECT transaction_id FROM transactions WHERE date = '$LAST_DATE');
"

# 5. Check customer growth
echo ""
echo "5. Checking customer growth..."
echo "-----------------------------------"
psql -c "
WITH daily_customers AS (
    SELECT 
        date,
        (SELECT COUNT(*) FROM customers WHERE customer_id <= 
            (SELECT MAX(customer_id) FROM transactions t2 WHERE t2.date <= t1.date)
        ) as total_customers
    FROM (SELECT DISTINCT date FROM transactions ORDER BY date DESC LIMIT 7) t1
)
SELECT 
    date,
    total_customers,
    total_customers - LAG(total_customers) OVER (ORDER BY date) as daily_growth
FROM daily_customers
ORDER BY date DESC;
"

# 6. Check for data integrity issues
echo ""
echo "6. Checking data integrity..."
echo "-----------------------------------"

# Check for orphaned records
ORPHANED_ITEMS=$(psql -t -c "
SELECT COUNT(*) 
FROM transaction_line_items tli
LEFT JOIN transactions t ON tli.transaction_id = t.transaction_id
WHERE t.transaction_id IS NULL;
" | xargs)

if [ "$ORPHANED_ITEMS" -eq 0 ]; then
    echo "✓ No orphaned transaction line items"
else
    echo "✗ ERROR: Found $ORPHANED_ITEMS orphaned transaction line items"
fi

# Check for invalid dates
FUTURE_DATES=$(psql -t -c "
SELECT COUNT(*) FROM transactions WHERE date > CURRENT_DATE;
" | xargs)

if [ "$FUTURE_DATES" -eq 0 ]; then
    echo "✓ No future-dated transactions"
else
    echo "⚠ WARNING: Found $FUTURE_DATES transactions with future dates"
fi

# 7. Summary
echo ""
echo "========================================="
echo "Validation Summary"
echo "========================================="
echo "Date range: $(psql -t -c "SELECT MIN(date) || ' to ' || MAX(date) FROM sales_daily;" | xargs)"
echo "Total days: $(psql -t -c "SELECT COUNT(DISTINCT date) FROM sales_daily;" | xargs)"
echo "Total transactions: $(psql -t -c "SELECT COUNT(*) FROM transactions;" | xargs)"
echo "Total customers: $(psql -t -c "SELECT COUNT(*) FROM customers;" | xargs)"
echo ""

if [ "$GAPS" -eq 0 ] && [ "$ORPHANED_ITEMS" -eq 0 ]; then
    echo "✓ All validation checks passed!"
    exit 0
else
    echo "⚠ Some validation checks failed - review output above"
    exit 1
fi