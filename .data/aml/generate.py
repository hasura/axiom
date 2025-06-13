import random
import pandas as pd
from datetime import datetime, timedelta
import json
import uuid
from faker import Faker

# Initialize Faker
fake = Faker()

# Constants
CURRENT_DATE = datetime.today()
COUNTRIES = ["USA", "Canada", "UK", "Germany", "South Africa", "Cuba", "Iran", "Russia"]
HIGH_RISK_COUNTRIES = ["Cuba", "Iran", "Russia"]
CURRENCIES = ["USD", "CAD", "EUR", "ZAR", "BTC"]
PAYMENT_TYPES = ["wire", "check", "cash", "crypto"]
RISK_LEVELS = ["low", "medium", "high"]

# Generate customers/accounts with Faker
def generate_customers(num_customers=50):
    customers = []
    accounts = []
    for i in range(num_customers):
        account_id = 10000 + i
        name = fake.name() if random.random() < 0.8 else fake.company()  # 80% individuals, 20% companies
        dob = CURRENT_DATE - timedelta(days=random.randint(20*365, 60*365))
        nationality = random.choices(COUNTRIES, weights=[30, 20, 20, 20, 5, 2, 2, 1], k=1)[0]
        address = fake.address().replace("\n", ", ")  # Realistic multi-line address
        risk = random.choices(RISK_LEVELS, weights=[70, 20, 10], k=1)[0]
        pep = random.random() < 0.05  # 5% PEP chance
        blacklisted = nationality in HIGH_RISK_COUNTRIES and random.random() < 0.2
        
        customers.append({
            "customer_id": i + 1,
            "name": name,
            "account": account_id,
            "dob": dob.strftime("%Y-%m-%d"),
            "nationality": nationality,
            "address": address,
            "risk_level": risk,
            "pep_status": pep,
            "blacklisted": blacklisted
        })
        accounts.append({
            "account_id": account_id,
            "name": name,
            "entity_type": "individual" if "Inc" not in name and "Ltd" not in name else "company",
            "contact_information": {
                "address": address,
                "phone_number": fake.phone_number(),
                "email": fake.email()
            },
            "risk": risk,
            "transaction_limits": {
                "max_transaction_limit": 10000 if risk != "high" else 5000,
                "max_num_transactions": 5 if risk != "high" else 3
            }
        })
    return customers, accounts

# Generate transactions (mostly normal, few suspicious)
def generate_transactions(customers, num_transactions=200):
    pg_transactions = []
    mongo_transactions = []
    suspicious_accounts = [c["account"] for c in customers if c["risk_level"] == "high" or c["blacklisted"] or c["pep_status"]]
    
    for i in range(num_transactions):
        sender = random.choice(customers)
        receiver = random.choice([c for c in customers if c["account"] != sender["account"]])
        date = CURRENT_DATE - timedelta(days=random.randint(1, 90))
        time = f"{random.randint(0,23):02d}:{random.randint(0,59):02d}"
        amount = random.uniform(100, 5000)  # Normal range
        payment_currency = random.choices(CURRENCIES, weights=[40, 30, 25, 4, 1], k=1)[0]
        received_currency = payment_currency
        payment_type = random.choices(PAYMENT_TYPES, weights=[50, 30, 15, 5], k=1)[0]
        sender_location = sender["nationality"]
        receiver_location = receiver["nationality"]
        
        # Suspicious patterns (10-15% chance, tied to risky accounts)
        is_laundering = False
        laundering_type = "none"
        aml_flags = {"structuring": False, "cross_border": False, "darknet": False}
        
        if random.random() < 0.15 and (sender["account"] in suspicious_accounts or receiver["account"] in suspicious_accounts):
            if payment_type == "cash" and amount < 2000 and random.random() < 0.4:  # Structuring
                amount = random.uniform(500, 1900)
                is_laundering = True
                laundering_type = "structuring"
                aml_flags["structuring"] = True
            elif sender["nationality"] in HIGH_RISK_COUNTRIES or receiver["nationality"] in HIGH_RISK_COUNTRIES:  # Cross-border
                received_currency = random.choice(CURRENCIES)
                is_laundering = random.random() < 0.6
                laundering_type = "cross_border" if is_laundering else "none"
                aml_flags["cross_border"] = True
                sender_location = random.choice(HIGH_RISK_COUNTRIES)
                receiver_location = random.choice(HIGH_RISK_COUNTRIES)
            elif payment_type == "crypto" and random.random() < 0.7:  # Darknet
                amount = random.uniform(50, 1000)
                is_laundering = True
                laundering_type = "darknet"
                aml_flags["darknet"] = True
        
        transaction_id = 1000 + i
        pg_transactions.append({
            "transaction_id": transaction_id,
            "time": time,
            "date": date.strftime("%Y-%m-%d"),
            "sender_account": sender["account"],
            "receiver_account": receiver["account"],
            "amount": round(amount, 2),
            "payment_currency": payment_currency,
            "received_currency": received_currency,
            "sender_bank_location": sender_location,
            "receiver_bank_location": receiver_location,
            "payment_type": payment_type,
            "is_laundering": is_laundering,
            "laundering_type": laundering_type
        })
        mongo_transactions.append({
            "transaction_id": transaction_id,
            "transaction_date": date.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
            "originator_id": sender["account"],
            "originator_name": sender["name"],
            "originator_address": sender["address"],
            "beneficiary_id": receiver["account"],
            "beneficiary_name": receiver["name"],
            "beneficiary_address": receiver["address"],
            "amount": round(amount, 2),
            "aml_flags": aml_flags
        })
    return pg_transactions, mongo_transactions

# Generate SARs (only for suspicious transactions)
def generate_sars(customers, transactions):
    sars = []
    laundering_transactions = [t for t in transactions if t["is_laundering"]]
    for i, tx in enumerate(laundering_transactions[:min(10, len(laundering_transactions))]):
        customer = next(c for c in customers if c["account"] == tx["sender_account"])
        reason = {
            "structuring": "Multiple small cash deposits below $2,000 threshold detected.",
            "cross_border": f"High-risk cross-border transfer to {tx['receiver_bank_location']}.",
            "darknet": "Cryptocurrency transaction with potential darknet association."
        }.get(tx["laundering_type"], "Suspicious activity detected.")
        
        sars.append({
            "sar_id": i + 1,
            "customer_id": customer["customer_id"],
            "transaction_id": tx["transaction_id"],
            "reason": reason,
            "status": random.choice(["pending", "filed"]),
            "filed_date": CURRENT_DATE.strftime("%Y-%m-%d %H:%M:%S")
        })
    return sars

# Generate sanctions with Faker
def generate_sanctions(num_sanctions=5):
    sanctions = []
    for i in range(num_sanctions):
        name = fake.name() if random.random() < 0.5 else fake.company()
        sanctions.append({
            "_id": str(uuid.uuid4()),
            "entity_name": name,
            "entity_type": "individual" if "Inc" not in name and "Ltd" not in name else "company",
            "address": fake.address().replace("\n", ", ") + f", {random.choice(HIGH_RISK_COUNTRIES)}",
            "listed_date": (CURRENT_DATE - timedelta(days=random.randint(365, 5*365))).strftime("%Y-%m-%dT00:00:00.000Z"),
            "program": random.choice(["OFAC-SDN", "UN-Sanctions", "EU-Restrictive"]),
            "list_type": random.choice(["OFAC", "UN", "EU"])
        })
    return sanctions

# Main execution
customers, accounts = generate_customers(1000)
pg_transactions, mongo_transactions = generate_transactions(customers, 10000)
sars = generate_sars(customers, pg_transactions)
sanctions = generate_sanctions(100)

# Save PostgreSQL data as CSV
pd.DataFrame(customers).to_csv("postgres/customers.csv", index=False)
pd.DataFrame(pg_transactions).to_csv("postgres/financial_transfers.csv", index=False)
pd.DataFrame(sars).to_csv("postgres/sars.csv", index=False)

# Save MongoDB data as JSON
with open("mongo_seed/accounts.json", "w") as f:
    json.dump(accounts, f, indent=2)
with open("mongo_seed/aml_cases.json", "w") as f:
    json.dump(mongo_transactions, f, indent=2)
with open("mongo_seed/sanctions.json", "w") as f:
    json.dump(sanctions, f, indent=2)

print("Data generation complete. Files saved: customers.csv, financial_transfers.csv, sars.csv, accounts.json, aml_cases.json, sanctions.json")
