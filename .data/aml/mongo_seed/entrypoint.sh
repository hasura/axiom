#!/bin/bash
set -e  # Exit on any error

echo "⏳ Waiting for MongoDB to start..."
RETRY_COUNT=0
MAX_RETRIES=60

until mongosh "$DATABASE_URI" --quiet --eval "db.runCommand({ ping: 1 })" > /dev/null 2>&1; do
  RETRY_COUNT=$((RETRY_COUNT + 1))
  if [ $RETRY_COUNT -ge $MAX_RETRIES ]; then
    echo "❌ Failed to connect to MongoDB after $MAX_RETRIES attempts"
    exit 1
  fi
  echo "Attempt $RETRY_COUNT/$MAX_RETRIES - waiting for MongoDB..."
  sleep 3
done
echo "✅ MongoDB is up!"

# Wait a bit more for MongoDB initialization to complete
echo "⏳ Waiting for MongoDB initialization to complete..."
sleep 10

# Function to import JSON files
import_json() {
  local collection=$1
  local file=$2
  
  if [[ -f "$file" ]]; then
    echo "🚀 Importing data into '$collection' from '$file'..."
    mongoimport --uri "$DATABASE_URI" --username "$USERNAME" --password "$PASSWORD" --collection "$collection" --drop --file "$file" --jsonArray --authenticationDatabase aml
    echo "✅ Successfully imported '$collection'"
  else
    echo "❌ File '$file' not found! Skipping..."
  fi
}

# Import collections
import_json "accounts" "/accounts.json"
import_json "sanctions" "/sanctions.json"
import_json "aml_cases" "/aml_cases.json"

# Create read-only user
echo "👤 Creating read-only user..."
mongosh "$DATABASE_URI" --username "$USERNAME" --password "$PASSWORD" --quiet --authenticationDatabase aml --eval "
try {
  db.createUser({
    user: 'aml_readonly',
    pwd: '$READONLY_PASSWORD',
    roles: [
      {
        role: 'read',
        db: 'aml'
      }
    ]
  });
  print('✅ Read-only user aml_readonly created successfully');
} catch (error) {
  if (error.code === 51003) {
    print('ℹ️ Read-only user aml_readonly already exists');
  } else {
    print('❌ Error creating read-only user: ' + error.message);
    throw error;
  }
}
"

echo "🎉 MongoDB initialization complete!"
exec "$@"  # Run any additional commands passed to the container
