-- C360 Fashion Retail Database: Foreign Key and Data Quality Fixes
-- This script addresses all identified foreign key gaps and data quality issues

-- Start transaction to ensure all changes are applied atomically
BEGIN;

-- =============================================================================
-- PHASE 1: DATA TYPE STANDARDIZATION
-- =============================================================================

-- Fix Customer ID data type inconsistencies
-- Convert varchar customer_id fields to integer to match customers table

ALTER TABLE customer_addresses 
ALTER COLUMN customer_id TYPE integer USING customer_id::integer;

ALTER TABLE website_sessions 
ALTER COLUMN customer_id TYPE integer USING customer_id::integer;

ALTER TABLE customer_service_interactions 
ALTER COLUMN customer_id TYPE integer USING customer_id::integer;

ALTER TABLE loyalty_profiles 
ALTER COLUMN customer_id TYPE integer USING customer_id::integer;

ALTER TABLE loyalty_activities 
ALTER COLUMN customer_id TYPE integer USING customer_id::integer;

ALTER TABLE customer_style_embeddings 
ALTER COLUMN customer_id TYPE integer USING customer_id::integer;

ALTER TABLE social_mentions 
ALTER COLUMN customer_id TYPE integer USING customer_id::integer;

ALTER TABLE email_engagement 
ALTER COLUMN customer_id TYPE integer USING customer_id::integer;

ALTER TABLE campaign_responses 
ALTER COLUMN customer_id TYPE integer USING customer_id::integer;

-- Fix Product ID data type inconsistencies  
-- Convert integer product_id fields to varchar to match products table

ALTER TABLE order_items 
ALTER COLUMN product_id TYPE varchar(20) USING product_id::varchar;

ALTER TABLE product_variants 
ALTER COLUMN product_id TYPE varchar(20) USING product_id::varchar;

ALTER TABLE reviews 
ALTER COLUMN product_id TYPE varchar(20) USING product_id::varchar;

-- Fix Order ID data type inconsistencies
-- Convert varchar order_id fields to integer to match orders table

ALTER TABLE returns 
ALTER COLUMN order_id TYPE integer USING order_id::integer;

ALTER TABLE customer_reviews 
ALTER COLUMN order_id TYPE integer USING order_id::integer;

ALTER TABLE customer_service_interactions 
ALTER COLUMN related_order_id TYPE integer USING related_order_id::integer;

ALTER TABLE loyalty_activities 
ALTER COLUMN related_order_id TYPE integer USING related_order_id::integer;

ALTER TABLE reviews 
ALTER COLUMN order_id TYPE integer USING order_id::integer;

ALTER TABLE campaign_responses 
ALTER COLUMN conversion_order_id TYPE integer USING conversion_order_id::integer;

-- Convert return_items.order_item_id to integer
ALTER TABLE return_items 
ALTER COLUMN order_item_id TYPE integer USING order_item_id::integer;

-- =============================================================================
-- PHASE 2: ADD PRIMARY KEYS TO STAGING TABLES
-- =============================================================================

-- Add primary key to staging_customer_sessions
ALTER TABLE staging_customer_sessions 
ADD COLUMN id SERIAL PRIMARY KEY;

-- Add primary key to staging_order_items_simple  
ALTER TABLE staging_order_items_simple 
ADD COLUMN id SERIAL PRIMARY KEY;

-- =============================================================================
-- PHASE 3: ADD MISSING FOREIGN KEY CONSTRAINTS
-- =============================================================================

-- Customer Addresses -> Customers
ALTER TABLE customer_addresses 
ADD CONSTRAINT fk_customer_addresses_customer_id 
FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
ON DELETE CASCADE ON UPDATE CASCADE;

-- Product Variants -> Products
ALTER TABLE product_variants 
ADD CONSTRAINT fk_product_variants_product_id 
FOREIGN KEY (product_id) REFERENCES products(product_id)
ON DELETE CASCADE ON UPDATE CASCADE;

-- Returns -> Orders
ALTER TABLE returns 
ADD CONSTRAINT fk_returns_order_id 
FOREIGN KEY (order_id) REFERENCES orders(order_id)
ON DELETE CASCADE ON UPDATE CASCADE;

-- Returns -> Customers
ALTER TABLE returns 
ADD CONSTRAINT fk_returns_customer_id 
FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
ON DELETE CASCADE ON UPDATE CASCADE;

-- Customer Service Interactions -> Customers
ALTER TABLE customer_service_interactions 
ADD CONSTRAINT fk_customer_service_interactions_customer_id 
FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
ON DELETE CASCADE ON UPDATE CASCADE;

-- Customer Service Interactions -> Orders (related_order_id)
ALTER TABLE customer_service_interactions 
ADD CONSTRAINT fk_customer_service_interactions_order_id 
FOREIGN KEY (related_order_id) REFERENCES orders(order_id)
ON DELETE SET NULL ON UPDATE CASCADE;

-- Loyalty Profiles -> Customers
ALTER TABLE loyalty_profiles 
ADD CONSTRAINT fk_loyalty_profiles_customer_id 
FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
ON DELETE CASCADE ON UPDATE CASCADE;

-- Loyalty Activities -> Customers
ALTER TABLE loyalty_activities 
ADD CONSTRAINT fk_loyalty_activities_customer_id 
FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
ON DELETE CASCADE ON UPDATE CASCADE;

-- Loyalty Activities -> Orders (related_order_id)
ALTER TABLE loyalty_activities 
ADD CONSTRAINT fk_loyalty_activities_order_id 
FOREIGN KEY (related_order_id) REFERENCES orders(order_id)
ON DELETE SET NULL ON UPDATE CASCADE;

-- Website Sessions -> Customers
ALTER TABLE website_sessions 
ADD CONSTRAINT fk_website_sessions_customer_id 
FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
ON DELETE CASCADE ON UPDATE CASCADE;

-- Customer Style Embeddings -> Customers
ALTER TABLE customer_style_embeddings 
ADD CONSTRAINT fk_customer_style_embeddings_customer_id 
FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
ON DELETE CASCADE ON UPDATE CASCADE;

-- Social Mentions -> Customers
ALTER TABLE social_mentions 
ADD CONSTRAINT fk_social_mentions_customer_id 
FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
ON DELETE SET NULL ON UPDATE CASCADE;

-- Email Engagement -> Customers
ALTER TABLE email_engagement 
ADD CONSTRAINT fk_email_engagement_customer_id 
FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
ON DELETE CASCADE ON UPDATE CASCADE;

-- Campaign Responses -> Customers
ALTER TABLE campaign_responses 
ADD CONSTRAINT fk_campaign_responses_customer_id 
FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
ON DELETE CASCADE ON UPDATE CASCADE;

-- Campaign Responses -> Orders (conversion_order_id)
ALTER TABLE campaign_responses 
ADD CONSTRAINT fk_campaign_responses_order_id 
FOREIGN KEY (conversion_order_id) REFERENCES orders(order_id)
ON DELETE SET NULL ON UPDATE CASCADE;

-- Return Items -> Order Items
ALTER TABLE return_items 
ADD CONSTRAINT fk_return_items_order_item_id 
FOREIGN KEY (order_item_id) REFERENCES order_items(order_item_id)
ON DELETE CASCADE ON UPDATE CASCADE;

-- Reviews -> Customers
ALTER TABLE reviews 
ADD CONSTRAINT fk_reviews_customer_id 
FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
ON DELETE CASCADE ON UPDATE CASCADE;

-- Reviews -> Products
ALTER TABLE reviews 
ADD CONSTRAINT fk_reviews_product_id 
FOREIGN KEY (product_id) REFERENCES products(product_id)
ON DELETE CASCADE ON UPDATE CASCADE;

-- Reviews -> Orders
ALTER TABLE reviews 
ADD CONSTRAINT fk_reviews_order_id 
FOREIGN KEY (order_id) REFERENCES orders(order_id)
ON DELETE CASCADE ON UPDATE CASCADE;

-- Customer Reviews -> Customers
ALTER TABLE customer_reviews 
ADD CONSTRAINT fk_customer_reviews_customer_id 
FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
ON DELETE CASCADE ON UPDATE CASCADE;

-- Customer Reviews -> Orders
ALTER TABLE customer_reviews 
ADD CONSTRAINT fk_customer_reviews_order_id 
FOREIGN KEY (order_id) REFERENCES orders(order_id)
ON DELETE CASCADE ON UPDATE CASCADE;

-- Style Similarity Matches -> Customers
ALTER TABLE style_similarity_matches 
ADD CONSTRAINT fk_style_similarity_matches_customer_id 
FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
ON DELETE CASCADE ON UPDATE CASCADE;

-- Order Items -> Products
ALTER TABLE order_items 
ADD CONSTRAINT fk_order_items_product_id 
FOREIGN KEY (product_id) REFERENCES products(product_id)
ON DELETE CASCADE ON UPDATE CASCADE;

-- =============================================================================
-- PHASE 4: ADD DATA QUALITY CHECK CONSTRAINTS
-- =============================================================================

-- Customer Reviews: Rating should be between 1 and 5
ALTER TABLE customer_reviews 
ADD CONSTRAINT chk_customer_reviews_rating 
CHECK (rating >= 1 AND rating <= 5);

-- Customer Reviews: Sentiment score should be between -1 and 1
ALTER TABLE customer_reviews 
ADD CONSTRAINT chk_customer_reviews_sentiment 
CHECK (sentiment_score >= -1.0 AND sentiment_score <= 1.0);

-- Reviews: Rating should be between 1 and 5
ALTER TABLE reviews 
ADD CONSTRAINT chk_reviews_rating 
CHECK (rating >= 1 AND rating <= 5);

-- Reviews: Quality/Style/Value ratings should be between 1 and 5
ALTER TABLE reviews 
ADD CONSTRAINT chk_reviews_quality_rating 
CHECK (quality_rating >= 1 AND quality_rating <= 5);

ALTER TABLE reviews 
ADD CONSTRAINT chk_reviews_style_rating 
CHECK (style_rating >= 1 AND style_rating <= 5);

ALTER TABLE reviews 
ADD CONSTRAINT chk_reviews_value_rating 
CHECK (value_rating >= 1 AND value_rating <= 5);

-- Reviews: Sentiment score should be between -1 and 1
ALTER TABLE reviews 
ADD CONSTRAINT chk_reviews_sentiment 
CHECK (sentiment_score >= -1.0 AND sentiment_score <= 1.0);

-- Orders: Amounts should be non-negative
ALTER TABLE orders 
ADD CONSTRAINT chk_orders_subtotal_positive 
CHECK (subtotal_amount >= 0);

ALTER TABLE orders 
ADD CONSTRAINT chk_orders_tax_positive 
CHECK (tax_amount >= 0);

ALTER TABLE orders 
ADD CONSTRAINT chk_orders_shipping_positive 
CHECK (shipping_amount >= 0);

ALTER TABLE orders 
ADD CONSTRAINT chk_orders_discount_positive 
CHECK (discount_amount >= 0);

ALTER TABLE orders 
ADD CONSTRAINT chk_orders_total_positive 
CHECK (total_amount >= 0);

-- Order Items: Quantities and prices should be positive
ALTER TABLE order_items 
ADD CONSTRAINT chk_order_items_quantity_positive 
CHECK (quantity > 0);

ALTER TABLE order_items 
ADD CONSTRAINT chk_order_items_unit_price_positive 
CHECK (unit_price >= 0);

ALTER TABLE order_items 
ADD CONSTRAINT chk_order_items_total_price_positive 
CHECK (total_price >= 0);

ALTER TABLE order_items 
ADD CONSTRAINT chk_order_items_final_price_positive 
CHECK (final_price >= 0);

-- Product Variants: Stock quantity should be non-negative
ALTER TABLE product_variants 
ADD CONSTRAINT chk_product_variants_stock_positive 
CHECK (stock_quantity >= 0);

-- Returns: Refund amount should be non-negative
ALTER TABLE returns 
ADD CONSTRAINT chk_returns_refund_positive 
CHECK (refund_amount >= 0);

ALTER TABLE returns 
ADD CONSTRAINT chk_returns_restocking_fee_positive 
CHECK (restocking_fee >= 0);

-- Customer Service: Satisfaction score should be between 1 and 10
ALTER TABLE customer_service_interactions 
ADD CONSTRAINT chk_customer_service_satisfaction 
CHECK (satisfaction_score >= 1 AND satisfaction_score <= 10);

-- Customer Service: Resolution time should be non-negative
ALTER TABLE customer_service_interactions 
ADD CONSTRAINT chk_customer_service_resolution_time 
CHECK (resolution_time_hours >= 0);

-- Loyalty Profiles: Points should be non-negative
ALTER TABLE loyalty_profiles 
ADD CONSTRAINT chk_loyalty_profiles_points_balance 
CHECK (points_balance >= 0);

ALTER TABLE loyalty_profiles 
ADD CONSTRAINT chk_loyalty_profiles_points_lifetime 
CHECK (points_lifetime >= 0);

-- Website Sessions: Duration should be non-negative
ALTER TABLE website_sessions 
ADD CONSTRAINT chk_website_sessions_duration 
CHECK (duration_minutes >= 0);

ALTER TABLE website_sessions 
ADD CONSTRAINT chk_website_sessions_page_views 
CHECK (page_views >= 0);

-- Social Mentions: Engagement and follower counts should be non-negative
ALTER TABLE social_mentions 
ADD CONSTRAINT chk_social_mentions_engagement 
CHECK (engagement_count >= 0);

ALTER TABLE social_mentions 
ADD CONSTRAINT chk_social_mentions_followers 
CHECK (follower_count >= 0);

-- Email Engagement: Open and click counts should be non-negative
ALTER TABLE email_engagement 
ADD CONSTRAINT chk_email_engagement_opens 
CHECK (total_opens >= 0);

ALTER TABLE email_engagement 
ADD CONSTRAINT chk_email_engagement_clicks 
CHECK (total_clicks >= 0);

-- =============================================================================
-- PHASE 5: ADD NOT NULL CONSTRAINTS WHERE APPROPRIATE
-- =============================================================================

-- Make critical foreign key columns NOT NULL where they should be required
ALTER TABLE customer_addresses 
ALTER COLUMN customer_id SET NOT NULL;

ALTER TABLE product_variants 
ALTER COLUMN product_id SET NOT NULL;

ALTER TABLE return_items 
ALTER COLUMN return_id SET NOT NULL;

ALTER TABLE loyalty_profiles 
ALTER COLUMN customer_id SET NOT NULL;

-- =============================================================================
-- PHASE 6: CREATE INDEXES FOR PERFORMANCE
-- =============================================================================

-- Create indexes on foreign key columns for better query performance
CREATE INDEX IF NOT EXISTS idx_customer_addresses_customer_id ON customer_addresses(customer_id);
CREATE INDEX IF NOT EXISTS idx_product_variants_product_id ON product_variants(product_id);
CREATE INDEX IF NOT EXISTS idx_returns_order_id ON returns(order_id);
CREATE INDEX IF NOT EXISTS idx_returns_customer_id ON returns(customer_id);
CREATE INDEX IF NOT EXISTS idx_customer_service_customer_id ON customer_service_interactions(customer_id);
CREATE INDEX IF NOT EXISTS idx_loyalty_profiles_customer_id ON loyalty_profiles(customer_id);
CREATE INDEX IF NOT EXISTS idx_loyalty_activities_customer_id ON loyalty_activities(customer_id);
CREATE INDEX IF NOT EXISTS idx_website_sessions_customer_id ON website_sessions(customer_id);
CREATE INDEX IF NOT EXISTS idx_reviews_customer_id ON reviews(customer_id);
CREATE INDEX IF NOT EXISTS idx_reviews_product_id ON reviews(product_id);
CREATE INDEX IF NOT EXISTS idx_reviews_order_id ON reviews(order_id);

-- Commit all changes
COMMIT;

-- =============================================================================
-- VERIFICATION QUERIES
-- =============================================================================

-- Count foreign key constraints
SELECT 
    'Total Foreign Key Constraints' as description,
    COUNT(*) as count
FROM information_schema.table_constraints 
WHERE constraint_type = 'FOREIGN KEY' 
  AND table_schema = 'public';

-- Count check constraints  
SELECT 
    'Total Check Constraints' as description,
    COUNT(*) as count
FROM information_schema.table_constraints 
WHERE constraint_type = 'CHECK' 
  AND table_schema = 'public';

-- List all foreign key constraints
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

PRINT 'Foreign key and data quality fixes completed successfully!';