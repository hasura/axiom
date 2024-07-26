#!/usr/bin/env bash

# Function to display usage information
usage() {
    echo "Usage: $0 -s ::SUBGRAPH:: -c ::CONNECTOR:: -d ::DB_TYPE:: -u ::DB_URI:: -h ::HASURA_URL:: [-n ::CLICKHOUSE_USERNAME:: -p ::CLICKHOUSE_PASSWORD::]"
    echo
    echo "Example for MongoDB:"
    echo "$0 -s my_subgraph -c my_mongo -d mongodb -u \"mongodb+srv://username:password@cluster.mongodb.net/sample_analytics\" -h \"http://local.hasura.dev:8082\""
    echo
    echo "Example for PostgreSQL:"
    echo "$0 -s my_subgraph -c my_postgres -d postgres -u \"postgres://username:password@host:port/dbname\" -h \"http://local.hasura.dev:8082\""
    echo
    echo "Example for ClickHouse:"
    echo "$0 -s my_subgraph -c my_clickhouse -d clickhouse -u \"https://host\" -h \"http://local.hasura.dev:8082\" -n clickhouse_username -p clickhouse_password"
    exit 1
}

# Function to check if ddn is installed
check_ddn_installed() {
    if ! command -v ddn &> /dev/null; then
        echo "ddn is not installed or not in your PATH. Please install ddn and ensure it's in your PATH."
        exit 1
    fi
}

# Function to initialize the connector
initialize_connector() {
    ddn connector init "$CONNECTOR" --subgraph "$SUBGRAPH" --hub-connector "hasura/$DB_TYPE" || {
        echo "Failed to initialize connector."
        exit 1
    }
}

# Function to update environment variables
update_env_variables() {
    local env_file="$DEMO_DIR/$SUBGRAPH/connector/$CONNECTOR/.env.local"

    case $DB_TYPE in
        mongodb)
            echo "\nMONGODB_DATABASE_URI=\"$DB_URI\"" >> "$env_file"
            ;;
        postgres)
            echo "\nCONNECTION_URI=\"$DB_URI\"" >> "$env_file"
            ;;
        clickhouse)
            if [[ -z "$CLICKHOUSE_USERNAME" || -z "$CLICKHOUSE_PASSWORD" ]]; then
                echo "ClickHouse requires both username and password."
                usage
            fi
            echo "\nCLICKHOUSE_URL=\"$DB_URI\"" >> "$env_file"
            echo "CLICKHOUSE_USERNAME=\"$CLICKHOUSE_USERNAME\"" >> "$env_file"
            echo "CLICKHOUSE_PASSWORD=\"$CLICKHOUSE_PASSWORD\"" >> "$env_file"
            ;;
        *)
            echo "Unsupported DB_TYPE: $DB_TYPE"
            exit 1
            ;;
    esac
}

# Function to manage Docker configurations
manage_docker_configs() {
    cp "$SCRIPT_DIR/$CONNECTOR-docker-compose.hasura.yaml" "$DEMO_DIR/docker-compose.hasura.yaml"
    cp "$SCRIPT_DIR/8082-docker-compose.$CONNECTOR.yaml" "$DEMO_DIR/$SUBGRAPH/connector/$CONNECTOR/"
}

# Parse command-line arguments
while getopts "s:c:d:u:h:n:p:" opt; do
    case $opt in
        s) SUBGRAPH=$OPTARG ;;
        c) CONNECTOR=$OPTARG ;;
        d) DB_TYPE=$OPTARG ;;
        u) DB_URI=$OPTARG ;;
        h) HASURA_URL=$OPTARG ;;
        n) CLICKHOUSE_USERNAME=$OPTARG ;;
        p) CLICKHOUSE_PASSWORD=$OPTARG ;;
        *) usage ;;
    esac
done

# Check if all required arguments are provided
if [[ -z "$SUBGRAPH" || -z "$CONNECTOR" || -z "$DB_TYPE" || -z "$DB_URI" || -z "$HASURA_URL" ]]; then
    usage
fi

# Convert SUBGRAPH and CONNECTOR to uppercase for consistent naming
UPPER_SUBGRAPH=$(echo "${SUBGRAPH}" | tr '[:lower:]' '[:upper:]')
UPPER_CONNECTOR=$(echo "${CONNECTOR}" | tr '[:lower:]' '[:upper:]')

# Output URLs
READ_URL="${UPPER_SUBGRAPH}_${UPPER_CONNECTOR}_READ_URL=${HASURA_URL}"
WRITE_URL="${UPPER_SUBGRAPH}_${UPPER_CONNECTOR}_WRITE_URL=${HASURA_URL}"

echo "${READ_URL}"
echo "${WRITE_URL}"

# Determine the script's directory and set relative paths
SCRIPT_DIR=$(dirname "$0")
DEMO_DIR=$(realpath "$SCRIPT_DIR/../..")

# Check if ddn is installed
check_ddn_installed

# Initialize the connector
initialize_connector

# Update environment variables based on the DB_TYPE
update_env_variables

# Introspect the connector
ddn connector introspect --connector "$DEMO_DIR/$SUBGRAPH/connector/$CONNECTOR/connector.yaml" || {
    echo "Failed to introspect connector."
    exit 1
}

# Add the connector link
ddn connector-link add "$CONNECTOR" || {
    echo "Failed to add connector link."
    exit 1
}

# Manage Docker configurations
manage_docker_configs

# Append URLs to the subgraph's environment file
echo "${READ_URL}" >> "$DEMO_DIR/$SUBGRAPH/.env.$SUBGRAPH"
echo "${WRITE_URL}" >> "$DEMO_DIR/$SUBGRAPH/.env.$SUBGRAPH"

# Start the Docker Compose watch
HASURA_DDN_PAT=$(ddn auth print-pat) docker compose -f "$DEMO_DIR/docker-compose.hasura.yaml" watch &

# Uncomment if needed
# ddn connector-link update "$CONNECTOR" --subgraph "$SUBGRAPH" --add-all-resources

# Add the model to the connector link
ddn model add --connector-link "$CONNECTOR" --name transactions || {
    echo "Failed to add model."
    exit 1
}

# Build the supergraph
ddn supergraph build local --output-dir "$DEMO_DIR/engine" || {
    echo "Failed to build supergraph."
    exit 1
}

