CREATE SCHEMA ops;

CREATE TABLE ops.cases (
    case_id SERIAL PRIMARY KEY,
    patient_id VARCHAR(20) REFERENCES patient.patients(patient_id),
    clinic_id VARCHAR(10) NOT NULL,
    procedure_code VARCHAR(5) REFERENCES ref.procedure_codes(hcpc),
    urgency_level VARCHAR(10) CHECK (urgency_level IN ('urgent', 'normal')),
    recommended_date DATE NOT NULL,
    status VARCHAR(20) CHECK (status IN ('pending', 'assigned', 'completed')),
    operator_id VARCHAR(10) REFERENCES ops.operators(operator_id),
    region VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE ops.operators (
    operator_id VARCHAR(10) PRIMARY KEY,
    full_name VARCHAR(100),
    region VARCHAR(50),
    specialty VARCHAR(50)
);

CREATE TABLE ops.operator_schedule (
    schedule_id SERIAL PRIMARY KEY,
    operator_id VARCHAR(10) REFERENCES ops.operators(operator_id),
    work_date DATE,
    booked_minutes INT DEFAULT 0,
    max_minutes INT DEFAULT 480,
    UNIQUE (operator_id, work_date)
);

\COPY ops.operators FROM '/tmp/ops_operators.csv' WITH (FORMAT csv, HEADER true);
\COPY ops.operator_schedule FROM '/tmp/ops_operator_schedule.csv' WITH (FORMAT csv, HEADER true);
\COPY ops.cases FROM '/tmp/ops_cases.csv' WITH (FORMAT csv, HEADER true);