SELECT
document_uuid,
embeddings <=> {{query_vector}}::vector as distance
FROM document_embeddings
ORDER BY distance ASC