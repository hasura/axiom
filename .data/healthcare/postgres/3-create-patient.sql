CREATE SCHEMA patient;

CREATE TABLE patient.patients (
    patient_id VARCHAR(20) PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    date_of_birth DATE,
    insurance_plan_id VARCHAR(20) REFERENCES patient.insurance_plans(plan_id)
);

CREATE TABLE patient.insurance_plans (
    plan_id VARCHAR(20) PRIMARY KEY,
    plan_name VARCHAR(100),
    payer_name VARCHAR(100)
);

\COPY patient.patients FROM '/tmp/patient_patients.csv' WITH (FORMAT csv, HEADER true);
\COPY patient.insurance_plans FROM '/tmp/patient_insurance_plans.csv' WITH (FORMAT csv, HEADER true);