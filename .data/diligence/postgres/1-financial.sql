CREATE DATABASE financial;

\c financial;

-- Chart of Accounts
CREATE TABLE chart_of_accounts (
    account_id SERIAL PRIMARY KEY,
    account_number VARCHAR(20) NOT NULL UNIQUE,
    account_name VARCHAR(100) NOT NULL,
    account_type VARCHAR(50) NOT NULL CHECK (account_type IN ('Asset', 'Liability', 'Equity', 'Revenue', 'Expense')),
    account_subtype VARCHAR(50),
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- General Ledger
CREATE TABLE general_ledger (
    entry_id SERIAL PRIMARY KEY,
    entry_date DATE NOT NULL,
    account_id INTEGER,
    debit_amount NUMERIC(15, 2) DEFAULT 0,
    credit_amount NUMERIC(15, 2) DEFAULT 0,
    reference_number VARCHAR(50),
    description TEXT,
    fiscal_year INTEGER NOT NULL,
    fiscal_quarter INTEGER NOT NULL CHECK (fiscal_quarter BETWEEN 1 AND 4),
    fiscal_month INTEGER NOT NULL CHECK (fiscal_month BETWEEN 1 AND 12),
    entry_source VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_gl_entry_date ON general_ledger(entry_date);
CREATE INDEX idx_gl_account_id ON general_ledger(account_id);
CREATE INDEX idx_gl_fiscal_period ON general_ledger(fiscal_year, fiscal_quarter, fiscal_month);

-- Financial Statements
CREATE TABLE financial_statements (
    statement_id SERIAL PRIMARY KEY,
    statement_type VARCHAR(50) NOT NULL CHECK (statement_type IN ('Income Statement', 'Balance Sheet', 'Cash Flow Statement')),
    fiscal_year INTEGER NOT NULL,
    fiscal_quarter INTEGER CHECK (fiscal_quarter BETWEEN 1 AND 4),
    fiscal_month INTEGER CHECK (fiscal_month BETWEEN 1 AND 12),
    is_audited BOOLEAN DEFAULT FALSE,
    prepared_by VARCHAR(100),
    approved_by VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (statement_type, fiscal_year, fiscal_quarter, fiscal_month)
);

-- Financial Statement Line Items
CREATE TABLE financial_statement_items (
    item_id SERIAL PRIMARY KEY,
    statement_id INTEGER NOT NULL REFERENCES financial_statements(statement_id),
    account_id INTEGER,
    line_item_name VARCHAR(100) NOT NULL,
    line_item_value NUMERIC(15, 2) NOT NULL,
    line_item_order INTEGER NOT NULL,
    parent_item_id INTEGER REFERENCES financial_statement_items(item_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Budget Planning
CREATE TABLE budget_plans (
    budget_id SERIAL PRIMARY KEY,
    budget_name VARCHAR(100) NOT NULL,
    fiscal_year INTEGER NOT NULL,
    description TEXT,
    status VARCHAR(20) CHECK (status IN ('Draft', 'Approved', 'Closed')),
    prepared_by VARCHAR(100),
    approved_by VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (budget_name, fiscal_year)
);

-- Budget vs Actual
CREATE TABLE budget_vs_actual (
    id SERIAL PRIMARY KEY,
    budget_id INTEGER NOT NULL REFERENCES budget_plans(budget_id),
    account_id INTEGER NOT NULL REFERENCES chart_of_accounts(account_id),
    fiscal_year INTEGER NOT NULL,
    fiscal_quarter INTEGER CHECK (fiscal_quarter BETWEEN 1 AND 4),
    fiscal_month INTEGER CHECK (fiscal_month BETWEEN 1 AND 12),
    budget_amount NUMERIC(15, 2) NOT NULL,
    actual_amount NUMERIC(15, 2),
    variance_amount NUMERIC(15, 2),
    variance_percentage NUMERIC(8, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (budget_id, account_id, fiscal_year, fiscal_quarter, fiscal_month)
);

-- Cash Flow
CREATE TABLE cash_flow (
    cash_flow_id SERIAL PRIMARY KEY,
    transaction_date DATE NOT NULL,
    account_id INTEGER NOT NULL REFERENCES chart_of_accounts(account_id),
    amount NUMERIC(15, 2) NOT NULL,
    flow_type VARCHAR(20) NOT NULL CHECK (flow_type IN ('Inflow', 'Outflow')),
    category VARCHAR(50) NOT NULL CHECK (category IN ('Operating', 'Investing', 'Financing')),
    description TEXT,
    reference_number VARCHAR(50),
    fiscal_year INTEGER NOT NULL,
    fiscal_quarter INTEGER NOT NULL CHECK (fiscal_quarter BETWEEN 1 AND 4),
    fiscal_month INTEGER NOT NULL CHECK (fiscal_month BETWEEN 1 AND 12),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_cf_transaction_date ON cash_flow(transaction_date);
CREATE INDEX idx_cf_category ON cash_flow(category);

-- Capital Expenditures
CREATE TABLE capital_expenditures (
    capex_id SERIAL PRIMARY KEY,
    project_name VARCHAR(100) NOT NULL,
    asset_type VARCHAR(50) NOT NULL,
    purchase_date DATE,
    acquisition_cost NUMERIC(15, 2) NOT NULL,
    expected_useful_life_years INTEGER NOT NULL,
    depreciation_method VARCHAR(50) NOT NULL,
    annual_depreciation NUMERIC(15, 2) NOT NULL,
    accumulated_depreciation NUMERIC(15, 2) DEFAULT 0,
    net_book_value NUMERIC(15, 2),
    department VARCHAR(50),
    project_manager VARCHAR(100),
    approval_date DATE,
    status VARCHAR(20) CHECK (status IN ('Planned', 'In Progress', 'Completed', 'Cancelled')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Debt Instruments
CREATE TABLE debt_instruments (
    debt_id SERIAL PRIMARY KEY,
    instrument_name VARCHAR(100) NOT NULL,
    instrument_type VARCHAR(50) NOT NULL CHECK (instrument_type IN ('Term Loan', 'Revolving Credit', 'Bond', 'Note Payable', 'Lease', 'Other')),
    lender_name VARCHAR(100) NOT NULL,
    principal_amount NUMERIC(15, 2) NOT NULL,
    interest_rate NUMERIC(6, 3) NOT NULL,
    interest_type VARCHAR(20) CHECK (interest_type IN ('Fixed', 'Variable')),
    origination_date DATE NOT NULL,
    maturity_date DATE NOT NULL,
    payment_frequency VARCHAR(20) CHECK (payment_frequency IN ('Monthly', 'Quarterly', 'Semi-Annual', 'Annual')),
    payment_amount NUMERIC(15, 2),
    outstanding_balance NUMERIC(15, 2) NOT NULL,
    is_secured BOOLEAN DEFAULT FALSE,
    collateral_description TEXT,
    covenant_details TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Department information for cost allocation
CREATE TABLE departments (
    department_id SERIAL PRIMARY KEY,
    department_name VARCHAR(100) NOT NULL,
    department_code VARCHAR(20) NOT NULL UNIQUE,
    manager_name VARCHAR(100),
    cost_center BOOLEAN DEFAULT FALSE,
    parent_department_id INTEGER REFERENCES departments(department_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Import data from CSVs
\copy chart_of_accounts(account_number, account_name, account_type, account_subtype, description, is_active) FROM '/docker-entrypoint-initdb.d/chart_of_accounts.csv' DELIMITER ',' CSV HEADER;
\copy general_ledger(entry_id, entry_date, account_id, debit_amount, credit_amount, reference_number, description, fiscal_year, fiscal_quarter, fiscal_month, entry_source) FROM '/docker-entrypoint-initdb.d/general_ledger.csv' DELIMITER ',' CSV HEADER;
\copy financial_statements(statement_id, statement_type, fiscal_year, fiscal_quarter,fiscal_month, is_audited, prepared_by, approved_by) FROM '/docker-entrypoint-initdb.d/financial_statements.csv' DELIMITER ',' CSV HEADER;
\copy financial_statement_items(item_id, statement_id, account_id, line_item_name, line_item_value, line_item_order, parent_item_id) FROM '/docker-entrypoint-initdb.d/financial_statement_items.csv' DELIMITER ',' CSV HEADER;
\copy budget_plans(budget_id, budget_name, fiscal_year, description, status, prepared_by, approved_by) FROM '/docker-entrypoint-initdb.d/budget_plans.csv' DELIMITER ',' CSV HEADER;
\copy budget_vs_actual(id, budget_id, account_id, fiscal_year, fiscal_quarter, fiscal_month, budget_amount, actual_amount, variance_amount, variance_percentage) FROM '/docker-entrypoint-initdb.d/budget_vs_actual.csv' DELIMITER ',' CSV HEADER;
\copy cash_flow(cash_flow_id, transaction_date, account_id, amount, flow_type, category, description, reference_number, fiscal_year, fiscal_quarter, fiscal_month) FROM '/docker-entrypoint-initdb.d/cash_flow.csv' DELIMITER ',' CSV HEADER;
\copy capital_expenditures(capex_id, project_name, asset_type, purchase_date, acquisition_cost, expected_useful_life_years, depreciation_method, annual_depreciation, accumulated_depreciation, net_book_value, department, project_manager, approval_date, status) FROM '/docker-entrypoint-initdb.d/capital_expenditures.csv' DELIMITER ',' CSV HEADER;
\copy debt_instruments(debt_id, instrument_name, instrument_type, lender_name, principal_amount, interest_rate, interest_type, origination_date, maturity_date, payment_frequency, payment_amount, outstanding_balance, is_secured, collateral_description, covenant_details) FROM '/docker-entrypoint-initdb.d/debt_instruments.csv' DELIMITER ',' CSV HEADER;
\copy departments(department_id, department_name, department_code, manager_name, cost_center, parent_department_id) FROM '/docker-entrypoint-initdb.d/departments.csv' DELIMITER ',' CSV HEADER;