-- Staging table for COPY
DROP TABLE IF EXISTS pdf_chunks_stage;
CREATE TABLE pdf_chunks_stage (
  id text,
  pdf_id text,
  url text,
  chunk_index int,
  start_pos int,
  title text,
  text text,
  embedding_text text
);

-- COPY from the mounted CSV
-- NOTE: path is inside the container
COPY pdf_chunks_stage
FROM '/docker-entrypoint-initdb.d/embeddings_words10_overlap2.csv'
WITH (FORMAT csv, HEADER true, QUOTE '"');

-- Move into final table, casting the vector; skip empty embeddings
INSERT INTO pdf_chunks (id, pdf_id, url, chunk_index, start_pos, title, text, embedding)
SELECT
  id,
  pdf_id,
  url,
  chunk_index,
  start_pos,
  title,
  text,
  CASE
    WHEN embedding_text IS NULL OR embedding_text = '' THEN NULL
    ELSE embedding_text::vector
  END
FROM pdf_chunks_stage
ON CONFLICT (id) DO UPDATE
SET
  pdf_id = EXCLUDED.pdf_id,
  url = EXCLUDED.url,
  chunk_index = EXCLUDED.chunk_index,
  start_pos = EXCLUDED.start_pos,
  title = EXCLUDED.title,
  text = EXCLUDED.text,
  embedding = COALESCE(EXCLUDED.embedding, pdf_chunks.embedding);

-- Clean up (optional)
DROP TABLE pdf_chunks_stage;