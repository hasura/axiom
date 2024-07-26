#!/usr/bin/env bash

# Function to display usage information
usage() {
    echo "Usage: $0 -s SUBGRAPH -c CONNECTOR -u DB_URI -h HASURA_URL"
    echo
    echo "Example:"
    echo "$0 -s my_subgraph -c my_mongo -u \"mongodb+srv://username:password@cluster.mongodb.net/sample_analytics\" -h \"http://local.hasura.dev:8082\""
    exit 1
}

# Function to check if ddn is installed
check_ddn_installed() {
    if ! command -v ddn &> /dev/null; then
        echo "ddn is not installed or not in your PATH. Please install ddn and ensure it's in your PATH."
        exit 1
    fi
}

# Check if ddn is installed
check_ddn_installed

# Parse command-line arguments
while getopts "s:c:u:h:" opt; do
    case $opt in
        s) SUBGRAPH=$OPTARG ;;
        c) CONNECTOR=$OPTARG ;;
        u) DB_URI=$OPTARG ;;
        h) HASURA_URL=$OPTARG ;;
        *) usage ;;
    esac
done

# Check if all required arguments are provided
if [ -z "$SUBGRAPH" ] || [ -z "$CONNECTOR" ] || [ -z "$DB_URI" ] || [ -z "$HASURA_URL" ]; then
    usage
fi

# Convert SUBGRAPH and CONNECTOR to uppercase
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

# Initialize the connector
ddn connector init "$CONNECTOR" --subgraph "$SUBGRAPH" --hub-connector hasura/mongodb

# Append MongoDB URI to the local environment file
echo "\nMONGODB_DATABASE_URI=\"$DB_URI\"" >> "$DEMO_DIR/$SUBGRAPH/connector/$CONNECTOR/.env.local"

# Introspect the connector
ddn connector introspect --connector "$DEMO_DIR/$SUBGRAPH/connector/$CONNECTOR/connector.yaml"

# Add the connector link
ddn connector-link add "$CONNECTOR"

# Copy docker-compose files
cp "$SCRIPT_DIR/$CONNECTOR-docker-compose.hasura.yaml" "$DEMO_DIR/docker-compose.hasura.yaml"
cp "$SCRIPT_DIR/8082-docker-compose.$CONNECTOR.yaml" "$DEMO_DIR/$SUBGRAPH/connector/$CONNECTOR/"

# Append URLs to the subgraph's environment file
echo "${READ_URL}" >> "$DEMO_DIR/$SUBGRAPH/.env.$SUBGRAPH"
echo "${WRITE_URL}" >> "$DEMO_DIR/$SUBGRAPH/.env.$SUBGRAPH"

# Start the Docker Compose watch
HASURA_DDN_PAT=$(ddn auth print-pat) docker compose -f "$DEMO_DIR/docker-compose.hasura.yaml" watch &

# Uncomment if needed
# ddn connector-link update "$CONNECTOR" --subgraph "$SUBGRAPH" --add-all-resources

# Add the model to the connector link
ddn model add --connector-link "$CONNECTOR" --name transactions

# Build the supergraph
ddn supergraph build local --output-dir "$DEMO_DIR/engine"

