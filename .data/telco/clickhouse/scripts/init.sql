-- Generate CDR table (Call Detail Records)
CREATE TABLE cdr ( CUID Int32, GUID String, Call_Duration Int32, Call_Type String, Timestamp DateTime64(6) ) ENGINE = MergeTree ORDER BY (Timestamp, GUID);
-- Generate network performance table
CREATE TABLE network_performance ( CUID Int32, GUID String, Download_Speed Float32, Upload_Speed Float32, Latency Int32, Timestamp DateTime64(6) ) ENGINE = MergeTree ORDER BY (Timestamp, GUID);
-- Generate data usage table
CREATE TABLE data_usage ( CUID Int32, GUID String, Data_Usage Float32, Timestamp DateTime64(6) ) ENGINE = MergeTree ORDER BY (Timestamp, GUID);
-- Create materialized view
CREATE MATERIALIZED VIEW detailed_user_activity_mv ENGINE = MergeTree ORDER BY (CDR_Timestamp, CDR_GUID) AS
SELECT
    cdr.GUID AS "CDR_GUID",
    cdr.Call_Duration AS "Call_Duration",
    cdr.Call_Type AS "Call_Type",
    cdr.Timestamp AS "CDR_Timestamp",
    network_performance.GUID AS "NP_GUID",
    network_performance.Download_Speed AS "Download_Speed",
    network_performance.Upload_Speed AS "Upload_Speed",
    network_performance.Latency AS "Latency",
    network_performance.Timestamp AS "NP_Timestamp",
    data_usage.GUID AS "DU_GUID",
    data_usage.Data_Usage AS "Data_Usage",
    data_usage.Timestamp AS "DU_Timestamp"
FROM cdr
LEFT JOIN network_performance ON cdr.GUID = network_performance.GUID AND date(cdr.Timestamp) = date(network_performance.Timestamp)
LEFT JOIN data_usage ON cdr.GUID = data_usage.GUID AND date(cdr.Timestamp) = date(data_usage.Timestamp);

-- Load data into cdr table
INSERT INTO cdr FROM INFILE '/etc/clickhouse-server/csv/cdr.csv' FORMAT CSVWithNames;

-- Load data into network_performance table
INSERT INTO network_performance FROM INFILE '/etc/clickhouse-server/csv/network_performance.csv' FORMAT CSVWithNames;

-- Load data into data_usage table
INSERT INTO data_usage FROM INFILE '/etc/clickhouse-server/csv/data_usage.csv' FORMAT CSVWithNames;