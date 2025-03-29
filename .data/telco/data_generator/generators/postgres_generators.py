"""
PostgreSQL Data Generators

This module contains functions to generate data for PostgreSQL tables in the telco schema.
"""

import random
import uuid
import datetime
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

def generate_phone_number() -> str:
    """Generate a realistic phone number."""
    return f"+{random.randint(1, 9)}{random.randint(10, 99)}{random.randint(1000000, 9999999)}"

def generate_cell_number() -> str:
    """Generate a cell number (last 10 digits of phone number)."""
    return f"{random.randint(1000000000, 9999999999)}"

def fake_email():
    """
    Generate a random email that's suitable for large unique datasets
    """
    # Get random username from faker but add randomness for uniqueness
    username = fake.user_name() + str(random.randint(1, 999999))
    
    # Get random domain from a large variety of options
    domains = [
        "gmail.com", "gmail.com", "gmail.com", "gmail.com", "gmail.com",
        "yahoo.com", "yahoo.com", "yahoo.com",
        "outlook.com", "outlook.com", "outlook.com",
        "hotmail.com", "hotmail.com",
        "icloud.com", "icloud.com",
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
            email = "alexis.smith@gmail.com"
            role = "customer"
        else:
            email = fake_email()
            role = "customer" if i <= num_customers - 5 else "support"
            
        # Using a fixed password hash for simplicity
        password_hash = "$2a$10$DSRHAPZP0fuEFioGOPOdW.kgFWZvQgmMihaBYsUs8rO4cdHFFK7cS"
        
        users.append({
            "id": i,
            "email": email,
            "password": password_hash,
            "roles": role,
            "created_at": fake.date_time_between(start_date="-3y", end_date="now").isoformat(),
            "updated_at": fake.date_time_between(start_date="-1y", end_date="now").isoformat()
        })
    return users

def generate_customers(auth_users: List[Dict]) -> List[Dict]:
    """Generate customer data."""
    customers = []
    for i, user in enumerate(auth_users, 1):
        # Special case for customer ID 7 - Alexis Smith
        if i == 7:
            first_name = "Alexis"
            last_name = "Smith"
            country = "United States"
            state = "California"
            segment = "Premium"  # Tech savvy user would likely be on a premium plan
            satisfaction_score = 9  # High satisfaction
            churn_risk = 0.05  # Low churn risk
            churn_risk_factors = None  # No risk factors
        else:
            first_name = fake.first_name()
            last_name = fake.last_name()
            country = random.choice(list(COUNTRIES.keys()))
            state = random.choice(COUNTRIES[country])
            segment = random.choice(CUSTOMER_SEGMENTS)
            
            # Generate satisfaction score (1-10)
            satisfaction_score = random.randint(1, 10)
            
            # Generate churn risk (0-1)
            # Higher satisfaction = lower churn risk
            base_churn_risk = 1.0 - (satisfaction_score / 10.0)
            # Add some randomness
            churn_risk = round(max(0.0, min(1.0, base_churn_risk + random.uniform(-0.2, 0.2))), 2)
            
            # Generate churn risk factors for high-risk customers
            if churn_risk > 0.6:
                num_factors = random.randint(1, 3)
                factors = random.sample([
                    "Price sensitivity",
                    "Service quality issues",
                    "Competitor offers",
                    "Moving location",
                    "Network coverage",
                    "Customer service experience",
                    "Device upgrade needs",
                    "Contract ending soon"
                ], num_factors)
                churn_risk_factors = "{" + ",".join(factors) + "}"
            else:
                churn_risk_factors = None
            
        image = f"avatar_{random.randint(1, 20)}.jpg"
        
        # Generate last survey date (within last 6 months)
        last_survey_date = fake.date_time_between(start_date="-6m", end_date="now").date() if random.random() < 0.7 else None
        
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
            "image": image,
            "segment": segment,
            "auth_user_id": user["id"],
            "satisfaction_score": satisfaction_score,
            "last_survey_date": last_survey_date.isoformat() if last_survey_date else None,
            "churn_risk": churn_risk,
            "churn_risk_factors": churn_risk_factors
        })
    return customers

def generate_plans(num_plans: int) -> List[Dict]:
    """Generate plan data with increased randomness to avoid clashes."""
    plans = []
    
    # More varied name components
    PREFIXES = {
        "Mobile": [
            'Basic', 'Standard', 'Premium', 'Ultimate', 'Essential', 'Freedom', 
            'Value', 'Smart', 'Elite', 'Flex', 'Max', 'Power', 'Select', 'Prime',
            'Everyday', 'Connect', 'Go', 'Lite', 'Advance', 'Pro',
            'Swift', 'Rapid', 'Quick', 'Express', 'Direct', 'Simple', 'Easy',
            'Complete', 'Total', 'Active', 'Dynamic', 'Agile', 'Mobile', 'Personal',
            'Traveler', 'Explorer', 'Journey', 'Adventure', 'Liberty', 'Freedom+',
            'Core', 'Student', 'Youth', 'Senior', 'Family', 'Business', 'Executive',
            'Community', 'National', 'Global', 'Signature', 'Custom', 'Flex+'
        ],
        
        "Internet": [
            '', 'High-Speed ', 'Ultra ', 'Fiber ', 'Premium ', 'Turbo ',
            'Fast ', 'Broadband ', 'Streaming ', 'Home ',
            'Lightning ', 'Gigabit ', 'Express ', 'Quick ', 'Rapid ', 'Flash ',
            'Mega ', 'Super ', 'Hyper ', 'Quantum ', 'Optical ', 'Digital ', 
            'Connected ', 'Smart ', 'Office ', 'Pro ', 'Business ', 'Gaming ',
            'Streaming+ ', 'HD ', '4K ', 'Unlimited ', 'Advanced ', 'NextGen ',
            'Future ', 'Modern ', 'Tech ', 'Cloud ', 'Speed ', 'Performance '
        ],
        
        "Bundle": [
            'Home & Mobile', 'Complete', 'Family', 'All-in-One', 'Ultimate', 
            'Total', 'Full-Service', 'Connected Home', 'Smart Home', 'Digital',
            'Fusion', 'Combo', 'Joint', 'Dual', 'Twin', 'Multi', 'Triple',
            'Quad', 'Combined', 'Integrated', 'United', 'Packaged', 'Bundled',
            'Comprehensive', 'Full', 'Whole-Home', 'Household', 'Home-Office',
            'Lifestyle', 'Converged', 'Unified', 'Power', 'Essential', 'Value',
            'Premium', 'Deluxe', 'Executive', 'Elite', 'Signature', 'Custom',
            'Family+', 'Home Complete', 'Advantage', 'Connected+'
        ],
        
        "IoT": [
            'IoT', 'Smart Device', 'Connected', 'Device', 'Smart', 'Sensor',
            'Tracker', 'Remote', 'Monitoring',
            'Machine', 'Network', 'Link', 'Grid', 'Web', 'Mesh', 'Cloud',
            'Auto', 'Intelligent', 'Connected+', 'Smart+', 'Things', 'Object',
            'Device+', 'Industrial', 'Home', 'Business', 'Enterprise', 'City',
            'Urban', 'Rural', 'Field', 'Tracker+', 'Control', 'Command',
            'Automation', 'Automated', 'Responsive', 'Adaptive', 'DataPoint',
            'Measure', 'Sense', 'Beacon', 'Signal', 'Transmit'
        ],
        
        "Enterprise": [
            'Business', 'Corporate', 'Enterprise', 'Commercial', 'Professional',
            'Office', 'Workforce', 'Operations', 'Executive', 'Team',
            'Company', 'Organization', 'Institutional', 'Industrial', 'Firm',
            'Group', 'Agency', 'Bureau', 'Division', 'Department', 'Corporate+',
            'Enterprise+', 'Global', 'International', 'National', 'Regional',
            'Local', 'Industry', 'Sector', 'Market', 'Commerce', 'Trade',
            'Wholesale', 'Retail', 'B2B', 'SME', 'Scale-Up', 'Startup',
            'MNC', 'Conglomerate', 'Solution', 'Performance', 'Productivity',
            'Efficiency', 'Capacity', 'Managed', 'Dedicated', 'Premium'
        ]
    }
    
    for i in range(1, num_plans + 1):
        plan_type = random.choice(PLAN_TYPES)
        
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
            # More varied data options
            data_options = [1, 2, 3, 5, 8, 10, 15, 20, 25, 30, 40, 50, None]
            data_gb = random.choice(data_options)
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
                # Progressive pricing based on data amount
                if data_gb <= 5:
                    base_fee = 15 + (data_gb * 2.5)
                elif data_gb <= 20:
                    base_fee = 25 + (data_gb * 1.2)
                else:
                    base_fee = 45 + (data_gb * 0.5)
            
            fee = round(base_fee * pricing_variation, 2)
            
            # Set mobile-specific fields with more variation
            data_limit_gb = data_gb
            voice_limit_minutes = random.choice([500, 750, 1000, 1500, 2000, 3000, None])
            sms_limit = random.choice([500, 1000, 1500, 2000, None])
            
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
            roaming_probability = 0.3 if is_premium else 0.15
            international_roaming = random.random() < roaming_probability
            
            if international_roaming:
                # More variation in country counts
                all_countries = list(COUNTRIES.keys())
                max_countries = min(len(all_countries), random.randint(3, 10))
                num_countries = random.randint(1, max_countries)
                countries_sample = random.sample(all_countries, num_countries)
                roaming_countries = "{" + ",".join(country for country in countries_sample) + "}"
                
                # More varied roaming data and voice
                roaming_data_gb = round(random.uniform(0.5, 10.0), 2)
                roaming_voice_minutes = random.randint(30, 600)
                
                # Increase fee for roaming
                fee += num_countries * 1.5
                fee += roaming_data_gb * 2
                
        elif plan_type == "Internet":
            # More varied speeds
            speed = random.choice([25, 50, 75, 100, 200, 300, 500, 750, 1000])
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
            
            # Set internet-specific fields with more variation
            data_options = [500, 750, 1000, 1500, 2000, None]
            # Higher speeds more likely to have unlimited data
            if speed >= 500 and random.random() < 0.7:
                data_limit_gb = None
            else:
                data_limit_gb = random.choice(data_options)
                
            if data_limit_gb is not None:
                description += f" and {data_limit_gb}GB data limit"
            else:
                description += " with unlimited data"
                # Premium for unlimited
                fee += random.uniform(10, 15)
            
        elif plan_type == "Bundle":
            # More varied bundle sizes
            sizes = ['XS', 'S', 'M', 'L', 'XL', 'XXL']
            size = random.choice(sizes)
            size_index = sizes.index(size)
            
            prefix = random.choice(PREFIXES["Bundle"])
            name = f"{prefix} Bundle {size}"
            description = "Combined home internet and mobile service"
            
            # More varied pricing based on size
            base_fee = 60 + (size_index * 10)
            fee = round(base_fee * pricing_variation, 2)
            
            # Set bundle-specific fields with size-dependent variation
            data_options = [100, 200, 300, 500, 750, None]
            if size_index >= 3:  # L, XL, XXL
                data_limit_gb = random.choice(data_options[3:])  # More data for larger plans
                voice_limit_minutes = random.choice([2000, 3000, 5000, None])
                sms_limit = random.choice([2000, 5000, None])
            else:  # XS, S, M
                data_limit_gb = random.choice(data_options[:4])  # Less data for smaller plans
                voice_limit_minutes = random.choice([500, 1000, 1500, 2000])
                sms_limit = random.choice([500, 1000, 2000])
            
            # Add feature details to description
            description += f" with {data_limit_gb}GB data" if data_limit_gb else " with unlimited data"
            
            # Bundles more likely to have roaming based on size
            roaming_probability = 0.2 + (size_index * 0.1)
            international_roaming = random.random() < roaming_probability
            
            if international_roaming:
                all_countries = list(COUNTRIES.keys())
                max_countries = min(len(all_countries), 3 + size_index * 2)
                num_countries = random.randint(2, max_countries)
                countries_sample = random.sample(all_countries, num_countries)
                roaming_countries = "{" + ",".join(country for country in countries_sample) + "}"
                roaming_data_gb = round(random.uniform(1.0, 5.0) * (1 + size_index * 0.5), 2)
                roaming_voice_minutes = random.randint(60, 300) * (1 + size_index // 2)
                
                # Increase fee for roaming
                fee += num_countries * 2
                
        elif plan_type == "IoT":
            # More varied tiers with descriptive names
            tiers = [('Basic', 1), ('Plus', 3), ('Pro', 5), ('Advanced', 10), 
                    ('Premium', 20), ('Enterprise', 50)]
            tier_name, devices = random.choice(tiers)
            
            prefix = random.choice(PREFIXES["IoT"])
            
            # More varied naming patterns
            name_pattern = random.randint(0, 2)
            if name_pattern == 0:
                name = f"{prefix} Connect {tier_name}"
            elif name_pattern == 1:
                name = f"{tier_name} {prefix} Plan"
            else:
                name = f"{prefix} {tier_name} {devices}-Device"
                
            description = f"Connectivity for {devices} IoT devices"
            
            # More varied pricing based on devices and tier
            base_fee = 5 + (devices * 0.8)
            fee = round(base_fee * pricing_variation, 2)
            
            # Set IoT-specific fields
            data_limit_gb = 1
            description += f" with {data_limit_gb}GB data"
            
        else:  # Enterprise
            # More varied enterprise sizes
            sizes = ['Starter', 'Small', 'Medium', 'Large', 'Corporate', 'Global']
            size = random.choice(sizes)
            size_index = sizes.index(size)
            
            prefix = random.choice(PREFIXES["Enterprise"])
            
            # More varied naming patterns
            name_pattern = random.randint(0, 2)
            if name_pattern == 0:
                name = f"{prefix} {size} Plan"
            elif name_pattern == 1:
                name = f"{size} {prefix} Solution"
            else:
                name = f"{prefix} {random.choice(['Professional', 'Complete', 'Connected', 'Premium'])} {size}"
                
            description = f"Enterprise connectivity solution for {size.lower()} businesses"
            
            # More varied pricing based on size
            base_fee = 80 + (size_index * 30)
            fee = round(base_fee * pricing_variation, 2)
            
            # Set enterprise-specific fields based on size
            if size_index <= 1:  # Starter, Small
                data_limit_gb = random.choice([300, 500, 750])
                voice_limit_minutes = random.choice([3000, 5000])
                sms_limit = random.choice([3000, 5000])
            elif size_index <= 3:  # Medium, Large
                data_limit_gb = random.choice([750, 1000, 1500])
                voice_limit_minutes = random.choice([5000, 10000, None])
                sms_limit = random.choice([5000, 10000, None])
            else:  # Corporate, Global
                data_limit_gb = random.choice([1500, 2000, None])
                voice_limit_minutes = None  # Always unlimited
                sms_limit = None  # Always unlimited
            
            # Enterprise plans very likely to have roaming, increasing with size
            roaming_probability = 0.6 + (size_index * 0.06)
            international_roaming = random.random() < roaming_probability
            

        if international_roaming:
            all_countries = list(COUNTRIES.keys())
            base_countries = 5 + (size_index * 3)
            max_countries = min(len(all_countries), base_countries)
            min_countries = min(base_countries // 2, max_countries - 1)
            
            if min_countries < max_countries:
                num_countries = random.randint(min_countries, max_countries)
            else:
                num_countries = min_countries
            
            num_countries = min(num_countries, len(all_countries))
            countries_sample = random.sample(all_countries, num_countries)
            roaming_countries = "{" + ",".join(country for country in countries_sample) + "}"
            roaming_data_gb = round(random.uniform(5.0, 10.0) * (1 + size_index * 0.3), 2)
            roaming_voice_minutes = random.randint(300, 800) * (1 + size_index // 2)
            
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
    """Generate device data."""
    devices = []
    
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
    
    for i in range(2, num_devices + 1):
        brand = random.choice(DEVICE_BRANDS)
        model = random.choice(DEVICE_MODELS[brand])
        image = f"{brand.lower()}_{model.lower().replace(' ', '_')}.jpg"
        sf_record = f"DEV{random.randint(10000000, 99999999)}"
        
        devices.append({
            "device_id": i,
            "created_at": fake.date_time_between(start_date="-3y", end_date="-1y").isoformat(),
            "updated_at": fake.date_time_between(start_date="-1y", end_date="now").isoformat(),
            "brand": brand,
            "model": model,
            "image": image,
            "sf_record": sf_record
        })
    return devices

def generate_network_nodes(num_nodes: int) -> List[Dict]:
    """Generate network infrastructure nodes."""
    nodes = []
    for i in range(1, num_nodes + 1):
        # Generate nodes across different regions
        latitude = random.uniform(25.0, 49.0)  # Roughly covers US/Canada
        longitude = random.uniform(-125.0, -70.0)
        
        nodes.append({
            "node_id": i,
            "node_name": f"NODE-{fake.word().upper()}-{random.randint(100, 999)}",
            "latitude": latitude,
            "longitude": longitude,
            "capacity": random.randint(1000, 10000),
            "status": random.choice(NODE_STATUSES)
        })
    return nodes

def generate_customer_plans(customers: List[Dict], plans: List[Dict]) -> List[Dict]:
    """Generate customer plan associations."""
    customer_plans = []
    customer_plan_id = 1
    
    # Create a lookup for plans
    plan_lookup = {plan["plan_id"]: plan for plan in plans}
    
    for customer in customers:
        customer_id = customer["customer_id"]
        
        # Special case for Alexis Smith (customer ID 7)
        if customer_id == 7:
            # Find a mobile plan for Alexis
            mobile_plans = [p for p in plans if p["type"] == "Mobile"]
            if mobile_plans:
                selected_plan = random.choice(mobile_plans)
                start_date = fake.date_time_between(start_date="-1y", end_date="-3m")
                
                # Get data allocation based on the plan
                data_allocation_gb = selected_plan.get("data_limit_gb", 0)
                if data_allocation_gb is None:  # Unlimited plan
                    data_allocation_gb = 1000  # Represent unlimited with a large number
                
                # Generate realistic data usage (between 10% and 90% of allocation)
                data_used_gb = round(random.uniform(0.1 * data_allocation_gb, 0.9 * data_allocation_gb), 2)
                
                # Some rollover data from previous month
                rollover_data_gb = round(random.uniform(0, 5), 2)
                
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
            # Each customer has 1-3 plans
            num_plans = random.randint(1, 3)
            selected_plans = random.sample(plans, min(num_plans, len(plans)))
            
            for plan in selected_plans:
                start_date = fake.date_time_between(start_date="-3y", end_date="-1m")
                
                # Some plans might have ended
                if random.random() < 0.2:
                    end_date = fake.date_time_between(start_date=start_date, end_date="now")
                    status = "inactive"
                else:
                    end_date = None
                    status = random.choices(
                        ["active", "activating"],
                        weights=[0.95, 0.05]
                    )[0]
                
                # Get data allocation based on the plan
                data_allocation_gb = plan.get("data_limit_gb", 0)
                if data_allocation_gb is None:  # Unlimited plan
                    data_allocation_gb = 1000  # Represent unlimited with a large number
                
                # Generate realistic data usage
                if status == "active":
                    # Active plans have usage between 10% and 90% of allocation
                    data_used_gb = round(random.uniform(0.1 * data_allocation_gb, 0.9 * data_allocation_gb), 2)
                    # Some rollover data from previous month (0-5GB)
                    rollover_data_gb = round(random.uniform(0, 5), 2)
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

def generate_customer_plan_devices(customer_plans: List[Dict], devices: List[Dict]) -> List[Dict]:
    """Generate associations between customer plans and devices."""
    customer_plan_devices = []
    
    # Find Alexis's plan
    alexis_plans = [p for p in customer_plans if p["customer_id"] == 7]
    
    for plan in customer_plans:
        # Special case for Alexis Smith
        if plan["customer_id"] == 7:
            # Ensure Alexis has an iPhone
            iphone = next((d for d in devices if d["brand"] == "Apple" and "iPhone" in d["model"]), devices[0])
            
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
        # Not all plans have devices (e.g., internet-only plans)
        elif random.random() < 0.7:
            device = random.choice(devices)
            
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
    """Generate associations between customers and network nodes."""
    customer_network = []
    
    for customer in customers:
        # Each customer is connected to 1-2 nodes
        num_nodes = random.randint(1, 2)
        selected_nodes = random.sample(nodes, min(num_nodes, len(nodes)))
        
        for node in selected_nodes:
            customer_network.append({
                "customer_id": customer["customer_id"],
                "node_id": node["node_id"]
            })
    
    return customer_network

def generate_billing(customers: List[Dict], customer_plans: List[Dict], plans: List[Dict]) -> List[Dict]:
    """Generate billing records."""
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
    
    for customer in customers:
        customer_id = customer["customer_id"]
        
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
            
            # Determine payment status (older bills more likely to be paid)
            if month_offset > 2:
                payment_status = random.choices(
                    ["Paid", "Refunded"], 
                    weights=[0.95, 0.05]
                )[0]
            elif month_offset == 1:
                payment_status = random.choices(
                    ["Paid", "Pending", "Overdue"], 
                    weights=[0.7, 0.2, 0.1]
                )[0]
            else:  # Current month
                payment_status = random.choices(
                    ["Pending", "Paid"], 
                    weights=[0.8, 0.2]
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
    """Generate credit card information."""
    credit_cards = []
    credit_card_id = 1
    
    for customer in customers:
        # Some customers have multiple cards
        num_cards = random.choices([1, 2], weights=[0.8, 0.2])[0]
        
        for _ in range(num_cards):
            # Generate a future expiry date
            expiry_year = datetime.datetime.now().year + random.randint(1, 5)
            expiry_month = random.randint(1, 12)
            expiry_date = datetime.date(expiry_year, expiry_month, 1)
            
            credit_cards.append({
                "credit_card_id": credit_card_id,
                "created_at": fake.date_time_between(start_date="-3y", end_date="-1y").isoformat(),
                "updated_at": fake.date_time_between(start_date="-1y", end_date="now").isoformat(),
                "expiry": expiry_date.isoformat(),
                "cvv": random.randint(100, 999),
                "number": f"XXXX-XXXX-XXXX-{random.randint(1000, 9999)}",  # Masked for privacy
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
    """Generate promotional deals."""
    deals = []
    
    for i in range(1, num_deals + 1):
        segment = random.choice(CUSTOMER_SEGMENTS)
        min_spend = random.randint(20, 100)
        max_spend = min_spend + random.randint(50, 200)
        
        start_date = fake.date_time_between(start_date="-1y", end_date="now")
        end_date = fake.date_time_between(start_date=start_date, end_date="+1y")
        
        deals.append({
            "deal_id": i,
            "deal_name": f"{segment} {random.choice(['Special', 'Discount', 'Promotion', 'Offer'])}",
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

def generate_calls(customer_plans: List[Dict], nodes: List[Dict]) -> List[Dict]:
    """Generate call records."""
    calls = []
    call_id = 1
    
    for plan in customer_plans:
        if plan["status"] != "active":
            continue
            
        customer_id = plan["customer_id"]
        
        # Find a device for this plan
        device_id = random.randint(1, 50)  # Simplified
        
        # Generate multiple calls for each customer
        for _ in range(random.randint(5, 20)):
            timestamp = fake.date_time_between(start_date="-3m", end_date="now")
            duration = random.randint(10, 3600)  # 10 seconds to 1 hour
            call_type = random.choice(CALL_TYPES)
            
            # If it's a missed call, duration should be 0
            if call_type == "Missed":
                duration = 0
                
            # Generate a random receiver number
            receiver_number = generate_phone_number()
            
            # Assign a random network node
            node = random.choice(nodes)

            latitude = random.uniform(25.0, 49.0)
            longitude = random.uniform(-125.0, -70.0)
            
            calls.append({
                "CallID": call_id,
                "CustomerID": customer_id,
                "DeviceID": device_id,
                "TimeStamp": timestamp.isoformat(),
                "Duration": duration,
                "CallType": call_type,
                "ReceiverNumber": receiver_number,
                "NodeId": node["node_id"],
                "latitude": latitude,
                "longitude": longitude
            })
            call_id += 1
    
    return calls

def generate_texts(customer_plans: List[Dict], nodes: List[Dict]) -> List[Dict]:
    """Generate text message records."""
    texts = []
    text_id = 1
    
    for plan in customer_plans:
        if plan["status"] != "active":
            continue
            
        customer_id = plan["customer_id"]
        
        # Find a device for this plan
        device_id = random.randint(1, 50)  # Simplified
        
        # Generate multiple texts for each customer
        for _ in range(random.randint(10, 30)):
            timestamp = fake.date_time_between(start_date="-3m", end_date="now")
            message_type = random.choice(MESSAGE_TYPES)
            
            # Generate a random receiver number
            receiver_number = generate_phone_number()
            
            # Assign a random network node
            node = random.choice(nodes)

            latitude = random.uniform(25.0, 49.0)
            longitude = random.uniform(-125.0, -70.0)
            
            texts.append({
                "TextID": text_id,
                "CustomerID": customer_id,
                "DeviceID": device_id,
                "TimeStamp": timestamp.isoformat(),
                "MessageType": message_type,
                "ReceiverNumber": receiver_number,
                "NodeId": node["node_id"],
                "latitude": latitude,
                "longitude": longitude
            })
            text_id += 1
    
    return texts

def generate_service_interactions(customers: List[Dict]) -> List[Dict]:
    """Generate customer service interaction records."""
    interactions = []
    interaction_id = 1
    
    # Define possible categories and channels
    categories = ['technical', 'billing', 'account', 'plan', 'device', 'coverage']
    channels = ['phone', 'chat', 'email', 'store', 'social']
    resolution_statuses = ['resolved', 'pending', 'escalated']
    
    for customer in customers:
        # Generate 0-5 interactions per customer
        num_interactions = random.randint(0, 5)
        
        for _ in range(num_interactions):
            # Generate interaction details
            interaction_date = fake.date_time_between(start_date="-1y", end_date="now")
            category = random.choice(categories)
            channel = random.choice(channels)
            resolution_status = random.choice(resolution_statuses)
            
            # Satisfaction score more likely to be high for resolved issues
            if resolution_status == 'resolved':
                satisfaction_score = random.choices(
                    range(1, 11),
                    weights=[0.01, 0.02, 0.03, 0.04, 0.05, 0.1, 0.15, 0.2, 0.2, 0.2]
                )[0]
            else:
                satisfaction_score = random.choices(
                    range(1, 11),
                    weights=[0.1, 0.1, 0.15, 0.15, 0.15, 0.1, 0.1, 0.05, 0.05, 0.05]
                )[0]
            
            # Resolution time depends on complexity and status
            if category in ['technical', 'billing']:
                base_time = random.randint(15, 60)
            else:
                base_time = random.randint(5, 30)
                
            if resolution_status == 'escalated':
                resolution_time = base_time * random.randint(2, 4)
            elif resolution_status == 'pending':
                resolution_time = 0  # Not resolved yet
            else:
                resolution_time = base_time
            
            # Agent ID (1-20)
            agent_id = random.randint(1, 20)
            
            # Generate notes based on category and status
            if category == 'technical':
                notes = random.choice([
                    "Customer reported connectivity issues. Troubleshooting steps provided.",
                    "Device not connecting to network. Reset network settings.",
                    "Slow data speeds reported. Checked tower status and signal strength.",
                    "Customer unable to make calls. Verified account status and signal."
                ])
            elif category == 'billing':
                notes = random.choice([
                    "Customer disputed recent charges. Reviewed bill with customer.",
                    "Question about proration on latest bill. Explained billing cycle.",
                    "Customer requested payment extension. Approved for 7 days.",
                    "Billing address update requested. Information updated in system."
                ])
            else:
                notes = f"Customer inquiry about {category}. Provided information and assistance."
            
            interactions.append({
                "interaction_id": interaction_id,
                "customer_id": customer["customer_id"],
                "interaction_date": interaction_date.isoformat(),
                "channel": channel,
                "category": category,
                "resolution_status": resolution_status,
                "satisfaction_score": satisfaction_score,
                "agent_id": agent_id,
                "resolution_time_minutes": resolution_time,
                "notes": notes
            })
            
            interaction_id += 1
    
    return interactions

def generate_interactions(customers: List[Dict]) -> List[Dict]:
    """Generate general customer interaction records across channels."""
    interactions = []
    interaction_id = 1
    
    # Define possible channels and topics
    channels = ['call', 'chat', 'email', 'store', 'social media', 'website']
    topics = [
        'account inquiry', 'technical support', 'billing question',
        'upgrade options', 'new service', 'cancellation request',
        'feature explanation', 'promotion inquiry', 'complaint',
        'general question'
    ]
    resolution_statuses = ['resolved', 'pending', 'transferred', 'follow-up required']
    
    for customer in customers:
        # Generate 1-8 interactions per customer
        num_interactions = random.randint(1, 8)
        
        for _ in range(num_interactions):
            # Generate interaction details
            interaction_time = fake.date_time_between(start_date="-6m", end_date="now")
            channel = random.choice(channels)
            topic = random.choice(topics)
            
            # Duration depends on channel and topic
            if channel in ['call', 'store']:
                duration = random.randint(180, 1200)  # 3-20 minutes in seconds
            elif channel == 'chat':
                duration = random.randint(300, 1800)  # 5-30 minutes in seconds
            else:
                duration = 0  # No duration for email, social media, etc.
            
            # Agent ID (1-30)
            agent_id = random.randint(1, 30)
            
            # Resolution status
            resolution_status = random.choice(resolution_statuses)
            
            # Satisfaction rating (1-5 stars)
            if resolution_status == 'resolved':
                satisfaction_rating = random.choices(
                    range(1, 6),
                    weights=[0.05, 0.1, 0.15, 0.3, 0.4]
                )[0]
            else:
                satisfaction_rating = random.choices(
                    range(1, 6),
                    weights=[0.2, 0.3, 0.3, 0.15, 0.05]
                )[0]
            
            # Notes
            notes = f"{topic.capitalize()} via {channel}. " + random.choice([
                "Customer was satisfied with the resolution.",
                "Customer needed additional information.",
                "Provided detailed explanation of services.",
                "Addressed customer concerns about recent changes.",
                "Scheduled follow-up for additional assistance.",
                "Transferred to specialized department for further help."
            ])
            
            interactions.append({
                "interaction_id": interaction_id,
                "customer_id": customer["customer_id"],
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
    """Generate number portability records."""
    portability_records = []
    portability_id = 1
    
    # List of possible carriers
    carriers = [
        "Verizon", "AT&T", "T-Mobile", "Sprint", "US Cellular",
        "Boost Mobile", "Cricket Wireless", "Metro by T-Mobile",
        "Xfinity Mobile", "Spectrum Mobile", "Google Fi"
    ]
    
    # Statuses and their weights
    statuses = ["requested", "in_progress", "completed", "failed"]
    status_weights = [0.1, 0.2, 0.6, 0.1]
    
    # Only about 30% of customers have ported numbers
    for customer in customers:
        if random.random() < 0.3:
            status = random.choices(statuses, weights=status_weights)[0]
            
            # Generate port date (within last 6 months)
            port_date = fake.date_time_between(start_date="-6m", end_date="-1d")
            
            # Completion date depends on status
            if status == "completed":
                completion_date = fake.date_time_between(start_date=port_date, end_date=port_date + datetime.timedelta(days=7))
            elif status == "failed":
                completion_date = fake.date_time_between(start_date=port_date, end_date=port_date + datetime.timedelta(days=10))
            else:
                completion_date = None
            
            # Generate notes based on status
            if status == "completed":
                notes = "Number successfully ported from previous carrier."
            elif status == "failed":
                notes = random.choice([
                    "Account information mismatch with previous carrier.",
                    "Customer canceled port request.",
                    "Previous carrier rejected port request.",
                    "Technical issue during port process."
                ])
            elif status == "in_progress":
                notes = "Port request being processed by previous carrier."
            else:
                notes = "Initial port request submitted. Awaiting processing."
            
            portability_records.append({
                "portability_id": portability_id,
                "customer_id": customer["customer_id"],
                "phone_number": generate_phone_number(),
                "previous_carrier": random.choice(carriers),
                "port_date": port_date.isoformat(),
                "status": status,
                "completion_date": completion_date.isoformat() if completion_date else None,
                "notes": notes
            })
            
            portability_id += 1
    
    return portability_records

def generate_voip_services(customers: List[Dict]) -> List[Dict]:
    """Generate VoIP service records."""
    voip_services = []
    voip_id = 1
    
    # Service types and features
    service_types = ["Business VoIP", "Residential VoIP", "SIP Trunking", "Cloud PBX", "Virtual Phone"]
    features_options = [
        "Call Forwarding", "Voicemail", "Call Recording", "Auto Attendant",
        "Conference Calling", "Call Analytics", "Number Porting", "Call Queuing",
        "Video Conferencing", "Mobile App", "CRM Integration", "International Calling"
    ]
    
    # Only about 20% of customers have VoIP services
    for customer in customers:
        if random.random() < 0.2:
            # Number of VoIP services per customer (1-2)
            num_services = random.choices([1, 2], weights=[0.8, 0.2])[0]
            
            for _ in range(num_services):
                service_type = random.choice(service_types)
                
                # Generate monthly fee based on service type
                if service_type in ["Business VoIP", "SIP Trunking", "Cloud PBX"]:
                    monthly_fee = random.uniform(50, 200)
                else:
                    monthly_fee = random.uniform(15, 50)
                
                # Generate features (3-6 random features)
                num_features = random.randint(3, 6)
                features_list = random.sample(features_options, num_features)
                features = "{" + ",".join('"' + feature + '"' for feature in features_list) + "}"
                
                # Generate activation date (within last 2 years)
                activation_date = fake.date_time_between(start_date="-2y", end_date="-1m")
                activation_date_str = activation_date.date().isoformat()
                
                # Status (mostly active)
                status = random.choices(
                    ["active", "suspended", "terminated"],
                    weights=[0.9, 0.07, 0.03]
                )[0]
                
                voip_services.append({
                    "voip_id": voip_id,
                    "customer_id": customer["customer_id"],
                    "service_number": generate_phone_number(),
                    "service_type": service_type,
                    "monthly_fee": round(monthly_fee, 2),
                    "features": features,
                    "activation_date": activation_date_str,
                    "status": status
                })
                
                voip_id += 1
    
    return voip_services

def generate_iot_devices(customers: List[Dict], plans: List[Dict]) -> List[Dict]:
    """Generate IoT device records."""
    iot_devices = []
    iot_device_id = 1
    
    # Device types
    device_types = [
        "Smart Tracker", "Asset Monitor", "Fleet Tracker", "Smart Meter",
        "Security Sensor", "Environmental Monitor", "Agricultural Sensor",
        "Industrial Monitor", "Smart City Sensor", "Health Monitor"
    ]
    
    # Find IoT plans
    iot_plans = [p for p in plans if p["type"] == "IoT"]
    if not iot_plans:
        iot_plans = [random.choice(plans)]  # Fallback if no IoT plans
    
    # About 15% of customers have IoT devices
    for customer in customers:
        if random.random() < 0.15:
            # Number of IoT devices per customer (1-5)
            num_devices = random.randint(1, 5)
            
            for _ in range(num_devices):
                device_type = random.choice(device_types)
                
                # Generate IMEI and SIM ICCID
                imei = f"{random.randint(100000000000000, 999999999999999)}"
                sim_iccid = f"89{random.randint(10000000000000000000, 99999999999999999999)}"
                
                # Assign a data plan
                data_plan = random.choice(iot_plans)
                
                # Generate activation date (within last 3 years)
                activation_date = fake.date_time_between(start_date="-3y", end_date="-1m")
                activation_date_str = activation_date.date().isoformat()
                
                # Generate last active date
                last_active_date = fake.date_time_between(
                    start_date=activation_date,
                    end_date="now"
                )
                
                # Generate monthly data usage (typically low for IoT)
                monthly_data_usage = random.uniform(5, 500)  # 5MB to 500MB
                
                # Status (mostly active)
                status = random.choices(
                    ["active", "inactive", "suspended"],
                    weights=[0.85, 0.1, 0.05]
                )[0]
                
                iot_devices.append({
                    "iot_device_id": iot_device_id,
                    "customer_id": customer["customer_id"],
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
    """Generate customer referral records."""
    referrals = []
    referral_id = 1
    
    # About 25% of customers have made referrals
    potential_referrers = [c for c in customers if random.random() < 0.25]
    
    for referrer in potential_referrers:
        # Number of referrals made by this customer (1-3)
        num_referrals = random.randint(1, 3)
        
        # Find potential referred customers (excluding self)
        potential_referred = [c for c in customers if c["customer_id"] != referrer["customer_id"]]
        
        # Select random referred customers
        if len(potential_referred) >= num_referrals:
            referred_customers = random.sample(potential_referred, num_referrals)
            
            for referred in referred_customers:
                # Generate referral date (within last year)
                referral_date = fake.date_time_between(start_date="-1y", end_date="-1d")
                referral_date_str = referral_date.date().isoformat()
                
                # Status
                status = random.choices(
                    ["pending", "accepted", "expired"],
                    weights=[0.2, 0.7, 0.1]
                )[0]
                
                # Bonus amount
                bonus_amount = random.choice([25, 50, 75, 100])
                
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
    """Generate device upgrade and trade-in records."""
    upgrades = []
    upgrade_id = 1
    
    # About 30% of customers have upgraded devices
    for customer in customers:
        if random.random() < 0.3:
            # Number of upgrades per customer (1-2)
            num_upgrades = random.choices([1, 2], weights=[0.8, 0.2])[0]
            
            for _ in range(num_upgrades):
                # Select random old and new devices
                if len(devices) >= 2:
                    old_device, new_device = random.sample(devices, 2)
                    
                    # Generate upgrade date (within last 2 years)
                    upgrade_date = fake.date_time_between(start_date="-2y", end_date="-1d")
                    upgrade_date_str = upgrade_date.date().isoformat()
                    
                    # Trade-in value based on old device
                    trade_in_value = random.uniform(50, 500)
                    
                    # Contract extension
                    contract_extension = random.choice([0, 12, 24])
                    
                    # Promotion applied
                    promotions = [
                        "New Customer Discount", "Loyalty Upgrade", "Trade-In Bonus",
                        "Holiday Special", "Limited Time Offer", "Bundle Discount"
                    ]
                    promotion_applied = random.choice(promotions) if random.random() < 0.7 else None
                    
                    upgrades.append({
                        "upgrade_id": upgrade_id,
                        "customer_id": customer["customer_id"],
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
    """Generate family plan records."""
    family_plans = []
    family_plan_members = []
    family_plan_id = 1
    
    # About 20% of customers are primary on family plans
    potential_primaries = [c for c in customers if random.random() < 0.2]
    
    for primary in potential_primaries:
        # Generate family plan details
        plan_name = random.choice([
            "Family Share", "Family Unlimited", "Family Basic",
            "Family Premium", "Family Value", "Family Elite"
        ])
        
        # Created date (within last 3 years)
        created_at = fake.date_time_between(start_date="-3y", end_date="-1m")
        
        # Max members (2-6)
        max_members = random.randint(2, 6)
        
        # Shared data (10-100GB)
        shared_data_gb = random.choice([10, 20, 30, 50, 100])
        
        # Monthly fee
        monthly_fee = 50 + (shared_data_gb * 0.5) + (max_members * 10)
        
        family_plans.append({
            "family_plan_id": family_plan_id,
            "primary_customer_id": primary["customer_id"],
            "plan_name": plan_name,
            "created_at": created_at.isoformat(),
            "max_members": max_members,
            "shared_data_gb": shared_data_gb,
            "monthly_fee": round(monthly_fee, 2)
        })
        
        # Add primary member
        family_plan_members.append({
            "family_plan_id": family_plan_id,
            "customer_id": primary["customer_id"],
            "role": "primary",
            "data_allocation_percentage": random.randint(20, 40)
        })
        
        # Find potential secondary members (excluding primary)
        potential_secondaries = [c for c in customers if c["customer_id"] != primary["customer_id"]]
        
        # Number of additional members (1 to max_members-1)
        num_additional = min(random.randint(1, max_members-1), len(potential_secondaries))
        
        if num_additional > 0 and potential_secondaries:
            secondary_members = random.sample(potential_secondaries, num_additional)
            
            for i, member in enumerate(secondary_members):
                # Determine role (first is usually secondary, rest are children)
                if i == 0 and random.random() < 0.8:
                    role = "secondary"
                else:
                    role = random.choice(["secondary", "child"])
                
                # Data allocation (remaining percentage divided somewhat evenly)
                data_allocation = random.randint(10, 30)
                
                family_plan_members.append({
                    "family_plan_id": family_plan_id,
                    "customer_id": member["customer_id"],
                    "role": role,
                    "data_allocation_percentage": data_allocation
                })
        
        family_plan_id += 1
    
    return family_plans, family_plan_members

def generate_loyalty_rewards(customers: List[Dict]) -> List[Dict]:
    """Generate customer loyalty rewards records."""
    rewards = []
    reward_id = 1
    
    # About 60% of customers have loyalty rewards
    for customer in customers:
        if random.random() < 0.6:
            # Points earned based on customer tenure and spending
            # Assuming higher customer IDs are newer customers
            base_points = max(1000, 10000 - customer["customer_id"] * 10)
            points_earned = random.randint(int(base_points * 0.8), int(base_points * 1.2))
            
            # Points redeemed (0-80% of earned)
            max_redeemed = int(points_earned * 0.8)
            points_redeemed = random.randint(0, max_redeemed)
            
            # Points balance
            points_balance = points_earned - points_redeemed
            
            # Last activity date
            last_activity_date = fake.date_time_between(start_date="-6m", end_date="-1d")
            last_activity_date_str = last_activity_date.date().isoformat()
            
            # Tier based on points balance
            if points_balance < 1000:
                tier = "bronze"
            elif points_balance < 5000:
                tier = "silver"
            elif points_balance < 15000:
                tier = "gold"
            else:
                tier = "platinum"
            
            rewards.append({
                "reward_id": reward_id,
                "customer_id": customer["customer_id"],
                "points_earned": points_earned,
                "points_redeemed": points_redeemed,
                "points_balance": points_balance,
                "last_activity_date": last_activity_date_str,
                "tier": tier
            })
            
            reward_id += 1
    
    return rewards

def generate_campaigns(num_campaigns: int) -> List[Dict]:
    """Generate marketing campaign records."""
    campaigns = []
    
    # Campaign channels
    channels = ["Email", "SMS", "Social Media", "Display Ads", "Search Ads", "Direct Mail", "TV", "Radio"]
    
    # Customer segments
    segments = ["All", "Premium", "Standard", "Budget", "Business", "Family", "New Customers", "Churned"]
    
    for i in range(1, num_campaigns + 1):
        # Campaign name
        campaign_name = f"Campaign {fake.word().capitalize()} {random.choice(['Q1', 'Q2', 'Q3', 'Q4'])} {random.choice([2022, 2023, 2024])}"
        
        # Start and end dates
        start_date = fake.date_time_between(start_date="-1y", end_date="now")
        start_date_str = start_date.date().isoformat()
        
        end_date = start_date.date() + datetime.timedelta(days=random.randint(14, 90))
        if end_date > datetime.date.today():
            end_date_str = None
        else:
            end_date_str = end_date.isoformat()
        
        # Target segment
        target_segment = random.choice(segments)
        
        # Channel
        channel = random.choice(channels)
        
        # Offer details
        offers = [
            "20% off for 3 months", "Free device with new line", "Double data for 6 months",
            "Waived activation fee", "Free premium service for 1 month", "$100 bill credit",
            "Free international calling for 3 months", "Buy one line, get one free"
        ]
        offer_details = random.choice(offers)
        
        # Budget
        budget = random.randint(5000, 100000)
        
        # Conversion goals and actuals
        conversion_goal = random.randint(100, 5000)
        
        # Actual conversions (only if campaign has ended)
        if end_date_str:
            goal_achievement = random.uniform(0.7, 1.3)  # 70-130% of goal
            actual_conversions = int(conversion_goal * goal_achievement)
        else:
            actual_conversions = None
        
        campaigns.append({
            "campaign_id": i,
            "campaign_name": campaign_name,
            "start_date": start_date_str,
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
    """Generate customer feedback records."""
    feedback_records = []
    feedback_id = 1
    
    # Feedback categories
    categories = ["Service Quality", "Network Coverage", "Customer Support", "Billing", "Device", "Plan Features", "Website/App"]
    
    # About 40% of customers have provided feedback
    for customer in customers:
        if random.random() < 0.4:
            # Number of feedback entries per customer (1-3)
            num_feedback = random.choices([1, 2, 3], weights=[0.7, 0.2, 0.1])[0]
            
            for _ in range(num_feedback):
                # Feedback date
                feedback_date = fake.date_time_between(start_date="-1y", end_date="-1d")
                
                # Category
                category = random.choice(categories)
                
                # Rating (1-10)
                # Higher customer_id (newer customers) tend to give slightly higher ratings
                base_rating = 7 if customer["customer_id"] % 10 > 5 else 5
                rating = max(1, min(10, base_rating + random.randint(-3, 3)))
                
                # Comments
                if rating >= 8:
                    comments = random.choice([
                        "Very satisfied with the service.",
                        f"Great experience with the {category.lower()}.",
                        "Exceeded my expectations.",
                        "Will definitely recommend to others.",
                        "Much better than my previous provider."
                    ])
                    requires_followup = False
                elif rating >= 5:
                    comments = random.choice([
                        "Satisfactory service but room for improvement.",
                        f"Generally good {category.lower()}, with minor issues.",
                        "Meets expectations but nothing exceptional.",
                        "Decent value for money.",
                        "Acceptable but could be better."
                    ])
                    requires_followup = random.random() < 0.3
                else:
                    comments = random.choice([
                        f"Disappointed with the {category.lower()}.",
                        "Below expectations.",
                        "Several issues need to be addressed.",
                        "Not worth the money.",
                        "Considering switching providers."
                    ])
                    requires_followup = random.random() < 0.8
                
                # Followup details
                if requires_followup:
                    if random.random() < 0.7:  # 70% of required followups have been completed
                        followup_date = fake.date_time_between(
                            start_date=feedback_date,
                            end_date=feedback_date + datetime.timedelta(days=7)
                        )
                        followup_notes = random.choice([
                            "Customer contacted and issues addressed.",
                            "Offered compensation for inconvenience.",
                            "Provided technical support.",
                            "Escalated to supervisor for resolution.",
                            "Scheduled service appointment."
                        ])
                    else:
                        followup_date = None
                        followup_notes = "Pending followup"
                else:
                    followup_date = None
                    followup_notes = None
                
                feedback_records.append({
                    "feedback_id": feedback_id,
                    "customer_id": customer["customer_id"],
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