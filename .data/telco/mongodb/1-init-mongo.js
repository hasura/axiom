db = db.getSiblingDB(process.env.MONGO_INITDB_DATABASE);

db.dropAllUsers();

db.getSiblingDB(process.env.MONGO_INITDB_DATABASE).createUser({
    user: "presales",
    pwd: process.env.MONGO_INITDB_ROOT_PASSWORD,
    roles: [
        { role: "readWrite", db: "holotel" },
        { role: "dbAdmin", db: "holotel" }
    ]
});

// Create userProfiles collection with schema validation
db.createCollection("userProfiles", {
    validator: {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["_id", "customer_id", "identification", "accountDetails", "preferences", "usageStats", "supportHistory", "notes", "memberID"],
            "properties": {
                "_id": {
                    "bsonType": "string",
                    "pattern": "^[a-f0-9]{32}$"
                },
                "customer_id": {
                    "bsonType": "number",
                },
                "identification": {
                    "bsonType": "object",
                    "required": ["type", "number", "issuedBy", "expiryDate"],
                    "properties": {
                        "type": {
                            "bsonType": "string"
                        },
                        "number": {
                            "bsonType": "string",
                            "pattern": "^[0-9A-F]{8}$"
                        },
                        "issuedBy": {
                            "bsonType": "string"
                        },
                        "expiryDate": {
                            "bsonType": "string"
                        }
                    }
                },
                "accountDetails": {
                    "bsonType": "object",
                    "required": ["accountNumber", "registrationDate"],
                    "properties": {
                        "accountNumber": {
                            "bsonType": "string"
                        },
                        "registrationDate": {
                            "bsonType": "string"
                        }
                    }
                },
                "preferences": {
                    "bsonType": "object",
                    "required": ["communication", "servicePreferences", "privacySettings"],
                    "properties": {
                        "communication": {
                            "bsonType": "object",
                            "required": ["emailUpdates", "smsNotifications", "appNotifications"],
                            "properties": {
                                "emailUpdates": {
                                    "bsonType": "bool"
                                },
                                "smsNotifications": {
                                    "bsonType": "bool"
                                },
                                "appNotifications": {
                                    "bsonType": "object",
                                    "required": ["enabled", "frequency"],
                                    "properties": {
                                        "enabled": {
                                            "bsonType": "bool"
                                        },
                                        "frequency": {
                                            "bsonType": "string",
                                            "enum": ["Daily", "Weekly", "Monthly"]
                                        }
                                    }
                                }
                            }
                        },
                        "servicePreferences": {
                            "bsonType": "object",
                            "required": ["favoriteLocations", "networkSettings"],
                            "properties": {
                                "favoriteLocations": {
                                    "bsonType": "array",
                                    "items": {
                                        "bsonType": "object",
                                        "required": ["name", "coordinates"],
                                        "properties": {
                                            "name": {
                                                "bsonType": "string"
                                            },
                                            "coordinates": {
                                                "bsonType": "object",
                                                "required": ["lat", "long"],
                                                "properties": {
                                                    "lat": {
                                                        "bsonType": "double"
                                                    },
                                                    "long": {
                                                        "bsonType": "double"
                                                    }
                                                }
                                            }
                                        }
                                    }
                                },
                                "networkSettings": {
                                    "bsonType": "object",
                                    "required": ["preferredNetworkType", "dataSaverMode"],
                                    "properties": {
                                        "preferredNetworkType": {
                                            "bsonType": "string",
                                            "enum": ["4G", "5G"]
                                        },
                                        "dataSaverMode": {
                                            "bsonType": "bool"
                                        }
                                    }
                                }
                            }
                        },
                        "privacySettings": {
                            "bsonType": "object",
                            "required": ["shareDataForImprovements", "adPersonalization"],
                            "properties": {
                                "shareDataForImprovements": {
                                    "bsonType": "bool"
                                },
                                "adPersonalization": {
                                    "bsonType": "bool"
                                }
                            }
                        }
                    }
                },
                "usageStats": {
                    "bsonType": "object",
                    "required": ["dataUsage", "callStats", "appUsage"],
                    "properties": {
                        "dataUsage": {
                            "bsonType": "object",
                            "required": ["total", "currentMonth"],
                            "properties": {
                                "total": {
                                    "bsonType": "string",
                                    "pattern": "^[0-9]+GB$"
                                },
                                "currentMonth": {
                                    "bsonType": "string",
                                    "pattern": "^[0-9]+GB$"
                                }
                            }
                        },
                        "callStats": {
                            "bsonType": "object",
                            "required": ["totalMinutes", "internationalMinutes"],
                            "properties": {
                                "totalMinutes": {
                                    "bsonType": "int"
                                },
                                "internationalMinutes": {
                                    "bsonType": "int"
                                }
                            }
                        },
                        "appUsage": {
                            "bsonType": "array",
                            "items": {
                                "bsonType": "object",
                                "required": ["name", "usage"],
                                "properties": {
                                    "name": {
                                        "bsonType": "string"
                                    },
                                    "usage": {
                                        "bsonType": "string",
                                        "pattern": "^[0-9]+GB$"
                                    }
                                }
                            }
                        }
                    }
                },
                "supportHistory": {
                    "bsonType": "array",
                    "items": {
                        "bsonType": "object",
                        "required": ["ticketId", "date", "issue", "status", "resolutionNotes"],
                        "properties": {
                            "ticketId": {
                                "bsonType": "string"
                            },
                            "date": {
                                "bsonType": "string"
                            },
                            "issue": {
                                "bsonType": "string"
                            },
                            "status": {
                                "bsonType": "string"
                            },
                            "resolutionNotes": {
                                "bsonType": "string"
                            }
                        }
                    }
                },
                "notes": {
                    "bsonType": "string"
                },
                "memberID": {
                    "bsonType": "string",
                    "pattern": "^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"
                }
            }
        }
    }
})
