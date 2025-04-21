-- SCHEMA
CREATE SCHEMA us;
SET search_path TO us;

-- SCHEMA SETUP
CREATE TABLE Suppliers (
    supplier_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    contact_email VARCHAR(100),
    country VARCHAR(50)
);

CREATE TABLE RawMaterials (
    material_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    unit VARCHAR(20),
    cost_per_unit NUMERIC(10,2)
);

CREATE TABLE SupplierMaterials (
    supplier_id INTEGER REFERENCES Suppliers(supplier_id),
    material_id INTEGER REFERENCES RawMaterials(material_id),
    lead_time_days INTEGER,
    PRIMARY KEY (supplier_id, material_id)
);

CREATE TABLE Factories (
    factory_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    location VARCHAR(100),
    capacity INTEGER -- max units per month
);

CREATE TABLE Shoes (
    shoe_id SERIAL PRIMARY KEY,
    model_name VARCHAR(100),
    category VARCHAR(50), -- running, casual, hiking, etc.
    release_date DATE
);

CREATE TABLE BillOfMaterials (
    shoe_id INTEGER REFERENCES Shoes(shoe_id),
    material_id INTEGER REFERENCES RawMaterials(material_id),
    quantity_required NUMERIC(10,2),
    PRIMARY KEY (shoe_id, material_id)
);

CREATE TABLE ProductionOrders (
    order_id SERIAL PRIMARY KEY,
    shoe_id INTEGER REFERENCES Shoes(shoe_id),
    factory_id INTEGER REFERENCES Factories(factory_id),
    quantity INTEGER,
    start_date DATE,
    expected_completion DATE
);

CREATE TABLE Warehouses (
    warehouse_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    location VARCHAR(100)
);

CREATE TABLE Shipments (
    shipment_id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES ProductionOrders(order_id),
    warehouse_id INTEGER REFERENCES Warehouses(warehouse_id),
    shipped_date DATE,
    arrival_date DATE,
    quantity INTEGER
);
