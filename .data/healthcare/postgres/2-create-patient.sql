CREATE DATABASE patient;

\c patient;

CREATE TABLE insurance_plans (
    plan_id VARCHAR(20) PRIMARY KEY,
    plan_name VARCHAR(100),
    payer_name VARCHAR(100)
);

CREATE TABLE patients (
    patient_id VARCHAR(20) PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    date_of_birth DATE,
    patient_ssn VARCHAR(11),
    patient_creditcard VARCHAR(16),
    insurance_plan_id VARCHAR(20) REFERENCES insurance_plans(plan_id)
);

\COPY insurance_plans FROM '/docker-entrypoint-initdb.d/insurance_plans.csv' WITH (FORMAT csv, HEADER true);
\COPY patients FROM '/docker-entrypoint-initdb.d/patients.csv' WITH (FORMAT csv, HEADER true);

CREATE INDEX idx_patients_last_name ON patients(last_name);
CREATE INDEX idx_patients_first_name ON patients(first_name);
CREATE INDEX idx_patients_insurance_plan_id ON patients(insurance_plan_id);
CREATE INDEX idx_insurance_plans_payer_name ON insurance_plans(payer_name);
