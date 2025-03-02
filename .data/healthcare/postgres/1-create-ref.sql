CREATE DATABASE ref;

\c ref;

CREATE TABLE drug_reference (
    product_ndc VARCHAR(11) PRIMARY KEY,
    proprietary_name VARCHAR(200),
    nonproprietary_name VARCHAR(200),
    dosage_form_name VARCHAR(50),
    route_name VARCHAR(100),
    labeler_name VARCHAR(200),
    substance_name VARCHAR(400),
    active_ingredients_info VARCHAR(400)
);

CREATE TABLE drug_packaging (
    ndc_package_code VARCHAR(12) PRIMARY KEY,
    product_ndc VARCHAR(11) REFERENCES drug_reference(product_ndc),
    package_description VARCHAR(150)
);

CREATE TABLE procedure_codes (
    hcpc VARCHAR(5) PRIMARY KEY,
    long_description TEXT NOT NULL,
    short_description VARCHAR(100),
    category VARCHAR(50),
    avg_duration_minutes INT
);

\COPY drug_reference FROM '/docker-entrypoint-initdb.d/drug_reference.csv' WITH (FORMAT csv, HEADER true);
\COPY drug_packaging FROM '/docker-entrypoint-initdb.d/drug_packaging.csv' WITH (FORMAT csv, HEADER true);
\COPY procedure_codes FROM '/docker-entrypoint-initdb.d/procedure_codes.csv' WITH (FORMAT csv, HEADER true);

CREATE INDEX idx_drug_packaging_product_ndc ON drug_packaging(product_ndc);
CREATE INDEX idx_drug_reference_proprietary_name ON drug_reference(proprietary_name);
CREATE INDEX idx_drug_reference_nonproprietary_name ON drug_reference(nonproprietary_name);
CREATE INDEX idx_drug_reference_labeler_name ON drug_reference(labeler_name);
CREATE INDEX idx_drug_reference_active_ingredients ON drug_reference(active_ingredients_info);
CREATE INDEX idx_procedure_codes_category ON procedure_codes(category);