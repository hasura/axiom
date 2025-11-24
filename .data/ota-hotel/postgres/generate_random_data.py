# This script is useful for generating random data for tables 
# like marketing.traffic_sources, user_data.search_queries_hotel_bookings, marketing.marketing_spends, 
# user_data.users and user_data.hotel_bookings

import csv
import random
import hashlib
from datetime import datetime, timedelta
from pathlib import Path

# Create output directory
OUTPUT_DIR = Path("random_seed_data")
OUTPUT_DIR.mkdir(exist_ok=True)

# ============================================
# HELPER FUNCTIONS
# ============================================

def generate_random_date(start_date, end_date):
    """Generate a random date between start_date and end_date"""
    time_between = end_date - start_date
    days_between = time_between.days
    random_days = random.randrange(days_between)
    return start_date + timedelta(days=random_days)

def generate_random_datetime(start_date, end_date):
    """Generate a random datetime between start_date and end_date"""
    time_between = end_date - start_date
    seconds_between = time_between.total_seconds()
    random_seconds = random.randrange(int(seconds_between))
    return start_date + timedelta(seconds=random_seconds)

def write_csv(filename, headers, data):
    """Write data to CSV file"""
    filepath = OUTPUT_DIR / filename
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)
    print(f"✓ Generated {filepath} with {len(data)} records")

# ============================================
# RANDOM DATA GENERATION FUNCTIONS
# ============================================

def generate_users(count=1000):
    """
    Generate random user data
    
    Args:
        count: Number of users to generate (default: 1000)
    
    Returns:
        List of user dictionaries
    """
    print(f"🎲 Generating {count} random users...")
    users = []
    user_types = ['regular', 'premium', 'corporate']
    
    start_date = datetime(2020, 1, 1)
    end_date = datetime(2024, 10, 31)
    
    for i in range(1, count + 1):
        registration_date = generate_random_date(start_date, end_date)
        
        users.append({
            'email': f'user{i}@example.com',
            'phone': f'+91{random.randint(7000000000, 9999999999)}',
            'registration_date': registration_date.strftime('%Y-%m-%d'),
            'user_type': random.choices(user_types, weights=[70, 20, 10])[0]
        })
    
    headers = ['email', 'phone', 'registration_date', 'user_type']
    write_csv('users.csv', headers, users)
    return users

def generate_search_queries_hotel_bookings(count=15000, user_count=1000):
    """
    Generate random search queries
    
    Args:
        count: Number of search queries to generate (default: 15000)
        user_count: Number of users in the system (default: 1000)
    
    Returns:
        List of search query dictionaries
    """
    print(f"🎲 Generating {count} random search queries...")
    queries = []
    
    destinations = [
        'Mumbai', 'Delhi', 'Bangalore', 'Goa', 'Jaipur', 'Kolkata', 'Chennai',
        'Hyderabad', 'Pune', 'Ahmedabad', 'Udaipur', 'Shimla', 'Manali',
        'Agra', 'Varanasi', 'Rishikesh', 'Mysore', 'Kochi', 'Amritsar', 'Darjeeling'
    ]
    
    start_date = datetime(2024, 6, 1)
    end_date = datetime(2024, 11, 30, 23, 59, 59)
    
    for i in range(1, count + 1):
        search_date = generate_random_datetime(start_date, end_date)
        check_in = search_date.date() + timedelta(days=random.randint(1, 60))
        check_out = check_in + timedelta(days=random.randint(2, 12))
        
        queries.append({
            'user_id': random.randint(1, user_count),
            'session_id': f'session_{hashlib.md5(str(random.random()).encode()).hexdigest()}',
            'destination': random.choice(destinations),
            'search_date': search_date.strftime('%Y-%m-%d %H:%M:%S'),
            'check_in_date': check_in.strftime('%Y-%m-%d'),
            'check_out_date': check_out.strftime('%Y-%m-%d'),
            'number_of_guests': random.randint(1, 6)
        })
    
    headers = ['user_id', 'session_id', 'destination', 'search_date', 'check_in_date', 'check_out_date', 'number_of_guests']
    write_csv('search_queries_hotel_bookings.csv', headers, queries)
    return queries

def generate_traffic_sources(search_queries_hotel_bookings, campaign_count=12):
    """
    Generate random traffic sources based on search queries
    
    Args:
        search_queries_hotel_bookings: List of search query dictionaries
        campaign_count: Number of campaigns in the system (default: 12)
    
    Returns:
        List of traffic source dictionaries
    """
    print(f"🎲 Generating {len(search_queries_hotel_bookings)} traffic source records...")
    traffic = []
    
    sources = ['organic', 'paid_ads', 'email', 'social_media', 'direct', 'referral', 'affiliate']
    source_weights = [30, 25, 15, 15, 10, 3, 2]  # Percentage distribution
    
    for query in search_queries_hotel_bookings:
        source = random.choices(sources, weights=source_weights)[0]
        
        # 40% chance of having a campaign_id (only for paid sources)
        campaign_id = None
        if source in ['paid_ads', 'email', 'social_media', 'affiliate'] and random.random() < 0.4:
            campaign_id = random.randint(1, campaign_count)
        
        # Generate referrer URL based on source
        referrer_url = None
        if source == 'organic':
            if random.random() < 0.7:
                referrer_url = f'https://google.com/search?q=hotels+{query["destination"]}'
            elif random.random() < 0.85:
                referrer_url = f'https://bing.com/search?q=best+hotels+{query["destination"]}'
        elif source == 'social_media':
            platforms = ['facebook.com/mmt', 'instagram.com/makemytrip', 'twitter.com/makemytrip']
            referrer_url = f'https://{random.choice(platforms)}'
        elif source == 'referral':
            referrers = ['tripadvisor.com', 'booking.com', 'expedia.com', 'travelblog.com']
            referrer_url = f'https://{random.choice(referrers)}'
        
        traffic.append({
            'user_id': query['user_id'],
            'session_id': query['session_id'],
            'source': source,
            'campaign_id': campaign_id if campaign_id else '',
            'visit_date': query['search_date'],
            'referrer_url': referrer_url if referrer_url else ''
        })
    
    headers = ['user_id', 'session_id', 'source', 'campaign_id', 'visit_date', 'referrer_url']
    write_csv('traffic_sources.csv', headers, traffic)
    return traffic

def generate_marketing_spends(campaign_count=12, start_date_str='2024-06-01', end_date_str='2024-11-30'):
    """
    Generate random marketing spend data for campaigns
    
    Args:
        campaign_count: Number of campaigns (default: 12)
        start_date_str: Start date for spend data (default: '2024-06-01')
        end_date_str: End date for spend data (default: '2024-11-30')
    
    Returns:
        List of marketing spend dictionaries
    """
    print(f"🎲 Generating marketing spend data for {campaign_count} campaigns...")
    spends = []
    
    # Campaign configurations (campaign_id: campaign_type)
    campaign_types = {
        1: 'email',
        2: 'search_ads',
        3: 'social_media',
        4: 'email',
        5: 'search_ads',
        6: 'social_media',
        7: 'affiliate',
        8: 'email',
        9: 'display_ads',
        10: 'email',
        11: 'search_ads',
        12: 'display_ads'
    }
    
    # Spend ranges by campaign type
    spend_ranges = {
        'search_ads': (50000, 150000),
        'display_ads': (30000, 100000),
        'social_media': (25000, 75000),
        'email': (10000, 30000),
        'affiliate': (40000, 100000)
    }
    
    impression_ranges = {
        'search_ads': (500000, 1000000),
        'display_ads': (800000, 1500000),
        'social_media': (1000000, 2000000),
        'email': (100000, 300000),
        'affiliate': (300000, 700000)
    }
    
    click_ranges = {
        'search_ads': (5000, 15000),
        'display_ads': (3000, 10000),
        'social_media': (8000, 20000),
        'email': (2000, 7000),
        'affiliate': (4000, 10000)
    }
    
    conversion_ranges = {
        'search_ads': (150, 500),
        'display_ads': (100, 400),
        'social_media': (200, 600),
        'email': (100, 350),
        'affiliate': (120, 450)
    }
    
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
    
    for campaign_id in range(1, campaign_count + 1):
        campaign_type = campaign_types.get(campaign_id, 'email')
        
        current = start_date
        
        while current <= end_date:
            spend_min, spend_max = spend_ranges.get(campaign_type, (20000, 50000))
            imp_min, imp_max = impression_ranges.get(campaign_type, (300000, 700000))
            click_min, click_max = click_ranges.get(campaign_type, (4000, 10000))
            conv_min, conv_max = conversion_ranges.get(campaign_type, (100, 400))
            
            # Add day-of-week variation (weekends typically perform differently)
            day_multiplier = 0.8 if current.weekday() in [5, 6] else 1.0
            
            spends.append({
                'campaign_id': campaign_id,
                'date': current.strftime('%Y-%m-%d'),
                'spend': round(random.uniform(spend_min, spend_max) * day_multiplier, 2),
                'impressions': int(random.randint(imp_min, imp_max) * day_multiplier),
                'clicks': int(random.randint(click_min, click_max) * day_multiplier),
                'conversions': int(random.randint(conv_min, conv_max) * day_multiplier)
            })
            
            current += timedelta(days=1)
    
    headers = ['campaign_id', 'date', 'spend', 'impressions', 'clicks', 'conversions']
    write_csv('marketing_spends.csv', headers, spends)
    return spends

def generate_hotel_bookings(search_queries_hotel_bookings, count=8000):
    """
    Generate random hotel bookings based on search queries
    
    Args:
        search_queries_hotel_bookings: List of search query dictionaries
        count: Number of bookings to generate (default: 8000)
    
    Returns:
        List of hotel booking dictionaries
    """
    print(f"🎲 Generating {count} random hotel bookings...")
    bookings = []
    
    # Mapping of cities to hotel IDs
    city_to_hotels = {
        'Mumbai': list(range(1, 6)),
        'Delhi': list(range(6, 11)),
        'Bangalore': list(range(11, 16)),
        'Goa': list(range(16, 21)),
        'Jaipur': list(range(21, 26)),
        'Kolkata': list(range(26, 31)),
        'Chennai': list(range(31, 36)),
        'Hyderabad': list(range(36, 41)),
        'Pune': list(range(41, 46)),
        'Ahmedabad': list(range(46, 51)),
        'Udaipur': list(range(51, 56)),
        'Shimla': list(range(56, 61)),
        'Manali': list(range(61, 66)),
        'Agra': list(range(66, 71)),
        'Varanasi': list(range(71, 76)),
        'Rishikesh': list(range(76, 81)),
        'Mysore': list(range(81, 86)),
        'Kochi': list(range(86, 91)),
        'Amritsar': list(range(91, 96)),
        'Darjeeling': list(range(96, 101)),
    }
    
    # Base prices by hotel tier (for calculation)
    base_prices = {
        range(1, 101): {  # All hotels
            'budget': (2000, 3000),
            'mid': (5000, 8000),
            'luxury': (15000, 25000),
            'premium': (30000, 50000)
        }
    }
    
    booking_statuses = ['confirmed', 'completed', 'cancelled', 'no_show']
    status_weights = [85, 8, 5, 2]  # Percentage distribution
    
    # Sample queries for conversion (approximately 5% conversion rate)
    sampled_queries = random.sample(search_queries_hotel_bookings, min(count, len(search_queries_hotel_bookings)))
    
    for query in sampled_queries[:count]:
        destination = query['destination']
        hotel_ids = city_to_hotels.get(destination, [1])
        
        if not hotel_ids:
            continue
        
        hotel_id = random.choice(hotel_ids)
        
        # Assign room_id based on hotel_id (simplified - 3-4 rooms per hotel)
        room_id = ((hotel_id - 1) * 4) + random.randint(1, 4)
        
        # Calculate booking date (within 48 hours of search)
        search_dt = datetime.strptime(query['search_date'], '%Y-%m-%d %H:%M:%S')
        booking_date = search_dt + timedelta(hours=random.uniform(1, 48))
        
        # Calculate stay duration
        check_in = datetime.strptime(query['check_in_date'], '%Y-%m-%d')
        check_out = datetime.strptime(query['check_out_date'], '%Y-%m-%d')
        num_nights = (check_out - check_in).days
        
        # Determine hotel tier based on hotel_id
        if hotel_id % 5 in [1, 2]:  # First two hotels in each city are luxury
            tier = 'luxury' if hotel_id % 5 == 1 else 'premium'
        elif hotel_id % 5 == 3:
            tier = 'mid'
        else:
            tier = 'budget'
        
        # Calculate amount based on tier and duration
        price_min, price_max = base_prices[range(1, 101)][tier]
        base_price_per_night = random.uniform(price_min, price_max)
        
        # Apply seasonal multiplier
        month = check_in.month
        if month in [10, 11, 12]:  # Festival season
            seasonal_multiplier = random.uniform(1.3, 1.6)
        elif month in [4, 5, 6]:  # Summer
            seasonal_multiplier = random.uniform(1.1, 1.3)
        elif month in [7, 8]:  # Monsoon discount
            seasonal_multiplier = random.uniform(0.7, 0.9)
        else:
            seasonal_multiplier = random.uniform(1.0, 1.2)
        
        amount_paid = round(base_price_per_night * num_nights * seasonal_multiplier, 2)
        
        bookings.append({
            'user_id': query['user_id'],
            'hotel_id': hotel_id,
            'room_id': room_id,
            'booking_date': booking_date.strftime('%Y-%m-%d %H:%M:%S'),
            'check_in_date': query['check_in_date'],
            'check_out_date': query['check_out_date'],
            'destination': destination,
            'amount_paid': amount_paid,
            'booking_status': random.choices(booking_statuses, weights=status_weights)[0],
            'number_of_guests': query['number_of_guests']
        })
    
    headers = ['user_id', 'hotel_id', 'room_id', 'booking_date', 'check_in_date', 'check_out_date', 'destination', 'amount_paid', 'booking_status', 'number_of_guests']
    write_csv('hotel_bookings.csv', headers, bookings)
    return bookings

# ============================================
# MAIN EXECUTION
# ============================================

def generate_all_random_data(
    user_count=1000,
    search_count=15000,
    booking_count=8000,
    campaign_count=12
):
    """
    Generate all random data tables
    
    Args:
        user_count: Number of users to generate
        search_count: Number of search queries to generate
        booking_count: Number of bookings to generate
        campaign_count: Number of campaigns for marketing spends
    """
    print("=" * 70)
    print("Starting Random Data Generation for MMT Hotel Booking System")
    print("=" * 70)
    print()
    
    # Step 1: Generate users
    print("👥 Step 1/5: Generating Users")
    users = generate_users(count=user_count)
    print()
    
    # Step 2: Generate search queries
    print("🔍 Step 2/5: Generating Search Queries")
    search_queries_hotel_bookings = generate_search_queries_hotel_bookings(count=search_count, user_count=user_count)
    print()
    
    # Step 3: Generate traffic sources
    print("🌐 Step 3/5: Generating Traffic Sources")
    traffic_sources = generate_traffic_sources(search_queries_hotel_bookings, campaign_count=campaign_count)
    print()
    
    # Step 4: Generate marketing spends
    print("💰 Step 4/5: Generating Marketing Spends")
    marketing_spends = generate_marketing_spends(campaign_count=campaign_count)
    print()
    
    # Step 5: Generate hotel bookings
    print("🏨 Step 5/5: Generating Hotel Bookings")
    hotel_bookings = generate_hotel_bookings(search_queries_hotel_bookings, count=booking_count)
    print()
    
    # Summary
    print("=" * 70)
    print("✅ Random Data Generation Complete!")
    print("=" * 70)
    print(f"📁 Output directory: {OUTPUT_DIR.absolute()}")
    print()
    print("📊 Summary:")
    print(f"   - Users: {len(users)} records")
    print(f"   - Search Queries: {len(search_queries_hotel_bookings)} records")
    print(f"   - Traffic Sources: {len(traffic_sources)} records")
    print(f"   - Marketing Spends: {len(marketing_spends)} records")
    print(f"   - Hotel Bookings: {len(hotel_bookings)} records")
    print()
    print("🎉 All random CSV files are ready for import!")
    print()
    print("💡 Import to PostgreSQL using:")
    print("   \\COPY user_data.users FROM 'random_seed_data/users.csv' CSV HEADER")
    print("   \\COPY user_data.search_queries_hotel_bookings FROM 'random_seed_data/search_queries_hotel_bookings.csv' CSV HEADER")
    print("   \\COPY marketing.traffic_sources FROM 'random_seed_data/traffic_sources.csv' CSV HEADER")
    print("   \\COPY marketing.marketing_spends FROM 'random_seed_data/marketing_spends.csv' CSV HEADER")
    print("   \\COPY user_data.hotel_bookings FROM 'random_seed_data/hotel_bookings.csv' CSV HEADER")

def main():
    """Main entry point with customizable parameters"""
    
    # Customize these parameters as needed
    USER_COUNT = 1000
    SEARCH_COUNT = 15000
    BOOKING_COUNT = 8000
    CAMPAIGN_COUNT = 12
    
    generate_all_random_data(
        user_count=USER_COUNT,
        search_count=SEARCH_COUNT,
        booking_count=BOOKING_COUNT,
        campaign_count=CAMPAIGN_COUNT
    )

if __name__ == "__main__":
    main()