\c ota_hotel;
-- ============================================
-- SEED DATA GENERATION
-- ============================================

-- ============================================
-- 1. EXTERNAL SCHEMA - CITIES
-- ============================================


INSERT INTO external.cities (city_name, state, country, timezone) VALUES
('Mumbai', 'Maharashtra', 'India', 'Asia/Kolkata'),
('Delhi', 'Delhi', 'India', 'Asia/Kolkata'),
('Bangalore', 'Karnataka', 'India', 'Asia/Kolkata'),
('Goa', 'Goa', 'India', 'Asia/Kolkata'),
('Jaipur', 'Rajasthan', 'India', 'Asia/Kolkata'),
('Kolkata', 'West Bengal', 'India', 'Asia/Kolkata'),
('Chennai', 'Tamil Nadu', 'India', 'Asia/Kolkata'),
('Hyderabad', 'Telangana', 'India', 'Asia/Kolkata'),
('Pune', 'Maharashtra', 'India', 'Asia/Kolkata'),
('Ahmedabad', 'Gujarat', 'India', 'Asia/Kolkata'),
('Udaipur', 'Rajasthan', 'India', 'Asia/Kolkata'),
('Shimla', 'Himachal Pradesh', 'India', 'Asia/Kolkata'),
('Manali', 'Himachal Pradesh', 'India', 'Asia/Kolkata'),
('Agra', 'Uttar Pradesh', 'India', 'Asia/Kolkata'),
('Varanasi', 'Uttar Pradesh', 'India', 'Asia/Kolkata'),
('Rishikesh', 'Uttarakhand', 'India', 'Asia/Kolkata'),
('Mysore', 'Karnataka', 'India', 'Asia/Kolkata'),
('Kochi', 'Kerala', 'India', 'Asia/Kolkata'),
('Amritsar', 'Punjab', 'India', 'Asia/Kolkata'),
('Darjeeling', 'West Bengal', 'India', 'Asia/Kolkata');

-- ============================================
-- 2. EXTERNAL SCHEMA - FESTIVALS
-- ============================================

INSERT INTO external.festivals (city_id, festival_name, start_date, end_date, festival_type, significance_level, expected_tourist_influx) VALUES
(1, 'Ganesh Chaturthi', '2024-09-07', '2024-09-17', 'religious', 'national', 500000),
(2, 'Diwali', '2024-11-01', '2024-11-05', 'religious', 'national', 800000),
(3, 'Diwali', '2024-11-01', '2024-11-05', 'religious', 'national', 600000),
(4, 'Goa Carnival', '2024-02-10', '2024-02-13', 'cultural', 'international', 300000),
(4, 'New Year Celebration', '2024-12-31', '2025-01-01', 'cultural', 'international', 400000),
(5, 'Jaipur Literature Festival', '2024-01-25', '2024-01-29', 'cultural', 'international', 250000),
(5, 'Diwali', '2024-11-01', '2024-11-05', 'religious', 'national', 400000),
(6, 'Durga Puja', '2024-10-10', '2024-10-14', 'religious', 'national', 700000),
(7, 'Pongal', '2025-01-14', '2025-01-17', 'religious', 'regional', 300000),
(8, 'Bonalu Festival', '2024-07-16', '2024-07-28', 'religious', 'regional', 200000),
(9, 'Ganesh Chaturthi', '2024-09-07', '2024-09-17', 'religious', 'national', 350000),
(10, 'Navratri', '2024-10-03', '2024-10-12', 'religious', 'regional', 450000),
(11, 'Mewar Festival', '2024-03-25', '2024-03-27', 'cultural', 'regional', 150000),
(14, 'Taj Mahotsav', '2024-02-18', '2024-02-27', 'cultural', 'international', 200000),
(15, 'Dev Deepawali', '2024-11-15', '2024-11-15', 'religious', 'national', 350000),
(16, 'International Yoga Festival', '2024-03-01', '2024-03-07', 'cultural', 'international', 180000),
(18, 'Kochi-Muziris Biennale', '2024-12-12', '2025-04-10', 'cultural', 'international', 250000),
(19, 'Baisakhi', '2024-04-13', '2024-04-14', 'religious', 'regional', 200000),
(1, 'Mumbai Film Festival', '2024-10-17', '2024-10-24', 'cultural', 'national', 100000),
(3, 'Bangalore Tech Summit', '2024-11-19', '2024-11-21', 'other', 'international', 150000);

-- ============================================
-- 3. EXTERNAL SCHEMA - EVENTS
-- ============================================

INSERT INTO external.events (city_id, event_name, event_date, event_type, expected_attendance) VALUES
(1, 'Mumbai Marathon', '2024-01-21', 'sports', 55000),
(1, 'Tech Conference Mumbai', '2024-03-15', 'business', 5000),
(2, 'Delhi Auto Expo', '2024-01-12', 'business', 600000),
(2, 'India International Trade Fair', '2024-11-14', 'business', 500000),
(3, 'Bangalore Comics Con', '2024-02-17', 'entertainment', 25000),
(3, 'Aero India', '2024-02-20', 'business', 100000),
(4, 'Sunburn Festival', '2024-12-27', 'music', 350000),
(5, 'Jaipur Wedding Season Peak', '2024-12-01', 'other', 100000),
(6, 'Kolkata Book Fair', '2024-01-31', 'cultural', 200000),
(7, 'Chennai Music Season', '2024-12-15', 'music', 150000),
(8, 'Hyderabad Comic Con', '2024-08-10', 'entertainment', 30000),
(11, 'World Music Festival Udaipur', '2024-02-10', 'music', 50000),
(12, 'Shimla Summer Festival', '2024-06-01', 'cultural', 75000),
(13, 'Manali Winter Carnival', '2025-01-02', 'cultural', 80000),
(14, 'Agra Food Festival', '2024-11-20', 'food', 40000),
(18, 'Kochi Design Week', '2024-12-05', 'cultural', 20000);

-- ============================================
-- 4. EXTERNAL SCHEMA - EXTERNAL FACTORS (Last 6 months)
-- ============================================

-- Generate weather data for major cities across different seasons
INSERT INTO external.external_factors (city_id, date, weather_condition, temperature, flight_availability_score, travel_advisory_level)
SELECT 
    city_id,
    date,
    CASE 
        WHEN EXTRACT(MONTH FROM date) IN (12, 1, 2) THEN 
            (ARRAY['clear', 'partly_cloudy', 'foggy'])[floor(random() * 3 + 1)::int]
        WHEN EXTRACT(MONTH FROM date) IN (3, 4, 5) THEN 
            (ARRAY['clear', 'hot', 'partly_cloudy'])[floor(random() * 3 + 1)::int]
        WHEN EXTRACT(MONTH FROM date) IN (6, 7, 8) THEN 
            (ARRAY['rainy', 'cloudy', 'humid'])[floor(random() * 3 + 1)::int]
        ELSE 
            (ARRAY['clear', 'pleasant', 'partly_cloudy'])[floor(random() * 3 + 1)::int]
    END as weather_condition,
    CASE 
        WHEN city_id IN (12, 13, 20) THEN 10 + random() * 15  -- Hill stations
        WHEN city_id IN (1, 4, 7, 18) THEN 25 + random() * 10  -- Coastal cities
        ELSE 20 + random() * 20  -- Other cities
    END as temperature,
    70 + floor(random() * 30)::int as flight_availability_score,
    (ARRAY['green', 'green', 'green', 'yellow'])[floor(random() * 4 + 1)::int] as travel_advisory_level
FROM 
    external.cities
CROSS JOIN 
    generate_series('2024-06-01'::date, '2024-11-30'::date, '1 day'::interval) as date
WHERE city_id <= 20;

-- ============================================
-- 5. HOTEL SCHEMA - HOTELS
-- ============================================

INSERT INTO hotel.hotels (name, city, state, star_rating, address, amenities) VALUES
-- Mumbai Hotels
('Taj Mahal Palace', 'Mumbai', 'Maharashtra', 5.0, 'Apollo Bunder, Colaba', '{"WiFi", "Pool", "Spa", "Gym", "Restaurant", "Bar", "Parking", "Room Service"}'),
('The Oberoi Mumbai', 'Mumbai', 'Maharashtra', 5.0, 'Nariman Point', '{"WiFi", "Pool", "Spa", "Gym", "Restaurant", "Bar", "Business Center"}'),
('Hotel Marine Plaza', 'Mumbai', 'Maharashtra', 4.0, 'Marine Drive', '{"WiFi", "Restaurant", "Gym", "Parking", "Room Service"}'),
('Treebo Trend', 'Mumbai', 'Maharashtra', 3.0, 'Andheri East', '{"WiFi", "Breakfast", "Parking"}'),
('FabHotel Prime', 'Mumbai', 'Maharashtra', 3.0, 'Vile Parle', '{"WiFi", "Breakfast"}'),

-- Delhi Hotels
('The Leela Palace', 'Delhi', 'Delhi', 5.0, 'Chanakyapuri', '{"WiFi", "Pool", "Spa", "Gym", "Restaurant", "Bar", "Parking", "Business Center"}'),
('ITC Maurya', 'Delhi', 'Delhi', 5.0, 'Sardar Patel Marg', '{"WiFi", "Pool", "Spa", "Gym", "Multiple Restaurants", "Bar"}'),
('Hotel Shanti Palace', 'Delhi', 'Delhi', 3.5, 'Paharganj', '{"WiFi", "Restaurant", "Parking"}'),
('Bloom Boutique', 'Delhi', 'Delhi', 3.0, 'Karol Bagh', '{"WiFi", "Breakfast", "Airport Shuttle"}'),
('Zostel Delhi', 'Delhi', 'Delhi', 2.5, 'Mahipalpur', '{"WiFi", "Common Area", "Cafe"}'),

-- Bangalore Hotels
('ITC Gardenia', 'Bangalore', 'Karnataka', 5.0, 'Residency Road', '{"WiFi", "Pool", "Spa", "Gym", "Restaurant", "Bar", "Business Center"}'),
('The Oberoi Bangalore', 'Bangalore', 'Karnataka', 5.0, 'MG Road', '{"WiFi", "Pool", "Spa", "Gym", "Restaurant", "Parking"}'),
('Lemon Tree Hotel', 'Bangalore', 'Karnataka', 3.5, 'Electronic City', '{"WiFi", "Restaurant", "Gym", "Parking"}'),
('Ginger Hotel', 'Bangalore', 'Karnataka', 3.0, 'Whitefield', '{"WiFi", "Restaurant", "Parking"}'),
('Treebo Trend Bliss', 'Bangalore', 'Karnataka', 3.0, 'Koramangala', '{"WiFi", "Breakfast"}'),

-- Goa Hotels
('Taj Exotica', 'Goa', 'Goa', 5.0, 'Benaulim Beach', '{"WiFi", "Beach Access", "Pool", "Spa", "Gym", "Restaurant", "Water Sports"}'),
('Alila Diwa Goa', 'Goa', 'Goa', 5.0, 'Majorda Beach', '{"WiFi", "Pool", "Spa", "Gym", "Restaurant", "Bar"}'),
('Resort Rio', 'Goa', 'Goa', 4.0, 'Arpora', '{"WiFi", "Pool", "Restaurant", "Parking"}'),
('OYO Beach Resort', 'Goa', 'Goa', 3.0, 'Calangute', '{"WiFi", "Beach Access", "Restaurant"}'),
('Backpacker Panda', 'Goa', 'Goa', 2.5, 'Anjuna', '{"WiFi", "Common Kitchen", "Beach Access"}'),

-- Jaipur Hotels
('Rambagh Palace', 'Jaipur', 'Rajasthan', 5.0, 'Bhawani Singh Road', '{"WiFi", "Pool", "Spa", "Heritage Property", "Restaurant", "Bar"}'),
('Fairmont Jaipur', 'Jaipur', 'Rajasthan', 5.0, 'Kukas', '{"WiFi", "Pool", "Spa", "Gym", "Restaurant", "Golf Course"}'),
('Umaid Bhawan', 'Jaipur', 'Rajasthan', 4.0, 'C-Scheme', '{"WiFi", "Restaurant", "Rooftop", "Parking"}'),
('Hotel Pearl Palace', 'Jaipur', 'Rajasthan', 3.0, 'Hathroi Fort', '{"WiFi", "Restaurant", "Terrace"}'),
('Zostel Jaipur', 'Jaipur', 'Rajasthan', 2.5, 'MI Road', '{"WiFi", "Common Area", "Cafe"}'),

-- Kolkata Hotels
('The Oberoi Grand', 'Kolkata', 'West Bengal', 5.0, 'Jawaharlal Nehru Road', '{"WiFi", "Pool", "Spa", "Gym", "Restaurant", "Heritage Property"}'),
('ITC Royal Bengal', 'Kolkata', 'West Bengal', 5.0, 'Golf Green', '{"WiFi", "Pool", "Spa", "Gym", "Multiple Restaurants"}'),
('The Park Kolkata', 'Kolkata', 'West Bengal', 4.5, 'Park Street', '{"WiFi", "Pool", "Restaurant", "Bar", "Nightclub"}'),
('Hotel Hindustan International', 'Kolkata', 'West Bengal', 4.0, 'Park Street', '{"WiFi", "Restaurant", "Gym", "Parking"}'),
('FabHotel Prime', 'Kolkata', 'West Bengal', 3.0, 'Salt Lake', '{"WiFi", "Breakfast"}'),

-- Chennai Hotels
('ITC Grand Chola', 'Chennai', 'Tamil Nadu', 5.0, 'Guindy', '{"WiFi", "Pool", "Spa", "Gym", "Multiple Restaurants", "Bar"}'),
('Taj Coromandel', 'Chennai', 'Tamil Nadu', 5.0, 'Nungambakkam', '{"WiFi", "Pool", "Spa", "Restaurant", "Business Center"}'),
('The Residency', 'Chennai', 'Tamil Nadu', 4.0, 'T Nagar', '{"WiFi", "Restaurant", "Gym", "Parking"}'),
('Treebo Trend Sabari', 'Chennai', 'Tamil Nadu', 3.0, 'Egmore', '{"WiFi", "Breakfast"}'),
('Zostel Chennai', 'Chennai', 'Tamil Nadu', 2.5, 'Teynampet', '{"WiFi", "Common Area", "Kitchen"}'),

-- Hyderabad Hotels
('Taj Falaknuma Palace', 'Hyderabad', 'Telangana', 5.0, 'Falaknuma', '{"WiFi", "Pool", "Spa", "Heritage Property", "Restaurant", "Butler Service"}'),
('ITC Kohenur', 'Hyderabad', 'Telangana', 5.0, 'HITEC City', '{"WiFi", "Pool", "Spa", "Gym", "Restaurant", "Business Center"}'),
('Lemon Tree Hotel', 'Hyderabad', 'Telangana', 3.5, 'Gachibowli', '{"WiFi", "Restaurant", "Gym"}'),
('Ginger Hotel', 'Hyderabad', 'Telangana', 3.0, 'Madhapur', '{"WiFi", "Restaurant", "Parking"}'),
('FabHotel Prime', 'Hyderabad', 'Telangana', 3.0, 'Kukatpally', '{"WiFi", "Breakfast"}'),

-- Pune Hotels
('JW Marriott Pune', 'Pune', 'Maharashtra', 5.0, 'Senapati Bapat Road', '{"WiFi", "Pool", "Spa", "Gym", "Restaurant", "Bar"}'),
('The Westin Pune', 'Pune', 'Maharashtra', 5.0, 'Koregaon Park', '{"WiFi", "Pool", "Spa", "Gym", "Restaurant"}'),
('Conrad Pune', 'Pune', 'Maharashtra', 4.5, 'Mangaldas Road', '{"WiFi", "Pool", "Restaurant", "Gym", "Bar"}'),
('Treebo Trend', 'Pune', 'Maharashtra', 3.0, 'Viman Nagar', '{"WiFi", "Breakfast"}'),
('Ginger Hotel Pune', 'Pune', 'Maharashtra', 3.0, 'Wakad', '{"WiFi", "Restaurant", "Parking"}'),

-- Ahmedabad Hotels
('The House of MG', 'Ahmedabad', 'Gujarat', 4.5, 'Lal Darwaja', '{"WiFi", "Pool", "Heritage Property", "Restaurant", "Spa"}'),
('Hyatt Regency', 'Ahmedabad', 'Gujarat', 5.0, 'Ashram Road', '{"WiFi", "Pool", "Spa", "Gym", "Restaurant", "Bar"}'),
('Lemon Tree Hotel', 'Ahmedabad', 'Gujarat', 3.5, 'SG Highway', '{"WiFi", "Restaurant", "Gym"}'),
('Ginger Hotel', 'Ahmedabad', 'Gujarat', 3.0, 'Satellite', '{"WiFi", "Restaurant", "Parking"}'),
('Treebo Trend Inder Residency', 'Ahmedabad', 'Gujarat', 3.0, 'Navrangpura', '{"WiFi", "Breakfast"}'),

-- Udaipur Hotels
('The Oberoi Udaivilas', 'Udaipur', 'Rajasthan', 5.0, 'Pichola Lake', '{"WiFi", "Pool", "Spa", "Lake View", "Heritage", "Restaurant", "Boat Service"}'),
('Taj Lake Palace', 'Udaipur', 'Rajasthan', 5.0, 'Lake Pichola', '{"WiFi", "Heritage Property", "Restaurant", "Spa", "Lake View"}'),
('Fateh Prakash Palace', 'Udaipur', 'Rajasthan', 4.5, 'City Palace Complex', '{"WiFi", "Heritage Property", "Restaurant", "Lake View"}'),
('Hotel Lakend', 'Udaipur', 'Rajasthan', 3.5, 'Near City Palace', '{"WiFi", "Restaurant", "Rooftop"}'),
('Zostel Udaipur', 'Udaipur', 'Rajasthan', 2.5, 'Old City', '{"WiFi", "Common Area", "Lake View"}'),

-- Shimla Hotels
('Wildflower Hall', 'Shimla', 'Himachal Pradesh', 5.0, 'Chharabra', '{"WiFi", "Spa", "Gym", "Restaurant", "Mountain View", "Hiking"}'),
('Radisson Jass Shimla', 'Shimla', 'Himachal Pradesh', 4.0, 'Khalini', '{"WiFi", "Restaurant", "Gym", "Mountain View"}'),
('Hotel Combermere', 'Shimla', 'Himachal Pradesh', 3.5, 'The Mall', '{"WiFi", "Restaurant", "Heritage Property"}'),
('Treebo Trend Woodays Resort', 'Shimla', 'Himachal Pradesh', 3.0, 'Kufri', '{"WiFi", "Restaurant", "Mountain View"}'),
('Zostel Shimla', 'Shimla', 'Himachal Pradesh', 2.5, 'Mall Road', '{"WiFi", "Common Area", "Cafe"}'),

-- Manali Hotels
('The Himalayan', 'Manali', 'Himachal Pradesh', 4.5, 'Hadimba Road', '{"WiFi", "Spa", "Restaurant", "Mountain View", "Adventure Activities"}'),
('Manuallaya Resort', 'Manali', 'Himachal Pradesh', 4.0, 'Sunny Side', '{"WiFi", "Spa", "Restaurant", "Mountain View"}'),
('Snow Valley Resorts', 'Manali', 'Himachal Pradesh', 3.5, 'Aleo', '{"WiFi", "Restaurant", "Bonfire", "Mountain View"}'),
('Apple Country Resort', 'Manali', 'Himachal Pradesh', 3.0, 'Prini', '{"WiFi", "Restaurant", "Garden"}'),
('Zostel Manali', 'Manali', 'Himachal Pradesh', 2.5, 'Old Manali', '{"WiFi", "Common Area", "Cafe", "Mountain View"}'),

-- Agra Hotels
('The Oberoi Amarvilas', 'Agra', 'Uttar Pradesh', 5.0, 'Taj East Gate Road', '{"WiFi", "Pool", "Spa", "Taj View", "Restaurant", "Bar"}'),
('ITC Mughal', 'Agra', 'Uttar Pradesh', 5.0, 'Fatehabad Road', '{"WiFi", "Pool", "Spa", "Gym", "Multiple Restaurants"}'),
('Taj Hotel & Convention Centre', 'Agra', 'Uttar Pradesh', 4.0, 'Fatehabad Road', '{"WiFi", "Pool", "Restaurant", "Gym"}'),
('Hotel Atulyaa Taj', 'Agra', 'Uttar Pradesh', 3.5, 'Taj East Gate', '{"WiFi", "Restaurant", "Rooftop", "Taj View"}'),
('Zostel Agra', 'Agra', 'Uttar Pradesh', 2.5, 'Taj Ganj', '{"WiFi", "Common Area", "Rooftop"}'),

-- Varanasi Hotels
('Taj Ganges', 'Varanasi', 'Uttar Pradesh', 5.0, 'Nadesar Palace Grounds', '{"WiFi", "Pool", "Spa", "Restaurant", "Heritage Property"}'),
('Radisson Hotel Varanasi', 'Varanasi', 'Uttar Pradesh', 4.0, 'The Mall', '{"WiFi", "Pool", "Restaurant", "Spa"}'),
('Ganges View Hotel', 'Varanasi', 'Uttar Pradesh', 3.5, 'Assi Ghat', '{"WiFi", "Restaurant", "River View", "Rooftop"}'),
('Hotel Buddha', 'Varanasi', 'Uttar Pradesh', 3.0, 'Meer Ghat', '{"WiFi", "Restaurant", "Ghat View"}'),
('Stops Hostel', 'Varanasi', 'Uttar Pradesh', 2.5, 'Bengali Tola', '{"WiFi", "Common Area", "Rooftop"}'),

-- Rishikesh Hotels
('Ananda in the Himalayas', 'Rishikesh', 'Uttarakhand', 5.0, 'The Palace Estate', '{"WiFi", "Spa", "Yoga", "Gym", "Restaurant", "Mountain View"}'),
('Taj Rishikesh Resort & Spa', 'Rishikesh', 'Uttarakhand', 5.0, 'Singthali', '{"WiFi", "Pool", "Spa", "Yoga", "Restaurant"}'),
('Ganga Kinare', 'Rishikesh', 'Uttarakhand', 4.0, 'Virbhadra Road', '{"WiFi", "River View", "Restaurant", "Yoga"}'),
('Swiss Cottage', 'Rishikesh', 'Uttarakhand', 3.0, 'Tapovan', '{"WiFi", "Restaurant", "River View"}'),
('Zostel Rishikesh', 'Rishikesh', 'Uttarakhand', 2.5, 'Tapovan', '{"WiFi", "Common Area", "Cafe", "River View"}'),

-- Mysore Hotels
('Lalitha Mahal Palace', 'Mysore', 'Karnataka', 5.0, 'T. Narasipur Road', '{"WiFi", "Pool", "Heritage Property", "Restaurant", "Spa"}'),
('The Windflower Resorts', 'Mysore', 'Karnataka', 4.0, 'Maharana Pratap Simha Road', '{"WiFi", "Pool", "Restaurant", "Spa"}'),
('Royal Orchid Metropole', 'Mysore', 'Karnataka', 4.0, 'Jhansi Lakshmi Bai Road', '{"WiFi", "Pool", "Heritage Property", "Restaurant"}'),
('Treebo Trend Maurya Residency', 'Mysore', 'Karnataka', 3.0, 'Nazarbad', '{"WiFi", "Breakfast"}'),
('Zostel Mysore', 'Mysore', 'Karnataka', 2.5, 'Chamarajpet', '{"WiFi", "Common Area", "Cafe"}'),

-- Kochi Hotels
('Taj Malabar Resort & Spa', 'Kochi', 'Kerala', 5.0, 'Willingdon Island', '{"WiFi", "Pool", "Spa", "Restaurant", "Backwater View"}'),
('Grand Hyatt Kochi Bolgatty', 'Kochi', 'Kerala', 5.0, 'Bolgatty Island', '{"WiFi", "Pool", "Spa", "Gym", "Restaurant"}'),
('Fragrant Nature Backwater Resort', 'Kochi', 'Kerala', 4.0, 'Vypeen Island', '{"WiFi", "Pool", "Backwater View", "Restaurant"}'),
('Old Harbour Hotel', 'Kochi', 'Kerala', 3.5, 'Fort Kochi', '{"WiFi", "Heritage Property", "Restaurant"}'),
('Zostel Kochi', 'Kochi', 'Kerala', 2.5, 'Fort Kochi', '{"WiFi", "Common Area", "Cafe"}'),

-- Amritsar Hotels
('Taj Swarna', 'Amritsar', 'Punjab', 5.0, 'Amritsar-Jalandhar Highway', '{"WiFi", "Pool", "Spa", "Gym", "Restaurant"}'),
('Hyatt Regency Amritsar', 'Amritsar', 'Punjab', 5.0, 'Trilok Nagar', '{"WiFi", "Pool", "Spa", "Restaurant", "Bar"}'),
('Hotel City Heart', 'Amritsar', 'Punjab', 3.5, 'Near Golden Temple', '{"WiFi", "Restaurant", "Temple View"}'),
('Hotel Sawera Grand', 'Amritsar', 'Punjab', 3.0, 'Crystal Chowk', '{"WiFi", "Restaurant"}'),
('Zostel Amritsar', 'Amritsar', 'Punjab', 2.5, 'Ranjit Avenue', '{"WiFi", "Common Area", "Cafe"}'),

-- Darjeeling Hotels
('Windamere Hotel', 'Darjeeling', 'West Bengal', 4.5, 'Observatory Hill', '{"WiFi", "Heritage Property", "Restaurant", "Mountain View"}'),
('Mayfair Darjeeling', 'Darjeeling', 'West Bengal', 4.5, 'The Mall', '{"WiFi", "Spa", "Restaurant", "Mountain View"}'),
('Cedar Inn', 'Darjeeling', 'West Bengal', 3.5, 'Jalapahar Road', '{"WiFi", "Restaurant", "Mountain View"}'),
('Hotel Dekeling', 'Darjeeling', 'West Bengal', 3.0, 'Gandhi Road', '{"WiFi", "Restaurant", "Tea Garden View"}'),
('Zostel Darjeeling', 'Darjeeling', 'West Bengal', 2.5, 'Mall Road', '{"WiFi", "Common Area", "Mountain View"}');

-- ============================================
-- 6. HOTEL SCHEMA - HOTEL ROOMS
-- ============================================

-- Generate 3-5 room types per hotel (total ~400 rooms)
INSERT INTO hotel.hotel_rooms (hotel_id, room_type, capacity, base_price)
SELECT 
    h.hotel_id,
    room_type,
    capacity,
    CASE 
        WHEN h.star_rating >= 5.0 THEN
            CASE room_type
                WHEN 'Deluxe Room' THEN 15000 + random() * 5000
                WHEN 'Executive Suite' THEN 25000 + random() * 10000
                WHEN 'Presidential Suite' THEN 50000 + random() * 30000
                WHEN 'Standard Room' THEN 10000 + random() * 3000
                ELSE 8000 + random() * 2000
            END
        WHEN h.star_rating >= 4.0 THEN
            CASE room_type
                WHEN 'Deluxe Room' THEN 8000 + random() * 3000
                WHEN 'Executive Suite' THEN 15000 + random() * 5000
                WHEN 'Standard Room' THEN 5000 + random() * 2000
                ELSE 4000 + random() * 1000
            END
        WHEN h.star_rating >= 3.0 THEN
            CASE room_type
                WHEN 'Deluxe Room' THEN 3000 + random() * 1000
                WHEN 'Standard Room' THEN 2000 + random() * 500
                ELSE 1500 + random() * 500
            END
        ELSE
            CASE room_type
                WHEN 'Dorm Bed' THEN 500 + random() * 300
                WHEN 'Private Room' THEN 1500 + random() * 500
                ELSE 1000 + random() * 500
            END
    END as base_price
FROM hotel.hotels h
CROSS JOIN (
    SELECT unnest(ARRAY['Standard Room', 'Deluxe Room', 'Executive Suite']) as room_type, 2 as capacity
    UNION ALL
    SELECT 'Presidential Suite', 4
    UNION ALL
    SELECT 'Dorm Bed', 1
    UNION ALL
    SELECT 'Private Room', 2
) room_types
WHERE 
    (h.star_rating >= 5.0 AND room_type != 'Dorm Bed') OR
    (h.star_rating >= 4.0 AND room_type NOT IN ('Presidential Suite', 'Dorm Bed')) OR
    (h.star_rating >= 3.0 AND room_type IN ('Standard Room', 'Deluxe Room')) OR
    (h.star_rating < 3.0 AND room_type IN ('Dorm Bed', 'Private Room', 'Standard Room'));

-- ============================================
-- 7. HOTEL SCHEMA - PRICING (Last 6 months)
-- ============================================

-- Generate pricing for each room for the last 6 months with seasonal variations
INSERT INTO hotel.pricing (hotel_id, room_id, date, price_per_night, availability_status)
SELECT 
    hr.hotel_id,
    hr.room_id,
    date,
    hr.base_price * 
    CASE 
        -- Festival season premium (Diwali, New Year)
        WHEN EXTRACT(MONTH FROM date) IN (10, 11, 12) THEN 1.3 + random() * 0.3
        -- Summer season
        WHEN EXTRACT(MONTH FROM date) IN (4, 5, 6) THEN 1.1 + random() * 0.2
        -- Monsoon discount
        WHEN EXTRACT(MONTH FROM date) IN (7, 8) THEN 0.7 + random() * 0.2
        -- Regular season
        ELSE 1.0 + random() * 0.2
    END *
    -- Weekend premium
    CASE WHEN EXTRACT(DOW FROM date) IN (0, 6) THEN 1.2 ELSE 1.0 END as price_per_night,
    CASE 
        WHEN random() < 0.7 THEN 'available'
        WHEN random() < 0.9 THEN 'limited'
        ELSE 'sold_out'
    END as availability_status
FROM 
    hotel.hotel_rooms hr
CROSS JOIN 
    generate_series('2024-06-01'::date, '2024-11-30'::date, '1 day'::interval) as date;

-- ============================================
-- 8. USER SCHEMA - USERS
-- ============================================

INSERT INTO user_data.users (email, phone, registration_date, user_type)
SELECT 
    'user' || generate_series || '@example.com',
    '+91' || (7000000000 + floor(random() * 999999999)::bigint)::text,
    '2020-01-01'::date + (random() * 1700)::int,
    CASE 
        WHEN random() < 0.7 THEN 'regular'
        WHEN random() < 0.9 THEN 'premium'
        ELSE 'corporate'
    END
FROM generate_series(1, 1000);

-- ============================================
-- 9. MARKETING SCHEMA - CAMPAIGNS
-- ============================================

INSERT INTO marketing.campaigns (campaign_name, start_date, end_date, campaign_type, target_audience) VALUES
('Summer Sale 2024', '2024-04-01', '2024-06-30', 'email', 'Existing customers'),
('Google Ads - Beach Destinations', '2024-01-01', '2024-12-31', 'search_ads', 'Beach lovers'),
('Facebook - Heritage Hotels', '2024-01-01', '2024-12-31', 'social_media', 'Culture enthusiasts'),
('Diwali Special Offer', '2024-10-01', '2024-11-15', 'email', 'All users'),
('New Year Campaign', '2024-11-15', '2025-01-05', 'search_ads', 'Party travelers'),
('Instagram - Hill Stations', '2024-03-01', '2024-09-30', 'social_media', 'Adventure seekers'),
('Affiliate - Travel Bloggers', '2024-01-01', '2024-12-31', 'affiliate', 'Blog readers'),
('Corporate Travel Program', '2024-01-01', '2024-12-31', 'email', 'Business travelers'),
('Weekend Getaway Flash Sale', '2024-06-01', '2024-11-30', 'display_ads', 'Weekend travelers'),
('Monsoon Special', '2024-06-15', '2024-09-15', 'email', 'Monsoon lovers'),
('Festival Season Mega Sale', '2024-09-01', '2024-11-30', 'search_ads', 'Festival travelers'),
('Luxury Hotels Premium', '2024-01-01', '2024-12-31', 'display_ads', 'Luxury seekers');

-- ============================================
-- 10. MARKETING SCHEMA - MARKETING SPENDS
-- ============================================

-- Generate daily marketing spend for each campaign
INSERT INTO marketing.marketing_spends (campaign_id, date, spend, impressions, clicks, conversions)
SELECT 
    c.campaign_id,
    date,
    CASE c.campaign_type
        WHEN 'search_ads' THEN 50000 + random() * 100000
        WHEN 'display_ads' THEN 30000 + random() * 70000
        WHEN 'social_media' THEN 25000 + random() * 50000
        WHEN 'email' THEN 10000 + random() * 20000
        WHEN 'affiliate' THEN 40000 + random() * 60000
        ELSE 20000 + random() * 30000
    END as spend,
    CASE c.campaign_type
        WHEN 'search_ads' THEN (500000 + random() * 500000)::bigint
        WHEN 'display_ads' THEN (800000 + random() * 700000)::bigint
        WHEN 'social_media' THEN (1000000 + random() * 1000000)::bigint
        WHEN 'email' THEN (100000 + random() * 200000)::bigint
        ELSE (300000 + random() * 400000)::bigint
    END as impressions,
    CASE c.campaign_type
        WHEN 'search_ads' THEN (5000 + random() * 10000)::int
        WHEN 'display_ads' THEN (3000 + random() * 7000)::int
        WHEN 'social_media' THEN (8000 + random() * 12000)::int
        WHEN 'email' THEN (2000 + random() * 5000)::int
        ELSE (4000 + random() * 6000)::int
    END as clicks,
    (100 + random() * 400)::int as conversions
FROM 
    marketing.campaigns c
CROSS JOIN 
    generate_series(c.start_date, LEAST(c.end_date, '2024-11-30'::date), '1 day'::interval) as date;

-- ============================================
-- 11. USER SCHEMA - SEARCH QUERIES
-- ============================================

-- Generate 15,000 search queries over the last 6 months
INSERT INTO user_data.search_queries (user_id, session_id, destination, search_date, check_in_date, check_out_date, number_of_guests)
SELECT 
    (random() * 999 + 1)::int as user_id,
    'session_' || md5(random()::text),
    (ARRAY['Mumbai', 'Delhi', 'Bangalore', 'Goa', 'Jaipur', 'Kolkata', 'Chennai', 'Hyderabad', 'Pune', 'Ahmedabad', 
          'Udaipur', 'Shimla', 'Manali', 'Agra', 'Varanasi', 'Rishikesh', 'Mysore', 'Kochi', 'Amritsar', 'Darjeeling'])[floor(random() * 20 + 1)::int],
    search_timestamp,
    check_in,
    check_in + (random() * 10 + 2)::int,  -- Ensure checkout is 2-12 days after check-in
    (1 + random() * 5)::int
FROM 
    (SELECT 
        search_timestamp,
        search_timestamp::date + (random() * 60)::int as check_in
     FROM generate_series(
        '2024-06-01 00:00:00'::timestamp,
        '2024-11-30 23:59:59'::timestamp,
        interval '30 minutes'
     ) as search_timestamp
    ) sub
LIMIT 15000;

-- ============================================
-- 12. MARKETING SCHEMA - TRAFFIC SOURCES
-- ============================================

-- Generate traffic source for each search query
INSERT INTO marketing.traffic_sources (user_id, session_id, source, campaign_id, visit_date, referrer_url)
SELECT 
    sq.user_id,
    sq.session_id,
    (ARRAY['organic', 'paid_ads', 'email', 'social_media', 'direct', 'referral', 'affiliate'])[floor(random() * 7 + 1)::int] as source,
    CASE 
        WHEN random() < 0.4 THEN (SELECT campaign_id FROM marketing.campaigns ORDER BY random() LIMIT 1)
        ELSE NULL
    END as campaign_id,
    sq.search_date,
    CASE 
        WHEN random() < 0.6 THEN 'https://google.com/search?q=hotels+' || sq.destination
        WHEN random() < 0.8 THEN 'https://facebook.com/mmt'
        ELSE NULL
    END as referrer_url
FROM user_data.search_queries sq;

-- ============================================
-- 13. USER SCHEMA - HOTEL BOOKINGS
-- ============================================

-- Generate ~8,000 bookings (conversion rate ~5% from searches)
INSERT INTO user_data.hotel_bookings (user_id, hotel_id, room_id, booking_date, check_in_date, check_out_date, destination, amount_paid, booking_status, number_of_guests)
SELECT 
    sq.user_id,
    h.hotel_id,
    hr.room_id,
    sq.search_date + interval '1 hour' * random() * 48,
    sq.check_in_date,
    sq.check_out_date,
    sq.destination,
    -- Calculate total price with fallback to room base_price
    COALESCE(
        (SELECT 
            AVG(p.price_per_night) * (sq.check_out_date - sq.check_in_date)
         FROM hotel.pricing p 
         WHERE p.hotel_id = h.hotel_id 
         AND p.room_id = hr.room_id
         AND p.date BETWEEN sq.check_in_date AND sq.check_out_date - 1
        ),
        -- Fallback: use room base_price if no pricing data found
        hr.base_price * (sq.check_out_date - sq.check_in_date)
    ) * (0.9 + random() * 0.2) as amount_paid,  -- Add some price variation
    CASE 
        WHEN random() < 0.85 THEN 'confirmed'
        WHEN random() < 0.93 THEN 'completed'
        WHEN random() < 0.97 THEN 'cancelled'
        ELSE 'no_show'
    END as booking_status,
    sq.number_of_guests
FROM 
    user_data.search_queries sq
INNER JOIN 
    hotel.hotels h ON h.city = sq.destination
INNER JOIN 
    hotel.hotel_rooms hr ON hr.hotel_id = h.hotel_id
WHERE 
    random() < 0.05  -- 5% conversion rate from searches
    AND sq.check_in_date > '2024-06-01'
    AND sq.check_in_date IS NOT NULL
    AND sq.check_out_date IS NOT NULL
    AND sq.check_out_date > sq.check_in_date
LIMIT 8000;

-- ============================================
-- VERIFICATION QUERIES
-- ============================================

-- Uncomment to verify data counts

-- SELECT 'Cities' as table_name, COUNT(*) as record_count FROM external.cities
-- UNION ALL
-- SELECT 'Festivals', COUNT(*) FROM external.festivals
-- UNION ALL
-- SELECT 'Events', COUNT(*) FROM external.events
-- UNION ALL
-- SELECT 'External Factors', COUNT(*) FROM external.external_factors
-- UNION ALL
-- SELECT 'Hotels', COUNT(*) FROM hotel.hotels
-- UNION ALL
-- SELECT 'Hotel Rooms', COUNT(*) FROM hotel.hotel_rooms
-- UNION ALL
-- SELECT 'Pricing', COUNT(*) FROM hotel.pricing
-- UNION ALL
-- SELECT 'Users', COUNT(*) FROM user_data.users
-- UNION ALL
-- SELECT 'Hotel Bookings', COUNT(*) FROM user_data.hotel_bookings
-- UNION ALL
-- SELECT 'Search Queries', COUNT(*) FROM user_data.search_queries
-- UNION ALL
-- SELECT 'Campaigns', COUNT(*) FROM marketing.campaigns
-- UNION ALL
-- SELECT 'Marketing Spends', COUNT(*) FROM marketing.marketing_spends
-- UNION ALL
-- SELECT 'Traffic Sources', COUNT(*) FROM marketing.traffic_sources;


-- ============================================
-- SCENARIO: Users who visited but didn't search or book
-- ============================================

-- This represents bounce traffic - users who land on the site but don't engage

-- ============================================
-- APPROACH 1: Generate standalone traffic records
-- ============================================

-- Insert traffic sources for users who visited but never searched
-- These represent ~30-40% of all web traffic (typical bounce rate)

INSERT INTO marketing.traffic_sources (user_id, session_id, source, campaign_id, visit_date, referrer_url)
SELECT 
    CASE 
        -- 70% of bounce traffic is from non-logged-in users (NULL user_id)
        WHEN random() < 0.7 THEN NULL
        -- 30% are from existing users who just browsed
        ELSE (SELECT user_id FROM user_data.users ORDER BY random() LIMIT 1)
    END as user_id,
    'session_' || md5(random()::text || current_timestamp::text) as session_id,
    (ARRAY['organic', 'paid_ads', 'social_media', 'direct', 'referral'])[floor(random() * 5 + 1)::int] as source,
    CASE 
        WHEN random() < 0.3 THEN (SELECT campaign_id FROM marketing.campaigns ORDER BY random() LIMIT 1)
        ELSE NULL
    END as campaign_id,
    timestamp '2024-06-01 00:00:00' + random() * (timestamp '2024-11-30 23:59:59' - timestamp '2024-06-01 00:00:00') as visit_date,
    CASE 
        WHEN random() < 0.5 THEN 'https://google.com/search?q=hotels+in+india'
        WHEN random() < 0.7 THEN 'https://facebook.com/makemytrip'
        WHEN random() < 0.85 THEN 'https://instagram.com/explore'
        ELSE NULL
    END as referrer_url
FROM generate_series(1, 5000);  -- Generate 5000 bounce visits

-- ============================================
-- APPROACH 2: Generate users who registered but never engaged
-- ============================================

-- Insert users who signed up but never searched or booked
INSERT INTO user_data.users (email, phone, registration_date, user_type)
SELECT 
    'inactive_user' || generate_series || '@example.com',
    '+91' || (7000000000 + floor(random() * 999999999)::bigint)::text,
    '2020-01-01'::date + (random() * 1700)::int,
    'regular'  -- Inactive users are typically regular tier
FROM generate_series(1001, 1200);  -- Generate 200 inactive users

-- Now create traffic records for these inactive users showing they visited
INSERT INTO marketing.traffic_sources (user_id, session_id, source, campaign_id, visit_date, referrer_url)
SELECT 
    u.user_id,
    'session_' || md5(random()::text || u.user_id::text) as session_id,
    (ARRAY['organic', 'email', 'social_media', 'direct'])[floor(random() * 4 + 1)::int] as source,
    NULL as campaign_id,  -- Usually no campaign for these inactive users
    u.registration_date::timestamp + interval '1 hour' * random() * 24,  -- Visit shortly after registration
    CASE 
        WHEN random() < 0.6 THEN 'https://google.com/search?q=hotel+booking'
        ELSE NULL
    END as referrer_url
FROM user_data.users u
WHERE u.user_id BETWEEN 1001 AND 1200;  -- Only for the inactive users we just created

-- ============================================
-- APPROACH 3: Generate anonymous bounce traffic
-- ============================================

-- High-volume anonymous visitors (no user_id)
-- These represent people who land on homepage but leave immediately

INSERT INTO marketing.traffic_sources (user_id, session_id, source, campaign_id, visit_date, referrer_url)
SELECT 
    NULL as user_id,  -- Anonymous visitor
    'anon_session_' || md5(random()::text || generate_series::text) as session_id,
    -- Higher proportion of paid ads and social media for anonymous traffic
    (ARRAY['paid_ads', 'social_media', 'organic', 'display_ads', 'direct'])[
        CASE 
            WHEN random() < 0.35 THEN 1  -- 35% paid_ads
            WHEN random() < 0.60 THEN 2  -- 25% social_media
            WHEN random() < 0.80 THEN 3  -- 20% organic
            WHEN random() < 0.90 THEN 4  -- 10% display_ads
            ELSE 5                        -- 10% direct
        END
    ] as source,
    CASE 
        WHEN random() < 0.5 THEN (SELECT campaign_id FROM marketing.campaigns WHERE campaign_type IN ('paid_ads', 'social_media') ORDER BY random() LIMIT 1)
        ELSE NULL
    END as campaign_id,
    timestamp '2024-06-01 00:00:00' + random() * (timestamp '2024-11-30 23:59:59' - timestamp '2024-06-01 00:00:00') as visit_date,
    CASE 
        WHEN random() < 0.4 THEN 'https://google.com/search?q=cheap+hotels'
        WHEN random() < 0.6 THEN 'https://facebook.com/ads/hotel_deals'
        WHEN random() < 0.75 THEN 'https://instagram.com/explore/travel'
        ELSE NULL
    END as referrer_url
FROM generate_series(1, 10000);  -- Generate 10,000 anonymous bounce visits

-- ============================================
-- APPROACH 4: Window shoppers - Multiple visits but no conversion
-- ============================================

-- Users who visit multiple times but never search or book
WITH window_shoppers AS (
    SELECT user_id
    FROM user_data.users 
    WHERE user_id BETWEEN 1 AND 1000
    ORDER BY random()
    LIMIT 100  -- 100 window shoppers
)
INSERT INTO marketing.traffic_sources (user_id, session_id, source, campaign_id, visit_date, referrer_url)
SELECT 
    ws.user_id,
    'session_' || md5(random()::text || ws.user_id::text || visit_num::text) as session_id,
    (ARRAY['direct', 'organic', 'email'])[floor(random() * 3 + 1)::int] as source,
    NULL as campaign_id,
    timestamp '2024-06-01' + (random() * interval '180 days') + (visit_num * interval '3 days') as visit_date,
    CASE 
        WHEN random() < 0.7 THEN 'https://makemytrip.com'
        ELSE 'https://google.com/search?q=hotel+booking+sites'
    END as referrer_url
FROM window_shoppers ws
CROSS JOIN generate_series(1, 5) as visit_num;  -- Each window shopper visits 5 times

-- ============================================
-- VERIFICATION QUERIES
-- ============================================

-- Check users who visited but never searched
SELECT 
    COUNT(DISTINCT ts.user_id) as users_visited_no_search
FROM marketing.traffic_sources ts
LEFT JOIN user_data.search_queries sq ON ts.user_id = sq.user_id
WHERE sq.user_id IS NULL
AND ts.user_id IS NOT NULL;

-- Check anonymous traffic (visited but no user_id)
SELECT 
    COUNT(*) as anonymous_visits,
    source,
    COUNT(*) * 100.0 / SUM(COUNT(*)) OVER () as percentage
FROM marketing.traffic_sources
WHERE user_id IS NULL
GROUP BY source
ORDER BY anonymous_visits DESC;

-- Overall conversion funnel analysis
SELECT 
    'Total Visits' as stage,
    COUNT(*) as count
FROM marketing.traffic_sources
UNION ALL
SELECT 
    'Users Who Searched',
    COUNT(DISTINCT user_id)
FROM user_data.search_queries
UNION ALL
SELECT 
    'Users Who Booked',
    COUNT(DISTINCT user_id)
FROM user_data.hotel_bookings;

-- Bounce rate by traffic source
SELECT 
    ts.source,
    COUNT(DISTINCT ts.session_id) as total_sessions,
    COUNT(DISTINCT sq.session_id) as sessions_with_search,
    ROUND(
        (COUNT(DISTINCT ts.session_id) - COUNT(DISTINCT sq.session_id)) * 100.0 / 
        COUNT(DISTINCT ts.session_id), 
        2
    ) as bounce_rate_percentage
FROM marketing.traffic_sources ts
LEFT JOIN user_data.search_queries sq ON ts.session_id = sq.session_id
GROUP BY ts.source
ORDER BY bounce_rate_percentage DESC;

-- Users by engagement level
WITH user_engagement AS (
    SELECT 
        u.user_id,
        u.email,
        u.registration_date,
        COUNT(DISTINCT ts.session_id) as visit_count,
        COUNT(DISTINCT sq.query_id) as search_count,
        COUNT(DISTINCT hb.booking_id) as booking_count
    FROM user_data.users u
    LEFT JOIN marketing.traffic_sources ts ON u.user_id = ts.user_id
    LEFT JOIN user_data.search_queries sq ON u.user_id = sq.user_id
    LEFT JOIN user_data.hotel_bookings hb ON u.user_id = hb.user_id
    GROUP BY u.user_id, u.email, u.registration_date
)
SELECT 
    CASE 
        WHEN booking_count > 0 THEN 'Converters'
        WHEN search_count > 0 THEN 'Searchers (No Booking)'
        WHEN visit_count > 0 THEN 'Visitors Only (No Search)'
        ELSE 'Registered (Never Visited)'
    END as user_segment,
    COUNT(*) as user_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) as percentage
FROM user_engagement
GROUP BY 
    CASE 
        WHEN booking_count > 0 THEN 'Converters'
        WHEN search_count > 0 THEN 'Searchers (No Booking)'
        WHEN visit_count > 0 THEN 'Visitors Only (No Search)'
        ELSE 'Registered (Never Visited)'
    END
ORDER BY user_count DESC;

-- ============================================
-- ANALYTICAL QUERIES FOR "VISITED BUT DIDN'T ENGAGE"
-- ============================================

-- Find all traffic that didn't result in a search
SELECT 
    ts.source,
    ts.campaign_id,
    DATE(ts.visit_date) as visit_date,
    COUNT(*) as bounced_visits,
    COUNT(DISTINCT ts.user_id) FILTER (WHERE ts.user_id IS NOT NULL) as registered_users_bounced,
    COUNT(*) FILTER (WHERE ts.user_id IS NULL) as anonymous_bounced
FROM marketing.traffic_sources ts
LEFT JOIN user_data.search_queries sq ON ts.session_id = sq.session_id
WHERE sq.session_id IS NULL  -- No search query for this session
GROUP BY ts.source, ts.campaign_id, DATE(ts.visit_date)
ORDER BY visit_date DESC, bounced_visits DESC
LIMIT 50;

-- Campaign performance including bounce data
SELECT 
    c.campaign_name,
    c.campaign_type,
    COUNT(DISTINCT ts.session_id) as total_sessions,
    COUNT(DISTINCT sq.session_id) as sessions_with_search,
    COUNT(DISTINCT hb.booking_id) as sessions_with_booking,
    ROUND(
        COUNT(DISTINCT sq.session_id) * 100.0 / NULLIF(COUNT(DISTINCT ts.session_id), 0),
        2
    ) as search_rate,
    ROUND(
        COUNT(DISTINCT hb.booking_id) * 100.0 / NULLIF(COUNT(DISTINCT ts.session_id), 0),
        2
    ) as conversion_rate
FROM marketing.campaigns c
LEFT JOIN marketing.traffic_sources ts ON c.campaign_id = ts.campaign_id
LEFT JOIN user_data.search_queries sq ON ts.session_id = sq.session_id
LEFT JOIN user_data.hotel_bookings hb ON sq.user_id = hb.user_id 
    AND hb.booking_date::date BETWEEN sq.search_date::date AND sq.search_date::date + 7
WHERE ts.visit_date BETWEEN '2024-06-01' AND '2024-11-30'
GROUP BY c.campaign_id, c.campaign_name, c.campaign_type
ORDER BY total_sessions DESC;