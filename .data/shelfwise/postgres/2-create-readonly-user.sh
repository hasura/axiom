#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
	-- Create read-only user with password (USER automatically creates a ROLE)
	CREATE USER shelfwise_readonly WITH PASSWORD '$READONLY_PASSWORD' NOCREATEDB NOCREATEROLE;
	
	-- Grant necessary permissions
	GRANT CONNECT ON DATABASE $POSTGRES_DB TO shelfwise_readonly;
	GRANT USAGE ON SCHEMA public TO shelfwise_readonly;
	GRANT SELECT ON ALL TABLES IN SCHEMA public TO shelfwise_readonly;
	ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO shelfwise_readonly;
	GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO shelfwise_readonly;
	ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT USAGE ON SEQUENCES TO shelfwise_readonly;
	REVOKE INSERT, UPDATE, DELETE, TRUNCATE ON ALL TABLES IN SCHEMA public FROM shelfwise_readonly;
	
	-- Add comment for documentation
	COMMENT ON ROLE shelfwise_readonly IS 'Read-only user for PromptQL queries and analytics';
EOSQL