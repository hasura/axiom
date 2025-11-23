
#!/usr/bin/env python3
"""
ShelfWise Synthetic Data Generator
Generates realistic, non-random synthetic dataset for grocery/retail analytics
with seasonality, trends, causal signals, lag effects, and explainable correlations.
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import json
import os
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

# Set deterministic seed for reproducibility
np.random.seed(42)
rng = np.random.default_rng(42)

# Configuration
START_DATE = datetime(2019, 1, 1)
END_DATE = datetime(2025, 11, 30)
NUM_DAYS = (END_DATE - START_DATE).days + 1

# Output directory - postgres subdirectory for Docker mounting
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'postgres')

class ShelfWiseDataGenerator:
    def __init__(self):
        """Initialize the data generator with configuration."""
        self.start_date = START_DATE
        self.end_date = END_DATE
        self.num_days = NUM_DAYS
        self.dates = pd.date_range(start=START_DATE, end=END_DATE, freq='D')

        # Initialize data containers
        self.products = None
        self.stores = None
        self.calendar = None
        self.promotions = None
        self.assortment = None
        self.ground_truth_events = None

        # Category configurations
        self.categories = {
            'cereal': {'elasticity': -0.6, 'seasonality': 'steady', 'dow_effect': 0.05},
            'dairy': {'elasticity': -0.8, 'seasonality': 'steady', 'dow_effect': 0.10},
            'snacks': {'elasticity': -1.0, 'seasonality': 'event_driven', 'dow_effect': 0.15},
            'beverages': {'elasticity': -1.2, 'seasonality': 'summer', 'dow_effect': 0.12},
            'produce': {'elasticity': -0.9, 'seasonality': 'steady', 'dow_effect': 0.08},
            'household': {'elasticity': -0.4, 'seasonality': 'steady', 'dow_effect': -0.05},
            'frozen': {'elasticity': -0.7, 'seasonality': 'winter', 'dow_effect': 0.06},
            'bakery': {'elasticity': -0.8, 'seasonality': 'steady', 'dow_effect': 0.12},
            'meat': {'elasticity': -0.9, 'seasonality': 'event_driven', 'dow_effect': 0.18},
            'canned': {'elasticity': -0.5, 'seasonality': 'winter', 'dow_effect': 0.03},
            'personal_care': {'elasticity': -0.6, 'seasonality': 'steady', 'dow_effect': 0.02},
            'candy': {'elasticity': -1.1, 'seasonality': 'event_driven', 'dow_effect': 0.10}
        }

        # Brand configurations with realistic manufacturer and ShelfWise private label brands
        self.brands = [
            # ShelfWise Private Label Brands
            {'name': 'ShelfWise Select', 'tier': 'premium', 'popularity': 1.1},  # Premium private label
            {'name': 'ShelfWise Basics', 'tier': 'value', 'popularity': 1.25},  # Value private label
            {'name': 'ShelfWise Organic', 'tier': 'premium', 'popularity': 0.9},  # Organic private label
            {'name': 'ShelfWise Fresh', 'tier': 'mid', 'popularity': 1.15},  # Fresh/produce private label

            # Major CPG Manufacturers
            {'name': 'Kelloggs', 'tier': 'premium', 'popularity': 1.2},
            {'name': 'General Mills', 'tier': 'premium', 'popularity': 1.15},
            {'name': 'Nestle', 'tier': 'mid', 'popularity': 1.1},
            {'name': 'Kraft Heinz', 'tier': 'mid', 'popularity': 1.3},
            {'name': 'PepsiCo', 'tier': 'mid', 'popularity': 1.2},
            {'name': 'Coca-Cola', 'tier': 'mid', 'popularity': 1.25},
            {'name': 'Unilever', 'tier': 'premium', 'popularity': 1.0},
            {'name': 'Procter & Gamble', 'tier': 'premium', 'popularity': 1.05},
            {'name': 'Campbell Soup', 'tier': 'mid', 'popularity': 0.95},
            {'name': 'ConAgra', 'tier': 'mid', 'popularity': 0.9},
            {'name': 'Mondelez', 'tier': 'mid', 'popularity': 1.1},  # Oreo, Cadbury, etc.
            {'name': 'Mars', 'tier': 'premium', 'popularity': 1.05},  # M&Ms, Snickers, etc.
            {'name': 'Hershey', 'tier': 'mid', 'popularity': 1.0},
            {'name': 'Frito-Lay', 'tier': 'mid', 'popularity': 1.35},  # Chips and snacks
            {'name': 'Quaker', 'tier': 'mid', 'popularity': 1.0},
            {'name': 'Dole', 'tier': 'mid', 'popularity': 0.95},
            {'name': 'Del Monte', 'tier': 'mid', 'popularity': 0.9},
            {'name': 'Tyson Foods', 'tier': 'mid', 'popularity': 1.1},
            {'name': 'Hormel', 'tier': 'mid', 'popularity': 0.95},
            {'name': 'Smithfield', 'tier': 'value', 'popularity': 0.9},
            {'name': 'Perdue', 'tier': 'mid', 'popularity': 0.95},
            {'name': 'Danone', 'tier': 'premium', 'popularity': 0.85},  # Yogurt, dairy
            {'name': 'Chobani', 'tier': 'premium', 'popularity': 0.9},
            {'name': 'Blue Diamond', 'tier': 'premium', 'popularity': 0.8},  # Nuts, almond products
            {'name': 'Wonderful', 'tier': 'premium', 'popularity': 0.85},  # Pistachios, POM
            {'name': 'Annies Homegrown', 'tier': 'premium', 'popularity': 0.85},
            {'name': 'Organic Valley', 'tier': 'premium', 'popularity': 0.8},
            {'name': 'Horizon Organic', 'tier': 'premium', 'popularity': 0.75},
            {'name': 'Bobs Red Mill', 'tier': 'premium', 'popularity': 0.7},
            {'name': 'Kind', 'tier': 'premium', 'popularity': 0.85},  # Snack bars
            {'name': 'Clif Bar', 'tier': 'premium', 'popularity': 0.8},
            {'name': 'Nature Valley', 'tier': 'mid', 'popularity': 1.05},
            {'name': 'Nabisco', 'tier': 'mid', 'popularity': 1.15},  # Cookies, crackers
            {'name': 'Ritz', 'tier': 'mid', 'popularity': 1.1},
            {'name': 'Pepperidge Farm', 'tier': 'premium', 'popularity': 0.95},
            {'name': 'Barilla', 'tier': 'mid', 'popularity': 1.0},  # Pasta
            {'name': 'Hunts', 'tier': 'value', 'popularity': 0.95},
            {'name': 'Progresso', 'tier': 'mid', 'popularity': 0.9},
            {'name': 'Swanson', 'tier': 'value', 'popularity': 0.85},
            {'name': 'Green Giant', 'tier': 'mid', 'popularity': 0.95},
            {'name': 'Birds Eye', 'tier': 'mid', 'popularity': 0.9},
            {'name': 'Lean Cuisine', 'tier': 'mid', 'popularity': 0.85},
            {'name': 'Stouffers', 'tier': 'mid', 'popularity': 0.95},
            {'name': 'DiGiorno', 'tier': 'premium', 'popularity': 1.0},
            {'name': 'Haagen-Dazs', 'tier': 'premium', 'popularity': 0.9},
            {'name': 'Ben & Jerrys', 'tier': 'premium', 'popularity': 0.95},
            {'name': 'Breyers', 'tier': 'mid', 'popularity': 1.0},
            {'name': 'Dreyers', 'tier': 'mid', 'popularity': 0.95},
            {'name': 'PolarSprings', 'tier': 'mid', 'popularity': 1.0},  # Keep for vendor shortage scenario
            {'name': 'Dasani', 'tier': 'mid', 'popularity': 0.95},
            {'name': 'Smartwater', 'tier': 'premium', 'popularity': 0.85},
            {'name': 'Fiji', 'tier': 'premium', 'popularity': 0.8},
            {'name': 'Poland Spring', 'tier': 'value', 'popularity': 1.1},
            {'name': 'Gatorade', 'tier': 'mid', 'popularity': 1.15},
            {'name': 'Powerade', 'tier': 'mid', 'popularity': 0.95},
            {'name': 'Tropicana', 'tier': 'premium', 'popularity': 1.05},
            {'name': 'Simply', 'tier': 'premium', 'popularity': 0.95},
            {'name': 'Minute Maid', 'tier': 'mid', 'popularity': 1.0},
            {'name': 'Ocean Spray', 'tier': 'mid', 'popularity': 0.9}
        ]

        # Store regions and types
        self.regions = ['west', 'southwest', 'midwest', 'northeast', 'southeast', 'nationwide']
        self.store_types = ['urban', 'suburban', 'convenience', 'big_box', 'online']
        self.climate_zones = {
            'west': 'temperate',
            'southwest': 'hot',
            'midwest': 'cold',
            'northeast': 'cold',
            'southeast': 'hot',
            'nationwide': 'controlled'  # For online/warehouse
        }

        # Comprehensive holiday data for US, Canada, and UK (2010-2025)
        # Using actual dates for major holidays
        self.holidays = self._generate_all_holidays()

    def _generate_all_holidays(self) -> dict:
        """Generate comprehensive holiday data for US, Canada, and UK from 2010-2025."""
        holidays = {
            'us': {},
            'canada': {},
            'uk': {}
        }

        # Generate holidays for each year from 2010 to 2025
        for year in range(2010, 2026):
            # US Holidays
            holidays['us'][year] = {
                'New Year': datetime(year, 1, 1),
                'MLK Day': self._get_nth_weekday(year, 1, 0, 3),  # 3rd Monday in January
                'Super Bowl Sunday': self._get_first_sunday_february(year),
                'Valentine\'s Day': datetime(year, 2, 14),
                'Presidents Day': self._get_nth_weekday(year, 2, 0, 3),  # 3rd Monday in February
                'Easter': self._calculate_easter(year),
                'Memorial Day': self._get_last_monday_may(year),
                'Independence Day': datetime(year, 7, 4),
                'Labor Day': self._get_nth_weekday(year, 9, 0, 1),  # 1st Monday in September
                'Columbus Day': self._get_nth_weekday(year, 10, 0, 2),  # 2nd Monday in October
                'Halloween': datetime(year, 10, 31),
                'Veterans Day': datetime(year, 11, 11),
                'Thanksgiving': self._get_nth_weekday(year, 11, 3, 4),  # 4th Thursday in November
                'Black Friday': self._get_nth_weekday(year, 11, 3, 4) + timedelta(days=1),
                'Cyber Monday': self._get_nth_weekday(year, 11, 3, 4) + timedelta(days=4),
                'Christmas Eve': datetime(year, 12, 24),
                'Christmas': datetime(year, 12, 25),
                'New Years Eve': datetime(year, 12, 31)
            }

            # Canada Holidays
            holidays['canada'][year] = {
                'New Year': datetime(year, 1, 1),
                'Family Day': self._get_nth_weekday(year, 2, 0, 3) if year >= 2013 else None,  # 3rd Monday in February (varies by province)
                'Good Friday': self._calculate_easter(year) - timedelta(days=2),
                'Easter Monday': self._calculate_easter(year) + timedelta(days=1),
                'Victoria Day': self._get_monday_before_may_25(year),
                'Canada Day': datetime(year, 7, 1),
                'Civic Holiday': self._get_nth_weekday(year, 8, 0, 1),  # 1st Monday in August
                'Labour Day': self._get_nth_weekday(year, 9, 0, 1),  # 1st Monday in September
                'Thanksgiving': self._get_nth_weekday(year, 10, 0, 2),  # 2nd Monday in October
                'Remembrance Day': datetime(year, 11, 11),
                'Christmas Eve': datetime(year, 12, 24),
                'Christmas': datetime(year, 12, 25),
                'Boxing Day': datetime(year, 12, 26),
                'New Years Eve': datetime(year, 12, 31)
            }

            # UK Holidays
            holidays['uk'][year] = {
                'New Year': datetime(year, 1, 1),
                'New Year Holiday': datetime(year, 1, 2) if datetime(year, 1, 1).weekday() == 6 else None,  # If Jan 1 is Sunday
                'Good Friday': self._calculate_easter(year) - timedelta(days=2),
                'Easter Monday': self._calculate_easter(year) + timedelta(days=1),
                'Early May Bank Holiday': self._get_nth_weekday(year, 5, 0, 1),  # 1st Monday in May
                'Spring Bank Holiday': self._get_last_monday_may(year),
                'Summer Bank Holiday': self._get_last_monday_august(year),  # Scotland: 1st Monday, England/Wales: Last Monday
                'Christmas Eve': datetime(year, 12, 24),
                'Christmas': datetime(year, 12, 25),
                'Boxing Day': datetime(year, 12, 26),
                'New Years Eve': datetime(year, 12, 31)
            }

            # Special UK holidays
            if year == 2011:
                holidays['uk'][year]['Royal Wedding'] = datetime(2011, 4, 29)
            if year == 2012:
                holidays['uk'][year]['Diamond Jubilee'] = datetime(2012, 6, 5)
            if year == 2022:
                holidays['uk'][year]['Platinum Jubilee'] = datetime(2022, 6, 3)
            if year == 2023:
                holidays['uk'][year]['Coronation'] = datetime(2023, 5, 8)

        # Remove None values
        for country in holidays:
            for year in holidays[country]:
                holidays[country][year] = {k: v for k, v in holidays[country][year].items() if v is not None}

        return holidays

    def _calculate_easter(self, year: int) -> datetime:
        """Calculate Easter Sunday using the Computus algorithm."""
        a = year % 19
        b = year // 100
        c = year % 100
        d = b // 4
        e = b % 4
        f = (b + 8) // 25
        g = (b - f + 1) // 3
        h = (19 * a + b - d - g + 15) % 30
        i = c // 4
        k = c % 4
        l = (32 + 2 * e + 2 * i - h - k) % 7
        m = (a + 11 * h + 22 * l) // 451
        month = (h + l - 7 * m + 114) // 31
        day = ((h + l - 7 * m + 114) % 31) + 1
        return datetime(year, month, day)

    def _get_nth_weekday(self, year: int, month: int, weekday: int, n: int) -> datetime:
        """Get the nth occurrence of a weekday in a month."""
        first_day = datetime(year, month, 1)
        first_weekday = first_day.weekday()
        days_until_weekday = (weekday - first_weekday) % 7
        first_occurrence = first_day + timedelta(days=days_until_weekday)
        return first_occurrence + timedelta(weeks=n-1)

    def _get_last_monday_may(self, year: int) -> datetime:
        """Get the last Monday in May."""
        last_day = datetime(year, 5, 31)
        days_back = (last_day.weekday() - 0) % 7
        if days_back == 0 and last_day.weekday() != 0:
            days_back = 7
        return last_day - timedelta(days=days_back)

    def _get_last_monday_august(self, year: int) -> datetime:
        """Get the last Monday in August."""
        last_day = datetime(year, 8, 31)
        days_back = (last_day.weekday() - 0) % 7
        if days_back == 0 and last_day.weekday() != 0:
            days_back = 7
        return last_day - timedelta(days=days_back)

    def _get_monday_before_may_25(self, year: int) -> datetime:
        """Get the Monday on or before May 25 (Victoria Day in Canada)."""
        may_25 = datetime(year, 5, 25)
        days_back = may_25.weekday()
        if days_back == 0:  # May 25 is already Monday
            return may_25
        return may_25 - timedelta(days=days_back)

    def _get_first_sunday_february(self, year: int) -> datetime:
        """Get the first Sunday in February (approximate Super Bowl date)."""
        # Super Bowl is typically first or second Sunday in February
        first_day = datetime(year, 2, 1)
        days_until_sunday = (6 - first_day.weekday()) % 7
        if days_until_sunday == 0:
            days_until_sunday = 7
        return first_day + timedelta(days=days_until_sunday)

    def generate_products(self) -> pd.DataFrame:
        """Generate products with Pareto distribution of demand."""
        products_list = []
        product_id = 1

        # Generate SKUs with long tail distribution
        for brand_info in self.brands:
            for category in self.categories.keys():
                # Number of SKUs per brand-category (REDUCED for faster processing)
                if brand_info['tier'] == 'premium':
                    num_skus = 1  # Reduced from rng.choice([1, 2], p=[0.7, 0.3])
                elif brand_info['tier'] == 'mid':
                    num_skus = 1  # Reduced from rng.choice([2, 3, 4], p=[0.3, 0.5, 0.2])
                else:  # value
                    num_skus = 1  # Reduced from rng.choice([3, 4, 5], p=[0.2, 0.5, 0.3])

                for sku_idx in range(num_skus):
                    # Expanded and more realistic sub-categories
                    sub_categories = {
                        'cereal': ['oats', 'corn_flakes', 'granola', 'kids_cereal', 'muesli', 'bran', 'rice_cereal', 'wheat_cereal'],
                        'dairy': ['whole_milk', '2_percent_milk', 'skim_milk', 'cheese', 'yogurt', 'butter', 'cream_cheese', 'sour_cream', 'cottage_cheese', 'ice_cream'],
                        'snacks': ['potato_chips', 'tortilla_chips', 'crackers', 'nuts', 'popcorn', 'pretzels', 'trail_mix', 'rice_cakes', 'fruit_snacks', 'granola_bars'],
                        'beverages': ['cola', 'lemon_lime_soda', 'juice', 'bottled_water', 'energy_drinks', 'sports_drinks', 'coffee', 'tea', 'sparkling_water', 'kombucha'],
                        'produce': ['apples', 'bananas', 'oranges', 'berries', 'lettuce', 'tomatoes', 'potatoes', 'onions', 'carrots', 'broccoli', 'avocados'],
                        'household': ['paper_towels', 'toilet_paper', 'dish_soap', 'laundry_detergent', 'batteries', 'trash_bags', 'aluminum_foil', 'plastic_wrap', 'cleaning_spray'],
                        'frozen': ['ice_cream', 'frozen_meals', 'frozen_vegetables', 'pizza', 'frozen_fruit', 'frozen_breakfast', 'frozen_seafood', 'frozen_desserts'],
                        'bakery': ['white_bread', 'wheat_bread', 'bagels', 'muffins', 'croissants', 'donuts', 'cakes', 'cookies', 'pies', 'rolls'],
                        'meat': ['chicken_breast', 'ground_beef', 'pork_chops', 'bacon', 'sausage', 'deli_meat', 'salmon', 'shrimp', 'steak', 'turkey'],
                        'canned': ['soup', 'canned_vegetables', 'canned_fruit', 'beans', 'pasta_sauce', 'canned_meat', 'broth', 'tomato_sauce', 'canned_fish'],
                        'personal_care': ['shampoo', 'body_wash', 'toothpaste', 'deodorant', 'razors', 'lotion', 'sunscreen', 'hand_soap', 'mouthwash', 'hair_gel'],
                        'candy': ['chocolate_bars', 'gummies', 'hard_candy', 'lollipops', 'mints', 'caramels', 'licorice', 'seasonal_candy', 'sugar_free']
                    }

                    sub_category = rng.choice(sub_categories.get(category, ['general']))

                    # Generate size variations
                    sizes = {
                        'beverages': ['500ml', '1L', '2L', '355ml'],
                        'cereal': ['300g', '500g', '750g', '1kg'],
                        'snacks': ['100g', '200g', '450g', 'family_size'],
                        'dairy': ['500ml', '1L', '2L', '250g', '500g'],
                        'default': ['small', 'medium', 'large', 'xl']
                    }
                    size = rng.choice(sizes.get(category, sizes['default']))

                    # Calculate pricing based on tier and category
                    base_price = rng.uniform(2, 20)
                    if brand_info['tier'] == 'premium':
                        list_price = base_price * 1.5
                    elif brand_info['tier'] == 'value':
                        list_price = base_price * 0.8
                    else:
                        list_price = base_price

                    cost = list_price * rng.uniform(0.5, 0.7)

                    # SKU naming convention - use first 3 chars of brand for better uniqueness
                    brand_code = ''.join([c for c in brand_info['name'].replace(' ', '').upper() if c.isalnum()])[:3]
                    cat_code = category[:3].upper()
                    subcat_code = sub_category.replace('_', '')[:4].upper()
                    size_code = size.replace(' ', '_').upper()
                    sku = f"{brand_code}-{cat_code}-{subcat_code}-{size_code}-{product_id:04d}"

                    # Launch and discontinue dates
                    launch_date = START_DATE
                    discontinue_date = None

                    # Add 2-3 new launches mid-period
                    if product_id in [150, 151, 152]:
                        launch_date = START_DATE + timedelta(days=180)

                    # Add 2 discontinues
                    if product_id in [50, 51]:
                        discontinue_date = START_DATE + timedelta(days=270)

                    # Special case for tracking specific products during events
                    if category == 'household' and sub_category == 'paper' and product_id == 100:
                        sku = 'PL-PAPER-TP-12PK'  # Toilet paper for COVID tracking

                    products_list.append({
                        'product_id': product_id,
                        'sku': sku,
                        'brand': brand_info['name'],
                        'category': category,
                        'sub_category': sub_category,
                        'size': size,
                        'unit_of_measure': 'each',
                        'list_price': round(list_price, 2),
                        'cost': round(cost, 2),
                        'launch_date': launch_date,
                        'discontinue_date': discontinue_date,
                        'brand_popularity': brand_info['popularity'],
                        'tier': brand_info['tier']
                    })

                    product_id += 1

                    # Limit total products to create Pareto distribution
                    if product_id > 200:
                        break
                if product_id > 200:
                    break

        self.products = pd.DataFrame(products_list)

        # Assign Pareto popularity scores (top 20% drive 80% of sales)
        num_products = len(self.products)
        pareto_scores = np.zeros(num_products)
        top_20_pct = int(num_products * 0.2)

        # Top 20% get 80% of the weight
        pareto_scores[:top_20_pct] = rng.exponential(scale=4, size=top_20_pct)
        # Bottom 80% get 20% of the weight
        pareto_scores[top_20_pct:] = rng.exponential(scale=0.5, size=num_products - top_20_pct)

        # Normalize and shuffle
        pareto_scores = pareto_scores / pareto_scores.sum()
        rng.shuffle(pareto_scores)

        self.products['pareto_weight'] = pareto_scores

        return self.products

    def generate_stores(self) -> pd.DataFrame:
        """Generate stores with regions, types, climate zones, and geographic coordinates."""
        stores_list = []
        store_id = 1

        # Define actual city locations with lat/long coordinates
        # Organized by region with realistic city distributions
        city_locations = {
            'west': [
                {'city': 'Los Angeles, CA', 'lat': 34.0522, 'lon': -118.2437},
                {'city': 'San Francisco, CA', 'lat': 37.7749, 'lon': -122.4194},
                {'city': 'San Diego, CA', 'lat': 32.7157, 'lon': -117.1611},
                {'city': 'Portland, OR', 'lat': 45.5152, 'lon': -122.6784},
                {'city': 'Seattle, WA', 'lat': 47.6062, 'lon': -122.3321},
                {'city': 'Sacramento, CA', 'lat': 38.5816, 'lon': -121.4944},
                {'city': 'Fresno, CA', 'lat': 36.7378, 'lon': -119.7871},
                {'city': 'Oakland, CA', 'lat': 37.8044, 'lon': -122.2712},
                {'city': 'San Jose, CA', 'lat': 37.3382, 'lon': -121.8863},
                {'city': 'Long Beach, CA', 'lat': 33.7701, 'lon': -118.1937},
                {'city': 'Anaheim, CA', 'lat': 33.8366, 'lon': -117.9143},
                {'city': 'Riverside, CA', 'lat': 33.9806, 'lon': -117.3755},
                {'city': 'Spokane, WA', 'lat': 47.6588, 'lon': -117.4260},
                {'city': 'Tacoma, WA', 'lat': 47.2529, 'lon': -122.4443},
                {'city': 'Eugene, OR', 'lat': 44.0521, 'lon': -123.0868},
            ],
            'southwest': [
                {'city': 'Phoenix, AZ', 'lat': 33.4484, 'lon': -112.0740},
                {'city': 'Las Vegas, NV', 'lat': 36.1699, 'lon': -115.1398},
                {'city': 'Albuquerque, NM', 'lat': 35.0853, 'lon': -106.6056},
                {'city': 'Tucson, AZ', 'lat': 32.2226, 'lon': -110.9747},
                {'city': 'Mesa, AZ', 'lat': 33.4152, 'lon': -111.8315},
                {'city': 'El Paso, TX', 'lat': 31.7619, 'lon': -106.4850},
                {'city': 'Henderson, NV', 'lat': 36.0395, 'lon': -114.9817},
                {'city': 'Scottsdale, AZ', 'lat': 33.4942, 'lon': -111.9261},
                {'city': 'Chandler, AZ', 'lat': 33.3062, 'lon': -111.8413},
                {'city': 'Glendale, AZ', 'lat': 33.5387, 'lon': -112.1860},
                {'city': 'Santa Fe, NM', 'lat': 35.6870, 'lon': -105.9378},
                {'city': 'Reno, NV', 'lat': 39.5296, 'lon': -119.8138},
            ],
            'midwest': [
                {'city': 'Chicago, IL', 'lat': 41.8781, 'lon': -87.6298},
                {'city': 'Detroit, MI', 'lat': 42.3314, 'lon': -83.0458},
                {'city': 'Minneapolis, MN', 'lat': 44.9778, 'lon': -93.2650},
                {'city': 'Milwaukee, WI', 'lat': 43.0389, 'lon': -87.9065},
                {'city': 'Columbus, OH', 'lat': 39.9612, 'lon': -82.9988},
                {'city': 'Indianapolis, IN', 'lat': 39.7684, 'lon': -86.1581},
                {'city': 'Cleveland, OH', 'lat': 41.4993, 'lon': -81.6944},
                {'city': 'Kansas City, MO', 'lat': 39.0997, 'lon': -94.5786},
                {'city': 'St. Louis, MO', 'lat': 38.6270, 'lon': -90.1994},
                {'city': 'Cincinnati, OH', 'lat': 39.1031, 'lon': -84.5120},
                {'city': 'St. Paul, MN', 'lat': 44.9537, 'lon': -93.0900},
                {'city': 'Madison, WI', 'lat': 43.0731, 'lon': -89.4012},
                {'city': 'Des Moines, IA', 'lat': 41.5868, 'lon': -93.6250},
                {'city': 'Omaha, NE', 'lat': 41.2565, 'lon': -95.9345},
                {'city': 'Grand Rapids, MI', 'lat': 42.9634, 'lon': -85.6681},
            ],
            'northeast': [
                {'city': 'New York, NY', 'lat': 40.7128, 'lon': -74.0060},
                {'city': 'Philadelphia, PA', 'lat': 39.9526, 'lon': -75.1652},
                {'city': 'Boston, MA', 'lat': 42.3601, 'lon': -71.0589},
                {'city': 'Washington, DC', 'lat': 38.9072, 'lon': -77.0369},
                {'city': 'Baltimore, MD', 'lat': 39.2904, 'lon': -76.6122},
                {'city': 'Pittsburgh, PA', 'lat': 40.4406, 'lon': -79.9959},
                {'city': 'Buffalo, NY', 'lat': 42.8864, 'lon': -78.8784},
                {'city': 'Newark, NJ', 'lat': 40.7357, 'lon': -74.1724},
                {'city': 'Jersey City, NJ', 'lat': 40.7282, 'lon': -74.0776},
                {'city': 'Hartford, CT', 'lat': 41.7658, 'lon': -72.6734},
                {'city': 'Providence, RI', 'lat': 41.8240, 'lon': -71.4128},
                {'city': 'Rochester, NY', 'lat': 43.1566, 'lon': -77.6088},
                {'city': 'Albany, NY', 'lat': 42.6526, 'lon': -73.7562},
                {'city': 'Syracuse, NY', 'lat': 43.0481, 'lon': -76.1474},
                {'city': 'Portland, ME', 'lat': 43.6591, 'lon': -70.2568},
            ],
            'southeast': [
                {'city': 'Atlanta, GA', 'lat': 33.7490, 'lon': -84.3880},
                {'city': 'Miami, FL', 'lat': 25.7617, 'lon': -80.1918},
                {'city': 'Tampa, FL', 'lat': 27.9506, 'lon': -82.4572},
                {'city': 'Orlando, FL', 'lat': 28.5383, 'lon': -81.3792},
                {'city': 'Charlotte, NC', 'lat': 35.2271, 'lon': -80.8431},
                {'city': 'Nashville, TN', 'lat': 36.1627, 'lon': -86.7816},
                {'city': 'Memphis, TN', 'lat': 35.1495, 'lon': -90.0490},
                {'city': 'Louisville, KY', 'lat': 38.2527, 'lon': -85.7585},
                {'city': 'Jacksonville, FL', 'lat': 30.3322, 'lon': -81.6557},
                {'city': 'Richmond, VA', 'lat': 37.5407, 'lon': -77.4360},
                {'city': 'Raleigh, NC', 'lat': 35.7796, 'lon': -78.6382},
                {'city': 'Birmingham, AL', 'lat': 33.5186, 'lon': -86.8104},
                {'city': 'New Orleans, LA', 'lat': 29.9511, 'lon': -90.0715},
                {'city': 'Charleston, SC', 'lat': 32.7765, 'lon': -79.9311},
                {'city': 'Savannah, GA', 'lat': 32.0809, 'lon': -81.0912},
            ],
            'international': [
                # Canada
                {'city': 'Toronto, ON', 'lat': 43.6532, 'lon': -79.3832},
                {'city': 'Vancouver, BC', 'lat': 49.2827, 'lon': -123.1207},
                {'city': 'Montreal, QC', 'lat': 45.5017, 'lon': -73.5673},
                # UK
                {'city': 'London, UK', 'lat': 51.5074, 'lon': -0.1278},
            ]
        }

        # Add online store first (store_id = 1) - the biggest revenue driver
        # Located at a major fulfillment center in Columbus, OH (central US location)
        stores_list.append({
            'store_id': store_id,
            'region': 'nationwide',  # Online serves all regions
            'store_type': 'online',
            'sq_ft': 500000,  # Represents warehouse/fulfillment center space
            'opened_date': START_DATE - timedelta(days=1825),  # 5 years old
            'climate_zone': 'controlled',  # Climate-controlled warehouse
            'city': 'Columbus, OH (Fulfillment Center)',
            'latitude': 39.9612,
            'longitude': -82.9988
        })
        store_id += 1

        # Generate 250 physical stores with realistic distribution for a mid-size retailer
        store_distribution = {
            'urban': {'count': 60, 'avg_sqft': 15000},
            'suburban': {'count': 100, 'avg_sqft': 35000},
            'convenience': {'count': 50, 'avg_sqft': 5000},
            'big_box': {'count': 40, 'avg_sqft': 80000}
        }

        # Track which cities have been used to avoid too many stores in one city
        city_store_counts = {}

        for store_type, config in store_distribution.items():
            for i in range(config['count']):
                # Allocate some stores to international locations (5 total)
                if store_id in [245, 246, 247, 248, 249, 250, 251]:  # Last 7 stores
                    if store_id <= 249:  # 5 in Canada
                        region = 'international'
                        available_cities = city_locations['international'][:3]  # Canadian cities
                    else:  # 2 in UK
                        region = 'international'
                        available_cities = [city_locations['international'][3]]  # London
                else:
                    region = rng.choice([r for r in self.regions if r != 'nationwide' and r != 'international'])
                    available_cities = city_locations.get(region, city_locations['midwest'])

                # Select a city, preferring less-used cities
                city_weights = []
                for city_info in available_cities:
                    city_name = city_info['city']
                    # Give lower weight to cities that already have many stores
                    count = city_store_counts.get(city_name, 0)
                    weight = 1.0 / (1.0 + count * 0.3)  # Reduce probability for cities with existing stores
                    city_weights.append(weight)

                # Normalize weights
                total_weight = sum(city_weights)
                city_weights = [w/total_weight for w in city_weights]

                # Select city
                selected_city = rng.choice(available_cities, p=city_weights)
                city_store_counts[selected_city['city']] = city_store_counts.get(selected_city['city'], 0) + 1

                # Add very small random offset to coordinates (within ~1 mile) to simulate different locations in same city
                # Using much smaller offset to avoid placing stores in water for coastal cities
                lat_offset = rng.normal(0, 0.01)  # ~0.7 miles standard deviation
                lon_offset = rng.normal(0, 0.01)  # ~0.7 miles standard deviation

                # For coastal cities, bias the offset inland to avoid ocean placement
                coastal_cities = ['San Francisco', 'San Diego', 'Seattle', 'Portland, ME', 'Miami',
                                 'Tampa', 'Jacksonville', 'Charleston', 'Savannah', 'Long Beach',
                                 'Oakland', 'Vancouver', 'London']

                if any(coastal in selected_city['city'] for coastal in coastal_cities):
                    # For west coast cities, bias slightly east (positive longitude)
                    if selected_city['lon'] < -100:  # West coast
                        lon_offset = abs(lon_offset) * 0.5  # Small positive offset (east)
                    # For east coast cities, bias slightly west (negative longitude)
                    elif selected_city['lon'] > -85:  # East coast
                        lon_offset = -abs(lon_offset) * 0.5  # Small negative offset (west)
                    # For UK (London), bias slightly north/west
                    elif 'London' in selected_city['city']:
                        lon_offset = -abs(lon_offset) * 0.3
                        lat_offset = abs(lat_offset) * 0.3
                    # Reduce overall offset magnitude for all coastal cities
                    lat_offset *= 0.5
                    lon_offset *= 0.5

                # Vary square footage
                sq_ft = int(config['avg_sqft'] * rng.uniform(0.7, 1.3))

                # Opening dates (most stores are established, few are new)
                if store_id > 245:  # Last 5 stores are new
                    opened_date = START_DATE - timedelta(days=int(rng.integers(30, 180)))
                else:
                    opened_date = START_DATE - timedelta(days=int(rng.integers(365, 3650)))

                # Determine climate zone
                if region == 'international':
                    if 'Canada' in selected_city['city'] or 'ON' in selected_city['city'] or 'BC' in selected_city['city'] or 'QC' in selected_city['city']:
                        climate_zone = 'cold'
                    else:  # UK
                        climate_zone = 'temperate'
                else:
                    climate_zone = self.climate_zones[region]

                stores_list.append({
                    'store_id': store_id,
                    'region': region if region != 'international' else 'international',
                    'store_type': store_type,
                    'sq_ft': sq_ft,
                    'opened_date': opened_date,
                    'climate_zone': climate_zone,
                    'city': selected_city['city'],
                    'latitude': round(selected_city['lat'] + lat_offset, 4),
                    'longitude': round(selected_city['lon'] + lon_offset, 4)
                })

                store_id += 1

        self.stores = pd.DataFrame(stores_list)

        # Mark specific stores for competitor impact (urban west stores)
        self.stores['competitor_impact'] = False
        urban_west_stores = self.stores[(self.stores['store_type'] == 'urban') &
                                        (self.stores['region'] == 'west')].sample(n=min(3, len(self.stores[(self.stores['store_type'] == 'urban') & (self.stores['region'] == 'west')])), random_state=42)
        if len(urban_west_stores) > 0:
            self.stores.loc[urban_west_stores.index, 'competitor_impact'] = True

        return self.stores

    def generate_calendar(self) -> pd.DataFrame:
        """Generate calendar with holidays and events mapped by country."""
        calendar_list = []

        for date in self.dates:
            dow = date.dayofweek
            is_weekend = dow >= 5
            year = date.year

            # Check for holidays in each country
            event_name_us = None
            event_name_canada = None
            event_name_uk = None
            is_holiday_us = False
            is_holiday_canada = False
            is_holiday_uk = False

            # Check US holidays
            if year in self.holidays['us']:
                for holiday_name, holiday_date in self.holidays['us'][year].items():
                    if holiday_date and date.date() == holiday_date.date():
                        event_name_us = holiday_name
                        is_holiday_us = True
                        break
                    # Week-long events for US
                    elif holiday_name == 'Thanksgiving' and holiday_date and \
                         (holiday_date - timedelta(days=7) <= date <= holiday_date):
                        event_name_us = 'Thanksgiving Week'
                    elif holiday_name == 'Christmas' and holiday_date and \
                         (holiday_date - timedelta(days=7) <= date <= holiday_date):
                        event_name_us = 'Christmas Week'

            # Check Canada holidays
            if year in self.holidays['canada']:
                for holiday_name, holiday_date in self.holidays['canada'][year].items():
                    if holiday_date and date.date() == holiday_date.date():
                        event_name_canada = holiday_name
                        is_holiday_canada = True
                        break
                    # Week-long events for Canada
                    elif holiday_name == 'Christmas' and holiday_date and \
                         (holiday_date - timedelta(days=7) <= date <= holiday_date):
                        event_name_canada = 'Christmas Week'

            # Check UK holidays
            if year in self.holidays['uk']:
                for holiday_name, holiday_date in self.holidays['uk'][year].items():
                    if holiday_date and date.date() == holiday_date.date():
                        event_name_uk = holiday_name
                        is_holiday_uk = True
                        break
                    # Week-long events for UK
                    elif holiday_name == 'Christmas' and holiday_date and \
                         (holiday_date - timedelta(days=7) <= date <= holiday_date):
                        event_name_uk = 'Christmas Week'

            # Determine season
            month = date.month
            if month in [3, 4, 5]:
                season = 'spring'
            elif month in [6, 7, 8]:
                season = 'summer'
            elif month in [9, 10, 11]:
                season = 'fall'
            else:
                season = 'winter'

            calendar_list.append({
                'date': date.date(),
                'dow': dow,
                'is_weekend': is_weekend,
                'is_holiday_us': is_holiday_us,
                'is_holiday_canada': is_holiday_canada,
                'is_holiday_uk': is_holiday_uk,
                'month': month,
                'week_of_year': date.isocalendar()[1],
                'season': season,
                'event_name_us': event_name_us,
                'event_name_canada': event_name_canada,
                'event_name_uk': event_name_uk
            })

        self.calendar = pd.DataFrame(calendar_list)
        return self.calendar

    def generate_ground_truth_events(self) -> pd.DataFrame:
        """Generate ground truth events reflecting actual macroeconomic trends 2019-2025."""
        events = [
            # COVID-19 Pandemic - Panic buying phase (March 2020)
            {
                'event_id': 1,
                'start_date': datetime(2020, 3, 15),
                'end_date': datetime(2020, 4, 15),
                'region': None,  # Nationwide
                'sku': None,
                'label': 'covid_panic_buying',
                'magnitude': 0.8,  # 80% increase in essentials
                'notes': 'COVID-19 panic buying - toilet paper, canned goods, sanitizer surge'
            },
            # COVID-19 Lockdowns (April-May 2020)
            {
                'event_id': 2,
                'start_date': datetime(2020, 4, 1),
                'end_date': datetime(2020, 5, 31),
                'region': None,
                'sku': None,
                'label': 'covid_lockdown',
                'magnitude': -0.25,  # 25% reduction in non-essentials
                'notes': 'COVID-19 lockdowns - reduced shopping frequency, focus on essentials'
            },
            # Supply Chain Crisis (2021-2022)
            {
                'event_id': 3,
                'start_date': datetime(2021, 3, 1),
                'end_date': datetime(2022, 6, 30),
                'region': None,
                'sku': None,
                'label': 'supply_chain_crisis',
                'magnitude': -0.15,  # 15% stock availability issues
                'notes': 'Global supply chain disruptions - container shortages, port delays'
            },
            # Inflation Surge (2021-2023)
            {
                'event_id': 4,
                'start_date': datetime(2021, 6, 1),
                'end_date': datetime(2023, 12, 31),
                'region': None,
                'sku': None,
                'label': 'inflation_surge',
                'magnitude': 0.25,  # 25% price increases over period
                'notes': 'High inflation period - 7-9% annual inflation affecting grocery prices'
            },
            # Great Resignation Labor Shortage (2021-2022)
            {
                'event_id': 5,
                'start_date': datetime(2021, 9, 1),
                'end_date': datetime(2022, 12, 31),
                'region': None,
                'sku': None,
                'label': 'labor_shortage',
                'magnitude': -0.10,  # 10% service degradation
                'notes': 'Labor shortage - reduced store hours, longer checkout times'
            },
            # Ukraine War - Grain/Oil Impact (2022)
            {
                'event_id': 6,
                'start_date': datetime(2022, 2, 24),
                'end_date': datetime(2022, 12, 31),
                'region': None,
                'sku': None,
                'label': 'ukraine_war_impact',
                'magnitude': 0.15,  # 15% increase in grain/oil products
                'notes': 'Ukraine war - wheat, sunflower oil, fertilizer price spikes'
            },
            # Recession Fears - Consumer Pullback (2023)
            {
                'event_id': 7,
                'start_date': datetime(2023, 3, 1),
                'end_date': datetime(2023, 9, 30),
                'region': None,
                'sku': None,
                'label': 'recession_fears',
                'magnitude': -0.12,  # 12% reduction in discretionary
                'notes': 'Banking crisis and recession fears - shift to value brands'
            },
            # Post-Pandemic Normalization (2024)
            {
                'event_id': 8,
                'start_date': datetime(2024, 1, 1),
                'end_date': datetime(2024, 12, 31),
                'region': None,
                'sku': None,
                'label': 'normalization',
                'magnitude': 0.05,  # 5% steady growth
                'notes': 'Return to normal shopping patterns, steady growth'
            },
            # AI/Automation Adoption (2025)
            {
                'event_id': 9,
                'start_date': datetime(2025, 1, 1),
                'end_date': datetime(2025, 11, 30),
                'region': None,
                'sku': None,
                'label': 'ai_automation',
                'magnitude': 0.08,  # 8% efficiency gains
                'notes': 'AI-driven inventory optimization and personalized promotions'
            }
        ]

        self.ground_truth_events = pd.DataFrame(events)
        return self.ground_truth_events

    def generate_promotions(self) -> pd.DataFrame:
        """Generate promotions with realistic cadence and overlap."""
        promotions_list = []
        promo_id = 1

        # Select products for promotions (focus on high-velocity items)
        promo_products = self.products.nlargest(100, 'pareto_weight')

        for _, product in promo_products.iterrows():
            # Generate 4-6 promotions per product throughout the year
            num_promos = rng.integers(4, 7)

            # Space promotions throughout the year
            promo_starts = sorted(rng.integers(0, NUM_DAYS - 21, size=num_promos))

            for start_day in promo_starts:
                start_date = START_DATE + timedelta(days=int(start_day))

                # Promotion duration: 2-3 weeks on, few weeks off
                duration = rng.integers(14, 22)
                end_date = start_date + timedelta(days=int(duration))

                # Promotion types based on category
                if product['category'] in ['beverages', 'snacks']:
                    promo_type = rng.choice(['price_cut', 'bogo', 'display', 'feature'],
                                           p=[0.4, 0.2, 0.2, 0.2])
                else:
                    promo_type = rng.choice(['price_cut', 'display', 'feature'],
                                           p=[0.5, 0.25, 0.25])

                # Discount percentage
                if promo_type == 'price_cut':
                    discount_pct = rng.choice([10, 15, 20, 25, 30], p=[0.2, 0.3, 0.3, 0.15, 0.05])
                elif promo_type == 'bogo':
                    discount_pct = 50
                else:
                    discount_pct = 0  # Feature or display only

                # Display type
                if promo_type in ['display', 'feature']:
                    display_type = rng.choice(['endcap', 'aisle', 'checkout'], p=[0.5, 0.3, 0.2])
                else:
                    display_type = 'none'

                # Ad feature
                ad_feature = rng.choice([True, False], p=[0.3, 0.7])

                # Expected uplift calculation
                base_uplift = 1.0
                if discount_pct > 0:
                    base_uplift += discount_pct / 100 * abs(self.categories[product['category']]['elasticity'])
                if display_type == 'endcap':
                    base_uplift *= 1.3
                elif display_type == 'aisle':
                    base_uplift *= 1.15
                elif display_type == 'checkout':
                    base_uplift *= 1.4
                if ad_feature:
                    base_uplift *= 1.2

                # Supplier funding (60% of promotions have funding)
                supplier_funding = 0
                if rng.random() < 0.6:
                    supplier_funding = round(discount_pct * product['list_price'] *
                                            rng.uniform(0.3, 0.7) * 100, 2)

                promotions_list.append({
                    'promo_id': promo_id,
                    'sku': product['sku'],
                    'start_date': start_date.date(),
                    'end_date': end_date.date(),
                    'promo_type': promo_type,
                    'discount_pct': discount_pct,
                    'ad_feature': ad_feature,
                    'display_type': display_type,
                    'expected_uplift': round(base_uplift, 2),
                    'supplier_funding_usd': supplier_funding
                })

                promo_id += 1

        self.promotions = pd.DataFrame(promotions_list)

        # Add intentional cannibalization (e.g., 1L and 500ml sodas)
        # This is handled in the demand model

        return self.promotions

    def generate_assortment(self) -> pd.DataFrame:
        """Generate store-SKU assortment matrix."""
        assortment_list = []

        for _, store in self.stores.iterrows():
            # Number of SKUs carried depends on store type
            if store['store_type'] == 'online':
                num_skus = len(self.products)  # Online carries everything
            elif store['store_type'] == 'big_box':
                num_skus = int(len(self.products) * 0.95)
            elif store['store_type'] == 'suburban':
                num_skus = int(len(self.products) * 0.80)
            elif store['store_type'] == 'urban':
                num_skus = int(len(self.products) * 0.70)
            else:  # convenience
                num_skus = int(len(self.products) * 0.40)

            # Select SKUs based on popularity and store type
            if store['store_type'] == 'online':
                # Online carries all products
                selected_products = self.products
            elif store['store_type'] == 'convenience':
                # Focus on high-velocity items
                selected_products = self.products.nlargest(num_skus, 'pareto_weight')
            else:
                # Mix of products with bias toward popular items
                selected_products = self.products.sample(n=num_skus, weights='pareto_weight',
                                                        random_state=store['store_id'])

            for _, product in selected_products.iterrows():
                # Planogram facings based on product popularity and store size
                base_facings = max(1, int(product['pareto_weight'] * 100))
                if store['store_type'] == 'online':
                    facings = 999  # Unlimited virtual shelf space
                elif store['store_type'] == 'big_box':
                    facings = base_facings * 3
                elif store['store_type'] == 'suburban':
                    facings = base_facings * 2
                else:
                    facings = base_facings

                # Shelf height
                shelf_height = rng.uniform(120, 200)

                # Active dates (some products enter/exit during period)
                active_from = START_DATE
                active_to = None

                # New products
                if product['launch_date'] > START_DATE:
                    active_from = product['launch_date']

                # Discontinued products
                if pd.notna(product['discontinue_date']):
                    active_to = product['discontinue_date']

                assortment_list.append({
                    'store_id': store['store_id'],
                    'sku': product['sku'],
                    'active_from': active_from.date() if isinstance(active_from, datetime) else active_from,
                    'active_to': active_to.date() if isinstance(active_to, datetime) else active_to,
                    'planogram_facings': facings,
                    'shelf_height_cm': round(shelf_height, 2)
                })

        self.assortment = pd.DataFrame(assortment_list)
        return self.assortment

    def calculate_demand(self, date: datetime, store: pd.Series, product: pd.Series,
                        active_promos: pd.DataFrame, compliance_score: float = 85) -> float:
        """
        Calculate demand using multiplicative model with deterministic factors.
        """
        # Base demand
        brand_pop = product['brand_popularity']
        category_pop = 1.0 + (0.2 if product['category'] in ['beverages', 'snacks'] else 0)
        store_type_factor = {
            'online': 15.0,  # Online store drives 10-15x more volume than physical stores
            'big_box': 1.5,
            'suburban': 1.2,
            'urban': 1.0,
            'convenience': 0.7
        }[store['store_type']]

        region_factor = {
            'west': 1.1,
            'southwest': 1.05,
            'midwest': 1.0,
            'northeast': 1.0,
            'southeast': 0.95,
            'nationwide': 1.2,  # Online store serves all regions, slight premium
            'international': 1.15  # International stores have good performance
        }[store['region']]

        # Price elastic baseline
        price_elastic = 1.0 - (product['list_price'] - 10) * 0.01

        units_base = (brand_pop * category_pop * store_type_factor *
                     region_factor * price_elastic * product['pareto_weight'] * 1000)

        # Daily multipliers
        multiplier = 1.0

        # Seasonality
        month = date.month
        climate = store['climate_zone']
        category = product['category']

        if category == 'beverages':
            if climate in ['hot', 'temperate'] and month in [6, 7, 8]:
                multiplier *= 1.4
            elif climate == 'cold' and month in [12, 1, 2]:
                multiplier *= 0.8
        elif category in ['canned', 'frozen']:
            if climate == 'cold' and month in [11, 12, 1, 2]:
                multiplier *= 1.3
        elif category == 'candy':
            if month == 10:  # Halloween
                multiplier *= 2.5
            elif month == 3:  # Easter
                multiplier *= 1.8
        elif category == 'snacks':
            # Check for Super Bowl Sunday (US only)
            if store['region'] != 'international':
                year = date.year
                if year in self.holidays['us'] and 'Super Bowl Sunday' in self.holidays['us'][year]:
                    if date.date() == self.holidays['us'][year]['Super Bowl Sunday'].date():
                        multiplier *= 2.0

        # Day of week effect
        dow = date.dayofweek
        dow_effect = self.categories[category]['dow_effect']
        if store['store_type'] == 'online':
            # Online has different patterns - stronger on weekdays for convenience
            if dow >= 5:  # Weekend
                multiplier *= 0.9  # Slightly lower on weekends
            else:
                multiplier *= 1.1  # Higher on weekdays
            # Cyber Monday boost (check appropriate country)
            calendar_row = self.calendar[self.calendar['date'] == date.date()]
            if not calendar_row.empty:
                # Determine which country's holidays to use based on store location
                if store['region'] == 'international':
                    # Check if it's a Canadian or UK store based on city
                    if any(loc in store['city'] for loc in ['ON', 'BC', 'QC', 'Toronto', 'Vancouver', 'Montreal']):
                        event_name = calendar_row.iloc[0].get('event_name_canada', None)
                    elif 'UK' in store['city'] or 'London' in store['city']:
                        event_name = calendar_row.iloc[0].get('event_name_uk', None)
                    else:
                        event_name = None
                else:
                    # US stores
                    event_name = calendar_row.iloc[0].get('event_name_us', None)

                if event_name == 'Cyber Monday':
                    multiplier *= 2.5  # Major boost for online on Cyber Monday
        elif dow >= 5:  # Weekend for physical stores
            multiplier *= (1 + dow_effect)
        else:
            if store['store_type'] == 'urban' and category == 'snacks':
                multiplier *= (1 - dow_effect * 0.5)  # Inverted for urban

        # Holiday lift based on store location
        calendar_row = self.calendar[self.calendar['date'] == date.date()]
        if not calendar_row.empty:
            # Determine which country's holidays to use
            if store['region'] == 'international':
                if any(loc in store['city'] for loc in ['ON', 'BC', 'QC', 'Toronto', 'Vancouver', 'Montreal']):
                    event = calendar_row.iloc[0].get('event_name_canada', None)
                    # Canada-specific holiday lifts
                    holiday_lifts = {
                        'Thanksgiving': {'meat': 1.6, 'produce': 1.4, 'bakery': 1.5},  # Canada Thanksgiving is in October
                        'Christmas Week': {'candy': 1.7, 'beverages': 1.3, 'snacks': 1.4},
                        'Boxing Day': {'snacks': 1.3, 'beverages': 1.2},  # Boxing Day shopping
                        'Canada Day': {'meat': 1.5, 'beverages': 1.4, 'snacks': 1.3},  # BBQ season
                        'Victoria Day': {'meat': 1.4, 'beverages': 1.3},  # Long weekend
                        'Easter': {'candy': 1.8, 'meat': 1.3},
                        'Easter Monday': {'candy': 1.5}
                    }
                elif 'UK' in store['city'] or 'London' in store['city']:
                    event = calendar_row.iloc[0].get('event_name_uk', None)
                    # UK-specific holiday lifts
                    holiday_lifts = {
                        'Christmas Week': {'candy': 1.6, 'beverages': 1.3, 'snacks': 1.3},
                        'Boxing Day': {'snacks': 1.4, 'beverages': 1.2},
                        'Easter': {'candy': 1.7, 'meat': 1.2},
                        'Easter Monday': {'candy': 1.4},
                        'Summer Bank Holiday': {'meat': 1.3, 'beverages': 1.3, 'snacks': 1.2},
                        'Spring Bank Holiday': {'meat': 1.2, 'beverages': 1.2}
                    }
                else:
                    event = None
                    holiday_lifts = {}
            else:
                # US stores
                event = calendar_row.iloc[0].get('event_name_us', None)
                holiday_lifts = {
                    'Thanksgiving Week': {'meat': 1.8, 'produce': 1.5, 'bakery': 1.6},
                    'Christmas Week': {'candy': 1.7, 'beverages': 1.3, 'snacks': 1.4},
                    'Super Bowl Sunday': {'snacks': 2.0, 'beverages': 1.6, 'meat': 1.4},
                    'Halloween': {'candy': 2.5},
                    'Easter': {'candy': 1.8, 'meat': 1.3},
                    'Independence Day': {'meat': 1.6, 'beverages': 1.4, 'snacks': 1.3},  # July 4th BBQ
                    'Memorial Day': {'meat': 1.5, 'beverages': 1.3},  # BBQ season start
                    'Labor Day': {'meat': 1.4, 'beverages': 1.2}  # BBQ season end
                }

            if event and event in holiday_lifts and category in holiday_lifts[event]:
                multiplier *= holiday_lifts[event][category]

        # Promotion uplift
        if not active_promos.empty:
            promo = active_promos.iloc[0]
            if promo['discount_pct'] > 0:
                elasticity = abs(self.categories[category]['elasticity'])
                multiplier *= (1 + promo['discount_pct'] / 100 * elasticity)

            if promo['display_type'] == 'endcap':
                multiplier *= 1.3
            elif promo['display_type'] == 'aisle':
                multiplier *= 1.15
            elif promo['display_type'] == 'checkout':
                multiplier *= 1.4

            if promo['ad_feature']:
                multiplier *= 1.2

        # Planogram compliance effect
        if compliance_score < 70:
            multiplier *= (0.6 + compliance_score / 175)  # Scale 0.6-1.0

        # Ground truth macroeconomic events
        for _, event in self.ground_truth_events.iterrows():
            if pd.to_datetime(event['start_date']) <= date <= pd.to_datetime(event['end_date']):

                if event['label'] == 'covid_panic_buying':
                    # Massive increase for essentials
                    if category in ['household', 'canned', 'frozen', 'personal_care']:
                        multiplier *= (1 + event['magnitude'] * 1.5)  # 120% increase
                    elif category in ['produce', 'dairy', 'meat']:
                        multiplier *= (1 + event['magnitude'] * 0.8)  # 64% increase
                    else:
                        multiplier *= (1 + event['magnitude'] * 0.3)  # 24% increase

                elif event['label'] == 'covid_lockdown':
                    # Reduction in non-essentials, increase in comfort foods
                    if category in ['candy', 'snacks', 'beverages']:
                        multiplier *= 1.1  # Comfort food increase
                    elif category in ['personal_care']:
                        multiplier *= 0.6  # Reduced grooming needs
                    else:
                        multiplier *= (1 + event['magnitude'])  # General reduction

                elif event['label'] == 'supply_chain_crisis':
                    # Random stockouts and availability issues
                    if rng.random() < 0.15:  # 15% chance of stockout
                        multiplier *= 0.3  # Severe shortage
                    else:
                        multiplier *= 0.95  # Slight reduction

                elif event['label'] == 'inflation_surge':
                    # Price elasticity effects - consumers buy less as prices rise
                    elasticity = abs(self.categories[category]['elasticity'])
                    price_increase = event['magnitude'] * (date - pd.to_datetime(event['start_date'])).days / 365
                    multiplier *= (1 - price_increase * elasticity * 0.3)  # Demand reduction

                elif event['label'] == 'labor_shortage':
                    # Service issues lead to slight demand reduction
                    if store['store_type'] != 'online':
                        multiplier *= 0.92  # 8% reduction due to poor service

                elif event['label'] == 'ukraine_war_impact':
                    # Grain and oil products affected
                    if category in ['bakery', 'cereal', 'snacks']:
                        multiplier *= 0.85  # Reduced demand due to high prices

                elif event['label'] == 'recession_fears':
                    # Shift to value brands and essentials
                    if product['brand'] in ['ShelfWise Basics']:  # Value brand
                        multiplier *= 1.25  # Increase in value brand
                    elif product['tier'] == 'premium':
                        multiplier *= 0.75  # Decrease in premium
                    else:
                        multiplier *= 0.90  # General reduction

                elif event['label'] == 'normalization':
                    # Steady growth return
                    multiplier *= (1 + event['magnitude'])

                elif event['label'] == 'ai_automation':
                    # Better inventory management and targeted promotions
                    if store['store_type'] == 'online':
                        multiplier *= 1.15  # Online benefits more
                    else:
                        multiplier *= 1.08  # Physical stores benefit too

        # Add small noise (max 3% of expectation)
        noise = rng.normal(1.0, 0.03)
        multiplier *= max(0.5, min(2.0, noise))

        # Calculate final demand
        daily_demand = units_base * multiplier

        return max(0, int(daily_demand))

    def generate_daily_data(self) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """Generate daily sales, inventory, returns, and other operational data."""
        sales_list = []
        inventory_list = []
        returns_list = []
        orders_list = []
        supplier_shipments_list = []
        waste_spoilage_list = []
        tickets_list = []
        feedback_list = []
        price_changes_list = []

        # Initialize inventory levels
        current_inventory = {}
        system_inventory = {}

        # Initialize tracking variables
        shipment_id = 1
        waste_id = 1

        ticket_id = 1
        feedback_id = 1
        change_id = 1

        # Process each day
        print(f"Generating daily data for {len(self.dates)} days with {len(self.stores)} stores...")
        for date_idx, date in enumerate(self.dates):
            if date_idx % 30 == 0:
                print(f"  Processing day {date_idx}/{len(self.dates)}...")

            date_str = date.date()

            # Daily orders tracking
            daily_orders = {}

            # Process each store
            for _, store in self.stores.iterrows():
                store_id = store['store_id']

                # Initialize daily order counts
                if store_id not in daily_orders:
                    daily_orders[store_id] = {'orders_count': 0, 'fulfilled_orders': 0}

                # Get active assortment for this store
                store_assortment = self.assortment[
                    (self.assortment['store_id'] == store_id) &
                    (self.assortment['active_from'] <= date_str) &
                    ((self.assortment['active_to'].isna()) | (self.assortment['active_to'] >= date_str))
                ]

                # Process each SKU in assortment
                # Online store processes more SKUs since it's the biggest revenue driver
                if store['store_type'] == 'online':
                    # Process 20% of SKUs for online store to capture its high volume
                    sampled_assortment = store_assortment.sample(frac=0.2, random_state=date_idx) if len(store_assortment) > 10 else store_assortment
                else:
                    # Sample 5% for physical stores for performance with 250 stores
                    sampled_assortment = store_assortment.sample(frac=0.05, random_state=date_idx) if len(store_assortment) > 10 else store_assortment
                for _, assort in sampled_assortment.iterrows():
                    sku = assort['sku']
                    product = self.products[self.products['sku'] == sku].iloc[0]

                    # Check for active promotions
                    active_promos = self.promotions[
                        (self.promotions['sku'] == sku) &
                        (self.promotions['start_date'] <= date_str) &
                        (self.promotions['end_date'] >= date_str)
                    ]

                    # Calculate demand (using default compliance of 85)
                    demand = self.calculate_demand(date, store, product, active_promos, 85)

                    # Get current inventory
                    inv_key = (store_id, sku)
                    if inv_key not in current_inventory:
                        # Initial inventory based on store type and product popularity
                        if store['store_type'] == 'online':
                            base_stock = demand * 14  # Online maintains 14 days of coverage
                        else:
                            base_stock = demand * 7  # 7 days of coverage for physical stores
                        current_inventory[inv_key] = int(base_stock * rng.uniform(0.8, 1.2))
                        system_inventory[inv_key] = current_inventory[inv_key]

                    on_hand = current_inventory[inv_key]
                    system_on_hand = system_inventory[inv_key]

                    # Calculate safety stock
                    safety_stock = int(demand * 3)  # 3 days of safety stock

                    # Replenishment logic (simple order-up-to)
                    if store['store_type'] == 'online':
                        target_inventory = demand * 20  # Online maintains higher inventory
                    else:
                        target_inventory = demand * 10  # 10 days of coverage
                    on_order = 0
                    in_transit = 0

                    if on_hand < safety_stock:
                        # Place order
                        on_order = target_inventory - on_hand

                        # Check for disruptions
                        for _, event in self.ground_truth_events.iterrows():
                            if (event['label'] == 'vendor_shortage' and
                                pd.to_datetime(event['start_date']) <= date <= pd.to_datetime(event['end_date']) and
                                store['region'] == event['region'] and
                                'PolarSprings' in product['brand']):
                                on_order = int(on_order * 0.4)  # 60% reduction

                    # Simulate deliveries and create shipment records
                    # Online has more frequent deliveries
                    delivery_chance = 0.4 if store['store_type'] == 'online' else 0.2
                    if rng.random() < delivery_chance:
                        if store['store_type'] == 'online':
                            delivered = rng.integers(200, 500)  # Larger deliveries for online
                        else:
                            delivered = rng.integers(50, 200)
                        current_inventory[inv_key] += delivered
                        on_hand = current_inventory[inv_key]

                        # Create supplier shipment record
                        supplier_shipments_list.append({
                            'shipment_id': shipment_id,
                            'shipment_date': (date - timedelta(days=int(rng.integers(1, 3)))).date(),
                            'delivery_date': date_str,
                            'store_id': store_id,
                            'sku': sku,
                            'quantity_shipped': delivered,
                            'quantity_received': delivered,
                            'supplier_name': product['brand'] + ' Supplier',
                            'po_number': f'PO-{shipment_id:06d}',
                            'shipment_status': 'delivered'
                        })
                        shipment_id += 1

                    # DC allocated quantity (looks large but not shipped)
                    dc_allocated = on_order if rng.random() < 0.3 else 0

                    # Calculate actual sales (constrained by inventory)
                    units_sold = min(demand, on_hand)
                    lost_sales = max(0, demand - units_sold)

                    # Update inventory
                    current_inventory[inv_key] = max(0, on_hand - units_sold)

                    # System inventory lag (24-48h)
                    if rng.random() < 0.92:  # 92% of time it's accurate
                        system_inventory[inv_key] = current_inventory[inv_key]
                    else:
                        # Stale or incorrect
                        system_inventory[inv_key] = int(on_hand * rng.uniform(0.5, 1.5))

                    # Calculate financials
                    regular_price = product['list_price']

                    # Apply promotion discount
                    if not active_promos.empty:
                        promo = active_promos.iloc[0]
                        discount_pct = promo['discount_pct']
                        net_price = regular_price * (1 - discount_pct / 100)
                        promo_id = promo['promo_id']
                        promo_funding = promo['supplier_funding_usd'] * units_sold / 100 if units_sold > 0 else 0
                    else:
                        discount_pct = 0
                        net_price = regular_price
                        promo_id = None
                        promo_funding = 0

                    gross_revenue = units_sold * net_price
                    revenue = gross_revenue

                    # Calculate ambiguous COGS columns
                    # cogs_c: Standard COGS calculation (average cost method)
                    # This uses the standard product cost
                    cogs_c = units_sold * product['cost']

                    # cogs_s: COGS with shrinkage adjustments (includes theft/damage/spoilage)
                    # Add 2-5% for shrinkage based on category and store type
                    shrinkage_rate = 0.02  # Base shrinkage rate
                    if product['category'] in ['produce', 'dairy', 'bakery', 'meat']:
                        shrinkage_rate += 0.02  # Higher shrinkage for perishables
                    if store['store_type'] == 'urban':
                        shrinkage_rate += 0.01  # Higher shrinkage in urban stores

                    # Apply shrinkage adjustment to COGS
                    cogs_s = cogs_c * (1 + shrinkage_rate)

                    # During high-theft periods (holidays), increase shrinkage
                    cal_row = self.calendar[self.calendar['date'] == date.date()]
                    if not cal_row.empty:
                        if cal_row.iloc[0]['is_holiday_us'] or cal_row.iloc[0].get('event_name_us'):
                            cogs_s *= 1.03  # Additional 3% during high-traffic periods

                    # Additional financial components
                    supplier_rebate = revenue * 0.02 if rng.random() < 0.3 else 0
                    spoilage_cost = cogs_c * 0.01 if product['category'] in ['dairy', 'produce', 'meat'] else 0

                    # Gross margin calculation (using standard COGS for margin calculation)
                    if revenue > 0:
                        gross_margin_pct = ((revenue - cogs_c) / revenue) * 100
                    else:
                        gross_margin_pct = 0

                    # Posting date (7 days after sales date for Monday posting)
                    days_until_monday = (7 - date.dayofweek) % 7
                    if days_until_monday == 0:
                        days_until_monday = 7
                    posting_date = date + timedelta(days=days_until_monday)

                    # Stock hours calculation
                    if store['store_type'] == 'online':
                        open_hours = 24  # Online is 24/7
                    elif store['store_type'] == 'convenience':
                        open_hours = 16
                    else:
                        open_hours = 12

                    if on_hand > 0:
                        in_stock_hours = open_hours * min(1, on_hand / max(1, demand))
                    else:
                        in_stock_hours = 0

                    # Available to promise
                    quarantine = 0
                    # Check for recall
                    for _, event in self.ground_truth_events.iterrows():
                        if (event['label'] == 'recall' and
                            event['sku'] == sku and
                            pd.to_datetime(event['start_date']) <= date <= pd.to_datetime(event['end_date'])):
                            quarantine = on_hand

                    available_to_promise = max(0, on_hand + in_transit - quarantine)

                    # Add sales record
                    sales_list.append({
                        'date': date_str,
                        'store_id': store_id,
                        'sku': sku,
                        'units_sold': units_sold,
                        'gross_revenue': round(gross_revenue, 2),
                        'promo_id': promo_id,
                        'regular_price': round(regular_price, 2),
                        'net_price': round(net_price, 2),
                        'revenue': round(revenue, 2),
                        'supplier_rebate_amt': round(supplier_rebate, 2),
                        'spoilage_cost': round(spoilage_cost, 2),
                        'promo_funding_received': round(promo_funding, 2),
                        'gross_margin_pct': round(gross_margin_pct, 2),
                        'discount_pct': discount_pct,
                        'cogs_c': round(cogs_c, 2),  # Standard COGS
                        'cogs_s': round(cogs_s, 2),  # COGS with shrinkage
                        'sales_date': date_str,
                        'posting_date': posting_date.date()
                    })

                    # Add inventory record
                    inventory_list.append({
                        'date': date_str,
                        'store_id': store_id,
                        'sku': sku,
                        'on_hand': current_inventory[inv_key],
                        'on_order': on_order,
                        'in_transit': in_transit,
                        'safety_stock': safety_stock,
                        'last_scan_ts': date,
                        'system_on_hand': system_inventory[inv_key],
                        'available_to_promise': available_to_promise,
                        'open_hours': open_hours,
                        'in_stock_hours': round(in_stock_hours, 2),
                        'dc_allocated_qty': dc_allocated,
                        'quarantine_hold': quarantine
                    })

                    # Generate waste/spoilage for perishable items
                    if product['category'] in ['dairy', 'produce', 'meat', 'bakery']:
                        if rng.random() < 0.02:  # 2% chance of waste
                            waste_qty = rng.integers(1, 5)
                            waste_reason = rng.choice(['expired', 'damaged', 'temperature', 'quality'])

                            waste_spoilage_list.append({
                                'waste_id': waste_id,
                                'date': date_str,
                                'store_id': store_id,
                                'sku': sku,
                                'quantity_wasted': waste_qty,
                                'waste_reason': waste_reason,
                                'waste_value': round(waste_qty * product['cost'], 2),
                                'recorded_by': f'emp_{rng.integers(100, 999)}'
                            })
                            waste_id += 1

                            # Reduce inventory for waste
                            current_inventory[inv_key] = max(0, current_inventory[inv_key] - waste_qty)

                    # Generate returns (1% of sales)
                    if units_sold > 0 and rng.random() < 0.01:
                        return_qty = min(units_sold, rng.integers(1, 3))
                        return_reason = rng.choice(['defective', 'wrong_item', 'not_as_described', 'damaged'])

                        returns_list.append({
                            'date': date_str,
                            'store_id': store_id,
                            'sku': sku,
                            'units_returned': return_qty,
                            'reason_code': return_reason,
                            'refund_value': round(return_qty * net_price, 2)
                        })

                        # Add returned items back to inventory
                        if return_reason != 'defective' and return_reason != 'damaged':
                            current_inventory[inv_key] += return_qty

                    # Generate customer feedback (0.5% chance)
                    if units_sold > 0 and rng.random() < 0.005:
                        sentiment = rng.choice([0.1, 0.3, 0.5, 0.7, 0.9], p=[0.05, 0.10, 0.20, 0.35, 0.30])
                        channel = rng.choice(['online', 'in-store', 'phone', 'email'])

                        # Generate feedback text based on sentiment
                        if sentiment < 0.4:
                            text = rng.choice([
                                'Product was out of stock',
                                'Poor quality, not as expected',
                                'Price too high compared to competitors'
                            ])
                        elif sentiment < 0.6:
                            text = 'Average product, nothing special'
                        else:
                            text = rng.choice([
                                'Great product, highly recommend!',
                                'Excellent quality and value',
                                'Very satisfied with purchase'
                            ])

                        feedback_list.append({
                            'feedback_id': feedback_id,
                            'date': date_str,
                            'store_id': store_id,
                            'sku': sku,
                            'channel': channel,
                            'text': text,
                            'sentiment_score': sentiment
                        })
                        feedback_id += 1

                    # Generate price changes (0.2% chance)
                    if rng.random() < 0.002:
                        change_reason = rng.choice(['competitor_match', 'clearance', 'cost_increase', 'promotion_end'])
                        price_multiplier = rng.choice([0.85, 0.90, 0.95, 1.05, 1.10])

                        price_changes_list.append({
                            'change_id': change_id,
                            'date': date_str,
                            'store_id': store_id,
                            'sku': sku,
                            'new_regular_price': round(regular_price * price_multiplier, 2),
                            'reason': change_reason
                        })
                        change_id += 1

                    # Generate support tickets (0.1% chance for stockouts)
                    if on_hand == 0 and demand > 0 and rng.random() < 0.1:
                        created_at = f"{date_str} {rng.integers(8, 18):02d}:{rng.integers(0, 60):02d}:00"
                        resolved = rng.random() < 0.7  # 70% resolved
                        resolved_at = None
                        if resolved:
                            # Resolved within 1-48 hours
                            hours_to_resolve = int(rng.integers(1, 49))
                            resolved_date = date + timedelta(hours=hours_to_resolve)
                            resolved_at = f"{resolved_date.date()} {resolved_date.hour:02d}:00:00"

                        tickets_list.append({
                            'ticket_id': ticket_id,
                            'created_at': created_at,
                            'resolved_at': resolved_at,
                            'store_id': store_id,
                            'sku': sku,
                            'issue_type': 'stockout',
                            'description': f'Out of stock for {sku}, demand was {demand} units',
                            'root_cause': rng.choice(['supplier_delay', 'forecast_error', 'unexpected_demand']) if resolved else None,
                            'resolved': resolved
                        })
                        ticket_id += 1

                    # Update order counts
                    if units_sold > 0:
                        daily_orders[store_id]['orders_count'] += units_sold
                        daily_orders[store_id]['fulfilled_orders'] += units_sold
                    if lost_sales > 0:
                        daily_orders[store_id]['orders_count'] += lost_sales

                # Add daily orders record
                orders_list.append({
                    'date': date_str,
                    'store_id': store_id,
                    'orders_count': daily_orders[store_id]['orders_count'],
                    'fulfilled_orders': daily_orders[store_id]['fulfilled_orders']
                })

        # Convert to DataFrames
        sales_df = pd.DataFrame(sales_list)
        inventory_df = pd.DataFrame(inventory_list)
        returns_df = pd.DataFrame(returns_list)
        orders_df = pd.DataFrame(orders_list)
        supplier_shipments_df = pd.DataFrame(supplier_shipments_list)
        waste_spoilage_df = pd.DataFrame(waste_spoilage_list)
        tickets_df = pd.DataFrame(tickets_list)
        feedback_df = pd.DataFrame(feedback_list)
        price_changes_df = pd.DataFrame(price_changes_list)

        return (sales_df, inventory_df, returns_df, orders_df,
                supplier_shipments_df, waste_spoilage_df, tickets_df, feedback_df, price_changes_df)

    def save_data(self, output_dir: str = OUTPUT_DIR):
        """Save all generated data to CSV files."""
        os.makedirs(output_dir, exist_ok=True)

        # Generate all data
        print("Generating products...")
        self.generate_products()

        print("Generating stores...")
        self.generate_stores()

        # print("Generating calendar...")
        # self.generate_calendar()

        # print("Generating ground truth events...")
        # self.generate_ground_truth_events()

        print("Generating promotions...")
        self.generate_promotions()

        print("Generating assortment...")
        self.generate_assortment()

        print("Generating daily transactional data...")
        (sales_df, inventory_df, returns_df, orders_df,
         supplier_shipments_df, waste_spoilage_df, tickets_df, feedback_df, price_changes_df) = self.generate_daily_data()

        # Save to CSV
        print("Saving data files...")
        self.products[['product_id', 'sku', 'brand', 'category', 'sub_category',
                      'size', 'unit_of_measure', 'list_price', 'cost',
                      'launch_date', 'discontinue_date']].to_csv(
            os.path.join(output_dir, 'products.csv'), index=False)

        self.stores[['store_id', 'region', 'store_type', 'sq_ft',
                    'opened_date', 'climate_zone', 'city', 'latitude', 'longitude']].to_csv(
            os.path.join(output_dir, 'stores.csv'), index=False)

        # self.calendar.to_csv(os.path.join(output_dir, 'calendar.csv'), index=False)

        self.promotions.to_csv(os.path.join(output_dir, 'promotions.csv'), index=False)

        self.assortment.to_csv(os.path.join(output_dir, 'assortment.csv'), index=False)

        # Fix integer columns with NaN values before export
        if 'promo_id' in sales_df.columns:
            sales_df['promo_id'] = sales_df['promo_id'].fillna(0).astype('Int64')
        sales_df.to_csv(os.path.join(output_dir, 'sales_daily.csv'), index=False, na_rep='')

        inventory_df.to_csv(os.path.join(output_dir, 'inventory_daily.csv'), index=False)

        # Always write these files (they should have some data now)
        returns_df.to_csv(os.path.join(output_dir, 'returns_daily.csv'), index=False)

        orders_df.to_csv(os.path.join(output_dir, 'orders_daily.csv'), index=False)

        if not supplier_shipments_df.empty:
            supplier_shipments_df.to_csv(os.path.join(output_dir, 'supplier_shipments.csv'), index=False)

        if not waste_spoilage_df.empty:
            waste_spoilage_df.to_csv(os.path.join(output_dir, 'waste_spoilage.csv'), index=False)

        # Always write these files (they should have some data now)
        tickets_df.to_csv(os.path.join(output_dir, 'tickets.csv'), index=False)
        feedback_df.to_csv(os.path.join(output_dir, 'customer_feedback.csv'), index=False)
        price_changes_df.to_csv(os.path.join(output_dir, 'price_changes.csv'), index=False)

        # self.ground_truth_events.to_csv(os.path.join(output_dir, 'ground_truth_events.csv'), index=False)

        # Print summary statistics
        print("\nDataset Summary:")
        print(f"  Products: {len(self.products)}")
        print(f"  Stores: {len(self.stores)}")
        print(f"  Days: {NUM_DAYS}")
        print(f"  Total sales records: {len(sales_df)}")
        print(f"  Total inventory records: {len(inventory_df)}")
        print(f"  Total promotions: {len(self.promotions)}")


# Main execution
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Generate ShelfWise synthetic dataset')
    parser.add_argument('--output', '-o', default=None, help='Output directory for CSV files')
    parser.add_argument('--seed', '-s', type=int, default=42, help='Random seed for reproducibility')

    args = parser.parse_args()

    # Set seed
    np.random.seed(args.seed)
    rng = np.random.default_rng(args.seed)

    # Generate data
    generator = ShelfWiseDataGenerator()
    output_dir = args.output if args.output else OUTPUT_DIR
    generator.save_data(output_dir)