"""
PostgreSQL Data Generators - Modified for Realistic Patterns

This module contains functions to generate realistic data for PostgreSQL tables in the telco schema.
The data includes meaningful patterns and correlations that reflect real-world telco scenarios.
"""

import random
import uuid
import datetime
import math
from faker import Faker
from typing import Dict, List, Any

# Initialize Faker
fake = Faker()

# Constants
CUSTOMER_SEGMENTS = ["Premium", "Standard", "Budget", "Business", "Family"]
PLAN_TYPES = ["Mobile", "Internet", "Bundle", "IoT", "Enterprise"]
DEVICE_BRANDS = ["Apple", "Samsung", "Google", "Xiaomi", "OnePlus", "Huawei"]
DEVICE_MODELS = {
    "Apple": ["iPhone 13", "iPhone 14", "iPhone 15", "iPhone SE"],
    "Samsung": ["Galaxy S22", "Galaxy S23", "Galaxy Note 20", "Galaxy A53"],
    "Google": ["Pixel 6", "Pixel 7", "Pixel 7a", "Pixel Fold"],
    "Xiaomi": ["Mi 12", "Redmi Note 11", "Poco F4", "Mi Mix Fold"],
    "OnePlus": ["OnePlus 10", "OnePlus 11", "Nord 2", "Nord CE"],
    "Huawei": ["P50", "Mate 40", "Nova 9", "Mate X2"]
}
NODE_STATUSES = ["Active", "Maintenance", "Upgrading", "Offline"]
CALL_TYPES = ["Outgoing", "Incoming", "Missed", "Conference", "Video"]
MESSAGE_TYPES = ["SMS", "MMS", "RCS"]
PAYMENT_STATUSES = ["Paid", "Pending", "Overdue", "Failed", "Refunded"]
PLAN_STATUSES = ["active", "inactive", "activating"]
COUNTRIES = {
    "United States": ["California", "New York", "Texas", "Florida", "Illinois"],
    "Canada": ["Ontario", "Quebec", "British Columbia", "Alberta", "Manitoba"],
    "United Kingdom": ["England", "Scotland", "Wales", "Northern Ireland"],
    "Australia": ["New South Wales", "Victoria", "Queensland", "Western Australia"]
}

# Define geographic hotspots for network quality
NETWORK_HOTSPOTS = [
    {"lat": 37.7749, "lon": -122.4194, "radius": 1.0, "quality": "excellent"},  # San Francisco
    {"lat": 40.7128, "lon": -74.0060, "radius": 1.0, "quality": "excellent"},   # New York
    {"lat": 34.0522, "lon": -118.2437, "radius": 1.0, "quality": "excellent"},  # Los Angeles
    {"lat": 32.7767, "lon": -96.7970, "radius": 1.0, "quality": "good"},        # Dallas
    {"lat": 41.8781, "lon": -87.6298, "radius": 1.0, "quality": "good"},        # Chicago
    {"lat": 29.7604, "lon": -95.3698, "radius": 1.0, "quality": "moderate"},    # Houston
    {"lat": 39.9612, "lon": -82.9988, "radius": 1.0, "quality": "moderate"},    # Columbus
    {"lat": 43.0731, "lon": -89.4012, "radius": 1.0, "quality": "poor"}         # Madison
]

# Add this helper function at the top of the script, after imports
def calculate_age(birth_date: datetime.date) -> int:
    """Calculate age from birth date."""
    today = datetime.date.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age

def generate_dob(target_age: int) -> datetime.date:
    """Generate a date of birth that would result in the target age."""
    today = datetime.date.today()
    # Set birth year to get the target age
    birth_year = today.year - target_age
    
    # Add some randomness to the birth month and day
    birth_month = random.randint(1, 12)
    max_day = 28 if birth_month == 2 else 30 if birth_month in [4, 6, 9, 11] else 31
    birth_day = random.randint(1, max_day)
    
    # If the generated date would make the person one year older or younger, adjust
    birth_date = datetime.date(birth_year, birth_month, birth_day)
    calculated_age = calculate_age(birth_date)
    
    if calculated_age > target_age:
        # Person is too old, add a year to birth year
        birth_date = datetime.date(birth_year + 1, birth_month, birth_day)
    elif calculated_age < target_age:
        # Person is too young, subtract a year from birth year
        birth_date = datetime.date(birth_year - 1, birth_month, birth_day)
        
    return birth_date

def generate_phone_number() -> str:
    """Generate a realistic phone number."""
    return f"+{random.randint(1, 9)}{random.randint(10, 99)}{random.randint(1000000, 9999999)}"

def generate_cell_number() -> str:
    """Generate a cell number (last 10 digits of phone number)."""
    return f"{random.randint(1000000000, 9999999999)}"

def fake_email():
    """Generate a random email that's suitable for large unique datasets."""
    # Get random username from faker but add randomness for uniqueness
    username = fake.user_name() + str(random.randint(1, 999999))
    
    # Get random domain with realistic frequency distribution
    domains = [
        "gmail.com", "gmail.com", "gmail.com", "gmail.com", "gmail.com",
        "yahoo.com", "yahoo.com", "yahoo.com",
        "outlook.com", "outlook.com", 
        "hotmail.com", "hotmail.com",
        "icloud.com",
        "aol.com", "protonmail.com", "zoho.com", "mail.com",
        "yandex.com", "gmx.com", "me.com", "live.com",
        "comcast.net", "verizon.net", "msn.com", "att.net", 
        "cox.net", "charter.net", "earthlink.net", "sbcglobal.net",        
        "btinternet.com", "web.de", "mail.ru", "qq.com", "naver.com"
    ]
    
    domain = random.choice(domains)
    
    return f"{username}@{domain}"

def generate_auth_users(num_customers: int) -> List[Dict]:
    """Generate users for auth database."""
    users = []
    for i in range(1, num_customers + 1):
        # Special case for user ID 7 - Alexis Smith
        if i == 7:
            email = "alexis.marchand@gmail.com"
            role = "customer"
        else:
            email = fake_email()
            # Most users are customers, but a few are support
            role = "customer" if random.random() < 0.95 else "support"
            
        # Using a fixed password hash for simplicity
        password_hash = "$2a$10$DSRHAPZP0fuEFioGOPOdW.kgFWZvQgmMihaBYsUs8rO4cdHFFK7cS"
        
        # Newer accounts (higher IDs) were created more recently
        if i < num_customers * 0.3:  # 30% oldest accounts
            created_at = fake.date_time_between(start_date="-3y", end_date="-2y").isoformat()
        elif i < num_customers * 0.7:  # 40% middle-aged accounts
            created_at = fake.date_time_between(start_date="-2y", end_date="-1y").isoformat()
        else:  # 30% newest accounts
            created_at = fake.date_time_between(start_date="-1y", end_date="-1m").isoformat()
            
        # Last update typically more recent than creation
        updated_at = fake.date_time_between(
            start_date=datetime.datetime.fromisoformat(created_at), 
            end_date="now"
        ).isoformat()
        
        users.append({
            "id": i,
            "email": email,
            "password": password_hash,
            "roles": role,
            "created_at": created_at,
            "updated_at": updated_at
        })
    return users

def generate_customers(auth_users: List[Dict]) -> List[Dict]:
    """Generate customer data with realistic correlations."""
    customers = []
    
    # Geographic distribution of customers
    # Based on population distribution
    region_weights = {
        "United States": 0.6,
        "Canada": 0.2,
        "United Kingdom": 0.15,
        "Australia": 0.05
    }
    
    # Age-based segment distribution
    # Different age groups prefer different segments
    age_segments = {
        (18, 25): {"Premium": 0.15, "Standard": 0.25, "Budget": 0.45, "Business": 0.05, "Family": 0.1},
        (26, 35): {"Premium": 0.25, "Standard": 0.3, "Budget": 0.2, "Business": 0.15, "Family": 0.1},
        (36, 45): {"Premium": 0.2, "Standard": 0.25, "Budget": 0.15, "Business": 0.2, "Family": 0.2},
        (46, 60): {"Premium": 0.15, "Standard": 0.3, "Budget": 0.2, "Business": 0.25, "Family": 0.1},
        (61, 80): {"Premium": 0.1, "Standard": 0.3, "Budget": 0.4, "Business": 0.1, "Family": 0.1}
    }
    
    for i, user in enumerate(auth_users, 1):
        # Special case for customer ID 7 - Alexis Smith
        if i == 7:
            first_name = "Alexis"
            last_name = "Marchand"
            country = "United States"
            state = "California"
            city = "San Francisco"
            address = "576 Folsom Street"
            postcode = "94105"
            phone_number = "+14158214231"
            segment = "Premium"
            satisfaction_score = 5
            churn_risk = 0.55
            churn_risk_factors = "{Service quality issues}"
            target_age = 34  # Mid-30s tech-savvy user
            dob = generate_dob(target_age)
            image = "avatar_20.jpg"
            last_survey_date_str = "2025-04-03"
        else:
            first_name = fake.first_name()
            last_name = fake.last_name()
            
            # Weighted selection of country based on distribution
            country = random.choices(
                list(region_weights.keys()),
                weights=list(region_weights.values())
            )[0]
            state = random.choice(COUNTRIES[country])
            
            # Generate a realistic age distribution
            # Age follows a normal-ish distribution centered around 40
            target_age = int(random.betavariate(2, 2) * 62) + 18  # Between 18-80
            dob = generate_dob(target_age)
            
            # Find the right age bracket for segment distribution
            age_bracket = next((bracket for bracket in age_segments.keys() 
                              if bracket[0] <= target_age <= bracket[1]), (36, 45))
            
            # Select segment based on age bracket
            segment_weights = age_segments[age_bracket]
            segment = random.choices(
                list(segment_weights.keys()),
                weights=list(segment_weights.values())
            )[0]
            
            # Generate correlated satisfaction score
            # Premium and Business tend to have higher expectations but also better service
            if segment == "Premium":
                base_satisfaction = 7
            elif segment == "Business":
                base_satisfaction = 6.5
            elif segment == "Family":
                base_satisfaction = 6
            elif segment == "Standard":
                base_satisfaction = 5.5
            else:  # Budget
                base_satisfaction = 5
                
            # Account age also impacts satisfaction - newer accounts tend to be more satisfied
            account_age_factor = 0
            created_at = datetime.datetime.fromisoformat(user["created_at"])
            days_since_creation = (datetime.datetime.now() - created_at).days
            
            if days_since_creation < 180:  # Less than 6 months
                account_age_factor = 1
            elif days_since_creation < 365:  # 6-12 months
                account_age_factor = 0.5
            elif days_since_creation < 730:  # 1-2 years
                account_age_factor = 0
            else:  # > 2 years
                account_age_factor = -0.5
                
            # Calculate final satisfaction with some randomness
            satisfaction_score = max(1, min(10, round(
                base_satisfaction + account_age_factor + random.uniform(-1.5, 1.5)
            )))
            
            # Churn risk correlates with satisfaction but isn't perfectly inverse
            base_churn_risk = 1.0 - (satisfaction_score / 12.0)  # Base inverse relationship
            
            # Different segments have different churn risk profiles
            if segment == "Premium":
                # Premium customers are less likely to churn even when dissatisfied
                segment_churn_factor = -0.1
            elif segment == "Business":
                # Business customers are very sticky
                segment_churn_factor = -0.15
            elif segment == "Budget":
                # Budget customers are price-sensitive and likely to churn
                segment_churn_factor = 0.15
            else:
                segment_churn_factor = 0
                
            # Account age also impacts churn risk
            if days_since_creation < 90:  # First 3 months - high churn risk
                tenure_churn_factor = 0.2
            elif days_since_creation < 365:  # 3-12 months - moderate risk
                tenure_churn_factor = 0.1
            elif days_since_creation < 730:  # 1-2 years - low risk
                tenure_churn_factor = -0.05
            else:  # > 2 years - very low risk
                tenure_churn_factor = -0.1
                
            # Calculate final churn risk
            churn_risk = round(max(0.1, min(0.95, 
                base_churn_risk + segment_churn_factor + tenure_churn_factor + random.uniform(-0.1, 0.1)
            )), 2)
            
            # Generate realistic churn risk factors
            if churn_risk > 0.4:
                # Number of factors increases with churn risk
                num_factors = 1 + int(churn_risk * 3)
                
                # Different segments have different churn factors
                if segment == "Premium":
                    # Premium users care about quality and experience
                    factors_pool = [
                        "Service quality issues",
                        "Customer service experience",
                        "Network coverage",
                        "Competitor offers",
                        "Device upgrade needs"
                    ]
                    weights = [0.3, 0.25, 0.2, 0.15, 0.1]
                elif segment == "Budget":
                    # Budget users care about price
                    factors_pool = [
                        "Price sensitivity",
                        "Competitor offers",
                        "Contract ending soon",
                        "Service quality issues",
                        "Moving location"
                    ]
                    weights = [0.4, 0.25, 0.15, 0.1, 0.1]
                elif segment == "Business":
                    # Business users care about reliability and service
                    factors_pool = [
                        "Service quality issues",
                        "Customer service experience",
                        "Network coverage",
                        "Competitor offers",
                        "Contract ending soon"
                    ]
                    weights = [0.3, 0.3, 0.2, 0.1, 0.1]
                else:  # Standard, Family
                    # Standard/Family users have mixed concerns
                    factors_pool = [
                        "Price sensitivity",
                        "Service quality issues",
                        "Customer service experience",
                        "Moving location",
                        "Competitor offers",
                        "Network coverage",
                        "Contract ending soon"
                    ]
                    weights = [0.2, 0.2, 0.15, 0.15, 0.1, 0.1, 0.1]
                    
                # Select factors with replacement (more important factors can appear multiple times)
                factors = []
                for _ in range(num_factors):
                    factor = random.choices(factors_pool, weights=weights)[0]
                    if factor not in factors:  # No duplicates
                        factors.append(factor)
                
                churn_risk_factors = "{" + ",".join(factors) + "}"
            else:
                churn_risk_factors = None
        
        # Generate image with some brands more popular in different segments
        if segment == "Premium":
            image_num = random.choices(range(1, 21), weights=[5]*5 + [3]*5 + [1]*10)[0]
        elif segment == "Budget":
            image_num = random.choices(range(1, 21), weights=[1]*5 + [3]*5 + [5]*10)[0]
        else:
            image_num = random.randint(1, 20)
            
        image = f"avatar_{image_num}.jpg"
        
        # Generate last survey date
        # Higher satisfaction, more likely to have completed a survey
        survey_probability = 0.4 + (satisfaction_score / 20)  # 0.4 to 0.9
        if random.random() < survey_probability:
            last_survey_date = fake.date_time_between(start_date="-6m", end_date="now").date()
            last_survey_date_str = last_survey_date.isoformat()
        else:
            last_survey_date_str = None
        
        customers.append({
            "customer_id": i,
            "first_name": first_name,
            "last_name": last_name,
            "email": user["email"],
            "phone_number": generate_phone_number(),
            "address": fake.street_address(),
            "city": fake.city(),
            "state": state,
            "postcode": fake.postcode(),
            "country": country,
            "dob": dob.isoformat(),
            "image": image,
            "segment": segment,
            "auth_user_id": user["id"],
            "satisfaction_score": satisfaction_score,
            "last_survey_date": last_survey_date_str,
            "churn_risk": churn_risk,
            "churn_risk_factors": churn_risk_factors
        })
    return customers

def generate_plans(num_plans: int) -> List[Dict]:
    """Generate plan data with realistic distributions and correlations."""
    plans = []
    
    # Realistic distribution of plan types
    plan_type_weights = {
        "Mobile": 0.5,     # 50% of plans are mobile
        "Internet": 0.25,  # 25% internet
        "Bundle": 0.15,    # 15% bundles
        "IoT": 0.05,       # 5% IoT
        "Enterprise": 0.05 # 5% enterprise
    }
    
    # More varied name components
    PREFIXES = {
        "Mobile": [
            'Basic', 'Standard', 'Premium', 'Ultimate', 'Essential', 'Freedom', 
            'Value', 'Smart', 'Elite', 'Flex', 'Max', 'Power', 'Select', 'Prime',
            'Everyday', 'Connect', 'Go', 'Lite', 'Advance', 'Pro'
        ],
        
        "Internet": [
            '', 'High-Speed ', 'Ultra ', 'Fiber ', 'Premium ', 'Turbo ',
            'Fast ', 'Broadband ', 'Streaming ', 'Home '
        ],
        
        "Bundle": [
            'Home & Mobile', 'Complete', 'Family', 'All-in-One', 'Ultimate', 
            'Total', 'Full-Service', 'Connected Home', 'Smart Home', 'Digital'
        ],
        
        "IoT": [
            'IoT', 'Smart Device', 'Connected', 'Device', 'Smart', 'Sensor',
            'Tracker', 'Remote', 'Monitoring'
        ],
        
        "Enterprise": [
            'Business', 'Corporate', 'Enterprise', 'Commercial', 'Professional',
            'Office', 'Workforce', 'Operations', 'Executive', 'Team'
        ]
    }
    
    for i in range(1, num_plans + 1):
        # Select plan type based on realistic distribution
        plan_type = random.choices(
            list(plan_type_weights.keys()),
            weights=list(plan_type_weights.values())
        )[0]
        
        # Initialize default values for all plans
        data_limit_gb = None
        voice_limit_minutes = None
        sms_limit = None
        international_roaming = False
        roaming_countries = None
        roaming_data_gb = None
        roaming_voice_minutes = None
        
        # Add more variability to pricing with continuous ranges
        pricing_variation = 0.85 + (random.random() * 0.3)  # ±15% variation
        
        if plan_type == "Mobile":
            # More realistic tiers of data options - not uniform distribution
            data_options = [
                (1, 0.05),    # 1GB - 5% of plans
                (3, 0.1),     # 3GB - 10% of plans
                (5, 0.2),     # 5GB - 20% of plans
                (10, 0.25),   # 10GB - 25% of plans
                (20, 0.2),    # 20GB - 20% of plans
                (50, 0.1),    # 50GB - 10% of plans
                (None, 0.1)   # Unlimited - 10% of plans
            ]
            data_gb_choices, data_weights = zip(*data_options)
            data_gb = random.choices(data_gb_choices, weights=data_weights)[0]
            
            prefix = random.choice(PREFIXES["Mobile"])
            
            # Vary naming patterns
            name_pattern = random.randint(0, 3)
            if name_pattern == 0:
                name = f"{prefix} Mobile {data_gb}GB" if data_gb else f"{prefix} Mobile Unlimited"
            elif name_pattern == 1:
                name = f"{prefix} {data_gb}GB Plan" if data_gb else f"{prefix} Unlimited Plan"
            elif name_pattern == 2:
                name = f"{data_gb}GB {prefix}" if data_gb else f"Unlimited {prefix}"
            else:
                name = f"{prefix} {random.choice(['Plan', 'Mobile', 'Connect', 'Service'])}"
            
            description = f"Mobile plan with {'unlimited' if data_gb is None else f'{data_gb}GB'} data"
            
            # More varied fee calculation
            if data_gb is None:  # Unlimited
                base_fee = random.uniform(45, 65)
            else:
                # Progressive pricing based on data amount with diminishing returns
                if data_gb <= 5:
                    base_fee = 15 + (data_gb * 2.5)
                elif data_gb <= 20:
                    base_fee = 25 + (data_gb * 1.2)
                else:
                    base_fee = 45 + (data_gb * 0.5)
            
            fee = round(base_fee * pricing_variation, 2)
            
            # Set mobile-specific fields with more variation
            data_limit_gb = data_gb
            
            # Voice limits correlated with data - more data, more voice
            if data_gb is None:  # Unlimited data
                voice_options = [(None, 0.8), (3000, 0.2)]  # 80% unlimited, 20% 3000 min
            elif data_gb >= 20:  # High data
                voice_options = [(None, 0.6), (3000, 0.3), (1500, 0.1)]
            elif data_gb >= 5:   # Medium data
                voice_options = [(None, 0.2), (2000, 0.3), (1000, 0.5)]
            else:  # Low data
                voice_options = [(1000, 0.3), (750, 0.3), (500, 0.4)]
                
            voice_choices, voice_weights = zip(*voice_options)
            voice_limit_minutes = random.choices(voice_choices, weights=voice_weights)[0]
            
            # SMS limits - similar pattern to voice
            if data_gb is None:  # Unlimited data
                sms_options = [(None, 0.9), (2000, 0.1)]  # 90% unlimited
            elif data_gb >= 20:  # High data
                sms_options = [(None, 0.7), (2000, 0.3)]
            elif data_gb >= 5:   # Medium data
                sms_options = [(None, 0.3), (1500, 0.4), (1000, 0.3)]
            else:  # Low data
                sms_options = [(1000, 0.4), (750, 0.3), (500, 0.3)]
                
            sms_choices, sms_weights = zip(*sms_options)
            sms_limit = random.choices(sms_choices, weights=sms_weights)[0]
            
            # Add text about limits to description
            if voice_limit_minutes is None:
                description += ", unlimited calls"
            else:
                description += f", {voice_limit_minutes} minutes"
                
            if sms_limit is None:
                description += " and unlimited texts"
            else:
                description += f" and {sms_limit} texts"
            
            # Adjust roaming probability based on plan quality
            is_premium = (data_gb is None or data_gb >= 20) and (voice_limit_minutes is None) 
            roaming_probability = 0.7 if is_premium else 0.1
            international_roaming = random.random() < roaming_probability
            
            if international_roaming:
                # Premium plans cover more countries
                all_countries = list(COUNTRIES.keys())
                if is_premium:
                    num_countries = random.choices([3, 4], weights=[0.3, 0.7])[0]
                else:
                    num_countries = random.choices([1, 2], weights=[0.7, 0.3])[0]
                    
                countries_sample = random.sample(all_countries, num_countries)
                roaming_countries = "{" + ",".join(country for country in countries_sample) + "}"
                
                # Roaming data and voice based on plan quality
                if is_premium:
                    roaming_data_gb = round(random.uniform(5.0, 10.0), 2)
                    roaming_voice_minutes = random.randint(300, 600)
                else:
                    roaming_data_gb = round(random.uniform(0.5, 3.0), 2)
                    roaming_voice_minutes = random.randint(30, 150)
                
                # Increase fee for roaming
                fee += num_countries * 1.5
                fee += roaming_data_gb * 2
                
        elif plan_type == "Internet":
            # Realistic speed tiers - not uniformly distributed
            speed_options = [
                (25, 0.1),     # 25Mbps - 10% of plans
                (50, 0.15),    # 50Mbps - 15% of plans
                (100, 0.25),   # 100Mbps - 25% of plans
                (300, 0.25),   # 300Mbps - 25% of plans
                (500, 0.15),   # 500Mbps - 15% of plans
                (1000, 0.1)    # 1Gbps - 10% of plans
            ]
            speed_choices, speed_weights = zip(*speed_options)
            speed = random.choices(speed_choices, weights=speed_weights)[0]
            
            prefix = random.choice(PREFIXES["Internet"])
            
            # More naming patterns
            name_pattern = random.randint(0, 2)
            if name_pattern == 0:
                name = f"{prefix}{speed}Mbps Internet"
            elif name_pattern == 1:
                name = f"{speed}Mbps {prefix}Internet"
            else:
                name = f"{prefix}Internet {speed}"
                
            description = f"Home internet with {speed}Mbps download speed"
            
            # More varied pricing based on speed with some randomness
            base_fee = 20 + (speed * 0.08)
            fee = round(base_fee * pricing_variation, 2)
            
            # Data limits correlated with speed
            if speed >= 500:  # High-speed usually unlimited
                data_options = [(None, 0.8), (2000, 0.15), (1500, 0.05)]
            elif speed >= 300:  # Mid-high speed
                data_options = [(None, 0.5), (2000, 0.25), (1500, 0.15), (1000, 0.1)]
            elif speed >= 100:  # Medium speed
                data_options = [(None, 0.2), (1500, 0.3), (1000, 0.3), (750, 0.2)]
            else:  # Low speed
                data_options = [(1000, 0.2), (750, 0.3), (500, 0.5)]
                
            data_choices, data_weights = zip(*data_options)
            data_limit_gb = random.choices(data_choices, weights=data_weights)[0]
                
            if data_limit_gb is not None:
                description += f" and {data_limit_gb}GB data limit"
            else:
                description += " with unlimited data"
                # Premium for unlimited
                fee += random.uniform(10, 15)
            
        elif plan_type == "Bundle":
            # More varied bundle sizes
            sizes = ['XS', 'S', 'M', 'L', 'XL', 'XXL']
            size_weights = [0.05, 0.15, 0.3, 0.3, 0.15, 0.05]  # Bell curve distribution
            size = random.choices(sizes, weights=size_weights)[0]
            size_index = sizes.index(size)
            
            prefix = random.choice(PREFIXES["Bundle"])
            name = f"{prefix} Bundle {size}"
            description = "Combined home internet and mobile service"
            
            # More varied pricing based on size
            base_fee = 60 + (size_index * 10)
            fee = round(base_fee * pricing_variation, 2)
            
            # Set bundle-specific fields with size-dependent variation
            if size_index >= 4:  # XL, XXL
                data_limit_gb = random.choices([None, 750, 500], weights=[0.7, 0.2, 0.1])[0]
                voice_limit_minutes = random.choices([None, 5000], weights=[0.8, 0.2])[0]
                sms_limit = random.choices([None, 5000], weights=[0.8, 0.2])[0]
            elif size_index >= 2:  # M, L
                data_limit_gb = random.choices([None, 500, 300, 200], weights=[0.3, 0.3, 0.2, 0.2])[0]
                voice_limit_minutes = random.choices([None, 3000, 2000], weights=[0.4, 0.3, 0.3])[0]
                sms_limit = random.choices([None, 2000, 1000], weights=[0.4, 0.3, 0.3])[0]
            else:  # XS, S
                data_limit_gb = random.choices([300, 200, 100], weights=[0.2, 0.4, 0.4])[0]
                voice_limit_minutes = random.choices([2000, 1500, 1000], weights=[0.2, 0.4, 0.4])[0]
                sms_limit = random.choices([2000, 1000, 500], weights=[0.2, 0.3, 0.5])[0]
            
            # Add feature details to description
            description += f" with {data_limit_gb}GB data" if data_limit_gb else " with unlimited data"
            
            # Bundles more likely to have roaming based on size
            roaming_probability = 0.1 + (size_index * 0.15)
            international_roaming = random.random() < roaming_probability
            
            if international_roaming:
                all_countries = list(COUNTRIES.keys())
                num_countries = min(len(all_countries), 1 + size_index)
                countries_sample = random.sample(all_countries, num_countries)
                roaming_countries = "{" + ",".join(country for country in countries_sample) + "}"
                roaming_data_gb = round(random.uniform(1.0, 5.0) * (1 + size_index * 0.5), 2)
                roaming_voice_minutes = random.randint(60, 300) * (1 + size_index // 2)
                
                # Increase fee for roaming
                fee += num_countries * 2
                
        elif plan_type == "IoT":
            # Tier distribution - most are basic or plus
            tier_options = [
                ('Basic', 1, 0.4),
                ('Plus', 3, 0.3),
                ('Pro', 5, 0.15),
                ('Advanced', 10, 0.1),
                ('Premium', 20, 0.03),
                ('Enterprise', 50, 0.02)
            ]
            tiers, devices, tier_weights = zip(*tier_options)
            tier_index = random.choices(range(len(tiers)), weights=tier_weights)[0]
            tier_name, devices = tiers[tier_index], devices[tier_index]
            
            prefix = random.choice(PREFIXES["IoT"])
            
            # Naming patterns
            name_pattern = random.randint(0, 2)
            if name_pattern == 0:
                name = f"{prefix} Connect {tier_name}"
            elif name_pattern == 1:
                name = f"{tier_name} {prefix} Plan"
            else:
                name = f"{prefix} {tier_name} {devices}-Device"
                
            description = f"Connectivity for {devices} IoT devices"
            
            # Pricing based on tier
            base_fee = 5 + (devices * 0.8)
            fee = round(base_fee * pricing_variation, 2)
            
            # Data limits scale with devices
            data_limit_gb = min(10, devices // 2 + 1)
            description += f" with {data_limit_gb}GB data"
            
        else:  # Enterprise
            # Enterprise size distribution - most are small/medium
            size_options = [
                ('Starter', 0, 0.15),
                ('Small', 1, 0.3),
                ('Medium', 2, 0.35),
                ('Large', 3, 0.15),
                ('Corporate', 4, 0.03),
                ('Global', 5, 0.02)
            ]
            sizes, indices, size_weights = zip(*size_options)
            size_index = random.choices(range(len(sizes)), weights=size_weights)[0]
            size, size_index = sizes[size_index], indices[size_index]
            
            prefix = random.choice(PREFIXES["Enterprise"])
            
            # Varied naming patterns
            name_pattern = random.randint(0, 2)
            if name_pattern == 0:
                name = f"{prefix} {size} Plan"
            elif name_pattern == 1:
                name = f"{size} {prefix} Solution"
            else:
                name = f"{prefix} {random.choice(['Professional', 'Complete', 'Connected', 'Premium'])} {size}"
                
            description = f"Enterprise connectivity solution for {size.lower()} businesses"
            
            # Pricing correlated with size
            base_fee = 80 + (size_index * 40)
            fee = round(base_fee * pricing_variation, 2)
            
            # Enterprise features correlated with size
            if size_index <= 1:  # Starter, Small
                data_limit_gb = random.choices([500, 750], weights=[0.6, 0.4])[0]
                voice_limit_minutes = random.choices([3000, 5000], weights=[0.7, 0.3])[0]
                sms_limit = random.choices([3000, 5000], weights=[0.7, 0.3])[0]
            elif size_index <= 3:  # Medium, Large
                data_limit_gb = random.choices([1000, 1500, None], weights=[0.4, 0.4, 0.2])[0]
                voice_limit_minutes = random.choices([5000, 10000, None], weights=[0.3, 0.4, 0.3])[0]
                sms_limit = random.choices([5000, 10000, None], weights=[0.3, 0.4, 0.3])[0]
            else:  # Corporate, Global
                data_limit_gb = random.choices([1500, 2000, None], weights=[0.2, 0.3, 0.5])[0]
                voice_limit_minutes = None  # Always unlimited
                sms_limit = None  # Always unlimited
            
            # Roaming probability increases with size
            roaming_probability = 0.3 + (size_index * 0.14)
            international_roaming = random.random() < roaming_probability
            
            if international_roaming:
                all_countries = list(COUNTRIES.keys())
                num_countries = min(len(all_countries), 1 + size_index)
                countries_sample = random.sample(all_countries, num_countries)
                roaming_countries = "{" + ",".join(country for country in countries_sample) + "}"
                roaming_data_gb = round(random.uniform(2.0, 10.0) * (1 + size_index * 0.4), 2)
                roaming_voice_minutes = random.randint(100, 500) * (1 + size_index)
            
        sf_record = f"PLN{random.randint(10000000, 99999999)}"
        
        plans.append({
            "plan_id": i,
            "plan_name": name,
            "description": description,
            "type": plan_type,
            "monthly_fee": fee,
            "sf_record": sf_record,
            "data_limit_gb": data_limit_gb,
            "voice_limit_minutes": voice_limit_minutes,
            "sms_limit": sms_limit,
            "international_roaming": international_roaming,
            "roaming_countries": roaming_countries,
            "roaming_data_gb": roaming_data_gb,
            "roaming_voice_minutes": roaming_voice_minutes
        })
    return plans

def generate_devices(num_devices: int) -> List[Dict]:
    """Generate device data with realistic market shares."""
    devices = []
    
    # Market share distribution - not uniformly random
    brand_shares = {
        "Apple": 0.35,     # 35% market share
        "Samsung": 0.3,    # 30% market share
        "Google": 0.15,    # 15% market share
        "Xiaomi": 0.1,     # 10% market share
        "OnePlus": 0.07,   # 7% market share
        "Huawei": 0.03     # 3% market share
    }
    
    # Ensure we have at least one iPhone for Alexis
    iphone_model = random.choice(DEVICE_MODELS["Apple"])
    devices.append({
        "device_id": 1,
        "created_at": fake.date_time_between(start_date="-3y", end_date="-1y").isoformat(),
        "updated_at": fake.date_time_between(start_date="-1y", end_date="now").isoformat(),
        "brand": "Apple",
        "model": iphone_model,
        "image": f"apple_{iphone_model.lower().replace(' ', '_')}.jpg",
        "sf_record": f"DEV{random.randint(10000000, 99999999)}"
    })
    
    # Model popularity within brands
    model_popularity = {}
    for brand in DEVICE_BRANDS:
        # Newer models are more popular
        models = DEVICE_MODELS[brand]
        weights = [0.1] * len(models)  # Base weights
        
        # Increase weights for newer models (assuming models are listed newest first)
        for i in range(min(3, len(models))):
            weights[i] += 0.2 * (3 - i)  # Newest model gets highest boost
            
        # Normalize weights
        total = sum(weights)
        weights = [w/total for w in weights]
        
        model_popularity[brand] = {
            "models": models,
            "weights": weights
        }
    
    for i in range(2, num_devices + 1):
        # Select brand based on market share
        brand = random.choices(
            list(brand_shares.keys()),
            weights=list(brand_shares.values())
        )[0]
        
        # Select model based on popularity within brand
        model_data = model_popularity[brand]
        model = random.choices(model_data["models"], weights=model_data["weights"])[0]
        
        image = f"{brand.lower()}_{model.lower().replace(' ', '_')}.jpg"
        sf_record = f"DEV{random.randint(10000000, 99999999)}"
        
        # Age of device record correlated with model (newer models have newer records)
        model_index = DEVICE_MODELS[brand].index(model)
        model_age_ratio = model_index / max(1, len(DEVICE_MODELS[brand]) - 1)
        
        if model_age_ratio < 0.3:  # Newest models
            created_at = fake.date_time_between(start_date="-1y", end_date="-3m").isoformat()
        elif model_age_ratio < 0.7:  # Mid-age models
            created_at = fake.date_time_between(start_date="-2y", end_date="-6m").isoformat()
        else:  # Oldest models
            created_at = fake.date_time_between(start_date="-3y", end_date="-1y").isoformat()
            
        updated_at = fake.date_time_between(
            start_date=datetime.datetime.fromisoformat(created_at), 
            end_date="now"
        ).isoformat()
        
        devices.append({
            "device_id": i,
            "created_at": created_at,
            "updated_at": updated_at,
            "brand": brand,
            "model": model,
            "image": image,
            "sf_record": sf_record
        })
    return devices

def generate_network_nodes(num_nodes: int) -> List[Dict]:
    """Generate network infrastructure nodes with realistic geographic patterns."""
    nodes = []
    
    for i in range(1, num_nodes + 1):
        # Decide if this node is in a hotspot
        is_in_hotspot = random.random() < 0.7  # 70% of nodes in concentrated areas
        
        if is_in_hotspot:
            # Select a hotspot
            hotspot = random.choice(NETWORK_HOTSPOTS)
            
            # Generate coordinates near hotspot
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(0, hotspot["radius"])
            
            # Simple approximation for small distances
            latitude = hotspot["lat"] + distance * math.cos(angle) * 0.01
            longitude = hotspot["lon"] + distance * math.sin(angle) * 0.015
            
            # Node quality based on hotspot quality
            quality = hotspot["quality"]
        else:
            # Random coordinates within US/Canada
            latitude = random.uniform(25.0, 49.0)
            longitude = random.uniform(-125.0, -70.0)
            quality = random.choices(
                ["excellent", "good", "moderate", "poor"],
                weights=[0.1, 0.2, 0.4, 0.3]
            )[0]
        
        # Node capacity based on quality
        if quality == "excellent":
            capacity = random.randint(8000, 10000)
            status_weights = {"Active": 0.95, "Maintenance": 0.04, "Upgrading": 0.01, "Offline": 0.0}
        elif quality == "good":
            capacity = random.randint(5000, 8000)
            status_weights = {"Active": 0.9, "Maintenance": 0.07, "Upgrading": 0.02, "Offline": 0.01}
        elif quality == "moderate":
            capacity = random.randint(3000, 5000)
            status_weights = {"Active": 0.8, "Maintenance": 0.1, "Upgrading": 0.05, "Offline": 0.05}
        else:  # poor
            capacity = random.randint(1000, 3000)
            status_weights = {"Active": 0.6, "Maintenance": 0.2, "Upgrading": 0.1, "Offline": 0.1}
            
        status = random.choices(
            list(status_weights.keys()),
            weights=list(status_weights.values())
        )[0]
        
        nodes.append({
            "node_id": i,
            "node_name": f"NODE-{fake.word().upper()}-{random.randint(100, 999)}",
            "latitude": latitude,
            "longitude": longitude,
            "capacity": capacity,
            "status": status,
            "quality": quality
        })
    return nodes

def generate_customer_plans(customers: List[Dict], plans: List[Dict]) -> List[Dict]:
    """Generate customer plan associations with realistic patterns."""
    customer_plans = []
    customer_plan_id = 1
    
    # Group plans by type
    plan_by_type = {}
    for plan_type in PLAN_TYPES:
        plan_by_type[plan_type] = [p for p in plans if p["type"] == plan_type]
    
    # Plan type preferences by segment
    segment_preferences = {
        "Premium": {
            "Mobile": 0.5,     # 50% chance of mobile plan
            "Internet": 0.2,   # 20% chance of internet plan
            "Bundle": 0.27,    # 27% chance of bundle
            "IoT": 0.02,       # 2% chance of IoT
            "Enterprise": 0.01 # 1% chance of enterprise
        },
        "Standard": {
            "Mobile": 0.6,
            "Internet": 0.25,
            "Bundle": 0.13,
            "IoT": 0.01,
            "Enterprise": 0.01
        },
        "Budget": {
            "Mobile": 0.7,
            "Internet": 0.28,
            "Bundle": 0.01,
            "IoT": 0.01,
            "Enterprise": 0.0
        },
        "Business": {
            "Mobile": 0.35,
            "Internet": 0.15,
            "Bundle": 0.2,
            "IoT": 0.1,
            "Enterprise": 0.2
        },
        "Family": {
            "Mobile": 0.3,
            "Internet": 0.2,
            "Bundle": 0.45,
            "IoT": 0.05,
            "Enterprise": 0.0
        }
    }
    
    # Number of plans by segment
    segment_plan_counts = {
        "Premium": {1: 0.3, 2: 0.5, 3: 0.2},
        "Standard": {1: 0.5, 2: 0.4, 3: 0.1},
        "Budget": {1: 0.8, 2: 0.18, 3: 0.02},
        "Business": {1: 0.2, 2: 0.6, 3: 0.2},
        "Family": {1: 0.1, 2: 0.5, 3: 0.4}
    }
    
    for customer in customers:
        customer_id = customer["customer_id"]
        segment = customer["segment"]
        
        # Special case for Alexis Smith (customer ID 7)
        if customer_id == 7:
            # Find a good mobile plan for Alexis
            premium_mobile_plans = [p for p in plans if p["type"] == "Mobile" and 
                                    (p["data_limit_gb"] is None or p["data_limit_gb"] >= 20)]
            
            if premium_mobile_plans:
                selected_plan = random.choice(premium_mobile_plans)
                start_date = fake.date_time_between(start_date="-1y", end_date="-3m")
                
                # Get data allocation based on the plan
                data_allocation_gb = selected_plan.get("data_limit_gb", 0)
                if data_allocation_gb is None:  # Unlimited plan
                    data_allocation_gb = 1000  # Represent unlimited with a large number
                
                # Heavy user, uses most of allocation
                data_used_gb = round(random.uniform(0.7 * data_allocation_gb, 0.95 * data_allocation_gb), 2)
                
                # Some rollover data
                rollover_data_gb = round(random.uniform(1, 3), 2)
                
                customer_plans.append({
                    "customer_plan_id": customer_plan_id,
                    "customer_id": customer_id,
                    "plan_id": selected_plan["plan_id"],
                    "start_date": start_date.date().isoformat(),
                    "end_date": None,
                    "cell_number": generate_cell_number(),
                    "status": "active",
                    "data_allocation_gb": data_allocation_gb,
                    "data_used_gb": data_used_gb,
                    "rollover_data_gb": rollover_data_gb
                })
                customer_plan_id += 1
        else:
            # Determine number of plans based on segment
            plan_count_weights = segment_plan_counts[segment]
            num_plans = random.choices(
                list(plan_count_weights.keys()),
                weights=list(plan_count_weights.values())
            )[0]
            
            # Select plan types based on segment preferences
            selected_plan_types = []
            for _ in range(num_plans):
                # Get preferences for this segment
                prefs = segment_preferences[segment]
                
                # Select plan type
                plan_type = random.choices(
                    list(prefs.keys()),
                    weights=list(prefs.values())
                )[0]
                
                if plan_type not in selected_plan_types:  # Avoid duplicates
                    selected_plan_types.append(plan_type)
            
            # Add plans
            for plan_type in selected_plan_types:
                available_plans = plan_by_type[plan_type]
                if not available_plans:
                    continue
                    
                # Select appropriate plan based on segment
                if segment == "Premium":
                    # Premium customers prefer high-end plans
                    if plan_type == "Mobile":
                        # Filter for unlimited or high-data plans
                        premium_options = [p for p in available_plans if p["data_limit_gb"] is None or 
                                           p["data_limit_gb"] >= 20]
                        if premium_options:
                            available_plans = premium_options
                    elif plan_type == "Internet":
                        # Filter for high-speed plans
                        premium_options = [p for p in available_plans if "1000" in p["plan_name"] or 
                                          "500" in p["plan_name"]]
                        if premium_options:
                            available_plans = premium_options
                elif segment == "Budget":
                    # Budget customers prefer lower-cost plans
                    if plan_type == "Mobile":
                        # Filter for basic plans
                        budget_options = [p for p in available_plans if p["data_limit_gb"] is not None and 
                                          p["data_limit_gb"] <= 10]
                        if budget_options:
                            available_plans = budget_options
                
                # Select from filtered options
                plan = random.choice(available_plans)
                
                # Plan start date - older customers likely have older plans
                if customer_id < len(customers) * 0.3:  # Oldest 30% of customers
                    start_date = fake.date_time_between(start_date="-3y", end_date="-1y")
                elif customer_id < len(customers) * 0.7:  # Middle 40%
                    start_date = fake.date_time_between(start_date="-2y", end_date="-6m")
                else:  # Newest 30%
                    start_date = fake.date_time_between(start_date="-1y", end_date="-1m")
                
                # Determine if plan is active
                # Newer plans more likely to be active
                days_since_start = (datetime.datetime.now() - start_date).days
                if days_since_start < 180:  # Less than 6 months
                    active_probability = 0.95
                elif days_since_start < 365:  # 6-12 months
                    active_probability = 0.9
                elif days_since_start < 730:  # 1-2 years
                    active_probability = 0.85
                else:  # > 2 years
                    active_probability = 0.75
                    
                is_active = random.random() < active_probability
                
                if is_active:
                    end_date = None
                    status = random.choices(
                        ["active", "activating"],
                        weights=[0.98, 0.02]
                    )[0]
                else:
                    # End date typically within last year
                    end_date = fake.date_time_between(
                        start_date=max(start_date, datetime.datetime.now() - datetime.timedelta(days=365)),
                        end_date="now"
                    )
                    status = "inactive"
                
                # Get data allocation based on the plan
                data_allocation_gb = plan.get("data_limit_gb", 0)
                if data_allocation_gb is None:  # Unlimited plan
                    data_allocation_gb = 1000  # Represent unlimited with a large number
                
                # Generate realistic data usage based on segment
                if status == "active":
                    if segment == "Premium":
                        # Premium users use more data
                        usage_min = 0.5
                        usage_max = 0.9
                    elif segment == "Business":
                        # Business users are more consistent
                        usage_min = 0.4
                        usage_max = 0.7
                    elif segment == "Budget":
                        # Budget users worry about going over
                        usage_min = 0.3
                        usage_max = 0.6
                    else:  # Standard, Family
                        usage_min = 0.3
                        usage_max = 0.8
                        
                    data_used_gb = round(random.uniform(
                        usage_min * data_allocation_gb,
                        usage_max * data_allocation_gb
                    ), 2)
                    
                    # Rollover data based on segment
                    if segment in ["Premium", "Business"]:
                        rollover_data_gb = round(random.uniform(1, 5), 2)
                    else:
                        rollover_data_gb = round(random.uniform(0, 3), 2)
                else:
                    # Inactive plans have no current usage
                    data_used_gb = 0
                    rollover_data_gb = 0
                
                customer_plans.append({
                    "customer_plan_id": customer_plan_id,
                    "customer_id": customer_id,
                    "plan_id": plan["plan_id"],
                    "start_date": start_date.date().isoformat(),
                    "end_date": end_date.date().isoformat() if end_date else None,
                    "cell_number": generate_cell_number(),
                    "status": status,
                    "data_allocation_gb": data_allocation_gb,
                    "data_used_gb": data_used_gb,
                    "rollover_data_gb": rollover_data_gb
                })
                customer_plan_id += 1
    
    return customer_plans

def generate_customer_plan_devices(customer_plans: List[Dict], devices: List[Dict], customers: List[Dict]) -> List[Dict]:
    """Generate associations between customer plans and devices with segment correlations."""
    customer_plan_devices = []
    
    # Create device lookup by brand
    devices_by_brand = {}
    for device in devices:
        brand = device["brand"]
        if brand not in devices_by_brand:
            devices_by_brand[brand] = []
        devices_by_brand[brand].append(device)
    
    # Create customer lookup
    customer_lookup = {c["customer_id"]: c for c in customers}
    
    # Create plan lookup to get plan types
    plan_types = {}
    for plan in customer_plans:
        # Get plan_id from the customer plan
        plan_id = plan.get("plan_id")
        if plan_id not in plan_types:
            # We don't have the actual plan type, so we'll use a default value
            plan_types[plan_id] = "Unknown"
    
    # Brand preferences by segment
    segment_brand_preferences = {
        "Premium": {
            "Apple": 0.6,      # Premium users prefer Apple
            "Samsung": 0.25,
            "Google": 0.1,
            "OnePlus": 0.03,
            "Xiaomi": 0.01,
            "Huawei": 0.01
        },
        "Standard": {
            "Apple": 0.35,
            "Samsung": 0.35,
            "Google": 0.15,
            "OnePlus": 0.05,
            "Xiaomi": 0.05,
            "Huawei": 0.05
        },
        "Budget": {
            "Apple": 0.15,     # Budget users less likely to have Apple
            "Samsung": 0.3,
            "Google": 0.2,
            "OnePlus": 0.05,
            "Xiaomi": 0.2,
            "Huawei": 0.1
        },
        "Business": {
            "Apple": 0.5,
            "Samsung": 0.3,
            "Google": 0.15,
            "OnePlus": 0.03,
            "Xiaomi": 0.01,
            "Huawei": 0.01
        },
        "Family": {
            "Apple": 0.3,
            "Samsung": 0.4,
            "Google": 0.15,
            "OnePlus": 0.05,
            "Xiaomi": 0.05,
            "Huawei": 0.05
        }
    }
    
    # Find Alexis's plan
    alexis_plans = [p for p in customer_plans if p["customer_id"] == 7]
    
    for plan in customer_plans:
        customer_id = plan["customer_id"]
        
        # Special case for Alexis Smith
        if customer_id == 7:
            # Ensure Alexis has an iPhone
            iphones = [d for d in devices if d["brand"] == "Apple" and "iPhone" in d["model"]]
            if iphones:
                iphone = random.choice(iphones)
            else:
                iphone = devices[0]
            
            # Generate SIM ICCID (Integrated Circuit Card Identifier)
            sim_iccid = f"89{random.randint(10000000000000000000, 99999999999999999999)}"
            
            # Generate device IMEI (International Mobile Equipment Identity)
            device_imei = f"{random.randint(100000000000000, 999999999999999)}"
            
            customer_plan_devices.append({
                "customer_plan_id": plan["customer_plan_id"],
                "device_id": iphone["device_id"],
                "sim_iccid": sim_iccid,
                "device_imei": device_imei
            })
        else:
            # For all other customers, we'll assign devices based on certain criteria
            
            # Criteria #1: Check if we should assign a device (70% chance)
            if random.random() < 0.7:
                # Select appropriate segment
                if customer_id in customer_lookup:
                    segment = customer_lookup[customer_id]["segment"]
                    # Default to Standard if segment not in our preferences
                    if segment not in segment_brand_preferences:
                        segment = "Standard"
                    preferences = segment_brand_preferences[segment]
                    
                    # Select brand based on segment preferences
                    brand = random.choices(
                        list(preferences.keys()),
                        weights=list(preferences.values())
                    )[0]
                    
                    # Get available devices for this brand
                    brand_devices = devices_by_brand.get(brand, [])
                    if not brand_devices:
                        # Fallback to any device
                        device = random.choice(devices)
                    else:
                        device = random.choice(brand_devices)
                    
                    # Generate SIM ICCID
                    sim_iccid = f"89{random.randint(10000000000000000000, 99999999999999999999)}"
                    
                    # Generate device IMEI
                    device_imei = f"{random.randint(100000000000000, 999999999999999)}"
                    
                    customer_plan_devices.append({
                        "customer_plan_id": plan["customer_plan_id"],
                        "device_id": device["device_id"],
                        "sim_iccid": sim_iccid,
                        "device_imei": device_imei
                    })
    
    return customer_plan_devices
def generate_customer_network(customers: List[Dict], nodes: List[Dict]) -> List[Dict]:
    """Generate associations between customers and network nodes with geographic correlation."""
    customer_network = []
    
    # Create lookup of node coordinates
    node_locations = {node["node_id"]: (node["latitude"], node["longitude"]) for node in nodes}
    
    for customer in customers:
        customer_id = customer["customer_id"]
        
        # Generate customer's approximate location
        # Use country to determine rough location
        country = customer["country"]
        if country == "United States":
            base_lat = random.uniform(30.0, 48.0)
            base_lon = random.uniform(-122.0, -75.0)
        elif country == "Canada":
            base_lat = random.uniform(43.0, 53.0)
            base_lon = random.uniform(-123.0, -79.0)
        elif country == "United Kingdom":
            base_lat = random.uniform(50.0, 58.0)
            base_lon = random.uniform(-4.0, 1.0)
        else:  # Australia
            base_lat = random.uniform(-37.0, -25.0)
            base_lon = random.uniform(115.0, 153.0)
            
        # Add more precision using state
        # (This is a simplification - in a real system you'd use geocoding)
        
        # Find nodes closest to this customer
        node_distances = []
        for node_id, (node_lat, node_lon) in node_locations.items():
            # Simple Euclidean distance (not accurate for long distances, but serves our purpose)
            distance = math.sqrt(
                (base_lat - node_lat)**2 + 
                (base_lon - node_lon)**2
            )
            node_distances.append((node_id, distance))
        
        # Sort by distance
        node_distances.sort(key=lambda x: x[1])
        
        # Take closest 1-3 nodes
        num_nodes = random.choices([1, 2, 3], weights=[0.6, 0.3, 0.1])[0]
        closest_nodes = node_distances[:num_nodes]
        
        for node_id, _ in closest_nodes:
            customer_network.append({
                "customer_id": customer_id,
                "node_id": node_id
            })
    
    return customer_network

def generate_billing(customers: List[Dict], customer_plans: List[Dict], plans: List[Dict]) -> List[Dict]:
    """Generate billing records with realistic payment patterns."""
    billing_records = []
    billing_id = 1
    
    # Create a lookup for plans
    plan_lookup = {plan["plan_id"]: plan for plan in plans}
    
    # Group plans by customer
    plans_by_customer = {}
    for plan in customer_plans:
        customer_id = plan["customer_id"]
        if customer_id not in plans_by_customer:
            plans_by_customer[customer_id] = []
        plans_by_customer[customer_id].append(plan)
    
    # Payment behavior by segment
    segment_payment_behavior = {
        "Premium": {
            "current": {"Paid": 0.4, "Pending": 0.6, "Overdue": 0.0, "Failed": 0.0},
            "recent": {"Paid": 0.9, "Pending": 0.08, "Overdue": 0.01, "Failed": 0.01},
            "old": {"Paid": 0.97, "Pending": 0.0, "Overdue": 0.02, "Failed": 0.01}
        },
        "Standard": {
            "current": {"Paid": 0.3, "Pending": 0.65, "Overdue": 0.05, "Failed": 0.0},
            "recent": {"Paid": 0.85, "Pending": 0.1, "Overdue": 0.04, "Failed": 0.01},
            "old": {"Paid": 0.94, "Pending": 0.0, "Overdue": 0.05, "Failed": 0.01}
        },
        "Budget": {
            "current": {"Paid": 0.2, "Pending": 0.65, "Overdue": 0.1, "Failed": 0.05},
            "recent": {"Paid": 0.75, "Pending": 0.1, "Overdue": 0.1, "Failed": 0.05},
            "old": {"Paid": 0.85, "Pending": 0.0, "Overdue": 0.1, "Failed": 0.05}
        },
        "Business": {
            "current": {"Paid": 0.45, "Pending": 0.55, "Overdue": 0.0, "Failed": 0.0},
            "recent": {"Paid": 0.95, "Pending": 0.05, "Overdue": 0.0, "Failed": 0.0},
            "old": {"Paid": 0.99, "Pending": 0.0, "Overdue": 0.01, "Failed": 0.0}
        },
        "Family": {
            "current": {"Paid": 0.25, "Pending": 0.65, "Overdue": 0.1, "Failed": 0.0},
            "recent": {"Paid": 0.8, "Pending": 0.1, "Overdue": 0.08, "Failed": 0.02},
            "old": {"Paid": 0.9, "Pending": 0.0, "Overdue": 0.08, "Failed": 0.02}
        }
    }
    
    for customer in customers:
        customer_id = customer["customer_id"]
        segment = customer["segment"]
        
        # Get payment behavior for this segment
        payment_behavior = segment_payment_behavior[segment]
        
        # Get plans for this customer
        customer_plans_list = plans_by_customer.get(customer_id, [])
        
        # Generate monthly bills for the past year
        for month_offset in range(12):  # 12 months
            bill_date = (datetime.datetime.now() - datetime.timedelta(days=30 * month_offset)).date()
            
            # Calculate total based on active plans for that month
            total_amount = 0
            for customer_plan in customer_plans_list:
                plan_start = datetime.date.fromisoformat(customer_plan["start_date"])
                plan_end = datetime.date.fromisoformat(customer_plan["end_date"]) if customer_plan["end_date"] else None
                
                if plan_start <= bill_date and (plan_end is None or plan_end >= bill_date):
                    # Get the plan details to find the fee
                    plan_id = customer_plan["plan_id"]
                    if plan_id in plan_lookup:
                        total_amount += float(plan_lookup[plan_id]["monthly_fee"])
            
            # Add some random charges
            total_amount += random.uniform(0, 20)
            
            # Determine payment status based on segment and bill age
            if month_offset == 0:  # Current month
                status_weights = payment_behavior["current"]
            elif month_offset <= 2:  # Recent months
                status_weights = payment_behavior["recent"]
            else:  # Older months
                status_weights = payment_behavior["old"]
                
            payment_status = random.choices(
                list(status_weights.keys()),
                weights=list(status_weights.values())
            )[0]
            
            billing_records.append({
                "billing_id": billing_id,
                "customer_id": customer_id,
                "billing_date": bill_date.isoformat(),
                "total_amount": round(total_amount, 2),
                "payment_status": payment_status
            })
            billing_id += 1
    
    return billing_records

def generate_credit_cards(customers: List[Dict]) -> List[Dict]:
    """Generate realistic but fictitious credit card information with segment correlations."""
    credit_cards = []
    credit_card_id = 1
    
    # Common credit card prefixes by provider
    card_prefixes = {
        "Visa": ["4"],
        "Mastercard": ["51", "52", "53", "54", "55"],
        "Amex": ["34", "37"],
        "Discover": ["6011", "644", "645", "646", "647", "648", "649", "65"]
    }
    
    # Card preferences by segment
    segment_card_preferences = {
        "Premium": {
            "Visa": 0.3,
            "Mastercard": 0.2,
            "Amex": 0.45,  # Premium users prefer Amex
            "Discover": 0.05
        },
        "Standard": {
            "Visa": 0.4,
            "Mastercard": 0.35,
            "Amex": 0.15,
            "Discover": 0.1
        },
        "Budget": {
            "Visa": 0.5,
            "Mastercard": 0.4,
            "Amex": 0.05,  # Budget users less likely to have Amex
            "Discover": 0.05
        },
        "Business": {
            "Visa": 0.25,
            "Mastercard": 0.25,
            "Amex": 0.45,  # Business users often have Amex
            "Discover": 0.05
        },
        "Family": {
            "Visa": 0.45,
            "Mastercard": 0.35,
            "Amex": 0.1,
            "Discover": 0.1
        }
    }
    
    # Number of cards by segment
    segment_card_counts = {
        "Premium": {1: 0.7, 2: 0.3},
        "Standard": {1: 0.85, 2: 0.15},
        "Budget": {1: 0.95, 2: 0.05},
        "Business": {1: 0.6, 2: 0.4},
        "Family": {1: 0.8, 2: 0.2}
    }
    
    for customer in customers:
        segment = customer["segment"]
        
        # Determine number of cards
        card_count_weights = segment_card_counts[segment]
        num_cards = random.choices(
            list(card_count_weights.keys()),
            weights=list(card_count_weights.values())
        )[0]
        
        # Card preferences for this segment
        card_preferences = segment_card_preferences[segment]
        
        for _ in range(num_cards):
            # Choose card type based on segment preferences
            card_type = random.choices(
                list(card_preferences.keys()),
                weights=list(card_preferences.values())
            )[0]
            prefix = random.choice(card_prefixes[card_type])
            
            # Generate card number based on type
            if card_type == "Amex":
                # Amex: 15 digits
                remaining_digits = 15 - len(prefix)
                suffix = ''.join([str(random.randint(0, 9)) for _ in range(remaining_digits)])
                number = prefix + suffix
                # Format with proper spacing (XXXX XXXXXX XXXXX)
                formatted_number = f"{number[0:4]} {number[4:10]} {number[10:15]}"
            else:
                # Other cards: 16 digits
                remaining_digits = 16 - len(prefix)
                suffix = ''.join([str(random.randint(0, 9)) for _ in range(remaining_digits)])
                number = prefix + suffix
                # Format with proper spacing (XXXX XXXX XXXX XXXX)
                formatted_number = f"{number[0:4]} {number[4:8]} {number[8:12]} {number[12:16]}"
            
            # Generate a future expiry date
            expiry_year = datetime.datetime.now().year + random.randint(1, 5)
            expiry_month = random.randint(1, 12)
            expiry_date = datetime.date(expiry_year, expiry_month, 1)
            
            # Format expiry as MM/YY
            expiry_formatted = f"{expiry_month:02d}/{str(expiry_year)[2:]}"
            
            # Card creation date - correlate with customer creation date
            if customer["customer_id"] < len(customers) * 0.3:  # Oldest 30% of customers
                created_at = fake.date_time_between(start_date="-3y", end_date="-2y").isoformat()
            elif customer["customer_id"] < len(customers) * 0.7:  # Middle 40%
                created_at = fake.date_time_between(start_date="-2y", end_date="-1y").isoformat()
            else:  # Newest 30%
                created_at = fake.date_time_between(start_date="-1y", end_date="-3m").isoformat()
                
            # Last update typically more recent than creation
            updated_at = fake.date_time_between(
                start_date=datetime.datetime.fromisoformat(created_at), 
                end_date="now"
            ).isoformat()
            
            credit_cards.append({
                "credit_card_id": credit_card_id,
                "created_at": created_at,
                "updated_at": updated_at,
                "expiry": expiry_date.isoformat(),
                "cvv": random.randint(100, 999),
                "number": formatted_number,
                "customer_id": customer["customer_id"]
            })
            credit_card_id += 1
    
    return credit_cards

def generate_customer_link(customers: List[Dict]) -> List[Dict]:
    """Generate customer link records with UUIDs."""
    customer_links = []
    
    for customer in customers:
        customer_links.append({
            "id": customer["customer_id"],
            "customer_id": customer["customer_id"],
            "customer_guid": str(uuid.uuid4())
        })
    
    return customer_links

def generate_deals(num_deals: int) -> List[Dict]:
    """Generate promotional deals with segment targeting."""
    deals = []
    
    # Deal distribution by segment
    segment_deal_distribution = {
        "Premium": 0.25,   # 25% of deals target Premium
        "Standard": 0.3,   # 30% of deals target Standard
        "Budget": 0.2,     # 20% of deals target Budget
        "Business": 0.15,  # 15% of deals target Business
        "Family": 0.1      # 10% of deals target Family
    }
    
    # Seasonal patterns
    current_month = datetime.datetime.now().month
    seasons = {
        "Winter": (current_month in [12, 1, 2]),
        "Spring": (current_month in [3, 4, 5]),
        "Summer": (current_month in [6, 7, 8]),
        "Fall": (current_month in [9, 10, 11])
    }
    current_season = next(season for season, is_current in seasons.items() if is_current)
    
    # Seasonal deal names
    seasonal_names = {
        "Winter": ["Winter Special", "Holiday Discount", "New Year Offer", "Frost Savings"],
        "Spring": ["Spring Deal", "Renewal Offer", "Bloom Special", "Fresh Start Discount"],
        "Summer": ["Summer Savings", "Vacation Special", "Hot Deal", "Sunshine Offer"],
        "Fall": ["Fall Promotion", "Back to School Special", "Autumn Deal", "Harvest Savings"]
    }
    
    for i in range(1, num_deals + 1):
        # Select target segment based on distribution
        segment = random.choices(
            list(segment_deal_distribution.keys()),
            weights=list(segment_deal_distribution.values())
        )[0]
        
        # Set min/max spend based on segment
        if segment == "Premium":
            min_spend = random.randint(60, 100)
            max_spend = min_spend + random.randint(100, 200)
        elif segment == "Budget":
            min_spend = random.randint(20, 40)
            max_spend = min_spend + random.randint(30, 70)
        elif segment == "Business":
            min_spend = random.randint(80, 120)
            max_spend = min_spend + random.randint(100, 300)
        else:  # Standard, Family
            min_spend = random.randint(40, 70)
            max_spend = min_spend + random.randint(50, 120)
        
        # Set deal dates - include more current deals
        if random.random() < 0.7:  # 70% current or future deals
            start_date = fake.date_time_between(start_date="-1m", end_date="+1m")
            end_date = fake.date_time_between(start_date=start_date + datetime.timedelta(days=30), 
                                             end_date=start_date + datetime.timedelta(days=90))
        else:  # 30% past deals
            start_date = fake.date_time_between(start_date="-1y", end_date="-1m")
            end_date = fake.date_time_between(start_date=start_date + datetime.timedelta(days=30),
                                             end_date=min(datetime.datetime.now(), 
                                                         start_date + datetime.timedelta(days=90)))
        
        # Deal name with seasonal component
        if random.random() < 0.3:  # 30% chance of seasonal name
            name = random.choice(seasonal_names[current_season])
        else:
            name = f"{segment} {random.choice(['Special', 'Discount', 'Promotion', 'Offer'])}"
            
        deals.append({
            "deal_id": i,
            "deal_name": name,
            "description": fake.paragraph(nb_sentences=3),
            "customer_segment": segment,
            "min_monthly_spend": min_spend,
            "max_monthly_spend": max_spend,
            "start_date": start_date.date().isoformat(),
            "end_date": end_date.date().isoformat(),
            "additional_benefits": fake.paragraph(nb_sentences=2),
            "terms_conditions": fake.paragraph(nb_sentences=5)
        })
    
    return deals

def generate_calls(customer_plans: List[Dict], nodes: List[Dict], customers: List[Dict], customer_plan_devices: List[Dict]) -> List[Dict]:
    """Generate call records with realistic temporal and geographic patterns."""
    calls = []
    call_id = 1
    
    # Create customer lookup for segment-based patterns
    customer_lookup = {c["customer_id"]: c for c in customers}
    
    # Create lookup for devices by customer_plan_id
    plan_device_lookup = {}
    for cpd in customer_plan_devices:
        plan_device_lookup[cpd["customer_plan_id"]] = cpd["device_id"]
    
    # Time-of-day patterns - calls are more common during certain hours
    hour_weights = {h: 1.0 for h in range(24)}
    # Increase likelihood during business hours
    for h in range(8, 18):
        hour_weights[h] = 3.0
    # Higher during lunch
    hour_weights[12] = 4.0
    hour_weights[13] = 4.0
    # Peak hours
    hour_weights[9] = 5.0
    hour_weights[16] = 5.0
    # Evening
    for h in range(18, 22):
        hour_weights[h] = 2.5
    # Late night
    for h in range(22, 24):
        hour_weights[h] = 0.5
    for h in range(0, 6):
        hour_weights[h] = 0.2
        
    # Day of week weights - fewer calls on weekends
    day_weights = {d: 1.0 for d in range(7)}
    day_weights[5] = 0.6  # Saturday
    day_weights[6] = 0.4  # Sunday
    
    # Create node lookup
    node_lookup = {n["node_id"]: n for n in nodes}
    
    for plan in customer_plans:
        # Only consider active plans
        if plan.get("status") != "active":
            continue
            
        customer_id = plan["customer_id"]
        customer_plan_id = plan["customer_plan_id"]
        
        # Get device ID for this plan
        device_id = plan_device_lookup.get(customer_plan_id)
        
        # Skip if no device associated with plan
        if not device_id:
            continue
        
        # Get customer segment for call patterns
        segment = customer_lookup.get(customer_id, {}).get("segment", "Standard")
        
        # Get customer node connection
        customer_nodes = [n for n in nodes if random.random() < 0.5]  # Simplified
        if not customer_nodes:
            customer_nodes = [random.choice(nodes)]
            
        # Different segments have different call patterns
        if segment == "Premium":
            num_calls = random.randint(15, 30)
            miss_probability = 0.1
            video_probability = 0.15
            conference_probability = 0.1
        elif segment == "Business":
            num_calls = random.randint(20, 40)
            miss_probability = 0.15
            video_probability = 0.2
            conference_probability = 0.15
        elif segment == "Budget":
            num_calls = random.randint(5, 15)
            miss_probability = 0.2
            video_probability = 0.05
            conference_probability = 0.02
        else:  # Standard, Family
            num_calls = random.randint(10, 25)
            miss_probability = 0.15
            video_probability = 0.08
            conference_probability = 0.05
            
        # Generate multiple calls
        for _ in range(num_calls):
            # Generate date with realistic distribution
            base_date = fake.date_time_between(start_date="-3m", end_date="now")
            
            # Adjust hour based on typical call patterns
            hour = random.choices(
                list(hour_weights.keys()),
                weights=list(hour_weights.values())
            )[0]
            
            # Adjust day of week
            day_of_week = base_date.weekday()
            day_adjustment = 0
            if day_weights[day_of_week] < 1.0 and random.random() > day_weights[day_of_week]:
                # Move to a weekday if rejected weekend
                day_adjustment = -day_of_week if day_of_week == 6 else 1  # Sunday → Monday, Saturday → Sunday
                
            # Create timestamp with adjusted hour and day
            timestamp = base_date.replace(hour=hour) + datetime.timedelta(days=day_adjustment)
            
            # Generate call type with segment-specific probabilities
            type_random = random.random()
            if type_random < miss_probability:
                call_type = "Missed"
                duration = 0
            elif type_random < miss_probability + video_probability:
                call_type = "Video"
                duration = random.randint(60, 1800)  # 1-30 minutes
            elif type_random < miss_probability + video_probability + conference_probability:
                call_type = "Conference"
                duration = random.randint(300, 3600)  # 5-60 minutes
            elif type_random < 0.6:
                call_type = "Outgoing"
                duration = random.randint(30, 1200)  # 30s-20m
            else:
                call_type = "Incoming"
                duration = random.randint(30, 1200)  # 30s-20m
                
            # Generate a random receiver number
            receiver_number = generate_phone_number()
            
            # Assign a network node - calls tend to use nearby nodes
            node = random.choice(customer_nodes)
            
            # Call coordinates - near node location
            # Check if node has latitude and longitude attributes
            if hasattr(node, "get") and "latitude" in node and "longitude" in node:
                base_lat = node["latitude"]
                base_lon = node["longitude"]
            else:
                # Default coordinates if node doesn't have them
                base_lat = 40.7128  # New York City latitude
                base_lon = -74.0060  # New York City longitude
            
            # Add small variation
            latitude = base_lat + random.uniform(-0.05, 0.05)
            longitude = base_lon + random.uniform(-0.05, 0.05)
            
            calls.append({
                "CallID": call_id,
                "CustomerID": customer_id,
                "DeviceID": device_id,  # Add the device ID
                "TimeStamp": timestamp.isoformat(),
                "Duration": duration,
                "CallType": call_type,
                "ReceiverNumber": receiver_number,
                "NodeId": node["node_id"] if hasattr(node, "get") and "node_id" in node else 1,
                "latitude": latitude,
                "longitude": longitude
                # Removed the quality field as it's not in the schema
            })
            call_id += 1
    
    return calls

def generate_texts(customer_plans: List[Dict], nodes: List[Dict], customers: List[Dict], customer_plan_devices: List[Dict]) -> List[Dict]:
    """Generate text message records with realistic patterns."""
    texts = []
    text_id = 1
    
    # Create customer lookup for segment-based patterns
    customer_lookup = {c["customer_id"]: c for c in customers}
    
    # Create lookup for devices by customer_plan_id
    plan_device_lookup = {}
    for cpd in customer_plan_devices:
        plan_device_lookup[cpd["customer_plan_id"]] = cpd["device_id"]
    
    # Time-of-day patterns - different from calls
    hour_weights = {h: 1.0 for h in range(24)}
    # Texting happens more throughout the day
    for h in range(9, 22):
        hour_weights[h] = 3.0
    # Peak texting hours
    hour_weights[12] = 3.5  # Lunch
    hour_weights[17] = 4.0  # After work
    hour_weights[20] = 3.5  # Evening
    # Late night
    for h in range(22, 24):
        hour_weights[h] = 1.5
    for h in range(0, 7):
        hour_weights[h] = 0.5
        
    # Day of week weights - more uniform than calls
    day_weights = {d: 1.0 for d in range(7)}
    day_weights[5] = 1.2  # Saturday - more texting
    day_weights[6] = 1.1  # Sunday
    
    # Create node lookup
    node_lookup = {n["node_id"]: n for n in nodes}
    
    for plan in customer_plans:
        if plan["status"] != "active":
            continue
            
        customer_id = plan["customer_id"]
        customer_plan_id = plan["customer_plan_id"]
        
        # Get device ID for this plan
        device_id = plan_device_lookup.get(customer_plan_id)
        
        # Skip if no device associated with plan
        if not device_id:
            continue
        
        # Get customer segment for texting patterns
        customer_data = customer_lookup.get(customer_id, {})
        segment = customer_data.get("segment", "Standard")
        
        # Get customer node connection
        customer_nodes = [n for n in nodes if random.random() < 0.5]  # Simplified
        if not customer_nodes:
            customer_nodes = [random.choice(nodes)]
            
        # Different segments have different texting patterns
        if segment == "Premium":
            num_texts = random.randint(25, 50)
            mms_probability = 0.2
            rcs_probability = 0.1
        elif segment == "Business":
            num_texts = random.randint(15, 35)
            mms_probability = 0.15
            rcs_probability = 0.15
        elif segment == "Budget":
            num_texts = random.randint(10, 30)
            mms_probability = 0.1
            rcs_probability = 0.05
        else:  # Standard, Family
            num_texts = random.randint(20, 40)
            mms_probability = 0.15
            rcs_probability = 0.05
            
        # Age factor - younger customers text more
        dob_str = customer_data.get("dob")
        target_age = 35  # Default if DOB is missing
        
        if dob_str:
            try:
                dob = datetime.date.fromisoformat(dob_str)
                target_age = calculate_age(dob)
            except:
                pass  # Use default if parsing fails
                
        if target_age < 30:
            num_texts = int(num_texts * 1.5)
        elif target_age > 60:
            num_texts = int(num_texts * 0.7)
            
        # Generate multiple texts
        for _ in range(num_texts):
            # Generate date with realistic distribution
            base_date = fake.date_time_between(start_date="-3m", end_date="now")
            
            # Adjust hour based on typical texting patterns
            hour = random.choices(
                list(hour_weights.keys()),
                weights=list(hour_weights.values())
            )[0]
            
            # Create timestamp with adjusted hour
            timestamp = base_date.replace(hour=hour)
            
            # Generate message type with segment-specific probabilities
            type_random = random.random()
            if type_random < mms_probability:
                message_type = "MMS"
            elif type_random < mms_probability + rcs_probability:
                message_type = "RCS"
            else:
                message_type = "SMS"
                
            # Generate a random receiver number
            receiver_number = generate_phone_number()
            
            # Assign a network node - texts tend to use nearby nodes
            node = random.choice(customer_nodes)
            node_quality = node_lookup.get(node["node_id"], {}).get("quality", "moderate")

            # Message coordinates - near node location
            base_lat = node["latitude"]
            base_lon = node["longitude"]
            
            # Add small variation
            latitude = base_lat + random.uniform(-0.05, 0.05)
            longitude = base_lon + random.uniform(-0.05, 0.05)
            
            texts.append({
                "TextID": text_id,
                "CustomerID": customer_id,
                "DeviceID": device_id,  # Add the device ID
                "TimeStamp": timestamp.isoformat(),
                "MessageType": message_type,
                "ReceiverNumber": receiver_number,
                "NodeId": node["node_id"],
                "latitude": latitude,
                "longitude": longitude
                # Removed the quality field as it's not in the schema
            })
            text_id += 1
    
    return texts

def generate_service_interactions(customers: List[Dict]) -> List[Dict]:
    """Generate customer service interaction records with realistic patterns."""
    interactions = []
    interaction_id = 1
    
    # Define categories and probabilities by segment
    category_probabilities = {
        "Premium": {
            "technical": 0.3,
            "billing": 0.1,
            "account": 0.1,
            "plan": 0.2,
            "device": 0.2,
            "coverage": 0.1
        },
        "Standard": {
            "technical": 0.25,
            "billing": 0.2,
            "account": 0.15,
            "plan": 0.15,
            "device": 0.15,
            "coverage": 0.1
        },
        "Budget": {
            "technical": 0.2,
            "billing": 0.35,
            "account": 0.1,
            "plan": 0.1,
            "device": 0.05,
            "coverage": 0.2
        },
        "Business": {
            "technical": 0.25,
            "billing": 0.15,
            "account": 0.1,
            "plan": 0.2,
            "device": 0.1,
            "coverage": 0.2
        },
        "Family": {
            "technical": 0.3,
            "billing": 0.2,
            "account": 0.1,
            "plan": 0.15,
            "device": 0.15,
            "coverage": 0.1
        }
    }
    
    # Channel preferences by segment
    channel_probabilities = {
        "Premium": {
            "phone": 0.6,
            "chat": 0.25,
            "email": 0.1,
            "store": 0.03,
            "social": 0.02
        },
        "Standard": {
            "phone": 0.4,
            "chat": 0.3,
            "email": 0.15,
            "store": 0.1,
            "social": 0.05
        },
        "Budget": {
            "phone": 0.3,
            "chat": 0.2,
            "email": 0.1,
            "store": 0.2,
            "social": 0.2
        },
        "Business": {
            "phone": 0.7,
            "chat": 0.15,
            "email": 0.1,
            "store": 0.03,
            "social": 0.02
        },
        "Family": {
            "phone": 0.35,
            "chat": 0.3,
            "email": 0.1,
            "store": 0.15,
            "social": 0.1
        }
    }
    
    # Resolution time by category and channel
    resolution_time_base = {
        "technical": {
            "phone": 30,
            "chat": 45,
            "email": 120,
            "store": 45,
            "social": 90
        },
        "billing": {
            "phone": 20,
            "chat": 25,
            "email": 60,
            "store": 25,
            "social": 60
        },
        "account": {
            "phone": 15,
            "chat": 20,
            "email": 40,
            "store": 20,
            "social": 45
        },
        "plan": {
            "phone": 25,
            "chat": 35,
            "email": 60,
            "store": 30,
            "social": 60
        },
        "device": {
            "phone": 35,
            "chat": 40,
            "email": 90,
            "store": 60,
            "social": 90
        },
        "coverage": {
            "phone": 15,
            "chat": 20,
            "email": 45,
            "store": 25,
            "social": 45
        }
    }
    
    # Interaction frequency by segment and satisfaction score
    # Customers with lower satisfaction tend to have more service interactions
    interaction_count_by_satisfaction = {
        (1, 3): [3, 8],   # 1-3 rating: 3-8 interactions
        (4, 6): [1, 4],   # 4-6 rating: 1-4 interactions
        (7, 8): [0, 2],   # 7-8 rating: 0-2 interactions
        (9, 10): [0, 1]   # 9-10 rating: 0-1 interactions
    }
    
    for customer in customers:
        customer_id = customer["customer_id"]
        segment = customer["segment"]
        satisfaction = customer.get("satisfaction_score", 7)  # Default to 7 if missing
        
        # Determine number of interactions based on satisfaction
        interaction_range = next(
            (r for sat_range, r in interaction_count_by_satisfaction.items() 
             if sat_range[0] <= satisfaction <= sat_range[1]),
            [0, 1]  # Default to 0-1 if no range matches
        )
        num_interactions = random.randint(interaction_range[0], interaction_range[1])
        
        for _ in range(num_interactions):
            # Select category based on segment preferences
            category_probs = category_probabilities[segment]
            category = random.choices(
                list(category_probs.keys()),
                weights=list(category_probs.values())
            )[0]
            
            # Select channel based on segment preferences
            channel_probs = channel_probabilities[segment]
            channel = random.choices(
                list(channel_probs.keys()),
                weights=list(channel_probs.values())
            )[0]
            
            # Generate interaction date - more recent for lower satisfaction
            if satisfaction <= 5:
                # Lower satisfaction: more recent interactions
                interaction_date = fake.date_time_between(start_date="-3m", end_date="now")
            else:
                # Higher satisfaction: interactions spread throughout the year
                interaction_date = fake.date_time_between(start_date="-1y", end_date="now")
            
            # Determine resolution status - correlated with satisfaction
            if satisfaction >= 8:
                # High satisfaction: mostly resolved
                resolution_probs = {"resolved": 0.85, "pending": 0.1, "escalated": 0.05}
            elif satisfaction >= 5:
                # Medium satisfaction: mixed
                resolution_probs = {"resolved": 0.7, "pending": 0.2, "escalated": 0.1}
            else:
                # Low satisfaction: more escalations
                resolution_probs = {"resolved": 0.5, "pending": 0.3, "escalated": 0.2}
                
            resolution_status = random.choices(
                list(resolution_probs.keys()),
                weights=list(resolution_probs.values())
            )[0]
            
            # Satisfaction score for this interaction - correlated with overall satisfaction
            # but with some randomness
            base_score = min(10, max(1, satisfaction + random.randint(-2, 2)))
            
            # Adjust based on resolution status
            if resolution_status == "resolved":
                interaction_satisfaction = min(10, base_score + random.randint(0, 2))
            elif resolution_status == "pending":
                interaction_satisfaction = max(1, base_score - random.randint(0, 2))
            else:  # escalated
                interaction_satisfaction = max(1, base_score - random.randint(1, 3))
            
            # Calculate resolution time
            base_time = resolution_time_base[category][channel]
            
            if resolution_status == "escalated":
                resolution_time = base_time * random.randint(2, 4)
            elif resolution_status == "pending":
                resolution_time = 0  # Not resolved yet
            else:
                # Add some randomness to base time
                resolution_time = int(base_time * random.uniform(0.8, 1.2))
            
            # Agent ID (1-20)
            agent_id = random.randint(1, 20)
            
            # Generate notes based on category, channel and status
            if category == 'technical':
                if resolution_status == 'resolved':
                    notes = random.choice([
                        "Customer reported connectivity issues. Troubleshooting steps provided and issue resolved.",
                        "Device not connecting to network. Reset network settings which resolved the issue.",
                        "Slow data speeds reported. Identified tower congestion as cause and suggested alternative connection methods."
                    ])
                else:
                    notes = random.choice([
                        "Customer reported connectivity issues. Initial troubleshooting unsuccessful, escalated to technical team.",
                        "Device not connecting to network. Basic troubleshooting attempted, awaiting customer to test additional steps.",
                        "Slow data speeds reported. No immediate resolution, monitoring for network improvements."
                    ])
            elif category == 'billing':
                if resolution_status == 'resolved':
                    notes = random.choice([
                        "Customer disputed recent charges. Reviewed bill with customer and explained charges.",
                        "Question about proration on latest bill. Explained billing cycle and customer understood.",
                        "Customer requested payment extension. Approved for 7 days."
                    ])
                else:
                    notes = random.choice([
                        "Customer disputed recent charges. Escalated to billing department for review.",
                        "Question about unexplained charges. Research required, billing team investigating.",
                        "Customer requested refund for service outage. Awaiting approval from management."
                    ])
            else:
                if resolution_status == 'resolved':
                    notes = f"Customer inquiry about {category}. Provided information and assistance. Issue resolved."
                else:
                    notes = f"Customer inquiry about {category}. Initial assistance provided. Awaiting further information."
            
            interactions.append({
                "interaction_id": interaction_id,
                "customer_id": customer_id,
                "interaction_date": interaction_date.isoformat(),
                "channel": channel,
                "category": category,
                "resolution_status": resolution_status,
                "satisfaction_score": interaction_satisfaction,
                "agent_id": agent_id,
                "resolution_time_minutes": resolution_time,
                "notes": notes
            })
            
            interaction_id += 1
    
    return interactions

def generate_interactions(customers: List[Dict]) -> List[Dict]:
    """Generate general customer interaction records across channels with behavioral patterns."""
    interactions = []
    interaction_id = 1
    
    # Define possible channels and topics with realistic distributions
    channels = {
        'call': 0.35,
        'chat': 0.25,
        'email': 0.2,
        'store': 0.1,
        'social media': 0.05,
        'website': 0.05
    }
    
    topics = {
        'account inquiry': 0.15,
        'technical support': 0.25,
        'billing question': 0.2,
        'upgrade options': 0.1,
        'new service': 0.05,
        'cancellation request': 0.05,
        'feature explanation': 0.08,
        'promotion inquiry': 0.07,
        'complaint': 0.03,
        'general question': 0.02
    }
    
    resolution_statuses = {
        'resolved': 0.7,
        'pending': 0.15,
        'transferred': 0.1,
        'follow-up required': 0.05
    }
    
    # Topic preferences by segment
    segment_topic_preferences = {
        "Premium": {
            'technical support': 0.3,
            'upgrade options': 0.2,
            'feature explanation': 0.15,
            'account inquiry': 0.1,
            'billing question': 0.1,
            'promotion inquiry': 0.05,
            'new service': 0.05,
            'cancellation request': 0.02,
            'complaint': 0.02,
            'general question': 0.01
        },
        "Budget": {
            'billing question': 0.3,
            'technical support': 0.2,
            'account inquiry': 0.15,
            'cancellation request': 0.1,
            'promotion inquiry': 0.1,
            'complaint': 0.05,
            'upgrade options': 0.03,
            'new service': 0.03,
            'feature explanation': 0.02,
            'general question': 0.02
        },
        "Business": {
            'technical support': 0.3,
            'account inquiry': 0.2,
            'feature explanation': 0.15,
            'billing question': 0.1,
            'upgrade options': 0.1,
            'new service': 0.05,
            'promotion inquiry': 0.05,
            'cancellation request': 0.02,
            'complaint': 0.02,
            'general question': 0.01
        }
    }
    
    # Channel preferences by age group
    age_channel_preferences = {
        (18, 30): {  # Young adults prefer digital channels
            'call': 0.15,
            'chat': 0.35,
            'email': 0.15,
            'store': 0.05,
            'social media': 0.15,
            'website': 0.15
        },
        (31, 50): {  # Middle-aged - balanced preferences
            'call': 0.3,
            'chat': 0.25,
            'email': 0.25,
            'store': 0.1,
            'social media': 0.05,
            'website': 0.05
        },
        (51, 80): {  # Older adults prefer traditional channels
            'call': 0.5,
            'chat': 0.15,
            'email': 0.15,
            'store': 0.15,
            'social media': 0.01,
            'website': 0.04
        }
    }
    
    # Time-of-day patterns - interactions happen at different times
    hour_weights = {h: 1.0 for h in range(24)}
    # Business hours
    for h in range(8, 18):
        hour_weights[h] = 4.0
    # Peak hours
    hour_weights[10] = 5.0
    hour_weights[14] = 5.0
    # Evening
    for h in range(18, 21):
        hour_weights[h] = 2.0
    # Late night/early morning
    for h in range(21, 24):
        hour_weights[h] = 0.5
    for h in range(0, 8):
        hour_weights[h] = 0.2
    
    for customer in customers:
        customer_id = customer["customer_id"]
        segment = customer["segment"]
        dob_str = customer.get("dob")
        satisfaction = customer.get("satisfaction_score", 7)  # Default to 7 if missing
        
        # Calculate age from DOB
        target_age = 40  # Default if DOB missing
        if dob_str:
            try:
                dob = datetime.date.fromisoformat(dob_str)
                target_age = calculate_age(dob)
            except:
                pass  # Use default if parsing fails
        
        # Number of interactions correlates with satisfaction (inverse)
        # and segment (Premium and Business have more interactions)
        base_interactions = max(1, int(10 - satisfaction))
        
        if segment == "Premium":
            base_interactions = int(base_interactions * 1.5)
        elif segment == "Business":
            base_interactions = int(base_interactions * 1.8)
        elif segment == "Budget":
            base_interactions = int(base_interactions * 0.8)
            
        num_interactions = max(1, base_interactions + random.randint(-1, 2))
        
        for _ in range(num_interactions):
            # Get topic preferences for segment
            topic_prefs = segment_topic_preferences.get(
                segment, 
                topics  # Default to general distribution if segment not specified
            )
            
            # Get channel preferences for age group
            age_group = next(
                (g for g in age_channel_preferences.keys() if g[0] <= target_age <= g[1]),
                (31, 50)  # Default to middle-aged if no match
            )
            channel_prefs = age_channel_preferences[age_group]
            
            # Select topic and channel based on preferences
            topic = random.choices(
                list(topic_prefs.keys()),
                weights=list(topic_prefs.values())
            )[0]
            
            channel = random.choices(
                list(channel_prefs.keys()),
                weights=list(channel_prefs.values())
            )[0]
            
            # Generate interaction time with hour distribution
            base_time = fake.date_time_between(start_date="-6m", end_date="now")
            hour = random.choices(
                list(hour_weights.keys()),
                weights=list(hour_weights.values())
            )[0]
            interaction_time = base_time.replace(hour=hour)
            
            # Duration depends on channel and topic complexity
            if channel in ['call', 'store']:
                base_duration = 300  # 5 minutes base
                
                # Complex topics take longer
                if topic in ['technical support', 'cancellation request']:
                    base_duration = 600  # 10 minutes
                elif topic in ['billing question', 'upgrade options']:
                    base_duration = 450  # 7.5 minutes
                    
                # Add randomness
                duration = int(base_duration * random.uniform(0.7, 1.3))
            elif channel == 'chat':
                base_duration = 450  # 7.5 minutes base
                
                # Complex topics take longer
                if topic in ['technical support', 'cancellation request']:
                    base_duration = 720  # 12 minutes
                elif topic in ['billing question', 'upgrade options']:
                    base_duration = 600  # 10 minutes
                    
                # Add randomness
                duration = int(base_duration * random.uniform(0.7, 1.3))
            else:
                duration = 0  # No duration for email, social media, etc.
            
            # Agent ID (1-30) - agents tend to specialize in certain topics
            if topic in ['technical support', 'feature explanation']:
                agent_id = random.randint(1, 10)  # Tech specialists
            elif topic in ['billing question', 'account inquiry']:
                agent_id = random.randint(11, 20)  # Account specialists
            else:
                agent_id = random.randint(21, 30)  # General agents
            
            # Resolution status - correlated with satisfaction and topic
            if satisfaction >= 8:
                # High satisfaction customers get better resolution
                res_weights = {"resolved": 0.85, "pending": 0.1, "transferred": 0.03, "follow-up required": 0.02}
            elif satisfaction >= 5:
                # Medium satisfaction
                res_weights = {"resolved": 0.7, "pending": 0.15, "transferred": 0.1, "follow-up required": 0.05}
            else:
                # Low satisfaction
                res_weights = {"resolved": 0.5, "pending": 0.2, "transferred": 0.2, "follow-up required": 0.1}
                
            # Adjust for complex topics
            if topic in ['technical support', 'cancellation request', 'complaint']:
                for status in res_weights:
                    if status != "resolved":
                        res_weights[status] *= 1.5
                # Normalize weights
                total = sum(res_weights.values())
                res_weights = {k: v/total for k, v in res_weights.items()}
                
            resolution_status = random.choices(
                list(res_weights.keys()),
                weights=list(res_weights.values())
            )[0]
            
            # Satisfaction rating (1-5 stars) - correlated with overall satisfaction
            # and resolution status
            if resolution_status == 'resolved':
                base_rating = max(1, min(5, satisfaction // 2))
                satisfaction_rating = max(1, min(5, base_rating + random.randint(-1, 1)))
            else:
                base_rating = max(1, min(5, (satisfaction // 2) - 1))
                satisfaction_rating = max(1, min(5, base_rating + random.randint(-1, 0)))
            
            # Generate notes
            if resolution_status == 'resolved':
                notes = f"{topic.capitalize()} via {channel}. " + random.choice([
                    "Customer was satisfied with the resolution.",
                    "Provided detailed explanation and resolved issue.",
                    "Customer's concern addressed successfully.",
                    "Resolved on first contact."
                ])
            elif resolution_status == 'pending':
                notes = f"{topic.capitalize()} via {channel}. " + random.choice([
                    "Customer needs additional information.",
                    "Awaiting system update to complete request.",
                    "Waiting for approval from management.",
                    "Research required before resolution."
                ])
            elif resolution_status == 'transferred':
                notes = f"{topic.capitalize()} via {channel}. " + random.choice([
                    "Transferred to specialized department for further help.",
                    "Escalated to supervisor due to complexity.",
                    "Required expertise not available, transferred to specialist.",
                    "Issue outside of agent's authority, transferred."
                ])
            else:  # follow-up required
                notes = f"{topic.capitalize()} via {channel}. " + random.choice([
                    "Scheduled follow-up for additional assistance.",
                    "Customer requested callback after reviewing options.",
                    "Follow-up needed to confirm resolution.",
                    "Additional information required from customer."
                ])
            
            interactions.append({
                "interaction_id": interaction_id,
                "customer_id": customer_id,
                "channel": channel,
                "agent_id": agent_id,
                "interaction_time": interaction_time.isoformat(),
                "duration_seconds": duration,
                "topic": topic,
                "resolution_status": resolution_status,
                "satisfaction_rating": satisfaction_rating,
                "notes": notes
            })
            
            interaction_id += 1
    
    return interactions

def generate_number_portability(customers: List[Dict]) -> List[Dict]:
    """Generate number portability records with realistic patterns."""
    portability_records = []
    portability_id = 1
    
    # List of carriers with realistic market share distribution
    carriers = {
        "Verizon": 0.3,
        "AT&T": 0.25,
        "T-Mobile": 0.2,
        "Sprint": 0.1,  # Still in records even after T-Mobile merger
        "US Cellular": 0.03,
        "Boost Mobile": 0.03,
        "Cricket Wireless": 0.03,
        "Metro by T-Mobile": 0.02,
        "Xfinity Mobile": 0.01,
        "Spectrum Mobile": 0.01,
        "Google Fi": 0.01,
        "Visible": 0.01
    }
    
    # Statuses and their realistic distributions
    # Most ports are completed successfully
    statuses = {
        "completed": 0.7,    # 70% complete successfully
        "in_progress": 0.15, # 15% in progress
        "requested": 0.1,    # 10% just requested
        "failed": 0.05       # 5% fail
    }
    
    # Failure reasons with distributions
    failure_reasons = {
        "Account information mismatch with previous carrier": 0.4,
        "Customer canceled port request": 0.2,
        "Previous carrier rejected port request": 0.2,
        "Technical issue during port process": 0.15,
        "Number not eligible for porting": 0.05
    }
    
    # Different segments have different port rates
    segment_port_rates = {
        "Premium": 0.2,    # 20% of Premium customers port numbers
        "Standard": 0.3,    # 30% of Standard customers port numbers
        "Budget": 0.5,     # 50% of Budget customers port numbers (price shoppers)
        "Business": 0.15,  # 15% of Business customers port numbers
        "Family": 0.25     # 25% of Family customers port numbers
    }
    
    for customer in customers:
        customer_id = customer["customer_id"]
        segment = customer["segment"]
        
        # Determine if this customer has ported a number
        port_rate = segment_port_rates.get(segment, 0.3)
        has_ported = random.random() < port_rate
        
        if has_ported:
            # Select previous carrier based on market share
            prev_carrier = random.choices(
                list(carriers.keys()),
                weights=list(carriers.values())
            )[0]
            
            # Select status based on distribution
            status = random.choices(
                list(statuses.keys()),
                weights=list(statuses.values())
            )[0]
            
            # Generate port date (more recent customers more likely to have recent ports)
            if customer_id < len(customers) * 0.3:  # Oldest 30% of customers
                port_date = fake.date_time_between(start_date="-2y", end_date="-6m")
            elif customer_id < len(customers) * 0.7:  # Middle 40%
                port_date = fake.date_time_between(start_date="-1y", end_date="-3m")
            else:  # Newest 30%
                port_date = fake.date_time_between(start_date="-6m", end_date="-1w")
            
            # Completion date depends on status
            if status == "completed":
                # Completed in 1-7 days
                completion_date = port_date + datetime.timedelta(days=random.randint(1, 7))
            elif status == "failed":
                # Failed after 1-10 days
                completion_date = port_date + datetime.timedelta(days=random.randint(1, 10))
            else:
                completion_date = None
                
                # If in progress/requested and old port date, adjust status and completion
                days_since_port = (datetime.datetime.now() - port_date).days
                if days_since_port > 14 and status == "in_progress":
                    # Old in-progress requests likely failed
                    status = "failed"
                    completion_date = port_date + datetime.timedelta(days=random.randint(1, 10))
                elif days_since_port > 7 and status == "requested":
                    # Old requests likely moved to in_progress or failed
                    status = random.choice(["in_progress", "failed"])
                    if status == "failed":
                        completion_date = port_date + datetime.timedelta(days=random.randint(1, 10))
            
            # Generate notes based on status
            if status == "completed":
                notes = random.choice([
                    "Number successfully ported from previous carrier.",
                    "Port completed without issues.",
                    "Customer can now use their old number with our service.",
                    "Port completed and service active."
                ])
            elif status == "failed":
                # Select failure reason based on distribution
                failure_reason = random.choices(
                    list(failure_reasons.keys()),
                    weights=list(failure_reasons.values())
                )[0]
                notes = failure_reason
            elif status == "in_progress":
                notes = random.choice([
                    "Port request being processed by previous carrier.",
                    "Awaiting confirmation from previous carrier.",
                    "Port scheduled to complete within 24-48 hours.",
                    "Verification in progress."
                ])
            else:  # requested
                notes = random.choice([
                    "Initial port request submitted. Awaiting processing.",
                    "Customer information verified. Port request initiated.",
                    "Documentation received. Request sent to previous carrier.",
                    "Port request in queue for processing."
                ])
            
            portability_records.append({
                "portability_id": portability_id,
                "customer_id": customer_id,
                "phone_number": generate_phone_number(),
                "previous_carrier": prev_carrier,
                "port_date": port_date.isoformat(),
                "status": status,
                "completion_date": completion_date.isoformat() if completion_date else None,
                "notes": notes
            })
            
            portability_id += 1
    
    return portability_records

def generate_voip_services(customers: List[Dict]) -> List[Dict]:
    """Generate VoIP service records with realistic adoption patterns."""
    voip_services = []
    voip_id = 1
    
    # Service types with realistic distribution
    service_types = {
        "Business VoIP": 0.35,
        "Residential VoIP": 0.3,
        "SIP Trunking": 0.15,
        "Cloud PBX": 0.15,
        "Virtual Phone": 0.05
    }
    
    # Features by service type with realistic adoption rates
    features_by_type = {
        "Business VoIP": {
            "Call Forwarding": 0.9,
            "Voicemail": 0.95,
            "Call Recording": 0.7,
            "Auto Attendant": 0.85,
            "Conference Calling": 0.8,
            "Call Analytics": 0.6,
            "Number Porting": 0.7,
            "Call Queuing": 0.65,
            "Video Conferencing": 0.5,
            "Mobile App": 0.75,
            "CRM Integration": 0.4,
            "International Calling": 0.3
        },
        "Residential VoIP": {
            "Call Forwarding": 0.8,
            "Voicemail": 0.9,
            "Call Recording": 0.3,
            "Auto Attendant": 0.2,
            "Conference Calling": 0.4,
            "Call Analytics": 0.1,
            "Number Porting": 0.6,
            "Call Queuing": 0.1,
            "Video Conferencing": 0.3,
            "Mobile App": 0.7,
            "CRM Integration": 0.05,
            "International Calling": 0.4
        },
        "SIP Trunking": {
            "Call Forwarding": 0.7,
            "Voicemail": 0.8,
            "Call Recording": 0.6,
            "Auto Attendant": 0.7,
            "Conference Calling": 0.6,
            "Call Analytics": 0.5,
            "Number Porting": 0.8,
            "Call Queuing": 0.6,
            "Video Conferencing": 0.3,
            "Mobile App": 0.5,
            "CRM Integration": 0.4,
            "International Calling": 0.5
        },
        "Cloud PBX": {
            "Call Forwarding": 0.9,
            "Voicemail": 0.95,
            "Call Recording": 0.8,
            "Auto Attendant": 0.9,
            "Conference Calling": 0.85,
            "Call Analytics": 0.7,
            "Number Porting": 0.75,
            "Call Queuing": 0.8,
            "Video Conferencing": 0.6,
            "Mobile App": 0.7,
            "CRM Integration": 0.5,
            "International Calling": 0.4
        },
        "Virtual Phone": {
            "Call Forwarding": 0.95,
            "Voicemail": 0.9,
            "Call Recording": 0.5,
            "Auto Attendant": 0.6,
            "Conference Calling": 0.7,
            "Call Analytics": 0.4,
            "Number Porting": 0.8,
            "Call Queuing": 0.3,
            "Video Conferencing": 0.4,
            "Mobile App": 0.9,
            "CRM Integration": 0.3,
            "International Calling": 0.6
        }
    }
    
    # Segment adoption rates for VoIP
    segment_voip_rates = {
        "Premium": 0.15,    # 15% of Premium customers have VoIP
        "Standard": 0.1,    # 10% of Standard customers have VoIP
        "Budget": 0.05,     # 5% of Budget customers have VoIP
        "Business": 0.6,    # 60% of Business customers have VoIP
        "Family": 0.1       # 10% of Family customers have VoIP
    }
    
    # Service type preferences by segment
    segment_service_preferences = {
        "Premium": {
            "Business VoIP": 0.3,
            "Residential VoIP": 0.3,
            "SIP Trunking": 0.1,
            "Cloud PBX": 0.2,
            "Virtual Phone": 0.1
        },
        "Standard": {
            "Business VoIP": 0.1,
            "Residential VoIP": 0.6,
            "SIP Trunking": 0.05,
            "Cloud PBX": 0.05,
            "Virtual Phone": 0.2
        },
        "Budget": {
            "Business VoIP": 0.05,
            "Residential VoIP": 0.7,
            "SIP Trunking": 0.05,
            "Cloud PBX": 0.0,
            "Virtual Phone": 0.2
        },
        "Business": {
            "Business VoIP": 0.4,
            "Residential VoIP": 0.0,
            "SIP Trunking": 0.2,
            "Cloud PBX": 0.35,
            "Virtual Phone": 0.05
        },
        "Family": {
            "Business VoIP": 0.1,
            "Residential VoIP": 0.7,
            "SIP Trunking": 0.0,
            "Cloud PBX": 0.0,
            "Virtual Phone": 0.2
        }
    }
    
    for customer in customers:
        customer_id = customer["customer_id"]
        segment = customer["segment"]
        
        # Determine if this customer has VoIP services
        voip_rate = segment_voip_rates.get(segment, 0.1)
        has_voip = random.random() < voip_rate
        
        if has_voip:
            # Number of VoIP services depends on segment
            if segment == "Business":
                # Business customers might have multiple services
                num_services_weights = {1: 0.7, 2: 0.3}
            else:
                # Other segments usually have just one
                num_services_weights = {1: 0.95, 2: 0.05}
                
            num_services = random.choices(
                list(num_services_weights.keys()),
                weights=list(num_services_weights.values())
            )[0]
            
            # Service preferences for this segment
            service_prefs = segment_service_preferences.get(
                segment, 
                service_types  # Default to general distribution if segment not specified
            )
            
            # Select services
            selected_services = []
            for _ in range(num_services):
                service_type = random.choices(
                    list(service_prefs.keys()),
                    weights=list(service_prefs.values())
                )[0]
                
                if service_type not in selected_services:
                    selected_services.append(service_type)
            
            for service_type in selected_services:
                # Set pricing based on service type and segment
                if service_type in ["Business VoIP", "SIP Trunking", "Cloud PBX"]:
                    if segment == "Business":
                        # Business customers pay more for premium features
                        base_fee = random.uniform(70, 150)
                    else:
                        base_fee = random.uniform(50, 100)
                else:
                    if segment == "Budget":
                        # Budget customers pick cheaper options
                        base_fee = random.uniform(15, 30)
                    else:
                        base_fee = random.uniform(20, 50)
                
                # Select features based on service type
                feature_probs = features_by_type[service_type]
                selected_features = []
                
                for feature, probability in feature_probs.items():
                    # Adjust probability based on segment
                    if segment == "Premium" or segment == "Business":
                        # Premium and Business customers more likely to have premium features
                        adj_probability = min(1.0, probability * 1.2)
                    elif segment == "Budget":
                        # Budget customers less likely to have premium features
                        adj_probability = probability * 0.8
                    else:
                        adj_probability = probability
                        
                    if random.random() < adj_probability:
                        selected_features.append(feature)
                
                # Format features for PostgreSQL array
                features = "{" + ",".join('"' + feature + '"' for feature in selected_features) + "}"
                
                # Generate activation date - correlate with customer creation
                if customer_id < len(customers) * 0.3:  # Oldest 30% of customers
                    activation_date = fake.date_time_between(start_date="-2y", end_date="-1y")
                elif customer_id < len(customers) * 0.7:  # Middle 40%
                    activation_date = fake.date_time_between(start_date="-1y", end_date="-6m")
                else:  # Newest 30%
                    activation_date = fake.date_time_between(start_date="-6m", end_date="-1m")
                
                activation_date_str = activation_date.date().isoformat()
                
                # Status - newer services and higher satisfaction more likely to be active
                satisfaction = customer.get("satisfaction_score", 7)
                days_since_activation = (datetime.datetime.now() - activation_date).days
                
                if days_since_activation < 90 or satisfaction >= 8:
                    # New service or satisfied customer - likely active
                    status_weights = {"active": 0.95, "suspended": 0.04, "terminated": 0.01}
                elif days_since_activation < 365 or satisfaction >= 5:
                    # Older service or medium satisfaction
                    status_weights = {"active": 0.85, "suspended": 0.1, "terminated": 0.05}
                else:
                    # Old service and low satisfaction
                    status_weights = {"active": 0.7, "suspended": 0.15, "terminated": 0.15}
                    
                status = random.choices(
                    list(status_weights.keys()),
                    weights=list(status_weights.values())
                )[0]
                
                voip_services.append({
                    "voip_id": voip_id,
                    "customer_id": customer_id,
                    "service_number": generate_phone_number(),
                    "service_type": service_type,
                    "monthly_fee": round(base_fee, 2),
                    "features": features,
                    "activation_date": activation_date_str,
                    "status": status
                })
                
                voip_id += 1
    
    return voip_services

def generate_iot_devices(customers: List[Dict], plans: List[Dict]) -> List[Dict]:
    """Generate IoT device records with realistic adoption patterns."""
    iot_devices = []
    iot_device_id = 1
    
    # Device types with realistic distribution and typical data usage
    device_types = {
        "Smart Tracker": {"share": 0.2, "data_range": (5, 50)},
        "Asset Monitor": {"share": 0.15, "data_range": (10, 80)},
        "Fleet Tracker": {"share": 0.1, "data_range": (20, 150)},
        "Smart Meter": {"share": 0.15, "data_range": (2, 30)},
        "Security Sensor": {"share": 0.15, "data_range": (30, 200)},
        "Environmental Monitor": {"share": 0.05, "data_range": (5, 50)},
        "Agricultural Sensor": {"share": 0.05, "data_range": (10, 100)},
        "Industrial Monitor": {"share": 0.05, "data_range": (50, 300)},
        "Smart City Sensor": {"share": 0.05, "data_range": (20, 150)},
        "Health Monitor": {"share": 0.05, "data_range": (2, 20)}
    }
    
    # Find IoT plans
    iot_plans = [p for p in plans if p["type"] == "IoT"]
    if not iot_plans:
        # Fallback to lowest data mobile plans if no IoT plans
        mobile_plans = [p for p in plans if p["type"] == "Mobile" and p["data_limit_gb"] is not None]
        if mobile_plans:
            # Sort by data limit to find smallest data plans
            iot_plans = sorted(mobile_plans, key=lambda p: p["data_limit_gb"] or 1000)[:3]
        else:
            iot_plans = [random.choice(plans)]  # Last resort
    
    # Segment adoption rates for IoT
    segment_iot_rates = {
        "Premium": 0.2,     # 20% of Premium customers have IoT
        "Standard": 0.1,    # 10% of Standard customers have IoT
        "Budget": 0.05,     # 5% of Budget customers have IoT
        "Business": 0.4,    # 40% of Business customers have IoT
        "Family": 0.15      # 15% of Family customers have IoT
    }
    
    # Device type preferences by segment
    segment_device_preferences = {
        "Premium": {
            "Smart Tracker": 0.25,
            "Security Sensor": 0.25,
            "Smart Meter": 0.15,
            "Health Monitor": 0.15,
            "Environmental Monitor": 0.1,
            "Fleet Tracker": 0.05,
            "Asset Monitor": 0.05
        },
        "Business": {
            "Fleet Tracker": 0.3,
            "Asset Monitor": 0.25,
            "Industrial Monitor": 0.2,
            "Security Sensor": 0.15,
            "Smart Tracker": 0.05,
            "Smart City Sensor": 0.05
        },
        "Family": {
            "Smart Tracker": 0.3,
            "Security Sensor": 0.25,
            "Smart Meter": 0.2,
            "Health Monitor": 0.15,
            "Environmental Monitor": 0.1
        }
    }
    
    for customer in customers:
        customer_id = customer["customer_id"]
        segment = customer["segment"]
        
        # Determine if this customer has IoT devices
        iot_rate = segment_iot_rates.get(segment, 0.1)
        has_iot = random.random() < iot_rate
        
        if has_iot:
            # Number of IoT devices depends on segment
            if segment == "Business":
                # Business customers often have multiple devices
                num_devices_weights = {1: 0.2, 2: 0.3, 3: 0.25, 4: 0.15, 5: 0.1}
            elif segment == "Premium":
                # Premium customers likely have a few devices
                num_devices_weights = {1: 0.4, 2: 0.35, 3: 0.15, 4: 0.07, 5: 0.03}
            else:
                # Other segments usually have fewer
                num_devices_weights = {1: 0.7, 2: 0.2, 3: 0.1}
                
            num_devices = random.choices(
                list(num_devices_weights.keys()),
                weights=list(num_devices_weights.values())
            )[0]
            
            # Get device preferences for this segment
            device_prefs = segment_device_preferences.get(
                segment, 
                {k: v["share"] for k, v in device_types.items()}  # Default to general distribution
            )
            
            for _ in range(num_devices):
                # Select device type based on segment preferences
                device_type = random.choices(
                    list(device_prefs.keys()),
                    weights=list(device_prefs.values())
                )[0]
                
                # Generate IMEI and SIM ICCID
                imei = f"{random.randint(100000000000000, 999999999999999)}"
                sim_iccid = f"89{random.randint(10000000000000000000, 99999999999999999999)}"
                
                # Assign a data plan
                data_plan = random.choice(iot_plans)
                
                # Generate activation date - different patterns by segment
                if segment == "Business":
                    # Business IoT adoption started earlier
                    activation_date = fake.date_time_between(start_date="-3y", end_date="-6m")
                elif segment == "Premium":
                    # Premium customers are early adopters
                    activation_date = fake.date_time_between(start_date="-2y", end_date="-3m")
                else:
                    # Others adopted more recently
                    activation_date = fake.date_time_between(start_date="-1y", end_date="-1m")
                
                activation_date_str = activation_date.date().isoformat()
                
                # Generate last active date with realistic patterns
                if segment == "Business":
                    # Business devices are used consistently
                    days_inactive = random.randint(0, 3)
                elif random.random() < 0.8:
                    # Most devices used recently
                    days_inactive = random.randint(0, 14)
                else:
                    # Some devices less frequently used
                    days_inactive = random.randint(7, 60)
                    
                last_active_date = (datetime.datetime.now() - datetime.timedelta(days=days_inactive))
                
                # Typical data usage range for this device type
                data_range = device_types[device_type]["data_range"]
                
                # Generate monthly data usage with some randomness
                base_usage = random.uniform(data_range[0], data_range[1])
                
                # Business devices tend to use more data
                if segment == "Business":
                    monthly_data_usage = base_usage * random.uniform(1.0, 1.5)
                else:
                    monthly_data_usage = base_usage * random.uniform(0.8, 1.2)
                
                # Status - newer devices and business customers more likely to have active devices
                days_since_activation = (datetime.datetime.now() - activation_date).days
                
                if segment == "Business" or days_since_activation < 180:
                    # Business or newer devices - likely active
                    status_weights = {"active": 0.95, "inactive": 0.04, "suspended": 0.01}
                elif days_since_activation < 365:
                    # Older devices
                    status_weights = {"active": 0.85, "inactive": 0.1, "suspended": 0.05}
                else:
                    # Very old devices
                    status_weights = {"active": 0.7, "inactive": 0.2, "suspended": 0.1}
                    
                status = random.choices(
                    list(status_weights.keys()),
                    weights=list(status_weights.values())
                )[0]
                
                iot_devices.append({
                    "iot_device_id": iot_device_id,
                    "customer_id": customer_id,
                    "device_type": device_type,
                    "imei": imei,
                    "sim_iccid": sim_iccid,
                    "data_plan_id": data_plan["plan_id"],
                    "activation_date": activation_date_str,
                    "last_active_date": last_active_date.isoformat(),
                    "monthly_data_usage_mb": round(monthly_data_usage, 2),
                    "status": status
                })
                
                iot_device_id += 1
    
    return iot_devices

def generate_referrals(customers: List[Dict]) -> List[Dict]:
    """Generate customer referral records with realistic patterns."""
    referrals = []
    referral_id = 1
    
    # Referral propensity by satisfaction and segment
    satisfaction_referral_rates = {
        (1, 4): 0.05,   # 5% of low satisfaction customers (1-4) refer
        (5, 7): 0.15,   # 15% of medium satisfaction customers (5-7) refer
        (8, 10): 0.35   # 35% of high satisfaction customers (8-10) refer
    }
    
    # Segment-specific adjustments
    segment_referral_multipliers = {
        "Premium": 1.5,    # Premium 50% more likely to refer
        "Standard": 1.0,   # Standard baseline
        "Budget": 0.8,     # Budget 20% less likely to refer
        "Business": 1.2,   # Business 20% more likely to refer
        "Family": 1.3      # Family 30% more likely to refer (family connections)
    }
    
    # Status probabilities
    status_probabilities = {
        "accepted": 0.65,  # 65% of referrals are accepted
        "pending": 0.25,   # 25% still pending
        "expired": 0.1     # 10% expired
    }
    
    # Customer relationship network - who refers whom
    # Create clusters of customers who might know each other
    
    # Group by location (country, state)
    location_groups = {}
    for customer in customers:
        location_key = (customer["country"], customer["state"])
        if location_key not in location_groups:
            location_groups[location_key] = []
        location_groups[location_key].append(customer)
    
    # Identify potential referrers based on satisfaction
    potential_referrers = []
    for customer in customers:
        satisfaction = customer.get("satisfaction_score", 7)
        segment = customer["segment"]
        
        # Find applicable satisfaction bracket
        referral_rate = next(
            (rate for sat_range, rate in satisfaction_referral_rates.items() 
             if sat_range[0] <= satisfaction <= sat_range[1]),
            0.1  # Default to 10% if no range matches
        )
        
        # Apply segment multiplier
        referral_rate *= segment_referral_multipliers.get(segment, 1.0)
        
        # Cap rate at 80%
        referral_rate = min(0.8, referral_rate)
        
        if random.random() < referral_rate:
            potential_referrers.append(customer)
    
    for referrer in potential_referrers:
        # Number of referrals made by this customer
        if referrer["segment"] in ["Family", "Business"]:
            # Family and Business customers tend to make more referrals
            num_referrals_weights = {1: 0.5, 2: 0.3, 3: 0.2}
        else:
            # Others usually make fewer
            num_referrals_weights = {1: 0.7, 2: 0.25, 3: 0.05}
            
        num_referrals = random.choices(
            list(num_referrals_weights.keys()),
            weights=list(num_referrals_weights.values())
        )[0]
        
        # Find potential referred customers
        # First look in same location (more likely to know people nearby)
        location_key = (referrer["country"], referrer["state"])
        same_location_customers = [
            c for c in location_groups.get(location_key, [])
            if c["customer_id"] != referrer["customer_id"]
        ]
        
        # If not enough local customers, include others
        if len(same_location_customers) < num_referrals:
            other_customers = [
                c for c in customers 
                if c["customer_id"] != referrer["customer_id"] and 
                (c["country"], c["state"]) != location_key
            ]
            
            # Prefer local customers with higher weight
            if same_location_customers and other_customers:
                referred_pool = random.choices(
                    [same_location_customers, other_customers],
                    weights=[0.7, 0.3]
                )[0]
            else:
                referred_pool = same_location_customers or other_customers
        else:
            referred_pool = same_location_customers
        
        # Select random referred customers
        if len(referred_pool) >= num_referrals:
            referred_customers = random.sample(referred_pool, num_referrals)
            
            for referred in referred_customers:
                # Referral date - more recent for newer customers
                days_since_account = min(
                    365,  # Cap at 1 year
                    (datetime.datetime.now() - datetime.datetime.fromisoformat(
                        referred.get("created_at", 
                                    (datetime.datetime.now() - datetime.timedelta(days=180)).isoformat()
                                    )
                    )).days
                )
                
                # Newer accounts have more recent referrals
                max_days_ago = min(days_since_account, 180)  # At most 6 months ago
                referral_date = fake.date_time_between(
                    start_date=f"-{max_days_ago}d", 
                    end_date="now"
                )
                referral_date_str = referral_date.date().isoformat()
                
                # Status depends on how recent the referral is
                days_since_referral = (datetime.datetime.now() - referral_date).days
                
                if days_since_referral < 14:
                    # Recent referrals mostly pending
                    status_weights = {"pending": 0.7, "accepted": 0.3, "expired": 0.0}
                elif days_since_referral < 45:
                    # Medium-age referrals
                    status_weights = {"pending": 0.2, "accepted": 0.7, "expired": 0.1}
                else:
                    # Older referrals
                    status_weights = {"pending": 0.1, "accepted": 0.7, "expired": 0.2}
                    
                status = random.choices(
                    list(status_weights.keys()),
                    weights=list(status_weights.values())
                )[0]
                
                # Bonus amount - higher for premium segments
                if referrer["segment"] in ["Premium", "Business"]:
                    bonus_options = [50, 75, 100]
                    bonus_weights = [0.2, 0.3, 0.5]
                else:
                    bonus_options = [25, 50, 75]
                    bonus_weights = [0.5, 0.3, 0.2]
                    
                bonus_amount = random.choices(
                    bonus_options,
                    weights=bonus_weights
                )[0]
                
                # Bonus paid (only if accepted)
                bonus_paid = status == "accepted" and random.random() < 0.9
                
                referrals.append({
                    "referral_id": referral_id,
                    "referrer_id": referrer["customer_id"],
                    "referred_id": referred["customer_id"],
                    "referral_date": referral_date_str,
                    "status": status,
                    "bonus_amount": bonus_amount,
                    "bonus_paid": bonus_paid
                })
                
                referral_id += 1
    
    return referrals

def generate_device_upgrades(customers: List[Dict], devices: List[Dict]) -> List[Dict]:
    """Generate device upgrade and trade-in records with realistic patterns."""
    upgrades = []
    upgrade_id = 1
    
    # Segment upgrade frequencies
    segment_upgrade_rates = {
        "Premium": 0.5,     # 50% of Premium customers upgrade devices
        "Standard": 0.3,    # 30% of Standard customers upgrade devices
        "Budget": 0.15,     # 15% of Budget customers upgrade devices
        "Business": 0.4,    # 40% of Business customers upgrade devices
        "Family": 0.25      # 25% of Family customers upgrade devices
    }
    
    # Group devices by brand
    devices_by_brand = {}
    for device in devices:
        brand = device["brand"]
        if brand not in devices_by_brand:
            devices_by_brand[brand] = []
        devices_by_brand[brand].append(device)
    
    # Device age categories - define 'new' and 'mid' first
    device_age_categories = {
        "new": [d for d in devices if "14" in d["model"] or "15" in d["model"] or 
                "S23" in d["model"] or "Pixel 7" in d["model"]],
        "mid": [d for d in devices if "13" in d["model"] or "S22" in d["model"] or 
                "Pixel 6" in d["model"]]
    }
    
    # Then add 'old' category afterward
    device_age_categories["old"] = [d for d in devices if 
                                    "SE" in d["model"] or 
                                    "Note 20" in d["model"] or 
                                    "A53" in d["model"] or 
                                    (d not in device_age_categories["new"] and 
                                     d not in device_age_categories["mid"])]
    
    # Brand loyalty patterns
    brand_loyalty = {
        "Apple": 0.9,       # 90% of Apple users stay with Apple
        "Samsung": 0.8,     # 80% of Samsung users stay with Samsung
        "Google": 0.7,      # 70% of Google users stay with Google
        "OnePlus": 0.6,     # 60% of OnePlus users stay with OnePlus
        "Xiaomi": 0.5,      # 50% of Xiaomi users stay with Xiaomi
        "Huawei": 0.4       # 40% of Huawei users stay with Huawei (lower due to restrictions)
    }
    
    for customer in customers:
        customer_id = customer["customer_id"]
        segment = customer["segment"]
        
        # Determine if this customer has upgraded devices
        upgrade_rate = segment_upgrade_rates.get(segment, 0.3)
        has_upgraded = random.random() < upgrade_rate
        
        if has_upgraded and len(devices) >= 2:
            # Number of upgrades correlates with segment and satisfaction
            satisfaction = customer.get("satisfaction_score", 7)
            
            if segment in ["Premium", "Business"] and satisfaction >= 7:
                # Satisfied premium/business customers upgrade more
                num_upgrades_weights = {1: 0.6, 2: 0.4}
            else:
                # Others usually upgrade once
                num_upgrades_weights = {1: 0.9, 2: 0.1}
                
            num_upgrades = random.choices(
                list(num_upgrades_weights.keys()),
                weights=list(num_upgrades_weights.values())
            )[0]
            
            for upgrade_num in range(num_upgrades):
                # For repeat upgrades, make sure the dates make sense
                min_date = "-2y" if upgrade_num == 0 else "-1y"
                
                # Select old device
                if upgrade_num == 0:
                    # First upgrade - old device more likely to be older model
                    if random.random() < 0.7:  # 70% chance of upgrading from old device
                        old_device_pool = device_age_categories["old"]
                        if not old_device_pool:
                            old_device_pool = device_age_categories["mid"]
                        if not old_device_pool:
                            old_device_pool = devices
                    else:  # 30% chance of upgrading from mid-age device
                        old_device_pool = device_age_categories["mid"]
                        if not old_device_pool:
                            old_device_pool = devices
                else:
                    # Second upgrade - old device likely mid-tier from previous upgrade
                    old_device_pool = device_age_categories["mid"]
                    if not old_device_pool:
                        old_device_pool = devices
                
                old_device = random.choice(old_device_pool)
                
                # Select new device based on brand loyalty
                old_brand = old_device["brand"]
                
                # Determine if customer stays with same brand
                stays_loyal = random.random() < brand_loyalty.get(old_brand, 0.6)
                
                if stays_loyal and old_brand in devices_by_brand:
                    # Stay with same brand but get newer model
                    same_brand_devices = devices_by_brand[old_brand]
                    
                    # Filter for newer models than old device
                    newer_models = [d for d in same_brand_devices if d["device_id"] != old_device["device_id"]]
                    
                    if newer_models:
                        # Prefer newest models
                        new_device_pool = [d for d in newer_models if d in device_age_categories["new"]]
                        if not new_device_pool:
                            new_device_pool = newer_models
                            
                        new_device = random.choice(new_device_pool)
                    else:
                        # Fallback to any other device
                        remaining_devices = [d for d in devices if d["device_id"] != old_device["device_id"]]
                        new_device = random.choice(remaining_devices)
                else:
                    # Switch brands
                    # Premium users more likely to switch to premium brands
                    if segment == "Premium":
                        new_brand_weights = {"Apple": 0.5, "Samsung": 0.3, "Google": 0.2}
                    elif segment == "Budget":
                        new_brand_weights = {"Xiaomi": 0.4, "OnePlus": 0.3, "Samsung": 0.2, "Apple": 0.1}
                    else:
                        new_brand_weights = {"Samsung": 0.3, "Apple": 0.3, "Google": 0.2, 
                                            "OnePlus": 0.1, "Xiaomi": 0.1}
                    
                    # Remove old brand from options
                    if old_brand in new_brand_weights:
                        del new_brand_weights[old_brand]
                        
                    # Select new brand
                    new_brand = random.choices(
                        list(new_brand_weights.keys()),
                        weights=list(new_brand_weights.values())
                    )[0]
                    
                    # Get devices of new brand
                    if new_brand in devices_by_brand:
                        new_brand_devices = devices_by_brand[new_brand]
                        
                        # Prefer newest models
                        new_device_pool = [d for d in new_brand_devices if d in device_age_categories["new"]]
                        if not new_device_pool:
                            new_device_pool = new_brand_devices
                            
                        new_device = random.choice(new_device_pool)
                    else:
                        # Fallback to any other device
                        remaining_devices = [d for d in devices if d["device_id"] != old_device["device_id"]]
                        new_device = random.choice(remaining_devices)
                
                # Generate upgrade date
                if segment in ["Premium", "Business"]:
                    # Premium/Business users upgrade more frequently
                    upgrade_date = fake.date_time_between(start_date=min_date, end_date="-1m")
                else:
                    # Others upgrade less frequently
                    upgrade_date = fake.date_time_between(start_date=min_date, end_date="-3m")
                
                upgrade_date_str = upgrade_date.date().isoformat()
                
                # Trade-in value based on old device and its age
                old_device_age_factor = 1.0
                if old_device in device_age_categories["old"]:
                    old_device_age_factor = 0.5  # Old devices worth less
                elif old_device in device_age_categories["mid"]:
                    old_device_age_factor = 0.7  # Mid-age devices worth more
                    
                # Brand value factor
                brand_value_factor = {
                    "Apple": 1.2,     # Apple devices retain value better
                    "Samsung": 1.1,   # Samsung good resale value
                    "Google": 1.0,    # Google standard
                    "OnePlus": 0.9,   # OnePlus slightly lower
                    "Xiaomi": 0.8,    # Xiaomi lower resale value
                    "Huawei": 0.7     # Huawei lowest due to restrictions
                }
                
                # Calculate trade-in value
                base_value = random.uniform(100, 300)
                trade_in_value = base_value * old_device_age_factor * brand_value_factor.get(old_brand, 1.0)
                
                # Contract extension based on segment
                if segment == "Budget":
                    # Budget users more likely to extend contract for better deal
                    contract_extension_weights = {0: 0.1, 12: 0.3, 24: 0.6}
                elif segment == "Premium":
                    # Premium users less likely to be locked in
                    contract_extension_weights = {0: 0.5, 12: 0.3, 24: 0.2}
                else:
                    # Others balanced
                    contract_extension_weights = {0: 0.3, 12: 0.4, 24: 0.3}
                    
                contract_extension = random.choices(
                    list(contract_extension_weights.keys()),
                    weights=list(contract_extension_weights.values())
                )[0]
                
                # Promotion applied
                if random.random() < 0.7:  # 70% chance of a promotion
                    # Seasonal promotions
                    month = upgrade_date.month
                    if month in [11, 12]:  # Holiday season
                        promo_options = ["Holiday Special", "Black Friday Deal", "Year-End Offer"]
                    elif month in [1, 2]:  # New Year
                        promo_options = ["New Year Discount", "Winter Special", "New Model Launch"]
                    elif month in [7, 8]:  # Summer
                        promo_options = ["Summer Deal", "Vacation Special", "Back to School Offer"]
                    else:
                        promo_options = ["Loyalty Upgrade", "Trade-In Bonus", "Limited Time Offer"]
                        
                    promotion_applied = random.choice(promo_options)
                else:
                    promotion_applied = None
                
                upgrades.append({
                    "upgrade_id": upgrade_id,
                    "customer_id": customer_id,
                    "old_device_id": old_device["device_id"],
                    "new_device_id": new_device["device_id"],
                    "upgrade_date": upgrade_date_str,
                    "trade_in_value": round(trade_in_value, 2),
                    "contract_extension_months": contract_extension,
                    "promotion_applied": promotion_applied
                })
                
                upgrade_id += 1
    
    return upgrades

def generate_family_plans(customers: List[Dict]) -> List[Dict]:
    """Generate family plan records with realistic patterns."""
    family_plans = []
    family_plan_members = []
    family_plan_id = 1
    
    # Family plan adoption rates by segment
    segment_family_plan_rates = {
        "Premium": 0.15,   # 15% of Premium customers are primary on family plans
        "Standard": 0.1,   # 10% of Standard customers are primary on family plans
        "Budget": 0.05,    # 5% of Budget customers are primary on family plans
        "Business": 0.01,  # 1% of Business customers are primary on family plans (rare)
        "Family": 0.7      # 70% of Family segment customers are primary on family plans
    }
    
    # Age-based family plan propensity
    # Middle-aged customers more likely to have family plans
    age_multipliers = {
        (18, 25): 0.3,    # Young adults rarely primary on family plans
        (26, 35): 0.8,    # Young parents may have small family plans
        (36, 55): 1.5,    # Mid-life - very likely to have family plans
        (56, 80): 0.7     # Older adults less likely to have new family plans
    }
    
    # Plan names and sizes with realistic distribution
    family_plan_options = [
        {"name": "Family Share", "min_members": 2, "max_members": 4, "weight": 0.3},
        {"name": "Family Unlimited", "min_members": 2, "max_members": 6, "weight": 0.25},
        {"name": "Family Basic", "min_members": 2, "max_members": 3, "weight": 0.15},
        {"name": "Family Premium", "min_members": 3, "max_members": 6, "weight": 0.1},
        {"name": "Family Value", "min_members": 2, "max_members": 4, "weight": 0.15},
        {"name": "Family Elite", "min_members": 3, "max_members": 6, "weight": 0.05}
    ]
    
    # Create network of relationships
    # Start by identifying potential primary members
    potential_primaries = []
    for customer in customers:
        customer_id = customer["customer_id"]
        segment = customer["segment"]
        age = customer.get("age", 35)  # Default to 35 if age not available
        
        # Skip Alexis Smith - ensure she's not a primary
        if customer_id == 7:
            continue
            
        # Base likelihood from segment
        family_plan_rate = segment_family_plan_rates.get(segment, 0.1)
        
        # Adjust based on age
        age_bracket = next(
            (bracket for bracket in age_multipliers.keys() if bracket[0] <= age <= bracket[1]),
            (36, 55)  # Default to mid-life if no match
        )
        family_plan_rate *= age_multipliers[age_bracket]
        
        # Cap rate at 90%
        family_plan_rate = min(0.9, family_plan_rate)
        
        if random.random() < family_plan_rate:
            potential_primaries.append(customer)
    
    # Identify potential secondary/child members
    all_customer_ids = {c["customer_id"] for c in customers}
    members_assigned = set()  # Track already assigned members
    
    for primary in potential_primaries:
        primary_id = primary["customer_id"]
        
        # Skip if primary already assigned as a member
        if primary_id in members_assigned:
            continue
            
        # Select plan type based on weights
        plan_weights = [option["weight"] for option in family_plan_options]
        plan_option = random.choices(family_plan_options, weights=plan_weights)[0]
        
        plan_name = plan_option["name"]
        max_members = plan_option["max_members"]
        
        # Created date - correlate with customer creation
        if primary_id < len(customers) * 0.3:  # Oldest 30% of customers
            created_at = fake.date_time_between(start_date="-3y", end_date="-1y")
        elif primary_id < len(customers) * 0.7:  # Middle 40%
            created_at = fake.date_time_between(start_date="-2y", end_date="-6m")
        else:  # Newest 30%
            created_at = fake.date_time_between(start_date="-1y", end_date="-1m")
        
        # Shared data and pricing scales with max_members
        shared_data_gb = random.choice([max_members * 5, max_members * 10, max_members * 15])
        monthly_fee = 40 + (shared_data_gb * 0.5) + (max_members * 10)
        
        family_plans.append({
            "family_plan_id": family_plan_id,
            "primary_customer_id": primary_id,
            "plan_name": plan_name,
            "created_at": created_at.isoformat(),
            "max_members": max_members,
            "shared_data_gb": shared_data_gb,
            "monthly_fee": round(monthly_fee, 2)
        })
        
        # Add primary member
        family_plan_members.append({
            "family_plan_id": family_plan_id,
            "customer_id": primary_id,
            "role": "primary",
            "data_allocation_percentage": random.randint(20, 40)
        })
        
        members_assigned.add(primary_id)
        
        # Find other members based on matching characteristics
        # Focus on location and last name to simulate family relationships
        primary_location = (primary["country"], primary["state"], primary["city"])
        primary_last_name = primary["last_name"]
        
        # Potential family members are either:
        # 1. Same location AND same last name (immediate family)
        # 2. Same location only (extended family, roommates)
        # 3. Same last name only (family living elsewhere)
        # 4. Neither (friends, distant relatives)
        
        immediate_family = [
            c for c in customers
            if c["customer_id"] != primary_id and
            c["customer_id"] not in members_assigned and
            (c["country"], c["state"], c["city"]) == primary_location and
            c["last_name"] == primary_last_name
        ]
        
        extended_family_local = [
            c for c in customers
            if c["customer_id"] != primary_id and
            c["customer_id"] not in members_assigned and
            (c["country"], c["state"], c["city"]) == primary_location and
            c["last_name"] != primary_last_name
        ]
        
        extended_family_distant = [
            c for c in customers
            if c["customer_id"] != primary_id and
            c["customer_id"] not in members_assigned and
            (c["country"], c["state"], c["city"]) != primary_location and
            c["last_name"] == primary_last_name
        ]
        
        others = [
            c for c in customers
            if c["customer_id"] != primary_id and
            c["customer_id"] not in members_assigned and
            c not in immediate_family and
            c not in extended_family_local and
            c not in extended_family_distant
        ]
        
        # Determine number of additional members (1 to max_members-1)
        num_additional = random.randint(1, max_members-1)
        
        # Preference order for selecting members
        all_potential_members = (
            immediate_family +
            extended_family_local +
            extended_family_distant +
            random.sample(others, min(len(others), 10))  # Limit to 10 random others
        )
        
        # Select members
        selected_members = []
        for potential_member in all_potential_members:
            if len(selected_members) >= num_additional:
                break
                
            selected_members.append(potential_member)
            members_assigned.add(potential_member["customer_id"])
        
        # Add selected members to family plan
        for i, member in enumerate(selected_members):
            # Determine role based on relationship and age
            member_age = member.get("age", 35)
            
            if member["last_name"] == primary_last_name:
                # Family member
                if member_age >= 18:
                    # Adult family member
                    role = "secondary"
                else:
                    # Child
                    role = "child"
            else:
                # Non-family member on plan
                role = "secondary"
            
            # Data allocation (distribute remaining percentage after primary)
            primary_pct = next(
                m["data_allocation_percentage"] for m in family_plan_members 
                if m["family_plan_id"] == family_plan_id and m["role"] == "primary"
            )
            
            remaining_pct = 100 - primary_pct
            individual_pct = round(remaining_pct / len(selected_members))
            
            # Adjust for last member to ensure total is 100%
            if i == len(selected_members) - 1:
                total_so_far = primary_pct + sum(
                    m["data_allocation_percentage"] for m in family_plan_members
                    if m["family_plan_id"] == family_plan_id and m["role"] != "primary"
                )
                individual_pct = 100 - total_so_far
            
            family_plan_members.append({
                "family_plan_id": family_plan_id,
                "customer_id": member["customer_id"],
                "role": role,
                "data_allocation_percentage": individual_pct
            })
        
        family_plan_id += 1
    
    return family_plans, family_plan_members

def generate_loyalty_rewards(customers: List[Dict]) -> List[Dict]:
    """Generate customer loyalty rewards records with realistic patterns."""
    rewards = []
    reward_id = 1
    
    # Loyalty factors by segment
    segment_loyalty_factors = {
        "Premium": 1.3,    # Premium customers earn 30% more points
        "Standard": 1.0,   # Standard baseline
        "Budget": 0.7,     # Budget customers earn 30% fewer points
        "Business": 1.5,   # Business customers earn 50% more points
        "Family": 1.2      # Family customers earn 20% more points
    }
    
    # Redemption patterns by segment
    # How actively customers redeem their points
    segment_redemption_rates = {
        "Premium": 0.7,    # Premium customers redeem 70% of available points
        "Standard": 0.5,   # Standard redeem 50%
        "Budget": 0.8,     # Budget customers actively redeem 80% (value conscious)
        "Business": 0.4,   # Business customers redeem less - 40%
        "Family": 0.6      # Family customers redeem 60%
    }
    
    # Tier thresholds
    tier_thresholds = {
        "bronze": 0,
        "silver": 1000,
        "gold": 5000,
        "platinum": 15000
    }
    
    # Account age factor for points accumulation
    # Longer accounts have more time to accumulate points
    account_age_factors = {
        "new": 0.3,      # < 6 months
        "recent": 0.6,   # 6-12 months
        "established": 1.0, # 1-2 years
        "veteran": 1.5   # > 2 years
    }
    
    for customer in customers:
        customer_id = customer["customer_id"]
        segment = customer["segment"]
        
        # About 90% of customers participate in loyalty program
        if random.random() < 0.9:
            # Base points based on customer tenure
            # Using ID as a proxy for account age (lower IDs are older accounts)
            relative_id = customer_id / len(customers)
            
            if relative_id < 0.3:  # Oldest 30% of customers
                account_age = "veteran"
                base_points = random.randint(5000, 20000)
            elif relative_id < 0.6:  # Next 30%
                account_age = "established"
                base_points = random.randint(2000, 10000)
            elif relative_id < 0.9:  # Next 30%
                account_age = "recent"
                base_points = random.randint(500, 3000)
            else:  # Newest 10%
                account_age = "new"
                base_points = random.randint(100, 1000)
            
            # Adjust based on segment and account age
            loyalty_factor = segment_loyalty_factors.get(segment, 1.0)
            age_factor = account_age_factors.get(account_age, 1.0)
            
            # Also consider satisfaction - more satisfied customers are more active
            satisfaction = customer.get("satisfaction_score", 7)
            satisfaction_factor = 0.6 + (satisfaction / 10) * 0.8  # 0.6-1.4 range
            
            # Calculate points earned
            points_earned = int(base_points * loyalty_factor * age_factor * satisfaction_factor)
            
            # Calculate points redeemed based on redemption rate
            redemption_rate = segment_redemption_rates.get(segment, 0.5)
            # Add some randomness to redemption rate (±20%)
            adjusted_redemption_rate = max(0, min(1, redemption_rate * random.uniform(0.8, 1.2)))
            
            points_redeemed = int(points_earned * adjusted_redemption_rate)
            
            # Points balance
            points_balance = points_earned - points_redeemed
            
            # Last activity date - more active for higher tiers
            if points_balance >= tier_thresholds["platinum"]:
                # Platinum: Very active
                last_activity_date = fake.date_time_between(start_date="-1m", end_date="now")
            elif points_balance >= tier_thresholds["gold"]:
                # Gold: Quite active
                last_activity_date = fake.date_time_between(start_date="-3m", end_date="now")
            elif points_balance >= tier_thresholds["silver"]:
                # Silver: Moderately active
                last_activity_date = fake.date_time_between(start_date="-6m", end_date="now")
            else:
                # Bronze: Less active
                last_activity_date = fake.date_time_between(start_date="-1y", end_date="-1m")
                
            last_activity_date_str = last_activity_date.date().isoformat()
            
            # Determine tier based on points balance
            if points_balance >= tier_thresholds["platinum"]:
                tier = "platinum"
            elif points_balance >= tier_thresholds["gold"]:
                tier = "gold"
            elif points_balance >= tier_thresholds["silver"]:
                tier = "silver"
            else:
                tier = "bronze"
            
            rewards.append({
                "reward_id": reward_id,
                "customer_id": customer_id,
                "points_earned": points_earned,
                "points_redeemed": points_redeemed,
                "points_balance": points_balance,
                "last_activity_date": last_activity_date_str,
                "tier": tier
            })
            
            reward_id += 1
    
    return rewards

def generate_campaigns(num_campaigns: int) -> List[Dict]:
    """Generate marketing campaign records with realistic patterns."""
    campaigns = []
    
    # Campaign channels with realistic distribution
    channels = {
        "Email": 0.35,
        "SMS": 0.2,
        "Social Media": 0.15,
        "Display Ads": 0.1,
        "Search Ads": 0.1,
        "Direct Mail": 0.05,
        "TV": 0.03,
        "Radio": 0.02
    }
    
    # Customer segments with realistic campaign focus
    segments = {
        "All": 0.15,            # 15% target all customers
        "Premium": 0.2,         # 20% target premium
        "Standard": 0.15,       # 15% target standard
        "Budget": 0.1,          # 10% target budget
        "Business": 0.15,       # 15% target business
        "Family": 0.15,         # 15% target family
        "New Customers": 0.05,  # 5% target new customers
        "Churned": 0.05         # 5% target churned customers
    }
    
    # Seasonal patterns - campaigns more common at certain times
    # Current month as reference point
    current_date = datetime.datetime.now()
    current_month = current_date.month
    current_year = current_date.year
    
    # Define quarters
    quarters = {
        "Q1": [1, 2, 3],
        "Q2": [4, 5, 6],
        "Q3": [7, 8, 9],
        "Q4": [10, 11, 12]
    }
    
    # Find current quarter
    current_quarter = next(q for q, months in quarters.items() if current_month in months)
    
    # Campaign budget ranges by channel
    channel_budget_ranges = {
        "Email": (5000, 15000),
        "SMS": (7000, 20000),
        "Social Media": (15000, 50000),
        "Display Ads": (20000, 70000),
        "Search Ads": (15000, 60000),
        "Direct Mail": (30000, 100000),
        "TV": (50000, 200000),
        "Radio": (30000, 80000)
    }
    
    # Conversion rates by channel (realistic but varied)
    # These determine how actual conversions relate to goals
    channel_conversion_factors = {
        "Email": (0.8, 1.2),      # Email campaigns vary ±20% from goal
        "SMS": (0.7, 1.3),        # SMS campaigns vary ±30% from goal
        "Social Media": (0.6, 1.4), # Social varies ±40% from goal
        "Display Ads": (0.5, 1.3),  # Display ads vary -50% to +30%
        "Search Ads": (0.9, 1.5),   # Search ads vary -10% to +50%
        "Direct Mail": (0.7, 1.1),  # Direct mail varies -30% to +10%
        "TV": (0.6, 1.3),           # TV varies -40% to +30%
        "Radio": (0.5, 1.2)         # Radio varies -50% to +20%
    }
    
    # Offer types by segment
    segment_offer_preferences = {
        "Premium": [
            "Free premium service for 3 months",
            "Double data for 6 months",
            "Free international calling for 3 months",
            "Free device upgrade with renewal"
        ],
        "Budget": [
            "20% off for 3 months",
            "$100 bill credit",
            "Waived activation fee",
            "Buy one line, get one free"
        ],
        "Business": [
            "Free premium service for business accounts",
            "Multi-line discount bundle",
            "Free enterprise features for 6 months",
            "$200 account credit with new line"
        ],
        "Family": [
            "Add a line for $10/month",
            "Family plan upgrade discount",
            "Free tablets for kids with new family plan",
            "50% off additional lines"
        ],
        "All": [
            "20% off for 3 months",
            "Waived activation fee",
            "$100 bill credit",
            "Double data for 6 months"
        ],
        "New Customers": [
            "Waived activation fee",
            "First month free",
            "Free device with new line",
            "$150 welcome credit"
        ],
        "Churned": [
            "50% off for 6 months if you return",
            "$200 win-back credit",
            "Premium features at standard price",
            "Waived fees and free first month"
        ],
        "Standard": [
            "Free device with new line",
            "25% off for 3 months",
            "Double data for 3 months",
            "$75 bill credit"
        ]
    }
    
    # Campaign duration patterns
    duration_patterns = {
        "short": (14, 30),    # 2-4 weeks
        "medium": (30, 60),   # 1-2 months
        "long": (60, 90)      # 2-3 months
    }
    
    # Create campaigns
    for i in range(1, num_campaigns + 1):
        # Select channel based on distribution
        channel = random.choices(
            list(channels.keys()),
            weights=list(channels.values())
        )[0]
        
        # Select target segment based on distribution
        target_segment = random.choices(
            list(segments.keys()),
            weights=list(segments.values())
        )[0]
        
        # Set budget based on channel
        budget_range = channel_budget_ranges.get(channel, (5000, 100000))
        budget = random.randint(*budget_range)
        
        # Calculate conversion goal BEFORE timing sections
        # Higher budget = higher goals
        base_conversion_goal = int(budget / random.uniform(50, 150))
        
        # Adjust based on channel effectiveness
        if channel in ["Email", "SMS"]:
            # High volume channels
            conversion_goal = base_conversion_goal * random.uniform(1.5, 2.5)
        elif channel in ["Social Media", "Search Ads"]:
            # Medium volume channels
            conversion_goal = base_conversion_goal * random.uniform(1.0, 2.0)
        else:
            # Lower volume channels
            conversion_goal = base_conversion_goal * random.uniform(0.5, 1.5)
            
        conversion_goal = int(conversion_goal)
        
        # Campaign timing - weight toward recent and current campaigns
        timing_random = random.random()
        
        if timing_random < 0.3:  # 30% active campaigns
            # Active campaign - started recently, still running
            start_date = fake.date_time_between(start_date="-1m", end_date="now")
            duration_type = random.choices(
                ["short", "medium", "long"],
                weights=[0.3, 0.5, 0.2]
            )[0]
            duration_days = random.randint(*duration_patterns[duration_type])
            end_date = start_date + datetime.timedelta(days=duration_days)
            
            # If end date is in the future, keep it as None in database terms
            if end_date > current_date:
                end_date_str = None
            else:
                end_date_str = end_date.date().isoformat()
                
            # No actual conversions yet for active campaigns
            actual_conversions = None
        elif timing_random < 0.7:  # 40% recent completed campaigns
            # Recently completed campaign
            end_date = fake.date_time_between(start_date="-2m", end_date="-1d")
            duration_type = random.choices(
                ["short", "medium", "long"],
                weights=[0.3, 0.5, 0.2]
            )[0]
            duration_days = random.randint(*duration_patterns[duration_type])
            start_date = end_date - datetime.timedelta(days=duration_days)
            
            end_date_str = end_date.date().isoformat()
            
            # Has actual conversions
            conversion_min, conversion_max = channel_conversion_factors.get(channel, (0.7, 1.3))
            goal_achievement = random.uniform(conversion_min, conversion_max)
            actual_conversions = int(conversion_goal * goal_achievement)
        else:  # 30% older campaigns
            # Older campaign
            end_date = fake.date_time_between(start_date="-1y", end_date="-2m")
            duration_type = random.choices(
                ["short", "medium", "long"],
                weights=[0.3, 0.5, 0.2]
            )[0]
            duration_days = random.randint(*duration_patterns[duration_type])
            start_date = end_date - datetime.timedelta(days=duration_days)
            
            end_date_str = end_date.date().isoformat()
            
            # Has actual conversions
            conversion_min, conversion_max = channel_conversion_factors.get(channel, (0.7, 1.3))
            goal_achievement = random.uniform(conversion_min, conversion_max)
            actual_conversions = int(conversion_goal * goal_achievement)
        
        # Create campaign name with quarter and year
        campaign_date = start_date
        campaign_year = campaign_date.year
        campaign_month = campaign_date.month
        
        # Find campaign quarter
        campaign_quarter = next(q for q, months in quarters.items() if campaign_month in months)
        
        # Generate random campaign name component
        name_adjectives = ["Summer", "Spring", "Winter", "Fall", "Holiday", "Special", 
                          "Limited", "Exclusive", "Premium", "Value", "Super", "Mega"]
        name_nouns = ["Deal", "Offer", "Promotion", "Campaign", "Special", "Discount", 
                     "Bundle", "Package", "Sale", "Event"]
        
        # For seasonal campaigns, align adjective with season
        if campaign_month in [12, 1, 2]:  # Winter
            season = "Winter"
        elif campaign_month in [3, 4, 5]:  # Spring
            season = "Spring"
        elif campaign_month in [6, 7, 8]:  # Summer
            season = "Summer"
        else:  # Fall
            season = "Fall"
            
        if random.random() < 0.3:  # 30% chance of seasonal name
            name_component = f"{season} {random.choice(name_nouns)}"
        else:
            name_component = f"{random.choice(name_adjectives)} {random.choice(name_nouns)}"
        
        campaign_name = f"{name_component} {campaign_quarter} {campaign_year}"
        
        # Select offer based on segment
        if target_segment in segment_offer_preferences:
            offer_details = random.choice(segment_offer_preferences[target_segment])
        else:
            offer_details = random.choice(segment_offer_preferences["All"])
        
        campaigns.append({
            "campaign_id": i,
            "campaign_name": campaign_name,
            "start_date": start_date.date().isoformat(),
            "end_date": end_date_str,
            "target_segment": target_segment,
            "channel": channel,
            "offer_details": offer_details,
            "budget": budget,
            "conversion_goal": conversion_goal,
            "actual_conversions": actual_conversions
        })
    
    return campaigns

def generate_feedback(customers: List[Dict]) -> List[Dict]:
    """Generate customer feedback records with realistic patterns."""
    feedback_records = []
    feedback_id = 1
    
    # Feedback categories with realistic distribution
    categories = {
        "Service Quality": 0.25,      # 25% of feedback about service quality
        "Network Coverage": 0.2,      # 20% about network coverage
        "Customer Support": 0.2,      # 20% about customer support
        "Billing": 0.15,              # 15% about billing
        "Device": 0.1,                # 10% about device issues
        "Plan Features": 0.07,        # 7% about plan features
        "Website/App": 0.03           # 3% about website/app
    }
    
    # Category preferences by segment - what each segment cares about most
    segment_category_preferences = {
        "Premium": {
            "Service Quality": 0.3,
            "Network Coverage": 0.25,
            "Customer Support": 0.2,
            "Device": 0.15,
            "Plan Features": 0.05,
            "Billing": 0.03,
            "Website/App": 0.02
        },
        "Budget": {
            "Billing": 0.35,
            "Network Coverage": 0.2,
            "Service Quality": 0.15,
            "Customer Support": 0.15,
            "Plan Features": 0.1,
            "Device": 0.03,
            "Website/App": 0.02
        },
        "Business": {
            "Service Quality": 0.3,
            "Network Coverage": 0.25,
            "Customer Support": 0.2,
            "Billing": 0.1,
            "Plan Features": 0.1,
            "Device": 0.03,
            "Website/App": 0.02
        },
        "Family": {
            "Network Coverage": 0.25,
            "Service Quality": 0.2,
            "Plan Features": 0.2,
            "Billing": 0.15,
            "Customer Support": 0.1,
            "Device": 0.05,
            "Website/App": 0.05
        }
    }
    
    # Feedback frequency based on satisfaction
    # Lower satisfaction customers give more feedback
    satisfaction_feedback_rates = {
        (1, 3): 0.7,    # 70% of very dissatisfied customers (1-3) give feedback
        (4, 6): 0.4,    # 40% of neutral customers (4-6) give feedback
        (7, 8): 0.25,   # 25% of satisfied customers (7-8) give feedback
        (9, 10): 0.15   # 15% of very satisfied customers (9-10) give feedback
    }
    
    # Feedback count by satisfaction level
    # Unhappy customers tend to give more feedback
    feedback_count_by_satisfaction = {
        (1, 3): {1: 0.4, 2: 0.4, 3: 0.2},   # Unhappy customers often give multiple feedback
        (4, 6): {1: 0.7, 2: 0.2, 3: 0.1},
        (7, 10): {1: 0.9, 2: 0.09, 3: 0.01} # Happy customers rarely give multiple feedback
    }
    
    # Detailed comments by category and sentiment
    detailed_comments = {
        "Service Quality": {
            "positive": [
                "Consistently reliable service with no interruptions.",
                "Excellent quality and reliability across all services.",
                "Service quality has been exceptional throughout my contract.",
                "Very stable service, even during peak usage times.",
                "The service quality exceeds my expectations consistently."
            ],
            "neutral": [
                "Service quality is acceptable but occasionally drops.",
                "Generally reliable service with occasional hiccups.",
                "Service meets basic expectations but nothing special.",
                "Some minor issues with service but generally acceptable.",
                "Service quality is adequate but could be improved."
            ],
            "negative": [
                "Frequent service interruptions are frustrating.",
                "Service quality is below industry standards.",
                "Persistent issues with call drops and data speeds.",
                "Poor service quality compared to what was promised.",
                "Recurring outages and slowdowns make this service unreliable."
            ]
        },
        "Network Coverage": {
            "positive": [
                "Excellent coverage even in remote areas.",
                "Never experienced dead zones in my regular areas.",
                "Coverage is significantly better than my previous carrier.",
                "Strong signal throughout my entire commute route.",
                "Impressive coverage in buildings and underground locations."
            ],
            "neutral": [
                "Coverage is generally good in urban areas but spotty elsewhere.",
                "Acceptable coverage in most places, with a few dead zones.",
                "Coverage meets expectations but nothing exceptional.",
                "Some weak spots in coverage but generally serviceable.",
                "Coverage could be improved in certain areas but works for basic needs."
            ],
            "negative": [
                "Poor coverage in many areas I frequently visit.",
                "Significant dead zones even in urban settings.",
                "Coverage map is misleading and overstates actual coverage.",
                "Constant signal drops during travel.",
                "Coverage is much worse than competing carriers in my area."
            ]
        },
        "Customer Support": {
            "positive": [
                "Support team was knowledgeable and resolved my issue quickly.",
                "Customer service rep went above and beyond to help me.",
                "Very impressed with the quick response and effective resolution.",
                "Support staff was patient and thorough in addressing my concerns.",
                "Excellent troubleshooting experience with the support team."
            ],
            "neutral": [
                "Support was adequate but took longer than expected.",
                "Rep was friendly but had to escalate to resolve my issue.",
                "Customer service was professional but solution was only temporary.",
                "Average support experience - not bad but not exceptional.",
                "Support got the job done, though it required multiple calls."
            ],
            "negative": [
                "Support representatives gave contradictory information.",
                "Extremely long wait times for basic customer service.",
                "Issue remains unresolved after multiple support contacts.",
                "Support staff seemed poorly trained and uninformed.",
                "Frustrating experience trying to get help with a simple issue."
            ]
        },
        "Billing": {
            "positive": [
                "Billing is always accurate and easy to understand.",
                "No surprises on my bill, exactly as agreed upon.",
                "The itemized billing makes it easy to track my usage.",
                "Appreciate the consistent and transparent billing practices.",
                "Autopay system works flawlessly every month."
            ],
            "neutral": [
                "Billing is generally accurate but statements are confusing.",
                "Occasional small discrepancies that get resolved.",
                "Bills are mostly correct but the format could be clearer.",
                "No major billing issues but had questions about some charges.",
                "Billing works but the online system could be more user-friendly."
            ],
            "negative": [
                "Consistently inaccurate bills requiring regular calls to fix.",
                "Hidden fees and charges not disclosed during sign-up.",
                "Billed for services I never ordered or received.",
                "Rates increased without proper notification.",
                "Extremely frustrating billing errors every month."
            ]
        },
        "Device": {
            "positive": [
                "Device performs exceptionally well with the network.",
                "Very satisfied with the recommended device's quality and features.",
                "Device has excellent battery life and performance on this network.",
                "The upgrade process was smooth and the new device works perfectly.",
                "Device integration with carrier services is seamless."
            ],
            "neutral": [
                "Device works as expected, no major issues.",
                "Acceptable performance but battery drains faster than expected.",
                "Device meets basic needs but has minor compatibility issues.",
                "Neither impressed nor disappointed with the device performance.",
                "Device is adequate but doesn't stand out in any way."
            ],
            "negative": [
                "Device frequently loses connection to the network.",
                "Severe performance issues with carrier-provided device.",
                "Device has compatibility problems with promised features.",
                "Constantly having to restart device to maintain connectivity.",
                "Device quality falls far below the premium price paid."
            ]
        },
        "Plan Features": {
            "positive": [
                "Plan includes all the features I need at a great value.",
                "The unlimited data feature truly has no hidden restrictions.",
                "International roaming feature saved me significant money.",
                "Family sharing features are intuitive and easy to manage.",
                "The bonus features exceeded what competing carriers offer."
            ],
            "neutral": [
                "Plan features are adequate but could offer more value.",
                "Basic features work well but premium features aren't worth the cost.",
                "Plan meets essential needs but lacks some conveniences.",
                "Features are as advertised but nothing exceptional.",
                "Acceptable feature set but some limitations compared to competitors."
            ],
            "negative": [
                "Plan features are misleading and include significant restrictions.",
                "Missing key features that were promised during sign-up.",
                "Features don't work as advertised, especially data throttling.",
                "Poor value compared to competitor plans with similar features.",
                "Essential features require additional fees not initially disclosed."
            ]
        },
        "Website/App": {
            "positive": [
                "The app makes account management incredibly easy.",
                "Website is intuitive and provides all the information I need.",
                "Online bill pay and account management tools are excellent.",
                "App notifications about usage and billing are timely and helpful.",
                "The self-service options in the app save me time and hassle."
            ],
            "neutral": [
                "Website functions adequately but has an outdated interface.",
                "App works for basic tasks but occasionally crashes.",
                "Online account management is functional but not intuitive.",
                "Can accomplish most tasks online but some still require a call.",
                "Website/app meet basic needs but could use improvements."
            ],
            "negative": [
                "App constantly crashes when trying to view or pay bills.",
                "Website is confusing and important features are hard to find.",
                "Significant bugs in the account management portal.",
                "App shows incorrect account information and usage data.",
                "Online chat support in the app/website is practically useless."
            ]
        }
    }
    
    # Track which customers have already given feedback in which categories
    customer_feedback_categories = {}
    
    for customer in customers:
        customer_id = customer["customer_id"]
        segment = customer["segment"]
        satisfaction = customer.get("satisfaction_score", 7)  # Default to 7 if missing
        
        # Initialize tracking for this customer
        if customer_id not in customer_feedback_categories:
            customer_feedback_categories[customer_id] = set()
        
        # Determine if customer gives feedback based on satisfaction
        feedback_rate = next(
            (rate for sat_range, rate in satisfaction_feedback_rates.items() 
             if sat_range[0] <= satisfaction <= sat_range[1]),
            0.3  # Default to 30% if no range matches
        )
        
        gives_feedback = random.random() < feedback_rate
        
        if gives_feedback:
            # Determine number of feedback entries based on satisfaction
            sat_bracket = next(
                bracket for bracket in feedback_count_by_satisfaction.keys()
                if bracket[0] <= satisfaction <= bracket[1]
            )
            count_weights = feedback_count_by_satisfaction[sat_bracket]
            
            num_feedback = random.choices(
                list(count_weights.keys()),
                weights=list(count_weights.values())
            )[0]
            
            # Get category preferences for this segment
            category_prefs = segment_category_preferences.get(
                segment, 
                categories  # Default to general distribution if segment not specified
            )
            
            for _ in range(num_feedback):
                # Ensure we don't have duplicate categories for the same customer
                available_categories = [
                    cat for cat in category_prefs.keys()
                    if cat not in customer_feedback_categories[customer_id]
                ]
                
                if not available_categories:
                    break  # No more unused categories
                    
                # Select category based on segment preferences
                category_weights = {
                    cat: weight for cat, weight in category_prefs.items()
                    if cat in available_categories
                }
                
                if not category_weights:
                    break
                    
                category = random.choices(
                    list(category_weights.keys()),
                    weights=list(category_weights.values())
                )[0]
                
                # Mark this category as used for this customer
                customer_feedback_categories[customer_id].add(category)
                
                # Generate feedback date - more recent for unhappy customers
                if satisfaction <= 4:
                    # Very unhappy customers - recent feedback
                    feedback_date = fake.date_time_between(start_date="-3m", end_date="-1d")
                elif satisfaction <= 7:
                    # Somewhat satisfied - medium timeframe
                    feedback_date = fake.date_time_between(start_date="-6m", end_date="-1d")
                else:
                    # Happy customers - any time in past year
                    feedback_date = fake.date_time_between(start_date="-1y", end_date="-1d")
                
                # Rating correlates strongly with overall satisfaction but varies by category
                # Premium customers have higher standards for service quality and network
                if segment == "Premium" and category in ["Service Quality", "Network Coverage"]:
                    # Premium customers are more critical of core services
                    rating_offset = random.uniform(-2, 1)
                elif segment == "Budget" and category == "Billing":
                    # Budget customers are very sensitive to billing issues
                    rating_offset = random.uniform(-3, 0)
                else:
                    # Normal variation
                    rating_offset = random.uniform(-1.5, 1.5)
                    
                # Final rating calculation
                rating = max(1, min(10, round(satisfaction + rating_offset)))
                
                # Determine sentiment for comments
                if rating >= 8:
                    sentiment = "positive"
                    requires_followup = False  # Happy customers rarely need followup
                elif rating >= 5:
                    sentiment = "neutral"
                    requires_followup = random.random() < 0.3  # 30% chance of followup
                else:
                    sentiment = "negative"
                    requires_followup = random.random() < 0.8  # 80% chance of followup
                
                # Select comment based on category and sentiment
                if category in detailed_comments and sentiment in detailed_comments[category]:
                    comments = random.choice(detailed_comments[category][sentiment])
                else:
                    # Fallback generic comments
                    if sentiment == "positive":
                        comments = f"Very satisfied with the {category.lower()}."
                    elif sentiment == "neutral":
                        comments = f"Generally acceptable {category.lower()}, but could be improved."
                    else:
                        comments = f"Disappointed with the {category.lower()}."
                
                # Followup details
                if requires_followup:
                    # Higher ratings get faster followup
                    followup_probability = 0.5 + (rating / 20)  # 0.55 to 1.0
                    
                    if random.random() < followup_probability:  # Followup completed
                        # Time to followup correlates with rating - lower ratings get faster response
                        if rating <= 3:
                            # Urgent issues - quick followup (1-3 days)
                            days_to_followup = random.randint(1, 3)
                        elif rating <= 6:
                            # Medium priority - moderate followup (2-5 days)
                            days_to_followup = random.randint(2, 5)
                        else:
                            # Low priority - longer followup (3-7 days)
                            days_to_followup = random.randint(3, 7)
                            
                        followup_date = feedback_date + datetime.timedelta(days=days_to_followup)
                        
                        # Followup notes based on category
                        if category == "Service Quality":
                            followup_notes = random.choice([
                                "Technician dispatched to investigate service issues.",
                                "Network team confirmed and resolved service interruption.",
                                "Provided service credits and confirmed resolution.",
                                "Conducted line test and optimized connection."
                            ])
                        elif category == "Network Coverage":
                            followup_notes = random.choice([
                                "Verified coverage in customer's area and identified improvement plan.",
                                "Provided signal booster options for improved coverage.",
                                "Confirmed recent network upgrade in customer's location.",
                                "Added location to priority list for coverage enhancement."
                            ])
                        elif category == "Billing":
                            followup_notes = random.choice([
                                "Billing discrepancy identified and corrected.",
                                "Applied appropriate credits to account.",
                                "Explained billing details and resolved misunderstanding.",
                                "Updated billing preferences and payment method."
                            ])
                        else:
                            followup_notes = random.choice([
                                "Customer contacted and issues addressed.",
                                "Provided technical support and resolution steps.",
                                "Escalated to supervisor who resolved customer concern.",
                                "Offered compensation and additional support options."
                            ])
                    else:
                        followup_date = None
                        followup_notes = random.choice([
                            "Pending followup - scheduled for next available agent",
                            "In queue for specialist review",
                            "Awaiting customer availability for callback",
                            "Scheduled for followup within 48 hours"
                        ])
                else:
                    followup_date = None
                    followup_notes = None
                
                feedback_records.append({
                    "feedback_id": feedback_id,
                    "customer_id": customer_id,
                    "feedback_date": feedback_date.isoformat(),
                    "category": category,
                    "rating": rating,
                    "comments": comments,
                    "requires_followup": requires_followup,
                    "followup_notes": followup_notes,
                    "followup_date": followup_date.isoformat() if followup_date else None
                })
                
                feedback_id += 1
    
    return feedback_records