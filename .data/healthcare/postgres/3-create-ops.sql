CREATE DATABASE ops;

\c ops;

CREATE TABLE operators (
    operator_id VARCHAR(10) PRIMARY KEY,
    full_name VARCHAR(100),
    region VARCHAR(50),
    specialty VARCHAR(50)
);

CREATE TABLE operator_schedule (
    schedule_id SERIAL PRIMARY KEY,
    operator_id VARCHAR(10) REFERENCES operators(operator_id),
    work_date DATE,
    booked_minutes INT DEFAULT 0,
    max_minutes INT DEFAULT 480,
    UNIQUE (operator_id, work_date)
);

CREATE TABLE cases (
    case_id SERIAL PRIMARY KEY,
    patient_id VARCHAR(20),
    clinic_id VARCHAR(10) NOT NULL,
    procedure_code VARCHAR(5),
    urgency_level VARCHAR(20),
    recommended_date DATE NOT NULL,
    status VARCHAR(20),
    operator_id VARCHAR(10) REFERENCES operators(operator_id),
    region VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

\COPY operators FROM '/docker-entrypoint-initdb.d/operators.csv' WITH (FORMAT csv, HEADER true);
\COPY operator_schedule(operator_id, work_date, booked_minutes, max_minutes) FROM '/docker-entrypoint-initdb.d/operator_schedule.csv' WITH (FORMAT csv, HEADER true);
\COPY cases(patient_id, clinic_id, procedure_code, urgency_level, recommended_date, status, operator_id, region, created_at) FROM '/docker-entrypoint-initdb.d/cases.csv' WITH (FORMAT csv, HEADER true);

CREATE INDEX idx_cases_patient_id ON cases(patient_id);
CREATE INDEX idx_cases_clinic_id ON cases(clinic_id);
CREATE INDEX idx_cases_procedure_code ON cases(procedure_code);
CREATE INDEX idx_cases_urgency_level ON cases(urgency_level);
CREATE INDEX idx_cases_status ON cases(status);
CREATE INDEX idx_cases_created_at ON cases(created_at DESC);
CREATE INDEX idx_cases_operator_id ON cases(operator_id);
CREATE INDEX idx_cases_region ON cases(region);
CREATE INDEX idx_operators_full_name ON operators(full_name);
CREATE INDEX idx_operators_specialty ON operators(specialty);
CREATE INDEX idx_operator_schedule_operator_id ON operator_schedule(operator_id);
CREATE INDEX idx_operator_schedule_work_date ON operator_schedule(work_date);
