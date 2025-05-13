
-- Create database if it doesn't exist
CREATE DATABASE scms;

\c scms;

--
-- PostgreSQL database dump
--

-- Dumped from database version 17.4 (Debian 17.4-1.pgdg120+2)
-- Dumped by pg_dump version 17.4 (Homebrew)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: us; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA us;


ALTER SCHEMA us OWNER TO "postgres";

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: billofmaterials; Type: TABLE; Schema: us; Owner: postgres
--

CREATE TABLE us.billofmaterials (
    shoe_id integer NOT NULL,
    material_id integer NOT NULL,
    quantity_required numeric(10,2)
);


ALTER TABLE us.billofmaterials OWNER TO "postgres";

--
-- Name: factories; Type: TABLE; Schema: us; Owner: postgres
--

CREATE TABLE us.factories (
    factory_id integer NOT NULL,
    name character varying(100),
    location character varying(100),
    capacity integer
);


ALTER TABLE us.factories OWNER TO "postgres";

--
-- Name: factories_factory_id_seq; Type: SEQUENCE; Schema: us; Owner: postgres
--

CREATE SEQUENCE us.factories_factory_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE us.factories_factory_id_seq OWNER TO "postgres";

--
-- Name: factories_factory_id_seq; Type: SEQUENCE OWNED BY; Schema: us; Owner: postgres
--

ALTER SEQUENCE us.factories_factory_id_seq OWNED BY us.factories.factory_id;


--
-- Name: productionorders; Type: TABLE; Schema: us; Owner: postgres
--

CREATE TABLE us.productionorders (
    order_id integer NOT NULL,
    shoe_id integer,
    factory_id integer,
    quantity integer,
    start_date date,
    expected_completion date
);


ALTER TABLE us.productionorders OWNER TO "postgres";

--
-- Name: productionorders_order_id_seq; Type: SEQUENCE; Schema: us; Owner: postgres
--

CREATE SEQUENCE us.productionorders_order_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE us.productionorders_order_id_seq OWNER TO "postgres";

--
-- Name: productionorders_order_id_seq; Type: SEQUENCE OWNED BY; Schema: us; Owner: postgres
--

ALTER SEQUENCE us.productionorders_order_id_seq OWNED BY us.productionorders.order_id;


--
-- Name: rawmaterials; Type: TABLE; Schema: us; Owner: postgres
--

CREATE TABLE us.rawmaterials (
    material_id integer NOT NULL,
    name character varying(100) NOT NULL,
    unit character varying(20),
    cost_per_unit numeric(10,2)
);


ALTER TABLE us.rawmaterials OWNER TO "postgres";

--
-- Name: rawmaterials_material_id_seq; Type: SEQUENCE; Schema: us; Owner: postgres
--

CREATE SEQUENCE us.rawmaterials_material_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE us.rawmaterials_material_id_seq OWNER TO "postgres";

--
-- Name: rawmaterials_material_id_seq; Type: SEQUENCE OWNED BY; Schema: us; Owner: postgres
--

ALTER SEQUENCE us.rawmaterials_material_id_seq OWNED BY us.rawmaterials.material_id;


--
-- Name: shipments; Type: TABLE; Schema: us; Owner: postgres
--

CREATE TABLE us.shipments (
    shipment_id integer NOT NULL,
    order_id integer,
    warehouse_id integer,
    shipped_date date,
    arrival_date date,
    quantity integer
);


ALTER TABLE us.shipments OWNER TO "postgres";

--
-- Name: shipments_shipment_id_seq; Type: SEQUENCE; Schema: us; Owner: postgres
--

CREATE SEQUENCE us.shipments_shipment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE us.shipments_shipment_id_seq OWNER TO "postgres";

--
-- Name: shipments_shipment_id_seq; Type: SEQUENCE OWNED BY; Schema: us; Owner: postgres
--

ALTER SEQUENCE us.shipments_shipment_id_seq OWNED BY us.shipments.shipment_id;


--
-- Name: shoes; Type: TABLE; Schema: us; Owner: postgres
--

CREATE TABLE us.shoes (
    shoe_id integer NOT NULL,
    model_name character varying(100),
    category character varying(50),
    release_date date
);


ALTER TABLE us.shoes OWNER TO "postgres";

--
-- Name: shoes_shoe_id_seq; Type: SEQUENCE; Schema: us; Owner: postgres
--

CREATE SEQUENCE us.shoes_shoe_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE us.shoes_shoe_id_seq OWNER TO "postgres";

--
-- Name: shoes_shoe_id_seq; Type: SEQUENCE OWNED BY; Schema: us; Owner: postgres
--

ALTER SEQUENCE us.shoes_shoe_id_seq OWNED BY us.shoes.shoe_id;


--
-- Name: suppliermaterials; Type: TABLE; Schema: us; Owner: postgres
--

CREATE TABLE us.suppliermaterials (
    supplier_id integer NOT NULL,
    material_id integer NOT NULL,
    lead_time_days integer
);


ALTER TABLE us.suppliermaterials OWNER TO "postgres";

--
-- Name: suppliers; Type: TABLE; Schema: us; Owner: postgres
--

CREATE TABLE us.suppliers (
    supplier_id integer NOT NULL,
    name character varying(100) NOT NULL,
    contact_email character varying(100),
    country character varying(50)
);


ALTER TABLE us.suppliers OWNER TO "postgres";

--
-- Name: suppliers_supplier_id_seq; Type: SEQUENCE; Schema: us; Owner: postgres
--

CREATE SEQUENCE us.suppliers_supplier_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE us.suppliers_supplier_id_seq OWNER TO "postgres";

--
-- Name: suppliers_supplier_id_seq; Type: SEQUENCE OWNED BY; Schema: us; Owner: postgres
--

ALTER SEQUENCE us.suppliers_supplier_id_seq OWNED BY us.suppliers.supplier_id;


--
-- Name: warehouses; Type: TABLE; Schema: us; Owner: postgres
--

CREATE TABLE us.warehouses (
    warehouse_id integer NOT NULL,
    name character varying(100),
    location character varying(100)
);


ALTER TABLE us.warehouses OWNER TO "postgres";

--
-- Name: warehouses_warehouse_id_seq; Type: SEQUENCE; Schema: us; Owner: postgres
--

CREATE SEQUENCE us.warehouses_warehouse_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE us.warehouses_warehouse_id_seq OWNER TO "postgres";

--
-- Name: warehouses_warehouse_id_seq; Type: SEQUENCE OWNED BY; Schema: us; Owner: postgres
--

ALTER SEQUENCE us.warehouses_warehouse_id_seq OWNED BY us.warehouses.warehouse_id;


--
-- Name: factories factory_id; Type: DEFAULT; Schema: us; Owner: postgres
--

ALTER TABLE ONLY us.factories ALTER COLUMN factory_id SET DEFAULT nextval('us.factories_factory_id_seq'::regclass);


--
-- Name: productionorders order_id; Type: DEFAULT; Schema: us; Owner: postgres
--

ALTER TABLE ONLY us.productionorders ALTER COLUMN order_id SET DEFAULT nextval('us.productionorders_order_id_seq'::regclass);


--
-- Name: rawmaterials material_id; Type: DEFAULT; Schema: us; Owner: postgres
--

ALTER TABLE ONLY us.rawmaterials ALTER COLUMN material_id SET DEFAULT nextval('us.rawmaterials_material_id_seq'::regclass);


--
-- Name: shipments shipment_id; Type: DEFAULT; Schema: us; Owner: postgres
--

ALTER TABLE ONLY us.shipments ALTER COLUMN shipment_id SET DEFAULT nextval('us.shipments_shipment_id_seq'::regclass);


--
-- Name: shoes shoe_id; Type: DEFAULT; Schema: us; Owner: postgres
--

ALTER TABLE ONLY us.shoes ALTER COLUMN shoe_id SET DEFAULT nextval('us.shoes_shoe_id_seq'::regclass);


--
-- Name: suppliers supplier_id; Type: DEFAULT; Schema: us; Owner: postgres
--

ALTER TABLE ONLY us.suppliers ALTER COLUMN supplier_id SET DEFAULT nextval('us.suppliers_supplier_id_seq'::regclass);


--
-- Name: warehouses warehouse_id; Type: DEFAULT; Schema: us; Owner: postgres
--

ALTER TABLE ONLY us.warehouses ALTER COLUMN warehouse_id SET DEFAULT nextval('us.warehouses_warehouse_id_seq'::regclass);

-- Import data from CSV files
-- Set default schema
SET search_path TO us;

-- Import suppliers
\COPY Suppliers(name, contact_email, country) FROM '/docker-entrypoint-initdb.d/suppliers.csv' WITH (FORMAT csv, HEADER true);

-- Import raw materials
\COPY RawMaterials(name, unit, cost_per_unit) FROM '/docker-entrypoint-initdb.d/raw_materials.csv' WITH (FORMAT csv, HEADER true);

-- Import supplier materials
\COPY SupplierMaterials(supplier_id, material_id, lead_time_days) FROM '/docker-entrypoint-initdb.d/supplier_materials.csv' WITH (FORMAT csv, HEADER true);

-- Import factories
\COPY Factories(name, location, capacity) FROM '/docker-entrypoint-initdb.d/factories.csv' WITH (FORMAT csv, HEADER true);

-- Import shoes
\COPY Shoes(model_name, category, release_date) FROM '/docker-entrypoint-initdb.d/shoes.csv' WITH (FORMAT csv, HEADER true);

-- Import bill of materials
\COPY BillOfMaterials(shoe_id, material_id, quantity_required) FROM '/docker-entrypoint-initdb.d/bill_of_materials.csv' WITH (FORMAT csv, HEADER true);

-- Import production orders
\COPY ProductionOrders(shoe_id, factory_id, quantity, start_date, expected_completion) FROM '/docker-entrypoint-initdb.d/production_orders.csv' WITH (FORMAT csv, HEADER true);

-- Import warehouses
\COPY Warehouses(name, location) FROM '/docker-entrypoint-initdb.d/warehouses.csv' WITH (FORMAT csv, HEADER true);

-- Import shipments
\COPY Shipments(order_id, warehouse_id, shipped_date, arrival_date, quantity) FROM '/docker-entrypoint-initdb.d/shipments.csv' WITH (FORMAT csv, HEADER true);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_suppliers_name ON Suppliers(name);
CREATE INDEX IF NOT EXISTS idx_rawmaterials_name ON RawMaterials(name);
CREATE INDEX IF NOT EXISTS idx_shoes_model_name ON Shoes(model_name);
CREATE INDEX IF NOT EXISTS idx_shoes_category ON Shoes(category);
CREATE INDEX IF NOT EXISTS idx_productionorders_shoe_id ON ProductionOrders(shoe_id);
CREATE INDEX IF NOT EXISTS idx_productionorders_factory_id ON ProductionOrders(factory_id);
CREATE INDEX IF NOT EXISTS idx_shipments_order_id ON Shipments(order_id);
CREATE INDEX IF NOT EXISTS idx_shipments_warehouse_id ON Shipments(warehouse_id);