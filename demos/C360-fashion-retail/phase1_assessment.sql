-- C360 Fashion Retail Database: Phase 1 - Pre-Implementation Assessment
-- This script implements the assessment phase of the foreign key implementation plan

-- =============================================================================
-- PHASE 1.1: Setup Progress Tracking
-- =============================================================================

-- Create progress tracking table
CREATE TABLE IF NOT EXISTS fk_implementation_progress (
    id SERIAL PRIMARY KEY,
    phase VARCHAR(50),
    step VARCHAR(100),
    table_name VARCHAR(100),
    status VARCHAR(20) DEFAULT 'pending', -- pending, in_progress, completed, failed
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    error_message TEXT,
    rollback_sql TEXT,
    notes TEXT
);

-- Clear any previous progress
TRUNCATE TABLE fk_implementation_progress;

-- Insert initial phase tracking
INSERT INTO fk_implementation_progress (phase, step, status) VALUES
('Phase1', '1.1 Setup Progress Tracking', 'completed'),
('Phase1', '1.2 Database Schema Assessment', 'pending'),
('Phase1', '1.3 Data Quality Assessment', 'pending'),
('Phase2', '2.1 Customer ID Standardization', 'pending'),
('Phase2', '2.2 Product ID Standardization', 'pending'),
('Phase2', '2.3 Order ID Standardization', 'pending'),
('Phase3', '3.1 Referential Integrity Validation', 'pending'),
('Phase3', '3.2 Data Cleanup', 'pending'),
('Phase4', '4.1 Column Replacement', 'pending'),
('Phase5', '5.1 Foreign Key Implementation', 'pending');

-- =============================================================================
-- PHASE 1.2: Database Schema Assessment
-- =============================================================================

UPDATE fk_implementation_progress 
SET status = 'in_progress', started_at = CURRENT_TIMESTAMP 
WHERE step = '1.2 Database Schema Assessment';

-- Check current foreign key status
CREATE OR REPLACE VIEW current_foreign_keys AS
SELECT 
    tc.table_name,
    tc.constraint_name,
    kcu.column_name,
    ccu.table_name AS foreign_table_name,
    ccu.column_name AS foreign_column_name 
FROM information_schema.table_constraints AS tc 
JOIN information_schema.key_column_usage AS kcu
    ON tc.constraint_name = kcu.constraint_name
    AND tc.table_schema = kcu.table_schema
JOIN information_schema.constraint_column_usage AS ccu
    ON ccu.constraint_name = tc.constraint_name
    AND ccu.table_schema = tc.table_schema
WHERE tc.constraint_type = 'FOREIGN KEY' 
  AND tc.table_schema = 'public'
ORDER BY tc.table_name, tc.constraint_name;

-- Assess data types for key columns
CREATE OR REPLACE VIEW column_type_assessment AS
SELECT 
    table_name,
    column_name,
    data_type,
    character_maximum_length,
    is_nullable,
    CASE 
        WHEN column_name LIKE '%customer_id%' THEN 'customer_id_group'
        WHEN column_name LIKE '%product_id%' THEN 'product_id_group'
        WHEN column_name LIKE '%order_id%' THEN 'order_id_group'
        ELSE 'other'
    END as column_group
FROM information_schema.columns 
WHERE table_schema = 'public'
  AND (column_name LIKE '%customer_id%' 
    OR column_name LIKE '%product_id%' 
    OR column_name LIKE '%order_id%')
ORDER BY column_group, table_name, column_name;

-- =============================================================================
-- PHASE 1.3: Data Quality Assessment Function
-- =============================================================================

UPDATE fk_implementation_progress 
SET status = 'in_progress', started_at = CURRENT_TIMESTAMP 
WHERE step = '1.3 Data Quality Assessment';

-- Create comprehensive data assessment function
CREATE OR REPLACE FUNCTION assess_data_compatibility()
RETURNS TABLE(
    assessment_type text,
    table_name text,
    column_name text,
    total_rows bigint,
    non_null_rows bigint,
    convertible_rows bigint,
    conversion_success_rate numeric,
    sample_unconvertible text[],
    max_length integer,
    recommended_action text
) AS $$
DECLARE
    table_rec RECORD;
    sql_text TEXT;
    result_record RECORD;
BEGIN
    -- Assess customer_id columns
    FOR table_rec IN 
        SELECT t.table_name, t.column_name, t.data_type
        FROM information_schema.columns t
        WHERE t.table_schema = 'public' 
          AND t.column_name LIKE '%customer_id%'
          AND t.table_name != 'customers' -- Skip the reference table
    LOOP
        sql_text := format('
            WITH assessment AS (
                SELECT 
                    COUNT(*) as total_rows,
                    COUNT(%I) as non_null_rows,
                    COUNT(CASE WHEN %I ~ ''^\\d+$'' THEN 1 END) as convertible_rows,
                    MAX(LENGTH(%I::text)) as max_length
                FROM %I
            ),
            samples AS (
                SELECT ARRAY(
                    SELECT DISTINCT %I::text 
                    FROM %I 
                    WHERE %I IS NOT NULL 
                      AND NOT (%I ~ ''^\\d+$'')
                    LIMIT 5
                ) as unconvertible_samples
            )
            SELECT 
                a.total_rows,
                a.non_null_rows, 
                a.convertible_rows,
                CASE WHEN a.non_null_rows > 0 
                     THEN ROUND(a.convertible_rows * 100.0 / a.non_null_rows, 2)
                     ELSE 100.0 END as success_rate,
                s.unconvertible_samples,
                a.max_length
            FROM assessment a CROSS JOIN samples s',
            table_rec.column_name, table_rec.column_name, table_rec.column_name,
            table_rec.table_name, table_rec.column_name, table_rec.table_name,
            table_rec.column_name, table_rec.column_name
        );
        
        EXECUTE sql_text INTO result_record;
        
        RETURN QUERY SELECT 
            'customer_id_conversion'::text,
            table_rec.table_name,
            table_rec.column_name,
            result_record.total_rows,
            result_record.non_null_rows,
            result_record.convertible_rows,
            result_record.success_rate,
            result_record.unconvertible_samples,
            result_record.max_length,
            CASE 
                WHEN result_record.success_rate >= 95 THEN 'Safe to convert'
                WHEN result_record.success_rate >= 85 THEN 'Convert with cleanup'
                ELSE 'Manual intervention required'
            END;
    END LOOP;
    
    -- Assess product_id columns (converting integer to varchar)
    FOR table_rec IN 
        SELECT t.table_name, t.column_name, t.data_type
        FROM information_schema.columns t
        WHERE t.table_schema = 'public' 
          AND t.column_name LIKE '%product_id%'
          AND t.data_type = 'integer'
          AND t.table_name != 'products'
    LOOP
        sql_text := format('
            SELECT 
                COUNT(*) as total_rows,
                COUNT(%I) as non_null_rows,
                COUNT(%I) as convertible_rows, -- all integers can convert to varchar
                100.0 as success_rate,
                ARRAY[]::text[] as unconvertible_samples,
                MAX(LENGTH(%I::text)) as max_length
            FROM %I',
            table_rec.column_name, table_rec.column_name, table_rec.column_name, table_rec.table_name
        );
        
        EXECUTE sql_text INTO result_record;
        
        RETURN QUERY SELECT 
            'product_id_conversion'::text,
            table_rec.table_name,
            table_rec.column_name,
            result_record.total_rows,
            result_record.non_null_rows,
            result_record.convertible_rows,
            result_record.success_rate,
            result_record.unconvertible_samples,
            result_record.max_length,
            'Safe to convert (integer to varchar)'::text;
    END LOOP;
END;
$$ LANGUAGE plpgsql;

-- Run the assessment
CREATE OR REPLACE VIEW data_compatibility_report AS
SELECT * FROM assess_data_compatibility();

-- =============================================================================
-- PHASE 1.4: Create Assessment Summary Views
-- =============================================================================

-- Summary of current state
CREATE OR REPLACE VIEW implementation_status_summary AS
SELECT 
    'Current Foreign Keys' as metric,
    COUNT(*)::text as value,
    'Implemented relationships' as description
FROM current_foreign_keys

UNION ALL

SELECT 
    'Data Type Issues',
    COUNT(DISTINCT table_name || '.' || column_name)::text,
    'Columns needing type conversion'
FROM column_type_assessment
WHERE (column_group = 'customer_id_group' AND data_type != 'integer' AND table_name != 'customers')
   OR (column_group = 'product_id_group' AND data_type = 'integer' AND table_name != 'products')
   OR (column_group = 'order_id_group' AND data_type != 'integer' AND table_name != 'orders')

UNION ALL

SELECT 
    'Tables Assessed',
    COUNT(DISTINCT table_name)::text,
    'Tables with foreign key columns'
FROM column_type_assessment;

-- Mark assessment steps as completed
UPDATE fk_implementation_progress 
SET status = 'completed', completed_at = CURRENT_TIMESTAMP 
WHERE step IN ('1.2 Database Schema Assessment', '1.3 Data Quality Assessment');

-- =============================================================================
-- ASSESSMENT RESULTS DISPLAY
-- =============================================================================

-- Display results
\echo '=== PHASE 1 ASSESSMENT RESULTS ==='

\echo '1. Current Foreign Keys:'
SELECT * FROM current_foreign_keys;

\echo ''
\echo '2. Column Type Assessment:'
SELECT * FROM column_type_assessment ORDER BY column_group, table_name;

\echo ''
\echo '3. Data Compatibility Report:'
SELECT 
    assessment_type,
    table_name,
    column_name,
    total_rows,
    non_null_rows,
    conversion_success_rate,
    recommended_action
FROM data_compatibility_report
ORDER BY assessment_type, table_name;

\echo ''
\echo '4. Implementation Status Summary:'
SELECT * FROM implementation_status_summary;

\echo ''
\echo '5. Progress Tracking:'
SELECT phase, step, status, started_at, completed_at FROM fk_implementation_progress ORDER BY id;

\echo ''
\echo '=== PHASE 1 ASSESSMENT COMPLETED ==='
\echo 'Review the results above before proceeding to Phase 2.'
\echo 'Next step: Run phase2_data_standardization.sql'