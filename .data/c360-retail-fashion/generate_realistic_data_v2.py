#!/usr/bin/env python3
"""
C360 Retail Fashion Database - Data Generator v2.0
Updated with consistent data types for foreign key compatibility
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

# Custom Faker providers
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

fake.add_provider(FashionProvider)

class DataGeneratorV2:
    def __init__(self, output_dir='postgres'):
        self.output_dir = output_dir
        self.data = {}
        os.makedirs(output_dir, exist_ok=True)
        print("🔄 C360 Data Generator v2.0 - Foreign Key Compatible")
        print("📊 Generating data with consistent data types for referential integrity")
        
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
            brand = {
                'brand_id': i + 1,  # INTEGER - matches schema
                'brand_name': FashionProvider.fashion_brands[i % len(FashionProvider.fashion_brands)] + (f' {i//len(FashionProvider.fashion_brands) + 1}' if i >= len(FashionProvider.fashion_brands) else ''),
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
        self.save_to_csv('brands', brands, headers)
        return brands

    def generate_categories(self):
        """Generate categories table (10-20 top-level)"""
        categories = []
        cat_id = 1
        
        for main_cat, subcats in list(FashionProvider.fashion_categories.items())[:random.randint(10, 20)]:
            # Add main category
            main_category = {
                'category_id': cat_id,  # INTEGER - matches schema
                'category_name': main_cat,
                'created_at': self.timestamp_between('-3y', '-1y'),
                'description': fake.text(max_nb_chars=150),
                'is_seasonal': random.choice([True, False]),
                'parent_category_id': None,
                'typical_margin_percentage': round(random.uniform(0.15, 0.45), 2)
            }
            categories.append(list(main_category.values()))
            main_cat_id = cat_id
            cat_id += 1
            
            # Add 1-2 subcategories
            num_subcats = random.randint(1, min(2, len(subcats)))
            for subcat in random.sample(subcats, num_subcats):
                sub_category = {
                    'category_id': cat_id,  # INTEGER - matches schema
                    'category_name': subcat,
                    'created_at': self.timestamp_between('-3y', '-1y'),
                    'description': fake.text(max_nb_chars=100),
                    'is_seasonal': random.choice([True, False]),
                    'parent_category_id': main_cat_id,  # INTEGER - matches parent
                    'typical_margin_percentage': round(random.uniform(0.15, 0.45), 2)
                }
                categories.append(list(sub_category.values()))
                cat_id += 1
        
        headers = ['category_id', 'category_name', 'created_at', 'description', 'is_seasonal', 'parent_category_id', 'typical_margin_percentage']
        self.save_to_csv('categories', categories, headers)
        return categories

    def generate_products(self):
        """Generate products table (500-1000 products) - VARCHAR(20) product_id"""
        num_products = random.randint(500, 1000)
        brands = [row[1] for row in self.data['brands']]  # brand_name from brands table
        categories = [row[1] for row in self.data['categories']]  # category_name from categories table
        
        products = []
        for i in range(num_products):
            brand = random.choice(brands)
            category = random.choice(categories)
            
            product = {
                'product_id': f'P{i+1:06d}',  # VARCHAR(20) - consistent format P000001
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
        self.save_to_csv('products', products, headers)
        return products

    def generate_product_variants(self):
        """Generate product variants (3-6 per product) - VARCHAR product_id to match products"""
        products = self.data['products']
        variants = []
        variant_id = 1
        
        for product in products:
            product_id = product[0]  # VARCHAR from products table P000001 format
            num_variants = random.randint(3, 6)
            
            for _ in range(num_variants):
                variant = {
                    'variant_id': variant_id,  # INTEGER auto-increment
                    'product_id': product_id,  # VARCHAR(20) - matches products.product_id
                    'sku': f"SKU{product_id[1:]}V{variant_id:03d}",
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
        self.save_to_csv('product_variants', variants, headers)
        return variants

    def generate_customers(self):
        """Generate customers table (5000 customers) - INTEGER customer_id"""
        customers = []
        
        # Distributions from the plan
        gender_dist = {'male': 0.49, 'female': 0.51}
        age_ranges = {'18-24': 0.12, '25-34': 0.20, '35-44': 0.17, '45-54': 0.16, '55-64': 0.15, '65+': 0.20}
        channels = {'organic': 0.40, 'paid_ads': 0.25, 'referral': 0.15, 'social': 0.10, 'email': 0.10}
        
        for i in range(5000):
            gender = self.weighted_choice(list(gender_dist.keys()), list(gender_dist.values()))
            age_range = self.weighted_choice(list(age_ranges.keys()), list(age_ranges.values()))
            
            # Calculate birth year from age range
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
            
            customer = {
                'customer_id': i + 1,  # INTEGER - consistent with customers table
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
        self.save_to_csv('customers', customers, headers)
        return customers

    def generate_customer_addresses(self):
        """Generate customer addresses - INTEGER customer_id to match customers"""
        customers = self.data['customers']
        addresses = []
        
        # US states with weights (simplified)
        states = ['CA', 'TX', 'FL', 'NY', 'PA', 'IL', 'OH', 'GA', 'NC', 'MI']
        
        for customer in customers:
            customer_id = customer[0]  # INTEGER from customers table
            num_addresses = 1 if random.random() < 0.5 else 2
            
            for j in range(num_addresses):
                address = {
                    'address_id': self.generate_id('ADDR'),
                    'customer_id': customer_id,  # INTEGER - matches customers.customer_id
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
        self.save_to_csv('customer_addresses', addresses, headers)
        return addresses

    def generate_orders(self):
        """Generate orders - INTEGER order_id and customer_id"""
        customers = self.data['customers']
        num_orders = random.randint(12000, 15000)
        orders = []
        
        # Distributions
        status_dist = {'delivered': 0.85, 'cancelled': 0.05, 'returned': 0.10}
        payment_methods = {'credit_card': 0.60, 'paypal': 0.20, 'bnpl': 0.15, 'gift_card': 0.05}
        
        for i in range(num_orders):
            customer = random.choice(customers)
            customer_id = customer[0]  # INTEGER from customers table
            
            # Order value from normal distribution
            order_value = max(20, min(200, np.random.normal(60, 15)))
            
            order_date = self.timestamp_between('-2y', 'now')
            
            order = {
                'order_id': i + 1,  # INTEGER - consistent 
                'customer_id': customer_id,  # INTEGER - matches customers.customer_id
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
        self.save_to_csv('orders', orders, headers)
        return orders

    def generate_order_items(self):
        """Generate order items - INTEGER order_id, VARCHAR product_id to match respective tables"""
        orders = self.data['orders']
        products = self.data['products']
        variants = self.data['product_variants']
        
        order_items = []
        item_id = 1
        
        for order in orders:
            order_id = order[0]  # INTEGER from orders table
            order_total = order[4]  # total_amount
            
            num_items = random.randint(1, 4)
            items_for_order = []
            
            for _ in range(num_items):
                variant = random.choice(variants)
                product_id = variant[1]  # VARCHAR(20) product_id from variant
                
                quantity = max(1, int(np.random.normal(1.2, 0.5)))
                if quantity > 3:
                    quantity = 3
                
                unit_price = round(order_total / num_items / quantity, 2)
                total_price = round(unit_price * quantity, 2)
                
                item = {
                    'order_item_id': item_id,  # INTEGER auto-increment
                    'order_id': order_id,  # INTEGER - matches orders.order_id
                    'product_id': product_id,  # VARCHAR(20) - matches products.product_id
                    'sku': variant[2],  # sku from variant
                    'size': variant[3],  # size from variant
                    'color': variant[4],  # color from variant
                    'quantity': quantity,
                    'unit_price': unit_price,
                    'total_price': total_price,
                    'final_price': total_price,
                    'discount_applied': round(random.uniform(0, total_price * 0.1), 2) if random.random() < 0.2 else 0,
                    'gift_wrap': random.random() < 0.05,
                    'personalization': fake.sentence(nb_words=3) if random.random() < 0.02 else None
                }
                items_for_order.append(list(item.values()))
                item_id += 1
            
            order_items.extend(items_for_order)
        
        headers = ['order_item_id', 'order_id', 'product_id', 'sku', 'size', 'color', 'quantity', 
                  'unit_price', 'total_price', 'final_price', 'discount_applied', 'gift_wrap', 'personalization']
        self.save_to_csv('order_items', order_items, headers)
        return order_items

    def generate_returns(self):
        """Generate returns - INTEGER order_id and customer_id to match respective tables"""
        orders = [row for row in self.data['orders'] if row[3] in ['delivered', 'returned']]  # Only delivered/returned orders
        num_returns = int(len(orders) * random.uniform(0.10, 0.12))
        
        returns = []
        return_reasons = {'fit': 0.40, 'defective': 0.20, 'changed_mind': 0.25, 'other': 0.15}
        refund_methods = {'store_credit': 0.40, 'original_payment': 0.60}
        
        selected_orders = random.sample(orders, num_returns)
        
        for i, order in enumerate(selected_orders):
            order_id = order[0]  # INTEGER from orders table
            customer_id = order[1]  # INTEGER from orders table
            order_date = order[2]
            order_total = order[4]
            
            return_date = self.timestamp_between(order_date, 'now')
            
            return_record = {
                'return_id': self.generate_id('RET'),
                'order_id': order_id,  # INTEGER - matches orders.order_id
                'customer_id': customer_id,  # INTEGER - matches customers.customer_id
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
        self.save_to_csv('returns', returns, headers)
        return returns

    def generate_return_items(self):
        """Generate return items - INTEGER order_item_id to match order_items"""
        returns = self.data['returns']
        order_items = self.data['order_items']
        return_items = []
        
        conditions = {'like_new': 0.70, 'damaged': 0.20, 'worn': 0.10}
        
        for return_record in returns:
            return_id = return_record[0]
            order_id = return_record[1]  # INTEGER from returns table
            
            # Find order items for this order
            order_items_for_order = [item for item in order_items if item[1] == order_id]
            
            if not order_items_for_order:
                continue
                
            num_items = min(random.randint(1, 2), len(order_items_for_order))
            selected_items = random.sample(order_items_for_order, num_items)
            
            for item in selected_items:
                order_item_id = item[0]  # INTEGER from order_items table
                quantity = item[6]
                
                return_item = {
                    'return_item_id': self.generate_id('RI'),
                    'return_id': return_id,
                    'order_item_id': order_item_id,  # INTEGER - matches order_items.order_item_id
                    'quantity_returned': min(quantity, random.randint(1, quantity)),
                    'item_condition': self.weighted_choice(list(conditions.keys()), list(conditions.values())),
                    'refund_eligible': random.random() < 0.9,
                    'restockable': random.random() < 0.8
                }
                return_items.append(list(return_item.values()))
        
        headers = ['return_item_id', 'return_id', 'order_item_id', 'quantity_returned', 
                  'item_condition', 'refund_eligible', 'restockable']
        self.save_to_csv('return_items', return_items, headers)
        return return_items

    def generate_all_data(self):
        """Generate all data in the correct order (respecting foreign key dependencies)"""
        print("\n🚀 Starting C360 Data Generation v2.0...")
        print("🔗 Generating foreign key compatible data with consistent data types")
        
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
        
        print(f"\n🎉 Data generation complete! Files saved to '{self.output_dir}' directory.")
        print("\n📊 Generated tables with consistent foreign key data types:")
        for table, data in self.data.items():
            print(f"  ✅ {table}: {len(data):,} rows")
        
        print("\n🔗 Foreign Key Compatibility:")
        print("  ✅ customer_id: INTEGER across all tables")
        print("  ✅ product_id: VARCHAR(20) across all tables")
        print("  ✅ order_id: INTEGER across all tables") 
        print("  ✅ order_item_id: INTEGER across all tables")
        print("\n🚀 Ready for foreign key implementation!")

if __name__ == "__main__":
    generator = DataGeneratorV2()
    generator.generate_all_data()