#!/bin/bash

# =====================================================
# FinIQ - Financial Intelligence & Quality Platform
# Database: finiq (MongoDB)  
# Purpose: Automated data import using mongoimport
# Version: 3.0 (Fully automated for any environment)
# =====================================================

echo "Starting automated MongoDB data import..."

# Wait for MongoDB to be fully ready
sleep 10

# Get database name from environment variable
DB_NAME=${MONGO_INITDB_DATABASE:-finiq}
USERNAME=${MONGO_INITDB_ROOT_USERNAME:-admin}  
PASSWORD=${MONGO_INITDB_ROOT_PASSWORD:-finiq123}

echo "Importing data into database: $DB_NAME"

# Import customer profiles
echo "Importing customer_profiles..."
mongoimport --db $DB_NAME --collection customer_profiles \
  --file /tmp/finiq-data/customer_profiles.json \
  --jsonArray \
  --username $USERNAME \
  --password $PASSWORD \
  --authenticationDatabase admin \
  --quiet

# Import merchant risk profiles  
echo "Importing merchant_risk_profiles..."
mongoimport --db $DB_NAME --collection merchant_risk_profiles \
  --file /tmp/finiq-data/merchant_risk_profiles.json \
  --jsonArray \
  --username $USERNAME \
  --password $PASSWORD \
  --authenticationDatabase admin \
  --quiet

# Import fraud alerts
echo "Importing fraud_alerts..."
mongoimport --db $DB_NAME --collection fraud_alerts \
  --file /tmp/finiq-data/fraud_alerts.json \
  --jsonArray \
  --username $USERNAME \
  --password $PASSWORD \
  --authenticationDatabase admin \
  --quiet

# Import transaction notes
echo "Importing transaction_notes..."
mongoimport --db $DB_NAME --collection transaction_notes \
  --file /tmp/finiq-data/transaction_notes.json \
  --jsonArray \
  --username $USERNAME \
  --password $PASSWORD \
  --authenticationDatabase admin \
  --quiet

# Import audit logs
echo "Importing audit_logs..."
mongoimport --db $DB_NAME --collection audit_logs \
  --file /tmp/finiq-data/audit_logs.json \
  --jsonArray \
  --username $USERNAME \
  --password $PASSWORD \
  --authenticationDatabase admin \
  --quiet

echo ""
echo "Data import completed!"

# Verify import results
echo "Verifying import results..."
mongosh --username $USERNAME --password $PASSWORD --authenticationDatabase admin $DB_NAME --eval "
console.log('=== Final Import Status ===');
var collections = ['customer_profiles', 'merchant_risk_profiles', 'fraud_alerts', 'transaction_notes', 'audit_logs'];
var total = 0;
collections.forEach(function(c) { 
    var count = db[c].countDocuments();
    console.log(c + ':', count, 'documents');
    total += count;
});
console.log('Total MongoDB documents:', total);
console.log('MongoDB initialization completed successfully!');
"