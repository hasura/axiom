-- ShelfWise Retail Analytics Database

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================================================
-- PERFORMANCE SETTINGS FOR DATA LOADING
-- ==============================================uuid-ossp==============================
-- Use session-level settings for parameters that support it
-- Note: autovacuum cannot be disabled at session level, only server level
-- For initial load, consider setting autovacuum=off in postgresql.conf

-- Set synchronous_commit to off for faster writes during data load
-- This trades durability for speed - acceptable during initial load
SET synchronous_commit = off;

-- Increase maintenance_work_mem for faster index creation
SET maintenance_work_mem = '1GB';

-- Increase work_mem for better sort performance
SET work_mem = '256MB';

-- Drop tables in reverse dependency order
DROP TABLE IF EXISTS delivery_assignments CASCADE;
DROP TABLE IF EXISTS transaction_line_items CASCADE;
DROP TABLE IF EXISTS delivery_zones CASCADE;
DROP TABLE IF EXISTS delivery_drivers CASCADE;
DROP TABLE IF EXISTS customer_addresses CASCADE;
DROP TABLE IF EXISTS customers CASCADE;
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
-- REFERENCE TABLES
-- ============================================================================

CREATE TABLE regions (
    region_id SERIAL PRIMARY KEY,
    region_code VARCHAR(20) UNIQUE NOT NULL,
    region_name VARCHAR(100) NOT NULL,
    country VARCHAR(50) NOT NULL,
    timezone VARCHAR(50),
    description VARCHAR(500)
);

CREATE TABLE categories (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(50) UNIQUE NOT NULL,
    category_group VARCHAR(50),
    margin_target_pct NUMERIC(4,2),
    is_perishable BOOLEAN,
    elasticity NUMERIC(3,2)
);

CREATE TABLE store_types (
    store_type_id SERIAL PRIMARY KEY,
    store_type_code VARCHAR(20) UNIQUE NOT NULL,
    store_type_name VARCHAR(50) NOT NULL,
    typical_sq_ft_min INTEGER,
    typical_sq_ft_max INTEGER,
    typical_sku_count SMALLINT,
    operating_hours SMALLINT
);

CREATE TABLE brands (
    brand_id SERIAL PRIMARY KEY,
    brand_name VARCHAR(100) UNIQUE NOT NULL,
    brand_tier VARCHAR(20) NOT NULL,
    manufacturer VARCHAR(100),
    is_private_label BOOLEAN,
    brand_popularity NUMERIC(3,2)
);

CREATE TABLE suppliers (
    supplier_id SERIAL PRIMARY KEY,
    supplier_name VARCHAR(100) UNIQUE NOT NULL,
    supplier_type VARCHAR(50),
    lead_time_days SMALLINT,
    reliability_score NUMERIC(3,2),
    payment_terms VARCHAR(50)
);

CREATE TABLE payment_methods (
    payment_method_id SERIAL PRIMARY KEY,
    payment_method_code VARCHAR(20) UNIQUE NOT NULL,
    payment_method_name VARCHAR(50) NOT NULL,
    processing_fee_pct NUMERIC(4,3),
    is_active BOOLEAN
);

CREATE TABLE promotion_types (
    promo_type_id SERIAL PRIMARY KEY,
    promo_type_code VARCHAR(50) UNIQUE NOT NULL,
    promo_type_name VARCHAR(100) NOT NULL,
    typical_discount_pct SMALLINT,
    typical_duration_days SMALLINT
);

CREATE TABLE return_reasons (
    return_reason_id SERIAL PRIMARY KEY,
    return_reason_code VARCHAR(50) UNIQUE NOT NULL,
    return_reason_name VARCHAR(100) NOT NULL,
    is_quality_issue BOOLEAN,
    is_preventable BOOLEAN
);

CREATE TABLE waste_reasons (
    waste_reason_id SERIAL PRIMARY KEY,
    waste_reason_code VARCHAR(50) UNIQUE NOT NULL,
    waste_reason_name VARCHAR(100) NOT NULL,
    is_preventable BOOLEAN
);

-- ============================================================================
-- MAIN TABLES
-- ============================================================================

CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    sku VARCHAR(25) UNIQUE NOT NULL,
    brand VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    sub_category VARCHAR(50),
    size VARCHAR(20),
    unit_of_measure VARCHAR(20),
    list_price NUMERIC(7,2) NOT NULL,
    cost NUMERIC(7,2) NOT NULL,
    launch_date DATE NOT NULL,
    discontinue_date DATE,
    brand_popularity NUMERIC(4,2),
    tier VARCHAR(20),
    pareto_weight NUMERIC(20,18)
);

CREATE TABLE stores (
    store_id INTEGER PRIMARY KEY,
    region VARCHAR(20) NOT NULL,
    store_type VARCHAR(20) NOT NULL,
    sq_ft INTEGER NOT NULL,
    opened_date DATE NOT NULL,
    climate_zone VARCHAR(20) NOT NULL,
    city VARCHAR(100),
    latitude NUMERIC(9, 6),
    longitude NUMERIC(10, 6)
);

-- ============================================================================
-- CUSTOMER TABLES
-- ============================================================================

CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    email VARCHAR(255) UNIQUE,
    phone VARCHAR(20),
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    age_bracket VARCHAR(20),
    household_size SMALLINT,
    income_bracket VARCHAR(20),
    primary_store_id INTEGER,
    primary_city VARCHAR(100),
    home_latitude NUMERIC(9, 6),
    home_longitude NUMERIC(10, 6),
    loyalty_member BOOLEAN DEFAULT FALSE,
    loyalty_tier VARCHAR(20),
    loyalty_join_date DATE,
    preferred_shopping_time VARCHAR(20),
    price_sensitivity VARCHAR(20),
    customer_segment VARCHAR(30),
    created_date DATE,  -- NULL for founding customers (pre-existing before tracking began)
    has_online_account BOOLEAN DEFAULT FALSE,
    prefers_online BOOLEAN DEFAULT FALSE
);

CREATE TABLE customer_addresses (
    address_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    address_type VARCHAR(20),
    is_default BOOLEAN DEFAULT FALSE,
    street_address VARCHAR(255),
    apartment_unit VARCHAR(50),
    city VARCHAR(100),
    state VARCHAR(2),
    zip_code VARCHAR(10),
    latitude NUMERIC(9, 6),
    longitude NUMERIC(10, 6),
    delivery_instructions VARCHAR(500),
    has_doorman BOOLEAN DEFAULT FALSE,
    requires_signature BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP
);

-- ============================================================================
-- DELIVERY & FULFILLMENT TABLES
-- ============================================================================

CREATE TABLE delivery_drivers (
    driver_id INTEGER PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    phone VARCHAR(20),
    email VARCHAR(255),
    driver_type VARCHAR(30),
    employment_status VARCHAR(20),
    primary_store_id INTEGER,
    service_radius_miles NUMERIC(5,2),
    service_cities VARCHAR(500),
    vehicle_type VARCHAR(30),
    vehicle_capacity_items SMALLINT,
    has_insulated_bags BOOLEAN,
    acceptance_rate NUMERIC(5,2),
    is_available BOOLEAN DEFAULT TRUE,
    current_latitude NUMERIC(9, 6),
    current_longitude NUMERIC(10, 6),
    last_location_update TIMESTAMP,
    hire_date DATE,
    base_pay_per_delivery NUMERIC(6,2),
    mileage_rate NUMERIC(4,2)
);

CREATE TABLE delivery_zones (
    zone_id SERIAL PRIMARY KEY,
    zone_name VARCHAR(100),
    store_id INTEGER,
    center_latitude NUMERIC(9, 6),
    center_longitude NUMERIC(10, 6),
    radius_miles NUMERIC(5,2),
    delivery_fee NUMERIC(6,2),
    min_order_amount NUMERIC(7,2),
    free_delivery_threshold NUMERIC(7,2),
    estimated_delivery_time_minutes SMALLINT,
    is_active BOOLEAN DEFAULT TRUE,
    service_hours_start TIME,
    service_hours_end TIME,
    avg_daily_orders INTEGER,
    peak_hours VARCHAR(200)
);

CREATE TABLE promotions (
    promo_id INTEGER PRIMARY KEY,
    sku VARCHAR(25) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    promo_type VARCHAR(20) NOT NULL,
    discount_pct NUMERIC(5,2),
    ad_feature BOOLEAN NOT NULL DEFAULT FALSE,
    display_type VARCHAR(20),
    expected_uplift NUMERIC(5,2),
    supplier_funding_usd NUMERIC(8,2) DEFAULT 0
);

CREATE TABLE assortment (
    store_id INTEGER NOT NULL,
    sku VARCHAR(25) NOT NULL,
    active_from DATE NOT NULL,
    active_to DATE,
    planogram_facings SMALLINT NOT NULL,
    shelf_height_cm NUMERIC(5,2),
    PRIMARY KEY (store_id, sku, active_from)
);

CREATE TABLE inventory_daily (
    date DATE NOT NULL,
    store_id INTEGER NOT NULL,
    sku VARCHAR(25) NOT NULL,
    on_hand INTEGER NOT NULL DEFAULT 0,
    on_order INTEGER NOT NULL DEFAULT 0,
    in_transit INTEGER NOT NULL DEFAULT 0,
    safety_stock INTEGER NOT NULL DEFAULT 0,
    last_scan_ts TIMESTAMP,
    system_on_hand INTEGER NOT NULL DEFAULT 0,
    available_to_promise INTEGER NOT NULL DEFAULT 0,
    open_hours SMALLINT DEFAULT 12,
    in_stock_hours REAL DEFAULT 0,
    dc_allocated_qty INTEGER DEFAULT 0,
    quarantine_hold INTEGER DEFAULT 0,
    PRIMARY KEY (date, store_id, sku)
);

CREATE TABLE sales_daily (
    date DATE NOT NULL,
    store_id INTEGER NOT NULL,
    sku VARCHAR(25) NOT NULL,
    units_sold INTEGER NOT NULL DEFAULT 0,
    gross_revenue NUMERIC(10,2) NOT NULL DEFAULT 0,
    promo_id INTEGER,
    regular_price NUMERIC(7,2) NOT NULL,
    net_price NUMERIC(7,2) NOT NULL,
    revenue NUMERIC(10,2) NOT NULL DEFAULT 0,
    supplier_rebate_amt NUMERIC(7,2) DEFAULT 0,
    spoilage_cost NUMERIC(7,2) DEFAULT 0,
    promo_funding_received NUMERIC(7,2) DEFAULT 0,
    gross_margin_pct NUMERIC(5,2),
    discount_pct NUMERIC(5,2) DEFAULT 0,
    cogs_c NUMERIC(10,2) DEFAULT 0,
    cogs_s NUMERIC(10,2) DEFAULT 0,
    sales_date DATE NOT NULL,
    posting_date DATE NOT NULL,
    PRIMARY KEY (date, store_id, sku)
);

CREATE TABLE returns_daily (
    date DATE NOT NULL,
    store_id INTEGER NOT NULL,
    sku VARCHAR(25) NOT NULL,
    units_returned INTEGER NOT NULL DEFAULT 0,
    reason_code VARCHAR(20),
    refund_value NUMERIC(8,2) NOT NULL DEFAULT 0,
    transaction_id INTEGER NOT NULL,
    line_number INTEGER NOT NULL,
    PRIMARY KEY (date, store_id, sku, transaction_id, line_number)
);

CREATE TABLE tickets (
    ticket_id INTEGER PRIMARY KEY,
    created_at TIMESTAMP NOT NULL,
    resolved_at TIMESTAMP,
    store_id INTEGER NOT NULL,
    sku VARCHAR(25),
    issue_type VARCHAR(30) NOT NULL,
    description VARCHAR(2000),
    root_cause VARCHAR(1000),
    resolved BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE supplier_shipments (
    shipment_id INTEGER PRIMARY KEY,
    shipment_date DATE NOT NULL,
    delivery_date DATE NOT NULL,
    store_id INTEGER NOT NULL,
    sku VARCHAR(25) NOT NULL,
    quantity_shipped INTEGER NOT NULL,
    quantity_received INTEGER NOT NULL,
    supplier_name VARCHAR(100),
    po_number VARCHAR(50),
    shipment_status VARCHAR(20)
);

CREATE TABLE price_changes (
    change_id INTEGER PRIMARY KEY,
    effective_date DATE NOT NULL,
    store_id INTEGER,
    sku VARCHAR(25) NOT NULL,
    new_regular_price NUMERIC(7,2) NOT NULL,
    reason VARCHAR(30) NOT NULL
);

CREATE TABLE waste_spoilage (
    waste_id INTEGER PRIMARY KEY,
    date DATE NOT NULL,
    store_id INTEGER NOT NULL,
    sku VARCHAR(25) NOT NULL,
    quantity_wasted INTEGER NOT NULL,
    waste_reason VARCHAR(50) NOT NULL,
    waste_value NUMERIC(8,2) NOT NULL,
    recorded_by VARCHAR(50)
);

CREATE TABLE transactions (
    transaction_id INTEGER PRIMARY KEY,
    date DATE NOT NULL,
    store_id INTEGER NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    total_items SMALLINT NOT NULL,
    payment_method VARCHAR(20) NOT NULL,
    customer_type VARCHAR(20) NOT NULL,
    total_amount NUMERIC(8,2) NOT NULL,
    customer_id INTEGER,
    is_loyalty_transaction BOOLEAN DEFAULT FALSE,
    loyalty_points_earned INTEGER DEFAULT 0,
    loyalty_points_redeemed INTEGER DEFAULT 0,
    fulfillment_type VARCHAR(30),
    order_status VARCHAR(30),
    fulfillment_store_id INTEGER,
    delivery_address_id INTEGER,
    delivery_fee NUMERIC(5,2) DEFAULT 0,
    tip_amount NUMERIC(5,2) DEFAULT 0,
    delivery_instructions VARCHAR(500),
    requested_delivery_time TIMESTAMP,
    actual_delivery_time TIMESTAMP
);

CREATE TABLE transaction_line_items (
    transaction_id INTEGER NOT NULL,
    line_number SMALLINT NOT NULL,
    sku VARCHAR(25) NOT NULL,
    quantity SMALLINT NOT NULL,
    unit_price NUMERIC(7,2) NOT NULL,
    line_total NUMERIC(8,2) NOT NULL,
    promo_id INTEGER,
    discount_amount NUMERIC(7,2) DEFAULT 0,
    PRIMARY KEY (transaction_id, line_number)
);

CREATE TABLE delivery_assignments (
    assignment_id INTEGER PRIMARY KEY,
    transaction_id INTEGER,
    driver_id INTEGER,
    assigned_at TIMESTAMP NOT NULL,
    accepted_at TIMESTAMP,
    picked_up_at TIMESTAMP,
    delivered_at TIMESTAMP,
    cancelled_at TIMESTAMP,
    assignment_status VARCHAR(30),
    cancellation_reason VARCHAR(100),
    pickup_store_id INTEGER,
    estimated_pickup_time TIMESTAMP,
    actual_pickup_time TIMESTAMP,
    estimated_delivery_time TIMESTAMP,
    actual_delivery_time TIMESTAMP,
    distance_miles NUMERIC(5,2),
    estimated_duration_minutes SMALLINT,
    actual_duration_minutes SMALLINT,
    driver_pay NUMERIC(6,2),
    driver_tip NUMERIC(6,2),
    driver_total_earnings NUMERIC(6,2),
    customer_rating SMALLINT,
    driver_notes VARCHAR(1000),
    customer_feedback VARCHAR(2000)
);

-- ============================================================================
-- LOAD DATA FROM CSV FILES
-- ============================================================================

\COPY regions FROM '/docker-entrypoint-initdb.d/regions.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',');
\COPY categories FROM '/docker-entrypoint-initdb.d/categories.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',');
\COPY store_types FROM '/docker-entrypoint-initdb.d/store_types.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',');
\COPY brands FROM '/docker-entrypoint-initdb.d/brands.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',');
\COPY suppliers FROM '/docker-entrypoint-initdb.d/suppliers.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',');
\COPY payment_methods FROM '/docker-entrypoint-initdb.d/payment_methods.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',');
\COPY promotion_types FROM '/docker-entrypoint-initdb.d/promotion_types.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',');
\COPY return_reasons FROM '/docker-entrypoint-initdb.d/return_reasons.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',');
\COPY waste_reasons FROM '/docker-entrypoint-initdb.d/waste_reasons.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',');
\COPY products FROM '/docker-entrypoint-initdb.d/products.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',');
\COPY stores FROM '/docker-entrypoint-initdb.d/stores.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',');
\COPY customers FROM '/docker-entrypoint-initdb.d/customers.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',');
\COPY customer_addresses FROM '/docker-entrypoint-initdb.d/customer_addresses.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',');
\COPY delivery_drivers FROM '/docker-entrypoint-initdb.d/delivery_drivers.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',');
\COPY delivery_zones FROM '/docker-entrypoint-initdb.d/delivery_zones.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',');
\COPY promotions FROM '/docker-entrypoint-initdb.d/promotions.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',');
\COPY assortment FROM '/docker-entrypoint-initdb.d/assortment.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',');
\COPY inventory_daily FROM '/docker-entrypoint-initdb.d/inventory_daily.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',');
\COPY sales_daily FROM '/docker-entrypoint-initdb.d/sales_daily.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',');
\COPY returns_daily FROM '/docker-entrypoint-initdb.d/returns_daily.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',');
\COPY supplier_shipments FROM '/docker-entrypoint-initdb.d/supplier_shipments.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',');
\COPY waste_spoilage FROM '/docker-entrypoint-initdb.d/waste_spoilage.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',');
\COPY price_changes FROM '/docker-entrypoint-initdb.d/price_changes.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',');
\COPY tickets FROM '/docker-entrypoint-initdb.d/tickets.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',');
\COPY transactions FROM '/docker-entrypoint-initdb.d/transactions.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',');
\COPY transaction_line_items FROM '/docker-entrypoint-initdb.d/transaction_line_items.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',');
\COPY delivery_assignments FROM '/docker-entrypoint-initdb.d/delivery_assignments.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',');

-- ============================================================================
-- FOREIGN KEY CONSTRAINTS
-- ============================================================================

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

ALTER TABLE returns_daily ADD CONSTRAINT fk_returns_store
    FOREIGN KEY (store_id) REFERENCES stores(store_id);
ALTER TABLE returns_daily ADD CONSTRAINT fk_returns_sku
    FOREIGN KEY (sku) REFERENCES products(sku);
ALTER TABLE returns_daily ADD CONSTRAINT fk_returns_transaction
    FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id);

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

ALTER TABLE price_changes ADD CONSTRAINT fk_price_store
    FOREIGN KEY (store_id) REFERENCES stores(store_id);
ALTER TABLE price_changes ADD CONSTRAINT fk_price_sku
    FOREIGN KEY (sku) REFERENCES products(sku);

ALTER TABLE customers ADD CONSTRAINT fk_customers_store
    FOREIGN KEY (primary_store_id) REFERENCES stores(store_id);

ALTER TABLE customer_addresses ADD CONSTRAINT fk_addresses_customer
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id);

ALTER TABLE transaction_line_items ADD CONSTRAINT fk_line_items_transaction
    FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id);
ALTER TABLE transaction_line_items ADD CONSTRAINT fk_line_items_sku
    FOREIGN KEY (sku) REFERENCES products(sku);

ALTER TABLE delivery_drivers ADD CONSTRAINT fk_drivers_store
    FOREIGN KEY (primary_store_id) REFERENCES stores(store_id);

ALTER TABLE delivery_zones ADD CONSTRAINT fk_zones_store
    FOREIGN KEY (store_id) REFERENCES stores(store_id);

ALTER TABLE transactions ADD CONSTRAINT fk_transactions_store
    FOREIGN KEY (store_id) REFERENCES stores(store_id);
ALTER TABLE transactions ADD CONSTRAINT fk_transactions_customer
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id);
ALTER TABLE transactions ADD CONSTRAINT fk_transactions_fulfillment_store
    FOREIGN KEY (fulfillment_store_id) REFERENCES stores(store_id);
ALTER TABLE transactions ADD CONSTRAINT fk_transactions_delivery_address
    FOREIGN KEY (delivery_address_id) REFERENCES customer_addresses(address_id);

ALTER TABLE delivery_assignments ADD CONSTRAINT fk_assignments_transaction
    FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id);
ALTER TABLE delivery_assignments ADD CONSTRAINT fk_assignments_driver
    FOREIGN KEY (driver_id) REFERENCES delivery_drivers(driver_id);
ALTER TABLE delivery_assignments ADD CONSTRAINT fk_assignments_pickup_store
    FOREIGN KEY (pickup_store_id) REFERENCES stores(store_id);

-- ============================================================================
-- INDEXES
-- ============================================================================

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

CREATE INDEX idx_sales_date_store_sku ON sales_daily(date, store_id, sku);
CREATE INDEX idx_inventory_date_store_sku ON inventory_daily(date, store_id, sku);

CREATE INDEX idx_returns_date ON returns_daily(date);
CREATE INDEX idx_returns_store ON returns_daily(store_id);
CREATE INDEX idx_returns_sku ON returns_daily(sku);
CREATE INDEX idx_returns_reason ON returns_daily(reason_code);

CREATE INDEX idx_waste_date ON waste_spoilage(date);
CREATE INDEX idx_waste_store ON waste_spoilage(store_id);
CREATE INDEX idx_waste_sku ON waste_spoilage(sku);
CREATE INDEX idx_waste_reason ON waste_spoilage(waste_reason);

CREATE INDEX idx_shipments_delivery_date ON supplier_shipments(delivery_date);
CREATE INDEX idx_shipments_store ON supplier_shipments(store_id);
CREATE INDEX idx_shipments_sku ON supplier_shipments(sku);
CREATE INDEX idx_shipments_status ON supplier_shipments(shipment_status);

CREATE INDEX idx_price_changes_sku ON price_changes(sku);

CREATE INDEX idx_tickets_resolved ON tickets(resolved);
CREATE INDEX idx_tickets_issue_type ON tickets(issue_type);

CREATE INDEX idx_assortment_store ON assortment(store_id);
CREATE INDEX idx_assortment_sku ON assortment(sku);
CREATE INDEX idx_assortment_dates ON assortment(active_from, active_to);

CREATE INDEX idx_products_category ON products(category);
CREATE INDEX idx_products_brand ON products(brand);

CREATE INDEX idx_stores_region ON stores(region);
CREATE INDEX idx_stores_type ON stores(store_type);

CREATE INDEX idx_tickets_unresolved ON tickets(store_id, created_at) WHERE resolved = FALSE;
CREATE INDEX idx_transactions_date ON transactions(date);
CREATE INDEX idx_transactions_store ON transactions(store_id);
CREATE INDEX idx_transactions_timestamp ON transactions(timestamp);

CREATE INDEX idx_promotions_active ON promotions(sku, start_date, end_date) WHERE ad_feature = TRUE;

-- Customer indexes
CREATE INDEX idx_customers_email ON customers(email);
CREATE INDEX idx_customers_primary_store ON customers(primary_store_id);
CREATE INDEX idx_customers_segment ON customers(customer_segment);
CREATE INDEX idx_customers_loyalty_member ON customers(loyalty_member);
CREATE INDEX idx_customers_loyalty_tier ON customers(loyalty_tier);
CREATE INDEX idx_customers_created_date ON customers(created_date);
CREATE INDEX idx_customers_city ON customers(primary_city);

CREATE INDEX idx_customer_addresses_customer ON customer_addresses(customer_id);
CREATE INDEX idx_customer_addresses_default ON customer_addresses(customer_id, is_default) WHERE is_default = TRUE;
CREATE INDEX idx_customer_addresses_city ON customer_addresses(city);

-- Transaction customer indexes
CREATE INDEX idx_transactions_customer ON transactions(customer_id);
CREATE INDEX idx_transactions_loyalty ON transactions(customer_id, is_loyalty_transaction) WHERE is_loyalty_transaction = TRUE;
CREATE INDEX idx_transactions_fulfillment_type ON transactions(fulfillment_type);
CREATE INDEX idx_transactions_order_status ON transactions(order_status);

-- Transaction line items indexes
CREATE INDEX idx_transaction_line_items_transaction ON transaction_line_items(transaction_id);
CREATE INDEX idx_transaction_line_items_sku ON transaction_line_items(sku);
CREATE INDEX idx_transaction_line_items_promo ON transaction_line_items(promo_id) WHERE promo_id IS NOT NULL;

-- Delivery indexes
CREATE INDEX idx_delivery_drivers_store ON delivery_drivers(primary_store_id);
CREATE INDEX idx_delivery_drivers_type ON delivery_drivers(driver_type);
CREATE INDEX idx_delivery_drivers_status ON delivery_drivers(employment_status);
CREATE INDEX idx_delivery_drivers_available ON delivery_drivers(is_available, primary_store_id) WHERE is_available = TRUE;

CREATE INDEX idx_delivery_zones_store ON delivery_zones(store_id);
CREATE INDEX idx_delivery_zones_active ON delivery_zones(is_active, store_id) WHERE is_active = TRUE;

CREATE INDEX idx_delivery_assignments_transaction ON delivery_assignments(transaction_id);
CREATE INDEX idx_delivery_assignments_driver ON delivery_assignments(driver_id);
CREATE INDEX idx_delivery_assignments_status ON delivery_assignments(assignment_status);
CREATE INDEX idx_delivery_assignments_assigned_at ON delivery_assignments(assigned_at);
CREATE INDEX idx_delivery_assignments_delivered_at ON delivery_assignments(delivered_at);

-- ============================================================================
-- FINALIZE DATA LOAD
-- ============================================================================
-- Session settings will automatically reset when connection closes
-- No need to explicitly re-enable autovacuum or synchronous_commit

-- Run ANALYZE to update statistics after bulk load
-- This is critical for query performance
ANALYZE;
