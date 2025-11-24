import csv
import random
import hashlib
from datetime import datetime, timedelta
from pathlib import Path

# Create output directory
OUTPUT_DIR = Path("seed_data_csv")
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
# STATIC DATA GENERATION (Non-random)
# ============================================

def generate_cities():
    """Generate cities data - static list"""
    cities = [
        {'city_name': 'Mumbai', 'state': 'Maharashtra', 'country': 'India', 'timezone': 'Asia/Kolkata'},
        {'city_name': 'Delhi', 'state': 'Delhi', 'country': 'India', 'timezone': 'Asia/Kolkata'},
        {'city_name': 'Bangalore', 'state': 'Karnataka', 'country': 'India', 'timezone': 'Asia/Kolkata'},
        {'city_name': 'Goa', 'state': 'Goa', 'country': 'India', 'timezone': 'Asia/Kolkata'},
        {'city_name': 'Jaipur', 'state': 'Rajasthan', 'country': 'India', 'timezone': 'Asia/Kolkata'},
        {'city_name': 'Kolkata', 'state': 'West Bengal', 'country': 'India', 'timezone': 'Asia/Kolkata'},
        {'city_name': 'Chennai', 'state': 'Tamil Nadu', 'country': 'India', 'timezone': 'Asia/Kolkata'},
        {'city_name': 'Hyderabad', 'state': 'Telangana', 'country': 'India', 'timezone': 'Asia/Kolkata'},
        {'city_name': 'Pune', 'state': 'Maharashtra', 'country': 'India', 'timezone': 'Asia/Kolkata'},
        {'city_name': 'Ahmedabad', 'state': 'Gujarat', 'country': 'India', 'timezone': 'Asia/Kolkata'},
        {'city_name': 'Udaipur', 'state': 'Rajasthan', 'country': 'India', 'timezone': 'Asia/Kolkata'},
        {'city_name': 'Shimla', 'state': 'Himachal Pradesh', 'country': 'India', 'timezone': 'Asia/Kolkata'},
        {'city_name': 'Manali', 'state': 'Himachal Pradesh', 'country': 'India', 'timezone': 'Asia/Kolkata'},
        {'city_name': 'Agra', 'state': 'Uttar Pradesh', 'country': 'India', 'timezone': 'Asia/Kolkata'},
        {'city_name': 'Varanasi', 'state': 'Uttar Pradesh', 'country': 'India', 'timezone': 'Asia/Kolkata'},
        {'city_name': 'Rishikesh', 'state': 'Uttarakhand', 'country': 'India', 'timezone': 'Asia/Kolkata'},
        {'city_name': 'Mysore', 'state': 'Karnataka', 'country': 'India', 'timezone': 'Asia/Kolkata'},
        {'city_name': 'Kochi', 'state': 'Kerala', 'country': 'India', 'timezone': 'Asia/Kolkata'},
        {'city_name': 'Amritsar', 'state': 'Punjab', 'country': 'India', 'timezone': 'Asia/Kolkata'},
        {'city_name': 'Darjeeling', 'state': 'West Bengal', 'country': 'India', 'timezone': 'Asia/Kolkata'},
    ]
    
    headers = ['city_name', 'state', 'country', 'timezone']
    write_csv('cities.csv', headers, cities)
    return cities

def generate_festivals():
    """Generate festivals data - static list"""
    festivals = [
        {'city_id': 1, 'festival_name': 'Ganesh Chaturthi', 'start_date': '2024-09-07', 'end_date': '2024-09-17', 'festival_type': 'religious', 'significance_level': 'national', 'expected_tourist_influx': 500000},
        {'city_id': 2, 'festival_name': 'Diwali', 'start_date': '2024-11-01', 'end_date': '2024-11-05', 'festival_type': 'religious', 'significance_level': 'national', 'expected_tourist_influx': 800000},
        {'city_id': 3, 'festival_name': 'Diwali', 'start_date': '2024-11-01', 'end_date': '2024-11-05', 'festival_type': 'religious', 'significance_level': 'national', 'expected_tourist_influx': 600000},
        {'city_id': 4, 'festival_name': 'Goa Carnival', 'start_date': '2024-02-10', 'end_date': '2024-02-13', 'festival_type': 'cultural', 'significance_level': 'international', 'expected_tourist_influx': 300000},
        {'city_id': 4, 'festival_name': 'New Year Celebration', 'start_date': '2024-12-31', 'end_date': '2025-01-01', 'festival_type': 'cultural', 'significance_level': 'international', 'expected_tourist_influx': 400000},
        {'city_id': 5, 'festival_name': 'Jaipur Literature Festival', 'start_date': '2024-01-25', 'end_date': '2024-01-29', 'festival_type': 'cultural', 'significance_level': 'international', 'expected_tourist_influx': 250000},
        {'city_id': 5, 'festival_name': 'Diwali', 'start_date': '2024-11-01', 'end_date': '2024-11-05', 'festival_type': 'religious', 'significance_level': 'national', 'expected_tourist_influx': 400000},
        {'city_id': 6, 'festival_name': 'Durga Puja', 'start_date': '2024-10-10', 'end_date': '2024-10-14', 'festival_type': 'religious', 'significance_level': 'national', 'expected_tourist_influx': 700000},
        {'city_id': 7, 'festival_name': 'Pongal', 'start_date': '2025-01-14', 'end_date': '2025-01-17', 'festival_type': 'religious', 'significance_level': 'regional', 'expected_tourist_influx': 300000},
        {'city_id': 8, 'festival_name': 'Bonalu Festival', 'start_date': '2024-07-16', 'end_date': '2024-07-28', 'festival_type': 'religious', 'significance_level': 'regional', 'expected_tourist_influx': 200000},
        {'city_id': 9, 'festival_name': 'Ganesh Chaturthi', 'start_date': '2024-09-07', 'end_date': '2024-09-17', 'festival_type': 'religious', 'significance_level': 'national', 'expected_tourist_influx': 350000},
        {'city_id': 10, 'festival_name': 'Navratri', 'start_date': '2024-10-03', 'end_date': '2024-10-12', 'festival_type': 'religious', 'significance_level': 'regional', 'expected_tourist_influx': 450000},
        {'city_id': 11, 'festival_name': 'Mewar Festival', 'start_date': '2024-03-25', 'end_date': '2024-03-27', 'festival_type': 'cultural', 'significance_level': 'regional', 'expected_tourist_influx': 150000},
        {'city_id': 14, 'festival_name': 'Taj Mahotsav', 'start_date': '2024-02-18', 'end_date': '2024-02-27', 'festival_type': 'cultural', 'significance_level': 'international', 'expected_tourist_influx': 200000},
        {'city_id': 15, 'festival_name': 'Dev Deepawali', 'start_date': '2024-11-15', 'end_date': '2024-11-15', 'festival_type': 'religious', 'significance_level': 'national', 'expected_tourist_influx': 350000},
        {'city_id': 16, 'festival_name': 'International Yoga Festival', 'start_date': '2024-03-01', 'end_date': '2024-03-07', 'festival_type': 'cultural', 'significance_level': 'international', 'expected_tourist_influx': 180000},
        {'city_id': 18, 'festival_name': 'Kochi-Muziris Biennale', 'start_date': '2024-12-12', 'end_date': '2025-04-10', 'festival_type': 'cultural', 'significance_level': 'international', 'expected_tourist_influx': 250000},
        {'city_id': 19, 'festival_name': 'Baisakhi', 'start_date': '2024-04-13', 'end_date': '2024-04-14', 'festival_type': 'religious', 'significance_level': 'regional', 'expected_tourist_influx': 200000},
        {'city_id': 1, 'festival_name': 'Mumbai Film Festival', 'start_date': '2024-10-17', 'end_date': '2024-10-24', 'festival_type': 'cultural', 'significance_level': 'national', 'expected_tourist_influx': 100000},
        {'city_id': 3, 'festival_name': 'Bangalore Tech Summit', 'start_date': '2024-11-19', 'end_date': '2024-11-21', 'festival_type': 'other', 'significance_level': 'international', 'expected_tourist_influx': 150000},
    ]
    
    headers = ['city_id', 'festival_name', 'start_date', 'end_date', 'festival_type', 'significance_level', 'expected_tourist_influx']
    write_csv('festivals.csv', headers, festivals)
    return festivals

def generate_events():
    """Generate events data - static list"""
    events = [
        {'city_id': 1, 'event_name': 'Mumbai Marathon', 'event_date': '2024-01-21', 'event_type': 'sports', 'expected_attendance': 55000},
        {'city_id': 1, 'event_name': 'Tech Conference Mumbai', 'event_date': '2024-03-15', 'event_type': 'business', 'expected_attendance': 5000},
        {'city_id': 2, 'event_name': 'Delhi Auto Expo', 'event_date': '2024-01-12', 'event_type': 'business', 'expected_attendance': 600000},
        {'city_id': 2, 'event_name': 'India International Trade Fair', 'event_date': '2024-11-14', 'event_type': 'business', 'expected_attendance': 500000},
        {'city_id': 3, 'event_name': 'Bangalore Comics Con', 'event_date': '2024-02-17', 'event_type': 'entertainment', 'expected_attendance': 25000},
        {'city_id': 3, 'event_name': 'Aero India', 'event_date': '2024-02-20', 'event_type': 'business', 'expected_attendance': 100000},
        {'city_id': 4, 'event_name': 'Sunburn Festival', 'event_date': '2024-12-27', 'event_type': 'music', 'expected_attendance': 350000},
        {'city_id': 5, 'event_name': 'Jaipur Wedding Season Peak', 'event_date': '2024-12-01', 'event_type': 'other', 'expected_attendance': 100000},
        {'city_id': 6, 'event_name': 'Kolkata Book Fair', 'event_date': '2024-01-31', 'event_type': 'cultural', 'expected_attendance': 200000},
        {'city_id': 7, 'event_name': 'Chennai Music Season', 'event_date': '2024-12-15', 'event_type': 'music', 'expected_attendance': 150000},
        {'city_id': 8, 'event_name': 'Hyderabad Comic Con', 'event_date': '2024-08-10', 'event_type': 'entertainment', 'expected_attendance': 30000},
        {'city_id': 11, 'event_name': 'World Music Festival Udaipur', 'event_date': '2024-02-10', 'event_type': 'music', 'expected_attendance': 50000},
        {'city_id': 12, 'event_name': 'Shimla Summer Festival', 'event_date': '2024-06-01', 'event_type': 'cultural', 'expected_attendance': 75000},
        {'city_id': 13, 'event_name': 'Manali Winter Carnival', 'event_date': '2025-01-02', 'event_type': 'cultural', 'expected_attendance': 80000},
        {'city_id': 14, 'event_name': 'Agra Food Festival', 'event_date': '2024-11-20', 'event_type': 'food', 'expected_attendance': 40000},
        {'city_id': 18, 'event_name': 'Kochi Design Week', 'event_date': '2024-12-05', 'event_type': 'cultural', 'expected_attendance': 20000},
    ]
    
    headers = ['city_id', 'event_name', 'event_date', 'event_type', 'expected_attendance']
    write_csv('events.csv', headers, events)
    return events

def generate_external_factors():
    """Generate external factors - weather data for cities across date range"""
    data = []
    start_date = datetime(2024, 6, 1)
    end_date = datetime(2024, 11, 30)
    
    cities = list(range(1, 21))  # 20 cities
    current_date = start_date
    
    weather_conditions = {
        'winter': ['clear', 'partly_cloudy', 'foggy'],
        'summer': ['clear', 'hot', 'partly_cloudy'],
        'monsoon': ['rainy', 'cloudy', 'humid'],
        'autumn': ['clear', 'pleasant', 'partly_cloudy']
    }
    
    while current_date <= end_date:
        month = current_date.month
        
        # Determine season
        if month in [12, 1, 2]:
            season = 'winter'
        elif month in [3, 4, 5]:
            season = 'summer'
        elif month in [6, 7, 8]:
            season = 'monsoon'
        else:
            season = 'autumn'
        
        for city_id in cities:
            # Temperature varies by city type
            if city_id in [12, 13, 20]:  # Hill stations
                temp = round(10 + random.uniform(0, 15), 2)
            elif city_id in [1, 4, 7, 18]:  # Coastal cities
                temp = round(25 + random.uniform(0, 10), 2)
            else:  # Other cities
                temp = round(20 + random.uniform(0, 20), 2)
            
            data.append({
                'city_id': city_id,
                'date': current_date.strftime('%Y-%m-%d'),
                'weather_condition': random.choice(weather_conditions[season]),
                'temperature': temp,
                'flight_availability_score': random.randint(70, 100),
                'travel_advisory_level': random.choice(['green', 'green', 'green', 'yellow'])
            })
        
        current_date += timedelta(days=1)
    
    headers = ['city_id', 'date', 'weather_condition', 'temperature', 'flight_availability_score', 'travel_advisory_level']
    write_csv('external_factors.csv', headers, data)
    return data

def generate_hotels():
    """Generate hotels data - static list of hotels"""
    hotels = [
        # Mumbai
        {'name': 'Taj Mahal Palace', 'city': 'Mumbai', 'state': 'Maharashtra', 'star_rating': 5.0, 'address': 'Apollo Bunder, Colaba', 'amenities': '["WiFi", "Pool", "Spa", "Gym", "Restaurant", "Bar", "Parking", "Room Service"]'},
        {'name': 'The Oberoi Mumbai', 'city': 'Mumbai', 'state': 'Maharashtra', 'star_rating': 5.0, 'address': 'Nariman Point', 'amenities': '["WiFi", "Pool", "Spa", "Gym", "Restaurant", "Bar", "Business Center"]'},
        {'name': 'Hotel Marine Plaza', 'city': 'Mumbai', 'state': 'Maharashtra', 'star_rating': 4.0, 'address': 'Marine Drive', 'amenities': '["WiFi", "Restaurant", "Gym", "Parking", "Room Service"]'},
        {'name': 'Treebo Trend', 'city': 'Mumbai', 'state': 'Maharashtra', 'star_rating': 3.0, 'address': 'Andheri East', 'amenities': '["WiFi", "Breakfast", "Parking"]'},
        {'name': 'FabHotel Prime', 'city': 'Mumbai', 'state': 'Maharashtra', 'star_rating': 3.0, 'address': 'Vile Parle', 'amenities': '["WiFi", "Breakfast"]'},
        
        # Delhi
        {'name': 'The Leela Palace', 'city': 'Delhi', 'state': 'Delhi', 'star_rating': 5.0, 'address': 'Chanakyapuri', 'amenities': '["WiFi", "Pool", "Spa", "Gym", "Restaurant", "Bar", "Parking", "Business Center"]'},
        {'name': 'ITC Maurya', 'city': 'Delhi', 'state': 'Delhi', 'star_rating': 5.0, 'address': 'Sardar Patel Marg', 'amenities': '["WiFi", "Pool", "Spa", "Gym", "Multiple Restaurants", "Bar"]'},
        {'name': 'Hotel Shanti Palace', 'city': 'Delhi', 'state': 'Delhi', 'star_rating': 3.5, 'address': 'Paharganj', 'amenities': '["WiFi", "Restaurant", "Parking"]'},
        {'name': 'Bloom Boutique', 'city': 'Delhi', 'state': 'Delhi', 'star_rating': 3.0, 'address': 'Karol Bagh', 'amenities': '["WiFi", "Breakfast", "Airport Shuttle"]'},
        {'name': 'Zostel Delhi', 'city': 'Delhi', 'state': 'Delhi', 'star_rating': 2.5, 'address': 'Mahipalpur', 'amenities': '["WiFi", "Common Area", "Cafe"]'},
        
        # Bangalore
        {'name': 'ITC Gardenia', 'city': 'Bangalore', 'state': 'Karnataka', 'star_rating': 5.0, 'address': 'Residency Road', 'amenities': '["WiFi", "Pool", "Spa", "Gym", "Restaurant", "Bar", "Business Center"]'},
        {'name': 'The Oberoi Bangalore', 'city': 'Bangalore', 'state': 'Karnataka', 'star_rating': 5.0, 'address': 'MG Road', 'amenities': '["WiFi", "Pool", "Spa", "Gym", "Restaurant", "Parking"]'},
        {'name': 'Lemon Tree Hotel', 'city': 'Bangalore', 'state': 'Karnataka', 'star_rating': 3.5, 'address': 'Electronic City', 'amenities': '["WiFi", "Restaurant", "Gym", "Parking"]'},
        {'name': 'Ginger Hotel', 'city': 'Bangalore', 'state': 'Karnataka', 'star_rating': 3.0, 'address': 'Whitefield', 'amenities': '["WiFi", "Restaurant", "Parking"]'},
        {'name': 'Treebo Trend Bliss', 'city': 'Bangalore', 'state': 'Karnataka', 'star_rating': 3.0, 'address': 'Koramangala', 'amenities': '["WiFi", "Breakfast"]'},
        
        # Goa
        {'name': 'Taj Exotica', 'city': 'Goa', 'state': 'Goa', 'star_rating': 5.0, 'address': 'Benaulim Beach', 'amenities': '["WiFi", "Beach Access", "Pool", "Spa", "Gym", "Restaurant", "Water Sports"]'},
        {'name': 'Alila Diwa Goa', 'city': 'Goa', 'state': 'Goa', 'star_rating': 5.0, 'address': 'Majorda Beach', 'amenities': '["WiFi", "Pool", "Spa", "Gym", "Restaurant", "Bar"]'},
        {'name': 'Resort Rio', 'city': 'Goa', 'state': 'Goa', 'star_rating': 4.0, 'address': 'Arpora', 'amenities': '["WiFi", "Pool", "Restaurant", "Parking"]'},
        {'name': 'OYO Beach Resort', 'city': 'Goa', 'state': 'Goa', 'star_rating': 3.0, 'address': 'Calangute', 'amenities': '["WiFi", "Beach Access", "Restaurant"]'},
        {'name': 'Backpacker Panda', 'city': 'Goa', 'state': 'Goa', 'star_rating': 2.5, 'address': 'Anjuna', 'amenities': '["WiFi", "Common Kitchen", "Beach Access"]'},
        
        # Jaipur
        {'name': 'Rambagh Palace', 'city': 'Jaipur', 'state': 'Rajasthan', 'star_rating': 5.0, 'address': 'Bhawani Singh Road', 'amenities': '["WiFi", "Pool", "Spa", "Heritage Property", "Restaurant", "Bar"]'},
        {'name': 'Fairmont Jaipur', 'city': 'Jaipur', 'state': 'Rajasthan', 'star_rating': 5.0, 'address': 'Kukas', 'amenities': '["WiFi", "Pool", "Spa", "Gym", "Restaurant", "Golf Course"]'},
        {'name': 'Umaid Bhawan', 'city': 'Jaipur', 'state': 'Rajasthan', 'star_rating': 4.0, 'address': 'C-Scheme', 'amenities': '["WiFi", "Restaurant", "Rooftop", "Parking"]'},
        {'name': 'Hotel Pearl Palace', 'city': 'Jaipur', 'state': 'Rajasthan', 'star_rating': 3.0, 'address': 'Hathroi Fort', 'amenities': '["WiFi", "Restaurant", "Terrace"]'},
        {'name': 'Zostel Jaipur', 'city': 'Jaipur', 'state': 'Rajasthan', 'star_rating': 2.5, 'address': 'MI Road', 'amenities': '["WiFi", "Common Area", "Cafe"]'},
        
        # Add more cities with 5 hotels each (condensed for brevity)
        # Kolkata
        {'name': 'The Oberoi Grand', 'city': 'Kolkata', 'state': 'West Bengal', 'star_rating': 5.0, 'address': 'Jawaharlal Nehru Road', 'amenities': '["WiFi", "Pool", "Spa", "Gym", "Restaurant", "Heritage Property"]'},
        {'name': 'ITC Royal Bengal', 'city': 'Kolkata', 'state': 'West Bengal', 'star_rating': 5.0, 'address': 'Golf Green', 'amenities': '["WiFi", "Pool", "Spa", "Gym", "Multiple Restaurants"]'},
        {'name': 'The Park Kolkata', 'city': 'Kolkata', 'state': 'West Bengal', 'star_rating': 4.5, 'address': 'Park Street', 'amenities': '["WiFi", "Pool", "Restaurant", "Bar", "Nightclub"]'},
        {'name': 'Hotel Hindustan International', 'city': 'Kolkata', 'state': 'West Bengal', 'star_rating': 4.0, 'address': 'Park Street', 'amenities': '["WiFi", "Restaurant", "Gym", "Parking"]'},
        {'name': 'FabHotel Prime', 'city': 'Kolkata', 'state': 'West Bengal', 'star_rating': 3.0, 'address': 'Salt Lake', 'amenities': '["WiFi", "Breakfast"]'},
        
        # Chennai
        {'name': 'ITC Grand Chola', 'city': 'Chennai', 'state': 'Tamil Nadu', 'star_rating': 5.0, 'address': 'Guindy', 'amenities': '["WiFi", "Pool", "Spa", "Gym", "Multiple Restaurants", "Bar"]'},
        {'name': 'Taj Coromandel', 'city': 'Chennai', 'state': 'Tamil Nadu', 'star_rating': 5.0, 'address': 'Nungambakkam', 'amenities': '["WiFi", "Pool", "Spa", "Restaurant", "Business Center"]'},
        {'name': 'The Residency', 'city': 'Chennai', 'state': 'Tamil Nadu', 'star_rating': 4.0, 'address': 'T Nagar', 'amenities': '["WiFi", "Restaurant", "Gym", "Parking"]'},
        {'name': 'Treebo Trend Sabari', 'city': 'Chennai', 'state': 'Tamil Nadu', 'star_rating': 3.0, 'address': 'Egmore', 'amenities': '["WiFi", "Breakfast"]'},
        {'name': 'Zostel Chennai', 'city': 'Chennai', 'state': 'Tamil Nadu', 'star_rating': 2.5, 'address': 'Teynampet', 'amenities': '["WiFi", "Common Area", "Kitchen"]'},
        
        # Hyderabad
        {'name': 'Taj Falaknuma Palace', 'city': 'Hyderabad', 'state': 'Telangana', 'star_rating': 5.0, 'address': 'Falaknuma', 'amenities': '["WiFi", "Pool", "Spa", "Heritage Property", "Restaurant", "Butler Service"]'},
        {'name': 'ITC Kohenur', 'city': 'Hyderabad', 'state': 'Telangana', 'star_rating': 5.0, 'address': 'HITEC City', 'amenities': '["WiFi", "Pool", "Spa", "Gym", "Restaurant", "Business Center"]'},
        {'name': 'Lemon Tree Hotel', 'city': 'Hyderabad', 'state': 'Telangana', 'star_rating': 3.5, 'address': 'Gachibowli', 'amenities': '["WiFi", "Restaurant", "Gym"]'},
        {'name': 'Ginger Hotel', 'city': 'Hyderabad', 'state': 'Telangana', 'star_rating': 3.0, 'address': 'Madhapur', 'amenities': '["WiFi", "Restaurant", "Parking"]'},
        {'name': 'FabHotel Prime', 'city': 'Hyderabad', 'state': 'Telangana', 'star_rating': 3.0, 'address': 'Kukatpally', 'amenities': '["WiFi", "Breakfast"]'},
        
        # Pune
        {'name': 'JW Marriott Pune', 'city': 'Pune', 'state': 'Maharashtra', 'star_rating': 5.0, 'address': 'Senapati Bapat Road', 'amenities': '["WiFi", "Pool", "Spa", "Gym", "Restaurant", "Bar"]'},
        {'name': 'The Westin Pune', 'city': 'Pune', 'state': 'Maharashtra', 'star_rating': 5.0, 'address': 'Koregaon Park', 'amenities': '["WiFi", "Pool", "Spa", "Gym", "Restaurant"]'},
        {'name': 'Conrad Pune', 'city': 'Pune', 'state': 'Maharashtra', 'star_rating': 4.5, 'address': 'Mangaldas Road', 'amenities': '["WiFi", "Pool", "Restaurant", "Gym", "Bar"]'},
        {'name': 'Treebo Trend', 'city': 'Pune', 'state': 'Maharashtra', 'star_rating': 3.0, 'address': 'Viman Nagar', 'amenities': '["WiFi", "Breakfast"]'},
        {'name': 'Ginger Hotel Pune', 'city': 'Pune', 'state': 'Maharashtra', 'star_rating': 3.0, 'address': 'Wakad', 'amenities': '["WiFi", "Restaurant", "Parking"]'},
        
        # Ahmedabad
        {'name': 'The House of MG', 'city': 'Ahmedabad', 'state': 'Gujarat', 'star_rating': 4.5, 'address': 'Lal Darwaja', 'amenities': '["WiFi", "Pool", "Heritage Property", "Restaurant", "Spa"]'},
        {'name': 'Hyatt Regency', 'city': 'Ahmedabad', 'state': 'Gujarat', 'star_rating': 5.0, 'address': 'Ashram Road', 'amenities': '["WiFi", "Pool", "Spa", "Gym", "Restaurant", "Bar"]'},
        {'name': 'Lemon Tree Hotel', 'city': 'Ahmedabad', 'state': 'Gujarat', 'star_rating': 3.5, 'address': 'SG Highway', 'amenities': '["WiFi", "Restaurant", "Gym"]'},
        {'name': 'Ginger Hotel', 'city': 'Ahmedabad', 'state': 'Gujarat', 'star_rating': 3.0, 'address': 'Satellite', 'amenities': '["WiFi", "Restaurant", "Parking"]'},
        {'name': 'Treebo Trend Inder Residency', 'city': 'Ahmedabad', 'state': 'Gujarat', 'star_rating': 3.0, 'address': 'Navrangpura', 'amenities': '["WiFi", "Breakfast"]'},
        
        # Udaipur
        {'name': 'The Oberoi Udaivilas', 'city': 'Udaipur', 'state': 'Rajasthan', 'star_rating': 5.0, 'address': 'Pichola Lake', 'amenities': '["WiFi", "Pool", "Spa", "Lake View", "Heritage", "Restaurant", "Boat Service"]'},
        {'name': 'Taj Lake Palace', 'city': 'Udaipur', 'state': 'Rajasthan', 'star_rating': 5.0, 'address': 'Lake Pichola', 'amenities': '["WiFi", "Heritage Property", "Restaurant", "Spa", "Lake View"]'},
        {'name': 'Fateh Prakash Palace', 'city': 'Udaipur', 'state': 'Rajasthan', 'star_rating': 4.5, 'address': 'City Palace Complex', 'amenities': '["WiFi", "Heritage Property", "Restaurant", "Lake View"]'},
        {'name': 'Hotel Lakend', 'city': 'Udaipur', 'state': 'Rajasthan', 'star_rating': 3.5, 'address': 'Near City Palace', 'amenities': '["WiFi", "Restaurant", "Rooftop"]'},
        {'name': 'Zostel Udaipur', 'city': 'Udaipur', 'state': 'Rajasthan', 'star_rating': 2.5, 'address': 'Old City', 'amenities': '["WiFi", "Common Area", "Lake View"]'},
        
        # Shimla
        {'name': 'Wildflower Hall', 'city': 'Shimla', 'state': 'Himachal Pradesh', 'star_rating': 5.0, 'address': 'Chharabra', 'amenities': '["WiFi", "Spa", "Gym", "Restaurant", "Mountain View", "Hiking"]'},
        {'name': 'Radisson Jass Shimla', 'city': 'Shimla', 'state': 'Himachal Pradesh', 'star_rating': 4.0, 'address': 'Khalini', 'amenities': '["WiFi", "Restaurant", "Gym", "Mountain View"]'},
        {'name': 'Hotel Combermere', 'city': 'Shimla', 'state': 'Himachal Pradesh', 'star_rating': 3.5, 'address': 'The Mall', 'amenities': '["WiFi", "Restaurant", "Heritage Property"]'},
        {'name': 'Treebo Trend Woodays Resort', 'city': 'Shimla', 'state': 'Himachal Pradesh', 'star_rating': 3.0, 'address': 'Kufri', 'amenities': '["WiFi", "Restaurant", "Mountain View"]'},
        {'name': 'Zostel Shimla', 'city': 'Shimla', 'state': 'Himachal Pradesh', 'star_rating': 2.5, 'address': 'Mall Road', 'amenities': '["WiFi", "Common Area", "Cafe"]'},
        
        # Manali
        {'name': 'The Himalayan', 'city': 'Manali', 'state': 'Himachal Pradesh', 'star_rating': 4.5, 'address': 'Hadimba Road', 'amenities': '["WiFi", "Spa", "Restaurant", "Mountain View", "Adventure Activities"]'},
        {'name': 'Manuallaya Resort', 'city': 'Manali', 'state': 'Himachal Pradesh', 'star_rating': 4.0, 'address': 'Sunny Side', 'amenities': '["WiFi", "Spa", "Restaurant", "Mountain View"]'},
        {'name': 'Snow Valley Resorts', 'city': 'Manali', 'state': 'Himachal Pradesh', 'star_rating': 3.5, 'address': 'Aleo', 'amenities': '["WiFi", "Restaurant", "Bonfire", "Mountain View"]'},
        {'name': 'Apple Country Resort', 'city': 'Manali', 'state': 'Himachal Pradesh', 'star_rating': 3.0, 'address': 'Prini', 'amenities': '["WiFi", "Restaurant", "Garden"]'},
        {'name': 'Zostel Manali', 'city': 'Manali', 'state': 'Himachal Pradesh', 'star_rating': 2.5, 'address': 'Old Manali', 'amenities': '["WiFi", "Common Area", "Cafe", "Mountain View"]'},
        
        # Agra
        {'name': 'The Oberoi Amarvilas', 'city': 'Agra', 'state': 'Uttar Pradesh', 'star_rating': 5.0, 'address': 'Taj East Gate Road', 'amenities': '["WiFi", "Pool", "Spa", "Taj View", "Restaurant", "Bar"]'},
        {'name': 'ITC Mughal', 'city': 'Agra', 'state': 'Uttar Pradesh', 'star_rating': 5.0, 'address': 'Fatehabad Road', 'amenities': '["WiFi", "Pool", "Spa", "Gym", "Multiple Restaurants"]'},
        {'name': 'Taj Hotel & Convention Centre', 'city': 'Agra', 'state': 'Uttar Pradesh', 'star_rating': 4.0, 'address': 'Fatehabad Road', 'amenities': '["WiFi", "Pool", "Restaurant", "Gym"]'},
        {'name': 'Hotel Atulyaa Taj', 'city': 'Agra', 'state': 'Uttar Pradesh', 'star_rating': 3.5, 'address': 'Taj East Gate', 'amenities': '["WiFi", "Restaurant", "Rooftop", "Taj View"]'},
        {'name': 'Zostel Agra', 'city': 'Agra', 'state': 'Uttar Pradesh', 'star_rating': 2.5, 'address': 'Taj Ganj', 'amenities': '["WiFi", "Common Area", "Rooftop"]'},
        
        # Varanasi
        {'name': 'Taj Ganges', 'city': 'Varanasi', 'state': 'Uttar Pradesh', 'star_rating': 5.0, 'address': 'Nadesar Palace Grounds', 'amenities': '["WiFi", "Pool", "Spa", "Restaurant", "Heritage Property"]'},
        {'name': 'Radisson Hotel Varanasi', 'city': 'Varanasi', 'state': 'Uttar Pradesh', 'star_rating': 4.0, 'address': 'The Mall', 'amenities': '["WiFi", "Pool", "Restaurant", "Spa"]'},
        {'name': 'Ganges View Hotel', 'city': 'Varanasi', 'state': 'Uttar Pradesh', 'star_rating': 3.5, 'address': 'Assi Ghat', 'amenities': '["WiFi", "Restaurant", "River View", "Rooftop"]'},
        {'name': 'Hotel Buddha', 'city': 'Varanasi', 'state': 'Uttar Pradesh', 'star_rating': 3.0, 'address': 'Meer Ghat', 'amenities': '["WiFi", "Restaurant", "Ghat View"]'},
        {'name': 'Stops Hostel', 'city': 'Varanasi', 'state': 'Uttar Pradesh', 'star_rating': 2.5, 'address': 'Bengali Tola', 'amenities': '["WiFi", "Common Area", "Rooftop"]'},
        
        # Rishikesh
        {'name': 'Ananda in the Himalayas', 'city': 'Rishikesh', 'state': 'Uttarakhand', 'star_rating': 5.0, 'address': 'The Palace Estate', 'amenities': '["WiFi", "Spa", "Yoga", "Gym", "Restaurant", "Mountain View"]'},
        {'name': 'Taj Rishikesh Resort & Spa', 'city': 'Rishikesh', 'state': 'Uttarakhand', 'star_rating': 5.0, 'address': 'Singthali', 'amenities': '["WiFi", "Pool", "Spa", "Yoga", "Restaurant"]'},
        {'name': 'Ganga Kinare', 'city': 'Rishikesh', 'state': 'Uttarakhand', 'star_rating': 4.0, 'address': 'Virbhadra Road', 'amenities': '["WiFi", "River View", "Restaurant", "Yoga"]'},
        {'name': 'Swiss Cottage', 'city': 'Rishikesh', 'state': 'Uttarakhand', 'star_rating': 3.0, 'address': 'Tapovan', 'amenities': '["WiFi", "Restaurant", "River View"]'},
        {'name': 'Zostel Rishikesh', 'city': 'Rishikesh', 'state': 'Uttarakhand', 'star_rating': 2.5, 'address': 'Tapovan', 'amenities': '["WiFi", "Common Area", "Cafe", "River View"]'},
        
        # Mysore
        {'name': 'Lalitha Mahal Palace', 'city': 'Mysore', 'state': 'Karnataka', 'star_rating': 5.0, 'address': 'T. Narasipur Road', 'amenities': '["WiFi", "Pool", "Heritage Property", "Restaurant", "Spa"]'},
        {'name': 'The Windflower Resorts', 'city': 'Mysore', 'state': 'Karnataka', 'star_rating': 4.0, 'address': 'Maharana Pratap Simha Road', 'amenities': '["WiFi", "Pool", "Restaurant", "Spa"]'},
        {'name': 'Royal Orchid Metropole', 'city': 'Mysore', 'state': 'Karnataka', 'star_rating': 4.0, 'address': 'Jhansi Lakshmi Bai Road', 'amenities': '["WiFi", "Pool", "Heritage Property", "Restaurant"]'},
        {'name': 'Treebo Trend Maurya Residency', 'city': 'Mysore', 'state': 'Karnataka', 'star_rating': 3.0, 'address': 'Nazarbad', 'amenities': '["WiFi", "Breakfast"]'},
        {'name': 'Zostel Mysore', 'city': 'Mysore', 'state': 'Karnataka', 'star_rating': 2.5, 'address': 'Chamarajpet', 'amenities': '["WiFi", "Common Area", "Cafe"]'},
        
        # Kochi
        {'name': 'Taj Malabar Resort & Spa', 'city': 'Kochi', 'state': 'Kerala', 'star_rating': 5.0, 'address': 'Willingdon Island', 'amenities': '["WiFi", "Pool", "Spa", "Restaurant", "Backwater View"]'},
        {'name': 'Grand Hyatt Kochi Bolgatty', 'city': 'Kochi', 'state': 'Kerala', 'star_rating': 5.0, 'address': 'Bolgatty Island', 'amenities': '["WiFi", "Pool", "Spa", "Gym", "Restaurant"]'},
        {'name': 'Fragrant Nature Backwater Resort', 'city': 'Kochi', 'state': 'Kerala', 'star_rating': 4.0, 'address': 'Vypeen Island', 'amenities': '["WiFi", "Pool", "Backwater View", "Restaurant"]'},
        {'name': 'Old Harbour Hotel', 'city': 'Kochi', 'state': 'Kerala', 'star_rating': 3.5, 'address': 'Fort Kochi', 'amenities': '["WiFi", "Heritage Property", "Restaurant"]'},
        {'name': 'Zostel Kochi', 'city': 'Kochi', 'state': 'Kerala', 'star_rating': 2.5, 'address': 'Fort Kochi', 'amenities': '["WiFi", "Common Area", "Cafe"]'},
        
        # Amritsar
        {'name': 'Taj Swarna', 'city': 'Amritsar', 'state': 'Punjab', 'star_rating': 5.0, 'address': 'Amritsar-Jalandhar Highway', 'amenities': '["WiFi", "Pool", "Spa", "Gym", "Restaurant"]'},
        {'name': 'Hyatt Regency Amritsar', 'city': 'Amritsar', 'state': 'Punjab', 'star_rating': 5.0, 'address': 'Trilok Nagar', 'amenities': '["WiFi", "Pool", "Spa", "Restaurant", "Bar"]'},
        {'name': 'Hotel City Heart', 'city': 'Amritsar', 'state': 'Punjab', 'star_rating': 3.5, 'address': 'Near Golden Temple', 'amenities': '["WiFi", "Restaurant", "Temple View"]'},
        {'name': 'Hotel Sawera Grand', 'city': 'Amritsar', 'state': 'Punjab', 'star_rating': 3.0, 'address': 'Crystal Chowk', 'amenities': '["WiFi", "Restaurant"]'},
        {'name': 'Zostel Amritsar', 'city': 'Amritsar', 'state': 'Punjab', 'star_rating': 2.5, 'address': 'Ranjit Avenue', 'amenities': '["WiFi", "Common Area", "Cafe"]'},
        
        # Darjeeling
        {'name': 'Windamere Hotel', 'city': 'Darjeeling', 'state': 'West Bengal', 'star_rating': 4.5, 'address': 'Observatory Hill', 'amenities': '["WiFi", "Heritage Property", "Restaurant", "Mountain View"]'},
        {'name': 'Mayfair Darjeeling', 'city': 'Darjeeling', 'state': 'West Bengal', 'star_rating': 4.5, 'address': 'The Mall', 'amenities': '["WiFi", "Spa", "Restaurant", "Mountain View"]'},
        {'name': 'Cedar Inn', 'city': 'Darjeeling', 'state': 'West Bengal', 'star_rating': 3.5, 'address': 'Jalapahar Road', 'amenities': '["WiFi", "Restaurant", "Mountain View"]'},
        {'name': 'Hotel Dekeling', 'city': 'Darjeeling', 'state': 'West Bengal', 'star_rating': 3.0, 'address': 'Gandhi Road', 'amenities': '["WiFi", "Restaurant", "Tea Garden View"]'},
        {'name': 'Zostel Darjeeling', 'city': 'Darjeeling', 'state': 'West Bengal', 'star_rating': 2.5, 'address': 'Mall Road', 'amenities': '["WiFi", "Common Area", "Mountain View"]'},
    ]
    
    headers = ['name', 'city', 'state', 'star_rating', 'address', 'amenities']
    write_csv('hotels.csv', headers, hotels)
    return hotels

def generate_hotel_rooms():
    """Generate hotel rooms based on hotel star ratings"""
    rooms = []
    room_id = 1
    
    # Room configurations based on star rating
    room_configs = {
        5.0: [
            ('Standard Room', 2, (10000, 13000)),
            ('Deluxe Room', 2, (15000, 20000)),
            ('Executive Suite', 3, (25000, 35000)),
            ('Presidential Suite', 4, (50000, 80000))
        ],
        4.5: [
            ('Standard Room', 2, (7000, 10000)),
            ('Deluxe Room', 2, (10000, 15000)),
            ('Executive Suite', 3, (18000, 25000))
        ],
        4.0: [
            ('Standard Room', 2, (5000, 7000)),
            ('Deluxe Room', 2, (8000, 11000)),
            ('Executive Suite', 3, (15000, 20000))
        ],
        3.5: [
            ('Standard Room', 2, (3000, 4000)),
            ('Deluxe Room', 2, (4500, 6000))
        ],
        3.0: [
            ('Standard Room', 2, (2000, 2500)),
            ('Deluxe Room', 2, (3000, 4000))
        ],
        2.5: [
            ('Dorm Bed', 1, (500, 800)),
            ('Private Room', 2, (1500, 2000)),
            ('Standard Room', 2, (2000, 2500))
        ]
    }
    
    # Generate rooms for 100 hotels
    for hotel_id in range(1, 101):
        # Determine star rating (cycle through ratings)
        star_ratings = [5.0, 5.0, 4.5, 4.0, 3.5, 3.0, 2.5]
        star_rating = star_ratings[(hotel_id - 1) % 7]
        
        config = room_configs.get(star_rating, room_configs[3.0])
        
        for room_type, capacity, (min_price, max_price) in config:
            base_price = round(random.uniform(min_price, max_price), 2)
            rooms.append({
                'hotel_id': hotel_id,
                'room_type': room_type,
                'capacity': capacity,
                'base_price': base_price
            })
            room_id += 1
    
    headers = ['hotel_id', 'room_type', 'capacity', 'base_price']
    write_csv('hotel_rooms.csv', headers, rooms)
    return rooms

def generate_pricing(hotel_rooms):
    """Generate pricing data for all rooms across date range"""
    pricing = []
    start_date = datetime(2024, 6, 1)
    end_date = datetime(2024, 11, 30)
    
    current_date = start_date
    pricing_id = 1
    
    while current_date <= end_date:
        month = current_date.month
        day_of_week = current_date.weekday()
        
        # Seasonal multiplier
        if month in [10, 11, 12]:  # Festival season
            seasonal_multiplier = random.uniform(1.3, 1.6)
        elif month in [4, 5, 6]:  # Summer
            seasonal_multiplier = random.uniform(1.1, 1.3)
        elif month in [7, 8]:  # Monsoon discount
            seasonal_multiplier = random.uniform(0.7, 0.9)
        else:
            seasonal_multiplier = random.uniform(1.0, 1.2)
        
        # Weekend premium
        weekend_multiplier = 1.2 if day_of_week in [5, 6] else 1.0
        
        for room in hotel_rooms:
            final_price = round(
                room['base_price'] * seasonal_multiplier * weekend_multiplier,
                2
            )
            
            availability = random.choices(
                ['available', 'limited', 'sold_out'],
                weights=[70, 20, 10]
            )[0]
            
            pricing.append({
                'hotel_id': room['hotel_id'],
                'room_id': pricing_id % len(hotel_rooms) + 1,  # Simplified room_id mapping
                'date': current_date.strftime('%Y-%m-%d'),
                'price_per_night': final_price,
                'availability_status': availability
            })
            pricing_id += 1
        
        current_date += timedelta(days=1)
    
    headers = ['hotel_id', 'room_id', 'date', 'price_per_night', 'availability_status']
    write_csv('pricing.csv', headers, pricing)
    return pricing

def generate_campaigns():
    """Generate marketing campaigns - static list"""
    campaigns = [
        {'campaign_name': 'Summer Sale 2024', 'start_date': '2024-04-01', 'end_date': '2024-06-30', 'campaign_type': 'email', 'target_audience': 'Existing customers'},
        {'campaign_name': 'Google Ads - Beach Destinations', 'start_date': '2024-01-01', 'end_date': '2024-12-31', 'campaign_type': 'search_ads', 'target_audience': 'Beach lovers'},
        {'campaign_name': 'Facebook - Heritage Hotels', 'start_date': '2024-01-01', 'end_date': '2024-12-31', 'campaign_type': 'social_media', 'target_audience': 'Culture enthusiasts'},
        {'campaign_name': 'Diwali Special Offer', 'start_date': '2024-10-01', 'end_date': '2024-11-15', 'campaign_type': 'email', 'target_audience': 'All users'},
        {'campaign_name': 'New Year Campaign', 'start_date': '2024-11-15', 'end_date': '2025-01-05', 'campaign_type': 'search_ads', 'target_audience': 'Party travelers'},
        {'campaign_name': 'Instagram - Hill Stations', 'start_date': '2024-03-01', 'end_date': '2024-09-30', 'campaign_type': 'social_media', 'target_audience': 'Adventure seekers'},
        {'campaign_name': 'Affiliate - Travel Bloggers', 'start_date': '2024-01-01', 'end_date': '2024-12-31', 'campaign_type': 'affiliate', 'target_audience': 'Blog readers'},
        {'campaign_name': 'Corporate Travel Program', 'start_date': '2024-01-01', 'end_date': '2024-12-31', 'campaign_type': 'email', 'target_audience': 'Business travelers'},
        {'campaign_name': 'Weekend Getaway Flash Sale', 'start_date': '2024-06-01', 'end_date': '2024-11-30', 'campaign_type': 'display_ads', 'target_audience': 'Weekend travelers'},
        {'campaign_name': 'Monsoon Special', 'start_date': '2024-06-15', 'end_date': '2024-09-15', 'campaign_type': 'email', 'target_audience': 'Monsoon lovers'},
        {'campaign_name': 'Festival Season Mega Sale', 'start_date': '2024-09-01', 'end_date': '2024-11-30', 'campaign_type': 'search_ads', 'target_audience': 'Festival travelers'},
        {'campaign_name': 'Luxury Hotels Premium', 'start_date': '2024-01-01', 'end_date': '2024-12-31', 'campaign_type': 'display_ads', 'target_audience': 'Luxury seekers'},
    ]
    
    headers = ['campaign_name', 'start_date', 'end_date', 'campaign_type', 'target_audience']
    write_csv('campaigns.csv', headers, campaigns)
    return campaigns

# ============================================
# RANDOM DATA GENERATION
# ============================================

def generate_users(count=1000):
    """Generate random user data"""
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

def generate_search_queries_hotel_bookings(count=15000):
    """Generate random search queries"""
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
            'user_id': random.randint(1, 1000),
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

def generate_traffic_sources(search_queries_hotel_bookings, campaigns):
    """Generate random traffic sources based on search queries"""
    traffic = []
    
    sources = ['organic', 'paid_ads', 'email', 'social_media', 'direct', 'referral', 'affiliate']
    
    for query in search_queries_hotel_bookings:
        source = random.choice(sources)
        
        # 40% chance of having a campaign_id
        campaign_id = None
        if random.random() < 0.4 and campaigns:
            campaign_id = random.randint(1, len(campaigns))
        
        referrer_url = None
        rand = random.random()
        if rand < 0.6:
            referrer_url = f'https://google.com/search?q=hotels+{query["destination"]}'
        elif rand < 0.8:
            referrer_url = 'https://facebook.com/mmt'
        
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

def generate_marketing_spends(campaigns):
    """Generate random marketing spend data"""
    spends = []
    
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
    
    for idx, campaign in enumerate(campaigns, 1):
        start = datetime.strptime(campaign['start_date'], '%Y-%m-%d')
        end = datetime.strptime(campaign['end_date'], '%Y-%m-%d')
        
        # Only generate for dates within our range
        start = max(start, datetime(2024, 6, 1))
        end = min(end, datetime(2024, 11, 30))
        
        if start > end:
            continue
        
        current = start
        campaign_type = campaign['campaign_type']
        
        while current <= end:
            spend_min, spend_max = spend_ranges.get(campaign_type, (20000, 50000))
            imp_min, imp_max = impression_ranges.get(campaign_type, (300000, 700000))
            click_min, click_max = click_ranges.get(campaign_type, (4000, 10000))
            
            spends.append({
                'campaign_id': idx,
                'date': current.strftime('%Y-%m-%d'),
                'spend': round(random.uniform(spend_min, spend_max), 2),
                'impressions': random.randint(imp_min, imp_max),
                'clicks': random.randint(click_min, click_max),
                'conversions': random.randint(100, 500)
            })
            
            current += timedelta(days=1)
    
    headers = ['campaign_id', 'date', 'spend', 'impressions', 'clicks', 'conversions']
    write_csv('marketing_spends.csv', headers, spends)
    return spends

def generate_hotel_bookings(search_queries_hotel_bookings, hotel_rooms, count=8000):
    """Generate random hotel bookings based on search queries"""
    bookings = []
    
    # Create a mapping of cities to hotel IDs (simplified)
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
    
    # Create room lookup by hotel_id
    rooms_by_hotel = {}
    for room in hotel_rooms:
        hotel_id = room['hotel_id']
        if hotel_id not in rooms_by_hotel:
            rooms_by_hotel[hotel_id] = []
        rooms_by_hotel[hotel_id].append(room)
    
    booking_statuses = ['confirmed', 'completed', 'cancelled', 'no_show']
    
    # Sample queries for conversion (5% conversion rate)
    sampled_queries = random.sample(search_queries_hotel_bookings, min(count, len(search_queries_hotel_bookings)))
    
    for query in sampled_queries[:count]:
        destination = query['destination']
        hotel_ids = city_to_hotels.get(destination, [1])
        
        if not hotel_ids:
            continue
        
        hotel_id = random.choice(hotel_ids)
        
        # Get a random room for this hotel
        available_rooms = rooms_by_hotel.get(hotel_id, [])
        if not available_rooms:
            continue
        
        room = random.choice(available_rooms)
        
        # Calculate booking date (within 48 hours of search)
        search_dt = datetime.strptime(query['search_date'], '%Y-%m-%d %H:%M:%S')
        booking_date = search_dt + timedelta(hours=random.uniform(1, 48))
        
        # Calculate stay duration
        check_in = datetime.strptime(query['check_in_date'], '%Y-%m-%d')
        check_out = datetime.strptime(query['check_out_date'], '%Y-%m-%d')
        num_nights = (check_out - check_in).days
        
        # Calculate amount (base price * nights with some variation)
        amount_paid = round(room['base_price'] * num_nights * random.uniform(0.9, 1.1), 2)
        
        bookings.append({
            'user_id': query['user_id'],
            'hotel_id': hotel_id,
            'room_id': room.get('room_id', random.randint(1, len(hotel_rooms))),
            'booking_date': booking_date.strftime('%Y-%m-%d %H:%M:%S'),
            'check_in_date': query['check_in_date'],
            'check_out_date': query['check_out_date'],
            'destination': destination,
            'amount_paid': amount_paid,
            'booking_status': random.choices(booking_statuses, weights=[85, 8, 5, 2])[0],
            'number_of_guests': query['number_of_guests']
        })
    
    headers = ['user_id', 'hotel_id', 'room_id', 'booking_date', 'check_in_date', 'check_out_date', 'destination', 'amount_paid', 'booking_status', 'number_of_guests']
    write_csv('hotel_bookings.csv', headers, bookings)
    return bookings

# ============================================
# MAIN EXECUTION
# ============================================

def main():
    """Main function to generate all CSV files"""
    print("=" * 60)
    print("Starting CSV Data Generation for MMT Hotel Booking System")
    print("=" * 60)
    print()
    
    # Step 1: Generate static data
    print("📋 Generating static data (non-random)...")
    cities = generate_cities()
    festivals = generate_festivals()
    events = generate_events()
    external_factors = generate_external_factors()
    hotels = generate_hotels()
    hotel_rooms = generate_hotel_rooms()
    pricing = generate_pricing(hotel_rooms)
    campaigns = generate_campaigns()
    print()
    
    # Step 2: Generate random data
    print("🎲 Generating random data...")
    users = generate_users(count=1000)
    search_queries_hotel_bookings = generate_search_queries_hotel_bookings(count=15000)
    traffic_sources = generate_traffic_sources(search_queries_hotel_bookings, campaigns)
    marketing_spends = generate_marketing_spends(campaigns)
    hotel_bookings = generate_hotel_bookings(search_queries_hotel_bookings, hotel_rooms, count=8000)
    print()
    
    # Summary
    print("=" * 60)
    print("✅ CSV Generation Complete!")
    print("=" * 60)
    print(f"📁 Output directory: {OUTPUT_DIR.absolute()}")
    print()
    print("📊 Summary:")
    print(f"   - Cities: {len(cities)} records")
    print(f"   - Festivals: {len(festivals)} records")
    print(f"   - Events: {len(events)} records")
    print(f"   - External Factors: {len(external_factors)} records")
    print(f"   - Hotels: {len(hotels)} records")
    print(f"   - Hotel Rooms: {len(hotel_rooms)} records")
    print(f"   - Pricing: {len(pricing)} records")
    print(f"   - Campaigns: {len(campaigns)} records")
    print(f"   - Users: {len(users)} records")
    print(f"   - Search Queries: {len(search_queries_hotel_bookings)} records")
    print(f"   - Traffic Sources: {len(traffic_sources)} records")
    print(f"   - Marketing Spends: {len(marketing_spends)} records")
    print(f"   - Hotel Bookings: {len(hotel_bookings)} records")
    print()
    print("🎉 All CSV files are ready for import!")

if __name__ == "__main__":
    main()