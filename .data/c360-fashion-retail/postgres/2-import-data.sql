-- C360 Retail Fashion Database - Data Loading Script
-- Loads all CSV data files in correct dependency order

-- Load brands first (no dependencies)
\COPY brands FROM '/docker-entrypoint-initdb.d/brands.csv' CSV HEADER;

-- Load categories (no dependencies) 
\COPY categories FROM '/docker-entrypoint-initdb.d/categories.csv' CSV HEADER;

-- Load products (depends on brands/categories via names, not FKs)
\COPY products FROM '/docker-entrypoint-initdb.d/products.csv' CSV HEADER;

-- Load product variants (depends on products)
\COPY product_variants FROM '/docker-entrypoint-initdb.d/product_variants.csv' CSV HEADER;

-- Load customers (no dependencies)
\COPY customers FROM '/docker-entrypoint-initdb.d/customers.csv' CSV HEADER;

-- Load customer addresses (depends on customers)
\COPY customer_addresses FROM '/docker-entrypoint-initdb.d/customer_addresses.csv' CSV HEADER;

-- Load orders (depends on customers)
\COPY orders FROM '/docker-entrypoint-initdb.d/orders.csv' CSV HEADER;

-- Load order items (depends on orders and products)
\COPY order_items FROM '/docker-entrypoint-initdb.d/order_items.csv' CSV HEADER;

-- Load returns (depends on orders and customers)
\COPY returns FROM '/docker-entrypoint-initdb.d/returns.csv' CSV HEADER;

-- Load return items (depends on returns and order_items)
\COPY return_items FROM '/docker-entrypoint-initdb.d/return_items.csv' CSV HEADER;

-- Load reviews (depends on customers and orders)
\COPY reviews FROM '/docker-entrypoint-initdb.d/reviews.csv' CSV HEADER;

-- Load social mentions (depends on customers)
\COPY social_mentions FROM '/docker-entrypoint-initdb.d/social_mentions.csv' CSV HEADER;

-- Load website sessions (depends on customers)
\COPY website_sessions FROM '/docker-entrypoint-initdb.d/website_sessions.csv' CSV HEADER;

-- Load style similarity matches (depends on products)
\COPY style_similarity_matches FROM '/docker-entrypoint-initdb.d/style_similarity_matches.csv' CSV HEADER;

-- Load optional/auxiliary CSVs if they exist (psql \COPY with ON_ERROR_STOP avoids failure)
\COPY campaigns FROM '/docker-entrypoint-initdb.d/campaigns.csv' CSV HEADER;
\COPY campaign_responses FROM '/docker-entrypoint-initdb.d/campaign_responses.csv' CSV HEADER;
\COPY customer_service_interactions FROM '/docker-entrypoint-initdb.d/customer_service_interactions.csv' CSV HEADER;
\COPY email_engagement FROM '/docker-entrypoint-initdb.d/email_engagement.csv' CSV HEADER;
\COPY loyalty_activities FROM '/docker-entrypoint-initdb.d/loyalty_activities.csv' CSV HEADER;
\COPY loyalty_profiles FROM '/docker-entrypoint-initdb.d/loyalty_profiles.csv' CSV HEADER;
\COPY session_summary FROM '/docker-entrypoint-initdb.d/session_summary.csv' CSV HEADER;

-- Ensure ON CONFLICT inserts work (add unique constraint on session_summary.date if not exists)
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 
        FROM pg_constraint 
        WHERE conname = 'session_summary_date_key'
    ) THEN
        EXECUTE 'ALTER TABLE session_summary ADD CONSTRAINT session_summary_date_key UNIQUE (summary_date)';
    END IF;
END $$;

-- Update sequences to match the highest IDs from imported data
DO $$
DECLARE
    seq_name TEXT;
    tbl_name TEXT;
    col_name TEXT;
    max_id INTEGER;
BEGIN
    -- Find each sequence and its owning table/column
    FOR seq_name, tbl_name, col_name IN
        SELECT s.sequence_name, c.table_name, c.column_name
        FROM information_schema.sequences s
        JOIN information_schema.columns c 
          ON c.column_default LIKE ('%' || s.sequence_name || '%')
        WHERE s.sequence_schema = 'public'
    LOOP
        EXECUTE format('SELECT COALESCE(MAX(%I), 0) FROM %I', col_name, tbl_name)
        INTO max_id;

        IF max_id > 0 THEN
            EXECUTE format('SELECT setval(%L, %s, true)', seq_name, max_id);
            RAISE NOTICE 'Updated sequence % to %', seq_name, max_id;
        END IF;
    END LOOP;
END $$;

-- Create some sample data for tables that might be empty to ensure they're functional
INSERT INTO campaigns (campaign_id, campaign_name, campaign_type, start_date, end_date, budget_allocated, target_audience, status)
VALUES
    ('CAMP001', 'Spring Fashion Launch', 'product_launch', CURRENT_DATE - INTERVAL '30 days', CURRENT_DATE + INTERVAL '30 days', 50000.00, 'Young professionals aged 25-35', 'active'),
    ('CAMP002', 'Summer Sale Campaign', 'promotional', CURRENT_DATE - INTERVAL '15 days', CURRENT_DATE + INTERVAL '45 days', 75000.00, 'All customers', 'active')
ON CONFLICT (campaign_id) DO NOTHING;

INSERT INTO session_summary (summary_date, total_sessions, unique_visitors, avg_session_duration)
VALUES
    (CURRENT_DATE - INTERVAL '1 day', 1250, 980, 505), -- 8.45 minutes in seconds
    (CURRENT_DATE - INTERVAL '2 days', 1180, 920, 469)  -- 7.82 minutes in seconds
ON CONFLICT (summary_date) DO NOTHING;

-- Show loading summary for core business tables only
DO $$
DECLARE
    rec RECORD;
    total_tables INTEGER := 0;
    total_rows BIGINT := 0;
BEGIN
    RAISE NOTICE '=== C360 RETAIL FASHION DATA LOADING SUMMARY ===';
    
    FOR rec IN
        SELECT
            t.table_name,
            COALESCE(s.n_tup_ins, 0) as rows_loaded
        FROM information_schema.tables t
        LEFT JOIN pg_stat_user_tables s 
          ON s.relname = t.table_name AND s.schemaname = 'public'
        WHERE t.table_schema = 'public'
          AND t.table_type = 'BASE TABLE'
          AND t.table_name NOT LIKE 'staging_%'
        ORDER BY t.table_name
    LOOP
        RAISE NOTICE 'Table: % - Rows: %', rec.table_name, rec.rows_loaded;
        total_tables := total_tables + 1;
        total_rows := total_rows + rec.rows_loaded;
    END LOOP;
    
    RAISE NOTICE '=== SUMMARY: % tables loaded with % total rows ===', total_tables, total_rows;
END $$;

-- Create a view for table row counts (useful for monitoring)
CREATE OR REPLACE VIEW table_row_counts AS
SELECT
    t.table_name,
    COALESCE(s.n_tup_ins, 0) as total_rows,
    COALESCE(s.n_tup_upd, 0) as updated_rows,
    COALESCE(s.n_tup_del, 0) as deleted_rows,
    s.last_vacuum,
    s.last_analyze,
    pg_size_pretty(pg_total_relation_size('public.'||t.table_name)) as table_size
FROM information_schema.tables t
LEFT JOIN pg_stat_user_tables s ON s.relname = t.table_name AND s.schemaname = 'public'
WHERE t.table_schema = 'public'
  AND t.table_type = 'BASE TABLE'
  AND t.table_name NOT LIKE 'staging_%'
ORDER BY s.n_tup_ins DESC NULLS LAST, t.table_name;

ANALYZE; -- Update table statistics for query optimization

\echo 'C360 Retail Fashion Database loading completed successfully!'
\echo 'Use: SELECT * FROM table_row_counts; to see loaded data summary'
