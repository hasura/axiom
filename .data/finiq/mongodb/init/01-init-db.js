// FinIQ MongoDB Initialization Script
// Creates database, collections, and indexes for optimal performance

db = db.getSiblingDB(process.env.MONGO_INITDB_DATABASE);

// Drop existing users and recreate
db.dropAllUsers();

// Create application user with proper permissions
db.getSiblingDB(process.env.MONGO_INITDB_DATABASE).createUser({
    user: "finiq_app",
    pwd: process.env.MONGO_INITDB_ROOT_PASSWORD,
    roles: [
        { role: "readWrite", db: process.env.MONGO_INITDB_DATABASE },
        { role: "dbAdmin", db: process.env.MONGO_INITDB_DATABASE },
        { role: "userAdmin", db: process.env.MONGO_INITDB_DATABASE }
    ]
});

print("Creating FinIQ MongoDB collections...");

// Create collections
db.createCollection('customer_profiles');
db.createCollection('merchant_risk_profiles');
db.createCollection('fraud_alerts');
db.createCollection('transaction_notes');
db.createCollection('audit_logs');

print("Creating indexes for better performance...");

// Customer Profiles Indexes
db.customer_profiles.createIndex({ "_id": 1 }, { unique: true });
db.customer_profiles.createIndex({ "customer_name": 1 });
db.customer_profiles.createIndex({ "email": 1 }, { unique: true });
db.customer_profiles.createIndex({ "card_last_four": 1 });
db.customer_profiles.createIndex({ "issuer_id": 1 });
db.customer_profiles.createIndex({ "risk_score": 1 });
db.customer_profiles.createIndex({ "address.city": 1 });
db.customer_profiles.createIndex({ "address.state": 1 });

// Merchant Risk Profiles Indexes
db.merchant_risk_profiles.createIndex({ "_id": 1 }, { unique: true });
db.merchant_risk_profiles.createIndex({ "merchant_id": 1 }, { unique: true });
db.merchant_risk_profiles.createIndex({ "risk_level": 1 });
db.merchant_risk_profiles.createIndex({ "risk_score": 1 });
db.merchant_risk_profiles.createIndex({ "chargeback_rate": 1 });
db.merchant_risk_profiles.createIndex({ "monitoring_status": 1 });
db.merchant_risk_profiles.createIndex({ "pci_compliance_status": 1 });
db.merchant_risk_profiles.createIndex({ "last_risk_assessment": 1 });

// Fraud Alerts Indexes
db.fraud_alerts.createIndex({ "_id": 1 }, { unique: true });
db.fraud_alerts.createIndex({ "transaction_id": 1 });
db.fraud_alerts.createIndex({ "customer_id": 1 });
db.fraud_alerts.createIndex({ "alert_type": 1 });
db.fraud_alerts.createIndex({ "severity": 1 });
db.fraud_alerts.createIndex({ "status": 1 });
db.fraud_alerts.createIndex({ "detected_at": 1 });
db.fraud_alerts.createIndex({ "assigned_to": 1 });
db.fraud_alerts.createIndex({ "risk_score": 1 });

// Transaction Notes Indexes
db.transaction_notes.createIndex({ "_id": 1 }, { unique: true });
db.transaction_notes.createIndex({ "transaction_id": 1 });
db.transaction_notes.createIndex({ "note_type": 1 });
db.transaction_notes.createIndex({ "author": 1 });
db.transaction_notes.createIndex({ "priority": 1 });
db.transaction_notes.createIndex({ "status": 1 });
db.transaction_notes.createIndex({ "tags": 1 });
db.transaction_notes.createIndex({ "created_at": 1 });

// Audit Logs Indexes
db.audit_logs.createIndex({ "_id": 1 }, { unique: true });
db.audit_logs.createIndex({ "timestamp": 1 });
db.audit_logs.createIndex({ "user": 1 });
db.audit_logs.createIndex({ "action": 1 });
db.audit_logs.createIndex({ "resource_type": 1 });
db.audit_logs.createIndex({ "resource_id": 1 });
db.audit_logs.createIndex({ "success": 1 });
db.audit_logs.createIndex({ "user": 1, "timestamp": 1 });

// Compound indexes for common query patterns
db.fraud_alerts.createIndex({ "status": 1, "severity": 1 });
db.fraud_alerts.createIndex({ "detected_at": 1, "status": 1 });
db.merchant_risk_profiles.createIndex({ "risk_level": 1, "monitoring_status": 1 });
db.transaction_notes.createIndex({ "transaction_id": 1, "created_at": 1 });
db.audit_logs.createIndex({ "timestamp": 1, "user": 1, "success": 1 });

print("MongoDB initialization completed successfully!");
print("Collections created: customer_profiles, merchant_risk_profiles, fraud_alerts, transaction_notes, audit_logs");
print("Indexes created for optimal query performance");