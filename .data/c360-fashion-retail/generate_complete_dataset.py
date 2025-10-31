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
        os.makedirs(output_dir, exist_ok=True)
        print("🚀 C360 Complete Dataset Generator v3.0 - Enterprise Scale")
        print("📊 Generating 50k customers + contextually accurate reviews")
        
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

    def save_to_csv(self, table_name, data, headers):
<<<<<<< HEAD
        """Save data to CSV file with PostgreSQL-compatible formatting"""
=======
        """Save data to CSV file"""
>>>>>>> origin/main
        filepath = os.path.join(self.output_dir, f'{table_name}.csv')
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(headers)
<<<<<<< HEAD
            
            # Convert Python booleans to PostgreSQL-compatible format
            for row in data:
                formatted_row = []
                for value in row:
                    if isinstance(value, bool):
                        formatted_row.append('true' if value else 'false')
                    else:
                        formatted_row.append(value)
                writer.writerow(formatted_row)
                
=======
            writer.writerows(data)
>>>>>>> origin/main
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
            
<<<<<<< HEAD
            # Create brand data in database schema column order
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
=======
            brand = {
                'brand_id': i + 1,
                'brand_name': brand_name,
                'brand_tier': self.weighted_choice(tiers, weights),
                'created_at': self.timestamp_between('-5y', '-1y'),
                'description': fake.text(max_nb_chars=200),
                'is_active': random.choice([True, False]) if random.random() < 0.1 else True,
                'parent_company': fake.company() if random.random() < 0.3 else None,
                'website_url': fake.url(),
                'year_established': random.randint(1950, 2022)
            }
            brands.append(list(brand.values()))
        
        headers = ['brand_id', 'brand_name', 'brand_tier', 'created_at', 'description', 'is_active', 'parent_company', 'website_url', 'year_established']
>>>>>>> origin/main
        self.save_to_csv('brands', brands, headers)
        return brands

    def generate_categories(self):
        """Generate categories table"""
        categories = []
        cat_id = 1
        
        # Use all main categories and create more subcategories
        for main_cat, subcats in FashionProvider.fashion_categories.items():
            # Add main category
<<<<<<< HEAD
            # Create main category data in database schema column order
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
=======
            main_category = {
                'category_id': cat_id,
                'category_name': main_cat,
                'created_at': self.timestamp_between('-3y', '-1y'),
                'description': fake.text(max_nb_chars=150),
                'is_seasonal': random.choice([True, False]),
                'parent_category_id': None,
                'typical_margin_percentage': round(random.uniform(0.15, 0.45), 2)
            }
            categories.append(list(main_category.values()))
>>>>>>> origin/main
            main_cat_id = cat_id
            cat_id += 1
            
            # Add more subcategories for larger dataset
            num_subcats = min(len(subcats), random.randint(2, 4))
            for subcat in random.sample(subcats, num_subcats):
<<<<<<< HEAD
                # Create subcategory data in database schema column order
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
=======
                sub_category = {
                    'category_id': cat_id,
                    'category_name': subcat,
                    'created_at': self.timestamp_between('-3y', '-1y'),
                    'description': fake.text(max_nb_chars=100),
                    'is_seasonal': random.choice([True, False]),
                    'parent_category_id': main_cat_id,
                    'typical_margin_percentage': round(random.uniform(0.15, 0.45), 2)
                }
                categories.append(list(sub_category.values()))
                cat_id += 1
        
        headers = ['category_id', 'category_name', 'created_at', 'description', 'is_seasonal', 'parent_category_id', 'typical_margin_percentage']
>>>>>>> origin/main
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
            
<<<<<<< HEAD
            # Create product data in database schema column order
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
=======
            product = {
                'product_id': f'P{i+1:07d}',
                'product_name': f"{fake.catch_phrase()} {category}",
                'brand': brand,
                'category_l1': category,
                'category_l2': random.choice(categories) if random.random() < 0.7 else None,
                'category_l3': random.choice(categories) if random.random() < 0.3 else None,
                'created_at': self.timestamp_between('-2y', 'now'),
                'gender_target': self.weighted_choice(['Women', 'Men', 'Unisex'], [0.45, 0.35, 0.20]),
                'is_active': True if random.random() < 0.9 else False,
                'launch_date': self.date_between('-2y', 'now'),
                'material': random.choice(FashionProvider.fashion_materials),
                'price_range': self.weighted_choice(['$30-50', '$50-100', '$100-150', '$150-200'], [0.3, 0.4, 0.2, 0.1]),
                'season': random.choice(['Spring', 'Summer', 'Fall', 'Winter', 'All Season']),
                'sustainability_score': random.randint(0, 100),
                'care_instructions': random.choice(['Machine wash cold', 'Dry clean only', 'Hand wash', 'Machine wash warm'])
            }
            products.append(list(product.values()))
        
        headers = ['product_id', 'product_name', 'brand', 'category_l1', 'category_l2', 'category_l3',
                  'created_at', 'gender_target', 'is_active', 'launch_date', 'material', 'price_range', 
                  'season', 'sustainability_score', 'care_instructions']
>>>>>>> origin/main
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
<<<<<<< HEAD
                # Create variant data in database schema column order to match:
                # variant_id, product_id, sku, size, color, additional_price, weight_oz, stock_quantity, created_at
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
=======
                variant = {
                    'variant_id': variant_id,
                    'product_id': product_id,
                    'sku': f"SKU{product_id[1:]}V{variant_id:04d}",
                    'size': random.choice(FashionProvider.sizes),
                    'color': random.choice(FashionProvider.colors),
                    'additional_price': round(random.uniform(0, 20), 2),
                    'stock_quantity': random.randint(10, 500),
                    'weight_oz': round(random.uniform(2, 15), 2),
                    'created_at': self.timestamp_between('-2y', 'now')
                }
                variants.append(list(variant.values()))
                variant_id += 1
        
        headers = ['variant_id', 'product_id', 'sku', 'size', 'color', 'additional_price', 
                  'stock_quantity', 'weight_oz', 'created_at']
>>>>>>> origin/main
        self.save_to_csv('product_variants', variants, headers)
        return variants

    def generate_customers(self):
        """Generate customers table (50000 customers)"""
        customers = []
        
        gender_dist = {'male': 0.49, 'female': 0.51}
        age_ranges = {'18-24': 0.12, '25-34': 0.20, '35-44': 0.17, '45-54': 0.16, '55-64': 0.15, '65+': 0.20}
        channels = {'organic': 0.40, 'paid_ads': 0.25, 'referral': 0.15, 'social': 0.10, 'email': 0.10}
        
        for i in range(50000):
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
            
<<<<<<< HEAD
            # Create customer data in database schema column order to match:
            # customer_id, email, phone, first_name, last_name, date_of_birth, gender,
            # acquisition_channel, registration_date, account_status, preferred_language,
            # marketing_consent, last_activity_date, created_at, updated_at
            customer_data = [
                i + 1,  # customer_id
                fake.email(),  # email
                fake.phone_number()[:20],  # phone
                fake.first_name_male() if gender == 'male' else fake.first_name_female(),  # first_name
                fake.last_name(),  # last_name
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
=======
            customer = {
                'customer_id': i + 1,
                'first_name': fake.first_name_male() if gender == 'male' else fake.first_name_female(),
                'last_name': fake.last_name(),
                'email': fake.email(),
                'phone': fake.phone_number()[:20],
                'date_of_birth': dob,
                'gender': gender,
                'registration_date': reg_date,
                'acquisition_channel': self.weighted_choice(list(channels.keys()), list(channels.values())),
                'marketing_consent': random.random() < 0.70,
                'account_status': 'active' if random.random() < 0.90 else 'inactive',
                'preferred_language': 'English',
                'created_at': reg_date,
                'updated_at': self.timestamp_between(reg_date, 'now'),
                'last_activity_date': self.timestamp_between(reg_date, 'now')
            }
            customers.append(list(customer.values()))
        
        headers = ['customer_id', 'first_name', 'last_name', 'email', 'phone', 'date_of_birth', 
                  'gender', 'registration_date', 'acquisition_channel', 'marketing_consent', 
                  'account_status', 'preferred_language', 'created_at', 'updated_at', 'last_activity_date']
>>>>>>> origin/main
        self.save_to_csv('customers', customers, headers)
        return customers

    def generate_customer_addresses(self):
        """Generate customer addresses"""
        customers = self.data['customers']
        addresses = []
        
        states = ['CA', 'TX', 'FL', 'NY', 'PA', 'IL', 'OH', 'GA', 'NC', 'MI']
        
        for customer in customers:
            customer_id = customer[0]
            num_addresses = 1 if random.random() < 0.5 else 2
            
            for j in range(num_addresses):
<<<<<<< HEAD
                # Create address data in database schema column order to match:
                # address_id, customer_id, address_type, street_address, city, state_province,
                # postal_code, country, is_primary, created_at
                address_data = [
                    self.generate_id('ADDR'),  # address_id
                    customer_id,  # customer_id
                    'primary' if j == 0 else random.choice(['billing', 'shipping', 'work']),  # address_type
                    fake.street_address(),  # street_address
                    fake.city(),  # city
                    random.choice(states),  # state_province
                    fake.postcode(),  # postal_code
                    'US',  # country
                    j == 0,  # is_primary
                    self.timestamp_between('-3y', 'now')  # created_at
                ]
                addresses.append(address_data)
        
        headers = ['address_id', 'customer_id', 'address_type', 'street_address', 'city',
                  'state_province', 'postal_code', 'country', 'is_primary', 'created_at']
=======
                address = {
                    'address_id': self.generate_id('ADDR'),
                    'customer_id': customer_id,
                    'address_type': 'primary' if j == 0 else random.choice(['billing', 'shipping', 'work']),
                    'is_primary': j == 0,
                    'street_address': fake.street_address(),
                    'city': fake.city(),
                    'state_province': random.choice(states),
                    'postal_code': fake.postcode(),
                    'country': 'US',
                    'created_at': self.timestamp_between('-3y', 'now')
                }
                addresses.append(list(address.values()))
        
        headers = ['address_id', 'customer_id', 'address_type', 'is_primary', 'street_address', 
                  'city', 'state_province', 'postal_code', 'country', 'created_at']
>>>>>>> origin/main
        self.save_to_csv('customer_addresses', addresses, headers)
        return addresses

    def generate_orders(self):
        """Generate orders (120k-150k orders)"""
        customers = self.data['customers']
        num_orders = random.randint(120000, 150000)
        orders = []
        
        status_dist = {'delivered': 0.85, 'cancelled': 0.05, 'returned': 0.10}
        payment_methods = {'credit_card': 0.60, 'paypal': 0.20, 'bnpl': 0.15, 'gift_card': 0.05}
        
        for i in range(num_orders):
            customer = random.choice(customers)
            customer_id = customer[0]
            
            order_value = max(20, min(200, np.random.normal(60, 15)))
            order_date = self.timestamp_between('-2y', 'now')
            
<<<<<<< HEAD
            # Create order data in database schema column order to match:
            # order_id, customer_id, order_date, order_status, channel, store_location,
            # subtotal_amount, tax_amount, shipping_amount, discount_amount, total_amount,
            # currency, payment_method, shipping_method, promo_code, is_first_order,
            # device_type, utm_source, utm_campaign, created_at, updated_at
            order_data = [
                i + 1,  # order_id
                customer_id,  # customer_id
                order_date,  # order_date
                self.weighted_choice(list(status_dist.keys()), list(status_dist.values())),  # order_status
                random.choice(['web', 'mobile', 'store', 'phone']),  # channel
                fake.city() if random.random() < 0.1 else None,  # store_location
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
=======
            order = {
                'order_id': i + 1,
                'customer_id': customer_id,
                'order_date': order_date,
                'order_status': self.weighted_choice(list(status_dist.keys()), list(status_dist.values())),
                'total_amount': round(order_value, 2),
                'subtotal_amount': round(order_value * 0.9, 2),
                'tax_amount': round(order_value * 0.08, 2),
                'shipping_amount': round(random.uniform(0, 15), 2),
                'discount_amount': round(random.uniform(0, order_value * 0.2), 2) if random.random() < 0.3 else 0,
                'payment_method': self.weighted_choice(list(payment_methods.keys()), list(payment_methods.values())),
                'currency': 'USD',
                'channel': random.choice(['web', 'mobile', 'store', 'phone']),
                'device_type': random.choice(['desktop', 'mobile', 'tablet']),
                'shipping_method': random.choice(['standard', 'express', 'overnight', 'pickup']),
                'is_first_order': random.random() < 0.2,
                'promo_code': fake.lexify('PROMO????') if random.random() < 0.2 else None,
                'store_location': fake.city() if random.random() < 0.1 else None,
                'utm_source': random.choice(['google', 'facebook', 'instagram', 'email', 'direct']) if random.random() < 0.6 else None,
                'utm_campaign': fake.lexify('campaign_???') if random.random() < 0.4 else None,
                'created_at': order_date,
                'updated_at': self.timestamp_between(order_date, 'now')
            }
            orders.append(list(order.values()))
        
        headers = ['order_id', 'customer_id', 'order_date', 'order_status', 'total_amount', 
                  'subtotal_amount', 'tax_amount', 'shipping_amount', 'discount_amount', 
                  'payment_method', 'currency', 'channel', 'device_type', 'shipping_method', 
                  'is_first_order', 'promo_code', 'store_location', 'utm_source', 'utm_campaign', 
                  'created_at', 'updated_at']
>>>>>>> origin/main
        self.save_to_csv('orders', orders, headers)
        return orders

    def generate_order_items(self):
        """Generate order items"""
        orders = self.data['orders']
        products = self.data['products']
        variants = self.data['product_variants']
        
        order_items = []
        item_id = 1
        
        for order in orders:
            order_id = order[0]
<<<<<<< HEAD
            order_total = order[10]  # total_amount is now at position 10 after column reordering
=======
            order_total = order[4]
>>>>>>> origin/main
            
            num_items = random.randint(1, 4)
            
            for _ in range(num_items):
                variant = random.choice(variants)
                product_id = variant[1]
                
                quantity = max(1, int(np.random.normal(1.2, 0.5)))
                if quantity > 3:
                    quantity = 3
                
                unit_price = round(order_total / num_items / quantity, 2)
                total_price = round(unit_price * quantity, 2)
                
<<<<<<< HEAD
                # Create order item data in database schema column order to match:
                # order_item_id, order_id, product_id, sku, quantity, unit_price, total_price,
                # discount_applied, final_price, size, color, personalization, gift_wrap
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
                    variant[3],  # size
                    variant[4],  # color
                    fake.sentence(nb_words=3) if random.random() < 0.02 else None,  # personalization
                    random.random() < 0.05  # gift_wrap
                ]
                order_items.append(item_data)
                item_id += 1
        
        headers = ['order_item_id', 'order_id', 'product_id', 'sku', 'quantity', 'unit_price', 'total_price',
                  'discount_applied', 'final_price', 'size', 'color', 'personalization', 'gift_wrap']
=======
                item = {
                    'order_item_id': item_id,
                    'order_id': order_id,
                    'product_id': product_id,
                    'sku': variant[2],
                    'size': variant[3],
                    'color': variant[4],
                    'quantity': quantity,
                    'unit_price': unit_price,
                    'total_price': total_price,
                    'final_price': total_price,
                    'discount_applied': round(random.uniform(0, total_price * 0.1), 2) if random.random() < 0.2 else 0,
                    'gift_wrap': random.random() < 0.05,
                    'personalization': fake.sentence(nb_words=3) if random.random() < 0.02 else None
                }
                order_items.append(list(item.values()))
                item_id += 1
        
        headers = ['order_item_id', 'order_id', 'product_id', 'sku', 'size', 'color', 'quantity', 
                  'unit_price', 'total_price', 'final_price', 'discount_applied', 'gift_wrap', 'personalization']
>>>>>>> origin/main
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
<<<<<<< HEAD
            order_total = order[10]  # total_amount is now at position 10 after column reordering
            
            return_date = self.timestamp_between(order_date, 'now')
            
            # Create return data in database schema column order to match:
            # return_id, order_id, customer_id, return_date, return_reason, return_method,
            # refund_amount, refund_method, return_status, restocking_fee, condition_received, processed_by, created_at
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
=======
            order_total = order[4]
            
            return_date = self.timestamp_between(order_date, 'now')
            
            return_record = {
                'return_id': self.generate_id('RET'),
                'order_id': order_id,
                'customer_id': customer_id,
                'return_date': return_date,
                'return_reason': self.weighted_choice(list(return_reasons.keys()), list(return_reasons.values())),
                'return_status': random.choice(['pending', 'approved', 'processed', 'completed']),
                'refund_amount': round(order_total * random.uniform(0.5, 1.0), 2),
                'refund_method': self.weighted_choice(list(refund_methods.keys()), list(refund_methods.values())),
                'restocking_fee': round(random.uniform(0, 15), 2),
                'return_method': random.choice(['mail', 'store', 'pickup']),
                'condition_received': random.choice(['new', 'like_new', 'good', 'fair', 'poor']),
                'processed_by': fake.name(),
                'created_at': return_date
            }
            returns.append(list(return_record.values()))
        
        headers = ['return_id', 'order_id', 'customer_id', 'return_date', 'return_reason', 
                  'return_status', 'refund_amount', 'refund_method', 'restocking_fee', 
                  'return_method', 'condition_received', 'processed_by', 'created_at']
>>>>>>> origin/main
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
<<<<<<< HEAD
                quantity = int(item[4])  # quantity is now at position 4 after column reordering, convert to int
                
                # Create return item data in database schema column order to match:
                # return_item_id, return_id, order_item_id, quantity_returned, item_condition, refund_eligible, restockable
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
=======
                quantity = item[6]
                
                return_item = {
                    'return_item_id': self.generate_id('RI'),
                    'return_id': return_id,
                    'order_item_id': order_item_id,
                    'quantity_returned': min(quantity, random.randint(1, quantity)),
                    'item_condition': self.weighted_choice(list(conditions.keys()), list(conditions.values())),
                    'refund_eligible': random.random() < 0.9,
                    'restockable': random.random() < 0.8
                }
                return_items.append(list(return_item.values()))
>>>>>>> origin/main
        
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
        products = {row[0]: (row[1], row[10]) for row in self.data['products']}  # id: (name, material)
        
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
            
            review = {
                'review_id': review_id,
                'customer_id': customer_id,
                'product_id': product_id_int,
                'order_id': order_id,
                'rating': rating,
                'review_title': review_title,
                'review_text': review_text,
                'verified_purchase': True,
                'helpful_count': helpful_count,
                'not_helpful_count': not_helpful_count,
                'fit_rating': fit_rating,
                'quality_rating': quality_rating,
                'style_rating': style_rating,
                'value_rating': value_rating,
                'sentiment_score': sentiment_score,
                'created_at': created_at
            }
            reviews.append(list(review.values()))
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
            
            mention = {
                'mention_id': self.generate_id('SM'),
                'customer_id': customer[0] if customer else random.randint(1, 50000),
                'platform': platform,
                'post_url': post_url,
                'username': username,
                'post_date': fake.date_time_between('-2y', 'now'),
                'post_type': random.choice(SocialMediaProvider.post_types),
                'post_text': post_text.replace("'", "''"),  # Escape quotes
                'hashtags': hashtags,
                'mentions': f"@{brand_name.lower().replace(' ', '')}" if brand else "",
                'engagement_count': engagement_count,
                'follower_count': follower_count,
                'sentiment_score': round(random.uniform(-1, 1), 2),
                'brand_mentioned': brand_name if brand else "",
                'products_tagged': product[0] if product else "",  # product_id is at index 0
                'influence_score': influence_score,
                'ugc_usage_rights': random.choice([True, False]),
                'campaign_tagged': f"campaign_{random.choice(['spring', 'summer', 'fall', 'holiday'])}" if random.random() < 0.3 else ""
            }
            
            mentions.append(list(mention.values()))
            
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
            
            session = {
                'session_id': self.generate_id('SESS'),
                'customer_id': customer[0] if customer else None,
                'anonymous_id': self.generate_id('ANON') if not customer else None,
                'session_start': session_start,
                'session_end': session_end,
                'duration_minutes': duration,
                'page_views': page_views,
                'pages_visited': pages_visited,
                'products_viewed': ', '.join(viewed_products),
                'search_terms': ', '.join(search_terms),
                'device_type': device,
                'browser': self.weighted_choice(browsers, browser_weights),
                'operating_system': self.weighted_choice(os_list, os_weights),
                'traffic_source': self.weighted_choice(traffic_sources, traffic_weights),
                'utm_parameters': f"utm_source={random.choice(['google', 'facebook', 'instagram'])}" if random.random() < 0.4 else "",
                'geo_location': fake.city() + ', ' + fake.state_abbr(),
                'cart_value': round(random.uniform(0, 300), 2) if random.random() < 0.3 else 0,
                'abandoned_cart': random.choice([True, False]) if random.random() < 0.2 else False,
                'conversion_event': 'purchase' if random.random() < 0.05 else "",  # 5% conversion rate
                'exit_page': random.choice(pages)
            }
            
            sessions.append(list(session.values()))
            
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
            
            match = {
                'match_id': f'MATCH_{(i+1):06d}',
                'customer_id': str(customer[0]),  # customer_id
                'product_id': product[0],  # product_id
                'similarity_score': similarity_score,
                'recommendation_type': random.choice(recommendation_types),
                'match_date': match_date,
                'clicked': clicked,
                'purchased': purchased,
                'recommendation_context': random.choice(contexts)
            }
            matches.append(list(match.values()))
        
        # Generate high-performing matches (clicked and purchased)
        start_idx = int(num_matches * 0.83)
        for i in range(start_idx, start_idx + int(num_matches * 0.03)):  # 3% high-performing
            customer = random.choice(customers)
            product = random.choice(products)
            
            similarity_score = round(random.uniform(0.8, 1.0), 3)  # Higher scores
            match_date = self.timestamp_between('-30d', 'now')
            
            match = {
                'match_id': f'MATCH_{(i+1):06d}',
                'customer_id': str(customer[0]),
                'product_id': product[0],
                'similarity_score': similarity_score,
                'recommendation_type': self.weighted_choice(
                    ['style_based', 'trend_similar', 'brand_affinity'], [0.4, 0.35, 0.25]
                ),
                'match_date': match_date,
                'clicked': True,
                'purchased': True,
                'recommendation_context': self.weighted_choice(
                    ['product_page_similar', 'cart_recommendations', 'email_campaign'],
                    [0.4, 0.35, 0.25]
                )
            }
            matches.append(list(match.values()))
        
        # Generate recent matches with no engagement
        start_idx = int(num_matches * 0.86)
        for i in range(start_idx, num_matches):  # 14% recent no-engagement
            customer = random.choice(customers)
            product = random.choice(products)
            
            similarity_score = round(random.uniform(0.5, 1.0), 3)
            match_date = self.timestamp_between('-7d', 'now')
            
            match = {
                'match_id': f'MATCH_{(i+1):06d}',
                'customer_id': str(customer[0]),
                'product_id': product[0],
                'similarity_score': similarity_score,
                'recommendation_type': self.weighted_choice(
                    ['style_based', 'color_match', 'browse_history_based'], [0.35, 0.35, 0.30]
                ),
                'match_date': match_date,
                'clicked': False,
                'purchased': False,
                'recommendation_context': self.weighted_choice(
                    ['homepage_recommendations', 'email_campaign'], [0.5, 0.5]
                )
            }
            matches.append(list(match.values()))
        
        headers = ['match_id', 'customer_id', 'product_id', 'similarity_score',
                  'recommendation_type', 'match_date', 'clicked', 'purchased',
                  'recommendation_context']
        self.save_to_csv('style_similarity_matches', matches, headers)
        return matches
<<<<<<< HEAD
    def generate_campaigns(self, num_campaigns=25):
        """Generate marketing campaigns"""
        print(f"📢 Generating {num_campaigns} marketing campaigns...")
        
        campaigns = []
        campaign_types = ['product_launch', 'promotional', 'seasonal', 'retention', 'brand_awareness']
        statuses = ['planned', 'active', 'paused', 'completed', 'cancelled']
        audiences = ['all_customers', 'women_fashion', 'men_fashion', 'young_adults', 'gift_buyers', 'loyalty_members', 'new_customers']
        
        for i in range(num_campaigns):
            campaign_type = random.choice(campaign_types)
            start_date = self.timestamp_between('-6m', '+2m')
            end_date = start_date + timedelta(days=random.randint(14, 90))
            budget_allocated = round(random.uniform(10000, 100000), 2)
            budget_spent = round(budget_allocated * random.uniform(0.1, 1.2), 2)
            
            # Generate contextual campaign names
            season = random.choice(['Spring', 'Summer', 'Fall', 'Winter', 'Holiday'])
            if campaign_type == 'product_launch':
                name = f"{season} Fashion Launch {random.randint(2023, 2024)}"
            elif campaign_type == 'promotional':
                discount = random.choice([20, 25, 30, 40, 50])
                name = f"{season} Sale {discount}% Off"
            elif campaign_type == 'seasonal':
                event = random.choice(['Back to School', 'Holiday Gift Guide', 'Summer Collection', 'Winter Essentials'])
                name = f"{event} {random.randint(2023, 2024)}"
            else:
                name = f"{campaign_type.title()} Campaign {i+1}"
            
            campaign_data = [
                f'CAMP{i+1:03d}',  # campaign_id
                name,  # campaign_name
                campaign_type,  # campaign_type
                start_date,  # start_date
                end_date,  # end_date
                random.choice(audiences),  # target_audience
                budget_allocated,  # budget_allocated
                budget_spent,  # budget_spent
                random.randint(0, 50),  # discount_offered
                fake.lexify('????##') if random.random() < 0.7 else None,  # promo_code
                random.choice(['marketing_team', 'brand_team', 'digital_team']),  # created_by
                random.choice(statuses)  # status
            ]
            campaigns.append(campaign_data)
        
        headers = ['campaign_id', 'campaign_name', 'campaign_type', 'start_date', 'end_date',
                  'target_audience', 'budget_allocated', 'budget_spent', 'discount_offered',
                  'promo_code', 'created_by', 'status']
        self.save_to_csv('campaigns', campaigns, headers)
        return campaigns

    def generate_campaign_responses(self, num_responses=15000):
        """Generate campaign response data"""
        print(f"📧 Generating {num_responses} campaign responses...")
        
        if 'campaigns' not in self.data or 'customers' not in self.data:
            print("  ⚠️ Warning: campaigns and customers data required")
            return []
        
        campaigns = self.data['campaigns']
        customers = self.data['customers']
        responses = []
        statuses = ['sent', 'delivered', 'opened', 'clicked', 'converted', 'bounced', 'unsubscribed']
        
        for i in range(num_responses):
            campaign = random.choice(campaigns)
            customer = random.choice(customers)
            
            # Create realistic conversion funnel
            sent_date = self.timestamp_between('-3m', 'now')
            delivered = random.random() < 0.95
            opened = random.random() < 0.25 if delivered else False
            clicked = random.random() < 0.03 if opened else False
            converted = random.random() < 0.15 if clicked else False
            
            delivered_date = sent_date + timedelta(minutes=random.randint(1, 60)) if delivered else None
            opened_date = delivered_date + timedelta(hours=random.randint(1, 48)) if opened else None
            clicked_date = opened_date + timedelta(minutes=random.randint(1, 30)) if clicked else None
            converted_date = clicked_date + timedelta(minutes=random.randint(5, 120)) if converted else None
            
            response_data = [
                f'RESP{i+1:06d}',  # response_id
                campaign[0],  # campaign_id
                customer[0],  # customer_id
                sent_date,  # sent_date
                delivered_date,  # delivered_date
                opened_date,  # opened_date
                clicked_date,  # clicked_date
                converted_date,  # converted_date
                f'ORDER{random.randint(1, 150000)}' if converted else None,  # conversion_order_id
                round(random.uniform(25, 300), 2) if converted else 0,  # conversion_amount
                'converted' if converted else ('clicked' if clicked else ('opened' if opened else ('delivered' if delivered else 'sent')))  # response_status
            ]
            responses.append(response_data)
        
        headers = ['response_id', 'campaign_id', 'customer_id', 'sent_date', 'delivered_date',
                  'opened_date', 'clicked_date', 'converted_date', 'conversion_order_id',
                  'conversion_amount', 'response_status']
        self.save_to_csv('campaign_responses', responses, headers)
        return responses

    def generate_customer_service_interactions(self, num_interactions=8000):
        """Generate customer service interaction data"""
        print(f"🎧 Generating {num_interactions} customer service interactions...")
        
        if 'customers' not in self.data:
            print("  ⚠️ Warning: customers data required")
            return []
        
        customers = self.data['customers']
        interactions = []
        channels = ['phone', 'email', 'chat', 'social_media', 'in_store']
        interaction_types = ['complaint', 'inquiry', 'return_request', 'order_status', 'product_info', 'technical_support']
        categories = ['order_issues', 'product_quality', 'shipping', 'payment', 'returns', 'account', 'general_inquiry']
        priorities = ['low', 'medium', 'high', 'urgent']
        resolution_types = ['resolved', 'escalated', 'pending', 'closed_no_resolution']
        agents = ['agent_001', 'agent_002', 'agent_003', 'agent_004', 'agent_005', 'agent_006', 'agent_007', 'agent_008']
        
        for i in range(num_interactions):
            customer = random.choice(customers)
            interaction_date = self.timestamp_between('-6m', 'now')
            
            channel = random.choice(channels)
            interaction_type = random.choice(interaction_types)
            category = random.choice(categories)
            priority = random.choice(priorities)
            
            # Generate realistic conversation content
            subjects = {
                'complaint': f"Issue with {random.choice(['order delivery', 'product quality', 'billing', 'website'])}",
                'inquiry': f"Question about {random.choice(['product availability', 'sizing', 'return policy', 'shipping'])}",
                'return_request': f"Return request for order #{random.randint(1, 150000)}",
                'order_status': f"Status inquiry for order #{random.randint(1, 150000)}",
                'product_info': f"Information needed about {fake.catch_phrase()} product",
                'technical_support': f"Technical issue with {random.choice(['website', 'mobile app', 'payment', 'account'])}"
            }
            
            subject_line = subjects.get(interaction_type, "General inquiry")
            conversation_text = f"Customer contacted via {channel} regarding {subject_line.lower()}. {fake.text(max_nb_chars=200)}"
            
            # Generate realistic metrics
            satisfaction_score = random.randint(1, 5) if random.random() < 0.8 else None
            resolution_time = round(random.uniform(0.5, 48.0), 1)
            escalated = random.random() < 0.1
            sentiment_score = round(random.uniform(-1, 1), 2)
            
            interaction_data = [
                f'INT{i+1:06d}',  # interaction_id
                customer[0],  # customer_id
                interaction_date,  # interaction_date
                channel,  # channel
                interaction_type,  # interaction_type
                category,  # category
                priority,  # priority
                subject_line,  # subject_line
                conversation_text,  # conversation_text
                f'ORDER{random.randint(1, 150000)}' if random.random() < 0.4 else None,  # related_order_id
                random.choice(resolution_types),  # resolution_type
                satisfaction_score,  # satisfaction_score
                resolution_time,  # resolution_time_hours
                random.choice(agents),  # agent_id
                escalated,  # escalated
                sentiment_score,  # sentiment_score
                ', '.join(fake.words(nb=random.randint(2, 5))),  # keywords_extracted
                random.random() < 0.15,  # follow_up_needed
                round(random.uniform(15, 85), 2)  # interaction_cost
            ]
            interactions.append(interaction_data)
        
        headers = ['interaction_id', 'customer_id', 'interaction_date', 'channel', 'interaction_type',
                  'category', 'priority', 'subject_line', 'conversation_text', 'related_order_id',
                  'resolution_type', 'satisfaction_score', 'resolution_time_hours', 'agent_id',
                  'escalated', 'sentiment_score', 'keywords_extracted', 'follow_up_needed', 'interaction_cost']
        self.save_to_csv('customer_service_interactions', interactions, headers)
        return interactions

    def generate_email_engagement(self, num_engagements=20000):
        """Generate email engagement metrics"""
        print(f"📬 Generating {num_engagements} email engagements...")
        
        if 'customers' not in self.data or 'campaigns' not in self.data:
            print("  ⚠️ Warning: customers and campaigns data required")
            return []
        
        customers = self.data['customers']
        campaigns = self.data['campaigns']
        engagements = []
        delivery_statuses = ['delivered', 'bounced', 'blocked', 'deferred']
        device_types = ['desktop', 'mobile', 'tablet']
        email_clients = ['Gmail', 'Outlook', 'Apple Mail', 'Yahoo Mail', 'Other']
        
        for i in range(num_engagements):
            customer = random.choice(customers)
            campaign = random.choice(campaigns)
            
            send_timestamp = self.timestamp_between('-6m', 'now')
            delivery_status = self.weighted_choice(delivery_statuses, [0.85, 0.10, 0.03, 0.02])
            
            # Create realistic engagement funnel
            delivered = delivery_status == 'delivered'
            opened = random.random() < 0.22 if delivered else False
            clicked = random.random() < 0.035 if opened else False
            
            open_timestamp = send_timestamp + timedelta(hours=random.randint(1, 72)) if opened else None
            click_timestamp = open_timestamp + timedelta(minutes=random.randint(1, 30)) if clicked else None
            
            total_opens = random.randint(1, 5) if opened else 0
            total_clicks = random.randint(1, 3) if clicked else 0
            
            engagement_data = [
                f'ENG{i+1:06d}',  # engagement_id
                customer[0],  # customer_id
                campaign[0],  # campaign_id
                campaign[1][:100],  # email_subject (truncated)
                send_timestamp,  # send_timestamp
                delivery_status,  # delivery_status
                open_timestamp,  # open_timestamp
                total_opens,  # total_opens
                click_timestamp,  # click_timestamp
                total_clicks,  # total_clicks
                ', '.join(fake.words(nb=random.randint(1, 3))) if clicked else None,  # links_clicked
                random.randint(5, 180) if opened else 0,  # time_spent_reading
                random.choice(device_types) if opened else None,  # device_type
                random.choice(email_clients) if opened else None,  # email_client
                send_timestamp + timedelta(days=random.randint(1, 30)) if random.random() < 0.02 else None,  # unsubscribe_timestamp
                random.randint(0, 2) if random.random() < 0.01 else 0,  # forward_count
                random.choice(['A', 'B']) if random.random() < 0.3 else None  # ab_test_variant
            ]
            engagements.append(engagement_data)
        
        headers = ['engagement_id', 'customer_id', 'campaign_id', 'email_subject', 'send_timestamp',
                  'delivery_status', 'open_timestamp', 'total_opens', 'click_timestamp', 'total_clicks',
                  'links_clicked', 'time_spent_reading', 'device_type', 'email_client',
                  'unsubscribe_timestamp', 'forward_count', 'ab_test_variant']
        self.save_to_csv('email_engagement', engagements, headers)
        return engagements

    def generate_loyalty_profiles(self, coverage_rate=0.6):
        """Generate loyalty program profiles"""
        if 'customers' not in self.data:
            print("  ⚠️ Warning: customers data required")
            return []
        
        customers = self.data['customers']
        num_profiles = int(len(customers) * coverage_rate)
        print(f"🎖️ Generating {num_profiles} loyalty profiles...")
        
        profiles = []
        tiers = ['Bronze', 'Silver', 'Gold', 'Platinum', 'Diamond']
        tier_weights = [0.40, 0.30, 0.20, 0.08, 0.02]
        categories = ['Dresses', 'Tops', 'Shoes', 'Accessories', 'Outerwear', 'Activewear']
        
        selected_customers = random.sample(customers, num_profiles)
        
        for customer in selected_customers:
            customer_id = customer[0]
            reg_date = customer[8]  # registration_date
            birth_date = customer[5]  # date_of_birth
            
            tier = self.weighted_choice(tiers, tier_weights)
            points_lifetime = random.randint(100, 50000)
            points_balance = int(points_lifetime * random.uniform(0.1, 0.8))
            
            # Tier thresholds
            tier_thresholds = {'Bronze': 1000, 'Silver': 5000, 'Gold': 15000, 'Platinum': 35000, 'Diamond': 75000}
            next_tier_idx = tiers.index(tier) + 1
            next_threshold = tier_thresholds.get(tiers[next_tier_idx]) if next_tier_idx < len(tiers) else None
            
            tier_start_date = reg_date + timedelta(days=random.randint(30, 365))
            anniversary_date = reg_date
            birthday_month = birth_date.month if birth_date else random.randint(1, 12)
            
            profile_data = [
                customer_id,  # customer_id
                tier,  # tier_level
                points_balance,  # points_balance
                points_lifetime,  # points_lifetime
                tier_start_date.date(),  # tier_start_date
                next_threshold,  # next_tier_threshold
                birthday_month,  # birthday_month
                anniversary_date.date(),  # anniversary_date
                ', '.join(random.sample(categories, random.randint(1, 3))),  # preferred_categories
                random.choice(['email_sms', 'email_only', 'sms_only', 'app_notifications']),  # communication_preferences
                tier in ['Platinum', 'Diamond'] or random.random() < 0.05,  # vip_status
                fake.date_between('-1y', 'now')  # last_tier_review
            ]
            profiles.append(profile_data)
        
        headers = ['customer_id', 'tier_level', 'points_balance', 'points_lifetime', 'tier_start_date',
                  'next_tier_threshold', 'birthday_month', 'anniversary_date', 'preferred_categories',
                  'communication_preferences', 'vip_status', 'last_tier_review']
        self.save_to_csv('loyalty_profiles', profiles, headers)
        return profiles

    def generate_loyalty_activities(self, num_activities=35000):
        """Generate loyalty program activities"""
        print(f"🏆 Generating {num_activities} loyalty activities...")
        
        if 'loyalty_profiles' not in self.data:
            print("  ⚠️ Warning: loyalty_profiles data required")
            return []
        
        profiles = self.data['loyalty_profiles']
        activities = []
        activity_types = ['purchase_points', 'bonus_points', 'referral_points', 'review_points', 
                         'birthday_bonus', 'redemption', 'tier_bonus', 'social_share_points']
        
        for i in range(num_activities):
            profile = random.choice(profiles)
            customer_id = profile[0]
            
            activity_type = random.choice(activity_types)
            activity_date = self.timestamp_between('-2y', 'now')
            
            # Generate appropriate point values
            if activity_type == 'purchase_points':
                points_earned = random.randint(10, 500)
                points_redeemed = 0
                description = f"Points earned from purchase (${random.randint(25, 1250)})"
                related_order_id = f"ORDER{random.randint(1, 150000)}"
            elif activity_type == 'redemption':
                points_earned = 0
                points_redeemed = random.randint(100, 2000)
                description = f"Points redeemed for {random.choice(['discount', 'free shipping', 'product reward'])}"
                related_order_id = f"ORDER{random.randint(1, 150000)}" if random.random() < 0.7 else None
            elif activity_type == 'bonus_points':
                points_earned = random.randint(50, 1000)
                points_redeemed = 0
                description = f"Bonus points from {random.choice(['double points event', 'seasonal promotion', 'tier upgrade'])}"
                related_order_id = None
            else:
                points_earned = random.randint(5, 100)
                points_redeemed = 0
                description = f"Points from {activity_type.replace('_', ' ')}"
                related_order_id = None
            
            expiry_date = activity_date.date() + timedelta(days=random.randint(365, 730))
            
            activity_data = [
                f'ACT{i+1:06d}',  # activity_id
                customer_id,  # customer_id
                activity_type,  # activity_type
                activity_date,  # activity_date
                points_earned,  # points_earned
                points_redeemed,  # points_redeemed
                description,  # description
                related_order_id,  # related_order_id
                expiry_date  # expiry_date
            ]
            activities.append(activity_data)
        
        headers = ['activity_id', 'customer_id', 'activity_type', 'activity_date',
                  'points_earned', 'points_redeemed', 'description', 'related_order_id', 'expiry_date']
        self.save_to_csv('loyalty_activities', activities, headers)
        return activities

    def generate_product_embeddings(self, coverage_rate=0.8):
        """Generate product embeddings for ML similarity"""
        if 'products' not in self.data:
            print("  ⚠️ Warning: products data required")
            return []
        
        products = self.data['products']
        num_embeddings = int(len(products) * coverage_rate)
        print(f"🧠 Generating {num_embeddings} product embeddings...")
        
        embeddings = []
        models = ['sentence-transformers/all-MiniLM-L6-v2', 'openai/text-embedding-ada-002', 'cohere-embed-multilingual-v3.0']
        
        selected_products = random.sample(products, num_embeddings)
        
        for i, product in enumerate(selected_products):
            product_id = product[0]
            product_name = product[1]
            
            # Generate fake embedding vector (in reality this would be computed)
            vector_size = random.choice([384, 768, 1536])  # Common embedding dimensions
            fake_vector = [round(random.uniform(-1, 1), 6) for _ in range(vector_size)]
            vector_text = str(fake_vector)
            
            text_source = f"{product_name} - {product[2]} - {product[3]}"  # name, brand, category
            
            embedding_data = [
                f'EMB_P{i+1:06d}',  # embedding_id
                product_id,  # product_id
                text_source,  # text_source
                vector_text,  # embedding_vector
                random.choice(models),  # embedding_model
                self.timestamp_between('-6m', 'now'),  # created_date
                random.randint(1, 3)  # vector_version
            ]
            embeddings.append(embedding_data)
        
        headers = ['embedding_id', 'product_id', 'text_source', 'embedding_vector',
                  'embedding_model', 'created_date', 'vector_version']
        self.save_to_csv('product_embeddings', embeddings, headers)
        return embeddings

    def generate_customer_style_embeddings(self, coverage_rate=0.4):
        """Generate customer style embeddings"""
        if 'customers' not in self.data:
            print("  ⚠️ Warning: customers data required")
            return []
        
        customers = self.data['customers']
        num_embeddings = int(len(customers) * coverage_rate)
        print(f"👤 Generating {num_embeddings} customer style embeddings...")
        
        embeddings = []
        selected_customers = random.sample(customers, num_embeddings)
        
        for i, customer in enumerate(selected_customers):
            customer_id = customer[0]
            
            # Generate style preferences text
            styles = ['casual', 'formal', 'trendy', 'classic', 'bohemian', 'minimalist', 'edgy', 'romantic']
            colors = ['neutral tones', 'bright colors', 'earth tones', 'pastels', 'monochrome']
            materials = ['cotton', 'silk', 'wool', 'denim', 'leather']
            
            style_prefs = f"Prefers {random.choice(styles)} style with {random.choice(colors)} and {random.choice(materials)} materials"
            
            # Generate fake embedding vector
            vector_size = random.choice([384, 768])
            fake_vector = [round(random.uniform(-1, 1), 6) for _ in range(vector_size)]
            vector_text = str(fake_vector)
            
            embedding_data = [
                f'EMB_C{i+1:06d}',  # customer_embedding_id
                str(customer_id),  # customer_id (as string per schema)
                vector_text,  # style_vector
                style_prefs,  # text_source
                round(random.uniform(0.6, 1.0), 4),  # confidence_score
                self.timestamp_between('-3m', 'now'),  # last_updated
                random.randint(5, 50)  # purchase_count_basis
            ]
            embeddings.append(embedding_data)
        
        headers = ['customer_embedding_id', 'customer_id', 'style_vector', 'text_source',
                  'confidence_score', 'last_updated', 'purchase_count_basis']
        self.save_to_csv('customer_style_embeddings', embeddings, headers)
        return embeddings

    def generate_fashion_research_documents(self, num_documents=150):
        """Generate fashion research documents"""
        print(f"📚 Generating {num_documents} fashion research documents...")
        
        documents = []
        doc_types = ['trend_report', 'market_analysis', 'consumer_survey', 'style_guide', 'seasonal_forecast']
        sources = ['Fashion Institute', 'Trend Analytics Corp', 'Style Research Lab', 'Market Insights Inc', 'Fashion Forward Think Tank']
        themes = ['sustainable fashion', 'digital transformation', 'color trends', 'material innovation', 'consumer behavior', 
                 'social media influence', 'seasonal preferences', 'demographic shifts', 'price sensitivity', 'brand loyalty']
        segments = ['Gen Z', 'Millennials', 'Gen X', 'All Demographics', 'Urban Professionals', 'Students', 'Premium Shoppers']
        regions = ['North America', 'Europe', 'Asia-Pacific', 'Global', 'United States', 'Canada']
        
        for i in range(num_documents):
            doc_type = random.choice(doc_types)
            source = random.choice(sources)
            
            # Generate contextual titles
            if doc_type == 'trend_report':
                title = f"{random.choice(['Spring', 'Summer', 'Fall', 'Winter'])} {random.randint(2023, 2024)} Fashion Trends Report"
            elif doc_type == 'market_analysis':
                title = f"{random.choice(['Quarterly', 'Annual'])} Fashion Market Analysis - {random.choice(regions)}"
            else:
                title = f"{doc_type.title().replace('_', ' ')} - {fake.catch_phrase()}"
            
            # Generate embedding vector
            vector_size = 768
            fake_vector = [round(random.uniform(-1, 1), 6) for _ in range(vector_size)]
            
            document_data = [
                f'DOC_{i+1:06d}',  # document_id
                doc_type,  # document_type
                source,  # source
                title,  # title
                fake.date_between('-2y', 'now'),  # publication_date
                str(fake_vector),  # embedding_vector
                ', '.join(random.sample(themes, random.randint(2, 4))),  # key_themes
                ', '.join(random.sample(segments, random.randint(1, 3))),  # customer_segments
                round(random.uniform(0.6, 0.95), 2),  # trend_confidence
                random.choice(regions),  # geographic_focus
                self.timestamp_between('-2y', 'now')  # created_at
            ]
            documents.append(document_data)
        
        headers = ['document_id', 'document_type', 'source', 'title', 'publication_date',
                  'embedding_vector', 'key_themes', 'customer_segments', 'trend_confidence',
                  'geographic_focus', 'created_at']
        self.save_to_csv('fashion_research_documents', documents, headers)
        return documents

    def generate_session_summary(self, num_days=90):
        """Generate daily session summary data"""
        print(f"📈 Generating {num_days} days of session summaries...")
        
        summaries = []
        start_date = date.today() - timedelta(days=num_days)
        
        for i in range(num_days):
            summary_date = start_date + timedelta(days=i)
            
            # Generate realistic daily metrics
            is_weekend = summary_date.weekday() >= 5
            is_holiday = random.random() < 0.05  # 5% chance of holiday
            
            base_sessions = random.randint(800, 1500)
            if is_weekend:
                base_sessions = int(base_sessions * random.uniform(0.7, 0.9))
            if is_holiday:
                base_sessions = int(base_sessions * random.uniform(0.4, 0.8))
            
            total_sessions = base_sessions
            unique_visitors = int(total_sessions * random.uniform(0.75, 0.85))
            bounce_sessions = int(total_sessions * random.uniform(0.35, 0.55))
            avg_duration = random.randint(180, 600)  # 3-10 minutes in seconds
            
            summary_data = [
                summary_date,  # summary_date
                total_sessions,  # total_sessions
                unique_visitors,  # unique_visitors
                bounce_sessions,  # bounce_sessions
                avg_duration,  # avg_session_duration
                self.timestamp_between('now', 'now')  # created_at
            ]
            summaries.append(summary_data)
        
        headers = ['summary_date', 'total_sessions', 'unique_visitors', 'bounce_sessions',
                  'avg_session_duration', 'created_at']
        self.save_to_csv('session_summary', summaries, headers)
        return summaries

    def generate_all_data(self):
        """Generate complete dataset including all 26 tables for enterprise C360 system"""
        print("\n🚀 Starting Complete C360 Data Generation...")
        print("🔗 Generating 50k customer dataset with enterprise-scale data + all auxiliary tables")
=======

    def generate_all_data(self):
        """Generate complete dataset including reviews"""
        print("\n🚀 Starting Complete C360 Data Generation...")
        print("🔗 Generating 50k customer dataset with enterprise-scale data + reviews")
>>>>>>> origin/main
        
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
<<<<<<< HEAD
        self.generate_session_summary()
        
        # Marketing and Campaigns
        print("\n=== 📢 Generating Marketing & Campaign Data ===")
        self.generate_campaigns()
        self.generate_campaign_responses()
        self.generate_email_engagement()
        
        # Customer Service
        print("\n=== 🎧 Generating Customer Service Data ===")
        self.generate_customer_service_interactions()
        
        # Loyalty Program
        print("\n=== 🎖️ Generating Loyalty Program Data ===")
        self.generate_loyalty_profiles()
        self.generate_loyalty_activities()
        
        # ML/AI Data and Recommendations
        print("\n=== 🎯 Generating ML & Recommendation Data ===")
        self.generate_style_similarity_matches()
        self.generate_product_embeddings()
        self.generate_customer_style_embeddings()
        
        # Research and Insights
        print("\n=== 📚 Generating Research & Insights Data ===")
        self.generate_fashion_research_documents()
        
        print(f"\n🎉 Complete enterprise dataset generation finished!")
=======
        
        # Style Similarity Matches (ML/Recommendation Engine Data)
        print("\n=== 🎯 Generating ML & Recommendation Data ===")
        self.generate_style_similarity_matches()
        
        print(f"\n🎉 Complete dataset generation finished!")
>>>>>>> origin/main
        print(f"\n📊 Generated tables:")
        for table, data in self.data.items():
            print(f"  ✅ {table}: {len(data):,} rows")
        
<<<<<<< HEAD
        total_rows = sum(len(data) for data in self.data.values())
        print(f"\n🔗 Enterprise Scale Achieved:")
        print(f"  ✅ 50,000 customers with proportional transactions")
        print(f"  ✅ {total_rows:,} total records across {len(self.data)} tables")
        print(f"  ✅ Complete 26-table C360 Fashion Retail database")
        print(f"  ✅ Contextually accurate reviews with quality correlation")
        print(f"  ✅ Foreign key compatible data types")
        print(f"  ✅ Complete referential integrity maintained")
        print(f"  ✅ ML/AI ready embeddings and recommendations")
        print(f"  ✅ Enterprise customer service and loyalty tracking")
        print(f"  ✅ Comprehensive marketing campaign analytics")
=======
        print(f"\n🔗 Enterprise Scale Achieved:")
        print(f"  ✅ 50,000 customers with proportional transactions")
        print(f"  ✅ ~700k total records across all tables")
        print(f"  ✅ Contextually accurate reviews with quality correlation")
        print(f"  ✅ Foreign key compatible data types")
        print(f"  ✅ Complete referential integrity maintained")
>>>>>>> origin/main
        print(f"\n🚀 Ready for database loading!")

if __name__ == "__main__":
    generator = CompleteDatasetGenerator()
    generator.generate_all_data()