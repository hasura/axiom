db = db.getSiblingDB(process.env.MONGO_INITDB_DATABASE);

db.dropAllUsers();

db.getSiblingDB(process.env.MONGO_INITDB_DATABASE).createUser({
    user: "presales",
    pwd: process.env.MONGO_INITDB_ROOT_PASSWORD,
    roles: [
        { role: "readWrite", db: process.env.MONGO_INITDB_DATABASE },
        { role: "dbAdmin", db: process.env.MONGO_INITDB_DATABASE }
    ]
});

// Create collections and load data
db.createCollection('accounts');
db.createCollection('aml_cases');
db.createCollection('sanctions');

try {
    const accountsData = cat("/docker-entrypoint-initdb.d/accounts.json");
    const amlCasesData = cat("/docker-entrypoint-initdb.d/transactions.json");
    const sanctionsData = cat("/docker-entrypoint-initdb.d/sanctions.json");

    db.accounts.insertMany(JSON.parse(accountsData));
    db.aml_cases.insertMany(JSON.parse(amlCasesData));
    db.sanctions.insertMany(JSON.parse(sanctionsData));
} catch (err) {
    print("Error loading JSON files: " + err);
}

// Create indexes for better performance
db.accounts.createIndex({ "account_id": 1 }, { unique: true });
db.aml_cases.createIndex({ "transaction_id": 1 }, { unique: true });
db.aml_cases.createIndex({ "originator_id": 1 });
db.aml_cases.createIndex({ "beneficiary_id": 1 });
db.aml_cases.createIndex({ "aml_flags.structuring": 1 });
db.aml_cases.createIndex({ "aml_flags.cross_border": 1 });
db.aml_cases.createIndex({ "aml_flags.darknet": 1 });
db.sanctions.createIndex({ "entity_name": 1 });