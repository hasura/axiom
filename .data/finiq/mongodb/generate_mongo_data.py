#!/usr/bin/env python3
"""
FinIQ - MongoDB Data Generator
Generates complementary unstructured data to enhance PostgreSQL transactional data
Includes: customer profiles, merchant reviews, fraud alerts, transaction notes, audit logs
"""

import json
import random
import string
from datetime import datetime, timedelta
from pathlib import Path
import csv

# Configuration
NUM_CUSTOMER_PROFILES = 5000
NUM_MERCHANT_RISK_PROFILES = 1000  # One per merchant
NUM_FRAUD_ALERTS = 500
NUM_TRANSACTION_NOTES = 1000
NUM_AUDIT_LOGS = 3000

# Date range
START_DATE = datetime(2024, 1, 1)
END_DATE = datetime(2025, 10, 15)

# Output directory
OUTPUT_DIR = Path("./data")
OUTPUT_DIR.mkdir(exist_ok=True)

# Read merchant and transaction IDs from PostgreSQL CSV files
POSTGRES_DIR = Path("../postgres/demo_data")


def load_ids_from_csv(filename, id_column):
    """Load IDs from PostgreSQL CSV files"""
    ids = []
    filepath = POSTGRES_DIR / filename
    if filepath.exists():
        with open(filepath, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                ids.append(row[id_column])
    return ids


def random_date(start, end):
    """Generate random datetime between start and end"""
    delta = end - start
    random_days = random.randint(0, delta.days)
    random_seconds = random.randint(0, 86400)
    return start + timedelta(days=random_days, seconds=random_seconds)


def random_phone():
    """Generate random phone number"""
    return f"+1-{random.randint(200,999)}-{random.randint(200,999)}-{random.randint(1000,9999)}"


def random_email(name):
    """Generate random email"""
    domains = ['gmail.com', 'yahoo.com', 'outlook.com', 'icloud.com', 'business.com']
    return f"{name.lower().replace(' ', '.')}@{random.choice(domains)}"


class MongoDataGenerator:
    def __init__(self):
        self.customer_profiles = []
        self.merchant_risk_profiles = []
        self.fraud_alerts = []
        self.transaction_notes = []
        self.audit_logs = []
        
        # Load IDs from PostgreSQL CSVs
        print("Loading IDs from PostgreSQL data...")
        self.merchant_ids = load_ids_from_csv('merchants.csv', 'merchant_id')
        self.auth_transaction_ids = load_ids_from_csv('auth_transactions.csv', 'transaction_id')
        self.issuer_ids = load_ids_from_csv('issuers.csv', 'issuer_id')
        
        print(f"Loaded {len(self.merchant_ids)} merchants, {len(self.auth_transaction_ids)} transactions")
        
        # Sample data
        self.first_names = [
            'James', 'Mary', 'John', 'Patricia', 'Robert', 'Jennifer', 'Michael',
            'Linda', 'William', 'Elizabeth', 'David', 'Barbara', 'Richard', 'Susan',
            'Joseph', 'Jessica', 'Thomas', 'Sarah', 'Charles', 'Karen'
        ]
        
        self.last_names = [
            'Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller',
            'Davis', 'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez',
            'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin'
        ]
        
        self.cities = [
            'New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia',
            'San Antonio', 'San Diego', 'Dallas', 'San Jose', 'Austin', 'Jacksonville',
            'Fort Worth', 'Columbus', 'San Francisco', 'Charlotte', 'Indianapolis',
            'Seattle', 'Denver', 'Boston'
        ]
        
        self.states = ['NY', 'CA', 'IL', 'TX', 'AZ', 'PA', 'FL', 'OH', 'WA', 'CO', 'MA']
        
        self.compliance_violations = [
            "Late settlement reporting",
            "Missing transaction documentation",
            "PCI-DSS non-compliance",
            "Excessive chargebacks",
            "AML reporting delay",
            "Know Your Customer (KYC) issues"
        ]
        
        self.red_flags = [
            "high_chargeback_rate",
            "unusual_refund_pattern",
            "frequent_amount_changes",
            "settlement_delays",
            "duplicate_transactions",
            "suspicious_velocity",
            "geographic_anomalies",
            "high_decline_rate"
        ]
        
        self.fraud_reasons = [
            "Unusual spending pattern detected",
            "Geographic anomaly - transaction from unexpected location",
            "Multiple rapid transactions",
            "High-value transaction outside normal range",
            "Card used in multiple locations simultaneously",
            "Merchant category mismatch with customer profile",
            "Transaction velocity exceeded threshold",
            "AVS mismatch on online transaction"
        ]
        
        self.note_types = [
            "Investigation", "Resolution", "Customer Contact", "Dispute",
            "Chargeback", "Reconciliation Issue", "Follow-up Required"
        ]
        
        self.user_actions = [
            "Logged in", "Viewed dashboard", "Ran report", "Exported data",
            "Updated settings", "Reviewed transaction", "Approved settlement",
            "Flagged transaction", "Added note", "Resolved issue"
        ]
    
    def generate_customer_profiles(self):
        """Generate customer profile documents"""
        print(f"Generating {NUM_CUSTOMER_PROFILES} customer profiles...")
        
        for i in range(NUM_CUSTOMER_PROFILES):
            first_name = random.choice(self.first_names)
            last_name = random.choice(self.last_names)
            full_name = f"{first_name} {last_name}"
            
            # Create realistic card numbers (last 4 digits)
            card_last_four = f"{random.randint(1000, 9999)}"
            
            profile = {
                "_id": f"CUST{str(i+1).zfill(8)}",
                "customer_name": full_name,
                "email": random_email(full_name),
                "phone": random_phone(),
                "card_last_four": card_last_four,
                "issuer_id": random.choice(self.issuer_ids) if self.issuer_ids else None,
                "address": {
                    "street": f"{random.randint(100, 9999)} {random.choice(['Main', 'Oak', 'Maple', 'Cedar', 'Elm'])} St",
                    "city": random.choice(self.cities),
                    "state": random.choice(self.states),
                    "zip": f"{random.randint(10000, 99999)}"
                },
                "account_opened": random_date(datetime(2020, 1, 1), datetime(2024, 12, 31)).isoformat(),
                "credit_limit": random.choice([5000, 10000, 15000, 25000, 50000]),
                "risk_score": random.randint(300, 850),
                "preferences": {
                    "email_alerts": random.choice([True, False]),
                    "sms_alerts": random.choice([True, False]),
                    "preferred_contact": random.choice(["email", "sms", "phone"])
                },
                "spending_patterns": {
                    "avg_monthly_spend": round(random.uniform(500, 5000), 2),
                    "frequent_categories": random.sample([
                        "GROCERY_STORES", "RESTAURANTS", "GAS_STATIONS", 
                        "ONLINE", "ENTERTAINMENT", "TRAVEL"
                    ], k=random.randint(2, 4)),
                    "typical_transaction_range": {
                        "min": round(random.uniform(5, 50), 2),
                        "max": round(random.uniform(200, 2000), 2)
                    }
                },
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
            
            self.customer_profiles.append(profile)
    
    def generate_merchant_risk_profiles(self):
        """Generate merchant risk profile documents - one per merchant"""
        print(f"Generating {NUM_MERCHANT_RISK_PROFILES} merchant risk profiles...")
        
        # Create a risk profile for each merchant
        for merchant_id in self.merchant_ids[:NUM_MERCHANT_RISK_PROFILES]:
            # Calculate risk metrics
            chargeback_rate = round(random.uniform(0.1, 2.5), 2)  # 0.1-2.5%
            fraud_incident_count = random.randint(0, 20)
            settlement_reliability = random.randint(70, 100)
            
            # Determine risk level based on metrics
            if chargeback_rate > 1.5 or fraud_incident_count > 10 or settlement_reliability < 80:
                risk_level = "HIGH"
                risk_score = random.randint(70, 100)
            elif chargeback_rate > 0.8 or fraud_incident_count > 5 or settlement_reliability < 90:
                risk_level = "MEDIUM"
                risk_score = random.randint(40, 69)
            else:
                risk_level = "LOW"
                risk_score = random.randint(0, 39)
            
            # Generate compliance violations (only for some merchants)
            violations = []
            if random.random() < 0.15:  # 15% have violations
                violations = random.sample(self.compliance_violations, k=random.randint(1, 2))
            
            # Generate red flags based on risk level
            num_flags = 0
            if risk_level == "HIGH":
                num_flags = random.randint(2, 4)
            elif risk_level == "MEDIUM":
                num_flags = random.randint(1, 2)
            else:
                num_flags = random.randint(0, 1)
            
            red_flags_list = random.sample(self.red_flags, k=num_flags) if num_flags > 0 else []
            
            # Assessment history
            assessment_history = []
            for i in range(random.randint(3, 8)):
                past_date = random_date(START_DATE, END_DATE)
                past_score = random.randint(
                    max(0, risk_score - 20),
                    min(100, risk_score + 20)
                )
                assessment_history.append({
                    "date": past_date.isoformat(),
                    "risk_score": past_score,
                    "analyst": random.choice(["risk_team_1", "risk_team_2", "risk_team_3"])
                })
            
            assessment_history.sort(key=lambda x: x["date"])
            
            profile = {
                "_id": f"MRISK{merchant_id[3:]}",  # Convert MER12345678 to MRISK12345678
                "merchant_id": merchant_id,
                "risk_score": risk_score,
                "risk_level": risk_level,
                "chargeback_rate": chargeback_rate,
                "chargeback_count_30d": random.randint(0, 50),
                "fraud_incident_count": fraud_incident_count,
                "fraud_loss_amount": round(random.uniform(0, 50000), 2) if fraud_incident_count > 0 else 0,
                "monthly_volume": round(random.uniform(10000, 500000), 2),
                "transaction_count_30d": random.randint(100, 5000),
                "avg_transaction_amount": round(random.uniform(25, 500), 2),
                "settlement_reliability_score": settlement_reliability,
                "settlement_delay_days": round(random.uniform(0, 5), 1),
                "decline_rate": round(random.uniform(1, 15), 2),
                "refund_rate": round(random.uniform(0.5, 8), 2),
                "compliance_violations": violations,
                "pci_compliance_status": random.choice([
                    "COMPLIANT", "COMPLIANT", "COMPLIANT",
                    "NON_COMPLIANT", "PENDING_REVIEW"
                ]),
                "last_pci_audit": random_date(datetime(2024, 1, 1), END_DATE).isoformat(),
                "monitoring_status": random.choice([
                    "active", "active", "active",
                    "enhanced", "under_review"
                ]),
                "red_flags": red_flags_list,
                "last_risk_assessment": random_date(datetime(2025, 8, 1), END_DATE).isoformat(),
                "next_review_date": random_date(END_DATE, datetime(2025, 12, 31)).isoformat(),
                "assessment_history": assessment_history,
                "notes": "Automated risk assessment" if risk_level == "LOW" else "Requires periodic review",
                "created_at": random_date(datetime(2023, 1, 1), datetime(2024, 1, 1)).isoformat(),
                "updated_at": datetime.now().isoformat()
            }
            
            self.merchant_risk_profiles.append(profile)
    
    def generate_fraud_alerts(self):
        """Generate fraud alert documents"""
        print(f"Generating {NUM_FRAUD_ALERTS} fraud alerts...")
        
        for i in range(NUM_FRAUD_ALERTS):
            severity = random.choice(["low", "medium", "high", "critical"])
            status = random.choice(["open", "investigating", "resolved", "false_positive"])
            
            alert = {
                "_id": f"FRAUD{str(i+1).zfill(8)}",
                "transaction_id": random.choice(self.auth_transaction_ids) if self.auth_transaction_ids else None,
                "customer_id": f"CUST{random.randint(1, NUM_CUSTOMER_PROFILES):08d}",
                "alert_type": random.choice([
                    "velocity_check", "geographic_anomaly", "amount_threshold",
                    "merchant_risk", "device_fingerprint", "behavioral_analysis"
                ]),
                "severity": severity,
                "risk_score": random.randint(1, 100),
                "reason": random.choice(self.fraud_reasons),
                "status": status,
                "detected_at": random_date(START_DATE, END_DATE).isoformat(),
                "resolved_at": random_date(START_DATE, END_DATE).isoformat() if status == "resolved" else None,
                "assigned_to": random.choice([
                    "fraud_team_1", "fraud_team_2", "fraud_team_3", None
                ]),
                "actions_taken": [
                    random.choice([
                        "Card temporarily blocked",
                        "Customer contacted",
                        "Merchant flagged",
                        "Transaction reversed",
                        "Additional verification required",
                        "No action needed"
                    ])
                ] if status != "open" else [],
                "false_positive": status == "false_positive",
                "notes": "Automated alert - requires investigation" if status == "open" else "Alert resolved",
                "metadata": {
                    "ip_address": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
                    "device_id": f"DEV{random.randint(1000000, 9999999)}",
                    "location": random.choice(self.cities)
                },
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
            
            self.fraud_alerts.append(alert)
    
    def generate_transaction_notes(self):
        """Generate transaction investigation notes"""
        print(f"Generating {NUM_TRANSACTION_NOTES} transaction notes...")
        
        for i in range(NUM_TRANSACTION_NOTES):
            note = {
                "_id": f"NOTE{str(i+1).zfill(8)}",
                "transaction_id": random.choice(self.auth_transaction_ids) if self.auth_transaction_ids else None,
                "note_type": random.choice(self.note_types),
                "author": random.choice([
                    "analyst_john", "analyst_sarah", "manager_mike",
                    "support_team", "reconciliation_team"
                ]),
                "content": random.choice([
                    "Customer confirmed transaction was legitimate",
                    "Settlement mismatch requires further investigation",
                    "Contacted merchant for clarification on amount difference",
                    "Chargeback initiated by cardholder",
                    "Reconciliation complete - variance explained by currency conversion",
                    "Dispute resolved in favor of merchant",
                    "Additional documentation requested from customer",
                    "Transaction appears to be fraudulent - card blocked",
                    "Settlement delayed due to merchant processing issues",
                    "Customer satisfied with resolution"
                ]),
                "priority": random.choice(["low", "medium", "high"]),
                "status": random.choice(["open", "in_progress", "resolved", "closed"]),
                "tags": random.sample([
                    "reconciliation", "dispute", "fraud", "customer-service",
                    "merchant-issue", "settlement-delay", "investigation"
                ], k=random.randint(1, 3)),
                "created_at": random_date(START_DATE, END_DATE).isoformat(),
                "updated_at": random_date(START_DATE, END_DATE).isoformat()
            }
            
            self.transaction_notes.append(note)
    
    def generate_audit_logs(self):
        """Generate system audit log documents"""
        print(f"Generating {NUM_AUDIT_LOGS} audit logs...")
        
        users = [
            "john.doe", "jane.smith", "mike.johnson", "sarah.williams",
            "david.brown", "emily.davis", "system_auto", "api_service"
        ]
        
        for i in range(NUM_AUDIT_LOGS):
            log = {
                "_id": f"LOG{str(i+1).zfill(8)}",
                "timestamp": random_date(START_DATE, END_DATE).isoformat(),
                "user": random.choice(users),
                "action": random.choice(self.user_actions),
                "resource_type": random.choice([
                    "transaction", "merchant", "customer", "report", "settings",
                    "settlement", "reconciliation", "alert"
                ]),
                "resource_id": random.choice(self.auth_transaction_ids) if random.random() > 0.5 and self.auth_transaction_ids else None,
                "ip_address": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
                "user_agent": random.choice([
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
                    "FinIQ-API/1.0",
                    "FinIQ-Mobile/2.1.0"
                ]),
                "success": random.choice([True, True, True, False]),  # 75% success rate
                "duration_ms": random.randint(50, 5000),
                "metadata": {
                    "session_id": f"SES{random.randint(100000, 999999)}",
                    "request_id": f"REQ{random.randint(1000000, 9999999)}"
                }
            }
            
            self.audit_logs.append(log)
    
    def write_json(self, filename, data):
        """Write data to JSON file"""
        filepath = OUTPUT_DIR / filename
        print(f"Writing {len(data)} documents to {filepath}...")
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def generate_all(self):
        """Generate all MongoDB collections"""
        print("\n" + "="*60)
        print("FinIQ MongoDB Data Generator")
        print("="*60 + "\n")
        
        # Generate all collections
        self.generate_customer_profiles()
        self.generate_merchant_risk_profiles()
        self.generate_fraud_alerts()
        self.generate_transaction_notes()
        self.generate_audit_logs()
        
        # Write to JSON files
        print("\nWriting JSON files...")
        
        self.write_json('customer_profiles.json', self.customer_profiles)
        self.write_json('merchant_risk_profiles.json', self.merchant_risk_profiles)
        self.write_json('fraud_alerts.json', self.fraud_alerts)
        self.write_json('transaction_notes.json', self.transaction_notes)
        self.write_json('audit_logs.json', self.audit_logs)
        
        print("\n" + "="*60)
        print("MongoDB Data Generation Summary")
        print("="*60)
        print(f"Customer Profiles: {len(self.customer_profiles)}")
        print(f"Merchant Risk Profiles: {len(self.merchant_risk_profiles)}")
        print(f"Fraud Alerts: {len(self.fraud_alerts)}")
        print(f"Transaction Notes: {len(self.transaction_notes)}")
        print(f"Audit Logs: {len(self.audit_logs)}")
        print(f"\nOutput directory: {OUTPUT_DIR.absolute()}")
        print("="*60 + "\n")


if __name__ == '__main__':
    generator = MongoDataGenerator()
    generator.generate_all()