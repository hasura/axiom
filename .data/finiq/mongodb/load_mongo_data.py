#!/usr/bin/env python3
"""
FinIQ MongoDB Data Loader
Loads generated JSON data into MongoDB collections
"""

import json
import pymongo
from pathlib import Path
import os
from datetime import datetime

# MongoDB connection configuration
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://admin:finiq123@localhost:27017/finiq?authSource=admin')
DATABASE_NAME = 'finiq'

# Data directory
DATA_DIR = Path('./data')

class MongoDataLoader:
    def __init__(self):
        print("Connecting to MongoDB...")
        try:
            self.client = pymongo.MongoClient(MONGO_URI)
            self.db = self.client[DATABASE_NAME]
            # Test the connection
            self.client.admin.command('ping')
            print(f"Successfully connected to MongoDB database: {DATABASE_NAME}")
        except Exception as e:
            print(f"Failed to connect to MongoDB: {e}")
            raise
    
    def load_collection(self, filename, collection_name):
        """Load JSON data into specified collection"""
        filepath = DATA_DIR / filename
        if not filepath.exists():
            print(f"Warning: File {filepath} does not exist, skipping...")
            return 0
        
        print(f"Loading {filename} into {collection_name} collection...")
        
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        if not data:
            print(f"No data found in {filename}")
            return 0
        
        # Clear existing data
        self.db[collection_name].delete_many({})
        
        # Insert new data
        if isinstance(data, list):
            result = self.db[collection_name].insert_many(data)
            count = len(result.inserted_ids)
        else:
            result = self.db[collection_name].insert_one(data)
            count = 1
        
        print(f"Successfully inserted {count} documents into {collection_name}")
        return count
    
    def create_indexes(self):
        """Create indexes for better performance"""
        print("Creating indexes...")
        
        # Customer Profiles indexes
        self.db.customer_profiles.create_index([("customer_name", 1)])
        self.db.customer_profiles.create_index([("email", 1)], unique=True)
        self.db.customer_profiles.create_index([("card_last_four", 1)])
        self.db.customer_profiles.create_index([("issuer_id", 1)])
        self.db.customer_profiles.create_index([("risk_score", 1)])
        
        # Merchant Risk Profiles indexes
        self.db.merchant_risk_profiles.create_index([("merchant_id", 1)], unique=True)
        self.db.merchant_risk_profiles.create_index([("risk_level", 1)])
        self.db.merchant_risk_profiles.create_index([("monitoring_status", 1)])
        
        # Fraud Alerts indexes
        self.db.fraud_alerts.create_index([("transaction_id", 1)])
        self.db.fraud_alerts.create_index([("status", 1)])
        self.db.fraud_alerts.create_index([("severity", 1)])
        self.db.fraud_alerts.create_index([("detected_at", 1)])
        
        # Transaction Notes indexes
        self.db.transaction_notes.create_index([("transaction_id", 1)])
        self.db.transaction_notes.create_index([("status", 1)])
        self.db.transaction_notes.create_index([("priority", 1)])
        
        # Audit Logs indexes
        self.db.audit_logs.create_index([("timestamp", 1)])
        self.db.audit_logs.create_index([("user", 1)])
        self.db.audit_logs.create_index([("action", 1)])
        
        print("Indexes created successfully!")
    
    def load_all_data(self):
        """Load all JSON files into MongoDB collections"""
        print("\n" + "="*60)
        print("FinIQ MongoDB Data Loader")
        print("="*60 + "\n")
        
        total_documents = 0
        
        # Define collections and their corresponding files
        collections = [
            ('customer_profiles.json', 'customer_profiles'),
            ('merchant_risk_profiles.json', 'merchant_risk_profiles'),
            ('fraud_alerts.json', 'fraud_alerts'),
            ('transaction_notes.json', 'transaction_notes'),
            ('audit_logs.json', 'audit_logs')
        ]
        
        for filename, collection_name in collections:
            try:
                count = self.load_collection(filename, collection_name)
                total_documents += count
            except Exception as e:
                print(f"Error loading {filename}: {e}")
        
        # Create indexes after loading data
        self.create_indexes()
        
        print("\n" + "="*60)
        print("MongoDB Data Loading Summary")
        print("="*60)
        print(f"Total documents loaded: {total_documents}")
        print(f"Collections: {len(collections)}")
        print(f"Database: {DATABASE_NAME}")
        print(f"Timestamp: {datetime.now().isoformat()}")
        print("="*60 + "\n")
    
    def close(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            print("MongoDB connection closed")

if __name__ == '__main__':
    loader = None
    try:
        loader = MongoDataLoader()
        loader.load_all_data()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if loader:
            loader.close()