// Load customer preferences data from JSON file
const customerPreferencesData = JSON.parse(cat('/docker-entrypoint-initdb.d/customer_preferences.json'));

db.createCollection("customerPreferences", {
    validator: {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["customer_guid", "preferences", "behavioralData", "customerNotes"],
            "properties": {
                "customer_guid": {
                    "bsonType": "string",
                    "description": "must be a string and is required"
                },
                "preferences": {
                    "bsonType": "object",
                    "required": ["contactMethod", "marketingOptIn"],
                    "properties": {
                        "contactMethod": {
                            "bsonType": "string",
                            "enum": ["email", "phone", "SMS"],
                            "description": "must be one of 'email', 'phone', or 'SMS' and is required"
                        },
                        "marketingOptIn": {
                            "bsonType": "bool",
                            "description": "must be a boolean value and is required"
                        }
                    }
                },
                "socialMedia": {
                    "bsonType": "object",
                    "properties": {
                        "facebook": {
                            "bsonType": "string",
                            "pattern": "^(https?:\\/\\/)?(www\\.)?facebook.com\\/.*$",
                            "description": "must be a valid Facebook URL"
                        },
                        "twitter": {
                            "bsonType": "string",
                            "pattern": "^(https?:\\/\\/)?(www\\.)?twitter.com\\/.*$",
                            "description": "must be a valid Twitter URL"
                        },
                        "linkedin": {
                            "bsonType": "string",
                            "pattern": "^(https?:\\/\\/)?(www\\.)?linkedin.com\\/.*$",
                            "description": "must be a valid LinkedIn URL"
                        }
                    },
                    "description": "socialMedia is an object containing social media profile URLs"
                },
                "behavioralData": {
                    "bsonType": "object",
                    "required": ["lastWebsiteVisit", "lastAppLogin"],
                    "properties": {
                        "lastWebsiteVisit": {
                            "bsonType": "string",
                            "description": "must be a valid ISO date and is required"
                        },
                        "lastAppLogin": {
                            "bsonType": "string",
                            "description": "must be a valid ISO date and is required"
                        }
                    },
                    "description": "behavioralData is an object containing behavioral metrics"
                },
                "customerNotes": {
                    "bsonType": "array",
                    "items": {
                        "bsonType": "object",
                        "required": ["author", "date", "content"],
                        "properties": {
                            "author": {
                                "bsonType": "string",
                                "description": "must be a string and is required"
                            },
                            "date": {
                                "bsonType": "string",
                                "description": "must be a valid ISO date and is required"
                            },
                            "content": {
                                "bsonType": "string",
                                "description": "must be a string and is required"
                            }
                        }
                    },
                    "description": "customerNotes is an array of note objects with author, date, and content"
                }
            }
        }
    }
})
db.getSiblingDB(process.env.MONGO_INITDB_DATABASE).customerPreferences.insertMany(customerPreferencesData);
