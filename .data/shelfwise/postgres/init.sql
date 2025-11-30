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
