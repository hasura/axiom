CREATE DATABASE emergent_metadata_main;

CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- CREATE EXTENSION IF NOT EXISTS anon CASCADE;
-- SELECT anon.start_dynamic_masking();
-- SECURITY LABEL FOR anon ON ROLE postgres IS 'MASKED';

-- CREATE USER demo;
-- CREATE DATABASE hasura_demo;
-- GRANT ALL PRIVILEGES ON DATABASE hasura_demo TO postgres;