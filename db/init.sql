-- Runs once, the first time the database is created.
-- Turns on the pgvector add-on so we can store and search embeddings.
CREATE EXTENSION IF NOT EXISTS vector;
