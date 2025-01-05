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

INSERT INTO customers (first_name, last_name, email, phone_number, address, city, state, postcode, country, image, segment) VALUES
('Adam', 'Mcdaniel', 'adam.mcdaniel@bigpond.com', '+61 444 221 835', 'Suite 801, 4 Kristen Circle', 'Patrickfort', 'ACT', '2681', 'Australia', '1.png', 'family'),
('Daniel', 'Lane', 'daniel.lane@yahoo.com.au', '6402.5420', '719 Mary Riverway', 'Colemanfort', 'NT', '2912', 'Australia', '2.png', 'tech-savvy'),
('Nathan', 'Moore', 'nathan.moore@outlook.com.au', '9743-6448', '70/66 Stephanie Entrance', 'Andersonberg', 'NT', '1943', 'Australia', '3.png', 'family'),
('Katherine', 'Arellano', 'katherine.arellano@gmail.com', '+61 454 197 812', 'Apt. 723, 9 Danielle Wade', 'Sanfordhaven', 'QLD', '2962', 'Australia', '4.png', 'high-data'),
('Jason', 'Willis', 'jason.willis@hotmail.com.au', '+61-435-516-086', '831 Garcia Square', 'Lake Erik', 'NT', '2674', 'Australia', '5.png', 'budget-conscious'),
('Mark', 'Holland', 'mark.holland@yahoo.com.au', '+61 476 702 740', '10 Holt Lookout', 'New Jameshaven', 'ACT', '8455', 'Australia', '6.png', 'family'),
('Alexis', 'Smith', 'alexis.smith@gmail.com', '0468 973 571', 'Flat 37, 294 Ellis Trail', 'Smithbury', 'SA', '2796', 'Australia', '7.png', 'tech-savvy'),
('Tiffany', 'Ayers', 'tiffany.ayers@gmail.com', '+61.464.133.362', '1 Silva Brow', 'St. Justinfurt', 'SA', '2208', 'Australia', '8.png', 'budget-conscious'),
('Matthew', 'Reed', 'matthew.reed@bigpond.com', '0411-345-572', '212 Jason Quadrant', 'East Kenneth', 'QLD', '2922', 'Australia', '9.png', 'frequent-traveler'),
('Isaac', 'Kramer', 'isaac.kramer@holotel.xyz', '0434.911.936', '009 Carl Mount', 'Nicholasport', 'NT', '2681', 'Australia', '10.png', 'tech-savvy');