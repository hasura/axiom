#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
	-- Create read-only user with password (USER automatically creates a ROLE)
	CREATE USER aml_readonly WITH PASSWORD '$READONLY_PASSWORD' NOCREATEDB NOCREATEROLE;
	
	-- Grant necessary permissions
	GRANT CONNECT ON DATABASE $POSTGRES_DB TO aml_readonly;
	GRANT USAGE ON SCHEMA public TO aml_readonly;
	GRANT SELECT ON ALL TABLES IN SCHEMA public TO aml_readonly;
	ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO aml_readonly;
EOSQL