CREATE DATABASE customer;

\c customer;

-- Table for storing customer information
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    phone_number VARCHAR(20) UNIQUE,
    address VARCHAR(255),
    city VARCHAR(255),
    state VARCHAR(255),
    postcode VARCHAR(255),
    country VARCHAR(255),
    dob DATE,
    image VARCHAR(30),
    segment VARCHAR(30),
    auth_user_id INTEGER,
    satisfaction_score INTEGER CHECK (satisfaction_score BETWEEN 1 AND 10),
    last_survey_date DATE,
    churn_risk DECIMAL(3,2) CHECK (churn_risk BETWEEN 0 AND 1),
    churn_risk_factors TEXT[]
);

-- Table for storing plans and services
CREATE TABLE plans (
    plan_id SERIAL PRIMARY KEY,
    plan_name VARCHAR(50) UNIQUE,
    description TEXT,
    type TEXT,
    monthly_fee DECIMAL(10, 2),
    sf_record VARCHAR(18),
    data_limit_gb INTEGER,
    voice_limit_minutes INTEGER,
    sms_limit INTEGER,
    international_roaming BOOLEAN DEFAULT FALSE,
    roaming_countries TEXT[],
    roaming_data_gb DECIMAL(10, 2),
    roaming_voice_minutes INTEGER
);

-- Table for associating customers with plans
CREATE TABLE customer_plans (
    customer_plan_id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customers(customer_id),
    plan_id INT REFERENCES plans(plan_id),
    start_date DATE,
    end_date DATE,
    cell_number VARCHAR(10),
    status VARCHAR(10) CHECK (status IN ('active', 'inactive', 'activating')),
    data_allocation_gb INTEGER,
    data_used_gb DECIMAL(10, 2) DEFAULT 0,
    rollover_data_gb DECIMAL(10, 2) DEFAULT 0
);

-- Table for storing billing information
CREATE TABLE billing (
    billing_id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customers(customer_id),
    billing_date DATE,
    total_amount DECIMAL(10, 2),
    payment_status VARCHAR(20) -- e.g., paid, overdue, pending
);

-- Table for network infrastructure
CREATE TABLE network (
    node_id SERIAL PRIMARY KEY,
    node_name VARCHAR(255),
    latitude DECIMAL(9,6),
    longitude DECIMAL(9,6),
    capacity INTEGER,
    status VARCHAR(50),
    quality VARCHAR(50)
);

-- Table for associating customers with network nodes
CREATE TABLE customer_network (
    customer_id INT REFERENCES customers(customer_id),
    node_id INT REFERENCES network(node_id),
    PRIMARY KEY (customer_id, node_id)
);

-- Table for credit card information
CREATE TABLE credit_cards (
    credit_card_id SERIAL PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    expiry DATE NOT NULL,
    cvv INT NOT NULL,
    number TEXT NOT NULL,
    customer_id INT REFERENCES customers(customer_id)
);

-- Table for storing phone information
CREATE TABLE devices (
    device_id SERIAL PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    brand VARCHAR(50) NOT NULL,
    model VARCHAR(50) NOT NULL,
    image VARCHAR(50),
    sf_record VARCHAR(18)
);

-- Table for associating phones with customers
CREATE TABLE customer_plan_devices (
    customer_plan_id INT REFERENCES customer_plans(customer_plan_id),
    device_id INT REFERENCES devices(device_id),
    sim_iccid VARCHAR(24),
    device_imei VARCHAR(16),
    PRIMARY KEY (customer_plan_id, device_id)
);

-- Table for linking customer records in pg to non-pg dbs
CREATE TABLE customer_link (
    id SERIAL PRIMARY KEY,
    customer_id INT UNIQUE REFERENCES customers(customer_id),
    customer_guid UUID NOT NULL
);

-- Table for storing deals based on customer segment
CREATE TABLE deals (
    deal_id SERIAL PRIMARY KEY,
    deal_name VARCHAR(255),
    description TEXT,
    customer_segment VARCHAR(50),
    min_monthly_spend DECIMAL(10, 2),
    max_monthly_spend DECIMAL(10, 2),
    start_date DATE,
    end_date DATE,
    additional_benefits TEXT,
    terms_conditions TEXT
);

-- Table for tracking customer service interactions
CREATE TABLE service_interactions (
    interaction_id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(customer_id),
    interaction_date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    channel VARCHAR(20) CHECK (channel IN ('phone', 'chat', 'email', 'store', 'social')),
    category VARCHAR(50) CHECK (category IN ('technical', 'billing', 'account', 'plan', 'device', 'coverage')),
    resolution_status VARCHAR(20) CHECK (resolution_status IN ('resolved', 'pending', 'escalated')),
    satisfaction_score INTEGER CHECK (satisfaction_score BETWEEN 1 AND 10),
    agent_id INTEGER,
    resolution_time_minutes INTEGER,
    notes TEXT
);

-- Table for tracking customer interactions across channels
CREATE TABLE interactions (
    interaction_id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(customer_id),
    channel VARCHAR(50) NOT NULL, -- e.g., 'call', 'chat', 'email', 'store'
    agent_id INTEGER,
    interaction_time TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    duration_seconds INTEGER,
    topic VARCHAR(100),
    resolution_status VARCHAR(50),
    satisfaction_rating INTEGER CHECK (satisfaction_rating BETWEEN 1 AND 5),
    notes TEXT
);

-- Table for tracking number portability
CREATE TABLE number_portability (
    portability_id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(customer_id),
    phone_number VARCHAR(20) UNIQUE,
    previous_carrier VARCHAR(100),
    port_date TIMESTAMP WITH TIME ZONE,
    status VARCHAR(20) CHECK (status IN ('requested', 'in_progress', 'completed', 'failed')),
    completion_date TIMESTAMP WITH TIME ZONE,
    notes TEXT
);

-- Table for tracking VoIP services
CREATE TABLE voip_services (
    voip_id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(customer_id),
    service_number VARCHAR(20),
    service_type VARCHAR(50),
    monthly_fee DECIMAL(10, 2),
    features TEXT[],
    activation_date DATE,
    status VARCHAR(20) CHECK (status IN ('active', 'suspended', 'terminated'))
);

-- Table for tracking IoT devices
CREATE TABLE iot_devices (
    iot_device_id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(customer_id),
    device_type VARCHAR(50),
    imei VARCHAR(15),
    sim_iccid VARCHAR(24),
    data_plan_id INTEGER REFERENCES plans(plan_id),
    activation_date DATE,
    last_active_date TIMESTAMP WITH TIME ZONE,
    monthly_data_usage_mb DECIMAL(10, 2),
    status VARCHAR(20) CHECK (status IN ('active', 'inactive', 'suspended'))
);

-- Table for a referral tracking system
CREATE TABLE referrals (
    referral_id SERIAL PRIMARY KEY,
    referrer_id INTEGER REFERENCES customers(customer_id),
    referred_id INTEGER REFERENCES customers(customer_id),
    referral_date DATE NOT NULL,
    status VARCHAR(20) CHECK (status IN ('pending', 'accepted', 'expired')),
    bonus_amount DECIMAL(10, 2),
    bonus_paid BOOLEAN DEFAULT FALSE
);

-- Table for tracking device upgrades and trade-ins
CREATE TABLE device_upgrades (
    upgrade_id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(customer_id),
    old_device_id INTEGER REFERENCES devices(device_id),
    new_device_id INTEGER REFERENCES devices(device_id),
    upgrade_date DATE NOT NULL,
    trade_in_value DECIMAL(10, 2),
    contract_extension_months INTEGER,
    promotion_applied VARCHAR(100)
);

-- Table for family plans and shared accounts
CREATE TABLE family_plans (
    family_plan_id SERIAL PRIMARY KEY,
    primary_customer_id INTEGER REFERENCES customers(customer_id),
    plan_name VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    max_members INTEGER,
    shared_data_gb INTEGER,
    monthly_fee DECIMAL(10, 2)
);

CREATE TABLE family_plan_members (
    family_plan_id INTEGER REFERENCES family_plans(family_plan_id),
    customer_id INTEGER REFERENCES customers(customer_id),
    role VARCHAR(20) CHECK (role IN ('primary', 'secondary', 'child')),
    data_allocation_percentage INTEGER,
    PRIMARY KEY (family_plan_id, customer_id)
);

-- Table for tracking customer loyalty rewards
CREATE TABLE loyalty_rewards (
    reward_id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(customer_id),
    points_earned INTEGER NOT NULL,
    points_redeemed INTEGER DEFAULT 0,
    points_balance INTEGER,
    last_activity_date DATE,
    tier VARCHAR(20) CHECK (tier IN ('bronze', 'silver', 'gold', 'platinum'))
);

-- Table for tracking promotional campaigns
CREATE TABLE campaigns (
    campaign_id SERIAL PRIMARY KEY,
    campaign_name VARCHAR(100) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE,
    target_segment VARCHAR(50),
    channel VARCHAR(50),
    offer_details TEXT,
    budget DECIMAL(10, 2),
    conversion_goal INTEGER,
    actual_conversions INTEGER
);

-- Table for tracking customer feedback
CREATE TABLE feedback (
    feedback_id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(customer_id),
    feedback_date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    category VARCHAR(50),
    rating INTEGER CHECK (rating BETWEEN 1 AND 10),
    comments TEXT,
    requires_followup BOOLEAN DEFAULT FALSE,
    followup_notes TEXT,
    followup_date TIMESTAMP WITH TIME ZONE
);

-- Import data from CSV files
\COPY customers FROM '/docker-entrypoint-initdb.d/customers.csv' WITH (FORMAT csv, HEADER true);
\COPY plans FROM '/docker-entrypoint-initdb.d/plans.csv' WITH (FORMAT csv, HEADER true);
\COPY devices FROM '/docker-entrypoint-initdb.d/devices.csv' WITH (FORMAT csv, HEADER true);
\COPY network FROM '/docker-entrypoint-initdb.d/network_nodes.csv' WITH (FORMAT csv, HEADER true);
\COPY customer_plans FROM '/docker-entrypoint-initdb.d/customer_plans.csv' WITH (FORMAT csv, HEADER true);
\COPY customer_plan_devices FROM '/docker-entrypoint-initdb.d/customer_plan_devices.csv' WITH (FORMAT csv, HEADER true);
\COPY customer_network FROM '/docker-entrypoint-initdb.d/customer_network.csv' WITH (FORMAT csv, HEADER true);
\COPY billing FROM '/docker-entrypoint-initdb.d/billing.csv' WITH (FORMAT csv, HEADER true);
\COPY credit_cards FROM '/docker-entrypoint-initdb.d/credit_cards.csv' WITH (FORMAT csv, HEADER true);
\COPY customer_link FROM '/docker-entrypoint-initdb.d/customer_link.csv' WITH (FORMAT csv, HEADER true);
\COPY deals FROM '/docker-entrypoint-initdb.d/deals.csv' WITH (FORMAT csv, HEADER true);
\COPY service_interactions FROM '/docker-entrypoint-initdb.d/service_interactions.csv' WITH (FORMAT csv, HEADER true);
\COPY interactions FROM '/docker-entrypoint-initdb.d/interactions.csv' WITH (FORMAT csv, HEADER true);
\COPY number_portability FROM '/docker-entrypoint-initdb.d/number_portability.csv' WITH (FORMAT csv, HEADER true);
\COPY voip_services FROM '/docker-entrypoint-initdb.d/voip_services.csv' WITH (FORMAT csv, HEADER true);
\COPY iot_devices FROM '/docker-entrypoint-initdb.d/iot_devices.csv' WITH (FORMAT csv, HEADER true);
\COPY referrals FROM '/docker-entrypoint-initdb.d/referrals.csv' WITH (FORMAT csv, HEADER true);
\COPY device_upgrades FROM '/docker-entrypoint-initdb.d/device_upgrades.csv' WITH (FORMAT csv, HEADER true);
\COPY family_plans FROM '/docker-entrypoint-initdb.d/family_plans.csv' WITH (FORMAT csv, HEADER true);
\COPY family_plan_members FROM '/docker-entrypoint-initdb.d/family_plan_members.csv' WITH (FORMAT csv, HEADER true);
\COPY loyalty_rewards FROM '/docker-entrypoint-initdb.d/loyalty_rewards.csv' WITH (FORMAT csv, HEADER true);
\COPY campaigns FROM '/docker-entrypoint-initdb.d/campaigns.csv' WITH (FORMAT csv, HEADER true);
\COPY feedback FROM '/docker-entrypoint-initdb.d/feedback.csv' WITH (FORMAT csv, HEADER true);
