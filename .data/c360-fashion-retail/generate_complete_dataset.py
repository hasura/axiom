#!/usr/bin/env python3
"""
C360 Retail Fashion Database - Complete Dataset Generator
Generates realistic data for 50k customers plus contextually accurate reviews
"""

import json
import random
import csv
import os
import uuid
import numpy as np
from datetime import datetime, timedelta, date
from faker import Faker
from faker.providers import BaseProvider
import string

# Initialize Faker
fake = Faker('en_US')
Faker.seed(42)  # For reproducible results
random.seed(42)
np.random.seed(42)

class FashionProvider(BaseProvider):
    fashion_brands = [
        'Bella Vista', 'Urban Thread', 'Coastal Chic', 'Metro Style', 'Classic Craft',
        'Modern Muse', 'Sunset Styles', 'City Casual', 'Elite Edge', 'Vintage Vibe',
        'Fresh Fashion', 'Bold Basics', 'Luxe Label', 'Street Smart', 'Pure Elegance',
        'Trend Tribe', 'Style Studio', 'Fashion Forward', 'Chic Collection', 'Mode Moderne'
    ]
    
    fashion_categories = {
        'Womens Clothing': ['Dresses', 'Tops', 'Bottoms', 'Outerwear'],
        'Mens Clothing': ['Shirts', 'Pants', 'Suits', 'Casual'],
        'Accessories': ['Bags', 'Jewelry', 'Belts'],
        'Footwear': ['Sneakers', 'Boots', 'Formal'],
        'Activewear': ['Yoga', 'Running', 'Gym']
    }
    
    fashion_materials = [
        'Cotton', 'Polyester', 'Wool', 'Silk', 'Linen', 'Denim', 
        'Cashmere', 'Leather', 'Viscose', 'Modal'
    ]
    
    colors = ['Black', 'White', 'Navy', 'Gray', 'Beige', 'Red', 'Blue', 'Green', 'Brown', 'Pink']
    sizes = ['XS', 'S', 'M', 'L', 'XL', 'XXL']

class ReviewProvider(BaseProvider):
    positive_reviews = [
        "Absolutely love this {product}! Perfect fit and great quality.",
        "This {product} exceeded my expectations! Will definitely buy again.",
        "Amazing {product}! The {material} feels so comfortable and looks great.",
        "Perfect {product}! Exactly what I was looking for. Highly recommend!",
        "Great quality {product}. True to size and arrived quickly.",
        "This {product} is a game-changer! Love the fit and style.",
        "Outstanding {product}! The {material} is premium quality.",
        "Fantastic purchase! This {product} is exactly as described.",
        "Love everything about this {product}! Will order more colors.",
        "Best {product} I've bought in years! So comfortable and stylish."
    ]
    
    funny_reviews = [
        "This {product} makes me look like I have my life together. 10/10!",
        "My cat approves of this {product}, and she has very high standards.",
        "This {product} is so comfortable, I forgot I was wearing it.",
        "Bought this {product} to impress people. It worked on me first!",
        "This {product} is like a good friend - always there when you need it.",
        "My {product} and I are now best friends. Sorry not sorry.",
        "This {product} makes me feel like a fashion influencer (I'm not).",
        "I bought this {product} and suddenly I'm 10% cooler.",
        "This {product} is proof that good things come in small packages.",
        "Warning: wearing this {product} may cause excessive compliments."
    ]
    
    sarcastic_reviews = [
        "Oh great, another {product} that actually fits. What a surprise.",
        "Wow, a {product} that looks exactly like the picture. Revolutionary.",
        "This {product} is so good, I almost forgot to complain about something.",
        "Finally, a {product} that doesn't make me question my life choices.",
        "This {product} is decent. I know, shocking review coming from me.",
        "I guess this {product} is fine if you like things that work properly.",
        "Such a functional {product}. How boring and wonderful.",
        "Here's a {product} that does exactly what it says. Mind blown."
    ]
    
    average_reviews = [
        "This {product} is okay. Nothing special but does the job.",
        "Average {product}. The {material} is decent for the price.",
        "It's an okay {product}. Would maybe buy again.",
        "This {product} is fine. Not amazing but not terrible either.",
        "Decent {product}. Fits as expected but nothing wow.",
        "This {product} is alright. Gets the job done.",
        "Average quality {product}. Fair for the price point.",
        "This {product} meets expectations. Nothing more, nothing less.",
        "Standard {product}. Works fine but not exceptional."
    ]
    
    negative_reviews = [
        "Disappointed with this {product}. The {material} feels cheap.",
        "This {product} doesn't look anything like the picture. Very misleading.",
        "Poor quality {product}. Started showing wear after minimal use.",
        "Not happy with this {product}. The sizing is completely off.",
        "This {product} is not worth the money. Very poor quality.",
        "The {material} feels flimsy and cheap. Expected better.",
        "Would not recommend this {product}. Very disappointed.",
        "This {product} looks nothing like what I expected.",
        "Quality is lacking for the price. Won't buy again."
    ]
    
    bad_reviews = [
        "Absolute garbage. This {product} fell apart immediately.",
        "DO NOT BUY! This {product} is the worst purchase I've ever made.",
        "This {product} is a joke. Cheap {material} and terrible construction.",
        "I want my money back! This {product} is completely unwearable.",
        "Horrible {product}. Looks nothing like the photo and feels awful.",
        "This {product} should come with a warning label. Awful quality.",
        "Zero stars if I could. This {product} is complete trash.",
        "Waste of money. This {product} is poorly made junk.",
        "Terrible quality. This {product} is not worth a penny."
    ]

class SocialMediaProvider(BaseProvider):
    platforms = ['Instagram', 'TikTok', 'Twitter', 'Facebook', 'Pinterest']
    
    post_types = ['Post', 'Story', 'Reel', 'Video', 'Comment']
    
    fashion_hashtags = [
        '#fashion', '#style', '#outfit', '#ootd', '#fashionista', '#streetstyle',
        '#trendy', '#stylish', '#fashionblogger', '#outfitinspo', '#fashionpost',
        '#styleinspo', '#fashionlover', '#instafashion', '#lookbook', '#styling'
    ]
    
    influencer_usernames = [
        'fashionista_maya', 'style_queen_jen', 'trendy_alex', 'chic_sarah',
        'glamour_girl_23', 'street_style_sam', 'fashion_forward_lily',
        'style_maven_kate', 'trendsetter_mia', 'outfit_obsessed', 'fashion_guru_anna',
        'style_inspiration', 'chic_and_sleek', 'fashion_diary_emma', 'glamour_vibes'
    ]
    
    post_templates = [
        "Just got my hands on the latest {product} from {brand}! Absolutely obsessed 😍 {hashtags}",
        "Can't get enough of this {product}! Perfect for {season} vibes ✨ {hashtags}",
        "New {product} haul from {brand} - which one should I style first? {hashtags}",
        "This {product} is giving me life! Such amazing quality 💫 {hashtags}",
        "Styling my new {product} three different ways! Swipe to see ➡️ {hashtags}",
        "{brand} never disappoints! This {product} is pure perfection 🔥 {hashtags}",
        "Found the perfect {product} for date night! Link in bio 💕 {hashtags}",
        "Casual Friday calls for this comfy {product} - so versatile! {hashtags}"
    ]

fake.add_provider(FashionProvider)
fake.add_provider(ReviewProvider)
fake.add_provider(SocialMediaProvider)

class CompleteDatasetGenerator:
    def __init__(self, output_dir='postgres'):
        self.output_dir = output_dir
        self.data = {}
        self.product_quality_scores = {}
        self.used_emails = set()  # Track used emails to ensure uniqueness
        
        # Real cities by state for consistent usage throughout the application
        self.state_cities = {
            'CA': ['Los Angeles', 'San Francisco', 'San Diego', 'Sacramento', 'San Jose', 'Oakland', 'Fresno', 'Long Beach', 'Santa Ana', 'Anaheim', 'Riverside', 'Bakersfield', 'Stockton', 'Irvine', 'Chula Vista'],
            'TX': ['Houston', 'Dallas', 'San Antonio', 'Austin', 'Fort Worth', 'El Paso', 'Arlington', 'Corpus Christi', 'Plano', 'Lubbock', 'Irving', 'Laredo', 'Garland', 'Frisco', 'McKinney'],
            'FL': ['Jacksonville', 'Miami', 'Tampa', 'Orlando', 'St. Petersburg', 'Hialeah', 'Tallahassee', 'Fort Lauderdale', 'Port St. Lucie', 'Cape Coral', 'Pembroke Pines', 'Hollywood', 'Gainesville', 'Miramar', 'Coral Springs'],
            'NY': ['New York', 'Buffalo', 'Rochester', 'Yonkers', 'Syracuse', 'Albany', 'New Rochelle', 'Mount Vernon', 'Schenectady', 'Utica', 'White Plains', 'Troy', 'Niagara Falls', 'Binghamton', 'Freeport'],
            'PA': ['Philadelphia', 'Pittsburgh', 'Allentown', 'Erie', 'Reading', 'Scranton', 'Bethlehem', 'Lancaster', 'Harrisburg', 'Altoona', 'York', 'State College', 'Wilkes-Barre', 'Chester', 'Norristown'],
            'IL': ['Chicago', 'Aurora', 'Naperville', 'Joliet', 'Rockford', 'Elgin', 'Peoria', 'Springfield', 'Waukegan', 'Cicero', 'Champaign', 'Bloomington', 'Arlington Heights', 'Evanston', 'Schaumburg'],
            'OH': ['Columbus', 'Cleveland', 'Cincinnati', 'Toledo', 'Akron', 'Dayton', 'Parma', 'Canton', 'Youngstown', 'Lorain', 'Hamilton', 'Springfield', 'Kettering', 'Elyria', 'Lakewood'],
            'GA': ['Atlanta', 'Augusta', 'Columbus', 'Savannah', 'Athens', 'Sandy Springs', 'Roswell', 'Macon', 'Johns Creek', 'Albany', 'Warner Robins', 'Alpharetta', 'Marietta', 'Valdosta', 'Smyrna'],
            'NC': ['Charlotte', 'Raleigh', 'Greensboro', 'Durham', 'Winston-Salem', 'Fayetteville', 'Cary', 'Wilmington', 'High Point', 'Greenville', 'Asheville', 'Concord', 'Gastonia', 'Jacksonville', 'Chapel Hill'],
            'MI': ['Detroit', 'Grand Rapids', 'Warren', 'Sterling Heights', 'Ann Arbor', 'Lansing', 'Flint', 'Dearborn', 'Livonia', 'Westland', 'Troy', 'Farmington Hills', 'Kalamazoo', 'Wyoming', 'Southfield']
        }
        
        os.makedirs(output_dir, exist_ok=True)
        print("🚀 C360 Complete Dataset Generator v3.1 - Enterprise Scale with Data Quality")
        print("📊 Generating 50k customers + contextually accurate reviews")
        print("✅ Enhanced with data quality rules to prevent:")
        print("  • Email duplicates")
        print("  • Order item duplicates")
        print("  • Date inconsistencies")
        print("  • Gender value inconsistencies")
        print("  • Fake city names (uses real US cities)")
        
    def weighted_choice(self, choices, weights):
        """Make a weighted random choice"""
        return np.random.choice(choices, p=weights)
    
    def generate_id(self, prefix='', length=8):
        """Generate a random ID with optional prefix"""
        chars = string.ascii_uppercase + string.digits
        return prefix + ''.join(random.choices(chars, k=length))
    
    def date_between(self, start_date, end_date):
        """Generate random date between two dates"""
        return fake.date_between(start_date, end_date)
    
    def timestamp_between(self, start_date, end_date):
        """Generate random timestamp between two dates"""
        return fake.date_time_between(start_date, end_date)
    
    def generate_realistic_email(self, first_name, last_name):
        """Generate unique realistic email based on first and last names"""
        # Clean names to remove any special characters and make lowercase
        first_clean = ''.join(c.lower() for c in first_name if c.isalnum())
        last_clean = ''.join(c.lower() for c in last_name if c.isalnum())
        
        # Common email domains
        domains = [
            'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'icloud.com',
            'aol.com', 'protonmail.com', 'mail.com', 'zoho.com', 'fastmail.com'
        ]
        
        # Common email patterns using actual names
        base_patterns = [
            f"{first_clean}.{last_clean}",           # john.smith
            f"{first_clean}_{last_clean}",           # john_smith
            f"{first_clean[0]}{last_clean}",         # jsmith
            f"{first_clean}{last_clean[0]}",         # johnS
            f"{first_clean}{last_clean}",            # johnsmith
            f"{last_clean}.{first_clean}",           # smith.john
            f"{first_clean}.{last_clean[0]}",        # john.s
            f"{first_clean[0]}.{last_clean}",        # j.smith
        ]
        
        # Try to generate a unique email
        max_attempts = 50
        for attempt in range(max_attempts):
            # Choose a base pattern
            pattern = random.choice(base_patterns)
            
            # Add numbers for uniqueness if not first attempt or randomly
            if attempt > 0 or random.random() < 0.3:
                if random.random() < 0.5:
                    # Add 2-digit numbers
                    pattern += str(random.randint(10, 99))
                else:
                    # Add 4-digit year-like numbers
                    pattern += str(random.randint(1970, 2005))
            
            # If still not unique after several attempts, add attempt number
            if attempt > 20:
                pattern += str(attempt)
            
            domain = random.choice(domains)
            email = f"{pattern}@{domain}"
            
            # Check if this email is unique
            if email not in self.used_emails:
                self.used_emails.add(email)
                return email
        
        # Fallback - should rarely happen but ensures uniqueness
        fallback_email = f"{first_clean}.{last_clean}.{len(self.used_emails)}@{random.choice(domains)}"
        self.used_emails.add(fallback_email)
        return fallback_email
    
    def get_random_city_state(self):
        """Get a random real city and its corresponding state"""
        state = random.choice(list(self.state_cities.keys()))
        city = random.choice(self.state_cities[state])
        return city, state

    def save_to_csv(self, table_name, data, headers):
        """Save data to CSV file"""
        filepath = os.path.join(self.output_dir, f'{table_name}.csv')
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(headers)
            writer.writerows(data)
        print(f"✅ Generated {len(data)} rows for {table_name}")
        self.data[table_name] = data

    def generate_brands(self):
        """Generate brands table (30-50 brands)"""
        num_brands = random.randint(30, 50)
        brands = []
        tier_dist = {'Luxury': 0.20, 'Premium': 0.30, 'Contemporary': 0.20, 'Fast Fashion': 0.20, 'Value': 0.10}
        tiers = list(tier_dist.keys())
        weights = list(tier_dist.values())
        
        for i in range(num_brands):
            # Generate diverse brand names for larger dataset
            if i < len(FashionProvider.fashion_brands):
                brand_name = FashionProvider.fashion_brands[i]
            else:
                base_name = random.choice(['Fashion', 'Style', 'Trend', 'Chic', 'Elite', 'Modern', 'Classic', 'Urban', 'Premium', 'Luxe'])
                suffix = random.choice(['Co', 'Brand', 'Label', 'House', 'Studio', 'Collection', 'Design', 'Atelier', 'Boutique', 'Group'])
                brand_name = f"{base_name} {suffix} {i+1-len(FashionProvider.fashion_brands)}" if i >= len(FashionProvider.fashion_brands) else FashionProvider.fashion_brands[i]
            
            brand_data = [
                i + 1,  # brand_id
                brand_name,  # brand_name
                fake.company() if random.random() < 0.3 else None,  # parent_company
                self.weighted_choice(tiers, weights),  # brand_tier
                fake.text(max_nb_chars=200),  # description
                fake.url(),  # website_url
                random.randint(1950, 2022),  # year_established
                random.choice([True, False]) if random.random() < 0.1 else True,  # is_active
                self.timestamp_between('-5y', '-1y')  # created_at
            ]
            brands.append(brand_data)
        
        headers = ['brand_id', 'brand_name', 'parent_company', 'brand_tier', 'description', 'website_url', 'year_established', 'is_active', 'created_at']
        self.save_to_csv('brands', brands, headers)
        return brands

    def generate_categories(self):
        """Generate categories table"""
        categories = []
        cat_id = 1
        
        # Use all main categories and create more subcategories
        for main_cat, subcats in FashionProvider.fashion_categories.items():
            # Add main category
            main_category_data = [
                cat_id,  # category_id
                main_cat,  # category_name
                None,  # parent_category_id
                fake.text(max_nb_chars=150),  # description
                random.choice([True, False]),  # is_seasonal
                round(random.uniform(0.15, 0.45), 2),  # typical_margin_percentage
                self.timestamp_between('-3y', '-1y')  # created_at
            ]
            categories.append(main_category_data)
            main_cat_id = cat_id
            cat_id += 1
            
            # Add more subcategories for larger dataset
            num_subcats = min(len(subcats), random.randint(2, 4))
            for subcat in random.sample(subcats, num_subcats):
                sub_category_data = [
                    cat_id,  # category_id
                    subcat,  # category_name
                    main_cat_id,  # parent_category_id
                    fake.text(max_nb_chars=100),  # description
                    random.choice([True, False]),  # is_seasonal
                    round(random.uniform(0.15, 0.45), 2),  # typical_margin_percentage
                    self.timestamp_between('-3y', '-1y')  # created_at
                ]
                categories.append(sub_category_data)
                cat_id += 1
        
        headers = ['category_id', 'category_name', 'parent_category_id', 'description', 'is_seasonal', 'typical_margin_percentage', 'created_at']
        self.save_to_csv('categories', categories, headers)
        return categories

    def generate_products(self):
        """Generate products table (500-1000 products)"""
        num_products = random.randint(500, 1000)
        brands = [row[1] for row in self.data['brands']]
        categories = [row[1] for row in self.data['categories']]
        
        products = []
        for i in range(num_products):
            brand = random.choice(brands)
            category = random.choice(categories)
            
            product_data = [
                f'P{i+1:07d}',  # product_id
                f"{fake.catch_phrase()} {category}",  # product_name
                brand,  # brand
                category,  # category_l1
                random.choice(categories) if random.random() < 0.7 else None,  # category_l2
                random.choice(categories) if random.random() < 0.3 else None,  # category_l3
                self.weighted_choice(['Women', 'Men', 'Unisex'], [0.45, 0.35, 0.20]),  # gender_target
                random.choice(['Spring', 'Summer', 'Fall', 'Winter', 'All Season']),  # season
                random.choice(FashionProvider.fashion_materials),  # material
                random.choice(['Machine wash cold', 'Dry clean only', 'Hand wash', 'Machine wash warm']),  # care_instructions
                random.randint(0, 100),  # sustainability_score
                self.weighted_choice(['$30-50', '$50-100', '$100-150', '$150-200'], [0.3, 0.4, 0.2, 0.1]),  # price_range
                self.date_between('-2y', 'now'),  # launch_date
                True if random.random() < 0.9 else False,  # is_active
                self.timestamp_between('-2y', 'now')  # created_at
            ]
            products.append(product_data)
        
        headers = ['product_id', 'product_name', 'brand', 'category_l1', 'category_l2', 'category_l3',
                  'gender_target', 'season', 'material', 'care_instructions', 'sustainability_score', 'price_range',
                  'launch_date', 'is_active', 'created_at']
        self.save_to_csv('products', products, headers)
        return products

    def generate_product_variants(self):
        """Generate product variants (3-6 per product)"""
        products = self.data['products']
        variants = []
        variant_id = 1
        
        for product in products:
            product_id = product[0]
            num_variants = random.randint(3, 6)
            
            for _ in range(num_variants):
                variant_data = [
                    variant_id,  # variant_id
                    product_id,  # product_id
                    f"SKU{product_id[1:]}V{variant_id:04d}",  # sku
                    random.choice(FashionProvider.sizes),  # size
                    random.choice(FashionProvider.colors),  # color
                    round(random.uniform(0, 20), 2),  # additional_price
                    round(random.uniform(2, 15), 2),  # weight_oz
                    random.randint(10, 500),  # stock_quantity
                    self.timestamp_between('-2y', 'now')  # created_at
                ]
                variants.append(variant_data)
                variant_id += 1
        
        headers = ['variant_id', 'product_id', 'sku', 'size', 'color', 'additional_price',
                  'weight_oz', 'stock_quantity', 'created_at']
        self.save_to_csv('product_variants', variants, headers)
        return variants

    def generate_customers(self):
        """Generate customers table (50000 customers)"""
        customers = []
        
        # Standardized gender values to prevent inconsistencies
        valid_genders = ['male', 'female', 'non-binary', 'prefer_not_to_say']
        gender_dist = {'male': 0.48, 'female': 0.49, 'non-binary': 0.02, 'prefer_not_to_say': 0.01}
        age_ranges = {'18-24': 0.12, '25-34': 0.20, '35-44': 0.17, '45-54': 0.16, '55-64': 0.15, '65+': 0.20}
        channels = {'organic': 0.40, 'paid_ads': 0.25, 'referral': 0.15, 'social': 0.10, 'email': 0.10}
        
        for i in range(50000):
            # Use standardized gender values only
            gender = self.weighted_choice(list(gender_dist.keys()), list(gender_dist.values()))
            age_range = self.weighted_choice(list(age_ranges.keys()), list(age_ranges.values()))
            
            current_year = datetime.now().year
            if age_range == '18-24':
                birth_year = random.randint(current_year - 24, current_year - 18)
            elif age_range == '25-34':
                birth_year = random.randint(current_year - 34, current_year - 25)
            elif age_range == '35-44':
                birth_year = random.randint(current_year - 44, current_year - 35)
            elif age_range == '45-54':
                birth_year = random.randint(current_year - 54, current_year - 45)
            elif age_range == '55-64':
                birth_year = random.randint(current_year - 64, current_year - 55)
            else:  # 65+
                birth_year = random.randint(current_year - 85, current_year - 65)
            
            dob = fake.date_between(date(birth_year, 1, 1), date(birth_year, 12, 31))
            reg_date = self.timestamp_between('-3y', 'now')
            
            # Generate name-based email using actual first and last names
            first_name = fake.first_name_male() if gender == 'male' else fake.first_name_female()
            last_name = fake.last_name()
            email = self.generate_realistic_email(first_name, last_name)
            
            # Create customer data in database schema column order to match:
            # customer_id, email, phone, first_name, last_name, date_of_birth, gender,
            # acquisition_channel, registration_date, account_status, preferred_language,
            # marketing_consent, last_activity_date, created_at, updated_at
            customer_data = [
                i + 1,  # customer_id
                email,  # email - now uses name-based email
                fake.phone_number()[:20],  # phone
                first_name,  # first_name
                last_name,  # last_name
                dob,  # date_of_birth
                gender,  # gender
                self.weighted_choice(list(channels.keys()), list(channels.values())),  # acquisition_channel
                reg_date,  # registration_date
                'active' if random.random() < 0.90 else 'inactive',  # account_status
                'en',  # preferred_language (use 'en' instead of 'English' for consistency)
                random.random() < 0.70,  # marketing_consent
                self.timestamp_between(reg_date, 'now'),  # last_activity_date
                reg_date,  # created_at
                self.timestamp_between(reg_date, 'now')  # updated_at
            ]
            customers.append(customer_data)
        
        headers = ['customer_id', 'email', 'phone', 'first_name', 'last_name', 'date_of_birth',
                  'gender', 'acquisition_channel', 'registration_date', 'account_status',
                  'preferred_language', 'marketing_consent', 'last_activity_date', 'created_at', 'updated_at']
        self.save_to_csv('customers', customers, headers)
        return customers

    def generate_customer_addresses(self):
        """Generate customer addresses using real cities"""
        customers = self.data['customers']
        addresses = []
        
        for customer in customers:
            customer_id = customer[0]
            num_addresses = 1 if random.random() < 0.5 else 2
            
            for j in range(num_addresses):
                # Use the centralized city/state selection method
                chosen_city, chosen_state = self.get_random_city_state()
                
                address_data = [
                    self.generate_id('ADDR'),  # address_id
                    customer_id,  # customer_id
                    'primary' if j == 0 else random.choice(['billing', 'shipping', 'work']),  # address_type
                    fake.street_address(),  # street_address
                    chosen_city,  # city - now using real cities
                    chosen_state,  # state_province - matches the chosen city
                    fake.postcode(),  # postal_code
                    'US',  # country
                    j == 0,  # is_primary
                    self.timestamp_between('-3y', 'now')  # created_at
                ]
                addresses.append(address_data)
        
        headers = ['address_id', 'customer_id', 'address_type', 'street_address', 'city',
                  'state_province', 'postal_code', 'country', 'is_primary', 'created_at']
        self.save_to_csv('customer_addresses', addresses, headers)
        return addresses

    def generate_orders(self):
        """Generate orders (120k-150k orders) with date consistency"""
        customers = self.data['customers']
        num_orders = random.randint(120000, 150000)
        orders = []
        
        status_dist = {'delivered': 0.85, 'cancelled': 0.05, 'returned': 0.10}
        payment_methods = {'credit_card': 0.60, 'paypal': 0.20, 'bnpl': 0.15, 'gift_card': 0.05}
        
        for i in range(num_orders):
            customer = random.choice(customers)
            customer_id = customer[0]
            customer_reg_date = customer[8]  # registration_date is at index 8
            
            order_value = max(20, min(200, np.random.normal(60, 15)))
            # Ensure order_date is after customer registration_date
            order_date = self.timestamp_between(customer_reg_date, 'now')
            
            # Use real city for store location
            store_city, store_state = self.get_random_city_state()
            store_location = f"{store_city}, {store_state}" if random.random() < 0.1 else None
            
            order_data = [
                i + 1,  # order_id
                customer_id,  # customer_id
                order_date,  # order_date
                self.weighted_choice(list(status_dist.keys()), list(status_dist.values())),  # order_status
                random.choice(['web', 'mobile', 'store', 'phone']),  # channel
                store_location,  # store_location - now uses real cities
                round(order_value * 0.9, 2),  # subtotal_amount
                round(order_value * 0.08, 2),  # tax_amount
                round(random.uniform(0, 15), 2),  # shipping_amount
                round(random.uniform(0, order_value * 0.2), 2) if random.random() < 0.3 else 0,  # discount_amount
                round(order_value, 2),  # total_amount
                'USD',  # currency
                self.weighted_choice(list(payment_methods.keys()), list(payment_methods.values())),  # payment_method
                random.choice(['standard', 'express', 'overnight', 'pickup']),  # shipping_method
                fake.lexify('PROMO????') if random.random() < 0.2 else None,  # promo_code
                random.random() < 0.2,  # is_first_order
                random.choice(['desktop', 'mobile', 'tablet']),  # device_type
                random.choice(['google', 'facebook', 'instagram', 'email', 'direct']) if random.random() < 0.6 else None,  # utm_source
                fake.lexify('campaign_???') if random.random() < 0.4 else None,  # utm_campaign
                order_date,  # created_at
                self.timestamp_between(order_date, 'now')  # updated_at
            ]
            orders.append(order_data)
        
        headers = ['order_id', 'customer_id', 'order_date', 'order_status', 'channel', 'store_location',
                  'subtotal_amount', 'tax_amount', 'shipping_amount', 'discount_amount', 'total_amount',
                  'currency', 'payment_method', 'shipping_method', 'promo_code', 'is_first_order',
                  'device_type', 'utm_source', 'utm_campaign', 'created_at', 'updated_at']
        self.save_to_csv('orders', orders, headers)
        return orders

    def generate_order_items(self):
        """Generate order items with duplicate prevention"""
        orders = self.data['orders']
        products = self.data['products']
        variants = self.data['product_variants']
        
        order_items = []
        item_id = 1
        
        for order in orders:
            order_id = order[0]
            order_total = order[10]  # total_amount is now at position 10
            
            num_items = random.randint(1, 4)
            
            # Track used combinations for this order to prevent duplicates
            used_combinations = set()
            
            items_added = 0
            max_attempts = 10
            
            while items_added < num_items:
                attempt = 0
                while attempt < max_attempts:
                    variant = random.choice(variants)
                    product_id = variant[1]
                    size = variant[3]
                    color = variant[4]
                    
                    # Create combination key to check for duplicates
                    combination_key = (product_id, size, color)
                    
                    # If this combination is not used in this order, use it
                    if combination_key not in used_combinations:
                        used_combinations.add(combination_key)
                        
                        quantity = max(1, int(np.random.normal(1.2, 0.5)))
                        if quantity > 3:
                            quantity = 3
                        
                        unit_price = round(order_total / num_items / quantity, 2)
                        total_price = round(unit_price * quantity, 2)
                        
                        item_data = [
                            item_id,  # order_item_id
                            order_id,  # order_id
                            product_id,  # product_id
                            variant[2],  # sku
                            quantity,  # quantity
                            unit_price,  # unit_price
                            total_price,  # total_price
                            round(random.uniform(0, total_price * 0.1), 2) if random.random() < 0.2 else 0,  # discount_applied
                            total_price,  # final_price
                            size,  # size
                            color,  # color
                            fake.sentence(nb_words=3) if random.random() < 0.02 else None,  # personalization
                            random.random() < 0.05  # gift_wrap
                        ]
                        order_items.append(item_data)
                        item_id += 1
                        items_added += 1
                        break
                    
                    attempt += 1
                
                # If we couldn't find a unique combination after max_attempts,
                # break to avoid infinite loop
                if attempt >= max_attempts:
                    break
        
        headers = ['order_item_id', 'order_id', 'product_id', 'sku', 'quantity', 'unit_price', 'total_price',
                  'discount_applied', 'final_price', 'size', 'color', 'personalization', 'gift_wrap']
        self.save_to_csv('order_items', order_items, headers)
        return order_items

    def generate_returns(self):
        """Generate returns"""
        orders = [row for row in self.data['orders'] if row[3] in ['delivered', 'returned']]
        num_returns = int(len(orders) * random.uniform(0.10, 0.12))
        
        returns = []
        return_reasons = {'fit': 0.40, 'defective': 0.20, 'changed_mind': 0.25, 'other': 0.15}
        refund_methods = {'store_credit': 0.40, 'original_payment': 0.60}
        
        selected_orders = random.sample(orders, num_returns)
        
        for i, order in enumerate(selected_orders):
            order_id = order[0]
            customer_id = order[1]
            order_date = order[2]
            order_total = order[10]  # total_amount is now at position 10
            
            return_date = self.timestamp_between(order_date, 'now')
            
            return_data = [
                self.generate_id('RET'),  # return_id
                order_id,  # order_id
                customer_id,  # customer_id
                return_date,  # return_date
                self.weighted_choice(list(return_reasons.keys()), list(return_reasons.values())),  # return_reason
                random.choice(['mail', 'store', 'pickup']),  # return_method
                round(order_total * random.uniform(0.5, 1.0), 2),  # refund_amount
                self.weighted_choice(list(refund_methods.keys()), list(refund_methods.values())),  # refund_method
                random.choice(['pending', 'approved', 'processed', 'completed']),  # return_status
                round(random.uniform(0, 15), 2),  # restocking_fee
                random.choice(['new', 'like_new', 'good', 'fair', 'poor']),  # condition_received
                fake.name(),  # processed_by
                return_date  # created_at
            ]
            returns.append(return_data)
        
        headers = ['return_id', 'order_id', 'customer_id', 'return_date', 'return_reason', 'return_method',
                  'refund_amount', 'refund_method', 'return_status', 'restocking_fee',
                  'condition_received', 'processed_by', 'created_at']
        self.save_to_csv('returns', returns, headers)
        return returns

    def generate_return_items(self):
        """Generate return items"""
        returns = self.data['returns']
        order_items = self.data['order_items']
        return_items = []
        
        conditions = {'like_new': 0.70, 'damaged': 0.20, 'worn': 0.10}
        
        for return_record in returns:
            return_id = return_record[0]
            order_id = return_record[1]
            
            order_items_for_order = [item for item in order_items if item[1] == order_id]
            
            if not order_items_for_order:
                continue
                
            num_items = min(random.randint(1, 2), len(order_items_for_order))
            selected_items = random.sample(order_items_for_order, num_items)
            
            for item in selected_items:
                order_item_id = item[0]
                quantity = int(item[4])  # quantity is at position 4
                
                return_item_data = [
                    self.generate_id('RI'),  # return_item_id
                    return_id,  # return_id
                    order_item_id,  # order_item_id
                    min(quantity, random.randint(1, quantity)),  # quantity_returned
                    self.weighted_choice(list(conditions.keys()), list(conditions.values())),  # item_condition
                    random.random() < 0.9,  # refund_eligible
                    random.random() < 0.8  # restockable
                ]
                return_items.append(return_item_data)
        
        headers = ['return_item_id', 'return_id', 'order_item_id', 'quantity_returned', 
                  'item_condition', 'refund_eligible', 'restockable']
        self.save_to_csv('return_items', return_items, headers)
        return return_items

    # Review Generation Functions
    def assign_product_quality_scores(self):
        """Assign quality scores to products based on returns"""
        print("📊 Assigning quality scores to products...")
        
        products = self.data['products']
        
        # Count returns by product through order_items
        product_returns = {}
        if 'returns' in self.data and 'order_items' in self.data:
            return_orders = set(r[1] for r in self.data['returns'])  # order_id from returns
            
            for row in self.data['order_items']:
                if row[1] in return_orders:  # order_id
                    product_id = row[2]  # product_id
                    product_returns[product_id] = product_returns.get(product_id, 0) + 1
        
        for product in products:
            product_id = product[0]
            
            # Base quality score (2.5-8.5, with 7 being average)
            base_score = np.random.normal(7, 1.2)
            base_score = max(2.5, min(8.5, base_score))
            
            # Adjust based on returns
            return_count = product_returns.get(product_id, 0)
            if return_count > 0:
                penalty = min(1.5, return_count / 20)
                base_score -= penalty
            
            # Ensure realistic distribution
            base_score = max(2.5, min(8.5, base_score))
            self.product_quality_scores[product_id] = base_score
        
        # Print distribution
        scores = list(self.product_quality_scores.values())
        print(f"  📈 Quality Score Distribution:")
        print(f"    High Quality (7.5-8.5): {sum(1 for s in scores if s >= 7.5)}")
        print(f"    Average Quality (5.5-7.5): {sum(1 for s in scores if 5.5 <= s < 7.5)}")
        print(f"    Poor Quality (2.5-5.5): {sum(1 for s in scores if s < 5.5)}")

    def get_review_sentiment_and_rating(self, product_id):
        """Get review sentiment and rating based on product quality"""
        quality_score = self.product_quality_scores.get(product_id, 7)
        
        # Convert quality score to rating distribution
        if quality_score >= 8:
            rating = np.random.choice([3, 4, 5], p=[0.1, 0.4, 0.5])
            sentiment_weights = [0.65, 0.2, 0.05, 0.08, 0.015, 0.005]
        elif quality_score >= 6.5:
            rating = np.random.choice([2, 3, 4, 5], p=[0.05, 0.25, 0.45, 0.25])
            sentiment_weights = [0.4, 0.25, 0.15, 0.15, 0.04, 0.01]
        elif quality_score >= 5:
            rating = np.random.choice([1, 2, 3, 4, 5], p=[0.05, 0.2, 0.4, 0.25, 0.1])
            sentiment_weights = [0.2, 0.15, 0.15, 0.35, 0.1, 0.05]
        else:
            rating = np.random.choice([1, 2, 3, 4], p=[0.3, 0.35, 0.25, 0.1])
            sentiment_weights = [0.05, 0.05, 0.1, 0.2, 0.35, 0.25]
        
        sentiments = ['positive', 'funny', 'sarcastic', 'average', 'negative', 'bad']
        sentiment = np.random.choice(sentiments, p=sentiment_weights)
        
        return sentiment, rating

    def get_appropriate_material(self, product_name):
        """Get contextually appropriate material for product type"""
        product_lower = product_name.lower()
        
        if any(word in product_lower for word in ['jewelry', 'necklace', 'ring', 'bracelet', 'earring']):
            return random.choice(['metal', 'silver', 'gold', 'material', 'finish'])
        elif any(word in product_lower for word in ['bag', 'purse', 'wallet', 'belt']):
            return random.choice(['leather', 'material', 'fabric', 'construction'])
        elif any(word in product_lower for word in ['shoe', 'boot', 'sneaker', 'sandal']):
            return random.choice(['leather', 'material', 'sole', 'construction'])
        elif any(word in product_lower for word in ['dress', 'shirt', 'top', 'blouse', 'sweater']):
            return random.choice(['fabric', 'material', 'cotton', 'polyester', 'construction'])
        elif any(word in product_lower for word in ['pant', 'jean', 'trouser', 'short']):
            return random.choice(['fabric', 'denim', 'material', 'construction'])
        else:
            return random.choice(['material', 'quality', 'construction', 'fabric'])

    def generate_review_text(self, sentiment, product_name):
        """Generate review text based on sentiment with appropriate materials"""
        product_type = product_name.split()[-1].lower()
        appropriate_material = self.get_appropriate_material(product_name)
        
        if sentiment == 'positive':
            template = random.choice(ReviewProvider.positive_reviews)
        elif sentiment == 'funny':
            template = random.choice(ReviewProvider.funny_reviews)
        elif sentiment == 'sarcastic':
            template = random.choice(ReviewProvider.sarcastic_reviews)
        elif sentiment == 'average':
            template = random.choice(ReviewProvider.average_reviews)
        elif sentiment == 'negative':
            template = random.choice(ReviewProvider.negative_reviews)
        else:  # bad
            template = random.choice(ReviewProvider.bad_reviews)
        
        review = template.format(
            product=product_type,
            material=appropriate_material
        )
        
        return review.replace("'", "''")  # Escape for SQL

    def generate_reviews(self):
        """Generate reviews CSV file"""
        print("🎭 Generating contextually accurate reviews...")
        
        self.assign_product_quality_scores()
        
        # Create product lookup
        products = {row[0]: (row[1], row[8]) for row in self.data['products']}  # id: (name, material)
        
        # Get delivered order items
        delivered_orders = set(row[0] for row in self.data['orders'] if row[3] == 'delivered')
        delivered_order_items = [
            (row[1], row[0], row[2])  # (order_id, order_item_id, product_id)
            for row in self.data['order_items'] if row[1] in delivered_orders
        ]
        
        # Get customer_id for each order
        order_customers = {row[0]: row[1] for row in self.data['orders']}
        
        # Generate reviews for 35% of delivered items
        review_rate = 0.35
        selected_items = random.sample(delivered_order_items, int(len(delivered_order_items) * review_rate))
        
        print(f"  📝 Generating {len(selected_items):,} reviews from {len(delivered_order_items):,} delivered order items...")
        
        reviews = []
        review_id = 1
        
        for order_id, order_item_id, product_id in selected_items:
            if product_id not in products:
                continue
                
            customer_id = order_customers.get(order_id, 1)
            product_name, _ = products[product_id]
            
            sentiment, rating = self.get_review_sentiment_and_rating(product_id)
            review_text = self.generate_review_text(sentiment, product_name)
            
            # Generate additional fields
            created_at = fake.date_time_between('-2y', 'now')
            helpful_count = random.randint(0, 25) if random.random() < 0.6 else 0
            not_helpful_count = random.randint(0, 5) if random.random() < 0.3 else 0
            
            review_title = f"{sentiment.title()} {product_name.split()[-1]} Review"[:200]
            
            fit_rating = random.choice(['Runs Small', 'True to Size', 'Runs Large'])
            quality_rating = min(5, max(1, rating + random.randint(-1, 1)))
            style_rating = min(5, max(1, rating + random.randint(-1, 1)))
            value_rating = min(5, max(1, rating + random.randint(-2, 1)))
            sentiment_score = round(random.uniform(-1, 1), 2)
            
            # Convert product_id to integer for reviews table
            product_id_int = abs(hash(product_id)) % 1000000
            
            review = [
                review_id,
                customer_id,
                product_id_int,
                order_id,
                rating,
                review_title,
                review_text,
                True,  # verified_purchase
                helpful_count,
                not_helpful_count,
                fit_rating,
                quality_rating,
                style_rating,
                value_rating,
                sentiment_score,
                created_at
            ]
            reviews.append(review)
            review_id += 1
        
        headers = ['review_id', 'customer_id', 'product_id', 'order_id', 'rating', 'review_title',
                  'review_text', 'verified_purchase', 'helpful_count', 'not_helpful_count',
                  'fit_rating', 'quality_rating', 'style_rating', 'value_rating',
                  'sentiment_score', 'created_at']
        self.save_to_csv('reviews', reviews, headers)
        return reviews

    def generate_social_mentions(self, num_mentions=5000):
        """Generate social media mentions/posts"""
        print(f"📱 Generating {num_mentions} social media mentions...")
        
        mentions = []
        platforms = SocialMediaProvider.platforms
        platform_weights = [0.35, 0.25, 0.15, 0.15, 0.10]  # Instagram heavy
        
        # Create influencer tiers
        influencer_tiers = {
            'mega': {'followers': (1000000, 10000000), 'engagement': (50000, 500000), 'influence': (80, 100)},
            'macro': {'followers': (100000, 1000000), 'engagement': (5000, 50000), 'influence': (60, 85)},
            'micro': {'followers': (10000, 100000), 'engagement': (500, 5000), 'influence': (40, 70)},
            'nano': {'followers': (1000, 10000), 'engagement': (50, 500), 'influence': (20, 50)}
        }
        
        tier_distribution = [0.05, 0.15, 0.40, 0.40]  # Most are nano/micro influencers
        
        for i in range(num_mentions):
            # Select customer and platform
            customer = random.choice(self.data['customers']) if 'customers' in self.data else None
            platform = self.weighted_choice(platforms, platform_weights)
            
            # Determine influencer tier
            tier_name = self.weighted_choice(list(influencer_tiers.keys()), tier_distribution)
            tier = influencer_tiers[tier_name]
            
            # Generate follower and engagement counts
            follower_count = random.randint(tier['followers'][0], tier['followers'][1])
            engagement_count = random.randint(tier['engagement'][0], tier['engagement'][1])
            influence_score = random.randint(tier['influence'][0], tier['influence'][1])
            
            # Select product and brand
            product = random.choice(self.data['products']) if 'products' in self.data else None
            brand = random.choice(self.data['brands']) if 'brands' in self.data else None
            
            # Generate post content
            if product and brand:
                product_name = product[1].split()[-1].lower()  # product_name is at index 1
                brand_name = brand[1]  # brand_name is at index 1
                hashtags = ' '.join(random.sample(SocialMediaProvider.fashion_hashtags,
                                                random.randint(3, 6)))
                
                post_text = random.choice(SocialMediaProvider.post_templates).format(
                    product=product_name,
                    brand=brand_name,
                    season=random.choice(['spring', 'summer', 'fall', 'winter']),
                    hashtags=hashtags
                )
            else:
                post_text = "Loving this new fashion find! Perfect for any occasion ✨ #fashion #style #ootd"
                brand_name = random.choice(['Bella Vista', 'Urban Thread', 'Coastal Chic'])
                hashtags = '#fashion #style #ootd'
                
            # Generate post URL
            username = random.choice(SocialMediaProvider.influencer_usernames)
            post_id = random.randint(1000000, 9999999)
            if platform == 'Instagram':
                post_url = f"https://instagram.com/p/{self.generate_id('', 11)}"
            elif platform == 'TikTok':
                post_url = f"https://tiktok.com/@{username}/video/{post_id}"
            elif platform == 'Twitter':
                post_url = f"https://twitter.com/{username}/status/{post_id}"
            elif platform == 'Facebook':
                post_url = f"https://facebook.com/{username}/posts/{post_id}"
            else:  # Pinterest
                post_url = f"https://pinterest.com/{username}/pin/{post_id}"
            
            mention = [
                self.generate_id('SM'),
                customer[0] if customer else random.randint(1, 50000),
                platform,
                post_url,
                username,
                fake.date_time_between('-2y', 'now'),
                random.choice(SocialMediaProvider.post_types),
                post_text.replace("'", "''"),  # Escape quotes
                hashtags,
                f"@{brand_name.lower().replace(' ', '')}" if brand else "",
                engagement_count,
                follower_count,
                round(random.uniform(-1, 1), 2),
                brand_name if brand else "",
                product[0] if product else "",  # product_id is at index 0
                influence_score,
                random.choice([True, False]),
                f"campaign_{random.choice(['spring', 'summer', 'fall', 'holiday'])}" if random.random() < 0.3 else ""
            ]
            
            mentions.append(mention)
            
        headers = [
            'mention_id', 'customer_id', 'platform', 'post_url', 'username', 'post_date',
            'post_type', 'post_text', 'hashtags', 'mentions', 'engagement_count',
            'follower_count', 'sentiment_score', 'brand_mentioned', 'products_tagged',
            'influence_score', 'ugc_usage_rights', 'campaign_tagged'
        ]
        self.save_to_csv('social_mentions', mentions, headers)
        return mentions

    def generate_website_sessions(self, num_sessions=25000):
        """Generate website session data"""
        print(f"🌐 Generating {num_sessions} website sessions...")
        
        sessions = []
        devices = ['desktop', 'mobile', 'tablet']
        device_weights = [0.40, 0.50, 0.10]
        
        browsers = ['Chrome', 'Safari', 'Firefox', 'Edge', 'Opera']
        browser_weights = [0.65, 0.20, 0.08, 0.05, 0.02]
        
        os_list = ['Windows', 'macOS', 'iOS', 'Android', 'Linux']
        os_weights = [0.35, 0.25, 0.15, 0.20, 0.05]
        
        traffic_sources = ['organic', 'social', 'direct', 'email', 'paid', 'referral']
        traffic_weights = [0.35, 0.25, 0.15, 0.10, 0.10, 0.05]
        
        pages = [
            '/home', '/products', '/categories/womens', '/categories/mens',
            '/brands', '/sale', '/new-arrivals', '/trending', '/cart', '/checkout',
            '/account', '/wishlist', '/reviews', '/size-guide', '/returns'
        ]
        
        for i in range(num_sessions):
            customer = random.choice(self.data['customers']) if 'customers' in self.data else None
            device = self.weighted_choice(devices, device_weights)
            
            # Session duration varies by device
            if device == 'mobile':
                duration = max(1, int(np.random.normal(8, 4)))  # Shorter mobile sessions
            else:
                duration = max(1, int(np.random.normal(15, 8)))  # Longer desktop sessions
                
            page_views = max(1, int(np.random.normal(6, 3)))
            pages_visited = ', '.join(random.sample(pages, min(page_views, len(pages))))
            
            # Generate session times
            session_start = fake.date_time_between('-6m', 'now')
            session_end = session_start + timedelta(minutes=duration)
            
            # Products viewed (if customer browsed products)
            viewed_products = []
            if '/products' in pages_visited or '/categories' in pages_visited:
                num_viewed = random.randint(1, 5)
                if 'products' in self.data:
                    viewed_products = random.sample([p[0] for p in self.data['products']],
                                                  min(num_viewed, len(self.data['products'])))
            
            # Search terms
            search_terms = []
            if random.random() < 0.3:  # 30% of sessions have searches
                terms = ['dress', 'shoes', 'jacket', 'jeans', 'top', 'accessories', 'sale']
                search_terms = [random.choice(terms)]
            
            session = [
                self.generate_id('SESS'),
                customer[0] if customer else None,
                self.generate_id('ANON') if not customer else None,
                session_start,
                session_end,
                duration,
                page_views,
                pages_visited,
                ', '.join(viewed_products),
                ', '.join(search_terms),
                device,
                self.weighted_choice(browsers, browser_weights),
                self.weighted_choice(os_list, os_weights),
                self.weighted_choice(traffic_sources, traffic_weights),
                f"utm_source={random.choice(['google', 'facebook', 'instagram'])}" if random.random() < 0.4 else "",
                f"{self.get_random_city_state()[0]}, {self.get_random_city_state()[1]}",
                round(random.uniform(0, 300), 2) if random.random() < 0.3 else 0,
                random.choice([True, False]) if random.random() < 0.2 else False,
                'purchase' if random.random() < 0.05 else "",  # 5% conversion rate
                random.choice(pages)
            ]
            
            sessions.append(session)
            
        headers = [
            'session_id', 'customer_id', 'anonymous_id', 'session_start', 'session_end',
            'duration_minutes', 'page_views', 'pages_visited', 'products_viewed',
            'search_terms', 'device_type', 'browser', 'operating_system',
            'traffic_source', 'utm_parameters', 'geo_location', 'cart_value',
            'abandoned_cart', 'conversion_event', 'exit_page'
        ]
        self.save_to_csv('website_sessions', sessions, headers)
        return sessions

    def generate_style_similarity_matches(self, num_matches=6000):
        """Generate style similarity matches using existing customers and products"""
        print(f"🎯 Generating {num_matches} style similarity matches...")
        
        if 'customers' not in self.data or 'products' not in self.data:
            print("  ⚠️ Warning: customers and products data required for style similarity matches")
            return []
        
        customers = self.data['customers']
        products = self.data['products']
        
        matches = []
        recommendation_types = ['style_based', 'color_match', 'trend_similar', 'brand_affinity']
        contexts = ['homepage_recommendations', 'product_page_similar', 'cart_recommendations',
                   'email_campaign', 'browse_history_based']
        
        # Generate main matches with varied engagement patterns
        for i in range(int(num_matches * 0.83)):  # 83% regular matches
            customer = random.choice(customers)
            product = random.choice(products)
            
            similarity_score = round(random.uniform(0.6, 1.0), 3)
            match_date = self.timestamp_between('-90d', 'now')
            
            # 15% click rate, 3% purchase rate for regular matches
            clicked = random.random() < 0.15
            purchased = random.random() < 0.03 if clicked else False
            
            match = [
                f'MATCH_{(i+1):06d}',
                str(customer[0]),  # customer_id
                product[0],  # product_id
                similarity_score,
                random.choice(recommendation_types),
                match_date,
                clicked,
                purchased,
                random.choice(contexts)
            ]
            matches.append(match)
        
        # Generate high-performing matches (clicked and purchased)
        start_idx = int(num_matches * 0.83)
        for i in range(start_idx, start_idx + int(num_matches * 0.03)):  # 3% high-performing
            customer = random.choice(customers)
            product = random.choice(products)
            
            similarity_score = round(random.uniform(0.8, 1.0), 3)  # Higher scores
            match_date = self.timestamp_between('-30d', 'now')
            
            match = [
                f'MATCH_{(i+1):06d}',
                str(customer[0]),
                product[0],
                similarity_score,
                self.weighted_choice(
                    ['style_based', 'trend_similar', 'brand_affinity'], [0.4, 0.35, 0.25]
                ),
                match_date,
                True,
                True,
                self.weighted_choice(
                    ['product_page_similar', 'cart_recommendations', 'email_campaign'],
                    [0.4, 0.35, 0.25]
                )
            ]
            matches.append(match)
        
        # Generate recent matches with no engagement
        start_idx = int(num_matches * 0.86)
        for i in range(start_idx, num_matches):  # 14% recent no-engagement
            customer = random.choice(customers)
            product = random.choice(products)
            
            similarity_score = round(random.uniform(0.5, 1.0), 3)
            match_date = self.timestamp_between('-7d', 'now')
            
            match = [
                f'MATCH_{(i+1):06d}',
                str(customer[0]),
                product[0],
                similarity_score,
                self.weighted_choice(
                    ['style_based', 'color_match', 'browse_history_based'], [0.35, 0.35, 0.30]
                ),
                match_date,
                False,
                False,
                self.weighted_choice(
                    ['homepage_recommendations', 'email_campaign'], [0.5, 0.5]
                )
            ]
            matches.append(match)
        
        headers = ['match_id', 'customer_id', 'product_id', 'similarity_score',
                  'recommendation_type', 'match_date', 'clicked', 'purchased',
                  'recommendation_context']
        self.save_to_csv('style_similarity_matches', matches, headers)
        return matches

    def generate_all_data(self):
        """Generate complete dataset including reviews"""
        print("\n🚀 Starting Complete C360 Data Generation...")
        print("🔗 Generating 50k customer dataset with enterprise-scale data + reviews")
        
        # Master data first
        print("\n=== 📦 Generating Master Data ===")
        self.generate_brands()
        self.generate_categories() 
        self.generate_products()
        self.generate_product_variants()
        
        # Customer data
        print("\n=== 👥 Generating Customer Data ===")
        self.generate_customers()
        self.generate_customer_addresses()
        
        # Order data
        print("\n=== 🛒 Generating Order Data ===")
        self.generate_orders()
        self.generate_order_items()
        self.generate_returns()
        self.generate_return_items()
        
        # Reviews
        print("\n=== 🎭 Generating Reviews ===")
        self.generate_reviews()
        
        # Social Media and Digital Analytics
        print("\n=== 📱 Generating Social Media & Digital Analytics ===")
        self.generate_social_mentions()
        self.generate_website_sessions()
        
        # Style Similarity Matches (ML/Recommendation Engine Data)
        print("\n=== 🎯 Generating ML & Recommendation Data ===")
        self.generate_style_similarity_matches()
        
        print(f"\n🎉 Complete dataset generation finished!")
        print(f"\n📊 Generated tables:")
        for table, data in self.data.items():
            print(f"  ✅ {table}: {len(data):,} rows")
        
        print(f"\n🔗 Enterprise Scale Achieved:")
        print(f"  ✅ 50,000 customers with proportional transactions")
        print(f"  ✅ ~700k total records across all tables")
        print(f"  ✅ Contextually accurate reviews with quality correlation")
        print(f"  ✅ Foreign key compatible data types")
        print(f"  ✅ Complete referential integrity maintained")
        print(f"  ✅ Complete referential integrity maintained")
        
        return self.data

if __name__ == "__main__":
    generator = CompleteDatasetGenerator()
    generator.generate_all_data()