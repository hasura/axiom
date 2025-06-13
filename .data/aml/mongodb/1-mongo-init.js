db = db.getSiblingDB(process.env.MONGO_INITDB_DATABASE);

db.dropAllUsers();

db.getSiblingDB(process.env.MONGO_INITDB_DATABASE).createUser({
    user: "presales",
    pwd: process.env.MONGO_INITDB_ROOT_PASSWORD,
    roles: [
        { role: "readWrite", db: process.env.MONGO_INITDB_DATABASE },
        { role: "dbAdmin", db: process.env.MONGO_INITDB_DATABASE },
        { role: "userAdmin", db: process.env.MONGO_INITDB_DATABASE }
    ]
});

// Create collections and load data
db.createCollection('accounts');
db.createCollection('aml_cases');
db.createCollection('sanctions');

// Create indexes for better performance
db.accounts.createIndex({ "account_id": 1 }, { unique: true });
db.aml_cases.createIndex({ "transaction_id": 1 }, { unique: true });
db.aml_cases.createIndex({ "originator_id": 1 });
db.aml_cases.createIndex({ "beneficiary_id": 1 });
db.aml_cases.createIndex({ "aml_flags.structuring": 1 });
db.aml_cases.createIndex({ "aml_flags.cross_border": 1 });
db.aml_cases.createIndex({ "aml_flags.darknet": 1 });
db.sanctions.createIndex({ "entity_name": 1 });