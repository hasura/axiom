CREATE DATABASE network;

\c network;

CREATE TABLE Calls (
    CallID SERIAL PRIMARY KEY,
    CustomerID INT NOT NULL,
    DeviceID INT NOT NULL,
    TimeStamp TIMESTAMP WITH TIME ZONE NOT NULL,
    Duration INT NOT NULL,
    CallType VARCHAR(50),
    ReceiverNumber VARCHAR(15),
    NodeId INT,
    latitude DECIMAL(9,6),
    longitude DECIMAL(9,6)
);

CREATE TABLE Texts (
    TextID SERIAL PRIMARY KEY,
    CustomerID INT NOT NULL,
    DeviceID INT NOT NULL,
    TimeStamp TIMESTAMP WITH TIME ZONE NOT NULL,
    MessageType VARCHAR(50),
    ReceiverNumber VARCHAR(15),
    NodeId Int,
    latitude DECIMAL(9,6),
    longitude DECIMAL(9,6)
);

-- Add network coverage areas table
CREATE TABLE coverage_areas (
    coverage_id SERIAL PRIMARY KEY,
    node_id INTEGER,
    technology VARCHAR(10) CHECK (technology IN ('2G', '3G', '4G', '5G')),
    coverage_radius_km DECIMAL(10, 2),
    population_covered INTEGER,
    terrain_type VARCHAR(50),
    signal_strength_dbm INTEGER,
    last_upgraded DATE
);

-- Add network equipment inventory
CREATE TABLE equipment (
    equipment_id SERIAL PRIMARY KEY,
    node_id INTEGER,
    equipment_type VARCHAR(50),
    manufacturer VARCHAR(100),
    model VARCHAR(100),
    serial_number VARCHAR(100),
    installation_date DATE,
    last_maintenance_date DATE,
    firmware_version VARCHAR(50),
    status VARCHAR(20) CHECK (status IN ('active', 'maintenance', 'offline', 'decommissioned')),
    capacity_mbps INTEGER,
    power_consumption_watts INTEGER
);

-- Add spectrum licenses table
CREATE TABLE spectrum_licenses (
    license_id SERIAL PRIMARY KEY,
    frequency_band VARCHAR(20),
    bandwidth_mhz DECIMAL(10, 2),
    geographic_area VARCHAR(100),
    acquisition_date DATE,
    expiration_date DATE,
    cost_million_usd DECIMAL(10, 2),
    regulatory_authority VARCHAR(100),
    license_number VARCHAR(50)
);

-- Add table for tracking network issues and outages
CREATE TABLE outages (
    outage_id SERIAL PRIMARY KEY,
    node_id INTEGER,
    start_time TIMESTAMP WITH TIME ZONE NOT NULL,
    end_time TIMESTAMP WITH TIME ZONE,
    affected_customers INTEGER,
    severity VARCHAR(20) CHECK (severity IN ('minor', 'major', 'critical')),
    cause VARCHAR(100),
    resolution TEXT
);

\COPY Calls FROM '/docker-entrypoint-initdb.d/calls.csv' WITH (FORMAT csv, HEADER true);
\COPY Texts FROM '/docker-entrypoint-initdb.d/texts.csv' WITH (FORMAT csv, HEADER true);
\COPY coverage_areas FROM '/docker-entrypoint-initdb.d/coverage_areas.csv' WITH (FORMAT csv, HEADER true);
\COPY equipment FROM '/docker-entrypoint-initdb.d/equipment.csv' WITH (FORMAT csv, HEADER true);
\COPY spectrum_licenses FROM '/docker-entrypoint-initdb.d/spectrum_licenses.csv' WITH (FORMAT csv, HEADER true);
\COPY outages FROM '/docker-entrypoint-initdb.d/outages.csv' WITH (FORMAT csv, HEADER true);
