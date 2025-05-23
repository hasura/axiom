
CREATE TABLE documents (
    uuid UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    status TEXT,
    language TEXT,
    view_count INTEGER,
    rating INTEGER,
    title TEXT,
    body TEXT,
    tags TEXT
);

CREATE TABLE document_embeddings (
    document_uuid UUID PRIMARY KEY REFERENCES documents(uuid) ON DELETE CASCADE,
    embeddings vector(1536)
);

\COPY documents FROM '/docker-entrypoint-initdb.d/documents.csv' WITH (FORMAT csv, HEADER true);
\COPY document_embeddings FROM '/docker-entrypoint-initdb.d/document_embeddings.csv' WITH (FORMAT csv, HEADER true);
