#!/usr/bin/env python3
"""
FinIQ - Financial Intelligence & Quality Platform
Data Generator for Transaction Reconciliation Demo
Generates realistic authorization and settlement transaction data
with proper business logic and referential integrity
Version: 2.0 (with Merchants & Enhanced Analytics)
"""

import csv
import random
import string
from datetime import datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

# Configuration - Optimized for realistic demo proportions
NUM_ISSUERS = 25              # Major card-issuing banks
NUM_ACQUIRERS = 75            # Merchant acquiring institutions
NUM_MERCHANTS = 1000          # Business entities accepting cards
NUM_AUTH_TRANSACTIONS = 100000  # Authorization requests
MISSING_CODE_PERCENTAGE = 2.0  # Industry standard 1-3%

# Industry-aligned decline rates by risk level
DECLINE_RATE_LOW_RISK = 12.5    # 10-15% for low-risk merchants
DECLINE_RATE_MEDIUM_RISK = 20.0 # 15-25% for medium-risk merchants
DECLINE_RATE_HIGH_RISK = 30.0   # 25-35% for high-risk merchants

# Settlement variance distribution (industry-aligned)
EXACT_MATCH_PERCENTAGE = 55.0   # Reduced from 80% to 55%
LOW_VARIANCE_PERCENTAGE = 27.0  # 0-1% variance (25-30% target)
MEDIUM_VARIANCE_PERCENTAGE = 12.0 # 1-2% variance (8-10% target)
HIGH_VARIANCE_PERCENTAGE = 4.0   # 2-5% variance (3-5% target)
EXTREME_VARIANCE_PERCENTAGE = 2.0 # >5% variance (1-2% target)

# Unsettled transaction percentage (industry standard)
UNSETTLED_PERCENTAGE = 1.5      # 0.5-2% of approved transactions remain unsettled

# Resulting ratios:
# - 4,000 transactions per issuer (more realistic for demo scale)
# - 1,333 transactions per acquirer (better volume)
# - 100 transactions per merchant (realistic for small-medium merchants)
# - 13.3 merchants per acquirer (good relationship density)

# Date range for transactions
START_DATE = datetime(2024, 1, 1)
END_DATE = datetime(2025, 10, 15)

# Output directory
OUTPUT_DIR = Path("./postgres/demo_data")
OUTPUT_DIR.mkdir(exist_ok=True)

# Merchant Category Codes (ISO 18245 MCC)
MERCHANT_CATEGORIES = {
    '5411': 'GROCERY_STORES',
    '5812': 'RESTAURANTS',
    '5541': 'GAS_STATIONS',
    '5311': 'DEPARTMENT_STORES',
    '5999': 'MISC_RETAIL',
    '5912': 'DRUG_STORES',
    '5942': 'BOOKSTORES',
    '7011': 'HOTELS_MOTELS',
    '4111': 'LOCAL_TRANSIT',
    '4511': 'AIRLINES',
    '5732': 'ELECTRONICS',
    '5661': 'SHOE_STORES',
    '5813': 'BARS_TAVERNS',
    '5814': 'FAST_FOOD',
    '7230': 'BEAUTY_SALONS',
    '7832': 'MOVIE_THEATERS',
    '7941': 'SPORTS_RECREATION',
    '5045': 'COMPUTERS',
    '5193': 'FLORISTS',
    '8011': 'DOCTORS',
}


def generate_id(prefix, length=8):
    """Generate random alphanumeric ID"""
    return f"{prefix}{random.randint(10**(length-1), 10**length - 1)}"


def generate_alpha_numeric_id(length=12):
    """Generate alphanumeric transaction ID"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


def random_date(start, end):
    """Generate random date between start and end"""
    delta = end - start
    random_days = random.randint(0, delta.days)
    return start + timedelta(days=random_days)


def random_datetime(date):
    """Generate random timestamp for a given date"""
    hour = random.randint(6, 23)  # Business hours weighted
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    return datetime.combine(date, datetime.min.time().replace(hour=hour, minute=minute, second=second))


def random_amount(min_amt=5.0, max_amt=5000.0):
    """Generate random transaction amount"""
    amount = random.uniform(min_amt, max_amt)
    return Decimal(str(amount)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


def get_category_amount_range(category_name):
    """Get realistic amount ranges by merchant category"""
    category_ranges = {
        # Food & Dining
        'RESTAURANTS': (30.0, 80.0),
        'BARS_TAVERNS': (25.0, 75.0),
        'FAST_FOOD': (8.0, 25.0),
        
        # Retail
        'DEPARTMENT_STORES': (120.0, 400.0),
        'SHOE_STORES': (80.0, 300.0),
        'MISC_RETAIL': (20.0, 150.0),
        
        # Services
        'BEAUTY_SALONS': (50.0, 200.0),
        'SPORTS_RECREATION': (75.0, 250.0),
        'DOCTORS': (100.0, 500.0),
        
        # Travel & Transportation
        'AIRLINES': (250.0, 600.0),
        'HOTELS_MOTELS': (80.0, 350.0),
        'LOCAL_TRANSIT': (2.0, 15.0),
        
        # Electronics & Technology
        'COMPUTERS': (500.0, 1500.0),
        'ELECTRONICS': (75.0, 800.0),
        
        # Everyday Purchases
        'GROCERY_STORES': (15.0, 150.0),
        'DRUG_STORES': (8.0, 75.0),
        'GAS_STATIONS': (20.0, 100.0),
        
        # Other
        'BOOKSTORES': (10.0, 80.0),
        'MOVIE_THEATERS': (15.0, 45.0),
        'FLORISTS': (25.0, 150.0),
    }
    return category_ranges.get(category_name, (20.0, 200.0))  # Default range


def get_category_decline_rate(category_name):
    """Get realistic decline rates by merchant category (as percentages)"""
    category_decline_rates = {
        # Low decline rate categories (3-5%) - Adjusted upward for industry compliance
        'AIRLINES': 4.0,
        'COMPUTERS': 3.5,
        'ELECTRONICS': 4.2,
        'HOTELS_MOTELS': 4.8,
        
        # Medium-low decline rates (5-7%)
        'DEPARTMENT_STORES': 6.0,
        'SHOE_STORES': 6.5,
        'GROCERY_STORES': 5.2,
        'DRUG_STORES': 5.5,
        
        # Medium decline rates (7-10%)
        'RESTAURANTS': 8.5,
        'BARS_TAVERNS': 9.2,
        'BEAUTY_SALONS': 8.0,
        'SPORTS_RECREATION': 7.5,
        'FAST_FOOD': 7.0,
        'GAS_STATIONS': 7.8,
        
        # Higher decline rates (9-12%)
        'MISC_RETAIL': 10.5,
        'MOVIE_THEATERS': 8.5,
        'BOOKSTORES': 7.5,
        'FLORISTS': 9.0,
        'DOCTORS': 8.2,
        'LOCAL_TRANSIT': 11.0,
    }
    return category_decline_rates.get(category_name, 8.0)  # Default 8.0%


def calculate_settlement_amount(auth_amount, variance_type='exact', merchant_category='MISC_RETAIL'):
    """
    Calculate settlement amount based on variance type and merchant category
    Industry-aligned variance patterns:
    - exact: no change
    - low_variance: 0-1% variance
    - medium_variance: 1-2% variance
    - high_variance: 2-5% variance
    - extreme_variance: >5% variance (hospitality, fuel, rental sectors)
    """
    if variance_type == 'exact':
        return auth_amount
    
    # Higher variance for hospitality, fuel, and rental sectors
    high_variance_categories = ['HOTELS_MOTELS', 'GAS_STATIONS', 'AIRLINES', 'RESTAURANTS']
    
    if variance_type == 'low_variance':
        variance_pct = random.uniform(0.001, 0.01)
    elif variance_type == 'medium_variance':
        variance_pct = random.uniform(0.01, 0.02)
    elif variance_type == 'high_variance':
        if merchant_category in high_variance_categories:
            variance_pct = random.uniform(0.02, 0.08)  # Higher for hospitality/fuel
        else:
            variance_pct = random.uniform(0.02, 0.05)
    else:  # extreme_variance
        if merchant_category in high_variance_categories:
            variance_pct = random.uniform(0.05, 0.15)  # Up to 15% for hospitality
        else:
            variance_pct = random.uniform(0.05, 0.10)
    
    variance = auth_amount * Decimal(str(variance_pct))
    # Randomly add or subtract
    settlement = auth_amount + (variance if random.random() > 0.5 else -variance)
    return settlement.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


def calculate_fees(amount):
    """Calculate interchange and network fees"""
    interchange_rate = random.uniform(0.015, 0.025)  # 1.5-2.5%
    network_rate = random.uniform(0.001, 0.005)      # 0.1-0.5%
    
    interchange = (amount * Decimal(str(interchange_rate))).quantize(
        Decimal('0.01'), rounding=ROUND_HALF_UP)
    network = (amount * Decimal(str(network_rate))).quantize(
        Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    return interchange, network


class DataGenerator:
    def __init__(self):
        self.issuers = []
        self.acquirers = []
        self.merchants = []
        self.auth_transactions = []
        self.settlement_transactions = []
        
        self.transaction_types = [
            'PURCHASE', 'PURCHASE', 'PURCHASE', 'PURCHASE',  # Weight toward purchases
            'REFUND', 'CASH_ADVANCE', 'BALANCE_INQUIRY'
        ]
        
        self.currencies = ['USD', 'USD', 'USD', 'EUR', 'GBP']  # Weight toward USD
        # Industry-realistic risk level distribution
        self.risk_levels = ['LOW', 'LOW', 'LOW', 'LOW', 'LOW', 'MEDIUM', 'MEDIUM', 'HIGH']
        
        # Merchant name templates
        self.merchant_name_templates = {
            'GROCERY_STORES': ['Fresh Market', 'Value Foods', 'Super Mart', 'Organic Market'],
            'RESTAURANTS': ['The Bistro', 'Italian Kitchen', 'Asian Fusion', 'Steakhouse'],
            'GAS_STATIONS': ['Quick Fuel', 'Express Gas', 'Highway Stop'],
            'DEPARTMENT_STORES': ['Mega Store', 'Family Department', 'City Center'],
            'MISC_RETAIL': ['General Store', 'Variety Shop', 'Everything Plus'],
            'DRUG_STORES': ['City Pharmacy', 'Health Drugs', 'Quick Meds'],
            'BOOKSTORES': ['Book Haven', 'Reader\'s Corner', 'Library Shop'],
            'HOTELS_MOTELS': ['Grand Hotel', 'Budget Inn', 'Luxury Suites'],
            'LOCAL_TRANSIT': ['Metro Transit', 'City Bus', 'Rapid Rail'],
            'AIRLINES': ['Sky Airlines', 'Global Air', 'Express Airways'],
            'ELECTRONICS': ['Tech World', 'Gadget Store', 'Electronics Plus'],
            'SHOE_STORES': ['Shoe Palace', 'Footwear Express', 'Comfort Shoes'],
            'BARS_TAVERNS': ['The Pub', 'Sports Bar', 'Corner Tavern'],
            'FAST_FOOD': ['Quick Bites', 'Fast Eats', 'Burger Joint'],
            'BEAUTY_SALONS': ['Beauty Spot', 'Hair Studio', 'Glamour Salon'],
            'MOVIE_THEATERS': ['Cinema Palace', 'Movie House', 'Film Center'],
            'SPORTS_RECREATION': ['Fitness Club', 'Sports Center', 'Active Life'],
            'COMPUTERS': ['Computer World', 'Tech Solutions', 'PC Store'],
            'FLORISTS': ['Flower Shop', 'Bloom Garden', 'Petal Palace'],
            'DOCTORS': ['Medical Center', 'Health Clinic', 'Care Doctors'],
        }
    
    def generate_issuers(self):
        """Generate issuer institutions"""
        print(f"Generating {NUM_ISSUERS} issuers...")
        
        issuer_names = [
            'Capital Bank', 'Metro Credit Union', 'First National Bank',
            'Prosperity Bank', 'Citizens Bank', 'Union Bank',
            'Regional Trust', 'Community Bank', 'Heritage Financial',
            'Summit Bank', 'Pinnacle Bank', 'Liberty Bank'
        ]
        
        for i in range(NUM_ISSUERS):
            issuer = {
                'issuer_id': generate_id('ISS', 8),
                'issuer_name': f"{random.choice(issuer_names)} {i+1}",
                'issuer_country': 'USA',
                'primary_currency': random.choice(self.currencies),
                'created_at': datetime.now().isoformat()
            }
            self.issuers.append(issuer)
    
    def generate_acquirers(self):
        """Generate acquirer institutions"""
        print(f"Generating {NUM_ACQUIRERS} acquirers...")
        
        acquirer_names = [
            'Merchant Services Inc', 'Payment Processing Corp', 'Global Payments',
            'Commerce Bank', 'Business Bank', 'Trade Finance Corp',
            'Enterprise Bank', 'Corporate Trust', 'Commercial Bank'
        ]
        
        for i in range(NUM_ACQUIRERS):
            acquirer = {
                'acquirer_id': generate_id('ACQ', 8),
                'acquirer_name': f"{random.choice(acquirer_names)} {i+1}",
                'acquirer_country': 'USA',
                'primary_currency': random.choice(self.currencies),
                'created_at': datetime.now().isoformat()
            }
            self.acquirers.append(acquirer)
    
    def generate_merchants(self):
        """Generate merchant entities"""
        print(f"Generating {NUM_MERCHANTS} merchants...")
        
        for i in range(NUM_MERCHANTS):
            # Select random category
            mcc_code = random.choice(list(MERCHANT_CATEGORIES.keys()))
            category_name = MERCHANT_CATEGORIES[mcc_code]
            
            # Generate merchant name
            name_templates = self.merchant_name_templates[category_name]
            base_name = random.choice(name_templates)
            
            # Add location suffix for uniqueness
            locations = ['Downtown', 'Uptown', 'West End', 'East Side', 'North', 'South', 
                        'Mall', 'Plaza', 'Center', 'Square', 'Avenue', 'Street']
            merchant_name = f"{base_name} - {random.choice(locations)} #{i+1}"
            
            # Assign to random acquirer
            acquirer = random.choice(self.acquirers)
            
            # Generate annual volume (varies by merchant size)
            annual_volume = random_amount(50000, 10000000)
            
            merchant = {
                'merchant_id': generate_id('MER', 8),
                'merchant_name': merchant_name,
                'merchant_category_code': mcc_code,
                'merchant_category_name': category_name,
                'merchant_country': 'USA',
                'acquirer_id': acquirer['acquirer_id'],
                'annual_volume': annual_volume,
                'risk_level': random.choice(self.risk_levels),
                'created_at': datetime.now().isoformat()
            }
            self.merchants.append(merchant)
    
    def generate_auth_transactions(self):
        """Generate authorization transactions with realistic category-specific patterns"""
        print(f"Generating {NUM_AUTH_TRANSACTIONS} authorization transactions...")
        
        missing_code_count = int(NUM_AUTH_TRANSACTIONS * MISSING_CODE_PERCENTAGE / 100)
        missing_code_indices = set(random.sample(range(NUM_AUTH_TRANSACTIONS), missing_code_count))
        
        for i in range(NUM_AUTH_TRANSACTIONS):
            issuer = random.choice(self.issuers)
            merchant = random.choice(self.merchants)
            # Acquirer comes from merchant relationship
            acquirer_id = merchant['acquirer_id']
            
            # Category-specific decline rates (realistic industry standards)
            category = merchant['merchant_category_name']
            base_decline_rate = get_category_decline_rate(category)
            
            # Risk-based adjustments to category decline rates
            risk_level = merchant['risk_level']
            if risk_level == 'LOW':
                decline_rate = base_decline_rate * 0.8  # 20% lower than category average
            elif risk_level == 'MEDIUM':
                decline_rate = base_decline_rate * 1.0  # Category average
            else:  # HIGH
                decline_rate = base_decline_rate * 1.4  # 40% higher than category average
            
            # Convert to decimal and cap at reasonable maximums
            decline_rate = min(decline_rate / 100, 0.20)  # Cap at 20% decline rate
            
            # Determine approval/decline and transaction code
            is_approved = random.random() > decline_rate
            
            if is_approved:
                transaction_code = '000'
                auth_status = 'APPROVED'
            else:
                # Realistic decline code distribution
                decline_codes = ['100', '101', '102']
                decline_weights = [0.7, 0.2, 0.1]  # Most declines are 100
                transaction_code = random.choices(decline_codes, weights=decline_weights)[0]
                auth_status = 'DECLINED'
            
            # Handle missing codes (system errors)
            if i in missing_code_indices:
                transaction_code = None
                auth_status = 'APPROVED' if is_approved else 'DECLINED'
            
            # Category-specific transaction amount
            min_amt, max_amt = get_category_amount_range(category)
            transaction_amount = random_amount(min_amt, max_amt)
            
            # Transaction date and timestamp
            txn_date = random_date(START_DATE, END_DATE)
            txn_timestamp = random_datetime(txn_date)
            
            transaction = {
                'transaction_id': generate_alpha_numeric_id(16),
                'issuer_id': issuer['issuer_id'],
                'acquirer_id': acquirer_id,
                'merchant_id': merchant['merchant_id'],
                'transaction_amount': transaction_amount,
                'transaction_date': txn_date.strftime('%Y-%m-%d'),
                'transaction_timestamp': txn_timestamp.isoformat(),
                'transaction_type': random.choice(self.transaction_types),
                'issuer_currency': issuer['primary_currency'],
                'acquirer_currency': 'USD',  # Most acquirers use USD
                'transaction_code': transaction_code,
                'card_last_four': f"{random.randint(1000, 9999)}",
                'authorization_status': auth_status,
                'created_at': datetime.now().isoformat()
            }
            
            self.auth_transactions.append(transaction)
    
    def generate_settlement_transactions(self):
        """Generate settlement transactions with realistic variance and timing patterns"""
        print(f"Generating settlement transactions...")
        
        # Only settle approved transactions
        approved_transactions = [txn for txn in self.auth_transactions if txn['authorization_status'] == 'APPROVED']
        
        # Calculate settlement counts based on industry standards
        total_approved = len(approved_transactions)
        unsettled_count = int(total_approved * UNSETTLED_PERCENTAGE / 100)
        total_settlements = total_approved - unsettled_count
        
        # Variance distribution calculations
        exact_match_count = int(total_settlements * EXACT_MATCH_PERCENTAGE / 100)
        low_variance_count = int(total_settlements * LOW_VARIANCE_PERCENTAGE / 100)
        medium_variance_count = int(total_settlements * MEDIUM_VARIANCE_PERCENTAGE / 100)
        high_variance_count = int(total_settlements * HIGH_VARIANCE_PERCENTAGE / 100)
        extreme_variance_count = int(total_settlements * EXTREME_VARIANCE_PERCENTAGE / 100)
        
        # Adjust for rounding errors
        total_variance = exact_match_count + low_variance_count + medium_variance_count + high_variance_count + extreme_variance_count
        if total_variance != total_settlements:
            exact_match_count += total_settlements - total_variance
        
        print(f"  - Approved transactions: {total_approved}")
        print(f"  - Total settlements: {total_settlements}")
        print(f"  - Unsettled (will remain unsettled): {unsettled_count}")
        print(f"  - Exact matches (0% variance): {exact_match_count}")
        print(f"  - Low variance (0-1%): {low_variance_count}")
        print(f"  - Medium variance (1-2%): {medium_variance_count}")
        print(f"  - High variance (2-5%): {high_variance_count}")
        print(f"  - Extreme variance (>5%): {extreme_variance_count}")
        
        # Randomly select which approved transactions to settle
        auth_to_settle = random.sample(approved_transactions, total_settlements)
        
        # Create variance type assignments
        variance_assignments = (
            ['exact'] * exact_match_count +
            ['low_variance'] * low_variance_count +
            ['medium_variance'] * medium_variance_count +
            ['high_variance'] * high_variance_count +
            ['extreme_variance'] * extreme_variance_count
        )
        random.shuffle(variance_assignments)
        
        # Settlement timeframe distribution (industry-aligned)
        timeframe_weights = {
            0: 0.07,   # 7% same-day settlements
            1: 0.43,   # 43% next-day settlements
            2: 0.25,   # 25% 2-day settlements
            3: 0.18,   # 18% 3-day settlements
            4: 0.04,   # 4% 4-day settlements
            5: 0.02,   # 2% 5-day settlements
            6: 0.01    # 1% 6+ day settlements
        }
        
        for auth_txn, variance_type in zip(auth_to_settle, variance_assignments):
            auth_date = datetime.strptime(auth_txn['transaction_date'], '%Y-%m-%d')
            
            # Select settlement delay based on realistic distribution
            settlement_delay = random.choices(
                list(timeframe_weights.keys()),
                weights=list(timeframe_weights.values())
            )[0]
            
            # Handle extended settlement periods (4-7+ days)
            if settlement_delay == 6:  # Extend some to 7-14 days for dispute resolution
                settlement_delay = random.randint(6, 14)
            
            settlement_date = auth_date + timedelta(days=settlement_delay)
            
            # Acquirer typically settles first, issuer 1 day later
            acquirer_settlement_date = settlement_date
            issuer_settlement_date = settlement_date + timedelta(days=random.randint(0, 1))
            
            # Get merchant category for variance calculations
            merchant_category = next(
                (m['merchant_category_name'] for m in self.merchants if m['merchant_id'] == auth_txn['merchant_id']),
                'MISC_RETAIL'
            )
            
            auth_amount = auth_txn['transaction_amount']
            acquirer_settlement_amt = calculate_settlement_amount(auth_amount, variance_type, merchant_category)
            
            # Issuer amount includes interchange fee adjustment
            interchange_fee, network_fee = calculate_fees(auth_amount)
            issuer_settlement_amt = auth_amount - interchange_fee
            
            settlement = {
                'transaction_id': generate_alpha_numeric_id(16),
                'auth_transaction_id': auth_txn['transaction_id'],
                'issuer_id': auth_txn['issuer_id'],
                'acquirer_id': auth_txn['acquirer_id'],
                'merchant_id': auth_txn['merchant_id'],
                'transaction_amount': auth_amount,
                'transaction_date': auth_txn['transaction_date'],
                'transaction_type': auth_txn['transaction_type'],
                'issuer_currency': auth_txn['issuer_currency'],
                'acquirer_currency': auth_txn['acquirer_currency'],
                'acquirer_settlement_amount': acquirer_settlement_amt,
                'issuer_settlement_amount': issuer_settlement_amt,
                'acquirer_settlement_date': acquirer_settlement_date.strftime('%Y-%m-%d'),
                'issuer_settlement_date': issuer_settlement_date.strftime('%Y-%m-%d'),
                'transaction_settlement_date': settlement_date.strftime('%Y-%m-%d'),
                'settlement_status': 'SETTLED',
                'interchange_fee': interchange_fee,
                'network_fee': network_fee,
                'created_at': datetime.now().isoformat()
            }
            
            self.settlement_transactions.append(settlement)
    
    def write_csv(self, filename, data, fieldnames):
        """Write data to CSV file"""
        filepath = OUTPUT_DIR / filename
        print(f"Writing {len(data)} records to {filepath}...")
        
        with open(filepath, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
    
    def generate_all(self):
        """Generate all data and write to CSV files"""
        print("\n" + "="*60)
        print("FinIQ Data Generator v2.0")
        print("Financial Intelligence & Quality Platform")
        print("="*60 + "\n")
        
        # Generate reference data
        self.generate_issuers()
        self.generate_acquirers()
        self.generate_merchants()
        
        # Generate transaction data
        self.generate_auth_transactions()
        self.generate_settlement_transactions()
        
        # Write to CSV files
        print("\nWriting CSV files...")
        
        self.write_csv('issuers.csv', self.issuers, [
            'issuer_id', 'issuer_name', 'issuer_country', 
            'primary_currency', 'created_at'
        ])
        
        self.write_csv('acquirers.csv', self.acquirers, [
            'acquirer_id', 'acquirer_name', 'acquirer_country',
            'primary_currency', 'created_at'
        ])
        
        self.write_csv('merchants.csv', self.merchants, [
            'merchant_id', 'merchant_name', 'merchant_category_code',
            'merchant_category_name', 'merchant_country', 'acquirer_id',
            'annual_volume', 'risk_level', 'created_at'
        ])
        
        self.write_csv('auth_transactions.csv', self.auth_transactions, [
            'transaction_id', 'issuer_id', 'acquirer_id', 'merchant_id',
            'transaction_amount', 'transaction_date', 'transaction_timestamp',
            'transaction_type', 'issuer_currency', 'acquirer_currency',
            'transaction_code', 'card_last_four', 'authorization_status',
            'created_at'
        ])
        
        self.write_csv('settlement_transactions.csv', self.settlement_transactions, [
            'transaction_id', 'auth_transaction_id', 'issuer_id', 'acquirer_id',
            'merchant_id', 'transaction_amount', 'transaction_date', 'transaction_type',
            'issuer_currency', 'acquirer_currency', 'acquirer_settlement_amount',
            'issuer_settlement_amount', 'acquirer_settlement_date',
            'issuer_settlement_date', 'transaction_settlement_date',
            'settlement_status', 'interchange_fee', 'network_fee', 'created_at'
        ])
        
        print("\n" + "="*60)
        print("Data Generation Summary")
        print("="*60)
        print(f"Issuers: {len(self.issuers)}")
        print(f"Acquirers: {len(self.acquirers)}")
        print(f"Merchants: {len(self.merchants)}")
        print(f"Authorization Transactions: {len(self.auth_transactions):,}")
        print(f"Settlement Transactions: {len(self.settlement_transactions):,}")
        print(f"Unsettled Transactions: {len(self.auth_transactions) - len(self.settlement_transactions):,}")
        print(f"\nKey Ratios:")
        print(f"  - Transactions per Issuer: {len(self.auth_transactions) // len(self.issuers):,}")
        print(f"  - Transactions per Acquirer: {len(self.auth_transactions) // len(self.acquirers):,}")
        print(f"  - Transactions per Merchant: {len(self.auth_transactions) // len(self.merchants)}")
        print(f"  - Merchants per Acquirer: {len(self.merchants) / len(self.acquirers):.1f}")
        print(f"  - Settlement Rate: {len(self.settlement_transactions) / len(self.auth_transactions) * 100:.1f}%")
        print(f"\nOutput directory: {OUTPUT_DIR.absolute()}")
        print("="*60 + "\n")


if __name__ == '__main__':
    generator = DataGenerator()
    generator.generate_all()