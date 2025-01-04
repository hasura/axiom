CREATE DATABASE customer;

\c customer;

-- Table for storing customer information
CREATE TABLE public.customers (
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
    image VARCHAR(30),
    segment VARCHAR(30)
);
