// =====================================================
// FinIQ - Financial Intelligence & Quality Platform  
// Database: finiq (MongoDB)
// Purpose: Schema Creation - Collections, Indexes & Users
// Version: 2.0 (Consistent with PostgreSQL approach)
// =====================================================

print("Starting FinIQ MongoDB schema creation...");

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

// =====================================================
// Drop existing collections if they exist (for clean runs)
// =====================================================
db.customer_profiles.drop();
db.merchant_risk_profiles.drop();  
db.fraud_alerts.drop();
db.transaction_notes.drop();
db.audit_logs.drop();

// =====================================================
// Create Collections
// =====================================================
db.createCollection('customer_profiles');
db.createCollection('merchant_risk_profiles');
db.createCollection('fraud_alerts');
db.createCollection('transaction_notes');
db.createCollection('audit_logs');

print("Collections created successfully!");

// =====================================================
// Create Indexes for Performance  
// =====================================================
print("Creating indexes for optimal query performance...");

// Customer Profiles Indexes
// Note: _id index is automatically created by MongoDB as unique
db.customer_profiles.createIndex({ "customer_name": 1 });
db.customer_profiles.createIndex({ "email": 1 }, { unique: true });
db.customer_profiles.createIndex({ "card_last_four": 1 });
db.customer_profiles.createIndex({ "issuer_id": 1 });
db.customer_profiles.createIndex({ "risk_score": 1 });
db.customer_profiles.createIndex({ "address.city": 1 });
db.customer_profiles.createIndex({ "address.state": 1 });
db.customer_profiles.createIndex({ "preferences.spending_categories": 1 });
db.customer_profiles.createIndex({ "last_transaction_date": 1 });

// Merchant Risk Profiles Indexes
// Note: _id index is automatically created by MongoDB as unique
db.merchant_risk_profiles.createIndex({ "merchant_id": 1 }, { unique: true });
db.merchant_risk_profiles.createIndex({ "risk_level": 1 });
db.merchant_risk_profiles.createIndex({ "risk_score": 1 });
db.merchant_risk_profiles.createIndex({ "chargeback_rate": 1 });
db.merchant_risk_profiles.createIndex({ "monitoring_status": 1 });
db.merchant_risk_profiles.createIndex({ "pci_compliance_status": 1 });
db.merchant_risk_profiles.createIndex({ "last_risk_assessment": 1 });

// Fraud Alerts Indexes
// Note: _id index is automatically created by MongoDB as unique
db.fraud_alerts.createIndex({ "transaction_id": 1 });
db.fraud_alerts.createIndex({ "customer_id": 1 });
db.fraud_alerts.createIndex({ "alert_type": 1 });
db.fraud_alerts.createIndex({ "severity": 1 });
db.fraud_alerts.createIndex({ "status": 1 });
db.fraud_alerts.createIndex({ "detected_at": 1 });
db.fraud_alerts.createIndex({ "assigned_to": 1 });
db.fraud_alerts.createIndex({ "risk_score": 1 });

// Transaction Notes Indexes
// Note: _id index is automatically created by MongoDB as unique
db.transaction_notes.createIndex({ "transaction_id": 1 });
db.transaction_notes.createIndex({ "note_type": 1 });
db.transaction_notes.createIndex({ "author": 1 });
db.transaction_notes.createIndex({ "priority": 1 });
db.transaction_notes.createIndex({ "status": 1 });
db.transaction_notes.createIndex({ "tags": 1 });
db.transaction_notes.createIndex({ "created_at": 1 });

// Audit Logs Indexes
// Note: _id index is automatically created by MongoDB as unique
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
db.fraud_alerts.createIndex({ "transaction_id": 1, "status": 1 });
db.merchant_risk_profiles.createIndex({ "risk_level": 1, "monitoring_status": 1 });
db.merchant_risk_profiles.createIndex({ "last_risk_assessment": 1, "risk_level": 1 });
db.transaction_notes.createIndex({ "transaction_id": 1, "created_at": 1 });
db.transaction_notes.createIndex({ "transaction_id": 1, "status": 1, "priority": 1 });
db.audit_logs.createIndex({ "timestamp": 1, "user": 1, "success": 1 });
db.audit_logs.createIndex({ "timestamp": -1, "action": 1 });

print("Indexes created successfully!");

// =====================================================
// Comments for Documentation
// =====================================================
print("Adding collection documentation...");

// Note: MongoDB doesn't have built-in comment system like PostgreSQL
// Documentation is maintained in code comments and external docs

print("=====================================");
print("MongoDB Schema Creation Summary");
print("=====================================");
print("Collections created: 5");
print("- customer_profiles: Customer profile documents with personal information");
print("- merchant_risk_profiles: Merchant risk assessment profiles");  
print("- fraud_alerts: Fraud detection alerts and investigation status");
print("- transaction_notes: Investigation notes and comments");
print("- audit_logs: System audit logs and user activity tracking");
print("");
print("Indexes created: Comprehensive indexing for optimal performance");
print("Users created: finiq_app user with appropriate permissions");
print("Database:", process.env.MONGO_INITDB_DATABASE);
print("=====================================");

print("MongoDB schema creation completed successfully!");