CREATE SCHEMA ref;

CREATE TABLE ref.drug_reference (
    product_ndc VARCHAR(11) PRIMARY KEY,
    proprietary_name VARCHAR(100),
    nonproprietary_name VARCHAR(100),
    dosage_form_name VARCHAR(50),
    route_name VARCHAR(50),
    labeler_name VARCHAR(100),
    substance_name VARCHAR(100),
    active_ingredients_info VARCHAR(50)
);

CREATE TABLE ref.drug_packaging (
    ndc_package_code VARCHAR(12) PRIMARY KEY,
    product_ndc VARCHAR(11) REFERENCES ref.drug_reference(product_ndc),
    package_description VARCHAR(150)
);

CREATE TABLE ref.procedure_codes (
    hcpc VARCHAR(5) PRIMARY KEY,
    long_description TEXT NOT NULL,
    short_description VARCHAR(100),
    category VARCHAR(50),
    avg_duration_minutes INT
);

\COPY ref.drug_reference FROM '/tmp/ref_drug_reference.csv' WITH (FORMAT csv, HEADER true);
\COPY ref.drug_packaging FROM '/tmp/ref_drug_packaging.csv' WITH (FORMAT csv, HEADER true);
\COPY ref.procedure_codes FROM '/tmp/ref_procedure_codes.csv' WITH (FORMAT csv, HEADER true);