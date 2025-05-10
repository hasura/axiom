CREATE DATABASE salesforce;

\c salesforce;

CREATE TABLE accounts (
    id VARCHAR(255) PRIMARY KEY,
    account_buying_stage_6_sense_c VARCHAR(255),
    account_intent_score_6_sense_c VARCHAR(255),
    account_tier_c VARCHAR(255),
    annual_revenue VARCHAR(255),
    became_customer_date_c VARCHAR(255),
    billing_city VARCHAR(255),
    billing_country VARCHAR(255),
    billing_state VARCHAR(255),
    billing_street VARCHAR(255),
    csm_owner_c VARCHAR(255),
    customer_subscription_end_date_c VARCHAR(255),
    customer_subscription_initial_start_date_c VARCHAR(255),
    customer_support_tier_c VARCHAR(255),
    customer_type_c VARCHAR(255),
    geo_c VARCHAR(255),
    industry VARCHAR(255),
    name VARCHAR(255),
    named_account_c VARCHAR(255),
    nps_score_c VARCHAR(255),
    oss_last_ping_date_c VARCHAR(255),
    oss_total_instances_c VARCHAR(255),
    oss_total_pings_c VARCHAR(255),
    oss_usage_last_updated_c VARCHAR(255),
    oss_user_c VARCHAR(255),
    owner_id INTEGER,
    primary_churn_score_c VARCHAR(255),
    projects_on_annual_plan_c VARCHAR(255),
    projects_on_monthly_plan_c VARCHAR(255),
    purchased_models_v_2_c VARCHAR(255),
    record_type_id VARCHAR(255),
    region_c VARCHAR(255),
    saasoptics_arr_at_end_of_month_c VARCHAR(255),
    type VARCHAR(255),
    ultimate_parent_c VARCHAR(255),
    usage_annual_prod_models_v_2_c VARCHAR(255),
    usage_annual_v_2_api_last_month_c VARCHAR(255),
    usage_annual_v_2_api_yesterday_c VARCHAR(255),
    usage_annual_v_2_data_gb_last_month_c VARCHAR(255),
    usage_annual_v_2_data_gb_yesterday_c VARCHAR(255),
    usage_payg_last_invoiced_amount_c VARCHAR(255),
    usage_payg_models_c VARCHAR(255),
    website VARCHAR(255)
);

CREATE TABLE contacts (
    id VARCHAR(255) PRIMARY KEY,
    account_id VARCHAR(255) REFERENCES accounts(id),
    cloud_user_activated_date_c VARCHAR(255),
    cloud_user_id_c VARCHAR(255),
    contact_grade_6_sense_c VARCHAR(255),
    contact_intent_score_6_sense_c VARCHAR(255),
    contact_requested_date_c VARCHAR(255),
    contact_roles_c VARCHAR(255),
    contact_status_c VARCHAR(255),
    ddn_advanced_trial_end_date_c VARCHAR(255),
    ddn_advanced_trial_start_date_c VARCHAR(255),
    ddn_base_trial_end_date_c VARCHAR(255),
    ddn_base_trial_start_date_c VARCHAR(255),
    ddn_signup_date_c VARCHAR(255),
    discovery_call_completed_c VARCHAR(255),
    discovery_call_notes_c TEXT,
    ead_successful_touch_channel_c VARCHAR(255),
    email VARCHAR(255),
    first_name VARCHAR(255),
    free_email_domain_c VARCHAR(255),
    groove_last_touch_c VARCHAR(255),
    groove_last_touch_type_c VARCHAR(255),
    last_activity_by_c VARCHAR(255),
    last_activity_date_c VARCHAR(255),
    last_discovery_call_c VARCHAR(255),
    last_mql_date_c VARCHAR(255),
    last_name VARCHAR(255),
    last_successful_touch_channel_c VARCHAR(255),
    last_successful_touch_date_c VARCHAR(255),
    last_successful_touch_family_c VARCHAR(255),
    last_successful_touch_program_detail_c VARCHAR(255),
    last_successful_touch_type_c VARCHAR(255),
    last_working_date_c VARCHAR(255),
    lead_source VARCHAR(255),
    lead_source_channel_c VARCHAR(255),
    lead_source_detail_c VARCHAR(255),
    middle_name VARCHAR(255),
    mkto_si_last_interesting_moment_date_c VARCHAR(255),
    mkto_si_last_interesting_moment_desc_c VARCHAR(255),
    mql_counter_c VARCHAR(255),
    mql_source_c VARCHAR(255),
    name VARCHAR(255),
    owner_id VARCHAR(255),
    person_city_c VARCHAR(255),
    person_country_c VARCHAR(255),
    person_geo_c VARCHAR(255),
    person_state_c VARCHAR(255),
    prompt_ql_activated_c VARCHAR(255),
    prompt_ql_signup_date_c VARCHAR(255),
    status_reason_c VARCHAR(255),
    title VARCHAR(255),
    trial_end_date_c VARCHAR(255),
    trial_start_date_c VARCHAR(255),
    v_3_user_c VARCHAR(255)
);

CREATE TABLE campaigns (
    id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255),
    type VARCHAR(255)
);

CREATE TABLE campaign_members (
    id VARCHAR(255) PRIMARY KEY,
    campaign_id VARCHAR(255) REFERENCES campaigns(id),
    company_or_account VARCHAR(255),
    contact_id VARCHAR(255) REFERENCES contacts(id),
    created_date VARCHAR(255),
    lead_id VARCHAR(255),
    net_new_lead_c VARCHAR(255),
    status VARCHAR(255)
);

CREATE TABLE cloud_project_c (
    id VARCHAR(255) PRIMARY KEY,
    account_c VARCHAR(255) REFERENCES accounts(id),
    active_models_count_c VARCHAR(255),
    api_request_previous_day_c VARCHAR(255),
    api_requests_previous_month_c VARCHAR(255),
    contact_c VARCHAR(255) REFERENCES contacts(id),
    data_passthrough_gb_previous_day_c VARCHAR(255),
    data_passthrough_gb_previous_month_c VARCHAR(255),
    is_ddn_project_c VARCHAR(255),
    last_invoiced_amount_c VARCHAR(255),
    last_invoiced_date_c VARCHAR(255),
    lead_c VARCHAR(255),
    models_count_c VARCHAR(255),
    name VARCHAR(255),
    plan_name_c VARCHAR(255),
    project_name_c VARCHAR(255),
    uid_c VARCHAR(255)
);

CREATE TABLE contracts (
    id VARCHAR(255) PRIMARY KEY,
    account_id VARCHAR(255) REFERENCES accounts(id),
    activated_date VARCHAR(255),
    agreement_status_c VARCHAR(255),
    agreement_type_c VARCHAR(255),
    contract_opportunity_c VARCHAR(255),
    end_date VARCHAR(255),
    last_status_change_c VARCHAR(255),
    name VARCHAR(255),
    start_date VARCHAR(255),
    status VARCHAR(255)
);

CREATE TABLE events (
    id VARCHAR(255) PRIMARY KEY,
    activity_date VARCHAR(255),
    description TEXT,
    event_subtype VARCHAR(255),
    owner_id VARCHAR(255),
    subject VARCHAR(255),
    type VARCHAR(255),
    what_id VARCHAR(255),
    who_id VARCHAR(255)
);

CREATE TABLE leads (
    id VARCHAR(255) PRIMARY KEY,
    account_6_qa_6_sense_c VARCHAR(255),
    account_buying_stage_6_sense_c VARCHAR(255),
    account_intent_score_6_sense_c VARCHAR(255),
    annual_revenue VARCHAR(255),
    cloud_user_activated_date_c VARCHAR(255),
    cloud_user_id_c VARCHAR(255),
    company VARCHAR(255),
    contact_requested_date_c VARCHAR(255),
    ddn_advanced_trial_end_date_c VARCHAR(255),
    ddn_advanced_trial_start_date_c VARCHAR(255),
    ddn_base_trial_end_date_c VARCHAR(255),
    ddn_base_trial_start_date_c VARCHAR(255),
    ddn_signup_date_c VARCHAR(255),
    discovery_call_completed_c VARCHAR(255),
    discovery_call_notes_c TEXT,
    email VARCHAR(255),
    finished_sequences_c VARCHAR(255),
    first_name VARCHAR(255),
    free_email_domain_c VARCHAR(255),
    geo_c VARCHAR(255),
    groove_last_touch_c VARCHAR(255),
    groove_last_touch_type_c VARCHAR(255),
    industry VARCHAR(255),
    last_activity_by_c VARCHAR(255),
    last_activity_date_c VARCHAR(255),
    last_discovery_call_c VARCHAR(255),
    last_mql_date_c VARCHAR(255),
    last_name VARCHAR(255),
    last_recycle_date_c VARCHAR(255),
    last_set_to_nurture_date_c VARCHAR(255),
    last_submitted_to_sales_date_c VARCHAR(255),
    last_successful_touch_channel_c VARCHAR(255),
    last_successful_touch_date_c VARCHAR(255),
    last_successful_touch_family_c VARCHAR(255),
    last_successful_touch_program_detail_c VARCHAR(255),
    last_successful_touch_type_c VARCHAR(255),
    last_working_date_c VARCHAR(255),
    lead_grade_6_sense_c VARCHAR(255),
    lead_source VARCHAR(255),
    lead_source_channel_c VARCHAR(255),
    lead_source_detail_c VARCHAR(255),
    mkto_si_last_interesting_moment_date_c VARCHAR(255),
    mkto_si_last_interesting_moment_desc_c VARCHAR(255),
    mql_counter_c VARCHAR(255),
    mql_source_c VARCHAR(255),
    mql_source_most_recent_c VARCHAR(255),
    name VARCHAR(255),
    number_of_employees VARCHAR(255),
    outreach_actively_being_sequenced_c VARCHAR(255),
    outreach_current_sequence_name_c VARCHAR(255),
    owner_id VARCHAR(255),
    person_city_c VARCHAR(255),
    person_country_c VARCHAR(255),
    person_geo_c VARCHAR(255),
    person_state_c VARCHAR(255),
    prompt_ql_activated_c VARCHAR(255),
    prompt_ql_signup_date_c VARCHAR(255),
    region_c VARCHAR(255),
    status VARCHAR(255),
    status_reason_c VARCHAR(255),
    title VARCHAR(255),
    trial_end_date_c VARCHAR(255),
    trial_start_date_c VARCHAR(255),
    v_3_user_c VARCHAR(255),
    website VARCHAR(255)
);

CREATE TABLE opportunity_contact_roles (
    id VARCHAR(255) PRIMARY KEY,
    contact_id VARCHAR(255) REFERENCES contacts(id),
    is_primary VARCHAR(255),
    opportunity_id VARCHAR(255),
    role VARCHAR(255)
);

CREATE TABLE opportunity_line_items (
    id VARCHAR(255) PRIMARY KEY,
    description TEXT,
    end_date_c VARCHAR(255),
    list_price VARCHAR(255),
    name VARCHAR(255),
    opportunity_id VARCHAR(255),
    product_2_id VARCHAR(255),
    product_code VARCHAR(255),
    product_family_text_c VARCHAR(255),
    product_line_type_c VARCHAR(255),
    quantity VARCHAR(255),
    start_date_c VARCHAR(255),
    subtotal VARCHAR(255),
    total_price VARCHAR(255),
    unit_price VARCHAR(255)
);

CREATE TABLE opportunities (
    id VARCHAR(255) PRIMARY KEY,
    account_id VARCHAR(255) REFERENCES accounts(id),
    name VARCHAR(255),
    amount VARCHAR(255),
    stage VARCHAR(255),
    probability INTEGER,
    close_date VARCHAR(255),
    owner_id INTEGER,
    created_date VARCHAR(255),
    metrics_c TEXT,
    economic_buyer_c VARCHAR(255),
    decision_criteria_c TEXT,
    decision_process_c TEXT,
    paper_process_c TEXT,
    identified_pain_c TEXT,
    champion_c VARCHAR(255),
    competition_c TEXT
);

CREATE TABLE product_2 (
    id VARCHAR(255) PRIMARY KEY,
    description TEXT,
    family VARCHAR(255),
    name VARCHAR(255),
    product_code VARCHAR(255),
    sku_family_c VARCHAR(255),
    stock_keeping_unit VARCHAR(255),
    support_level_c VARCHAR(255)
);

CREATE TABLE tasks (
    id VARCHAR(255) PRIMARY KEY,
    activity_date VARCHAR(255),
    call_disposition VARCHAR(255),
    call_type VARCHAR(255),
    completed_date_time VARCHAR(255),
    description TEXT,
    owner_id VARCHAR(255),
    status VARCHAR(255),
    subject VARCHAR(255),
    task_subtype VARCHAR(255),
    type VARCHAR(255),
    what_id VARCHAR(255),
    who_id VARCHAR(255)
);

CREATE TABLE users (
    id VARCHAR(255) PRIMARY KEY,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    user_role_id VARCHAR(255)
);

CREATE TABLE user_role (
    id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255)
);

CREATE TABLE sequences (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    description TEXT,
    created_by VARCHAR(255),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE sequence_steps (
    id SERIAL PRIMARY KEY,
    sequence_id INT REFERENCES sequences(id),
    step_number INT,
    step_type VARCHAR(50),
    template_subject VARCHAR(255),
    template_body TEXT,
    delay_days INT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE lead_sequences (
    id SERIAL PRIMARY KEY,
    lead_id VARCHAR(255) REFERENCES leads(id),
    sequence_id INT REFERENCES sequences(id),
    current_step INT,
    status VARCHAR(50),
    started_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- Function to add a lead to a sequence
CREATE OR REPLACE FUNCTION add_lead_to_sequence(
    p_lead_id VARCHAR(255),
    p_sequence_id INT
) RETURNS VOID AS $$
BEGIN
    INSERT INTO lead_sequences (lead_id, sequence_id, current_step, status)
    VALUES (p_lead_id, p_sequence_id, 1, 'ACTIVE');
END;
$$ LANGUAGE plpgsql;

-- Function to mark a lead as MQL
CREATE OR REPLACE FUNCTION mark_as_mql(
    p_lead_id VARCHAR(255)
) RETURNS VOID AS $$
BEGIN
    UPDATE leads
    SET status = 'MQL',
        rating = 'Hot'
    WHERE id = p_lead_id;
END;
$$ LANGUAGE plpgsql; 


\COPY accounts FROM '/docker-entrypoint-initdb.d/salesforce_accounts.csv' WITH (FORMAT csv, HEADER true);
\COPY contacts FROM '/docker-entrypoint-initdb.d/salesforce_contacts.csv' WITH (FORMAT csv, HEADER true);
\COPY campaigns FROM '/docker-entrypoint-initdb.d/salesforce_campaigns.csv' WITH (FORMAT csv, HEADER true);
\COPY campaign_members FROM '/docker-entrypoint-initdb.d/salesforce_campaign_members.csv' WITH (FORMAT csv, HEADER true);
\COPY opportunities FROM '/docker-entrypoint-initdb.d/salesforce_opportunities.csv' WITH (FORMAT csv, HEADER true);
\COPY opportunity_contact_roles FROM '/docker-entrypoint-initdb.d/salesforce_opportunity_contact_roles.csv' WITH (FORMAT csv, HEADER true);
\COPY tasks FROM '/docker-entrypoint-initdb.d/salesforce_tasks.csv' WITH (FORMAT csv, HEADER true);