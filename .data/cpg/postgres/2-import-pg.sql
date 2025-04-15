CREATE DATABASE inventory;

\c inventory;

CREATE TABLE warehouses (
    warehouse_id SERIAL PRIMARY KEY,
    warehouse_name VARCHAR(100) NOT NULL,
    warehouse_type VARCHAR(50) CHECK (warehouse_type IN ('Regional DC', 'Central DC', 'Fulfillment Center', '3PL')),
    location_city VARCHAR(100),
    location_state VARCHAR(50),
    location_country VARCHAR(50) DEFAULT 'USA',
    square_footage INT,
    max_capacity_pallets INT,
    operating_cost_per_month DECIMAL(12,2)
);

CREATE TABLE inventory (
    inventory_id SERIAL PRIMARY KEY,
    product_id INT NOT NULL,
    warehouse_id INT REFERENCES warehouses(warehouse_id),
    date DATE NOT NULL,
    quantity_on_hand INT NOT NULL,
    quantity_allocated INT DEFAULT 0,
    quantity_available INT GENERATED ALWAYS AS (quantity_on_hand - quantity_allocated) STORED,
    days_of_supply INT,
    inventory_value DECIMAL(12,2),
    reorder_point INT,
    max_capacity INT,
    lot_number VARCHAR(50),
    expiration_date DATE
);

CREATE TABLE inventory_transactions (
    transaction_id SERIAL PRIMARY KEY,
    product_id INT NOT NULL,
    warehouse_id INT REFERENCES warehouses(warehouse_id),
    transaction_date TIMESTAMP NOT NULL,
    transaction_type VARCHAR(50) CHECK (transaction_type IN ('Receipt', 'Shipment', 'Adjustment', 'Transfer In', 'Transfer Out', 'Return')),
    quantity INT NOT NULL,
    reference_number VARCHAR(100),
    notes TEXT
);

CREATE TABLE retailers_copy (
    retailer_id SERIAL PRIMARY KEY,
    retailer_name VARCHAR(100) NOT NULL,
    channel_id INT,
    sales_region VARCHAR(100),
    has_ecommerce BOOLEAN DEFAULT FALSE,
    annual_revenue_tier VARCHAR(50),
    account_tier VARCHAR(50) CHECK (account_tier IN ('Strategic', 'Key', 'Core', 'Small'))
);

CREATE TABLE product_categories_copy (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL,
    parent_category_id INT,
    category_description TEXT,
    is_seasonal BOOLEAN DEFAULT FALSE,
    typical_margin_percentage DECIMAL(5,2)
);

CREATE TABLE products_copy (
    product_id SERIAL PRIMARY KEY,
    product_sku VARCHAR(50) UNIQUE NOT NULL,
    product_name VARCHAR(200) NOT NULL,
    brand_id INT,
    category_id INT,
    subcategory_id INT,
    unit_size VARCHAR(50),
    unit_measure VARCHAR(20),
    case_pack INT,
    weight_oz DECIMAL(8,2),
    wholesale_price DECIMAL(10,2),
    msrp DECIMAL(10,2),
    launch_date DATE,
    discontinue_date DATE,
    is_organic BOOLEAN DEFAULT FALSE,
    is_glutenfree BOOLEAN DEFAULT FALSE,
    is_seasonal BOOLEAN DEFAULT FALSE,
    high_velocity BOOLEAN DEFAULT FALSE
);

CREATE TABLE availability (
    availability_id SERIAL PRIMARY KEY,
    product_id INT REFERENCES products_copy(product_id),
    retailer_id INT REFERENCES retailers_copy(retailer_id),
    date DATE NOT NULL,
    in_stock_percentage DECIMAL(5,2),
    out_of_stock_incidents INT DEFAULT 0,
    on_shelf_availability_percentage DECIMAL(5,2),
    is_online BOOLEAN DEFAULT FALSE,
    days_of_supply INT,
    notes TEXT
);

CREATE TABLE assortment (
    assortment_id SERIAL PRIMARY KEY,
    product_id INT REFERENCES products_copy(product_id),
    retailer_id INT REFERENCES retailers_copy(retailer_id),
    start_date DATE NOT NULL,
    end_date DATE,
    status VARCHAR(50) CHECK (status IN ('Active', 'Planned', 'Discontinued', 'Seasonal')),
    is_core_assortment BOOLEAN DEFAULT FALSE,
    is_promotional_only BOOLEAN DEFAULT FALSE,
    is_online_only BOOLEAN DEFAULT FALSE,
    planogram_position VARCHAR(50),
    facings INT,
    notes TEXT
);

CREATE TABLE demand_forecasts (
    forecast_id SERIAL PRIMARY KEY,
    product_id INT REFERENCES products_copy(product_id),
    retailer_id INT REFERENCES retailers_copy(retailer_id),
    forecast_date DATE NOT NULL,
    forecast_period_start DATE NOT NULL,
    forecast_period_end DATE NOT NULL,
    forecasted_quantity INT NOT NULL,
    forecast_confidence DECIMAL(5,2),
    actual_quantity INT,
    forecast_error_percentage DECIMAL(5,2),
    notes TEXT
);

CREATE TABLE supply_chain_events (
    event_id SERIAL PRIMARY KEY,
    event_type VARCHAR(100),
    start_date DATE NOT NULL,
    end_date DATE,
    severity VARCHAR(20) CHECK (severity IN ('Low', 'Medium', 'High', 'Critical')),
    description TEXT,
    affected_products INT[],
    affected_warehouses INT[],
    impact_estimate TEXT,
    mitigation_actions TEXT
);

CREATE TABLE shipping (
    shipping_id SERIAL PRIMARY KEY,
    origin_warehouse_id INT REFERENCES warehouses(warehouse_id),
    destination_type VARCHAR(50) CHECK (destination_type IN ('Warehouse', 'Retailer', 'Customer')),
    destination_id INT,
    product_id INT REFERENCES products_copy(product_id),
    quantity INT NOT NULL,
    ship_date DATE NOT NULL,
    expected_arrival_date DATE NOT NULL,
    actual_arrival_date DATE,
    status VARCHAR(50) CHECK (status IN ('Planned', 'In Transit', 'Delayed', 'Delivered', 'Cancelled')),
    tracking_number VARCHAR(100),
    carrier VARCHAR(100),
    shipping_cost DECIMAL(10,2)
);

-- Create indexes for better query performance
-- Warehouses indexes
CREATE INDEX idx_warehouses_name ON warehouses(warehouse_name);
CREATE INDEX idx_warehouses_type ON warehouses(warehouse_type);
CREATE INDEX idx_warehouses_location ON warehouses(location_city, location_state);

-- Inventory indexes
CREATE INDEX idx_inventory_product_id ON inventory(product_id);
CREATE INDEX idx_inventory_warehouse_id ON inventory(warehouse_id);
CREATE INDEX idx_inventory_date ON inventory(date);
CREATE INDEX idx_inventory_expiration_date ON inventory(expiration_date);

-- Inventory transactions indexes
CREATE INDEX idx_inventory_transactions_product_id ON inventory_transactions(product_id);
CREATE INDEX idx_inventory_transactions_warehouse_id ON inventory_transactions(warehouse_id);
CREATE INDEX idx_inventory_transactions_date ON inventory_transactions(transaction_date);
CREATE INDEX idx_inventory_transactions_type ON inventory_transactions(transaction_type);

-- Retailers copy indexes
CREATE INDEX idx_retailers_copy_name ON retailers_copy(retailer_name);
CREATE INDEX idx_retailers_copy_channel_id ON retailers_copy(channel_id);
CREATE INDEX idx_retailers_copy_region ON retailers_copy(sales_region);

-- Product categories copy indexes
CREATE INDEX idx_product_categories_copy_name ON product_categories_copy(category_name);
CREATE INDEX idx_product_categories_copy_parent ON product_categories_copy(parent_category_id);

-- Products copy indexes
CREATE INDEX idx_products_copy_name ON products_copy(product_name);
CREATE INDEX idx_products_copy_brand_id ON products_copy(brand_id);
CREATE INDEX idx_products_copy_category_id ON products_copy(category_id);
CREATE INDEX idx_products_copy_subcategory_id ON products_copy(subcategory_id);

-- Availability indexes
CREATE INDEX idx_availability_product_id ON availability(product_id);
CREATE INDEX idx_availability_retailer_id ON availability(retailer_id);
CREATE INDEX idx_availability_date ON availability(date);
CREATE INDEX idx_availability_online ON availability(is_online);

-- Assortment indexes
CREATE INDEX idx_assortment_product_id ON assortment(product_id);
CREATE INDEX idx_assortment_retailer_id ON assortment(retailer_id);
CREATE INDEX idx_assortment_dates ON assortment(start_date, end_date);
CREATE INDEX idx_assortment_status ON assortment(status);

-- Demand forecasts indexes
CREATE INDEX idx_demand_forecasts_product_id ON demand_forecasts(product_id);
CREATE INDEX idx_demand_forecasts_retailer_id ON demand_forecasts(retailer_id);
CREATE INDEX idx_demand_forecasts_date ON demand_forecasts(forecast_date);
CREATE INDEX idx_demand_forecasts_period ON demand_forecasts(forecast_period_start, forecast_period_end);

-- Supply chain events indexes
CREATE INDEX idx_supply_chain_events_type ON supply_chain_events(event_type);
CREATE INDEX idx_supply_chain_events_dates ON supply_chain_events(start_date, end_date);
CREATE INDEX idx_supply_chain_events_severity ON supply_chain_events(severity);

-- Shipping indexes
CREATE INDEX idx_shipping_origin_warehouse_id ON shipping(origin_warehouse_id);
CREATE INDEX idx_shipping_product_id ON shipping(product_id);
CREATE INDEX idx_shipping_dates ON shipping(ship_date, expected_arrival_date);
CREATE INDEX idx_shipping_status ON shipping(status);

COPY warehouses FROM '/docker-entrypoint-initdb.d/warehouses.csv' WITH (FORMAT csv, HEADER true);
COPY inventory FROM '/docker-entrypoint-initdb.d/inventory.csv' WITH (FORMAT csv, HEADER true);
COPY retailers_copy FROM '/docker-entrypoint-initdb.d/retailers.csv' WITH (FORMAT csv, HEADER true);
COPY product_categories_copy FROM '/docker-entrypoint-initdb.d/product_categories.csv' WITH (FORMAT csv, HEADER true);
COPY products_copy FROM '/docker-entrypoint-initdb.d/products.csv' WITH (FORMAT csv, HEADER true);
COPY availability FROM '/docker-entrypoint-initdb.d/availability.csv' WITH (FORMAT csv, HEADER true);
COPY assortment FROM '/docker-entrypoint-initdb.d/assortment.csv' WITH (FORMAT csv, HEADER true);
COPY demand_forecasts FROM '/docker-entrypoint-initdb.d/demand_forecasts.csv' WITH (FORMAT csv, HEADER true);
COPY supply_chain_events FROM '/docker-entrypoint-initdb.d/supply_chain_events.csv' WITH (FORMAT csv, HEADER true);
COPY shipping FROM '/docker-entrypoint-initdb.d/shipping.csv' WITH (FORMAT csv, HEADER true);
