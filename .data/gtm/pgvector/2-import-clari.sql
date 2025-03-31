CREATE DATABASE clari;

\c clari;

-- Enable vector extension for embeddings
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE calls (
    id TEXT PRIMARY KEY,
    account_name TEXT,
    call_action_items_discussed TEXT,
    call_action_items_discussed_embedding vector(3),
    call_full_transcript TEXT,
    call_full_transcript_embedding vector(3),
    call_key_takeaways TEXT,
    call_key_takeaways_embedding vector(3),
    call_review_page TEXT NOT NULL,
    call_summary TEXT,
    call_summary_embedding vector(3),
    call_topics_discussed TEXT,
    call_topics_discussed_embedding vector(3),
    last_modified_time TIMESTAMP NOT NULL,
    salesforce_account_id TEXT,
    salesforce_contact_ids TEXT[],
    salesforce_deal_id TEXT,
    source_id TEXT,
    time TIMESTAMP NOT NULL,
    title TEXT NOT NULL,
    type TEXT NOT NULL
);

CREATE TABLE call_participants (
    call_id TEXT NOT NULL REFERENCES calls(id),
    call_person_id TEXT PRIMARY KEY,
    email TEXT,
    is_organizer BOOLEAN NOT NULL,
    name TEXT,
    person_id INTEGER NOT NULL,
    user_id TEXT
);

CREATE TABLE call_transcriptions (
    call_id TEXT NOT NULL REFERENCES calls(id),
    call_person_id TEXT REFERENCES call_participants(call_person_id),
    end_time DOUBLE PRECISION NOT NULL,
    person_id INTEGER NOT NULL,
    start_time DOUBLE PRECISION NOT NULL,
    text TEXT NOT NULL,
    text_embedding vector(3),
    transcription_id TEXT PRIMARY KEY
);

CREATE TABLE call_action_items (
    action_item TEXT,
    call_id TEXT NOT NULL REFERENCES calls(id),
    end_timestamp TIME,
    owner_name TEXT,
    reasoning TEXT,
    speaker_name TEXT,
    start_timestamp TIME,
    timeline TEXT
);

CREATE TABLE call_topics (
    call_id TEXT NOT NULL REFERENCES calls(id),
    end_timestamp TIME,
    name TEXT,
    start_timestamp TIME,
    summary TEXT
);

-- Function to calculate engagement score based on call participation
CREATE OR REPLACE FUNCTION calculate_call_engagement(
    p_account_id TEXT,
    p_start_date TIMESTAMP,
    p_end_date TIMESTAMP
) RETURNS DECIMAL AS $$
DECLARE
    v_score DECIMAL;
BEGIN
    SELECT COALESCE(
        (
            SELECT COUNT(DISTINCT c.id)::DECIMAL / 
            (EXTRACT(EPOCH FROM (p_end_date - p_start_date)) / 86400)
            FROM calls c
            WHERE c.salesforce_account_id = p_account_id
            AND c.time BETWEEN p_start_date AND p_end_date
        ),
        0.0
    )
    INTO v_score;
    
    RETURN v_score;
END;
$$ LANGUAGE plpgsql;

-- Function to analyze call sentiment and topics
CREATE OR REPLACE FUNCTION analyze_call_topics(
    p_call_id TEXT
) RETURNS TABLE (
    topic TEXT,
    sentiment DECIMAL,
    duration INTERVAL
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        ct.name,
        0.0::DECIMAL,
        (ct.end_timestamp::TIMESTAMP - ct.start_timestamp::TIMESTAMP)::INTERVAL
    FROM call_topics ct
    WHERE ct.call_id = p_call_id;
END;
$$ LANGUAGE plpgsql; 

\COPY calls FROM '/docker-entrypoint-initdb.d/clari_calls.csv' WITH (FORMAT csv, HEADER true);
\COPY call_action_items FROM '/docker-entrypoint-initdb.d/clari_call_action_items.csv' WITH (FORMAT csv, HEADER true);
\COPY call_participants FROM '/docker-entrypoint-initdb.d/clari_call_participants.csv' WITH (FORMAT csv, HEADER true);
\COPY transcriptions FROM '/docker-entrypoint-initdb.d/clari_transcriptions.csv' WITH (FORMAT csv, HEADER true);
\COPY topics FROM '/docker-entrypoint-initdb.d/clari_topics.csv' WITH (FORMAT csv, HEADER true);
