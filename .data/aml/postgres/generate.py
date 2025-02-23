import csv
import random
import datetime
from faker import Faker

# Initialize Faker for random data generation
fake = Faker()

# Number of records to generate
NUM_CUSTOMERS = 100000
NUM_SARS = 50000

# Risk levels and statuses
RISK_LEVELS = ["low", "medium", "high"]
SAR_STATUSES = ["pending", "filed", "dismissed"]

# Generate customers data
def generate_customers():
    customers = []
    for customer_id in range(1, NUM_CUSTOMERS + 1):
        name = fake.name()
        account = str(random.randint(100000000, 9999999999))
        dob = fake.date_of_birth(minimum_age=18, maximum_age=80).strftime("%Y-%m-%d")
        nationality = fake.country()
        risk_level = random.choice(RISK_LEVELS)
        pep_status = random.choice([True, False])
        blacklisted = random.choice([True, False]) if risk_level == "high" else False
        customers.append([customer_id, name, account, dob, nationality, risk_level, pep_status, blacklisted])
    return customers

# Generate SARs data
def generate_sars(customers):
    import random

    aml_reasons = [
        "rapid large deposits",
        "multiple small cash deposits",
        "frequent wire transfers",
        "high volume of transactions",
        "unexplained wealth increase",
        "rapid movement of funds",
        "transactions just below reporting threshold",
        "frequent ATM withdrawals",
        "multiple high-value purchases",
        "inconsistent deposit amounts",
        "repeated failed transactions",
        "high-risk merchant activity",
        "large round-dollar transactions",
        "unusual payment frequency",
        "excessive refund requests",
        "transactions with sanctioned countries",
        "cross-border high-risk jurisdiction",
        "frequent offshore transactions",
        "use of multiple foreign accounts",
        "payments to unknown international entities",
        "transfers to high-risk tax havens",
        "funds originating from conflict zones",
        "frequent cross-border remittances",
        "sudden shift in transaction locations",
        "transactions from high-risk jurisdictions",
        "shell company detected",
        "business lacks operational activity",
        "high volume of cash transactions",
        "transactions do not match business profile",
        "unregistered business receiving payments",
        "high-risk industry involvement",
        "front company suspected",
        "misuse of business accounts",
        "fake invoices detected",
        "unusual supplier payments",
        "business operating with no clear income source",
        "charity receiving unexplained large donations",
        "structuring detected",
        "layering through multiple accounts",
        "use of third-party intermediaries",
        "funds rapidly transferred across multiple accounts",
        "complex transaction chain with no clear purpose",
        "transaction smurfing detected",
        "rapid movement between personal and business accounts",
        "multiple deposits from unknown sources",
        "withdrawal pattern inconsistent with income",
        "mismatched identity details",
        "account holder uses multiple aliases",
        "multiple accounts linked to single individual",
        "synthetic identity detected",
        "high-risk account takeover attempt",
        "fraudulent ID used for onboarding",
        "accounts opened with false information",
        "loan applications using stolen credentials",
        "identity inconsistencies across accounts",
        "duplicate account credentials detected",
        "large cash deposit without declared source",
        "frequent deposits at multiple locations",
        "cash transactions inconsistent with known income",
        "sudden increase in cash deposits",
        "high cash activity without justification",
        "cash deposits followed by immediate withdrawals",
        "large-volume cash business with no payroll activity",
        "real estate purchase with no clear source of funds",
        "luxury purchases inconsistent with income",
        "high-value asset flipping detected",
        "multiple property transactions in short period",
        "unregistered ownership changes",
        "cash purchase of high-value assets",        
        "credit card laundering suspected",
        "excessive prepaid card loading",
        "use of multiple credit cards in short time",
        "digital wallet with frequent high-value deposits",
        "unexplained gift card transactions",
        "cryptocurrency exchange activity without declared source of funds",        
        "funds linked to darknet marketplaces",
        "use of privacy coins",
        "anonymized transactions detected",
        "multiple IP addresses accessing account",
        "high volume of online gambling transactions",
        "sudden increase in e-commerce refunds",
        "use of VPN or TOR network in transactions",
        "payments to social media-based traders",        
        "funds received from unrelated third parties",
        "transactions between linked individuals flagged",
        "repeated transactions with same unknown entity",
        "funds moved through multiple third-party accounts",
        "proxy account suspected",
        "multiple account holders accessing single device",
        "third-party involvement without clear business reason",        
        "abnormal behavior detected in transaction monitoring",
        "PEP transaction flagged",
        "unusual financial product usage",
        "misuse of government stimulus funds",
        "emergency loans fraud detected",
        "fake employment claims linked to account",
        "transaction pattern linked to known fraud cases",
        "large transactions immediately reversed"
    ]
    sars = []
    for sar_id in range(1, NUM_SARS + 1):
        customer = random.choice(customers)
        customer_id = customer[0]
        transaction_id = random.randint(1000000000, 9999999999)
        reason = random.choice(aml_reasons)
        status = random.choice(SAR_STATUSES)
        filed_date = fake.date_time_this_year().strftime("%Y-%m-%d %H:%M:%S")
        sars.append([sar_id, customer_id, transaction_id, reason, status, filed_date])
    return sars

# Save to CSV
def save_to_csv(filename, data, headers):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(data)
    print(f"✅ Generated {filename}")

# Generate data
customers_data = generate_customers()
sars_data = generate_sars(customers_data)

# Save data to CSV files
save_to_csv("customers.csv", customers_data, ["customer_id", "name", "account", "dob", "nationality", "risk_level", "pep_status", "blacklisted"])
save_to_csv("sars.csv", sars_data, ["sar_id", "customer_id", "transaction_id", "reason", "status", "filed_date"])
