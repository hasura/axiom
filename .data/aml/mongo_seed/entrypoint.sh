#!/bin/bash
set -e  # Exit on any error

echo "⏳ Waiting for MongoDB to start..."
until mongosh "$DATABASE_URI" --quiet --eval "db.runCommand({ ping: 1 })" > /dev/null 2>&1; do
  sleep 2
done
echo "✅ MongoDB is up!"

# Function to import JSON files
import_json() {
  local collection=$1
  local file=$2
  
  if [[ -f "$file" ]]; then
    echo "🚀 Importing data into '$collection' from '$file'..."
    mongoimport --uri "$DATABASE_URI" --username "$USERNAME" --password "$PASSWORD" --collection "$collection" --drop --file "$file" --jsonArray
    echo "✅ Successfully imported '$collection'"
  else
    echo "❌ File '$file' not found! Skipping..."
  fi
}

# Import collections
import_json "accounts" "/accounts.json"
import_json "sanctions" "/sanctions.json"
import_json "aml_cases" "/aml_cases.json"

echo "🎉 MongoDB initialization complete!"
exec "$@"  # Run any additional commands passed to the container
