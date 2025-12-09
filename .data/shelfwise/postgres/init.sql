-- ShelfWise Retail Analytics Database
-- PostgreSQL initialization script

-- Create database if not exists
-- CREATE DATABASE shelfwise;
-- \c shelfwise;

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Drop existing tables if they exist (in reverse dependency order)
DROP TABLE IF EXISTS transactions CASCADE;
DROP TABLE IF EXISTS waste_spoilage CASCADE;
DROP TABLE IF EXISTS supplier_shipments CASCADE;
DROP TABLE IF EXISTS price_changes CASCADE;
DROP TABLE IF EXISTS tickets CASCADE;
DROP TABLE IF EXISTS returns_daily CASCADE;
DROP TABLE IF EXISTS sales_daily CASCADE;
DROP TABLE IF EXISTS inventory_daily CASCADE;
DROP TABLE IF EXISTS assortment CASCADE;
DROP TABLE IF EXISTS promotions CASCADE;
DROP TABLE IF EXISTS stores CASCADE;
DROP TABLE IF EXISTS products CASCADE;

-- Drop reference tables
DROP TABLE IF EXISTS waste_reasons CASCADE;
DROP TABLE IF EXISTS return_reasons CASCADE;
DROP TABLE IF EXISTS promotion_types CASCADE;
DROP TABLE IF EXISTS payment_methods CASCADE;
DROP TABLE IF EXISTS suppliers CASCADE;
DROP TABLE IF EXISTS brands CASCADE;
DROP TABLE IF EXISTS store_types CASCADE;
DROP TABLE IF EXISTS categories CASCADE;
DROP TABLE IF EXISTS regions CASCADE;

-- ============================================================================
-- REFERENCE TABLES (Small lookup tables)
-- ============================================================================

-- Regions table
CREATE TABLE regions (
    region_id SERIAL PRIMARY KEY,
    region_code VARCHAR(20) UNIQUE NOT NULL,
    region_name VARCHAR(100) NOT NULL,
    country VARCHAR(50) NOT NULL,
    timezone VARCHAR(50),
    description TEXT
);

INSERT INTO regions (region_code, region_name, country, timezone, description) VALUES
('west_coast', 'West Coast', 'USA', 'America/Los_Angeles', 'Bay Area core market - company founded here'),
('southwest', 'Southwest', 'USA', 'America/Phoenix', 'Arizona, Nevada, Colorado expansion'),
('expansion', 'National Expansion', 'USA', 'America/Chicago', 'Strategic national markets - Austin, Chicago, NYC, Boston, Atlanta, Miami'),
('international', 'International', 'Multiple', 'UTC', 'Canada and UK test markets'),
('nationwide', 'Nationwide Online', 'USA', 'America/Los_Angeles', 'Online fulfillment center');

-- Categories table
CREATE TABLE categories (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(50) UNIQUE NOT NULL,
    category_group VARCHAR(50),
    margin_target_pct DECIMAL(5,2),
    is_perishable BOOLEAN,
    elasticity DECIMAL(4,2)
);

INSERT INTO categories (category_name, category_group, margin_target_pct, is_perishable, elasticity) VALUES
('cereal', 'dry_goods', 35.00, false, -0.6),
('dairy', 'refrigerated', 25.00, true, -0.8),
('snacks', 'dry_goods', 42.00, false, -1.0),
('beverages', 'dry_goods', 40.00, false, -1.2),
('produce', 'fresh', 22.00, true, -0.9),
('household', 'non_food', 52.00, false, -0.4),
('frozen', 'frozen', 32.00, false, -0.7),
('bakery', 'fresh', 30.00, true, -0.8),
('meat', 'fresh', 20.00, true, -0.9),
('canned', 'dry_goods', 35.00, false, -0.5),
('personal_care', 'non_food', 55.00, false, -0.6),
('candy', 'dry_goods', 45.00, false, -1.1);

-- Store types table
CREATE TABLE store_types (
    store_type_id SERIAL PRIMARY KEY,
    store_type_code VARCHAR(20) UNIQUE NOT NULL,
    store_type_name VARCHAR(50) NOT NULL,
    typical_sq_ft_min INTEGER,
    typical_sq_ft_max INTEGER,
    typical_sku_count INTEGER,
    operating_hours INTEGER
);

INSERT INTO store_types (store_type_code, store_type_name, typical_sq_ft_min, typical_sq_ft_max, typical_sku_count, operating_hours) VALUES
('online', 'Online Fulfillment Center', 400000, 600000, 400, 24),
('big_box', 'Big Box Store', 60000, 100000, 360, 14),
('suburban', 'Suburban Store', 25000, 45000, 280, 12),
('urban', 'Urban Store', 10000, 20000, 280, 14),
('convenience', 'Convenience Store', 3000, 8000, 280, 16);

-- Brands table
CREATE TABLE brands (
    brand_id SERIAL PRIMARY KEY,
    brand_name VARCHAR(100) UNIQUE NOT NULL,
    brand_tier VARCHAR(20) NOT NULL,
    manufacturer VARCHAR(100),
    is_private_label BOOLEAN
);

INSERT INTO brands (brand_name, brand_tier, manufacturer, is_private_label) VALUES
-- ShelfWise Private Label
('ShelfWise Select', 'premium', 'ShelfWise', true),
('ShelfWise Basics', 'value', 'ShelfWise', true),
('ShelfWise Organic', 'premium', 'ShelfWise', true),
('ShelfWise Fresh', 'mid', 'ShelfWise', true),
-- Major CPG Manufacturers
('Kelloggs', 'premium', 'Kellogg Company', false),
('General Mills', 'premium', 'General Mills Inc', false),
('Nestle', 'mid', 'Nestle SA', false),
('Kraft Heinz', 'mid', 'Kraft Heinz Company', false),
('PepsiCo', 'mid', 'PepsiCo Inc', false),
('Coca-Cola', 'mid', 'The Coca-Cola Company', false),
('Unilever', 'premium', 'Unilever PLC', false),
('Procter & Gamble', 'premium', 'Procter & Gamble Co', false),
('Campbell Soup', 'mid', 'Campbell Soup Company', false),
('ConAgra', 'mid', 'Conagra Brands Inc', false),
('Mondelez', 'mid', 'Mondelez International', false),
('Mars', 'premium', 'Mars Inc', false),
('Hershey', 'mid', 'The Hershey Company', false),
('Frito-Lay', 'mid', 'PepsiCo Inc', false),
('Quaker', 'mid', 'PepsiCo Inc', false),
('Dole', 'mid', 'Dole Food Company', false),
('Del Monte', 'mid', 'Del Monte Foods', false),
('Tyson Foods', 'mid', 'Tyson Foods Inc', false),
('Hormel', 'mid', 'Hormel Foods Corp', false),
('Smithfield', 'value', 'Smithfield Foods', false),
('Perdue', 'mid', 'Perdue Farms', false),
('Danone', 'premium', 'Danone SA', false),
('Chobani', 'premium', 'Chobani LLC', false),
('Blue Diamond', 'premium', 'Blue Diamond Growers', false),
('Wonderful', 'premium', 'The Wonderful Company', false),
('Annies Homegrown', 'premium', 'General Mills Inc', false),
('Organic Valley', 'premium', 'Organic Valley', false),
('Horizon Organic', 'premium', 'Danone SA', false),
('Bobs Red Mill', 'premium', 'Bob''s Red Mill', false),
('Kind', 'premium', 'Mars Inc', false),
('Clif Bar', 'premium', 'Mondelez International', false),
('Nature Valley', 'mid', 'General Mills Inc', false),
('Nabisco', 'mid', 'Mondelez International', false),
('Ritz', 'mid', 'Mondelez International', false),
('Pepperidge Farm', 'premium', 'Campbell Soup Company', false),
('Barilla', 'mid', 'Barilla Group', false),
('Hunts', 'value', 'Conagra Brands Inc', false),
('Progresso', 'mid', 'General Mills Inc', false),
('Swanson', 'value', 'Campbell Soup Company', false),
('Green Giant', 'mid', 'B&G Foods', false),
('Birds Eye', 'mid', 'Conagra Brands Inc', false),
('Lean Cuisine', 'mid', 'Nestle SA', false),
('Stouffers', 'mid', 'Nestle SA', false),
('DiGiorno', 'premium', 'Nestle SA', false),
('Haagen-Dazs', 'premium', 'General Mills Inc', false),
('Ben & Jerrys', 'premium', 'Unilever PLC', false),
('Breyers', 'mid', 'Unilever PLC', false),
('Dreyers', 'mid', 'Nestle SA', false),
('PolarSprings', 'mid', 'Nestle SA', false),
('Dasani', 'mid', 'The Coca-Cola Company', false),
('Smartwater', 'premium', 'The Coca-Cola Company', false),
('Fiji', 'premium', 'The Wonderful Company', false),
('Poland Spring', 'value', 'Nestle SA', false),
('Gatorade', 'mid', 'PepsiCo Inc', false),
('Powerade', 'mid', 'The Coca-Cola Company', false),
('Tropicana', 'premium', 'PepsiCo Inc', false),
('Simply', 'premium', 'The Coca-Cola Company', false),
('Minute Maid', 'mid', 'The Coca-Cola Company', false),
('Ocean Spray', 'mid', 'Ocean Spray Cranberries', false);

-- Suppliers table
CREATE TABLE suppliers (
    supplier_id SERIAL PRIMARY KEY,
    supplier_name VARCHAR(100) UNIQUE NOT NULL,
    supplier_type VARCHAR(50),
    lead_time_days INTEGER,
    reliability_score DECIMAL(3,2),
    payment_terms VARCHAR(50)
);

INSERT INTO suppliers (supplier_name, supplier_type, lead_time_days, reliability_score, payment_terms) VALUES
('Kellogg Company Supplier', 'manufacturer', 5, 0.95, 'Net 30'),
('General Mills Inc Supplier', 'manufacturer', 5, 0.96, 'Net 30'),
('Nestle SA Supplier', 'manufacturer', 7, 0.94, 'Net 45'),
('Kraft Heinz Company Supplier', 'manufacturer', 6, 0.93, 'Net 30'),
('PepsiCo Inc Supplier', 'manufacturer', 4, 0.97, 'Net 30'),
('The Coca-Cola Company Supplier', 'manufacturer', 4, 0.98, 'Net 30'),
('Unilever PLC Supplier', 'manufacturer', 8, 0.92, 'Net 45'),
('Procter & Gamble Co Supplier', 'manufacturer', 7, 0.94, 'Net 45'),
('Campbell Soup Company Supplier', 'manufacturer', 6, 0.91, 'Net 30'),
('Conagra Brands Inc Supplier', 'manufacturer', 6, 0.90, 'Net 30'),
('Mondelez International Supplier', 'manufacturer', 7, 0.93, 'Net 45'),
('Mars Inc Supplier', 'manufacturer', 8, 0.91, 'Net 45'),
('The Hershey Company Supplier', 'manufacturer', 5, 0.95, 'Net 30'),
('Tyson Foods Inc Supplier', 'manufacturer', 3, 0.89, 'Net 15'),
('Hormel Foods Corp Supplier', 'manufacturer', 4, 0.90, 'Net 15'),
('Smithfield Foods Supplier', 'manufacturer', 3, 0.88, 'Net 15'),
('Perdue Farms Supplier', 'manufacturer', 3, 0.89, 'Net 15'),
('Danone SA Supplier', 'manufacturer', 4, 0.92, 'Net 21'),
('Chobani LLC Supplier', 'manufacturer', 3, 0.94, 'Net 21'),
('Blue Diamond Growers Supplier', 'manufacturer', 6, 0.91, 'Net 30'),
('The Wonderful Company Supplier', 'manufacturer', 5, 0.93, 'Net 30'),
('Organic Valley Supplier', 'manufacturer', 4, 0.90, 'Net 21'),
('Bob''s Red Mill Supplier', 'manufacturer', 7, 0.89, 'Net 30'),
('Barilla Group Supplier', 'manufacturer', 10, 0.87, 'Net 45'),
('B&G Foods Supplier', 'manufacturer', 8, 0.88, 'Net 30'),
('Ocean Spray Cranberries Supplier', 'manufacturer', 5, 0.92, 'Net 30'),
('ShelfWise Private Label Supplier', 'private_label', 6, 0.94, 'Net 30'),
('Regional Produce Distributor', 'distributor', 2, 0.85, 'Net 7'),
('Regional Dairy Distributor', 'distributor', 2, 0.87, 'Net 7'),
('Regional Meat Distributor', 'distributor', 1, 0.86, 'Net 7');

-- Payment methods table
CREATE TABLE payment_methods (
    payment_method_id SERIAL PRIMARY KEY,
    payment_method_code VARCHAR(20) UNIQUE NOT NULL,
    payment_method_name VARCHAR(50) NOT NULL,
    processing_fee_pct DECIMAL(4,3),
    is_active BOOLEAN
);

INSERT INTO payment_methods (payment_method_code, payment_method_name, processing_fee_pct, is_active) VALUES
('credit', 'Credit Card', 2.500, true),
('debit', 'Debit Card', 1.500, true),
('cash', 'Cash', 0.000, true),
('mobile_pay', 'Mobile Payment', 2.200, true),
('gift_card', 'Gift Card', 0.000, true),
('ebt', 'EBT/SNAP', 0.500, true),
('check', 'Check', 0.750, false),
('crypto', 'Cryptocurrency', 1.000, false);

-- Promotion types table
CREATE TABLE promotion_types (
    promo_type_id SERIAL PRIMARY KEY,
    promo_type_code VARCHAR(50) UNIQUE NOT NULL,
    promo_type_name VARCHAR(100) NOT NULL,
    typical_discount_pct INTEGER,
    typical_duration_days INTEGER
);

INSERT INTO promotion_types (promo_type_code, promo_type_name, typical_discount_pct, typical_duration_days) VALUES
('price_cut', 'Price Reduction', 20, 14),
('bogo', 'Buy One Get One', 50, 7),
('bundle', 'Bundle Deal', 15, 14),
('loyalty', 'Loyalty Member Exclusive', 10, 30),
('clearance', 'Clearance Sale', 40, 30),
('seasonal', 'Seasonal Promotion', 25, 21),
('flash_sale', 'Flash Sale', 30, 3),
('new_product', 'New Product Introduction', 15, 14);

-- Return reasons table
CREATE TABLE return_reasons (
    return_reason_id SERIAL PRIMARY KEY,
    return_reason_code VARCHAR(50) UNIQUE NOT NULL,
    return_reason_name VARCHAR(100) NOT NULL,
    is_quality_issue BOOLEAN,
    is_preventable BOOLEAN
);

INSERT INTO return_reasons (return_reason_code, return_reason_name, is_quality_issue, is_preventable) VALUES
('defective', 'Defective Product', true, true),
('wrong_item', 'Wrong Item Received', false, true),
('expired', 'Expired Product', true, true),
('damaged', 'Damaged in Transit', true, true),
('changed_mind', 'Customer Changed Mind', false, false),
('not_as_described', 'Not As Described', false, true),
('allergic_reaction', 'Allergic Reaction', false, false),
('duplicate_purchase', 'Duplicate Purchase', false, false),
('gift_return', 'Gift Return', false, false),
('price_match', 'Price Match Request', false, false);

-- Waste reasons table
CREATE TABLE waste_reasons (
    waste_reason_id SERIAL PRIMARY KEY,
    waste_reason_code VARCHAR(50) UNIQUE NOT NULL,
    waste_reason_name VARCHAR(100) NOT NULL,
    is_preventable BOOLEAN
);

INSERT INTO waste_reasons (waste_reason_code, waste_reason_name, is_preventable) VALUES
('expired', 'Expired/Past Sell-By Date', true),
('damaged', 'Damaged Product', true),
('recalled', 'Product Recall', false),
('overstocked', 'Overstocked/Slow Moving', true),
('display_damage', 'Display/Shelf Damage', true),
('temperature_abuse', 'Temperature Abuse', true),
('pest_contamination', 'Pest Contamination', true),
('customer_damage', 'Customer Damaged', false);

-- ============================================================================
-- MAIN TABLES
-- ============================================================================

-- Products table
CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    sku VARCHAR(50) UNIQUE NOT NULL,
    brand VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    sub_category VARCHAR(50),
    size VARCHAR(20),
    unit_of_measure VARCHAR(20),
    list_price DECIMAL(10,2) NOT NULL,
    cost DECIMAL(10,2) NOT NULL,
    launch_date DATE NOT NULL,
    discontinue_date DATE,
    brand_popularity DECIMAL(10,2),
    tier VARCHAR(20),
    pareto_weight DECIMAL(20,18)
);

-- Stores table
CREATE TABLE stores (
    store_id INTEGER PRIMARY KEY,
    region VARCHAR(20) NOT NULL,
    store_type VARCHAR(20) NOT NULL,
    sq_ft INTEGER NOT NULL,
    opened_date DATE NOT NULL,
    climate_zone VARCHAR(20) NOT NULL,
    city VARCHAR(100),
    latitude DECIMAL(10, 6),
    longitude DECIMAL(10, 6)
);

-- Promotions table
CREATE TABLE promotions (
    promo_id INTEGER PRIMARY KEY,
    sku VARCHAR(50) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    promo_type VARCHAR(20) NOT NULL,
    discount_pct DECIMAL(5,2),
    ad_feature BOOLEAN NOT NULL DEFAULT FALSE,
    display_type VARCHAR(20),
    expected_uplift DECIMAL(5,2),
    supplier_funding_usd DECIMAL(10,2) DEFAULT 0
);

-- Assortment table
CREATE TABLE assortment (
    store_id INTEGER NOT NULL,
    sku VARCHAR(50) NOT NULL,
    active_from DATE NOT NULL,
    active_to DATE,
    planogram_facings INTEGER NOT NULL,
    shelf_height_cm DECIMAL(6,2),
    PRIMARY KEY (store_id, sku, active_from)
);

-- Inventory daily table
CREATE TABLE inventory_daily (
    date DATE NOT NULL,
    store_id INTEGER NOT NULL,
    sku VARCHAR(50) NOT NULL,
    on_hand INTEGER NOT NULL DEFAULT 0,
    on_order INTEGER NOT NULL DEFAULT 0,
    in_transit INTEGER NOT NULL DEFAULT 0,
    safety_stock INTEGER NOT NULL DEFAULT 0,
    last_scan_ts TIMESTAMP,
    system_on_hand INTEGER NOT NULL DEFAULT 0,
    available_to_promise INTEGER NOT NULL DEFAULT 0,
    open_hours DECIMAL(4,2) DEFAULT 12,
    in_stock_hours DECIMAL(4,2) DEFAULT 0,
    dc_allocated_qty INTEGER DEFAULT 0,
    quarantine_hold INTEGER DEFAULT 0,
    PRIMARY KEY (date, store_id, sku)
);

-- Sales daily table
CREATE TABLE sales_daily (
    date DATE NOT NULL,
    store_id INTEGER NOT NULL,
    sku VARCHAR(50) NOT NULL,
    units_sold INTEGER NOT NULL DEFAULT 0,
    gross_revenue DECIMAL(12,2) NOT NULL DEFAULT 0,
    promo_id INTEGER,
    regular_price DECIMAL(10,2) NOT NULL,
    net_price DECIMAL(10,2) NOT NULL,
    revenue DECIMAL(12,2) NOT NULL DEFAULT 0,
    supplier_rebate_amt DECIMAL(10,2) DEFAULT 0,
    spoilage_cost DECIMAL(10,2) DEFAULT 0,
    promo_funding_received DECIMAL(10,2) DEFAULT 0,
    gross_margin_pct DECIMAL(5,2),
    discount_pct DECIMAL(5,2) DEFAULT 0,
    cogs_c DECIMAL(12,2) DEFAULT 0,  -- Ambiguous: COGS calculated (standard average cost method)
    cogs_s DECIMAL(12,2) DEFAULT 0,  -- Ambiguous: COGS with shrinkage (includes theft/damage/spoilage adjustments)
    sales_date DATE NOT NULL,
    posting_date DATE NOT NULL,
    PRIMARY KEY (date, store_id, sku)
);

-- Returns daily table
CREATE TABLE returns_daily (
    date DATE NOT NULL,
    store_id INTEGER NOT NULL,
    sku VARCHAR(50) NOT NULL,
    units_returned INTEGER NOT NULL DEFAULT 0,
    reason_code VARCHAR(20),
    refund_value DECIMAL(10,2) NOT NULL DEFAULT 0,
    PRIMARY KEY (date, store_id, sku)
);

-- Tickets table
CREATE TABLE tickets (
    ticket_id INTEGER PRIMARY KEY,
    created_at TIMESTAMP NOT NULL,
    resolved_at TIMESTAMP,
    store_id INTEGER NOT NULL,
    sku VARCHAR(50),
    issue_type VARCHAR(30) NOT NULL,
    description TEXT,
    root_cause TEXT,
    resolved BOOLEAN NOT NULL DEFAULT FALSE
);

-- Supplier shipments table
CREATE TABLE supplier_shipments (
    shipment_id INTEGER PRIMARY KEY,
    shipment_date DATE NOT NULL,
    delivery_date DATE NOT NULL,
    store_id INTEGER NOT NULL,
    sku VARCHAR(50) NOT NULL,
    quantity_shipped INTEGER NOT NULL,
    quantity_received INTEGER NOT NULL,
    supplier_name VARCHAR(100),
    po_number VARCHAR(50),
    shipment_status VARCHAR(20)
);

-- Price changes table
CREATE TABLE price_changes (
    change_id INTEGER PRIMARY KEY,
    effective_date DATE NOT NULL,
    store_id INTEGER,
    sku VARCHAR(50) NOT NULL,
    new_regular_price DECIMAL(10,2) NOT NULL,
    reason VARCHAR(30) NOT NULL
);

-- Waste and spoilage table
CREATE TABLE waste_spoilage (
    waste_id INTEGER PRIMARY KEY,
    date DATE NOT NULL,
    store_id INTEGER NOT NULL,
    sku VARCHAR(50) NOT NULL,
    quantity_wasted INTEGER NOT NULL,
    waste_reason VARCHAR(50) NOT NULL,
    waste_value DECIMAL(10,2) NOT NULL,
    recorded_by VARCHAR(50)
);

-- Transactions table (customer basket summary)
-- Column order matches Rust CSV output
CREATE TABLE transactions (
    transaction_id BIGINT PRIMARY KEY,
    date DATE NOT NULL,
    store_id INTEGER NOT NULL REFERENCES stores(store_id),
    timestamp TIMESTAMP NOT NULL,
    total_items INTEGER NOT NULL,
    payment_method VARCHAR(20) NOT NULL,
    customer_type VARCHAR(20) NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL
);

-- Copy data from CSV files
-- All CSV files are in the same directory as this SQL file
\COPY products FROM '/docker-entrypoint-initdb.d/products.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',');
\COPY stores FROM '/docker-entrypoint-initdb.d/stores.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',');
\COPY promotions FROM '/docker-entrypoint-initdb.d/promotions.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',');
\COPY assortment FROM '/docker-entrypoint-initdb.d/assortment.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',');
\COPY inventory_daily FROM '/docker-entrypoint-initdb.d/inventory_daily.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',');
\COPY sales_daily FROM '/docker-entrypoint-initdb.d/sales_daily.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',');
\COPY supplier_shipments FROM '/docker-entrypoint-initdb.d/supplier_shipments.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',');
\COPY waste_spoilage FROM '/docker-entrypoint-initdb.d/waste_spoilage.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',');
-- Import additional tables with generated data
\COPY price_changes FROM '/docker-entrypoint-initdb.d/price_changes.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',');
\COPY tickets FROM '/docker-entrypoint-initdb.d/tickets.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',');
\COPY returns_daily FROM '/docker-entrypoint-initdb.d/returns_daily.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',');
-- Import transaction data AFTER table is created
\COPY transactions FROM '/docker-entrypoint-initdb.d/transactions.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',');

-- Add foreign key constraints after data is loaded
ALTER TABLE promotions ADD CONSTRAINT fk_promotions_sku 
    FOREIGN KEY (sku) REFERENCES products(sku);

ALTER TABLE assortment ADD CONSTRAINT fk_assortment_store 
    FOREIGN KEY (store_id) REFERENCES stores(store_id);
ALTER TABLE assortment ADD CONSTRAINT fk_assortment_sku
    FOREIGN KEY (sku) REFERENCES products(sku);

ALTER TABLE inventory_daily ADD CONSTRAINT fk_inventory_store
    FOREIGN KEY (store_id) REFERENCES stores(store_id);
ALTER TABLE inventory_daily ADD CONSTRAINT fk_inventory_sku
    FOREIGN KEY (sku) REFERENCES products(sku);

ALTER TABLE sales_daily ADD CONSTRAINT fk_sales_store
    FOREIGN KEY (store_id) REFERENCES stores(store_id);
ALTER TABLE sales_daily ADD CONSTRAINT fk_sales_sku
    FOREIGN KEY (sku) REFERENCES products(sku);

-- Re-enable FK constraints for returns_daily (table now has data)
ALTER TABLE returns_daily ADD CONSTRAINT fk_returns_store
    FOREIGN KEY (store_id) REFERENCES stores(store_id);
ALTER TABLE returns_daily ADD CONSTRAINT fk_returns_sku
    FOREIGN KEY (sku) REFERENCES products(sku);

-- Re-enable FK constraints for tickets (table now has data)
ALTER TABLE tickets ADD CONSTRAINT fk_tickets_store
    FOREIGN KEY (store_id) REFERENCES stores(store_id);
ALTER TABLE tickets ADD CONSTRAINT fk_tickets_sku
    FOREIGN KEY (sku) REFERENCES products(sku);

ALTER TABLE supplier_shipments ADD CONSTRAINT fk_shipments_store
    FOREIGN KEY (store_id) REFERENCES stores(store_id);
ALTER TABLE supplier_shipments ADD CONSTRAINT fk_shipments_sku
    FOREIGN KEY (sku) REFERENCES products(sku);

ALTER TABLE waste_spoilage ADD CONSTRAINT fk_waste_store
    FOREIGN KEY (store_id) REFERENCES stores(store_id);
ALTER TABLE waste_spoilage ADD CONSTRAINT fk_waste_sku
    FOREIGN KEY (sku) REFERENCES products(sku);

-- Re-enable FK constraints for price_changes (table now has data)
ALTER TABLE price_changes ADD CONSTRAINT fk_price_store
    FOREIGN KEY (store_id) REFERENCES stores(store_id);
ALTER TABLE price_changes ADD CONSTRAINT fk_price_sku
    FOREIGN KEY (sku) REFERENCES products(sku);

-- Create indexes for performance
-- Primary table indexes
CREATE INDEX idx_sales_date ON sales_daily(date);
CREATE INDEX idx_sales_store ON sales_daily(store_id);
CREATE INDEX idx_sales_sku ON sales_daily(sku);
CREATE INDEX idx_sales_promo ON sales_daily(promo_id);
CREATE INDEX idx_inventory_date ON inventory_daily(date);
CREATE INDEX idx_inventory_store ON inventory_daily(store_id);
CREATE INDEX idx_inventory_sku ON inventory_daily(sku);
CREATE INDEX idx_promotions_sku ON promotions(sku);
CREATE INDEX idx_promotions_dates ON promotions(start_date, end_date);
CREATE INDEX idx_tickets_store ON tickets(store_id);
CREATE INDEX idx_tickets_created ON tickets(created_at);
CREATE INDEX idx_price_changes_date ON price_changes(effective_date);

-- Additional strategic indexes for common query patterns
-- Composite indexes for date range queries with store/sku filters
CREATE INDEX idx_sales_date_store_sku ON sales_daily(date, store_id, sku);
CREATE INDEX idx_inventory_date_store_sku ON inventory_daily(date, store_id, sku);

-- Index for returns analysis
CREATE INDEX idx_returns_date ON returns_daily(date);
CREATE INDEX idx_returns_store ON returns_daily(store_id);
CREATE INDEX idx_returns_sku ON returns_daily(sku);
CREATE INDEX idx_returns_reason ON returns_daily(reason_code);

-- Index for waste/spoilage tracking
CREATE INDEX idx_waste_date ON waste_spoilage(date);
CREATE INDEX idx_waste_store ON waste_spoilage(store_id);
CREATE INDEX idx_waste_sku ON waste_spoilage(sku);
CREATE INDEX idx_waste_reason ON waste_spoilage(waste_reason);

-- Index for supplier shipments tracking
CREATE INDEX idx_shipments_delivery_date ON supplier_shipments(delivery_date);
CREATE INDEX idx_shipments_store ON supplier_shipments(store_id);
CREATE INDEX idx_shipments_sku ON supplier_shipments(sku);
CREATE INDEX idx_shipments_status ON supplier_shipments(shipment_status);

-- Index for price changes by SKU
CREATE INDEX idx_price_changes_sku ON price_changes(sku);

-- Index for tickets resolution tracking
CREATE INDEX idx_tickets_resolved ON tickets(resolved);
CREATE INDEX idx_tickets_issue_type ON tickets(issue_type);

-- Index for assortment lookups
CREATE INDEX idx_assortment_store ON assortment(store_id);
CREATE INDEX idx_assortment_sku ON assortment(sku);
CREATE INDEX idx_assortment_dates ON assortment(active_from, active_to);

-- Index for product category queries
CREATE INDEX idx_products_category ON products(category);
CREATE INDEX idx_products_brand ON products(brand);

-- Index for store queries by region and type
CREATE INDEX idx_stores_region ON stores(region);
CREATE INDEX idx_stores_type ON stores(store_type);

-- Partial indexes for common filters (more efficient for specific queries)
CREATE INDEX idx_tickets_unresolved ON tickets(store_id, created_at) WHERE resolved = FALSE;

-- Create transaction indexes
CREATE INDEX idx_transactions_date ON transactions(date);
CREATE INDEX idx_transactions_store ON transactions(store_id);
CREATE INDEX idx_transactions_timestamp ON transactions(timestamp);

CREATE INDEX idx_promotions_active ON promotions(sku, start_date, end_date) WHERE ad_feature = TRUE;

-- Read-only user setup
CREATE USER shelfwise_readonly WITH PASSWORD '${READONLY_PASSWORD:-readonly_password}';
GRANT CONNECT ON DATABASE shelfwise TO shelfwise_readonly;
GRANT USAGE ON SCHEMA public TO shelfwise_readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO shelfwise_readonly;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO shelfwise_readonly;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO shelfwise_readonly;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT USAGE ON SEQUENCES TO shelfwise_readonly;
REVOKE INSERT, UPDATE, DELETE, TRUNCATE ON ALL TABLES IN SCHEMA public FROM shelfwise_readonly;
COMMENT ON ROLE shelfwise_readonly IS 'Read-only user for analytics, reporting, and Hasura DDN connectors';
