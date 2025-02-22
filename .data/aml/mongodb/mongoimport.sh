#!/bin/bash
set -e

echo "Starting MongoDB restore..."

DB_NAME="aml"
INITDB_DIR="/docker-entrypoint-initdb.d"

for bson_file in "$INITDB_DIR"/*.bson; do
    collection_name=$(basename "$bson_file" .bson)
    echo "Restoring collection: $collection_name"
    mongorestore --db="$DB_NAME" --collection="$collection_name" "$bson_file"
done

echo "MongoDB restore completed successfully."
