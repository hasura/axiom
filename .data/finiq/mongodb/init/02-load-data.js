// FinIQ MongoDB Data Loading Script
// Automatically loads JSON data files during container initialization
// Similar to how PostgreSQL loads CSV data

print("Starting MongoDB data loading...");

db = db.getSiblingDB(process.env.MONGO_INITDB_DATABASE);

// Helper function to load JSON data from file
function loadCollectionData(filename, collectionName) {
    try {
        print(`Loading ${filename} into ${collectionName} collection...`);
        
        // Read the JSON file
        var data = cat(`/tmp/finiq-data/${filename}`);
        var jsonData = JSON.parse(data);
        
        if (!jsonData || jsonData.length === 0) {
            print(`No data found in ${filename}`);
            return 0;
        }
        
        // Clear existing data
        db[collectionName].deleteMany({});
        
        // Insert new data
        var result;
        if (Array.isArray(jsonData)) {
            result = db[collectionName].insertMany(jsonData);
            print(`Successfully inserted ${result.insertedIds.length} documents into ${collectionName}`);
            return result.insertedIds.length;
        } else {
            result = db[collectionName].insertOne(jsonData);
            print(`Successfully inserted 1 document into ${collectionName}`);
            return 1;
        }
        
    } catch (error) {
        print(`Error loading ${filename}: ${error}`);
        return 0;
    }
}

// Load all collections
var totalDocuments = 0;
var collections = [
    { file: 'customer_profiles.json', collection: 'customer_profiles' },
    { file: 'merchant_risk_profiles.json', collection: 'merchant_risk_profiles' },
    { file: 'fraud_alerts.json', collection: 'fraud_alerts' },
    { file: 'transaction_notes.json', collection: 'transaction_notes' },
    { file: 'audit_logs.json', collection: 'audit_logs' }
];

print("Loading MongoDB collections...");

collections.forEach(function(item) {
    var count = loadCollectionData(item.file, item.collection);
    totalDocuments += count;
});

print("Creating additional indexes for loaded data...");

// Additional performance indexes for the loaded data
db.customer_profiles.createIndex({ "preferences.spending_categories": 1 });
db.customer_profiles.createIndex({ "last_transaction_date": 1 });
db.merchant_risk_profiles.createIndex({ "last_risk_assessment": 1, "risk_level": 1 });
db.fraud_alerts.createIndex({ "transaction_id": 1, "status": 1 });
db.transaction_notes.createIndex({ "transaction_id": 1, "created_at": -1 });
db.audit_logs.createIndex({ "timestamp": -1, "action": 1 });

// Compound indexes for common query patterns
db.fraud_alerts.createIndex({ "status": 1, "severity": 1, "detected_at": -1 });
db.merchant_risk_profiles.createIndex({ "risk_level": 1, "monitoring_status": 1, "pci_compliance_status": 1 });
db.transaction_notes.createIndex({ "transaction_id": 1, "status": 1, "priority": 1 });

print("Additional indexes created!");

print("=====================================");
print("MongoDB Data Loading Summary");
print("=====================================");
print(`Total documents loaded: ${totalDocuments}`);
print(`Collections loaded: ${collections.length}`);
print(`Database: ${process.env.MONGO_INITDB_DATABASE}`);
print(`Timestamp: ${new Date().toISOString()}`);
print("=====================================");

// Verify data was loaded by showing collection counts
print("\nCollection Record Counts:");
collections.forEach(function(item) {
    var count = db[item.collection].countDocuments();
    print(`${item.collection}: ${count} documents`);
});

print("\nMongoDB data loading completed successfully!");