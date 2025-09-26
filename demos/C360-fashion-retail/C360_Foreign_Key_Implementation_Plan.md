# C360 Fashion Retail Database: Foreign Key Implementation Plan

## Executive Summary

Based on our analysis and testing results, this document provides a **safe, phased implementation plan** to fix foreign key relationships and data quality issues in the C360 database. The plan addresses the root cause of data type incompatibilities discovered during testing.

## Implementation Strategy: **"Blue-Green Column Migration"**

Instead of modifying existing columns directly, we'll:
1. **Add new columns** with correct data types
2. **Migrate data** with validation and cleanup
3. **Update applications** to use new columns
4. **Drop old columns** and rename new ones
5. **Add foreign keys** incrementally with testing

## Phase 1: Pre-Implementation Assessment (Duration: 2-3 days)

### 1.1 Database Backup and Environment Setup
```bash
# Create full backup
docker exec axiomretailfashion_postgres pg_dump -U postgres retail_fashion > retail_fashion_backup_$(date +%Y%m%d).sql

# Create test environment copy
docker exec axiomretailfashion_postgres createdb -U postgres retail_fashion_test
docker exec axiomretailfashion_postgres psql -U postgres -d retail_fashion_test < retail_fashion_backup_$(date +%Y%m%d).sql
```

### 1.2 Data Quality Assessment
```sql
-- Assess customer_id data quality across tables
CREATE OR REPLACE FUNCTION assess_customer_id_compatibility()
RETURNS TABLE(
    table_name text,
    total_rows bigint,
    non_null_rows bigint,
    numeric_compatible bigint,
    max_length int,
    sample_values text[]
) AS $$
BEGIN
    -- Returns assessment for each table with customer_id
    RETURN QUERY
    SELECT 
        'returns'::text,
        COUNT(*),
        COUNT(customer_id),
        COUNT(CASE WHEN customer_id ~ '^\d+$' THEN 1 END),
        MAX(LENGTH(customer_id))::int,
        ARRAY(SELECT DISTINCT customer_id FROM returns WHERE customer_id IS NOT NULL LIMIT 5)
    FROM returns
    
    UNION ALL
    
    SELECT 
        'customer_addresses'::text,
        COUNT(*),
        COUNT(customer_id),
        COUNT(CASE WHEN customer_id ~ '^\d+$' THEN 1 END),
        MAX(LENGTH(customer_id))::int,
        ARRAY(SELECT DISTINCT customer_id FROM customer_addresses WHERE customer_id IS NOT NULL LIMIT 5)
    FROM customer_addresses;
    -- Add similar blocks for other tables
END;
$$ LANGUAGE plpgsql;

SELECT * FROM assess_customer_id_compatibility();
```

### 1.3 Create Implementation Tracking
```sql
-- Create progress tracking table
CREATE TABLE IF NOT EXISTS fk_implementation_progress (
    id SERIAL PRIMARY KEY,
    phase VARCHAR(50),
    step VARCHAR(100),
    table_name VARCHAR(100),
    status VARCHAR(20) DEFAULT 'pending', -- pending, in_progress, completed, failed
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    error_message TEXT,
    rollback_sql TEXT
);
```

## Phase 2: Data Type Standardization (Duration: 3-5 days)

### 2.1 Customer ID Standardization
```sql
-- Step 1: Add new integer customer_id columns
ALTER TABLE customer_addresses ADD COLUMN customer_id_new INTEGER;
ALTER TABLE returns ADD COLUMN customer_id_new INTEGER;
ALTER TABLE loyalty_profiles ADD COLUMN customer_id_new INTEGER;
ALTER TABLE loyalty_activities ADD COLUMN customer_id_new INTEGER;
ALTER TABLE website_sessions ADD COLUMN customer_id_new INTEGER;
ALTER TABLE customer_service_interactions ADD COLUMN customer_id_new INTEGER;

-- Step 2: Create data migration function
CREATE OR REPLACE FUNCTION migrate_customer_ids()
RETURNS void AS $$
DECLARE
    table_record RECORD;
    sql_text TEXT;
BEGIN
    FOR table_record IN 
        SELECT table_name 
        FROM information_schema.columns 
        WHERE column_name = 'customer_id_new' 
        AND table_schema = 'public'
    LOOP
        sql_text := format('
            UPDATE %I 
            SET customer_id_new = CASE 
                WHEN customer_id ~ ''^\\d+$'' THEN customer_id::integer
                ELSE NULL 
            END
            WHERE customer_id IS NOT NULL',
            table_record.table_name
        );
        
        EXECUTE sql_text;
        
        RAISE NOTICE 'Migrated customer_id for table: %', table_record.table_name;
    END LOOP;
END;
$$ LANGUAGE plpgsql;

-- Step 3: Execute migration
SELECT migrate_customer_ids();

-- Step 4: Validate migration
SELECT 
    'customer_addresses' as table_name,
    COUNT(*) as total_rows,
    COUNT(customer_id) as old_non_null,
    COUNT(customer_id_new) as new_non_null,
    COUNT(*) - COUNT(customer_id_new) as conversion_failures
FROM customer_addresses
UNION ALL
SELECT 
    'returns',
    COUNT(*),
    COUNT(customer_id),
    COUNT(customer_id_new),
    COUNT(*) - COUNT(customer_id_new)
FROM returns;
-- Add for other tables
```

### 2.2 Product ID Standardization  
```sql
-- Convert integer product_ids to varchar to match products table
ALTER TABLE order_items ADD COLUMN product_id_new VARCHAR(20);
ALTER TABLE product_variants ADD COLUMN product_id_new VARCHAR(20);
ALTER TABLE reviews ADD COLUMN product_id_new VARCHAR(20);

-- Migrate data
UPDATE order_items SET product_id_new = product_id::varchar WHERE product_id IS NOT NULL;
UPDATE product_variants SET product_id_new = product_id::varchar WHERE product_id IS NOT NULL;
UPDATE reviews SET product_id_new = product_id::varchar WHERE product_id IS NOT NULL;
```

### 2.3 Order ID Standardization
```sql
-- Convert varchar order_ids to integer to match orders table
ALTER TABLE returns ADD COLUMN order_id_new INTEGER;
ALTER TABLE customer_reviews ADD COLUMN order_id_new INTEGER;

-- Migrate data with validation
UPDATE returns 
SET order_id_new = order_id::integer 
WHERE order_id ~ '^\d+$';

UPDATE customer_reviews 
SET order_id_new = order_id::integer 
WHERE order_id ~ '^\d+$';
```

## Phase 3: Data Validation and Cleanup (Duration: 2-3 days)

### 3.1 Referential Integrity Validation
```sql
-- Check for orphaned records before adding foreign keys
CREATE OR REPLACE FUNCTION check_referential_integrity()
RETURNS TABLE(
    check_name text,
    orphaned_records bigint,
    total_records bigint,
    integrity_percentage numeric
) AS $$
BEGIN
    RETURN QUERY
    -- Customer references
    SELECT 
        'customer_addresses -> customers'::text,
        COUNT(CASE WHEN c.customer_id IS NULL THEN 1 END),
        COUNT(*),
        ROUND(COUNT(CASE WHEN c.customer_id IS NOT NULL THEN 1 END) * 100.0 / COUNT(*), 2)
    FROM customer_addresses ca
    LEFT JOIN customers c ON ca.customer_id_new = c.customer_id
    WHERE ca.customer_id_new IS NOT NULL
    
    UNION ALL
    
    -- Product references  
    SELECT 
        'product_variants -> products'::text,
        COUNT(CASE WHEN p.product_id IS NULL THEN 1 END),
        COUNT(*),
        ROUND(COUNT(CASE WHEN p.product_id IS NOT NULL THEN 1 END) * 100.0 / COUNT(*), 2)
    FROM product_variants pv
    LEFT JOIN products p ON pv.product_id_new = p.product_id
    WHERE pv.product_id_new IS NOT NULL;
    
    -- Add more integrity checks
END;
$$ LANGUAGE plpgsql;

SELECT * FROM check_referential_integrity();
```

### 3.2 Data Cleanup
```sql
-- Clean up orphaned records or create missing parent records
-- Example: Create missing customers for orphaned addresses
INSERT INTO customers (customer_id, email, first_name, last_name, registration_date, account_status)
SELECT DISTINCT 
    ca.customer_id_new,
    'unknown_' || ca.customer_id_new || '@placeholder.com',
    'Unknown',
    'Customer',
    CURRENT_TIMESTAMP,
    'inactive'
FROM customer_addresses ca
LEFT JOIN customers c ON ca.customer_id_new = c.customer_id
WHERE ca.customer_id_new IS NOT NULL 
  AND c.customer_id IS NULL;
```

## Phase 4: Column Replacement (Duration: 1-2 days)

### 4.1 Safe Column Replacement
```sql
-- For each table, replace old columns with new ones
BEGIN;

-- Customer ID replacements
ALTER TABLE customer_addresses DROP COLUMN customer_id;
ALTER TABLE customer_addresses RENAME COLUMN customer_id_new TO customer_id;
ALTER TABLE customer_addresses ALTER COLUMN customer_id SET NOT NULL;

-- Product ID replacements
ALTER TABLE product_variants DROP COLUMN product_id;
ALTER TABLE product_variants RENAME COLUMN product_id_new TO product_id;
ALTER TABLE product_variants ALTER COLUMN product_id SET NOT NULL;

-- Continue for other tables...

COMMIT;
```

## Phase 5: Foreign Key Implementation (Duration: 2-3 days)

### 5.1 Add Foreign Keys Incrementally
```sql
-- Add foreign keys one by one with proper error handling
CREATE OR REPLACE FUNCTION add_foreign_key_safe(
    table_name text,
    constraint_name text,
    column_name text,
    ref_table text,
    ref_column text
) RETURNS boolean AS $$
BEGIN
    BEGIN
        EXECUTE format(
            'ALTER TABLE %I ADD CONSTRAINT %I FOREIGN KEY (%I) REFERENCES %I(%I) ON DELETE CASCADE ON UPDATE CASCADE',
            table_name, constraint_name, column_name, ref_table, ref_column
        );
        
        INSERT INTO fk_implementation_progress (phase, step, table_name, status, completed_at)
        VALUES ('Phase5', 'Add FK: ' || constraint_name, table_name, 'completed', NOW());
        
        RETURN true;
    EXCEPTION WHEN OTHERS THEN
        INSERT INTO fk_implementation_progress (phase, step, table_name, status, error_message, completed_at)
        VALUES ('Phase5', 'Add FK: ' || constraint_name, table_name, 'failed', SQLERRM, NOW());
        
        RETURN false;
    END;
END;
$$ LANGUAGE plpgsql;

-- Execute foreign key additions
SELECT add_foreign_key_safe('customer_addresses', 'fk_customer_addresses_customer_id', 'customer_id', 'customers', 'customer_id');
SELECT add_foreign_key_safe('product_variants', 'fk_product_variants_product_id', 'product_id', 'products', 'product_id');
SELECT add_foreign_key_safe('returns', 'fk_returns_customer_id', 'customer_id', 'customers', 'customer_id');
SELECT add_foreign_key_safe('returns', 'fk_returns_order_id', 'order_id', 'orders', 'order_id');
-- Continue with all foreign keys...
```

## Phase 6: Data Quality Constraints (Duration: 1 day)

### 6.1 Add Business Rule Constraints
```sql
-- Add check constraints for business rules
ALTER TABLE customer_reviews ADD CONSTRAINT chk_rating_range CHECK (rating BETWEEN 1 AND 5);
ALTER TABLE orders ADD CONSTRAINT chk_positive_amounts CHECK (total_amount >= 0 AND subtotal_amount >= 0);
ALTER TABLE order_items ADD CONSTRAINT chk_positive_quantity CHECK (quantity > 0);
-- Add more constraints...
```

## Phase 7: Performance Optimization (Duration: 1 day)

### 7.1 Create Indexes
```sql
-- Create indexes on foreign key columns
CREATE INDEX CONCURRENTLY idx_customer_addresses_customer_id ON customer_addresses(customer_id);
CREATE INDEX CONCURRENTLY idx_product_variants_product_id ON product_variants(product_id);
CREATE INDEX CONCURRENTLY idx_returns_customer_id ON returns(customer_id);
CREATE INDEX CONCURRENTLY idx_returns_order_id ON returns(order_id);
```

## Phase 8: Validation and Testing (Duration: 2-3 days)

### 8.1 Comprehensive Testing
```sql
-- Test all foreign key relationships
CREATE OR REPLACE FUNCTION test_foreign_keys()
RETURNS TABLE(
    constraint_name text,
    table_name text,
    status text,
    test_result text
) AS $$
DECLARE
    fk_record RECORD;
    test_sql TEXT;
    violation_count INTEGER;
BEGIN
    FOR fk_record IN
        SELECT tc.constraint_name, tc.table_name, kcu.column_name, ccu.table_name as ref_table, ccu.column_name as ref_column
        FROM information_schema.table_constraints tc
        JOIN information_schema.key_column_usage kcu ON tc.constraint_name = kcu.constraint_name
        JOIN information_schema.constraint_column_usage ccu ON tc.constraint_name = ccu.constraint_name
        WHERE tc.constraint_type = 'FOREIGN KEY' AND tc.table_schema = 'public'
    LOOP
        -- Test for violations
        test_sql := format(
            'SELECT COUNT(*) FROM %I t LEFT JOIN %I r ON t.%I = r.%I WHERE t.%I IS NOT NULL AND r.%I IS NULL',
            fk_record.table_name, fk_record.ref_table, fk_record.column_name, fk_record.ref_column,
            fk_record.column_name, fk_record.ref_column
        );
        
        EXECUTE test_sql INTO violation_count;
        
        RETURN QUERY SELECT 
            fk_record.constraint_name,
            fk_record.table_name,
            CASE WHEN violation_count = 0 THEN 'PASS' ELSE 'FAIL' END,
            violation_count || ' violations found';
    END LOOP;
END;
$$ LANGUAGE plpgsql;

SELECT * FROM test_foreign_keys();
```

## Implementation Timeline

| Phase | Duration | Risk Level | Dependencies |
|-------|----------|------------|--------------|
| Phase 1: Assessment | 2-3 days | Low | Database access |
| Phase 2: Data Type Standardization | 3-5 days | Medium | Phase 1 complete |
| Phase 3: Data Validation | 2-3 days | Medium | Phase 2 complete |
| Phase 4: Column Replacement | 1-2 days | High | Phase 3 complete |
| Phase 5: Foreign Key Implementation | 2-3 days | Medium | Phase 4 complete |
| Phase 6: Data Quality Constraints | 1 day | Low | Phase 5 complete |
| Phase 7: Performance Optimization | 1 day | Low | Phase 6 complete |
| Phase 8: Validation and Testing | 2-3 days | Low | All phases complete |

**Total Estimated Duration: 12-20 days**

## Risk Mitigation

### High-Risk Operations
1. **Column Replacement (Phase 4)**: Use transactions and have rollback procedures ready
2. **Data Type Conversions**: Validate all data before conversion
3. **Application Dependencies**: Coordinate with application teams

### Rollback Procedures
```sql
-- Example rollback for Phase 4
BEGIN;
ALTER TABLE customer_addresses RENAME COLUMN customer_id TO customer_id_backup;
ALTER TABLE customer_addresses RENAME COLUMN customer_id_old TO customer_id;
ROLLBACK; -- Only if issues found
```

### Success Criteria
- [ ] All expected foreign key relationships implemented
- [ ] Zero referential integrity violations
- [ ] No data loss during migration
- [ ] Performance maintained or improved
- [ ] All applications function correctly

## Monitoring and Alerts

```sql
-- Create monitoring views
CREATE VIEW fk_health_dashboard AS
SELECT 
    COUNT(*) as total_foreign_keys,
    COUNT(CASE WHEN tc.constraint_name LIKE 'fk_%' THEN 1 END) as implemented_fks,
    ROUND(COUNT(CASE WHEN tc.constraint_name LIKE 'fk_%' THEN 1 END) * 100.0 / COUNT(*), 2) as completion_percentage
FROM information_schema.table_constraints tc
WHERE tc.constraint_type = 'FOREIGN KEY' AND tc.table_schema = 'public';
```

## Post-Implementation

### Documentation Updates
- [ ] Update data dictionary
- [ ] Update application documentation
- [ ] Create maintenance procedures

### Ongoing Monitoring
- [ ] Set up data quality monitoring
- [ ] Create alerts for constraint violations
- [ ] Schedule regular integrity checks

---

**Next Steps**: 
1. Review and approve this implementation plan
2. Set up dedicated test environment
3. Begin Phase 1: Pre-Implementation Assessment
4. Schedule regular checkpoints for progress review