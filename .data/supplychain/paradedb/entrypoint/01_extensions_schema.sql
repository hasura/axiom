-- Extensions
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS pg_search;

-- Final table
CREATE TABLE IF NOT EXISTS pdf_chunks (
  id          text PRIMARY KEY,
  pdf_id      text NOT NULL,
  url         text NOT NULL,
  chunk_index int  NOT NULL,
  start_pos   int  NOT NULL,
  title       text,
  text        text NOT NULL,
  tsv         tsvector,
  embedding   vector(1024),
  created_at  timestamptz DEFAULT now()
);

-- -- Auto-populate tsv
-- CREATE OR REPLACE FUNCTION chunks_tsv_trigger() RETURNS trigger AS $$
-- BEGIN
--   NEW.tsv := to_tsvector('english',
--               coalesce(NEW.title,'') || ' ' || coalesce(NEW.text,''));
--   RETURN NEW;
-- END
-- $$ LANGUAGE plpgsql;

-- DROP TRIGGER IF EXISTS tsvupdate ON pdf_chunks;
-- CREATE TRIGGER tsvupdate BEFORE INSERT OR UPDATE
-- ON pdf_chunks FOR EACH ROW EXECUTE FUNCTION chunks_tsv_trigger();

-- -- Indexes
-- CREATE INDEX IF NOT EXISTS idx_chunks_tsv ON pdf_chunks USING GIN (tsv);
-- CREATE INDEX IF NOT EXISTS idx_chunks_embed_hnsw
--   ON pdf_chunks USING hnsw (embedding vector_cosine_ops);