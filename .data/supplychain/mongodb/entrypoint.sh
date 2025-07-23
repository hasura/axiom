#!/bin/bash
set -e  # Exit on any error

# This script is executed by the MongoDB container during initialization
# The MongoDB server is already running when this script is executed

echo "🚀 Importing customer orders data..."
if [[ -f "/customer_orders.json" ]]; then
  # Use mongoimport with the environment variables provided by the MongoDB container
  mongoimport --db "$MONGO_INITDB_DATABASE" --collection customer_orders --drop --file /customer_orders.json --jsonArray
  echo "✅ Successfully imported customer orders"
else
  echo "❌ File '/customer_orders.json' not found! Skipping..."
fi

echo "🎉 MongoDB initialization complete!"