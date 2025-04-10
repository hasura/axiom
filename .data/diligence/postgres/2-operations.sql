CREATE DATABASE operations;

\c operations;

-- Regions
CREATE TABLE regions (
    region_id SERIAL PRIMARY KEY,
    region_name VARCHAR(50) NOT NULL,
    country VARCHAR(50) NOT NULL,
    currency_code CHAR(3) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Business Units
CREATE TABLE business_units (
    unit_id SERIAL PRIMARY KEY,
    unit_name VARCHAR(100) NOT NULL,
    unit_code VARCHAR(20) NOT NULL UNIQUE,
    region_id INTEGER NOT NULL REFERENCES regions(region_id),
    director VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    established_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Customers
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    business_name VARCHAR(100) NOT NULL,
    industry VARCHAR(50),
    business_type VARCHAR(30) CHECK (business_type IN ('B2B', 'B2C', 'Government', 'Non-profit')),
    region_id INTEGER NOT NULL REFERENCES regions(region_id),
    acquisition_date DATE NOT NULL,
    account_manager VARCHAR(100),
    credit_limit NUMERIC(15, 2),
    payment_terms VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE,
    total_lifetime_value NUMERIC(15, 2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_customers_region ON customers(region_id);
CREATE INDEX idx_customers_industry ON customers(industry);

-- Customer Contacts
CREATE TABLE customer_contacts (
    contact_id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(customer_id),
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    job_title VARCHAR(100),
    email VARCHAR(100) NOT NULL,
    phone VARCHAR(30),
    is_primary BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_contact_customer ON customer_contacts(customer_id);

-- Product Categories
CREATE TABLE product_categories (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL,
    parent_category_id INTEGER REFERENCES product_categories(category_id),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Products
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    product_code VARCHAR(30) NOT NULL UNIQUE,
    product_name VARCHAR(100) NOT NULL,
    category_id INTEGER NOT NULL REFERENCES product_categories(category_id),
    unit_id INTEGER NOT NULL REFERENCES business_units(unit_id),
    description TEXT,
    launch_date DATE,
    base_cost NUMERIC(15, 2) NOT NULL,
    list_price NUMERIC(15, 2) NOT NULL,
    status VARCHAR(20) CHECK (status IN ('Development', 'Active', 'Discontinued')),
    minimum_order_quantity INTEGER DEFAULT 1,
    reorder_point INTEGER,
    target_inventory_level INTEGER,
    lead_time_days INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_product_category ON products(category_id);
CREATE INDEX idx_product_unit ON products(unit_id);

-- Inventory
CREATE TABLE inventory (
    inventory_id SERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES products(product_id),
    warehouse_location VARCHAR(100) NOT NULL,
    quantity_on_hand INTEGER NOT NULL,
    quantity_allocated INTEGER DEFAULT 0,
    restock_threshold INTEGER NOT NULL,
    last_restock_date DATE,
    next_restock_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (product_id, warehouse_location)
);
CREATE INDEX idx_inventory_product ON inventory(product_id);

-- Inventory Movement Log
CREATE TABLE inventory_movements (
    movement_id SERIAL PRIMARY KEY,
    inventory_id INTEGER NOT NULL REFERENCES inventory(inventory_id),
    transaction_date TIMESTAMP NOT NULL,
    transaction_type VARCHAR(20) CHECK (transaction_type IN ('Restock', 'Sale', 'Return', 'Adjustment', 'Transfer')),
    quantity INTEGER NOT NULL,
    reference_document VARCHAR(50),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_inv_movement_inventory ON inventory_movements(inventory_id);
CREATE INDEX idx_inv_movement_date ON inventory_movements(transaction_date);

-- Suppliers
CREATE TABLE suppliers (
    supplier_id SERIAL PRIMARY KEY,
    supplier_name VARCHAR(100) NOT NULL,
    contact_name VARCHAR(100),
    contact_email VARCHAR(100),
    contact_phone VARCHAR(30),
    address TEXT,
    country VARCHAR(50),
    supplier_rating INTEGER CHECK (supplier_rating BETWEEN 1 AND 5),
    primary_category VARCHAR(50),
    payment_terms VARCHAR(50),
    lead_time_days INTEGER,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Purchase Orders
CREATE TABLE purchase_orders (
    po_id SERIAL PRIMARY KEY,
    po_number VARCHAR(30) NOT NULL UNIQUE,
    supplier_id INTEGER NOT NULL REFERENCES suppliers(supplier_id),
    order_date DATE NOT NULL,
    expected_delivery_date DATE,
    actual_delivery_date DATE,
    total_amount NUMERIC(15, 2) NOT NULL,
    status VARCHAR(20) CHECK (status IN ('Draft', 'Submitted', 'Approved', 'Shipped', 'Received', 'Cancelled')),
    payment_status VARCHAR(20) CHECK (payment_status IN ('Unpaid', 'Partially Paid', 'Paid')),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_po_supplier ON purchase_orders(supplier_id);
CREATE INDEX idx_po_dates ON purchase_orders(order_date, expected_delivery_date);

-- Purchase Order Items
CREATE TABLE po_items (
    item_id SERIAL PRIMARY KEY,
    po_id INTEGER NOT NULL REFERENCES purchase_orders(po_id),
    product_id INTEGER NOT NULL REFERENCES products(product_id),
    quantity INTEGER NOT NULL,
    unit_price NUMERIC(15, 2) NOT NULL,
    line_total NUMERIC(15, 2) NOT NULL,
    received_quantity INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_po_items_po ON po_items(po_id);
CREATE INDEX idx_po_items_product ON po_items(product_id);

-- Sales Orders
CREATE TABLE sales_orders (
    order_id SERIAL PRIMARY KEY,
    order_number VARCHAR(30) NOT NULL UNIQUE,
    customer_id INTEGER NOT NULL REFERENCES customers(customer_id),
    order_date DATE NOT NULL,
    required_date DATE,
    shipped_date DATE,
    ship_to_address TEXT,
    shipping_method VARCHAR(50),
    shipping_cost NUMERIC(15, 2) DEFAULT 0,
    sales_rep VARCHAR(100),
    unit_id INTEGER NOT NULL REFERENCES business_units(unit_id),
    subtotal NUMERIC(15, 2) NOT NULL,
    tax_amount NUMERIC(15, 2) DEFAULT 0,
    discount_amount NUMERIC(15, 2) DEFAULT 0,
    total_amount NUMERIC(15, 2) NOT NULL,
    status VARCHAR(20) CHECK (status IN ('New', 'Processing', 'Shipped', 'Delivered', 'Cancelled')),
    payment_status VARCHAR(20) CHECK (payment_status IN ('Unpaid', 'Partially Paid', 'Paid')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_orders_customer ON sales_orders(customer_id);
CREATE INDEX idx_orders_dates ON sales_orders(order_date, required_date, shipped_date);
CREATE INDEX idx_orders_unit ON sales_orders(unit_id);

-- Order Items
CREATE TABLE order_items (
    item_id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES sales_orders(order_id),
    product_id INTEGER NOT NULL REFERENCES products(product_id),
    quantity INTEGER NOT NULL,
    unit_price NUMERIC(15, 2) NOT NULL,
    discount_percentage NUMERIC(5, 2) DEFAULT 0,
    line_total NUMERIC(15, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_order_items_order ON order_items(order_id);
CREATE INDEX idx_order_items_product ON order_items(product_id);

-- Marketing Campaigns
CREATE TABLE marketing_campaigns (
    campaign_id SERIAL PRIMARY KEY,
    campaign_name VARCHAR(100) NOT NULL,
    campaign_type VARCHAR(50) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE,
    budget NUMERIC(15, 2) NOT NULL,
    actual_spend NUMERIC(15, 2),
    target_audience VARCHAR(100),
    target_region INTEGER REFERENCES regions(region_id),
    target_products TEXT,
    expected_revenue NUMERIC(15, 2),
    actual_revenue NUMERIC(15, 2),
    roi_percentage NUMERIC(8, 2),
    status VARCHAR(20) CHECK (status IN ('Planning', 'Active', 'Completed', 'Cancelled')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_campaigns_dates ON marketing_campaigns(start_date, end_date);
CREATE INDEX idx_campaigns_region ON marketing_campaigns(target_region);

-- Import data from CSVs
\copy regions(region_id, region_name, country, currency_code) FROM '/docker-entrypoint-initdb.d/regions.csv' DELIMITER ',' CSV HEADER;
\copy business_units(unit_id, unit_name, unit_code, region_id, director, is_active, established_date) FROM '/docker-entrypoint-initdb.d/business_units.csv' DELIMITER ',' CSV HEADER;
\copy customers(customer_id, business_name, industry, business_type, region_id, acquisition_date, account_manager, credit_limit, payment_terms, is_active, total_lifetime_value) FROM '/docker-entrypoint-initdb.d/customers.csv' DELIMITER ',' CSV HEADER;
\copy customer_contacts(contact_id, customer_id, first_name, last_name, job_title, email, phone, is_primary) FROM '/docker-entrypoint-initdb.d/customer_contacts.csv' DELIMITER ',' CSV HEADER;
\copy product_categories(category_id, category_name, parent_category_id, description) FROM '/docker-entrypoint-initdb.d/product_categories.csv' DELIMITER ',' CSV HEADER;
\copy products(product_id, product_code, product_name, category_id, unit_id, description, launch_date, base_cost, list_price, status, minimum_order_quantity, reorder_point, target_inventory_level, lead_time_days) FROM '/docker-entrypoint-initdb.d/products.csv' DELIMITER ',' CSV HEADER;
\copy inventory(inventory_id, product_id, warehouse_location, quantity_on_hand, quantity_allocated, restock_threshold, last_restock_date, next_restock_date) FROM '/docker-entrypoint-initdb.d/inventory.csv' DELIMITER ',' CSV HEADER;
\copy inventory_movements(movement_id, inventory_id, transaction_date, transaction_type, quantity, reference_document, notes) FROM '/docker-entrypoint-initdb.d/inventory_movements.csv' DELIMITER ',' CSV HEADER;
\copy suppliers(supplier_id, supplier_name, contact_name, contact_email, contact_phone, address, country, supplier_rating, primary_category, payment_terms, lead_time_days, is_active) FROM '/docker-entrypoint-initdb.d/suppliers.csv' DELIMITER ',' CSV HEADER;
\copy purchase_orders(po_id, po_number, supplier_id, order_date, expected_delivery_date, actual_delivery_date, total_amount, status, payment_status, notes) FROM '/docker-entrypoint-initdb.d/purchase_orders.csv' DELIMITER ',' CSV HEADER;
\copy po_items(item_id, po_id, product_id, quantity, unit_price, line_total, received_quantity) FROM '/docker-entrypoint-initdb.d/po_items.csv' DELIMITER ',' CSV HEADER;
\copy sales_orders(order_id, order_number, customer_id, order_date, required_date, shipped_date, ship_to_address, shipping_method, shipping_cost, sales_rep, unit_id, subtotal, tax_amount, discount_amount, total_amount, status, payment_status) FROM '/docker-entrypoint-initdb.d/sales_orders.csv' DELIMITER ',' CSV HEADER;
\copy order_items(item_id, order_id, product_id, quantity, unit_price, discount_percentage, line_total) FROM '/docker-entrypoint-initdb.d/order_items.csv' DELIMITER ',' CSV HEADER;
\copy marketing_campaigns(campaign_id, campaign_name, campaign_type, start_date, end_date, budget, actual_spend, target_audience, target_region, target_products, expected_revenue, actual_revenue, roi_percentage, status) FROM '/docker-entrypoint-initdb.d/marketing_campaigns.csv' DELIMITER ',' CSV HEADER;