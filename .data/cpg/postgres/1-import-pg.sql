CREATE DATABASE sales;

\c sales;

CREATE TABLE brands (
    brand_id SERIAL PRIMARY KEY,
    brand_name VARCHAR(100) NOT NULL,
    parent_company VARCHAR(100),
    brand_tier VARCHAR(50) CHECK (brand_tier IN ('Premium', 'Mainstream', 'Value', 'Private Label')),
    category_focus VARCHAR(100),
    year_established INT,
    is_active BOOLEAN DEFAULT TRUE
);

CREATE TABLE product_categories (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL,
    parent_category_id INT REFERENCES product_categories(category_id),
    category_description TEXT,
    is_seasonal BOOLEAN DEFAULT FALSE,
    typical_margin_percentage DECIMAL(5,2)
);

CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    product_sku VARCHAR(50) UNIQUE NOT NULL,
    product_name VARCHAR(200) NOT NULL,
    brand_id INT REFERENCES brands(brand_id),
    category_id INT REFERENCES product_categories(category_id),
    subcategory_id INT REFERENCES product_categories(category_id),
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

CREATE TABLE competitors (
    competitor_id SERIAL PRIMARY KEY,
    competitor_name VARCHAR(100) NOT NULL,
    competitor_type VARCHAR(50) CHECK (competitor_type IN ('Direct', 'Indirect', 'Private Label')),
    primary_categories TEXT[],
    notes TEXT
);

CREATE TABLE competitor_products (
    competitor_product_id SERIAL PRIMARY KEY,
    competitor_id INT REFERENCES competitors(competitor_id),
    product_name VARCHAR(200) NOT NULL,
    category_id INT REFERENCES product_categories(category_id),
    estimated_price DECIMAL(10,2),
    notes TEXT
);

CREATE TABLE channels (
    channel_id SERIAL PRIMARY KEY,
    channel_name VARCHAR(100) NOT NULL,
    channel_type VARCHAR(50) CHECK (channel_type IN ('Grocery', 'Mass Merchant', 'Club', 'Convenience', 'Drug', 'E-commerce', 'Specialty', 'Food Service')),
    is_direct_to_consumer BOOLEAN DEFAULT FALSE,
    is_online BOOLEAN DEFAULT FALSE,
    region VARCHAR(100),
    distribution_cost_percentage DECIMAL(5,2)
);

CREATE TABLE retailers (
    retailer_id SERIAL PRIMARY KEY,
    retailer_name VARCHAR(100) NOT NULL,
    channel_id INT REFERENCES channels(channel_id),
    sales_region VARCHAR(100),
    has_ecommerce BOOLEAN DEFAULT FALSE,
    annual_revenue_tier VARCHAR(50),
    account_tier VARCHAR(50) CHECK (account_tier IN ('Strategic', 'Key', 'Core', 'Small'))
);

CREATE TABLE sales_transactions (
    transaction_id SERIAL PRIMARY KEY,
    product_id INT REFERENCES products(product_id),
    retailer_id INT REFERENCES retailers(retailer_id),
    transaction_date DATE NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    is_promoted BOOLEAN DEFAULT FALSE,
    discount_percentage DECIMAL(5,2) DEFAULT 0,
    is_online_sale BOOLEAN DEFAULT FALSE
);

CREATE TABLE market_shares (
    share_id SERIAL PRIMARY KEY,
    category_id INT REFERENCES product_categories(category_id),
    brand_id INT REFERENCES brands(brand_id),
    channel_id INT REFERENCES channels(channel_id),
    report_date DATE NOT NULL,
    share_percentage DECIMAL(5,2) NOT NULL,
    volume_share_percentage DECIMAL(5,2),
    dollar_sales DECIMAL(12,2),
    volume_sales DECIMAL(12,2),
    measurement_period VARCHAR(50) CHECK (measurement_period IN ('Weekly', 'Monthly', 'Quarterly', 'Yearly')),
    data_source VARCHAR(100)
);

CREATE TABLE promotions (
    promotion_id SERIAL PRIMARY KEY,
    promotion_name VARCHAR(200) NOT NULL,
    promotion_type VARCHAR(50) CHECK (promotion_type IN ('Price Discount', 'BOGO', 'Bundle', 'Display', 'Feature', 'TPR', 'Digital Coupon')),
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    discount_value DECIMAL(10,2),
    discount_type VARCHAR(20) CHECK (discount_type IN ('Percentage', 'Fixed Amount', 'Free Item')),
    min_purchase_qty INT DEFAULT 1,
    budget DECIMAL(12,2),
    channel_id INT REFERENCES channels(channel_id),
    notes TEXT
);

CREATE TABLE promotion_products (
    promotion_id INT REFERENCES promotions(promotion_id),
    product_id INT REFERENCES products(product_id),
    PRIMARY KEY (promotion_id, product_id)
);

CREATE TABLE pricing_history (
    pricing_id SERIAL PRIMARY KEY,
    product_id INT REFERENCES products(product_id),
    retailer_id INT REFERENCES retailers(retailer_id),
    effective_date DATE NOT NULL,
    end_date DATE,
    base_price DECIMAL(10,2) NOT NULL,
    promotion_id INT REFERENCES promotions(promotion_id),
    actual_price DECIMAL(10,2) NOT NULL
);

-- Create indexes for better query performance
-- Brands indexes
CREATE INDEX idx_brands_name ON brands(brand_name);
CREATE INDEX idx_brands_tier ON brands(brand_tier);
CREATE INDEX idx_brands_category_focus ON brands(category_focus);

-- Product categories indexes
CREATE INDEX idx_product_categories_name ON product_categories(category_name);
CREATE INDEX idx_product_categories_parent ON product_categories(parent_category_id);

-- Products indexes
CREATE INDEX idx_products_brand_id ON products(brand_id);
CREATE INDEX idx_products_category_id ON products(category_id);
CREATE INDEX idx_products_subcategory_id ON products(subcategory_id);
CREATE INDEX idx_products_launch_date ON products(launch_date);

-- Competitors indexes
CREATE INDEX idx_competitors_name ON competitors(competitor_name);
CREATE INDEX idx_competitors_type ON competitors(competitor_type);

-- Competitor products indexes
CREATE INDEX idx_competitor_products_competitor_id ON competitor_products(competitor_id);
CREATE INDEX idx_competitor_products_category_id ON competitor_products(category_id);

-- Channels indexes
CREATE INDEX idx_channels_name ON channels(channel_name);
CREATE INDEX idx_channels_type ON channels(channel_type);

-- Retailers indexes
CREATE INDEX idx_retailers_name ON retailers(retailer_name);
CREATE INDEX idx_retailers_channel_id ON retailers(channel_id);
CREATE INDEX idx_retailers_region ON retailers(sales_region);

-- Sales transactions indexes
CREATE INDEX idx_sales_transactions_product_id ON sales_transactions(product_id);
CREATE INDEX idx_sales_transactions_retailer_id ON sales_transactions(retailer_id);
CREATE INDEX idx_sales_transactions_date ON sales_transactions(transaction_date);
CREATE INDEX idx_sales_transactions_promoted ON sales_transactions(is_promoted);

-- Market shares indexes
CREATE INDEX idx_market_shares_category_id ON market_shares(category_id);
CREATE INDEX idx_market_shares_brand_id ON market_shares(brand_id);
CREATE INDEX idx_market_shares_channel_id ON market_shares(channel_id);
CREATE INDEX idx_market_shares_report_date ON market_shares(report_date);

-- Promotions indexes
CREATE INDEX idx_promotions_type ON promotions(promotion_type);
CREATE INDEX idx_promotions_dates ON promotions(start_date, end_date);
CREATE INDEX idx_promotions_channel_id ON promotions(channel_id);

-- Pricing history indexes
CREATE INDEX idx_pricing_history_product_id ON pricing_history(product_id);
CREATE INDEX idx_pricing_history_retailer_id ON pricing_history(retailer_id);
CREATE INDEX idx_pricing_history_effective_date ON pricing_history(effective_date);
CREATE INDEX idx_pricing_history_promotion_id ON pricing_history(promotion_id);

COPY brands FROM '/docker-entrypoint-initdb.d/brands.csv' WITH (FORMAT csv, HEADER true);
COPY product_categories FROM '/docker-entrypoint-initdb.d/product_categories.csv' WITH (FORMAT csv, HEADER true);
COPY products FROM '/docker-entrypoint-initdb.d/products.csv' WITH (FORMAT csv, HEADER true);
COPY competitors FROM '/docker-entrypoint-initdb.d/competitors.csv' WITH (FORMAT csv, HEADER true);
COPY channels FROM '/docker-entrypoint-initdb.d/channels.csv' WITH (FORMAT csv, HEADER true);
COPY retailers FROM '/docker-entrypoint-initdb.d/retailers.csv' WITH (FORMAT csv, HEADER true);
COPY sales_transactions FROM '/docker-entrypoint-initdb.d/sales_transactions.csv' WITH (FORMAT csv, HEADER true);
COPY market_shares FROM '/docker-entrypoint-initdb.d/market_shares.csv' WITH (FORMAT csv, HEADER true);
COPY promotions FROM '/docker-entrypoint-initdb.d/promotions.csv' WITH (FORMAT csv, HEADER true);
COPY promotion_products FROM '/docker-entrypoint-initdb.d/promotion_products.csv' WITH (FORMAT csv, HEADER true);
