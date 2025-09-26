# C360 Fashion Retail Database: Foreign Key and Data Quality Analysis

## Executive Summary

The C360 Fashion Retail database has **significant foreign key and data quality gaps** that limit its effectiveness for comprehensive customer 360-degree analytics. Our analysis reveals that only **38% of expected foreign key relationships are implemented**, with critical data type inconsistencies preventing many logical relationships from being properly constrained.

## Current Implementation Status

### ✅ Implemented Foreign Keys (9 total)
1. `campaign_responses.campaign_id` → `campaigns.campaign_id`
2. `categories.parent_category_id` → `categories.category_id` (self-referential)
3. `customer_reviews.product_id` → `products.product_id`
4. `email_engagement.campaign_id` → `campaigns.campaign_id`
5. `order_items.order_id` → `orders.order_id`
6. `orders.customer_id` → `customers.customer_id`
7. `product_embeddings.product_id` → `products.product_id`
8. `return_items.return_id` → `returns.return_id`
9. `style_similarity_matches.product_id` → `products.product_id`

### ❌ Missing Critical Foreign Keys (~15 major gaps)

#### Customer Relationship Gaps
- `customer_addresses.customer_id` → `customers.customer_id`
- `customer_service_interactions.customer_id` → `customers.customer_id`
- `loyalty_profiles.customer_id` → `customers.customer_id`
- `loyalty_activities.customer_id` → `customers.customer_id`
- `website_sessions.customer_id` → `customers.customer_id`
- `customer_style_embeddings.customer_id` → `customers.customer_id`
- `social_mentions.customer_id` → `customers.customer_id`

#### Product Relationship Gaps
- `product_variants.product_id` → `products.product_id`

#### Order/Transaction Relationship Gaps
- `returns.order_id` → `orders.order_id`
- `returns.customer_id` → `customers.customer_id`
- `return_items.order_item_id` → `order_items.order_item_id`

## Data Quality Issues

### Critical Data Type Inconsistencies

#### Customer ID Fields
| Table | Column | Data Type | Status |
|-------|--------|-----------|---------|
| `customers` | `customer_id` | `integer` | ✅ Reference |
| `orders` | `customer_id` | `integer` | ✅ Compatible |
| `customer_addresses` | `customer_id` | `varchar(20)` | ❌ Incompatible |
| `website_sessions` | `customer_id` | `varchar(20)` | ❌ Incompatible |
| `loyalty_profiles` | `customer_id` | `varchar(20)` | ❌ Incompatible |
| `returns` | `customer_id` | `varchar(20)` | ❌ Incompatible |

#### Product ID Fields
| Table | Column | Data Type | Status |
|-------|--------|-----------|---------|
| `products` | `product_id` | `varchar(20)` | ✅ Reference |
| `order_items` | `product_id` | `integer` | ❌ Incompatible |
| `product_variants` | `product_id` | `integer` | ❌ Incompatible |
| `reviews` | `product_id` | `integer` | ❌ Incompatible |

#### Order ID Fields
| Table | Column | Data Type | Status |
|-------|--------|-----------|---------|
| `orders` | `order_id` | `integer` | ✅ Reference |
| `order_items` | `order_id` | `integer` | ✅ Compatible |
| `returns` | `order_id` | `varchar(20)` | ❌ Incompatible |
| `customer_reviews` | `order_id` | `varchar(20)` | ❌ Incompatible |

### Missing Business Rule Constraints
- No check constraints for ratings (should be 1-5)
- No validation for positive monetary amounts
- No validation for sentiment scores (-1 to 1 range)
- Missing primary keys on staging tables

## Attempted Solution and Results

### Fix Script Created
We developed a comprehensive SQL script (`fix_foreign_keys_and_data_quality.sql`) that attempted to:

1. **Standardize Data Types**: Convert incompatible data types to match reference tables
2. **Add Missing Foreign Keys**: Implement all identified missing relationships
3. **Add Data Quality Constraints**: Implement business rule validation
4. **Optimize Performance**: Create indexes on foreign key columns

### Execution Results
❌ **FAILED** - The script failed during execution with the error:
```
ERROR: foreign key constraint "fk_returns_customer_id" cannot be implemented
DETAIL: Key columns "customer_id" and "customer_id" are of incompatible types: character varying and integer.
```

### Root Cause Analysis
The failure occurred because:
1. **Existing Data**: Tables already contain data that may not convert cleanly between data types
2. **Schema Mismatch**: The actual database schema differs from the configuration file analysis
3. **Data Dependencies**: Some data conversions require careful handling of NULL values and existing relationships

## Recommended Solution Approach

### Phase 1: Data Assessment and Backup
```sql
-- 1. Create full database backup
pg_dump -U postgres retail_fashion > retail_fashion_backup.sql

-- 2. Analyze existing data compatibility
SELECT COUNT(*) as total_rows, 
       COUNT(customer_id) as non_null_customer_ids,
       COUNT(CASE WHEN customer_id ~ '^\d+$' THEN 1 END) as numeric_customer_ids
FROM returns;
```

### Phase 2: Gradual Data Type Standardization
```sql
-- Example: Fix customer_id in returns table
-- Step 1: Add new column with correct type
ALTER TABLE returns ADD COLUMN customer_id_new INTEGER;

-- Step 2: Populate new column with converted values
UPDATE returns 
SET customer_id_new = customer_id::integer 
WHERE customer_id ~ '^\d+$';

-- Step 3: Drop old column and rename
ALTER TABLE returns DROP COLUMN customer_id;
ALTER TABLE returns RENAME COLUMN customer_id_new TO customer_id;
```

### Phase 3: Implement Foreign Keys Incrementally
```sql
-- Add foreign keys one by one, handling any data cleanup needed
ALTER TABLE customer_addresses 
ADD CONSTRAINT fk_customer_addresses_customer_id 
FOREIGN KEY (customer_id) REFERENCES customers(customer_id);
```

## Business Impact

### Current Limitations
- **Data Integrity Risks**: No referential integrity across 62% of logical relationships
- **Analytical Reliability**: Joins between tables may return inconsistent results
- **Data Quality**: No validation of business rules leading to potential bad data

### Benefits of Implementation
- **Complete Customer 360**: Full referential integrity enables comprehensive customer analytics
- **Data Quality Assurance**: Constraints prevent invalid data entry
- **Performance Optimization**: Proper indexing improves query performance
- **Compliance Readiness**: Enhanced data governance and auditability

## Next Steps

1. **Data Assessment**: Analyze existing data for conversion compatibility
2. **Staged Implementation**: Apply fixes incrementally with testing
3. **Data Migration**: Clean existing data to meet new constraints
4. **Validation**: Comprehensive testing of all relationships
5. **Monitoring**: Implement data quality monitoring post-migration

## Files Created
- `fix_foreign_keys_and_data_quality.sql` - Comprehensive fix script (needs refinement)
- `foreign_key_analysis_and_solution.md` - This analysis document

## Conclusion

While the C360 dataset provides a solid foundation with core transactional relationships properly implemented, **significant work is needed** to achieve complete referential integrity. The data type inconsistencies are the primary blocker, requiring careful data migration before foreign key implementation can succeed.

**Recommendation**: Implement the fixes in phases, starting with data type standardization and existing data cleanup, followed by incremental foreign key implementation with thorough testing at each stage.