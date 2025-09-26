-- C360 Fashion Retail: Targeted Foreign Key Implementation
-- This script focuses on implementing the foreign keys that can work with current schema

BEGIN;

-- =============================================================================
-- STEP 1: Add missing foreign keys that are compatible with current data types
-- =============================================================================

-- Customer Addresses -> Customers (if customer_id is already integer)
DO $$
BEGIN
    -- Check if we can add the foreign key
    IF EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'customer_addresses' 
          AND column_name = 'customer_id' 
          AND data_type = 'integer'
    ) THEN
        ALTER TABLE customer_addresses 
        ADD CONSTRAINT fk_customer_addresses_customer_id 
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        ON DELETE CASCADE ON UPDATE CASCADE;
        
        RAISE NOTICE 'Added foreign key: customer_addresses -> customers';
    ELSE
        RAISE NOTICE 'Skipped customer_addresses FK: data type mismatch';
    END IF;
EXCEPTION WHEN OTHERS THEN
    RAISE NOTICE 'Failed to add customer_addresses FK: %', SQLERRM;
END $$;

-- Product Variants -> Products (if product_id is already varchar)
DO $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM information_schema.columns c1
        JOIN information_schema.columns c2 ON c1.data_type = c2.data_type
        WHERE c1.table_name = 'product_variants' AND c1.column_name = 'product_id'
          AND c2.table_name = 'products' AND c2.column_name = 'product_id'
    ) THEN
        ALTER TABLE product_variants 
        ADD CONSTRAINT fk_product_variants_product_id 
        FOREIGN KEY (product_id) REFERENCES products(product_id)
        ON DELETE CASCADE ON UPDATE CASCADE;
        
        RAISE NOTICE 'Added foreign key: product_variants -> products';
    ELSE
        RAISE NOTICE 'Skipped product_variants FK: data type mismatch';
    END IF;
EXCEPTION WHEN OTHERS THEN
    RAISE NOTICE 'Failed to add product_variants FK: %', SQLERRM;
END $$;

-- Reviews -> Customers (if customer_id types match)
DO $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM information_schema.columns c1
        JOIN information_schema.columns c2 ON c1.data_type = c2.data_type
        WHERE c1.table_name = 'reviews' AND c1.column_name = 'customer_id'
          AND c2.table_name = 'customers' AND c2.column_name = 'customer_id'
    ) THEN
        ALTER TABLE reviews 
        ADD CONSTRAINT fk_reviews_customer_id 
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        ON DELETE CASCADE ON UPDATE CASCADE;
        
        RAISE NOTICE 'Added foreign key: reviews -> customers';
    ELSE
        RAISE NOTICE 'Skipped reviews customer FK: data type mismatch';
    END IF;
EXCEPTION WHEN OTHERS THEN
    RAISE NOTICE 'Failed to add reviews customer FK: %', SQLERRM;
END $$;

-- Reviews -> Products (if product_id types match)
DO $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM information_schema.columns c1
        JOIN information_schema.columns c2 ON c1.data_type = c2.data_type
        WHERE c1.table_name = 'reviews' AND c1.column_name = 'product_id'
          AND c2.table_name = 'products' AND c2.column_name = 'product_id'
    ) THEN
        ALTER TABLE reviews 
        ADD CONSTRAINT fk_reviews_product_id 
        FOREIGN KEY (product_id) REFERENCES products(product_id)
        ON DELETE CASCADE ON UPDATE CASCADE;
        
        RAISE NOTICE 'Added foreign key: reviews -> products';
    ELSE
        RAISE NOTICE 'Skipped reviews product FK: data type mismatch';
    END IF;
EXCEPTION WHEN OTHERS THEN
    RAISE NOTICE 'Failed to add reviews product FK: %', SQLERRM;
END $$;

-- Reviews -> Orders (if order_id types match)
DO $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM information_schema.columns c1
        JOIN information_schema.columns c2 ON c1.data_type = c2.data_type
        WHERE c1.table_name = 'reviews' AND c1.column_name = 'order_id'
          AND c2.table_name = 'orders' AND c2.column_name = 'order_id'
    ) THEN
        ALTER TABLE reviews 
        ADD CONSTRAINT fk_reviews_order_id 
        FOREIGN KEY (order_id) REFERENCES orders(order_id)
        ON DELETE CASCADE ON UPDATE CASCADE;
        
        RAISE NOTICE 'Added foreign key: reviews -> orders';
    ELSE
        RAISE NOTICE 'Skipped reviews order FK: data type mismatch';
    END IF;
EXCEPTION WHEN OTHERS THEN
    RAISE NOTICE 'Failed to add reviews order FK: %', SQLERRM;
END $$;

-- =============================================================================
-- STEP 2: Add essential data quality constraints that will work
-- =============================================================================

-- Rating constraints for reviews
DO $$
BEGIN
    ALTER TABLE reviews ADD CONSTRAINT chk_reviews_rating CHECK (rating >= 1 AND rating <= 5);
    RAISE NOTICE 'Added rating constraint to reviews table';
EXCEPTION WHEN OTHERS THEN
    RAISE NOTICE 'Rating constraint already exists or failed: %', SQLERRM;
END $$;

-- Rating constraints for customer_reviews
DO $$
BEGIN
    ALTER TABLE customer_reviews ADD CONSTRAINT chk_customer_reviews_rating CHECK (rating >= 1 AND rating <= 5);
    RAISE NOTICE 'Added rating constraint to customer_reviews table';
EXCEPTION WHEN OTHERS THEN
    RAISE NOTICE 'Rating constraint already exists or failed: %', SQLERRM;
END $$;

-- Positive amounts for orders
DO $$
BEGIN
    ALTER TABLE orders ADD CONSTRAINT chk_orders_total_positive CHECK (total_amount >= 0);
    RAISE NOTICE 'Added positive amount constraint to orders';
EXCEPTION WHEN OTHERS THEN
    RAISE NOTICE 'Orders constraint already exists or failed: %', SQLERRM;
END $$;

-- Positive quantity for order_items
DO $$
BEGIN
    ALTER TABLE order_items ADD CONSTRAINT chk_order_items_quantity_positive CHECK (quantity > 0);
    RAISE NOTICE 'Added positive quantity constraint to order_items';
EXCEPTION WHEN OTHERS THEN
    RAISE NOTICE 'Order items constraint already exists or failed: %', SQLERRM;
END $$;

-- =============================================================================
-- STEP 3: Create summary report
-- =============================================================================

-- Count current foreign keys
SELECT 
    'Foreign Keys After Implementation' as metric,
    COUNT(*) as count
FROM information_schema.table_constraints 
WHERE constraint_type = 'FOREIGN KEY' 
  AND table_schema = 'public'

UNION ALL

SELECT 
    'Check Constraints After Implementation',
    COUNT(*)
FROM information_schema.table_constraints 
WHERE constraint_type = 'CHECK' 
  AND table_schema = 'public';

-- List all foreign keys
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

COMMIT;

\echo 'Targeted foreign key implementation completed!'
\echo 'Check the results above to see what was successfully implemented.'