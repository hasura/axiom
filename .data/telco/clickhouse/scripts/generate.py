import random
import datetime

# Number of records to generate for each table
NUM_RECORDS = 100000

# Mapping of GUIDs to CUIDs
guid_to_cuid = {
    '5e58b417-3cde-4cbd-b9e7-7896cf3d435b': 1,
    '859d2da9-c54d-4501-82ec-04bd3a276cd8': 2,
    '6d4f76b5-31b4-4018-bb54-2cdd2bd4ace6': 3,
    'fe0d91d6-2237-4343-9b70-626997d40025': 4,
    '4a071173-8666-4368-bc46-ef8dd58c9406': 5,
    'b8b31280-c88c-44c8-8f89-66262c1b57b0': 6,
    'dd264970-f61f-429f-97f8-4761fea4de2f': 7,
    'd6d8dc95-2321-49f2-a86f-e5ddf50e3129': 8,
    'e6b467db-557a-443f-8da0-c3dcaec5663a': 9,
    '3afe9e44-7e01-4d8c-a610-ddac5662396d': 10,
    '2e8dd6e8-cc7d-4bd7-ba52-ce7ae20bc0c6': 11,
    '2373100d-630d-41fe-93dd-1134dbbe7e0e': 12,
    'c2646b8f-6f3d-4b91-a8ae-b5a47073f997': 13,
    'adff1f8e-e518-4ea6-80ca-c9ac9c7a5c33': 14,
    '5e609951-4c6d-47b8-8d25-d6f73ab1032b': 15,
    '1a284372-b632-491a-95e9-fff159a76d21': 16,
    'b2570f3f-8f2e-4f2b-a82f-00da213f68bc': 17,
    '1ec159cd-1e5b-4519-8a15-233fb6badd4d': 18,
    '250de58a-17b3-4aad-96e5-21b8028f2da2': 19,
    'a9e2c82b-cbb3-48a0-88e2-8c4c370e727c': 20,
    '3f711a10-53ac-4609-b061-c4d6ae5cd2d6': 21,
    'eadeab1b-eb46-4257-9680-62a4e846ff56': 22,
    'bea981be-622c-47dc-b06e-f93e7f6fcc8c': 23,
    'cdf887b8-8fd0-4fe1-b3b0-857792813f3d': 24,
    '56f07f91-10ad-45ab-a0bb-3133f125a669': 25,
    'b1b77625-4046-4753-8dac-52d95248aee7': 26,
    '83a58359-c018-4190-90ca-459d0794ebdb': 27,
    '60843adc-b408-4146-b75a-120a53ebe69c': 28,
    'd5f16f1a-a4d3-4775-bf8d-54a7537c1af7': 29,
    '1969bbcb-d9bf-43db-b849-f31969a5391c': 30,
    'e213281b-339d-403c-aaae-e925e19d4da9': 31,
    'c09ea3a3-a7e9-46cd-bfb7-9a2bedc95cc2': 32,
    'fb6e1f6b-6eb0-4e43-bef0-412fae682158': 33,
    '3ce95a8e-0775-4c74-a76c-c0d4b1d9169e': 34,
    'cba3ab69-fac8-4094-a271-38d6a9600bac': 35,
    'ede031dc-6370-4307-bb7b-375187141ee3': 36,
    'cc611e70-8af8-4315-a35a-69198e35c526': 37,
    'a2f97322-bc51-46ed-a14f-c0c587151796': 38,
    '3d4da6a7-ff85-4eb1-955e-61beb017c170': 39,
    'cdb74bc6-00f7-4cf7-8d42-527238afe3a2': 40,
    '2d553286-835f-4404-804d-d281e0d4a0b6': 41,
    '928d1630-2258-49f4-8821-f5b1f3ac40ea': 42,
    '59898f71-c9c9-48f4-8104-ad62b7b441b2': 43,
    '2a5c829c-dbed-415d-bd77-59029fb9c0f5': 44,
    '47e9397f-3af9-466b-9513-9b40d5ef027f': 45,
    '3a4f0839-310a-440f-b6d8-748c934d7cec': 46,
    'eb783b09-7997-424a-869c-210e58e38d91': 47,
    '54350f41-ad97-40f4-8161-6e9a628a0df7': 48,
    '8c418e68-48aa-411b-8ced-21984fe9db6d': 49,
    '98cc225f-1ade-4936-af64-701183f4eeaf': 50,
    '13e68987-db07-423c-b1f8-69fbc461658e': 51,
    '1ba53ec7-c99d-46b6-80e8-8650c4696ba1': 52,
    'fdf4cba8-4c47-4038-9515-e61360a666ed': 53,
    'd83da028-a09b-4b4b-bde2-fec4af6a31b0': 54,
    'ce396a23-10e2-4252-b756-685308207bf1': 55,
    '361986fa-123f-4817-aa16-3f6b8ae368a2': 56,
    '03775cc7-9186-45ef-a090-ba6fc711fb81': 57,
    '1f8d6822-8b51-452f-8a80-f4d03d01384e': 58,
    'd35250ee-1615-4490-aabc-32cfec3c43f3': 59,
    '838f7882-b114-42ce-98e3-1c9facaf4835': 60,
    '6d363273-8278-4013-9f7e-e8da036e634a': 61,
    '41f8b31e-a172-4b68-8148-a0d350998c03': 62,
    '1d8576dd-a741-4c55-828f-90154dce55fd': 63,
    'eb36ad5b-f6ab-4c18-a180-4f0f8f4964c5': 64,
    '8e616e1c-e514-484d-bddc-5296e3fde187': 65,
    'e2304b5c-15b5-4d84-aec6-fdef4d6bb3d2': 66,
    'f46eed39-eeff-4d80-b6d2-9849226c6816': 67,
    'bc024054-49fa-45c4-90fd-3a44980fdf78': 68,
    'c4eb8d4c-d28d-4bbf-b2af-a72c97cfccb6': 69,
    '3ebc550d-c14b-4a18-9dad-2fa328063486': 70,
    'f1a5ea36-30c6-4d0e-99ab-c9578ff321ce': 71,
    'beceb10a-a2a4-4ba3-a7ec-202724124330': 72,
    'd97d5a32-ac0a-45d3-8baf-bb3b24a4f1f6': 73,
    '55bb9264-3230-421c-b249-3e299d4de9d7': 74,
    '1da7707e-d1a1-4989-a104-aae364d2f9b7': 75,
    '96dbde7a-aa94-466e-9480-666220398fff': 76,
    'a4008bd3-cd15-4581-944e-c2e003ce6da4': 77,
    'c32f754b-ef6c-4140-aa96-4736b1d0739d': 78,
    'aee7a5f0-0b6a-46c8-968f-49a087e69e58': 79,
    'f7c7820a-fefc-4ecc-b120-5f0869cbf4cc': 80,
    'fb58ecf7-c670-4729-bec2-9b5eb877c5d9': 81,
    '825cd363-053e-4f6e-b7c3-7c3cb3d7336c': 82,
    'fabe9a77-cc2d-43bb-93e4-0f5d90aaf077': 83,
    'db2f7e4a-6682-4ba2-9568-edb2a005d543': 84,
    'f995b872-6bbb-4553-aebd-5e8a241b05af': 85,
    '1bdfcbdb-b9d2-4a55-9dfb-cb1e8afc245d': 86,
    'db8b20a0-e387-4c5b-bb63-ce5467edcf91': 87,
    '27d71eb9-250f-4130-9485-fdf8ace8bb3e': 88,
    'd562c9e4-1415-465e-b0c5-1ccfe1032832': 89,
    '087d4d2a-1f7b-461c-b13c-ab55c79cb4d4': 90,
    '38745d1f-3200-49a8-bc0e-b5ba34f98152': 91,
    '11798e10-aa49-4c28-8075-eac791ca1a8f': 92,
    '285e3e2b-9d48-479a-9528-c46dc59b6e2e': 93,
    'b5a20328-6237-4bdc-b2b0-bc5496bac4b1': 94,
    '7b0dcbb9-1291-4bdd-aa24-2a3fa2faa51b': 95,
    'ee4006c8-1bd9-421a-af88-1828ab96e6b5': 96,
    '536aadf0-1098-487c-9a63-5fe623591da7': 97,
    '130dce11-b01f-4e0e-82e0-c7fc00922225': 98,
    '31750099-435b-46c8-9271-1c30fd70d156': 99,
    'cc52ba76-6236-4c5b-b999-93fd74194c7d': 100
}

def generate_timestamp():
    end_date = datetime.datetime.today()
    start_date = end_date - datetime.timedelta(days=365)
    timestamps = [start_date + datetime.timedelta(seconds=i * (end_date - start_date).total_seconds() / NUM_RECORDS) for i in range(NUM_RECORDS)]
    return [ts.strftime('%Y-%m-%d %H:%M:%S') for ts in timestamps]

def generate_anomalous_value(normal_range, anomaly_range, anomaly_probability=0.1):
    return random.uniform(*anomaly_range) if random.random() < anomaly_probability else random.uniform(*normal_range)

def generate_cdr_data():
    call_types = ['Incoming', 'Outgoing']
    timestamps = generate_timestamp()
    data = []
    for i in range(NUM_RECORDS):
        guid = random.choice(list(guid_to_cuid.keys()))
        cuid = guid_to_cuid[guid]
        duration = int(generate_anomalous_value((1, 3600), (5000, 10000)))
        call_type = random.choice(call_types)
        timestamp = timestamps[i]
        data.append(f"({cuid}, '{guid}', {duration}, '{call_type}', '{timestamp}')")
    return data

def generate_network_performance_data():
    timestamps = generate_timestamp()
    data = []
    for i in range(NUM_RECORDS):
        guid = random.choice(list(guid_to_cuid.keys()))
        cuid = guid_to_cuid[guid]
        download_speed = round(generate_anomalous_value((0.5, 100), (500, 1000)), 2)
        upload_speed = round(generate_anomalous_value((0.1, 50), (200, 500)), 2)
        latency = int(generate_anomalous_value((10, 1000), (2000, 5000)))
        timestamp = timestamps[i]
        data.append(f"({cuid}, '{guid}', {download_speed}, {upload_speed}, {latency}, '{timestamp}')")
    return data

def generate_data_usage():
    timestamps = generate_timestamp()
    data = []
    for i in range(NUM_RECORDS):
        guid = random.choice(list(guid_to_cuid.keys()))
        cuid = guid_to_cuid[guid]
        data_usage = round(generate_anomalous_value((0.1, 10), (50, 100)), 2)
        timestamp = timestamps[i]
        data.append(f"({cuid}, '{guid}', {data_usage}, '{timestamp}')")
    return data

def generate_tables():
    table_statements = [
        "-- Generate CDR table (Call Detail Records)",
        "CREATE TABLE cdr ( CUID Int32, GUID String, Call_Duration Int32, Call_Type String, Timestamp DateTime ) ENGINE = MergeTree ORDER BY (Timestamp, GUID);",
        "-- Generate network performance table",
        "CREATE TABLE network_performance ( CUID Int32, GUID String, Download_Speed Float32, Upload_Speed Float32, Latency Int32, Timestamp DateTime ) ENGINE = MergeTree ORDER BY (Timestamp, GUID);",
        "-- Generate data usage table",
        "CREATE TABLE data_usage ( CUID Int32, GUID String, Data_Usage Float32, Timestamp DateTime ) ENGINE = MergeTree ORDER BY (Timestamp, GUID);",
        "-- Create materialized view",
        "CREATE MATERIALIZED VIEW detailed_user_activity_mv ENGINE = MergeTree ORDER BY (CDR_Timestamp, CDR_GUID) AS\nSELECT\n    cdr.GUID AS \"CDR_GUID\",\n    cdr.Call_Duration AS \"Call_Duration\",\n    cdr.Call_Type AS \"Call_Type\",\n    cdr.Timestamp AS \"CDR_Timestamp\",\n    network_performance.GUID AS \"NP_GUID\",\n    network_performance.Download_Speed AS \"Download_Speed\",\n    network_performance.Upload_Speed AS \"Upload_Speed\",\n    network_performance.Latency AS \"Latency\",\n    network_performance.Timestamp AS \"NP_Timestamp\",\n    data_usage.GUID AS \"DU_GUID\",\n    data_usage.Data_Usage AS \"Data_Usage\",\n    data_usage.Timestamp AS \"DU_Timestamp\"\nFROM cdr\nLEFT JOIN network_performance ON cdr.GUID = network_performance.GUID AND date(cdr.Timestamp) = date(network_performance.Timestamp)\nLEFT JOIN data_usage ON cdr.GUID = data_usage.GUID AND date(cdr.Timestamp) = date(data_usage.Timestamp);",
    ]
    return "\n".join(table_statements)

def generate_sql():
    table_inserts = generate_tables()
    cdr_data = generate_cdr_data()
    network_data = generate_network_performance_data()
    data_usage_data = generate_data_usage()
    
    sql_statements = [
        table_inserts,
        "INSERT INTO cdr (CUID, GUID, Call_Duration, Call_Type, Timestamp) VALUES " + ", ".join(cdr_data) + ";",
        "INSERT INTO network_performance (CUID, GUID, Download_Speed, Upload_Speed, Latency, Timestamp) VALUES " + ", ".join(network_data) + ";",
        "INSERT INTO data_usage (CUID, GUID, Data_Usage, Timestamp) VALUES " + ", ".join(data_usage_data) + ";"
    ]
    return "\n".join(sql_statements)

# Generate SQL and save to file
sql_output = generate_sql()
with open('generated_data.sql', 'w') as file:
    file.write(sql_output)

print("Generated SQL saved to generated_data.sql")