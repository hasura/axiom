#!/usr/bin/env python3
"""
CPG E-commerce Data Generator
This script generates realistic CSV data for a CPG company's business analytics,
including sales, market share, availability, and assortment data.
"""

import os
import random
import datetime
import csv
import math
import argparse
from typing import List, Dict, Any, Tuple
from collections import defaultdict
promotion_product_pairs = set()

# Create output directory for CSV files
OUTPUT_DIR = "postgres"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Set a seed for reproducibility
random.seed(42)

# Time range for data generation
START_DATE = datetime.date(2022, 1, 1)
END_DATE = datetime.date(2025, 3, 31)  # Generate some future data for forecasting
DAYS = (END_DATE - START_DATE).days + 1

# Seasonal patterns (month -> multiplier)
SEASONALITY = {
    1: 0.85,  # January - Post-holiday slump
    2: 0.80,  # February
    3: 0.90,  # March
    4: 1.00,  # April
    5: 1.05,  # May
    6: 1.10,  # June - Summer begins
    7: 1.15,  # July
    8: 1.20,  # August - Peak summer
    9: 1.10,  # September - Back to school
    10: 1.15,  # October - Halloween
    11: 1.25,  # November - Thanksgiving
    12: 1.40,  # December - Holiday season
}

# Holiday spikes
HOLIDAYS = {
    # Format: datetime.date(year, month, day): (multiplier, duration_days, affected_categories)
    datetime.date(2022, 1, 1): (1.2, 1, ["Breakfast", "Snacks"]),  # New Year's Day
    datetime.date(2022, 2, 14): (1.5, 3, ["Baking", "Desserts"]),  # Valentine's Day
    datetime.date(2022, 5, 8): (1.3, 2, ["Breakfast", "Baking"]),   # Mother's Day
    datetime.date(2022, 7, 4): (1.6, 3, ["Snacks", "Condiments"]),  # Independence Day
    datetime.date(2022, 10, 31): (1.8, 7, ["Snacks", "Candy"]),     # Halloween
    datetime.date(2022, 11, 24): (2.0, 5, ["Baking", "Sides"]),     # Thanksgiving
    datetime.date(2022, 12, 25): (2.2, 10, ["Baking", "Desserts", "Breakfast"]),  # Christmas
    
    datetime.date(2023, 1, 1): (1.2, 1, ["Breakfast", "Snacks"]),
    datetime.date(2023, 2, 14): (1.5, 3, ["Baking", "Desserts"]),
    datetime.date(2023, 5, 14): (1.3, 2, ["Breakfast", "Baking"]),
    datetime.date(2023, 7, 4): (1.6, 3, ["Snacks", "Condiments"]),
    datetime.date(2023, 10, 31): (1.8, 7, ["Snacks", "Candy"]),
    datetime.date(2023, 11, 23): (2.0, 5, ["Baking", "Sides"]),
    datetime.date(2023, 12, 25): (2.2, 10, ["Baking", "Desserts", "Breakfast"]),
    
    datetime.date(2024, 1, 1): (1.2, 1, ["Breakfast", "Snacks"]),
    datetime.date(2024, 2, 14): (1.5, 3, ["Baking", "Desserts"]),
    datetime.date(2024, 5, 12): (1.3, 2, ["Breakfast", "Baking"]),
    datetime.date(2024, 7, 4): (1.6, 3, ["Snacks", "Condiments"]),
    datetime.date(2024, 10, 31): (1.8, 7, ["Snacks", "Candy"]),
    datetime.date(2024, 11, 28): (2.0, 5, ["Baking", "Sides"]),
    datetime.date(2024, 12, 25): (2.2, 10, ["Baking", "Desserts", "Breakfast"]),
    
    datetime.date(2025, 1, 1): (1.2, 1, ["Breakfast", "Snacks"]),
    datetime.date(2025, 2, 14): (1.5, 3, ["Baking", "Desserts"]),
}

# Multi-year trends
TRENDS = {
    "E-commerce Growth": {
        "start": 0.10,  # Initial e-commerce percentage
        "end": 0.28,    # Final e-commerce percentage
        "affected_channels": ["E-commerce"],
        "type": "channel"
    },
    "Organic Growth": {
        "start": 1.0,
        "end": 1.25,
        "affected_products": "is_organic",
        "type": "product"
    },
    "Gluten-Free Growth": {
        "start": 1.0,
        "end": 1.18,
        "affected_products": "is_glutenfree",
        "type": "product"
    },
    "Snacking Increase": {
        "start": 1.0,
        "end": 1.15,
        "affected_categories": ["Snacks"],
        "type": "category"
    },
    "Breakfast Decline": {
        "start": 1.0,
        "end": 0.92,
        "affected_categories": ["Cereal"],
        "type": "category"
    }
}

# Supply chain disruptions
DISRUPTIONS = [
    {
        "start_date": datetime.date(2022, 3, 15),
        "end_date": datetime.date(2022, 4, 10),
        "severity": "Medium",
        "description": "Packaging supplier shortage",
        "affected_categories": ["Cereal", "Bars"],
        "impact": 0.7  # Availability multiplier
    },
    {
        "start_date": datetime.date(2022, 7, 8),
        "end_date": datetime.date(2022, 7, 20),
        "severity": "Low",
        "description": "Transportation delay due to fuel costs",
        "affected_categories": ["All"],
        "impact": 0.9
    },
    {
        "start_date": datetime.date(2023, 1, 15),
        "end_date": datetime.date(2023, 2, 28),
        "severity": "High",
        "description": "Ingredient shortage - wheat",
        "affected_categories": ["Cereal", "Baking", "Flour", "Pasta"],
        "impact": 0.6
    },
    {
        "start_date": datetime.date(2023, 9, 10),
        "end_date": datetime.date(2023, 10, 5),
        "severity": "Medium",
        "description": "Labor shortage at manufacturing plants",
        "affected_categories": ["All"],
        "impact": 0.8
    },
    {
        "start_date": datetime.date(2024, 5, 1),
        "end_date": datetime.date(2024, 5, 30),
        "severity": "Critical",
        "description": "Major supplier bankruptcy",
        "affected_categories": ["Snacks", "Bars"],
        "impact": 0.5
    }
]

def apply_date_effects(date, base_value, category=None, channel_type=None, is_organic=False, is_glutenfree=False) -> float:
    """Apply seasonal, holiday, and trend effects to a base value based on date and attributes."""
    value = base_value
    
    # Apply seasonality
    month = date.month
    value *= SEASONALITY.get(month, 1.0)
    
    # Apply holiday effects
    for holiday_date, (multiplier, duration, affected_cats) in HOLIDAYS.items():
        if holiday_date <= date <= holiday_date + datetime.timedelta(days=duration):
            if category in affected_cats or "All" in affected_cats:
                day_diff = (date - holiday_date).days
                # Stronger effect closer to the holiday
                day_factor = 1 - (day_diff / duration)
                holiday_effect = 1 + ((multiplier - 1) * day_factor)
                value *= holiday_effect
    
    # Apply trends
    days_since_start = (date - START_DATE).days
    total_days = DAYS
    progress = days_since_start / total_days if total_days > 0 else 0
    
    for trend_name, trend in TRENDS.items():
        apply_trend = False
        
        if trend["type"] == "channel" and channel_type in trend.get("affected_channels", []):
            apply_trend = True
        elif trend["type"] == "product":
            if trend.get("affected_products") == "is_organic" and is_organic:
                apply_trend = True
            elif trend.get("affected_products") == "is_glutenfree" and is_glutenfree:
                apply_trend = True
        elif trend["type"] == "category" and category in trend.get("affected_categories", []):
            apply_trend = True
            
        if apply_trend:
            trend_factor = trend["start"] + (trend["end"] - trend["start"]) * progress
            value *= trend_factor
    
    # Apply disruption effects to availability
    for disruption in DISRUPTIONS:
        if disruption["start_date"] <= date <= disruption["end_date"]:
            if category in disruption["affected_categories"] or "All" in disruption["affected_categories"]:
                # This primarily affects availability, but indirectly affects sales
                impact_on_sales = (1 + disruption["impact"]) / 2  # Less impact on sales than availability
                value *= impact_on_sales
    
    return value

def generate_realistic_value(base, variation_pct=0.1, min_val=None, max_val=None):
    """Generate a value with realistic variation around a base value."""
    variation = random.uniform(-variation_pct, variation_pct)
    value = base * (1 + variation)
    
    if min_val is not None:
        value = max(value, min_val)
    if max_val is not None:
        value = min(value, max_val)
        
    return value

def write_csv(filename, data, headers):
    """Write data to a CSV file."""
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        writer.writerows(data)
    print(f"Generated {filepath} with {len(data)} rows")

def generate_brands():
    """Generate brand data."""
    brands = [
        [1, "Harvest Morning", "Golden Foods Inc", "Mainstream", "Breakfast Foods", 1985, True],
        [2, "Nature's Path", "Golden Foods Inc", "Premium", "Organic Products", 1998, True],
        [3, "Family Baker", "Golden Foods Inc", "Mainstream", "Baking Products", 1975, True],
        [4, "Simply Sweet", "Golden Foods Inc", "Mainstream", "Desserts", 1990, True],
        [5, "Grain Power", "Golden Foods Inc", "Premium", "Whole Grains", 2005, True],
        [6, "Kids Choice", "Golden Foods Inc", "Mainstream", "Children's Food", 1992, True],
        [7, "Snack Time", "Golden Foods Inc", "Value", "Snacks", 1988, True],
        [8, "Pasta Perfect", "Golden Foods Inc", "Mainstream", "Pasta", 2000, True],
        [9, "Pure Goodness", "Golden Foods Inc", "Premium", "Organic Snacks", 2010, True],
        [10, "Budget Bites", "Golden Foods Inc", "Value", "Value Products", 2003, True]
    ]
    
    # Add competitor brands
    competitor_brands = [
        [11, "Morning Star", "Sunrise Foods", "Mainstream", "Breakfast Foods", 1980, True],
        [12, "Bake Master", "Quality Bakers Corp", "Mainstream", "Baking Products", 1978, True],
        [13, "Farm Fresh", "Healthful Brands", "Premium", "Organic Products", 2001, True],
        [14, "Daily Breakfast", "Sunrise Foods", "Value", "Breakfast Foods", 1995, True],
        [15, "Tasty Treats", "Snack Innovations", "Mainstream", "Snacks", 1990, True],
        [16, "Value Eats", "Discount Foods Inc", "Value", "Multiple Categories", 2005, True],
        [17, "Gourmet Selection", "Premium Brands Co", "Premium", "Multiple Categories", 1999, True],
        [18, "Market Basics", "Store Brand", "Private Label", "Multiple Categories", 2000, True]
    ]
    
    brands.extend(competitor_brands)
    headers = ["brand_id", "brand_name", "parent_company", "brand_tier", "category_focus", "year_established", "is_active"]
    
    write_csv("brands.csv", brands, headers)
    return {brand[0]: brand for brand in brands}

def generate_categories():
    """Generate product category data."""
    categories = [
        # Main categories
        [1, "Breakfast Foods", None, "Morning meal products", False, 35.00],
        [2, "Baking Products", None, "Ingredients for baking", False, 30.00],
        [3, "Snacks", None, "Between-meal food items", False, 40.00],
        [4, "Meal Solutions", None, "Products for main meals", False, 28.00],
        [5, "Desserts", None, "Sweet treat products", False, 32.00],
        
        # Subcategories
        [6, "Cereal", 1, "Ready-to-eat breakfast cereal", False, 38.00],
        [7, "Oatmeal", 1, "Hot cereal products", True, 32.00],
        [8, "Breakfast Bars", 1, "On-the-go breakfast options", False, 42.00],
        [9, "Pancake & Waffle Mixes", 1, "Mixes for breakfast items", False, 28.00],
        
        [10, "Flour", 2, "Baking flour products", False, 22.00],
        [11, "Cake & Brownie Mixes", 2, "Sweet baking mixes", False, 36.00],
        [12, "Cookie Mixes", 2, "Cookie preparation mixes", False, 34.00],
        [13, "Baking Ingredients", 2, "Other baking ingredients", False, 26.00],
        
        [14, "Granola Bars", 3, "Oat-based snack bars", False, 45.00],
        [15, "Fruit Snacks", 3, "Fruit-flavored snacks", False, 48.00],
        [16, "Crackers", 3, "Savory cracker products", False, 38.00],
        [17, "Popcorn", 3, "Popcorn products", False, 52.00],
        [18, "Trail Mix", 3, "Nut and fruit mixes", False, 36.00],
        [19, "Chips", 3, "Savory chip products", False, 44.00],
        
        [20, "Pasta", 4, "Dry pasta products", False, 25.00],
        [21, "Meal Kits", 4, "Complete meal preparation kits", False, 32.00],
        [22, "Rice", 4, "Rice products and mixes", False, 28.00],
        [23, "Sauce Mixes", 4, "Flavor mixes for meals", False, 38.00],
        
        [24, "Pudding", 5, "Pudding mixes and cups", False, 30.00],
        [25, "Gelatin Desserts", 5, "Gelatin-based dessert mixes", False, 34.00],
        [26, "Dessert Bars", 5, "Ready-to-eat dessert bars", False, 38.00],
        [27, "Candy", 5, "Confectionery products", True, 42.00]
    ]
    
    headers = ["category_id", "category_name", "parent_category_id", "category_description", "is_seasonal", "typical_margin_percentage"]
    write_csv("product_categories.csv", categories, headers)
    return {cat[0]: cat for cat in categories}

def generate_products(brands, categories):
    """Generate product data."""
    products = []
    product_id = 1
    
    # Helper to assign a category to a brand based on its focus
    def get_relevant_categories(brand, all_categories):
        focus = brand[4]  # category_focus field
        relevant_main_cats = []
        
        if "Breakfast" in focus:
            relevant_main_cats.append(1)  # Breakfast Foods
        if "Baking" in focus:
            relevant_main_cats.append(2)  # Baking Products
        if "Snacks" in focus:
            relevant_main_cats.append(3)  # Snacks
        if "Organic" in focus:
            # Organic products could be in any category
            return [cat_id for cat_id, cat in all_categories.items() if cat[2] is not None]  # Return all subcategories
        
        # Default if no specific focus
        if not relevant_main_cats:
            relevant_main_cats = [1, 2, 3, 4, 5]  # All main categories
            
        # Get subcategories of the relevant main categories
        subcategories = [cat_id for cat_id, cat in all_categories.items() 
                         if cat[2] in relevant_main_cats]
        return subcategories
    
    # Product templates by category to ensure realistic naming
    product_templates = {
        6: ["Crunchy {}", "Toasted {}", "{} Flakes", "{} Squares", "{} Crunch", "Honey {}", "Frosted {}"],
        7: ["Instant {} Oatmeal", "{} Oats", "Steel Cut {} Oats", "{} Hot Cereal", "Overnight {}"],
        8: ["Chewy {} Bar", "{} Breakfast Bar", "{} Morning Bar", "Crunchy {} Start"],
        9: ["{} Pancake Mix", "{} Waffle Mix", "Complete {} Mix", "{} & {} Pancake Mix"],
        10: ["All-Purpose {} Flour", "{} Baking Flour", "Organic {} Flour", "Whole Wheat {} Flour"],
        11: ["{} Cake Mix", "{} Brownie Mix", "Ultimate {} Mix", "{} Deluxe Cake"],
        12: ["{} Cookie Mix", "Easy {} Cookies", "{} & {} Cookies", "Homestyle {} Cookies"],
        13: ["{} Baking Chips", "{} Sprinkles", "{} Frosting", "Premade {} Dough"],
        14: ["{} Granola Bar", "Chewy {} Bar", "Crunchy {} Bar", "{} & {} Bar"],
        15: ["{} Fruit Snacks", "{} Fruit Bites", "{} Fruit Rolls", "Organic {} Fruit Snack"],
        16: ["{} Crackers", "{} Crisps", "{} Thins", "Whole Grain {} Crackers"],
        17: ["{} Popcorn", "Microwave {} Popcorn", "{} Kettle Corn", "{} Popcorn Bites"],
        18: ["{} Trail Mix", "{} & {} Mix", "Protein {} Mix", "Energy {} Blend"],
        19: ["{} Chips", "{} Crisps", "Baked {} Chips", "{} Tortilla Chips"],
        20: ["{} Pasta", "{} & {} Pasta", "{} Spaghetti", "{} Rotini"],
        21: ["{} Meal Kit", "{} Dinner Kit", "Easy {} Meal", "30-Minute {} Meal"],
        22: ["{} Rice", "{} Rice Mix", "{} & {} Rice", "Instant {} Rice"],
        23: ["{} Sauce Mix", "{} Gravy Mix", "{} Seasoning Blend", "{} Marinade Mix"],
        24: ["{} Pudding", "Instant {} Pudding", "{} Pudding Cups", "{} Parfait Mix"],
        25: ["{} Gelatin", "{} Gelatin Mix", "{} Gelatin Cups", "Sugar-Free {} Gelatin"],
        26: ["{} Dessert Bar", "{} Treat Bar", "Fudgy {} Bar", "{} & {} Dessert Square"],
        27: ["{} Candy", "{} Chocolate", "{} Gummies", "{} Candy Bites"]
    }
    
    flavor_descriptors = [
        "Chocolate", "Vanilla", "Strawberry", "Blueberry", "Cinnamon", "Apple", "Banana", 
        "Honey", "Maple", "Original", "Berry", "Cherry", "Almond", "Coconut", "Peanut Butter",
        "Caramel", "Raspberry", "Mixed Berry", "Lemon", "Orange", "Peach", "Tropical", 
        "Cranberry", "Grape", "Plain", "Tomato", "Cheese", "Garlic", "Herb", "Spicy",
        "Sea Salt", "BBQ", "Ranch", "Sour Cream", "Onion", "Whole Grain", "Multi-Grain"
    ]
    
    # Generate products for our own brands (1-10)
    for brand_id in range(1, 11):
        brand = brands[brand_id]
        relevant_categories = get_relevant_categories(brand, categories)
        
        # Number of products per brand varies by brand tier
        num_products = {
            "Premium": random.randint(8, 15),
            "Mainstream": random.randint(12, 25),
            "Value": random.randint(5, 10),
            "Private Label": random.randint(10, 20)
        }[brand[3]]
        
        for _ in range(num_products):
            category_id = random.choice(relevant_categories)
            category = categories[category_id]
            main_category_id = category[2] if category[2] else category_id
            
            # Select template and flavors
            if category_id in product_templates:
                template = random.choice(product_templates[category_id])
                
                # For templates with two placeholders
                if template.count("{}") == 2:
                    flavor1 = random.choice(flavor_descriptors)
                    flavor2 = random.choice([f for f in flavor_descriptors if f != flavor1])
                    product_name = template.format(flavor1, flavor2)
                else:
                    flavor = random.choice(flavor_descriptors)
                    product_name = template.format(flavor)
            else:
                # Generic template if specific one not found
                product_name = f"{random.choice(flavor_descriptors)} {category[1]}"
            
            # Add brand to product name
            product_name = f"{brand[1]} {product_name}"
            
            # Generate SKU
            sku_base = ''.join(word[0] for word in brand[1].split())
            sku = f"{sku_base}{category_id:02d}{product_id:06d}"            

            # Generate product attributes
            unit_sizes = ["Small", "Medium", "Large", "Family Size", "Single Serve", "Party Size"]
            unit_measures = ["oz", "g", "lbs", "kg", "count", "servings"]
            
            unit_size = random.choice(unit_sizes)
            unit_measure = random.choice(unit_measures)
            
            if unit_measure == "oz":
                weight = round(random.uniform(6.0, 48.0), 2)
            elif unit_measure == "g":
                weight = round(random.uniform(100.0, 1000.0), 2)
            elif unit_measure == "lbs":
                weight = round(random.uniform(0.5, 5.0), 2)
            elif unit_measure == "kg":
                weight = round(random.uniform(0.2, 2.0), 2)
            elif unit_measure == "count":
                weight = round(random.uniform(5.0, 50.0), 0)
            else:  # servings
                weight = round(random.uniform(4.0, 12.0), 0)
            
            case_pack = random.choice([6, 12, 24, 36, 48])
            
            # Price based on brand tier
            base_price_multipliers = {
                "Premium": random.uniform(1.3, 1.7),
                "Mainstream": random.uniform(0.9, 1.2),
                "Value": random.uniform(0.6, 0.8),
                "Private Label": random.uniform(0.5, 0.7)
            }
            
            base_price = round(weight * 0.25 * base_price_multipliers[brand[3]], 2)
            wholesale_price = round(base_price * 0.6, 2)
            msrp = round(base_price, 2)
            
            # Launch date - older for established brands
            years_active = 2023 - brand[5]  # Current year - established year
            max_years_back = min(years_active, 10)  # Cap at 10 years back
            launch_years_ago = random.randint(0, max_years_back)
            launch_date = datetime.date(2023 - launch_years_ago, random.randint(1, 12), random.randint(1, 28))
            
            # Discontinued date - small chance for discontinued products
            if random.random() < 0.05:  # 5% chance of being discontinued
                months_active = random.randint(6, 36)
                discontinue_date = (launch_date + datetime.timedelta(days=30*months_active)).strftime("%Y-%m-%d")
            else:
                discontinue_date = None
                
            # Product attributes
            is_organic = "Organic" in brand[4] or "Organic" in product_name or random.random() < 0.15
            is_glutenfree = random.random() < 0.20
            is_seasonal = category[4] or random.random() < 0.10  # Based on category seasonality
            high_velocity = random.random() < 0.25  # 25% are high velocity items
            
            products.append([
                product_id,
                sku,
                product_name,
                brand_id,
                main_category_id,
                category_id,
                unit_size,
                unit_measure,
                case_pack,
                weight,
                wholesale_price,
                msrp,
                launch_date.strftime("%Y-%m-%d"),
                discontinue_date,
                is_organic,
                is_glutenfree,
                is_seasonal,
                high_velocity
            ])
            
            product_id += 1
    
    # Generate competitor products (fewer details needed)
    for brand_id in range(11, 19):
        brand = brands[brand_id]
        relevant_categories = get_relevant_categories(brand, categories)
        
        num_products = {
            "Premium": random.randint(5, 10),
            "Mainstream": random.randint(8, 15),
            "Value": random.randint(4, 8),
            "Private Label": random.randint(6, 12)
        }[brand[3]]
        
        for _ in range(num_products):
            category_id = random.choice(relevant_categories)
            category = categories[category_id]
            main_category_id = category[2] if category[2] else category_id
            
            # Simpler product generation for competitors
            if category_id in product_templates:
                template = random.choice(product_templates[category_id])
                
                if template.count("{}") == 2:
                    flavor1 = random.choice(flavor_descriptors)
                    flavor2 = random.choice([f for f in flavor_descriptors if f != flavor1])
                    product_name = template.format(flavor1, flavor2)
                else:
                    flavor = random.choice(flavor_descriptors)
                    product_name = template.format(flavor)
            else:
                product_name = f"{random.choice(flavor_descriptors)} {category[1]}"
                
            product_name = f"{brand[1]} {product_name}"
            sku_base = ''.join(word[0] for word in brand[1].split())
            sku = f"{sku_base}{category_id:02d}{product_id:04d}"
            
            unit_size = random.choice(["Small", "Medium", "Large", "Family Size"])
            unit_measure = random.choice(["oz", "g", "lbs", "count"])
            weight = round(random.uniform(6.0, 48.0), 2) if unit_measure == "oz" else round(random.uniform(100.0, 1000.0), 2)
            case_pack = random.choice([6, 12, 24])
            
            base_price_multipliers = {
                "Premium": random.uniform(1.3, 1.7),
                "Mainstream": random.uniform(0.9, 1.2),
                "Value": random.uniform(0.6, 0.8),
                "Private Label": random.uniform(0.5, 0.7)
            }
            
            base_price = round(weight * 0.25 * base_price_multipliers[brand[3]], 2)
            wholesale_price = round(base_price * 0.6, 2)
            msrp = round(base_price, 2)
            
            launch_years_ago = random.randint(0, 5)
            launch_date = datetime.date(2023 - launch_years_ago, random.randint(1, 12), random.randint(1, 28))
            
            is_organic = "Organic" in brand[4] or "Organic" in product_name or random.random() < 0.15
            is_glutenfree = random.random() < 0.20
            is_seasonal = category[4] or random.random() < 0.10
            high_velocity = random.random() < 0.25
            
            products.append([
                product_id,
                sku,
                product_name,
                brand_id,
                main_category_id,
                category_id,
                unit_size,
                unit_measure,
                case_pack,
                weight,
                wholesale_price,
                msrp,
                launch_date.strftime("%Y-%m-%d"),
                None,  # No discontinued date for competitors
                is_organic,
                is_glutenfree,
                is_seasonal,
                high_velocity
            ])
            
            product_id += 1
    
    headers = ["product_id", "product_sku", "product_name", "brand_id", "category_id", "subcategory_id", 
              "unit_size", "unit_measure", "case_pack", "weight_oz", "wholesale_price", "msrp", 
              "launch_date", "discontinue_date", "is_organic", "is_glutenfree", "is_seasonal", "high_velocity"]
    
    write_csv("products.csv", products, headers)
    return {product[0]: product for product in products}

def generate_competitors():
    """Generate competitor data."""
    competitors = [
        [1, "Sunrise Foods", "Direct", ["Breakfast Foods", "Cereal", "Snacks"], "Major competitor in breakfast category"],
        [2, "Quality Bakers Corp", "Direct", ["Baking Products", "Flour", "Mixes"], "Leading baking products manufacturer"],
        [3, "Healthful Brands", "Direct", ["Organic", "Natural", "Premium"], "Premium organic competitor"],
        [4, "Snack Innovations", "Direct", ["Snacks", "Bars", "Chips"], "Snack foods specialist"],
        [5, "Discount Foods Inc", "Indirect", ["Value", "Multiple Categories"], "Value-oriented manufacturer"],
        [6, "Premium Brands Co", "Indirect", ["Premium", "Specialty", "Gourmet"], "High-end specialty foods"],
        [7, "Retailer Store Brands", "Private Label", ["All Categories"], "Private label products across categories"]
    ]
    
    headers = ["competitor_id", "competitor_name", "competitor_type", "primary_categories", "notes"]
    
    # Convert list to string for CSV
    for comp in competitors:
        comp[3] = "{" + ",".join(f'"{cat}"' for cat in comp[3]) + "}"
    
    write_csv("competitors.csv", competitors, headers)
    return {comp[0]: comp for comp in competitors}

def generate_channels():
    """Generate sales channel data."""
    channels = [
        [1, "Grocery", "Grocery", False, False, "National", 15.00],
        [2, "Mass Merchant", "Mass Merchant", False, False, "National", 12.00],
        [3, "Club", "Club", False, False, "National", 10.00],
        [4, "Convenience", "Convenience", False, False, "National", 18.00],
        [5, "Drug", "Drug", False, False, "National", 16.00],
        [6, "Online Grocery", "E-commerce", False, True, "National", 20.00],
        [7, "Direct to Consumer", "E-commerce", True, True, "National", 25.00],
        [8, "Specialty", "Specialty", False, False, "Regional", 22.00],
        [9, "Food Service", "Food Service", False, False, "National", 14.00],
        [10, "Marketplace", "E-commerce", False, True, "National", 22.00]
    ]
    
    headers = ["channel_id", "channel_name", "channel_type", "is_direct_to_consumer", "is_online", "region", "distribution_cost_percentage"]
    
    write_csv("channels.csv", channels, headers)
    return {chan[0]: chan for chan in channels}

def generate_retailers(channels):
    """Generate retailer data."""
    retailers = [
        [1, "FreshMart", 1, "National", True, ">$10B", "Strategic"],
        [2, "ValueGrocer", 1, "National", True, "$5B-$10B", "Key"],
        [3, "SuperFresh", 1, "National", True, "$5B-$10B", "Key"],
        [4, "LocalMarket", 1, "Regional", False, "$1B-$5B", "Core"],
        [5, "MegaMart", 2, "National", True, ">$10B", "Strategic"],
        [6, "Discounter", 2, "National", True, ">$10B", "Strategic"],
        [7, "Warehouse Deals", 3, "National", True, ">$10B", "Strategic"],
        [8, "BulkBuy Club", 3, "National", False, "$5B-$10B", "Key"],
        [9, "QuickStop", 4, "National", False, "$1B-$5B", "Core"],
        [10, "Corner Market", 4, "Regional", False, "<$1B", "Small"],
        [11, "PharmPlus", 5, "National", True, "$5B-$10B", "Key"],
        [12, "Health Essentials", 5, "Regional", True, "$1B-$5B", "Core"],
        [13, "eFresh Delivery", 6, "National", True, "$1B-$5B", "Core"],
        [14, "Online Grocery", 6, "National", True, "$1B-$5B", "Core"],
        [15, "Brand Direct", 7, "National", True, "<$1B", "Small"],
        [16, "Organic Market", 8, "Regional", True, "<$1B", "Small"],
        [17, "Gourmet Grocer", 8, "Regional", False, "<$1B", "Small"],
        [18, "Food Distributor", 9, "National", False, "$1B-$5B", "Core"],
        [19, "School Supplier", 9, "Regional", False, "<$1B", "Small"],
        [20, "E-Marketplace", 10, "National", True, ">$10B", "Strategic"]
    ]
    
    headers = ["retailer_id", "retailer_name", "channel_id", "sales_region", "has_ecommerce", "annual_revenue_tier", "account_tier"]
    
    write_csv("retailers.csv", retailers, headers)
    return {ret[0]: ret for ret in retailers}

def generate_warehouses():
    """Generate warehouse data."""
    warehouses = [
        [1, "East Coast DC", "Regional DC", "Philadelphia", "PA", "USA", 500000, 15000, 450000.00],
        [2, "Midwest DC", "Regional DC", "Chicago", "IL", "USA", 650000, 20000, 520000.00],
        [3, "West Coast DC", "Regional DC", "Sacramento", "CA", "USA", 550000, 16000, 480000.00],
        [4, "South DC", "Regional DC", "Atlanta", "GA", "USA", 475000, 14500, 420000.00],
        [5, "Central Distribution", "Central DC", "St. Louis", "MO", "USA", 800000, 25000, 680000.00],
        [6, "Northeast FC", "Fulfillment Center", "Edison", "NJ", "USA", 300000, 8000, 350000.00],
        [7, "Southwest FC", "Fulfillment Center", "Dallas", "TX", "USA", 320000, 8500, 360000.00],
        [8, "Northwest FC", "Fulfillment Center", "Seattle", "WA", "USA", 280000, 7500, 340000.00],
        [9, "Southeast 3PL", "3PL", "Miami", "FL", "USA", 400000, 12000, 320000.00],
        [10, "Midwest 3PL", "3PL", "Indianapolis", "IN", "USA", 380000, 11500, 310000.00]
    ]
    
    headers = ["warehouse_id", "warehouse_name", "warehouse_type", "location_city", "location_state", "location_country", "square_footage", "max_capacity_pallets", "operating_cost_per_month"]
    
    write_csv("warehouses.csv", warehouses, headers)
    return {wh[0]: wh for wh in warehouses}

def generate_sales_data(products, retailers, start_date=None, end_date=None, num_transactions=None):
    """Generate sales transaction data."""
    if start_date is None:
        start_date = START_DATE
    if end_date is None:
        end_date = datetime.date(2025, 3, 31)  # Generate data including future to have a complete dataset
    
    sales_data = []
    transaction_id = 1
    
    # Get our product IDs (brand_id 1-10)
    our_product_ids = [pid for pid, p in products.items() if p[3] <= 10]
    
    # For each date in the range
    current_date = start_date
    while current_date <= end_date:
        # If this date is in the future, only generate forecast data
        if current_date > datetime.date.today():
            current_date += datetime.timedelta(days=1)
            continue
            
        # For each retailer
        for retailer_id, retailer in retailers.items():
            channel_id = retailer[2]
            channel_type = "E-commerce" if channel_id in [6, 7, 10] else "Store"
            
            # Determine how many products to generate sales for on this day for this retailer
            # Larger retailers have more products sold per day
            num_products_per_day = {
                "Strategic": random.randint(20, 40),
                "Key": random.randint(15, 25),
                "Core": random.randint(8, 15),
                "Small": random.randint(3, 8)
            }[retailer[6]]
            
            # Select random products
            daily_products = random.sample(our_product_ids, min(num_products_per_day, len(our_product_ids)))
            
            for product_id in daily_products:
                product = products[product_id]
                category_id = product[4]
                category_name = None  # This would need to be looked up from categories if needed
                
                # Base sales quantity depends on product velocity and retailer size
                base_quantity_multipliers = {
                    "Strategic": 15,
                    "Key": 10,
                    "Core": 5,
                    "Small": 2
                }[retailer[6]]
                
                velocity_multiplier = 2.0 if product[17] else 1.0  # High velocity products sell better
                
                base_quantity = int(base_quantity_multipliers * velocity_multiplier)
                
                # Apply date effects to quantity
                final_quantity = int(apply_date_effects(
                    current_date,
                    base_quantity,
                    category=category_name,
                    channel_type=channel_type,
                    is_organic=product[14],
                    is_glutenfree=product[15]
                ))
                
                # Ensure at least 1 unit sold if the product is selected for the day
                final_quantity = max(1, final_quantity)
                
                # Determine if this sale is under promotion (more likely during holidays and for certain retailers)
                month = current_date.month
                is_holiday_month = month in [1, 2, 5, 7, 10, 11, 12]  # Months with major holidays
                
                promotion_base_chance = 0.15  # Base chance of promotion
                promotion_holiday_boost = 0.15 if is_holiday_month else 0
                promotion_retailer_boost = {
                    "Strategic": 0.10,
                    "Key": 0.05,
                    "Core": 0.02,
                    "Small": 0.01
                }[retailer[6]]
                
                promotion_chance = promotion_base_chance + promotion_holiday_boost + promotion_retailer_boost
                is_promoted = random.random() < promotion_chance
                
                # Determine price and discount
                base_price = product[11]  # MSRP
                discount_percentage = 0
                
                if is_promoted:
                    discount_percentage = random.choice([10, 15, 20, 25, 30, 35, 40])
                
                unit_price = base_price * (1 - discount_percentage / 100)
                unit_price = round(unit_price, 2)
                
                total_amount = round(unit_price * final_quantity, 2)
                
                # Determine if online sale
                is_online = retailer[4]  # has_ecommerce
                
                if is_online:
                    # For retailers with e-commerce, determine what percentage of sales are online
                    online_sales_percentage = {
                        "Grocery": 0.15,
                        "Mass Merchant": 0.25,
                        "Club": 0.20,
                        "Drug": 0.10,
                        "E-commerce": 1.00,  # Online-only retailers
                        "Specialty": 0.15,
                        "Food Service": 0.05
                    }
                    
                    is_online_sale = random.random() < online_sales_percentage.get(retailers[channel_id][1], 0.15)
                else:
                    is_online_sale = False
                
                # Add the transaction
                sales_data.append([
                    transaction_id,
                    product_id,
                    retailer_id,
                    current_date.strftime("%Y-%m-%d"),
                    final_quantity,
                    unit_price,
                    total_amount,
                    is_promoted,
                    discount_percentage,
                    is_online_sale
                ])
                
                transaction_id += 1
                
                # Stop if we've reached the requested number of transactions
                if num_transactions and transaction_id > num_transactions:
                    break
            
            if num_transactions and transaction_id > num_transactions:
                break
                
        current_date += datetime.timedelta(days=1)
        if num_transactions and transaction_id > num_transactions:
            break
    
    headers = ["transaction_id", "product_id", "retailer_id", "transaction_date", 
              "quantity", "unit_price", "total_amount", "is_promoted", "discount_percentage", "is_online_sale"]
    
    write_csv("sales_transactions.csv", sales_data, headers)
    return sales_data

def generate_market_shares(brands, categories, channels):
    """Generate market share data."""
    market_share_data = []
    share_id = 1
    
    # Define the main categories we'll track share for
    tracked_categories = [1, 2, 3, 4, 5]  # Main categories
    measurement_periods = ["Monthly"]  # For simplicity, just do monthly
    
    # Define our brands (1-10) and competitor brands (11-18)
    our_brands = [bid for bid in range(1, 11)]
    competitor_brands = [bid for bid in range(11, 19)]
    all_brands = our_brands + competitor_brands
    
    # For each month in the date range
    current_date = START_DATE.replace(day=1)  # Start at beginning of month
    end_date = END_DATE
    
    while current_date <= end_date:
        month_end = get_month_end(current_date)
        
        # For each category
        for category_id in tracked_categories:
            category = categories[category_id]
            
            # For each channel
            for channel_id, channel in channels.items():
                # Allocate market share among brands active in this category
                # First, determine which brands are active here
                active_brands = []
                for brand_id in all_brands:
                    brand = brands[brand_id]
                    if brand_matches_category(brand, category):
                        active_brands.append(brand_id)
                
                if not active_brands:
                    continue  # Skip if no brands in this category
                
                # Set baseline market shares to reasonable values
                total_share = 100.0
                brand_shares = {}
                
                # Share allocations depend on brand tier and our vs. competitor
                # Calculate initial shares based on brand strength
                for brand_id in active_brands:
                    brand = brands[brand_id]
                    tier = brand[3]
                    
                    # Base share by tier
                    if brand_id in our_brands:
                        # Our brands get slightly higher base share
                        base_share = {
                            "Premium": 15.0,
                            "Mainstream": 10.0,
                            "Value": 5.0,
                            "Private Label": 7.0
                        }[tier]
                    else:
                        # Competitor brands
                        base_share = {
                            "Premium": 12.0,
                            "Mainstream": 8.0,
                            "Value": 4.0,
                            "Private Label": 6.0
                        }[tier]
                    
                    # Apply some randomness
                    brand_shares[brand_id] = base_share * random.uniform(0.8, 1.2)
                
                # Normalize to ensure total is 100%
                total = sum(brand_shares.values())
                for brand_id in brand_shares:
                    brand_shares[brand_id] = (brand_shares[brand_id] / total) * 100.0
                
                # Apply trends over time
                days_since_start = (current_date - START_DATE).days
                total_days = (END_DATE - START_DATE).days
                progress = days_since_start / total_days if total_days > 0 else 0
                
                # Apply brand-specific trends
                for brand_id in brand_shares:
                    brand = brands[brand_id]
                    
                    # Our brands generally gain share over time
                    if brand_id in our_brands:
                        trend_factor = 1.0 + (0.15 * progress)  # Up to 15% increase
                    else:
                        trend_factor = 1.0 - (0.05 * progress)  # Up to 5% decrease
                    
                    # But premium and organic brands grow faster
                    if brand[3] == "Premium" or "Organic" in brand[4]:
                        trend_factor *= 1.0 + (0.10 * progress)  # Additional growth
                    
                    brand_shares[brand_id] *= trend_factor
                
                # Renormalize after trends
                total = sum(brand_shares.values())
                for brand_id in brand_shares:
                    brand_shares[brand_id] = (brand_shares[brand_id] / total) * 100.0
                
                # Apply seasonality and other effects
                for brand_id in brand_shares:
                    brand = brands[brand_id]
                    
                    # Seasonal effects vary by category
                    if category[4]:  # is_seasonal
                        month = current_date.month
                        season_factor = SEASONALITY.get(month, 1.0)
                        
                        # Seasonal brands do better in their season
                        if "Seasonal" in brand[4]:
                            brand_shares[brand_id] *= season_factor
                    
                    # Holiday effects
                    for holiday_date, (multiplier, duration, affected_cats) in HOLIDAYS.items():
                        holiday_month = holiday_date.month
                        if current_date.month == holiday_month:
                            if category[1] in affected_cats or "All" in affected_cats:
                                # Brands focused on these categories gain share
                                if category[1] in brand[4]:
                                    brand_shares[brand_id] *= 1.1
                
                # Renormalize after all effects
                total = sum(brand_shares.values())
                for brand_id in brand_shares:
                    brand_shares[brand_id] = (brand_shares[brand_id] / total) * 100.0
                
                # Calculate dollar and volume sales (fictional numbers for demonstration)
                total_market_size = random.uniform(5000000, 20000000)  # $5-20M per month
                
                # Add entry for each brand's share
                for brand_id, share in brand_shares.items():
                    # Round to 2 decimal places
                    share_percentage = round(share, 2)
                    
                    # Calculate dollar and volume sales
                    dollar_sales = round(total_market_size * (share / 100.0), 2)
                    
                    # Volume share might be different from dollar share
                    # Premium brands have higher dollar share than volume share
                    brand = brands[brand_id]
                    if brand[3] == "Premium":
                        volume_share = share * random.uniform(0.8, 0.9)  # Lower volume share
                    elif brand[3] == "Value":
                        volume_share = share * random.uniform(1.1, 1.2)  # Higher volume share
                    else:
                        volume_share = share * random.uniform(0.95, 1.05)  # Similar
                    
                    volume_share = round(volume_share, 2)
                    
                    # Volume in units
                    avg_price = random.uniform(2.5, 6.0)
                    volume_sales = round(dollar_sales / avg_price, 2)
                    
                    market_share_data.append([
                        share_id,
                        category_id,
                        brand_id,
                        channel_id,
                        current_date.strftime("%Y-%m-%d"),
                        share_percentage,
                        volume_share,
                        dollar_sales,
                        volume_sales,
                        "Monthly",
                        "Market Research Firm"
                    ])
                    
                    share_id += 1
        
        # Move to next month
        current_date = add_months(current_date, 1)
    
    headers = ["share_id", "category_id", "brand_id", "channel_id", "report_date", 
              "share_percentage", "volume_share_percentage", "dollar_sales", "volume_sales", 
              "measurement_period", "data_source"]
    
    write_csv("market_shares.csv", market_share_data, headers)
    return market_share_data

def generate_promotions(products, channels):
    """Generate promotion data."""
    promotions = []
    promotion_id = 1
    
    # Get our product IDs (brand_id 1-10)
    our_product_ids = [pid for pid, p in products.items() if p[3] <= 10]
    
    # Types of promotions
    promotion_types = ["Price Discount", "BOGO", "Bundle", "Display", "Feature", "TPR", "Digital Coupon"]
    
    # Create a calendar of promotions
    current_date = START_DATE
    
    while current_date <= END_DATE:
        # More promotions during key seasons
        month = current_date.month
        
        # Base number of new promotions starting this week
        if month in [11, 12]:  # Holiday season
            num_new_promotions = random.randint(3, 6)
        elif month in [1, 2, 5, 7, 10]:  # Other promotional periods
            num_new_promotions = random.randint(2, 4)
        else:
            num_new_promotions = random.randint(1, 3)
        
        for _ in range(num_new_promotions):
            # Select a channel for this promotion
            channel_id = random.randint(1, 10)
            channel = channels[channel_id]
            
            # Promotion name
            promo_name_prefixes = ["Spring", "Summer", "Fall", "Winter", "Holiday", "Back to School", 
                                 "Weekend", "Special", "Flash", "Member", "Digital", "In-Store"]
            promo_name_types = ["Sale", "Savings", "Discount", "Deal", "Promotion", "Event", "Offer"]
            
            promotion_name = f"{random.choice(promo_name_prefixes)} {random.choice(promo_name_types)}"
            
            # Promotion details
            promotion_type = random.choice(promotion_types)
            
            # Duration varies by type
            duration_days = {
                "Price Discount": random.randint(7, 14),
                "BOGO": random.randint(5, 10),
                "Bundle": random.randint(10, 21),
                "Display": random.randint(14, 28),
                "Feature": random.randint(7, 14),
                "TPR": random.randint(21, 90),  # Temporary Price Reduction tends to be longer
                "Digital Coupon": random.randint(5, 14)
            }[promotion_type]
            
            start_date = current_date
            end_date = start_date + datetime.timedelta(days=duration_days)
            
            # Discount details
            if promotion_type in ["Price Discount", "TPR", "Digital Coupon"]:
                discount_type = "Percentage"
                discount_value = random.choice([10, 15, 20, 25, 30, 40])
            elif promotion_type == "BOGO":
                discount_type = "Free Item"
                discount_value = 1  # Buy one get one free
            else:
                discount_type = "Fixed Amount"
                discount_value = random.choice([1, 2, 3, 5, 10])
            
            min_purchase_qty = 1
            if promotion_type == "BOGO":
                min_purchase_qty = 2
            elif promotion_type == "Bundle":
                min_purchase_qty = random.randint(2, 4)
            
            # Budget for the promotion
            budget = random.uniform(5000, 50000)
            
            # Notes
            notes = f"{promotion_type} promotion through {channel[1]} channel"
            
            promotions.append([
                promotion_id,
                promotion_name,
                promotion_type,
                start_date.strftime("%Y-%m-%d"),
                end_date.strftime("%Y-%m-%d"),
                discount_value,
                discount_type,
                min_purchase_qty,
                budget,
                channel_id,
                notes
            ])
            
            # Select products for this promotion
            num_products = random.randint(3, 10)
            promo_products = random.sample(our_product_ids, min(num_products, len(our_product_ids)))
            
            # Generate promotion_products entries
            for product_id in promo_products:
                write_promotion_product(promotion_id, product_id)
            
            promotion_id += 1
        
        # Move to next week
        current_date += datetime.timedelta(days=7)
    
    headers = ["promotion_id", "promotion_name", "promotion_type", "start_date", "end_date", 
              "discount_value", "discount_type", "min_purchase_qty", "budget", "channel_id", "notes"]
    
    write_csv("promotions.csv", promotions, headers)
    return {promo[0]: promo for promo in promotions}

def write_promotion_product(promotion_id=None, product_id=None, flush=False):
    """Track unique promotion-product pairs and write them if flush is True."""
    if flush:
        headers = ["promotion_id", "product_id"]
        data = sorted(promotion_product_pairs)
        write_csv("promotion_products.csv", data, headers)
        return

    promotion_product_pairs.add((promotion_id, product_id))

def generate_inventory_data(products, warehouses):
    """Generate inventory level data."""
    inventory_data = []
    inventory_id = 1
    
    # Get our product IDs (brand_id 1-10)
    our_product_ids = [pid for pid, p in products.items() if p[3] <= 10]
    
    # Generate monthly snapshots
    current_date = START_DATE.replace(day=1)  # Start at beginning of month
    
    while current_date <= END_DATE:
        # For each warehouse
        for warehouse_id, warehouse in warehouses.items():
            # For each product (not all products in all warehouses)
            # Select products for this warehouse based on region and type
            warehouse_region = warehouse[3]  # location_city
            warehouse_type = warehouse[1]  # warehouse_name
            
            # Regional DCs typically have most products
            # FCs have fewer products, focused on e-commerce
            if "Regional DC" in warehouse_type:
                num_products = int(len(our_product_ids) * 0.8)  # 80% of products
            elif "Central DC" in warehouse_type:
                num_products = len(our_product_ids)  # All products
            elif "Fulfillment Center" in warehouse_type:
                num_products = int(len(our_product_ids) * 0.6)  # 60% of products
            else:  # 3PL
                num_products = int(len(our_product_ids) * 0.4)  # 40% of products
            
            warehouse_products = random.sample(our_product_ids, min(num_products, len(our_product_ids)))
            
            for product_id in warehouse_products:
                product = products[product_id]
                
                # Base inventory levels depend on product velocity
                if product[17]:  # high_velocity
                    base_quantity = random.randint(1000, 5000)
                else:
                    base_quantity = random.randint(200, 1000)
                
                # Adjust for warehouse size
                warehouse_size_factor = warehouse[7] / 15000  # Normalize by average capacity
                base_quantity = int(base_quantity * warehouse_size_factor)
                
                # Apply seasonality and trends
                category_id = product[4]
                category_name = None  # Would need categories lookup
                
                adjusted_quantity = apply_date_effects(
                    current_date,
                    base_quantity,
                    category=category_name,
                    is_organic=product[14],
                    is_glutenfree=product[15]
                )
                
                # Apply supply chain disruptions specifically to inventory
                for disruption in DISRUPTIONS:
                    if disruption["start_date"] <= current_date <= disruption["end_date"]:
                        affected_categories = disruption["affected_categories"]
                        if category_name in affected_categories or "All" in affected_categories:
                            adjusted_quantity *= disruption["impact"]
                
                quantity_on_hand = int(adjusted_quantity)
                
                # Allocated inventory is a portion of on-hand inventory
                allocation_rate = random.uniform(0.2, 0.6)  # 20-60% allocated
                quantity_allocated = int(quantity_on_hand * allocation_rate)
                
                # Calculate days of supply
                daily_demand = random.uniform(5, 50)
                days_of_supply = int(quantity_on_hand / daily_demand) if daily_demand > 0 else 30
                
                # Inventory value
                unit_cost = product[10] * 0.8  # 80% of wholesale price
                inventory_value = round(quantity_on_hand * unit_cost, 2)
                
                # Reorder point and max capacity
                reorder_point = int(daily_demand * random.randint(5, 15))  # 5-15 days of demand
                max_capacity = int(quantity_on_hand * random.uniform(1.5, 3.0))  # 1.5-3x current quantity
                
                # Lot number and expiration date
                lot_number = f"LOT{current_date.year}{current_date.month:02d}-{product_id:06d}"
                
                # Expiration date (6-18 months in the future)
                shelf_life_days = random.randint(180, 540)
                expiration_date = (current_date + datetime.timedelta(days=shelf_life_days)).strftime("%Y-%m-%d")
                
                inventory_data.append([
                    inventory_id,
                    product_id,
                    warehouse_id,
                    current_date.strftime("%Y-%m-%d"),
                    quantity_on_hand,
                    quantity_allocated,
                    # quantity_available is calculated in DB
                    days_of_supply,
                    inventory_value,
                    reorder_point,
                    max_capacity,
                    lot_number,
                    expiration_date
                ])
                
                inventory_id += 1
        
        # Move to next month
        current_date = add_months(current_date, 1)
    
    headers = ["inventory_id", "product_id", "warehouse_id", "date", "quantity_on_hand", 
              "quantity_allocated", "days_of_supply", "inventory_value", "reorder_point", 
              "max_capacity", "lot_number", "expiration_date"]
    
    write_csv("inventory.csv", inventory_data, headers)
    return inventory_data

def generate_availability_data(products, retailers):
    """Generate product availability data."""
    availability_data = []
    availability_id = 1
    
    # Get our product IDs (brand_id 1-10)
    our_product_ids = [pid for pid, p in products.items() if p[3] <= 10]
    
    # Generate weekly snapshots
    current_date = START_DATE
    
    while current_date <= END_DATE:
        # Generate for a subset of retailer/product combinations
        # This avoids creating an enormous dataset
        num_combinations = 2000  # Limit number of entries per date
        
        # Create random combinations of products and retailers
        combinations = []
        for _ in range(num_combinations):
            product_id = random.choice(our_product_ids)
            retailer_id = random.randint(1, 20)
            combinations.append((product_id, retailer_id))
        
        for product_id, retailer_id in combinations:
            product = products[product_id]
            retailer = retailers[retailer_id]
            
            # Base availability - generally high for most products
            base_in_stock = random.uniform(0.85, 0.98)  # 85-98% in stock
            
            # Adjust for retailer tier
            retailer_tier_factors = {
                "Strategic": 1.05,  # Better availability at strategic accounts
                "Key": 1.02,
                "Core": 1.0,
                "Small": 0.95  # Less consistent availability
            }
            base_in_stock *= retailer_tier_factors[retailer[6]]
            
            # Cap at 1.0 (100%)
            base_in_stock = min(base_in_stock, 1.0)
            
            # Apply supply chain disruptions
            for disruption in DISRUPTIONS:
                if disruption["start_date"] <= current_date <= disruption["end_date"]:
                    category_id = product[4]
                    category_name = None  # Would need categories lookup
                    
                    affected_categories = disruption["affected_categories"]
                    if category_name in affected_categories or "All" in affected_categories:
                        base_in_stock *= disruption["impact"]
            
            # Calculate final in_stock_percentage
            in_stock_percentage = round(base_in_stock * 100, 2)  # Convert to percentage
            
            # Out of stock incidents
            if in_stock_percentage < 80:
                out_of_stock_incidents = random.randint(3, 8)
            elif in_stock_percentage < 90:
                out_of_stock_incidents = random.randint(1, 3)
            else:
                out_of_stock_incidents = random.randint(0, 1)
            
            # On-shelf availability might be lower than in-stock
            on_shelf_availability = round(in_stock_percentage * random.uniform(0.9, 0.99), 2)
            
            # Is online flag
            is_online = retailer[4]  # has_ecommerce
            if is_online:
                is_online_sale = random.random() < 0.3  # 30% chance of being an online record
            else:
                is_online_sale = False
            
            # Days of supply
            days_of_supply = random.randint(5, 30)
            
            # Notes
            notes = None
            if in_stock_percentage < 70:
                notes = "Critical availability issue"
            elif in_stock_percentage < 85:
                notes = "Availability below target"
            
            availability_data.append([
                availability_id,
                product_id,
                retailer_id,
                current_date.strftime("%Y-%m-%d"),
                in_stock_percentage,
                out_of_stock_incidents,
                on_shelf_availability,
                is_online_sale,
                days_of_supply,
                notes
            ])
            
            availability_id += 1
        
        # Move to next week
        current_date += datetime.timedelta(days=7)
    
    headers = ["availability_id", "product_id", "retailer_id", "date", "in_stock_percentage", 
              "out_of_stock_incidents", "on_shelf_availability", "is_online", "days_of_supply", "notes"]
    
    write_csv("availability.csv", availability_data, headers)
    return availability_data

def generate_assortment_data(products, retailers):
    """Generate assortment planning data."""
    assortment_data = []
    assortment_id = 1
    
    # Get our product IDs (brand_id 1-10)
    our_product_ids = [pid for pid, p in products.items() if p[3] <= 10]
    
    # For each retailer
    for retailer_id, retailer in retailers.items():
        # Determine how many products this retailer carries
        # Based on retailer tier
        assortment_size_factors = {
            "Strategic": 0.8,  # Carries 80% of our products
            "Key": 0.6,
            "Core": 0.4,
            "Small": 0.2
        }
        
        assortment_size = int(len(our_product_ids) * assortment_size_factors[retailer[6]])
        retailer_products = random.sample(our_product_ids, assortment_size)
        
        for product_id in retailer_products:
            product = products[product_id]
            
            # Determine status
            if product[16]:  # is_seasonal
                status = "Seasonal"
                
                # Seasonal products have specific timeframes
                if product[4] == 27:  # Candy
                    # Halloween candy
                    start_date = datetime.date(2022, 9, 1)
                    end_date = datetime.date(2022, 11, 15)
                elif product[4] == 7:  # Oatmeal
                    # Winter seasonal
                    start_date = datetime.date(2022, 10, 1)
                    end_date = datetime.date(2023, 3, 31)
                else:
                    # Generic seasonal period
                    start_date = datetime.date(2022, random.choice([1, 4, 7, 10]), 1)
                    end_date = start_date + datetime.timedelta(days=90)
            else:
                # Non-seasonal products
                status = "Active"
                start_date = START_DATE
                end_date = None
                
                # Some products might be discontinued
                if product[13]:  # discontinue_date
                    status = "Discontinued"
                    end_date = datetime.datetime.strptime(product[13], "%Y-%m-%d").date()
                
                # Some might be planned but not yet active
                elif random.random() < 0.1:  # 10% chance
                    status = "Planned"
                    start_date = datetime.date(2024, random.randint(1, 12), 1)
            
            # Core assortment flag - high velocity products are usually core
            is_core_assortment = product[17] or random.random() < 0.4  # 40% chance or high velocity
            
            # Promotional only flag - some products only appear during promotions
            is_promotional_only = False
            if not is_core_assortment and random.random() < 0.2:  # 20% chance if not core
                is_promotional_only = True
            
            # Online only flag - some products are only available online
            is_online_only = False
            if retailer[4]:  # has_ecommerce
                if random.random() < 0.15:  # 15% chance for online-only products
                    is_online_only = True
            
            # Planogram position - aisle and shelf location
            aisles = ["A", "B", "C", "D", "E", "F"]
            sections = list(range(1, 21))
            planogram_position = f"{random.choice(aisles)}{random.choice(sections)}"
            
            # Facings - number of product facings on shelf
            # Based on product velocity and retailer tier
            if product[17]:  # high_velocity
                base_facings = random.randint(3, 6)
            else:
                base_facings = random.randint(1, 3)
                
            retailer_tier_factors = {
                "Strategic": 1.5,
                "Key": 1.2,
                "Core": 1.0,
                "Small": 0.8
            }
            
            facings = int(base_facings * retailer_tier_factors[retailer[6]])
            facings = max(1, facings)  # At least 1 facing
            
            # Notes
            notes = None
            if is_promotional_only:
                notes = "Promotional feature only"
            elif is_online_only:
                notes = "E-commerce exclusive"
            elif status == "Discontinued":
                notes = "Being replaced by new product"
            
            assortment_data.append([
                assortment_id,
                product_id,
                retailer_id,
                start_date.strftime("%Y-%m-%d"),
                end_date.strftime("%Y-%m-%d") if end_date else None,
                status,
                is_core_assortment,
                is_promotional_only,
                is_online_only,
                planogram_position,
                facings,
                notes
            ])
            
            assortment_id += 1
    
    headers = ["assortment_id", "product_id", "retailer_id", "start_date", "end_date", 
              "status", "is_core_assortment", "is_promotional_only", "is_online_only", 
              "planogram_position", "facings", "notes"]
    
    write_csv("assortment.csv", assortment_data, headers)
    return assortment_data

def generate_demand_forecasts(products, retailers):
    """Generate demand forecast data."""
    forecast_data = []
    forecast_id = 1
    
    # Get our product IDs (brand_id 1-10)
    our_product_ids = [pid for pid, p in products.items() if p[3] <= 10]
    
    # Generate quarterly forecasts for the next year
    current_date = datetime.date.today()
    
    # Start from the beginning of the current quarter
    current_quarter_start = datetime.date(current_date.year, ((current_date.month - 1) // 3) * 3 + 1, 1)
    
    # Go back 1 quarter to include some historical forecasts
    forecast_start = add_months(current_quarter_start, -3)
    
    # Generate forecasts for 5 quarters (1 past, current, 3 future)
    for quarter in range(5):
        forecast_date = add_months(forecast_start, quarter * 3)
        
        # Forecast period is the quarter
        forecast_period_start = forecast_date
        forecast_period_end = add_months(forecast_period_start, 3) - datetime.timedelta(days=1)
        
        # Select some retailer/product combinations
        # Using fewer combinations to keep the dataset manageable
        num_combinations = 3000
        
        combinations = []
        for _ in range(num_combinations):
            product_id = random.choice(our_product_ids)
            retailer_id = random.randint(1, 20)
            combinations.append((product_id, retailer_id))
        
        for product_id, retailer_id in combinations:
            product = products[product_id]
            retailer = retailers[retailer_id]
            
            # Base forecast quantity - depends on product velocity and retailer size
            if product[17]:  # high_velocity
                base_quantity = random.randint(5000, 20000)
            else:
                base_quantity = random.randint(1000, 5000)
                
            retailer_tier_factors = {
                "Strategic": 5.0,
                "Key": 3.0,
                "Core": 1.5,
                "Small": 0.5
            }
            
            forecasted_quantity = int(base_quantity * retailer_tier_factors[retailer[6]])
            
            # Apply seasonality
            quarter_months = [forecast_period_start.month, 
                             add_months(forecast_period_start, 1).month,
                             add_months(forecast_period_start, 2).month]
            
            avg_seasonality = sum(SEASONALITY.get(month, 1.0) for month in quarter_months) / 3
            forecasted_quantity = int(forecasted_quantity * avg_seasonality)
            
            # Apply trends
            days_since_start = (forecast_period_start - START_DATE).days
            total_days = (END_DATE - START_DATE).days
            progress = days_since_start / total_days if total_days > 0 else 0
            
            # Apply relevant trends
            trend_factor = 1.0
            
            # E-commerce growth
            if retailer[2] in [6, 7, 10]:  # E-commerce channels
                ecomm_trend = TRENDS["E-commerce Growth"]
                ecomm_factor = ecomm_trend["start"] + (ecomm_trend["end"] - ecomm_trend["start"]) * progress
                trend_factor *= ecomm_factor
            
            # Organic growth
            if product[14]:  # is_organic
                organic_trend = TRENDS["Organic Growth"]
                organic_factor = organic_trend["start"] + (organic_trend["end"] - organic_trend["start"]) * progress
                trend_factor *= organic_factor
            
            # Gluten-free growth
            if product[15]:  # is_glutenfree
                gf_trend = TRENDS["Gluten-Free Growth"]
                gf_factor = gf_trend["start"] + (gf_trend["end"] - gf_trend["start"]) * progress
                trend_factor *= gf_factor
            
            # Category-specific trends
            category_id = product[4]
            if category_id == 3:  # Snacks
                snack_trend = TRENDS["Snacking Increase"]
                snack_factor = snack_trend["start"] + (snack_trend["end"] - snack_trend["start"]) * progress
                trend_factor *= snack_factor
            elif category_id == 1:  # Breakfast
                breakfast_trend = TRENDS["Breakfast Decline"]
                breakfast_factor = breakfast_trend["start"] + (breakfast_trend["end"] - breakfast_trend["start"]) * progress
                trend_factor *= breakfast_factor
            
            forecasted_quantity = int(forecasted_quantity * trend_factor)
            
            # Forecast confidence
            # Confidence decreases for forecasts further in the future
            base_confidence = 0.9  # Start with high confidence
            quarters_in_future = quarter
            confidence_decay = 0.05 * quarters_in_future  # 5% less confidence per quarter
            forecast_confidence = round(max(0.5, base_confidence - confidence_decay), 2)
            
            # Actual quantity - Only for past quarters
            if forecast_period_end < datetime.date.today():
                # Actual is forecast plus some error
                error_factor = random.uniform(-0.15, 0.15)  # ±15% error
                actual_quantity = int(forecasted_quantity * (1 + error_factor))
                forecast_error_percentage = round(abs(error_factor) * 100, 2)
            else:
                actual_quantity = None
                forecast_error_percentage = None
            
            # Notes
            notes = None
            if forecast_confidence < 0.7:
                notes = "Low confidence forecast - market volatility"
            elif product[16]:  # is_seasonal
                notes = "Seasonal product - forecast highly dependent on weather conditions"
            
            forecast_data.append([
                forecast_id,
                product_id,
                retailer_id,
                forecast_date.strftime("%Y-%m-%d"),
                forecast_period_start.strftime("%Y-%m-%d"),
                forecast_period_end.strftime("%Y-%m-%d"),
                forecasted_quantity,
                forecast_confidence,
                actual_quantity,
                forecast_error_percentage,
                notes
            ])
            
            forecast_id += 1
    
    headers = ["forecast_id", "product_id", "retailer_id", "forecast_date", 
              "forecast_period_start", "forecast_period_end", "forecasted_quantity", 
              "forecast_confidence", "actual_quantity", "forecast_error_percentage", "notes"]
    
    write_csv("demand_forecasts.csv", forecast_data, headers)
    return forecast_data

def generate_supply_chain_events():
    """Generate supply chain disruption events."""
    events = []
    event_id = 1
    
    # Use the global DISRUPTIONS list
    for disruption in DISRUPTIONS:
        # Convert affected_categories to product IDs
        # For demo purposes, use placeholder IDs
        affected_products = "{1,2,3,4,5}"
        affected_warehouses = "{1,2,3}"
        
        impact_estimate = f"Estimated {int((1 - disruption['impact']) * 100)}% reduction in availability"
        
        mitigation_actions = [
            "Secured alternative suppliers",
            "Increased safety stock levels",
            "Expedited shipping",
            "Shifted production to alternate facilities",
            "Implemented temporary rationing",
            "Reallocated inventory from less critical channels",
            "Adjusted promotional calendar"
        ]
        
        events.append([
            event_id,
            disruption["description"],
            disruption["start_date"].strftime("%Y-%m-%d"),
            disruption["end_date"].strftime("%Y-%m-%d"),
            disruption["severity"],
            disruption["description"],
            affected_products,
            affected_warehouses,
            impact_estimate,
            random.choice(mitigation_actions)
        ])
        
        event_id += 1
    
    headers = ["event_id", "event_type", "start_date", "end_date", "severity", 
              "description", "affected_products", "affected_warehouses", 
              "impact_estimate", "mitigation_actions"]
    
    write_csv("supply_chain_events.csv", events, headers)
    return events

def generate_shipping_data(products, warehouses, data_scale=1.0):
    """Generate shipping data."""
    shipping_data = []
    shipping_id = 1
    
    # Get our product IDs (brand_id 1-10)
    our_product_ids = [pid for pid, p in products.items() if p[3] <= 10]
    
    # Generate shipments for the past year
    start_date = max(START_DATE, datetime.date.today() - datetime.timedelta(days=365))
    end_date = datetime.date.today()
    
    current_date = start_date
    
    while current_date <= end_date:
        # Number of shipments per day varies
        # More shipments on weekdays
        weekday = current_date.weekday()
        if weekday < 5:  # Monday-Friday
            num_shipments = int(random.randint(15, 30) * data_scale)
        else:  # Weekend
            num_shipments = int(random.randint(5, 15) * data_scale)
        
        for _ in range(num_shipments):
            # Select origin warehouse
            origin_warehouse_id = random.randint(1, 10)
            
            # Determine destination type
            destination_type = random.choice(["Warehouse", "Retailer", "Customer"])
            
            # Select destination ID based on type
            if destination_type == "Warehouse":
                # Ship to another warehouse (not the same one)
                destination_warehouses = [w for w in range(1, 11) if w != origin_warehouse_id]
                destination_id = random.choice(destination_warehouses)
            elif destination_type == "Retailer":
                destination_id = random.randint(1, 20)  # Retailer ID
            else:  # Customer
                destination_id = None  # Direct to customer, no specific ID
            
            # Select product
            product_id = random.choice(our_product_ids)
            product = products[product_id]
            
            # Quantity depends on destination type
            if destination_type == "Warehouse":
                quantity = random.randint(100, 1000)
            elif destination_type == "Retailer":
                quantity = random.randint(10, 200)
            else:  # Customer
                quantity = random.randint(1, 5)
            
            # Shipping dates
            ship_date = current_date
            
            # Expected arrival based on distance and type
            if destination_type == "Warehouse":
                transit_days = random.randint(2, 5)
            elif destination_type == "Retailer":
                transit_days = random.randint(1, 3)
            else:  # Customer
                transit_days = random.randint(1, 7)  # Wider range for customer shipping
            
            expected_arrival_date = ship_date + datetime.timedelta(days=transit_days)
            
            # For past shipments, determine if delivered and when
            if expected_arrival_date <= datetime.date.today():
                # Most shipments arrive on time
                on_time_chance = 0.8
                
                if random.random() < on_time_chance:
                    actual_arrival_date = expected_arrival_date
                    status = "Delivered"
                else:
                    # Late delivery - anywhere from 1 to 5 days late
                    delay_days = random.randint(1, 5)
                    actual_arrival_date = expected_arrival_date + datetime.timedelta(days=delay_days)
                    
                    if actual_arrival_date <= datetime.date.today():
                        status = "Delivered"
                    else:
                        status = "Delayed"
                        actual_arrival_date = None
            else:
                # Future deliveries
                if ship_date == datetime.date.today():
                    status = "In Transit"
                else:
                    status = "Planned"
                
                actual_arrival_date = None
            
            # Small chance of cancelled shipment
            if random.random() < 0.02:  # 2% chance
                status = "Cancelled"
                actual_arrival_date = None
            
            # Tracking and carrier
            carriers = ["Fast Freight", "Reliable Shipping", "Express Logistics", "Value Transport", "Premium Delivery"]
            carrier = random.choice(carriers)
            
            tracking_prefix = ''.join(word[0] for word in carrier.split())
            tracking_number = f"{tracking_prefix}{random.randint(10000000, 99999999)}"
            
            # Shipping cost
            base_cost_per_unit = 0.5  # $0.50 per unit
            distance_factor = random.uniform(1.0, 3.0)  # Cost multiplier based on distance
            
            shipping_cost = round(quantity * base_cost_per_unit * distance_factor, 2)
            
            shipping_data.append([
                shipping_id,
                origin_warehouse_id,
                destination_type,
                destination_id,
                product_id,
                quantity,
                ship_date.strftime("%Y-%m-%d"),
                expected_arrival_date.strftime("%Y-%m-%d"),
                actual_arrival_date.strftime("%Y-%m-%d") if actual_arrival_date else None,
                status,
                tracking_number,
                carrier,
                shipping_cost
            ])
            
            shipping_id += 1
        
        # Move to next day
        current_date += datetime.timedelta(days=1)
    
    headers = ["shipping_id", "origin_warehouse_id", "destination_type", "destination_id", 
              "product_id", "quantity", "ship_date", "expected_arrival_date", "actual_arrival_date", 
              "status", "tracking_number", "carrier", "shipping_cost"]
    
    write_csv("shipping.csv", shipping_data, headers)
    return shipping_data

# Utility functions between these functions and main()
def add_months(date, months):
    """Add months to a date, handling month end correctly."""
    month = date.month - 1 + months
    year = date.year + month // 12
    month = month % 12 + 1
    
    # Handle day values that might not exist in the target month
    day = min(date.day, [31, 29 if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0) else 28, 
                          31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month-1])
    
    return datetime.date(year, month, day)

def get_month_end(date):
    """Get the last day of the month for a given date."""
    next_month = add_months(date, 1)
    month_end = next_month.replace(day=1) - datetime.timedelta(days=1)
    return month_end

def brand_matches_category(brand, category):
    """Determine if a brand is relevant for a category."""
    # Would need more complex logic in a real implementation
    return True

# Data size presets
DATA_SIZE_PRESETS = {
    "tiny": {
        "transactions": 1000,
        "data_scale": 0.1,
        "date_range": (datetime.date(2024, 1, 1), datetime.date(2024, 3, 31)),  # 3 months
        "description": "Minimal dataset for quick testing"
    },
    "small": {
        "transactions": 5000,
        "data_scale": 0.25,
        "date_range": (datetime.date(2023, 7, 1), datetime.date(2024, 3, 31)),  # 9 months
        "description": "Small dataset for development and testing"
    },
    "medium": {
        "transactions": 50000,
        "data_scale": 1.0,
        "date_range": (START_DATE, END_DATE),  # Full range
        "description": "Moderate-sized dataset for analysis and visualization"
    },
    "large": {
        "transactions": 200000,
        "data_scale": 2.5,
        "date_range": (START_DATE, END_DATE),  # Full range
        "description": "Large dataset for comprehensive analysis"
    },
    "enterprise": {
        "transactions": 1000000,
        "data_scale": 5.0,
        "date_range": (START_DATE, END_DATE),  # Full range
        "description": "Enterprise-scale dataset for performance testing"
    }
}

def main():
    """Main function to generate all data."""
    parser = argparse.ArgumentParser(description='Generate CPG e-commerce data for analytics demo')
    parser.add_argument('--size', type=str, choices=["tiny", "small", "medium", "large", "enterprise"], 
                        default="tiny", help='Size of dataset to generate')
    parser.add_argument('--scale', type=float, default=None, 
                   help='Custom scale factor for data volume (overrides size preset)')
    parser.add_argument('--transactions', type=int, default=None,
                   help='Custom number of transactions to generate (overrides size preset)')
    args = parser.parse_args()
    
    # Apply size preset
    size_preset = DATA_SIZE_PRESETS[args.size]
    num_transactions = size_preset["transactions"] if args.transactions is None else args.transactions
    data_scale = size_preset["data_scale"] if args.scale is None else args.scale
    date_range = size_preset["date_range"]
    
    
    print(f"Generating {args.size} dataset (scale factor: {data_scale}, transactions: ~{num_transactions})")
    print(f"Date range: {date_range[0]} to {date_range[1]}")
    print(f"Output directory: {OUTPUT_DIR}")
    
    # Generate base data
    print("Generating brands...")
    brands = generate_brands()
    
    print("Generating product categories...")
    categories = generate_categories()
    
    print("Generating products...")
    products = generate_products(brands, categories)
    
    print("Generating competitors...")
    competitors = generate_competitors()
    
    print("Generating channels...")
    channels = generate_channels()
    
    print("Generating retailers...")
    retailers = generate_retailers(channels)
    
    print("Generating warehouses...")
    warehouses = generate_warehouses()
    
    # Generate transaction and analysis data
    print("Generating sales data...")
    sales_data = generate_sales_data(products, retailers, 
                                     start_date=date_range[0], 
                                     end_date=date_range[1], 
                                     num_transactions=num_transactions)
    
    print("Generating market share data...")
    market_shares = generate_market_shares(brands, categories, channels)
    
    print("Generating promotions...")
    promotions = generate_promotions(products, channels)
    
    print("Generating inventory data...")
    inventory_data = generate_inventory_data(products, warehouses)
    
    print("Generating availability data...")
    availability_data = generate_availability_data(products, retailers)
    
    print("Generating assortment data...")
    assortment_data = generate_assortment_data(products, retailers)
    
    print("Generating demand forecasts...")
    forecast_data = generate_demand_forecasts(products, retailers)
    
    print("Generating supply chain events...")
    events = generate_supply_chain_events()
    
    print("Generating shipping data...")
    shipping_data = generate_shipping_data(products, warehouses, data_scale=data_scale)

    write_promotion_product(flush=True)
    
    print(f"All data generated in {OUTPUT_DIR} directory")
    print(f"Dataset size: {args.size} - {size_preset['description']}")

if __name__ == "__main__":
    main()