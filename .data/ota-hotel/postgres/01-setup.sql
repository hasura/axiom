CREATE DATABASE ota_hotel;

\c ota_hotel;

-- ============================================
-- SCHEMA CREATION
-- ============================================

CREATE SCHEMA IF NOT EXISTS hotel;
CREATE SCHEMA IF NOT EXISTS user_data;
CREATE SCHEMA IF NOT EXISTS marketing;
CREATE SCHEMA IF NOT EXISTS external;

-- ============================================
-- EXTERNAL SCHEMA TABLES
-- ============================================
-- Creating this first as other tables reference cities

CREATE TABLE external.cities (
    city_id SERIAL PRIMARY KEY,
    city_name VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL DEFAULT 'India',
    timezone VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_cities_name ON external.cities(city_name);
CREATE INDEX idx_cities_state ON external.cities(state);

CREATE TABLE external.external_factors (
    factor_id SERIAL PRIMARY KEY,
    city_id INTEGER NOT NULL,
    date DATE NOT NULL,
    weather_condition VARCHAR(50),
    temperature DECIMAL(5,2),
    flight_availability_score INTEGER CHECK (flight_availability_score BETWEEN 0 AND 100),
    travel_advisory_level VARCHAR(20) CHECK (travel_advisory_level IN ('green', 'yellow', 'orange', 'red')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (city_id) REFERENCES external.cities(city_id) ON DELETE CASCADE,
    UNIQUE(city_id, date)
);

CREATE INDEX idx_external_factors_city_date ON external.external_factors(city_id, date);
CREATE INDEX idx_external_factors_date ON external.external_factors(date);

CREATE TABLE external.events (
    event_id SERIAL PRIMARY KEY,
    city_id INTEGER NOT NULL,
    event_name VARCHAR(200) NOT NULL,
    event_date DATE NOT NULL,
    event_type VARCHAR(50),
    expected_attendance INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (city_id) REFERENCES external.cities(city_id) ON DELETE CASCADE
);

CREATE INDEX idx_events_city_date ON external.events(city_id, event_date);
CREATE INDEX idx_events_date ON external.events(event_date);

CREATE TABLE external.festivals (
    festival_id SERIAL PRIMARY KEY,
    city_id INTEGER NOT NULL,
    festival_name VARCHAR(200) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    festival_type VARCHAR(50) CHECK (festival_type IN ('religious', 'cultural', 'music', 'food', 'sports', 'other')),
    significance_level VARCHAR(20) CHECK (significance_level IN ('local', 'regional', 'national', 'international')),
    expected_tourist_influx INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (city_id) REFERENCES external.cities(city_id) ON DELETE CASCADE,
    CHECK (end_date >= start_date)
);

CREATE INDEX idx_festivals_city_dates ON external.festivals(city_id, start_date, end_date);
CREATE INDEX idx_festivals_dates ON external.festivals(start_date, end_date);

-- ============================================
-- HOTEL SCHEMA TABLES
-- ============================================

CREATE TABLE hotel.hotels (
    hotel_id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    star_rating DECIMAL(2,1) CHECK (star_rating BETWEEN 0 AND 5),
    address TEXT,
    amenities TEXT[],
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_hotels_city ON hotel.hotels(city);
CREATE INDEX idx_hotels_state ON hotel.hotels(state);
CREATE INDEX idx_hotels_star_rating ON hotel.hotels(star_rating);

CREATE TABLE hotel.hotel_rooms (
    room_id SERIAL PRIMARY KEY,
    hotel_id INTEGER NOT NULL,
    room_type VARCHAR(50) NOT NULL,
    capacity INTEGER NOT NULL CHECK (capacity > 0),
    base_price DECIMAL(10,2) NOT NULL CHECK (base_price >= 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (hotel_id) REFERENCES hotel.hotels(hotel_id) ON DELETE CASCADE
);

CREATE INDEX idx_hotel_rooms_hotel_id ON hotel.hotel_rooms(hotel_id);
CREATE INDEX idx_hotel_rooms_type ON hotel.hotel_rooms(room_type);

CREATE TABLE hotel.pricing (
    pricing_id SERIAL PRIMARY KEY,
    hotel_id INTEGER NOT NULL,
    room_id INTEGER,
    date DATE NOT NULL,
    price_per_night DECIMAL(10,2) NOT NULL CHECK (price_per_night >= 0),
    availability_status VARCHAR(20) CHECK (availability_status IN ('available', 'limited', 'sold_out')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (hotel_id) REFERENCES hotel.hotels(hotel_id) ON DELETE CASCADE,
    FOREIGN KEY (room_id) REFERENCES hotel.hotel_rooms(room_id) ON DELETE CASCADE,
    UNIQUE(hotel_id, room_id, date)
);

CREATE INDEX idx_pricing_hotel_date ON hotel.pricing(hotel_id, date);
CREATE INDEX idx_pricing_room_date ON hotel.pricing(room_id, date);
CREATE INDEX idx_pricing_date ON hotel.pricing(date);

-- ============================================
-- USER SCHEMA TABLES
-- ============================================

CREATE TABLE user_data.users (
    user_id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20),
    registration_date DATE NOT NULL DEFAULT CURRENT_DATE,
    user_type VARCHAR(20) CHECK (user_type IN ('regular', 'premium', 'corporate')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON user_data.users(email);
CREATE INDEX idx_users_registration_date ON user_data.users(registration_date);

CREATE TABLE user_data.hotel_bookings (
    booking_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    hotel_id INTEGER NOT NULL,
    room_id INTEGER,
    booking_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    check_in_date DATE NOT NULL,
    check_out_date DATE NOT NULL,
    destination VARCHAR(100) NOT NULL,
    amount_paid DECIMAL(10,2) NOT NULL CHECK (amount_paid >= 0),
    booking_status VARCHAR(20) CHECK (booking_status IN ('confirmed', 'cancelled', 'completed', 'no_show')),
    number_of_guests INTEGER CHECK (number_of_guests > 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user_data.users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (hotel_id) REFERENCES hotel.hotels(hotel_id) ON DELETE RESTRICT,
    FOREIGN KEY (room_id) REFERENCES hotel.hotel_rooms(room_id) ON DELETE RESTRICT,
    CHECK (check_out_date > check_in_date)
);

CREATE INDEX idx_bookings_user_id ON user_data.hotel_bookings(user_id);
CREATE INDEX idx_bookings_hotel_id ON user_data.hotel_bookings(hotel_id);
CREATE INDEX idx_bookings_dates ON user_data.hotel_bookings(check_in_date, check_out_date);
CREATE INDEX idx_bookings_booking_date ON user_data.hotel_bookings(booking_date);
CREATE INDEX idx_bookings_status ON user_data.hotel_bookings(booking_status);

CREATE TABLE user_data.search_queries (
    query_id SERIAL PRIMARY KEY,
    user_id INTEGER,
    session_id VARCHAR(100),
    destination VARCHAR(100) NOT NULL,
    search_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    check_in_date DATE,
    check_out_date DATE,
    number_of_guests INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user_data.users(user_id) ON DELETE SET NULL,
    CHECK (check_out_date IS NULL OR check_in_date IS NULL OR check_out_date > check_in_date)
);

CREATE INDEX idx_search_queries_user_id ON user_data.search_queries(user_id);
CREATE INDEX idx_search_queries_destination ON user_data.search_queries(destination);
CREATE INDEX idx_search_queries_search_date ON user_data.search_queries(search_date);
CREATE INDEX idx_search_queries_session_id ON user_data.search_queries(session_id);

-- ============================================
-- MARKETING SCHEMA TABLES
-- ============================================

CREATE TABLE marketing.campaigns (
    campaign_id SERIAL PRIMARY KEY,
    campaign_name VARCHAR(200) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE,
    campaign_type VARCHAR(50) CHECK (campaign_type IN ('email', 'social_media', 'search_ads', 'display_ads', 'affiliate', 'other')),
    target_audience TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CHECK (end_date IS NULL OR end_date >= start_date)
);

CREATE INDEX idx_campaigns_dates ON marketing.campaigns(start_date, end_date);
CREATE INDEX idx_campaigns_type ON marketing.campaigns(campaign_type);

CREATE TABLE marketing.marketing_spends (
    spend_id SERIAL PRIMARY KEY,
    campaign_id INTEGER NOT NULL,
    date DATE NOT NULL,
    spend DECIMAL(12,2) NOT NULL CHECK (spend >= 0),
    impressions BIGINT CHECK (impressions >= 0),
    clicks INTEGER CHECK (clicks >= 0),
    conversions INTEGER CHECK (conversions >= 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (campaign_id) REFERENCES marketing.campaigns(campaign_id) ON DELETE CASCADE,
    UNIQUE(campaign_id, date)
);

CREATE INDEX idx_marketing_spends_campaign_date ON marketing.marketing_spends(campaign_id, date);
CREATE INDEX idx_marketing_spends_date ON marketing.marketing_spends(date);

CREATE TABLE marketing.traffic_sources (
    traffic_id SERIAL PRIMARY KEY,
    user_id INTEGER,
    session_id VARCHAR(100) NOT NULL,
    source VARCHAR(50) NOT NULL CHECK (source IN ('organic', 'paid_ads', 'email', 'social_media', 'direct', 'referral', 'affiliate')),
    campaign_id INTEGER,
    visit_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    referrer_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user_data.users(user_id) ON DELETE SET NULL,
    FOREIGN KEY (campaign_id) REFERENCES marketing.campaigns(campaign_id) ON DELETE SET NULL
);

CREATE INDEX idx_traffic_sources_user_id ON marketing.traffic_sources(user_id);
CREATE INDEX idx_traffic_sources_session_id ON marketing.traffic_sources(session_id);
CREATE INDEX idx_traffic_sources_source ON marketing.traffic_sources(source);
CREATE INDEX idx_traffic_sources_campaign_id ON marketing.traffic_sources(campaign_id);
CREATE INDEX idx_traffic_sources_visit_date ON marketing.traffic_sources(visit_date);

-- ============================================
-- UPDATED_AT TRIGGER FUNCTION
-- ============================================

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply triggers to all tables with updated_at column
CREATE TRIGGER update_cities_updated_at BEFORE UPDATE ON external.cities
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_external_factors_updated_at BEFORE UPDATE ON external.external_factors
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_events_updated_at BEFORE UPDATE ON external.events
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_festivals_updated_at BEFORE UPDATE ON external.festivals
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_hotels_updated_at BEFORE UPDATE ON hotel.hotels
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_hotel_rooms_updated_at BEFORE UPDATE ON hotel.hotel_rooms
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_pricing_updated_at BEFORE UPDATE ON hotel.pricing
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON user_data.users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_hotel_bookings_updated_at BEFORE UPDATE ON user_data.hotel_bookings
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_campaigns_updated_at BEFORE UPDATE ON marketing.campaigns
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_marketing_spends_updated_at BEFORE UPDATE ON marketing.marketing_spends
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- COMMENTS FOR DOCUMENTATION
-- ============================================

COMMENT ON SCHEMA hotel IS 'Schema containing hotel-related entities and pricing information';
COMMENT ON SCHEMA user_data IS 'Schema containing user profiles, bookings, and search behavior';
COMMENT ON SCHEMA marketing IS 'Schema containing marketing campaigns, spends, and traffic sources';
COMMENT ON SCHEMA external IS 'Schema containing external factors like weather, events, and festivals';

COMMENT ON TABLE hotel.hotels IS 'Master table for hotel information';
COMMENT ON TABLE hotel.hotel_rooms IS 'Room inventory for each hotel';
COMMENT ON TABLE hotel.pricing IS 'Historical and current pricing data for hotel rooms';
COMMENT ON TABLE user_data.users IS 'User profile information';
COMMENT ON TABLE user_data.hotel_bookings IS 'All hotel bookings made through the platform';
COMMENT ON TABLE user_data.search_queries IS 'User search behavior tracking';
COMMENT ON TABLE marketing.campaigns IS 'Marketing campaign metadata';
COMMENT ON TABLE marketing.marketing_spends IS 'Daily marketing spend and performance metrics';
COMMENT ON TABLE marketing.traffic_sources IS 'Web and app traffic attribution';
COMMENT ON TABLE external.cities IS 'Master list of cities';
COMMENT ON TABLE external.external_factors IS 'External factors affecting travel demand';
COMMENT ON TABLE external.events IS 'Local events that may impact hotel demand';
COMMENT ON TABLE external.festivals IS 'Festivals and celebrations affecting travel patterns';