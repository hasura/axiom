import random
import pandas as pd
from datetime import datetime, timedelta
import json
import uuid
from faker import Faker

# Initialize Faker with seed for reproducibility
fake = Faker()
Faker.seed(42)
random.seed(42)

# Constants
CURRENT_DATE = datetime.today()
COUNTRIES = ["USA", "Canada", "UK", "Germany", "South Africa", "Cuba", "Iran", "Russia"]
HIGH_RISK_COUNTRIES = ["Cuba", "Iran", "Russia"]
CURRENCIES = ["USD", "CAD", "EUR", "ZAR", "BTC"]
PAYMENT_TYPES = ["wire", "check", "cash", "crypto"]
RISK_LEVELS = ["low", "medium", "high"]

# Advanced pattern generation for AI detection
def create_structuring_ring(customers, num_rings=3):
    """Create sophisticated structuring rings - multiple accounts making coordinated small transactions"""
    structuring_rings = []
    available_customers = [c for c in customers if c["risk_level"] in ["low", "medium"]]  # Use low-risk to hide pattern
    
    for ring_id in range(num_rings):
        ring_size = random.randint(4, 8)  # 4-8 accounts per ring
        ring_accounts = random.sample(available_customers, ring_size)
        
        # Create ring with shared characteristics that AI can detect
        shared_traits = {
            "target_amount": random.uniform(8000, 15000),  # Total amount to structure
            "time_window": random.randint(7, 21),  # Days to spread transactions
            "common_receiver": random.choice(customers)["account"],  # Common destination
            "transaction_pattern": random.choice(["daily", "every_other_day", "weekly"])
        }
        
        structuring_rings.append({
            "ring_id": ring_id,
            "accounts": [acc["account"] for acc in ring_accounts],
            "traits": shared_traits
        })
        
        # Remove used customers
        for acc in ring_accounts:
            available_customers.remove(acc)
    
    return structuring_rings

def create_layering_patterns(customers, num_patterns=5):
    """Create layering patterns - rapid movement of funds through multiple accounts"""
    layering_chains = []
    
    for pattern_id in range(num_patterns):
        chain_length = random.randint(5, 12)  # 5-12 hops
        chain_accounts = random.sample(customers, chain_length)
        
        layering_chains.append({
            "pattern_id": pattern_id,
            "chain": [acc["account"] for acc in chain_accounts],
            "base_amount": random.uniform(50000, 200000),
            "time_compression": random.randint(1, 3),  # Days to complete chain
            "amount_decay": random.uniform(0.02, 0.08)  # Small fees/losses per hop
        })
    
    return layering_chains

def create_integration_networks(customers, num_networks=4):
    """Create integration networks - legitimate-looking business transactions that integrate dirty money"""
    integration_networks = []
    
    for net_id in range(num_networks):
        # Select business accounts (companies)
        business_accounts = [c for c in customers if "Inc" in c["name"] or "Ltd" in c["name"] or "Corp" in c["name"]]
        if len(business_accounts) < 8:
            continue
            
        network_size = random.randint(6, 15)
        network_accounts = random.sample(business_accounts, min(network_size, len(business_accounts)))
        
        integration_networks.append({
            "network_id": net_id,
            "accounts": [acc["account"] for acc in network_accounts],
            "business_type": random.choice(["consulting", "trading", "services", "import_export"]),
            "monthly_volume": random.uniform(500000, 2000000),
            "suspicious_percentage": random.uniform(0.15, 0.35)  # 15-35% of volume is suspicious
        })
    
    return integration_networks

# Seasonal and business patterns
def get_seasonal_multiplier(date):
    """Returns multiplier based on seasonal patterns (higher activity in Q4, lower in summer)"""
    month = date.month
    if month in [11, 12]:  # Holiday season
        return 1.4
    elif month in [1, 2]:  # Post-holiday
        return 0.8
    elif month in [6, 7, 8]:  # Summer slowdown
        return 0.9
    else:
        return 1.0

def get_business_day_multiplier(date):
    """Returns multiplier based on business day patterns"""
    weekday = date.weekday()
    if weekday < 5:  # Monday-Friday
        return 1.2
    else:  # Weekend
        return 0.6

def get_time_of_day_weight(hour):
    """Returns weight for transaction likelihood based on hour"""
    if 9 <= hour <= 17:  # Business hours
        return 3.0
    elif 18 <= hour <= 22:  # Evening
        return 1.5
    else:  # Night/early morning
        return 0.3

# Generate customers/accounts with Faker - ensuring consistency between databases
def generate_customers(num_customers=50):
    customers = []
    accounts = []
    sanctioned_entities = []  # Track entities that will be sanctioned
    
    for i in range(num_customers):
        account_id = 10000 + i
        is_company = random.random() < 0.2  # 20% companies
        name = fake.company() if is_company else fake.name()
        
        # More realistic age distribution
        if is_company:
            dob = CURRENT_DATE - timedelta(days=random.randint(5*365, 50*365))  # Companies 5-50 years old
        else:
            dob = CURRENT_DATE - timedelta(days=random.randint(18*365, 80*365))  # Individuals 18-80 years old
        
        # Nationality influences risk and other factors
        nationality = random.choices(COUNTRIES, weights=[30, 20, 20, 20, 5, 2, 2, 1], k=1)[0]
        
        # Risk level influenced by nationality and entity type
        base_risk_weights = [70, 20, 10]  # low, medium, high
        if nationality in HIGH_RISK_COUNTRIES:
            base_risk_weights = [30, 40, 30]  # Higher risk for sanctioned countries
        if is_company:
            base_risk_weights = [base_risk_weights[0] * 0.8, base_risk_weights[1] * 1.2, base_risk_weights[2] * 1.5]
        
        risk = random.choices(RISK_LEVELS, weights=base_risk_weights, k=1)[0]
        
        # PEP status more likely for high-risk individuals from certain countries
        pep_chance = 0.02  # Base 2%
        if nationality in HIGH_RISK_COUNTRIES and not is_company:
            pep_chance = 0.15  # 15% for individuals from high-risk countries
        pep = random.random() < pep_chance
        
        # Blacklisted status based on multiple factors
        blacklist_chance = 0.01  # Base 1%
        if nationality in HIGH_RISK_COUNTRIES:
            blacklist_chance = 0.08
        if pep:
            blacklist_chance *= 2
        if risk == "high":
            blacklist_chance *= 1.5
        blacklisted = random.random() < blacklist_chance
        
        # Generate consistent address
        if nationality == "USA":
            fake.locale = 'en_US'
        elif nationality == "Canada":
            fake.locale = 'en_CA'
        elif nationality == "UK":
            fake.locale = 'en_GB'
        elif nationality == "Germany":
            fake.locale = 'de_DE'
        else:
            fake.locale = 'en_US'  # Default
            
        address = fake.address().replace("\n", ", ")
        
        # Store potential sanctioned entities (some customers will appear in sanctions)
        if blacklisted or (nationality in HIGH_RISK_COUNTRIES and random.random() < 0.3):
            sanctioned_entities.append({
                "name": name,
                "address": address,
                "entity_type": "company" if is_company else "individual",
                "nationality": nationality
            })
        
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
        
        # MongoDB accounts - exactly same data but different structure
        accounts.append({
            "account_id": account_id,
            "name": name,
            "entity_type": "company" if is_company else "individual",
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
    
    return customers, accounts, sanctioned_entities

# Generate transactions with realistic patterns and seasonality
def generate_transactions(customers, num_transactions=200):
    pg_transactions = []
    mongo_transactions = []
    suspicious_accounts = [c["account"] for c in customers if c["risk_level"] == "high" or c["blacklisted"] or c["pep_status"]]
    
    # Create customer lookup for faster access
    customer_lookup = {c["account"]: c for c in customers}
    
    # Generate sophisticated criminal patterns (hidden in normal transactions)
    structuring_rings = create_structuring_ring(customers, 3)
    layering_patterns = create_layering_patterns(customers, 5)
    integration_networks = create_integration_networks(customers, 4)
    
    print(f"   Created {len(structuring_rings)} structuring rings, {len(layering_patterns)} layering patterns, {len(integration_networks)} integration networks")
    
    # Generate transactions with realistic temporal distribution
    transaction_dates = []
    for i in range(num_transactions):
        # Generate dates with seasonal and business day patterns
        days_back = random.randint(1, 365)  # Full year of data
        base_date = CURRENT_DATE - timedelta(days=days_back)
        
        # Apply seasonal multiplier to determine if transaction should occur
        seasonal_mult = get_seasonal_multiplier(base_date)
        business_mult = get_business_day_multiplier(base_date)
        
        # Higher chance of transaction on favorable days
        if random.random() < (seasonal_mult * business_mult * 0.3):
            transaction_dates.append(base_date)
    
    # If we don't have enough dates, fill with random dates
    while len(transaction_dates) < num_transactions:
        days_back = random.randint(1, 365)
        transaction_dates.append(CURRENT_DATE - timedelta(days=days_back))
    
    # Sort dates for realistic chronological order
    transaction_dates.sort()
    
    for i in range(num_transactions):
        date = transaction_dates[i]
        
        # Realistic time distribution based on business patterns
        hour_weights = [get_time_of_day_weight(h) for h in range(24)]
        hour = random.choices(range(24), weights=hour_weights, k=1)[0]
        minute = random.randint(0, 59)
        time = f"{hour:02d}:{minute:02d}"
        
        # Select sender and receiver with some business logic
        sender = random.choice(customers)
        
        # Receivers more likely to be from same country for normal transactions
        same_country_customers = [c for c in customers if c["nationality"] == sender["nationality"] and c["account"] != sender["account"]]
        different_country_customers = [c for c in customers if c["nationality"] != sender["nationality"]]
        
        # 70% same country, 30% cross-border for normal transactions
        if same_country_customers and random.random() < 0.7:
            receiver = random.choice(same_country_customers)
        else:
            receiver = random.choice(different_country_customers) if different_country_customers else random.choice([c for c in customers if c["account"] != sender["account"]])
        
        # Amount influenced by sender's risk level and seasonal patterns
        base_amount = random.uniform(100, 5000)
        seasonal_mult = get_seasonal_multiplier(date)
        
        if sender["risk_level"] == "high":
            base_amount *= random.uniform(0.5, 2.5)  # More volatile amounts
        elif sender["risk_level"] == "low":
            base_amount *= random.uniform(0.8, 1.2)  # More stable amounts
        
        amount = base_amount * seasonal_mult
        
        # Currency selection based on countries involved
        if sender["nationality"] == "USA" or receiver["nationality"] == "USA":
            payment_currency = random.choices(CURRENCIES, weights=[60, 20, 15, 4, 1], k=1)[0]
        elif sender["nationality"] in ["UK", "Germany"] or receiver["nationality"] in ["UK", "Germany"]:
            payment_currency = random.choices(CURRENCIES, weights=[30, 20, 45, 4, 1], k=1)[0]
        else:
            payment_currency = random.choices(CURRENCIES, weights=[40, 30, 25, 4, 1], k=1)[0]
        
        received_currency = payment_currency
        
        # Payment type influenced by amount and countries
        if amount > 10000:
            payment_type = random.choices(PAYMENT_TYPES, weights=[70, 20, 5, 5], k=1)[0]  # Prefer wire for large amounts
        elif sender["nationality"] in HIGH_RISK_COUNTRIES or receiver["nationality"] in HIGH_RISK_COUNTRIES:
            payment_type = random.choices(PAYMENT_TYPES, weights=[40, 20, 20, 20], k=1)[0]  # More diverse for high-risk
        else:
            payment_type = random.choices(PAYMENT_TYPES, weights=[50, 30, 15, 5], k=1)[0]
        
        sender_location = sender["nationality"]
        receiver_location = receiver["nationality"]
        
        # Sophisticated pattern detection - requires AI to uncover
        is_laundering = False
        laundering_type = "none"
        aml_flags = {"structuring": False, "cross_border": False, "darknet": False}
        pattern_metadata = {}
        
        # Check if this transaction is part of a sophisticated criminal pattern
        
        # 1. STRUCTURING RINGS - Coordinated small transactions across multiple accounts
        for ring in structuring_rings:
            if sender["account"] in ring["accounts"]:
                if random.random() < 0.3:  # 30% of ring transactions are suspicious
                    target_per_account = ring["traits"]["target_amount"] / len(ring["accounts"])
                    individual_amount = target_per_account / random.randint(3, 8)  # Split into multiple transactions
                    amount = individual_amount * random.uniform(0.8, 1.2)  # Add variance
                    
                    # Make it look legitimate but follow pattern
                    if amount < 3000:  # Below CTR threshold
                        payment_type = "cash"
                        is_laundering = True
                        laundering_type = "structuring"
                        aml_flags["structuring"] = True
                        pattern_metadata = {
                            "ring_id": ring["ring_id"],
                            "pattern_type": "coordinated_structuring",
                            "target_receiver": ring["traits"]["common_receiver"]
                        }
                        # Set receiver to common destination
                        receiver = customer_lookup.get(ring["traits"]["common_receiver"], receiver)
                break
        
        # 2. LAYERING PATTERNS - Rapid movement through multiple accounts
        for pattern in layering_patterns:
            if sender["account"] in pattern["chain"]:
                sender_index = pattern["chain"].index(sender["account"])
                if sender_index < len(pattern["chain"]) - 1:  # Not the last in chain
                    next_account = pattern["chain"][sender_index + 1]
                    if random.random() < 0.4:  # 40% chance this hop is active
                        # Set receiver to next in chain
                        receiver = customer_lookup.get(next_account, receiver)
                        
                        # Amount decreases slightly with each hop (fees/losses)
                        hop_multiplier = (1 - pattern["amount_decay"]) ** sender_index
                        amount = (pattern["base_amount"] * hop_multiplier) * random.uniform(0.95, 1.05)
                        
                        # Use wire transfers for speed
                        payment_type = "wire"
                        
                        # Time compression - transactions happen quickly
                        if sender_index > 0:
                            # Subsequent hops happen within hours/days of previous
                            time_offset = random.randint(1, pattern["time_compression"] * 24)
                            # Adjust time to be close to previous transaction
                        
                        is_laundering = True
                        laundering_type = "layering"
                        pattern_metadata = {
                            "pattern_id": pattern["pattern_id"],
                            "hop_number": sender_index + 1,
                            "chain_length": len(pattern["chain"]),
                            "pattern_type": "rapid_layering"
                        }
                break
        
        # 3. INTEGRATION NETWORKS - Legitimate-looking business transactions
        for network in integration_networks:
            if sender["account"] in network["accounts"]:
                if random.random() < network["suspicious_percentage"]:
                    # Pick another account in the network
                    network_receivers = [acc for acc in network["accounts"] if acc != sender["account"]]
                    if network_receivers:
                        receiver = customer_lookup.get(random.choice(network_receivers), receiver)
                        
                        # Business-like amounts
                        business_amounts = {
                            "consulting": lambda: random.uniform(5000, 50000),
                            "trading": lambda: random.uniform(10000, 200000),
                            "services": lambda: random.uniform(2000, 25000),
                            "import_export": lambda: random.uniform(25000, 500000)
                        }
                        
                        amount = business_amounts[network["business_type"]]()
                        payment_type = "wire"  # Business transactions
                        
                        is_laundering = True
                        laundering_type = "integration"
                        pattern_metadata = {
                            "network_id": network["network_id"],
                            "business_type": network["business_type"],
                            "pattern_type": "business_integration",
                            "monthly_volume": network["monthly_volume"]
                        }
                break
        
        # 4. SMURFING - Multiple small transactions just under thresholds (hard to detect pattern)
        if not is_laundering and random.random() < 0.02:  # 2% chance - very rare
            if amount > 2000:  # Only for larger amounts
                # Split into amount just under common thresholds
                thresholds = [3000, 5000, 10000]  # Common reporting thresholds
                applicable_threshold = min([t for t in thresholds if t > amount], default=10000)
                smurf_amount = applicable_threshold * random.uniform(0.85, 0.95)  # Just under threshold
                
                if smurf_amount < amount:
                    amount = smurf_amount
                    payment_type = random.choice(["cash", "check"])
                    is_laundering = True
                    laundering_type = "smurfing"
                    aml_flags["structuring"] = True
                    pattern_metadata = {
                        "pattern_type": "threshold_avoidance",
                        "threshold_avoided": applicable_threshold,
                        "avoidance_percentage": (applicable_threshold - amount) / applicable_threshold
                    }
        
        # 5. ROUND DOLLAR BIAS - Suspicious round amounts (AI can detect this pattern)
        if not is_laundering and random.random() < 0.03:  # 3% chance
            round_amounts = [1000, 2500, 5000, 7500, 10000, 15000, 20000, 25000]
            if any(abs(amount - ra) < 100 for ra in round_amounts):  # If close to round amount
                amount = random.choice(round_amounts)
                is_laundering = random.random() < 0.4
                if is_laundering:
                    laundering_type = "round_dollar_structuring"
                    pattern_metadata = {
                        "pattern_type": "round_dollar_bias",
                        "exact_amount": amount
                    }
        
        transaction_id = 1000 + i
        
        # Ensure exact same transaction data in both databases
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
        
        # MongoDB version with same core data but different structure
        # Add pattern metadata for AI analysis (hidden in aml_flags)
        enhanced_aml_flags = aml_flags.copy()
        if pattern_metadata:
            enhanced_aml_flags["pattern_metadata"] = pattern_metadata
        
        mongo_transactions.append({
            "transaction_id": transaction_id,
            "transaction_date": f"{date.strftime('%Y-%m-%d')}T{time}:00.000Z",
            "originator_id": sender["account"],
            "originator_name": sender["name"],
            "originator_address": sender["address"],
            "beneficiary_id": receiver["account"],
            "beneficiary_name": receiver["name"],
            "beneficiary_address": receiver["address"],
            "amount": round(amount, 2),
            "aml_flags": enhanced_aml_flags
        })
    return pg_transactions, mongo_transactions

# Generate SARs (Suspicious Activity Reports) - properly linked to transactions and customers
def generate_sars(customers, transactions):
    sars = []
    laundering_transactions = [t for t in transactions if t["is_laundering"]]
    
    # Generate SARs for all suspicious transactions, not just first 10
    for i, tx in enumerate(laundering_transactions):
        customer = next(c for c in customers if c["account"] == tx["sender_account"])
        
        # More detailed and realistic reasons based on transaction patterns
        reason_templates = {
            "structuring": f"Structured cash transaction of ${tx['amount']:,.2f} below reporting threshold. Pattern suggests potential structuring to avoid CTR filing requirements.",
            "cross_border": f"High-risk cross-border transfer of ${tx['amount']:,.2f} to {tx['receiver_bank_location']}. Enhanced due diligence required for sanctions screening.",
            "darknet": f"Cryptocurrency transaction of ${tx['amount']:,.2f} with indicators of potential darknet marketplace activity. Digital asset monitoring flagged suspicious patterns."
        }
        
        reason = reason_templates.get(tx["laundering_type"], f"Suspicious transaction activity detected for ${tx['amount']:,.2f}. Manual review required.")
        
        # Status based on transaction date and severity
        tx_date = datetime.strptime(tx["date"], "%Y-%m-%d")
        days_since_tx = (CURRENT_DATE - tx_date).days
        
        # More recent transactions more likely to be pending
        if days_since_tx < 30:
            status = random.choices(["pending", "filed"], weights=[70, 30], k=1)[0]
        else:
            status = random.choices(["pending", "filed"], weights=[20, 80], k=1)[0]
        
        # Filed date should be after transaction date
        if status == "filed":
            filed_days_after = random.randint(1, min(30, days_since_tx + 1))
            filed_date = (tx_date + timedelta(days=filed_days_after)).strftime("%Y-%m-%d %H:%M:%S")
        else:
            filed_date = CURRENT_DATE.strftime("%Y-%m-%d %H:%M:%S")
        
        sars.append({
            "sar_id": i + 1,
            "customer_id": customer["customer_id"],
            "transaction_id": tx["transaction_id"],
            "reason": reason,
            "status": status,
            "filed_date": filed_date
        })
    return sars

# Generate sanctions list - mix of real customers and external entities
def generate_sanctions(sanctioned_entities, num_additional=50):
    sanctions = []
    
    # First, add some of our actual customers to sanctions (creates real relationships)
    for i, entity in enumerate(sanctioned_entities[:min(20, len(sanctioned_entities))]):
        # Use actual customer data for realistic sanctions entries
        sanctions.append({
            "_id": str(uuid.uuid4()),
            "entity_name": entity["name"],
            "entity_type": entity["entity_type"],
            "address": entity["address"],
            "listed_date": (CURRENT_DATE - timedelta(days=random.randint(30, 2*365))).strftime("%Y-%m-%dT00:00:00.000Z"),
            "program": random.choices(["OFAC-SDN", "UN-Sanctions", "EU-Restrictive"], weights=[50, 30, 20], k=1)[0],
            "list_type": random.choices(["OFAC", "UN", "EU"], weights=[50, 30, 20], k=1)[0]
        })
    
    # Then add additional fictional sanctioned entities
    for i in range(num_additional):
        is_company = random.random() < 0.4  # 40% companies in sanctions
        name = fake.company() if is_company else fake.name()
        
        # Sanctions more likely from high-risk countries
        country = random.choices(HIGH_RISK_COUNTRIES + ["North Korea", "Syria", "Venezuela"],
                                weights=[25, 25, 25, 10, 10, 5], k=1)[0]
        
        # Generate address in sanctioned country
        if country in ["Cuba", "Iran"]:
            fake.locale = 'en_US'  # Use generic for these
        else:
            fake.locale = 'en_US'
            
        address = fake.address().replace("\n", ", ") + f", {country}"
        
        # Listing date - sanctions can be quite old
        listing_age_days = random.randint(365, 10*365)  # 1-10 years old
        listed_date = (CURRENT_DATE - timedelta(days=listing_age_days)).strftime("%Y-%m-%dT00:00:00.000Z")
        
        # Program selection based on country and entity type
        if country in ["Iran", "Cuba"]:
            program = "OFAC-SDN"
            list_type = "OFAC"
        elif country == "Russia":
            program = random.choice(["OFAC-SDN", "EU-Restrictive"])
            list_type = "OFAC" if program == "OFAC-SDN" else "EU"
        else:
            program = random.choice(["OFAC-SDN", "UN-Sanctions", "EU-Restrictive"])
            list_type = {"OFAC-SDN": "OFAC", "UN-Sanctions": "UN", "EU-Restrictive": "EU"}[program]
        
        sanctions.append({
            "_id": str(uuid.uuid4()),
            "entity_name": name,
            "entity_type": "company" if is_company else "individual",
            "address": address,
            "listed_date": listed_date,
            "program": program,
            "list_type": list_type
        })
    
    return sanctions

# Main execution
print("Starting AML data generation...")
print("Generating 5,000 customers and accounts...")
customers, accounts, sanctioned_entities = generate_customers(5000)
print(f"Generated {len(customers)} customers, {len(accounts)} accounts, {len(sanctioned_entities)} potential sanctioned entities")

print("Generating 50,000 transactions with seasonal patterns...")
pg_transactions, mongo_transactions = generate_transactions(customers, 50000)
print(f"Generated {len(pg_transactions)} transactions ({sum(1 for t in pg_transactions if t['is_laundering'])} suspicious)")

print("Generating SARs for all suspicious transactions...")
sars = generate_sars(customers, pg_transactions)
print(f"Generated {len(sars)} SARs ({sum(1 for s in sars if s['status'] == 'filed')} filed, {sum(1 for s in sars if s['status'] == 'pending')} pending)")

print("Generating sanctions list with customer relationships...")
sanctions = generate_sanctions(sanctioned_entities, 400)
print(f"Generated {len(sanctions)} sanctions entries")

print("Saving PostgreSQL data as CSV files...")
pd.DataFrame(customers).to_csv("postgres/customers.csv", index=False)
print("   customers.csv saved")
pd.DataFrame(pg_transactions).to_csv("postgres/financial_transfers.csv", index=False)
print("   financial_transfers.csv saved")
pd.DataFrame(sars).to_csv("postgres/sars.csv", index=False)
print("   sars.csv saved")

print("Saving MongoDB data as JSON files...")
with open("mongo_seed/accounts.json", "w") as f:
    json.dump(accounts, f, indent=2)
print("   accounts.json saved")
with open("mongo_seed/aml_cases.json", "w") as f:
    json.dump(mongo_transactions, f, indent=2)
print("   aml_cases.json saved")
with open("mongo_seed/sanctions.json", "w") as f:
    json.dump(sanctions, f, indent=2)
print("   sanctions.json saved")

print("\nData generation complete!")
print(f"Summary:")
print(f"   - {len(customers):,} customers/accounts")
print(f"   - {len(pg_transactions):,} transactions")
print(f"   - {sum(1 for t in pg_transactions if t['is_laundering']):,} suspicious transactions")
print(f"   - {len(sars):,} SARs generated")
print(f"   - {len(sanctions):,} sanctions entries")
print(f"   - Files saved to postgres/ and mongo_seed/ directories")
