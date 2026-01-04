use crate::config::Config;
use crate::demand::DemandCalculator;
use crate::holidays::generate_all_holidays;
use crate::models::*;
use crate::streaming::StreamingWriters;
use anyhow::Result;
use chrono::{Datelike, Duration, NaiveDate, NaiveDateTime, Timelike};
use rand::prelude::*;
use rand_distr::{Distribution, Exp, LogNormal, Beta, Normal};
use std::collections::HashMap;
use std::path::Path;
use indicatif::{ProgressBar, ProgressStyle};

// ============================================================================
// BEHAVIORAL CONSTANTS
// These control the realism of generated data but are not user-configurable
// ============================================================================

// Store assortment coverage by type
const ONLINE_COVERAGE: f64 = 1.0;      // 100% - online has everything
const BIG_BOX_COVERAGE: f64 = 0.9;     // 90% of products
const SUBURBAN_COVERAGE: f64 = 0.7;    // 70% of products
const URBAN_COVERAGE: f64 = 0.7;       // 70% of products
const CONVENIENCE_COVERAGE: f64 = 0.7; // 70% of products

// Customer demographics distribution
const AGE_18_24: f64 = 0.12;
const AGE_25_34: f64 = 0.22;
const AGE_35_44: f64 = 0.20;
const AGE_45_54: f64 = 0.18;
const AGE_55_64: f64 = 0.15;
const AGE_65_PLUS: f64 = 0.13;

const HOUSEHOLD_SIZE_1: f64 = 0.28;
const HOUSEHOLD_SIZE_2: f64 = 0.34;
const HOUSEHOLD_SIZE_3: f64 = 0.18;
const HOUSEHOLD_SIZE_4: f64 = 0.12;
const HOUSEHOLD_SIZE_5_PLUS: f64 = 0.08;

const INCOME_LOW: f64 = 0.25;
const INCOME_MEDIUM: f64 = 0.40;
const INCOME_HIGH: f64 = 0.25;
const INCOME_VERY_HIGH: f64 = 0.10;

// Customer segment distribution
const SEGMENT_FREQUENT_SHOPPER: f64 = 0.20;
const SEGMENT_WEEKLY_SHOPPER: f64 = 0.40;
const SEGMENT_BULK_BUYER: f64 = 0.15;
const SEGMENT_OCCASIONAL: f64 = 0.25;



// Transaction tracking rates by store type
// Loyalty program penetration over time
const LOYALTY_PENETRATION_2019: f64 = 0.10;
const LOYALTY_PENETRATION_2020: f64 = 0.20;
const LOYALTY_PENETRATION_2021: f64 = 0.28;
const LOYALTY_PENETRATION_2022: f64 = 0.33;
const LOYALTY_PENETRATION_2023: f64 = 0.36;
const LOYALTY_PENETRATION_2024: f64 = 0.38;
const LOYALTY_PENETRATION_2025: f64 = 0.38;

// Delivery configuration
const DRIVERS_PER_STORE_URBAN: usize = 6;
const DRIVERS_PER_STORE_SUBURBAN: usize = 5;
const DRIVERS_PER_STORE_BIG_BOX: usize = 8;
const DRIVERS_PER_STORE_CONVENIENCE: usize = 2;
const DRIVERS_FULFILLMENT_CENTER: usize = 50;

const EMPLOYEE_DRIVER_PCT: f64 = 0.30;
const CONTRACTOR_DRIVER_PCT: f64 = 0.60;
const THIRD_PARTY_DRIVER_PCT: f64 = 0.10;

// ============================================================================
// NAME AND ADDRESS DATA
// Comprehensive lists for realistic data generation
// ============================================================================

// First names - mix of traditional and modern, diverse backgrounds
const FIRST_NAMES: &[&str] = &[
    // Traditional American
    "James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda",
    "William", "Barbara", "David", "Elizabeth", "Richard", "Susan", "Joseph", "Jessica",
    "Thomas", "Sarah", "Charles", "Karen", "Christopher", "Nancy", "Daniel", "Lisa",
    "Matthew", "Betty", "Anthony", "Margaret", "Mark", "Sandra", "Adam", "Ashley",
    "Steven", "Kimberly", "Paul", "Emily", "Andrew", "Donna", "Joshua", "Michelle",
    "Kenneth", "Dorothy", "Kevin", "Carol", "Brian", "Amanda", "George", "Melissa",
    "Timothy", "Deborah", "Ronald", "Stephanie", "Edward", "Rebecca", "Jason", "Sharon",
    "Jeffrey", "Laura", "Ryan", "Cynthia", "Jacob", "Kathleen", "Gary", "Amy",
    "Nicholas", "Angela", "Eric", "Shirley", "Jonathan", "Anna", "Stephen", "Brenda",
    // Hispanic/Latino
    "Carlos", "Maria", "Miguel", "Rosa", "Luis", "Carmen", "Jose", "Sofia",
    "Juan", "Isabella", "Francisco", "Gabriela", "Antonio", "Valentina", "Alejandro", "Lucia",
    "Diego", "Camila", "Rafael", "Mariana", "Fernando", "Elena", "Ricardo", "Paula",
    "Javier", "Andrea", "Oscar", "Daniela", "Sergio", "Natalia", "Eduardo", "Victoria",
    // Asian
    "Wei", "Mei", "Chen", "Li", "Hiroshi", "Yuki", "Kenji", "Sakura",
    "Raj", "Priya", "Amit", "Ananya", "Vikas", "Deepa", "Arjun", "Kavya",
    "Jin", "Hana", "Min", "Soo", "Tae", "Ji", "Hyun", "Eun",
    "Nguyen", "Linh", "Minh", "Tran", "Phong", "Mai", "Duc", "Thao",
    // Modern/Unisex
    "Alex", "Jordan", "Taylor", "Morgan", "Casey", "Riley", "Avery", "Quinn",
    "Skylar", "Dakota", "Reese", "Peyton", "Cameron", "Sage", "River", "Phoenix",
    "Blake", "Drew", "Finley", "Harper", "Hayden", "Logan", "Parker", "Spencer",
    // Additional diverse names
    "Omar", "Fatima", "Ahmed", "Aisha", "Malik", "Zara", "Darius", "Imani",
    "Marcus", "Jasmine", "Isaiah", "Aaliyah", "Terrell", "Ebony", "DeShawn", "Keisha",
    "Connor", "Molly", "Sean", "Bridget", "Patrick", "Siobhan", "Declan", "Fiona",
    "Dmitri", "Natasha", "Ivan", "Olga", "Mikhail", "Anastasia", "Vladimir", "Yelena",
];

// Last names - diverse mix reflecting US demographics
const LAST_NAMES: &[&str] = &[
    // Common American
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Miller", "Davis", "Wilson",
    "Moore", "Taylor", "Anderson", "Thomas", "Jackson", "White", "Harris", "Martin",
    "Thompson", "Robinson", "Clark", "Lewis", "Lee", "Walker", "Hall", "Allen",
    "Young", "King", "Wright", "Scott", "Green", "Baker", "Adams", "Nelson",
    "Hill", "Campbell", "Mitchell", "Roberts", "Carter", "Phillips", "Evans", "Turner",
    "Collins", "Edwards", "Stewart", "Morris", "Murphy", "Cook", "Rogers", "Morgan",
    "Peterson", "Cooper", "Reed", "Bailey", "Bell", "Howard", "Ward", "Cox",
    // Hispanic/Latino
    "Garcia", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Perez", "Sanchez",
    "Ramirez", "Torres", "Flores", "Rivera", "Gomez", "Diaz", "Reyes", "Morales",
    "Jimenez", "Ruiz", "Ortiz", "Gutierrez", "Chavez", "Mendoza", "Vasquez", "Castillo",
    "Cruz", "Moreno", "Romero", "Herrera", "Medina", "Aguilar", "Vargas", "Fernandez",
    // Asian
    "Chen", "Wang", "Li", "Zhang", "Liu", "Yang", "Huang", "Wu",
    "Kim", "Park", "Lee", "Choi", "Jung", "Kang", "Cho", "Yoon",
    "Nguyen", "Tran", "Le", "Pham", "Hoang", "Vo", "Dang", "Bui",
    "Patel", "Shah", "Kumar", "Singh", "Sharma", "Gupta", "Joshi", "Mehta",
    "Tanaka", "Suzuki", "Yamamoto", "Watanabe", "Nakamura", "Sato", "Ito", "Kobayashi",
    // European
    "O'Brien", "O'Connor", "Murphy", "Kelly", "Sullivan", "Walsh", "Burke", "Ryan",
    "Schmidt", "Schneider", "Fischer", "Weber", "Meyer", "Wagner", "Becker", "Hoffmann",
    "Rossi", "Russo", "Ferrari", "Romano", "Colombo", "Ricci", "Marino", "Greco",
    "Cohen", "Levy", "Friedman", "Goldstein", "Schwartz", "Weiss", "Shapiro", "Katz",
    // African/African-American
    "Washington", "Jefferson", "Franklin", "Lincoln", "Grant", "Freeman", "Brooks", "Price",
    "Powell", "Russell", "Foster", "Butler", "Barnes", "Henderson", "Coleman", "Jenkins",
];

// Street names for address generation
const STREET_NAMES: &[&str] = &[
    "Main St", "Oak Ave", "Maple Dr", "Pine Rd", "Cedar Ln", "Elm St",
    "Washington Blvd", "Park Ave", "Broadway", "Market St", "1st St", "2nd Ave",
    "3rd St", "4th Ave", "5th St", "Church St", "High St", "Mill Rd",
    "Lake Dr", "Forest Ave", "River Rd", "Spring St", "Valley View Dr", "Sunset Blvd",
    "Highland Ave", "Meadow Ln", "Hillside Dr", "Chestnut St", "Walnut St", "Cherry Ln",
    "Lincoln Ave", "Jefferson St", "Madison Ave", "Franklin Blvd", "Grant St", "Adams Rd",
    "Central Ave", "Union St", "Liberty St", "Commerce Dr", "Industrial Blvd", "Tech Way",
    "College Ave", "University Dr", "School St", "Academy Rd", "Campus Dr", "Stadium Way",
];

// Apartment/unit type prefixes
const APARTMENT_TYPES: &[&str] = &["Apt", "Unit", "#", "Suite", "Flat", "Ste"];

// Email domains
const EMAIL_DOMAINS: &[&str] = &[
    "gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "icloud.com", "aol.com",
    "protonmail.com", "mail.com", "zoho.com", "yandex.com", "gmx.com", "live.com",
];

// US area codes (California focus but includes others for realism)
const AREA_CODES: &[u32] = &[
    // California
    415, 510, 650, 408, 925, 707, 209, 559, 916, 530, 831, 805, 818, 310, 213, 323,
    // Other major US cities
    212, 718, 646, // NYC
    312, 773, // Chicago
    713, 832, // Houston
    602, 480, // Phoenix
    215, 267, // Philadelphia
    214, 972, // Dallas
    404, 678, // Atlanta
    305, 786, // Miami
    206, 425, // Seattle
    303, 720, // Denver
];

// City to zip code prefix mapping for realistic addresses
// Format: (city_substring, zip_prefix, zip_range_start, zip_range_end)
// Zip codes will be generated as prefix + random(range_start..range_end)
const CITY_ZIP_CODES: &[(&str, &str, u32, u32)] = &[
    // Bay Area - California
    ("San Francisco", "941", 0, 99),
    ("San Jose", "951", 0, 99),
    ("Oakland", "946", 0, 99),
    ("Berkeley", "947", 0, 99),
    ("Palo Alto", "943", 0, 99),
    ("Mountain View", "940", 40, 49),
    ("Fremont", "945", 36, 39),
    ("San Mateo", "944", 0, 99),
    ("Redwood City", "940", 61, 65),
    ("Sunnyvale", "940", 85, 89),
    ("Santa Clara", "950", 50, 56),
    ("Cupertino", "950", 14, 16),
    ("Daly City", "940", 14, 17),
    ("San Rafael", "949", 0, 15),
    ("Walnut Creek", "945", 95, 98),
    // Greater California
    ("Sacramento", "958", 0, 99),
    ("Los Angeles", "900", 0, 99),
    ("San Diego", "921", 0, 99),
    ("Fresno", "937", 0, 99),
    ("Santa Rosa", "954", 0, 99),
    ("Monterey", "939", 0, 99),
    ("Santa Cruz", "950", 60, 67),
    ("Napa", "945", 58, 59),
    ("Stockton", "952", 0, 99),
    ("Modesto", "953", 50, 59),
    // Pacific Northwest
    ("Seattle", "981", 0, 99),
    ("Portland", "972", 0, 99),
    ("Bellevue", "980", 0, 99),
    ("Tacoma", "984", 0, 99),
    ("Eugene", "974", 0, 99),
    ("Spokane", "992", 0, 99),
    ("Boise", "837", 0, 99),
    // Southwest
    ("Phoenix", "850", 0, 99),
    ("Denver", "802", 0, 99),
    ("Las Vegas", "891", 0, 99),
    ("Tucson", "857", 0, 99),
    ("Albuquerque", "871", 0, 99),
    ("Salt Lake City", "841", 0, 99),
    ("Colorado Springs", "809", 0, 99),
    // Texas
    ("Austin", "787", 0, 99),
    ("Dallas", "752", 0, 99),
    ("Houston", "770", 0, 99),
    // East Coast
    ("New York", "100", 0, 99),
    ("Boston", "021", 0, 99),
    ("Chicago", "606", 0, 99),
    ("Miami", "331", 0, 99),
    ("Atlanta", "303", 0, 99),
    ("Philadelphia", "191", 0, 99),
    ("Washington", "200", 0, 99),
    // International (use local formats)
    ("Toronto", "M5", 0, 0),      // Canadian postal codes handled specially
    ("Vancouver", "V6", 0, 0),
    ("London", "SW", 0, 0),       // UK postal codes handled specially
    ("Manchester", "M1", 0, 0),
];

/// Extract state/province/country code from city string (e.g., "San Francisco, CA" -> "CA")
fn get_state_from_city(city: &str) -> String {
    // City format is typically "City Name, ST" or "City Name, ST (description)"
    if let Some(comma_pos) = city.find(',') {
        let after_comma = city[comma_pos + 1..].trim();
        // Take the first word/code after the comma
        let state = after_comma.split_whitespace().next().unwrap_or("CA");
        // Handle special cases for international
        if city.contains("Toronto") || city.contains("Vancouver") {
            return "ON".to_string(); // Ontario / BC simplified
        }
        if city.contains("London") || city.contains("Manchester") {
            return "UK".to_string();
        }
        return state.to_string();
    }
    "CA".to_string() // Default
}

/// Get a realistic zip code for a city
fn get_zip_for_city(city: &str, rng: &mut impl Rng) -> String {
    // Find matching city
    for (city_match, prefix, range_start, range_end) in CITY_ZIP_CODES {
        if city.contains(city_match) {
            // Handle international postal codes
            if *city_match == "Toronto" || *city_match == "Vancouver" {
                // Canadian postal code format: A1A 1A1
                let letters = ['A', 'B', 'C', 'E', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'R', 'S', 'T', 'V', 'W', 'X', 'Y'];
                return format!("{}{}{} {}{}{}",
                    prefix,
                    letters[rng.gen_range(0..letters.len())],
                    rng.gen_range(0..10),
                    rng.gen_range(0..10),
                    letters[rng.gen_range(0..letters.len())],
                    rng.gen_range(0..10));
            }
            if *city_match == "London" || *city_match == "Manchester" {
                // UK postal code format: XX## #XX
                return format!("{}{} {}{}{}",
                    prefix,
                    rng.gen_range(1..20),
                    rng.gen_range(1..10),
                    ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'R', 'S', 'T', 'W', 'X', 'Y'][rng.gen_range(0..20)],
                    ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'R', 'S', 'T', 'W', 'X', 'Y'][rng.gen_range(0..20)]);
            }
            // US zip code
            let suffix = rng.gen_range(*range_start..=*range_end);
            return format!("{}{:02}", prefix, suffix);
        }
    }
    // Fallback: California zip code
    format!("9{:04}", rng.gen_range(4000..4999))
}

pub struct ShelfWiseDataGenerator {
    rng: StdRng,
    config: Config,
    start_date: NaiveDate,
    end_date: NaiveDate,
    dates: Vec<NaiveDate>,
    products: Vec<Product>,
    stores: Vec<Store>,
    store_economics: HashMap<u32, StoreEconomics>,
    calendar: HashMap<NaiveDate, Calendar>,
    promotions: Vec<Promotion>,
    assortment: Vec<Assortment>,
    ground_truth_events: Vec<GroundTruthEvent>,
    holidays: HashMap<String, HashMap<u32, HashMap<String, NaiveDate>>>,
    categories: HashMap<String, CategoryConfig>,
    brands: Vec<BrandInfo>,
    suppliers: Vec<Supplier>,

    // Customer data
    customers: Vec<Customer>,
    customer_addresses: Vec<CustomerAddress>,

    // Delivery data
    delivery_drivers: Vec<DeliveryDriver>,
    delivery_zones: Vec<DeliveryZone>,
}

impl ShelfWiseDataGenerator {
    // Helper to round currency to 2 decimal places
    fn round_currency(value: f64) -> f64 {
        (value * 100.0).round() / 100.0
    }

    // Helper function to round rates/percentages to 4 decimal places
    fn round_rate(value: f64) -> f64 {
        (value * 10000.0).round() / 10000.0
    }

    // Helper function to round costs to 4 decimal places
    fn round_cost(value: f64) -> f64 {
        (value * 10000.0).round() / 10000.0
    }

    // Helper to get valid return reason codes from reference data
    fn get_return_reason_codes() -> Vec<String> {
        crate::reference_data::init_return_reasons()
            .into_iter()
            .map(|r| r.return_reason_code)
            .collect()
    }

    // Helper to get valid waste reason codes from reference data
    fn get_waste_reason_codes() -> Vec<String> {
        crate::reference_data::init_waste_reasons()
            .into_iter()
            .map(|r| r.waste_reason_code)
            .collect()
    }

    // Helper to get valid payment method codes from reference data
    fn get_payment_method_codes() -> Vec<String> {
        crate::reference_data::init_payment_methods()
            .into_iter()
            .filter(|pm| pm.is_active)  // Only active payment methods
            .map(|pm| pm.payment_method_code)
            .collect()
    }

    // Helper to get valid promotion type codes from reference data
    fn get_promotion_type_codes() -> Vec<String> {
        crate::reference_data::init_promotion_types()
            .into_iter()
            .map(|pt| pt.promo_type_code)
            .collect()
    }

    pub fn new(seed: u64, config: Config) -> Self {
        let rng = StdRng::seed_from_u64(seed);

        // Parse dates from config
        let start_date = NaiveDate::parse_from_str(&config.date_range.start_date, "%Y-%m-%d")
            .expect("Invalid start_date format in config.toml");
        let mut end_date = NaiveDate::parse_from_str(&config.date_range.end_date, "%Y-%m-%d")
            .expect("Invalid end_date format in config.toml");

        // Cap end_date to tomorrow if flag is set and end_date is in the future
        if config.date_range.cap_to_tomorrow {
            let today = chrono::Local::now().date_naive();
            let tomorrow = today + Duration::days(1);
            if end_date > tomorrow {
                println!("⚠️  Capping end_date from {} to {} (tomorrow)", end_date, tomorrow);
                end_date = tomorrow;
            }
        }

        let mut dates = Vec::new();
        let mut current = start_date;
        while current <= end_date {
            dates.push(current);
            current += Duration::days(1);
        }

        let holidays = generate_all_holidays();
        let categories = Self::init_categories();
        let brands = Self::init_brands();
        let suppliers = crate::reference_data::init_suppliers();

        Self {
            rng,
            config,
            start_date,
            end_date,
            dates,
            products: Vec::new(),
            stores: Vec::new(),
            store_economics: HashMap::new(),
            calendar: HashMap::new(),
            promotions: Vec::new(),
            assortment: Vec::new(),
            ground_truth_events: Vec::new(),
            holidays,
            categories,
            brands,
            suppliers,
            customers: Vec::new(),
            customer_addresses: Vec::new(),
            delivery_drivers: Vec::new(),
            delivery_zones: Vec::new(),
        }
    }

    /// Load customers from CSV file
    pub fn load_customers_from_csv(&mut self, path: &Path) -> Result<()> {
        let mut rdr = csv::Reader::from_path(path)?;
        let mut count = 0;
        for result in rdr.deserialize() {
            let customer: Customer = result?;
            self.customers.push(customer);
            count += 1;
        }
        println!("  ✓ Loaded {} customers from {}", count, path.display());
        Ok(())
    }

    /// Load customer addresses from CSV file
    pub fn load_customer_addresses_from_csv(&mut self, path: &Path) -> Result<()> {
        let mut rdr = csv::Reader::from_path(path)?;
        let mut count = 0;
        for result in rdr.deserialize() {
            let address: CustomerAddress = result?;
            self.customer_addresses.push(address);
            count += 1;
        }
        println!("  ✓ Loaded {} customer addresses from {}", count, path.display());
        Ok(())
    }

    /// Load delivery drivers from CSV file
    pub fn load_drivers_from_csv(&mut self, path: &Path) -> Result<()> {
        let mut rdr = csv::Reader::from_path(path)?;
        let mut count = 0;
        for result in rdr.deserialize() {
            let driver: DeliveryDriver = result?;
            self.delivery_drivers.push(driver);
            count += 1;
        }
        println!("  ✓ Loaded {} delivery drivers from {}", count, path.display());
        Ok(())
    }

    /// Load products from CSV file
    pub fn load_products_from_csv(&mut self, path: &Path) -> Result<()> {
        let mut rdr = csv::Reader::from_path(path)?;
        let mut count = 0;
        for result in rdr.deserialize() {
            let product: Product = result?;
            self.products.push(product);
            count += 1;
        }
        println!("  ✓ Loaded {} products from {}", count, path.display());
        Ok(())
    }

    /// Load stores from CSV file
    pub fn load_stores_from_csv(&mut self, path: &Path) -> Result<()> {
        let mut rdr = csv::Reader::from_path(path)?;
        let mut count = 0;
        for result in rdr.deserialize() {
            let store: Store = result?;
            self.stores.push(store);
            count += 1;
        }
        println!("  ✓ Loaded {} stores from {}", count, path.display());
        Ok(())
    }

    /// Load all reference data from a directory (products, stores, customers, addresses, drivers)
    pub fn load_reference_from_dir(&mut self, dir: &str) -> Result<()> {
        let dir_path = Path::new(dir);

        println!("\n📂 Loading reference data from {}...", dir);

        // Load products first (needed for transactions)
        let products_path = dir_path.join("products.csv");
        if products_path.exists() {
            self.load_products_from_csv(&products_path)?;
        } else {
            println!("  ⚠️  products.csv not found, will generate");
        }

        // Load stores (needed for transactions)
        let stores_path = dir_path.join("stores.csv");
        if stores_path.exists() {
            self.load_stores_from_csv(&stores_path)?;
        } else {
            println!("  ⚠️  stores.csv not found, will generate");
        }

        let customers_path = dir_path.join("customers.csv");
        if customers_path.exists() {
            self.load_customers_from_csv(&customers_path)?;
        } else {
            println!("  ⚠️  customers.csv not found, will generate");
        }

        let addresses_path = dir_path.join("customer_addresses.csv");
        if addresses_path.exists() {
            self.load_customer_addresses_from_csv(&addresses_path)?;
        } else {
            println!("  ⚠️  customer_addresses.csv not found, will generate");
        }

        let drivers_path = dir_path.join("delivery_drivers.csv");
        if drivers_path.exists() {
            self.load_drivers_from_csv(&drivers_path)?;
        } else {
            println!("  ⚠️  delivery_drivers.csv not found, will generate");
        }

        Ok(())
    }

    fn init_categories() -> HashMap<String, CategoryConfig> {
        let mut categories = HashMap::new();

        // Load from reference data and add generation-specific parameters
        for cat in crate::reference_data::init_categories() {
            let dow_effect = match cat.category_name.as_str() {
                "meat" => 0.18,
                "snacks" => 0.15,
                "bakery" | "beverages" => 0.12,
                "dairy" => 0.10,
                "candy" => 0.10,
                "produce" => 0.08,
                "frozen" => 0.06,
                "cereal" => 0.05,
                "canned" => 0.03,
                "personal_care" => 0.02,
                "household" => -0.05,
                _ => 0.05,
            };

            categories.insert(
                cat.category_name.clone(),
                CategoryConfig {
                    elasticity: cat.elasticity,
                    dow_effect,
                }
            );
        }
        categories
    }

    fn init_brands() -> Vec<BrandInfo> {
        // Load from reference data - now includes popularity
        crate::reference_data::init_brands_reference()
            .into_iter()
            .map(|brand| BrandInfo {
                name: brand.brand_name,
                tier: brand.brand_tier,
                popularity: brand.brand_popularity,
            })
            .collect()
    }

    pub fn generate_products(&mut self) {
        let mut products = Vec::new();
        let mut product_id = 1;

        // Define which brands can produce which categories
        let brand_categories: HashMap<&str, Vec<&str>> = [
            // Private label - can do everything
            ("ShelfWise Select", vec!["cereal", "dairy", "snacks", "beverages", "produce", "household", "frozen", "bakery", "meat", "canned", "personal_care", "candy"]),
            ("ShelfWise Basics", vec!["cereal", "dairy", "snacks", "beverages", "produce", "household", "frozen", "bakery", "meat", "canned", "personal_care", "candy"]),
            ("ShelfWise Organic", vec!["cereal", "dairy", "snacks", "produce", "frozen", "bakery", "meat"]),
            ("ShelfWise Fresh", vec!["produce", "dairy", "bakery", "meat"]),
            ("Trader Joes", vec!["cereal", "dairy", "snacks", "beverages", "produce", "household", "frozen", "bakery", "canned", "personal_care", "candy"]),
            ("365 Whole Foods", vec!["cereal", "dairy", "snacks", "beverages", "produce", "household", "frozen", "bakery", "meat", "canned", "personal_care"]),
            ("Kirkland", vec!["cereal", "dairy", "snacks", "beverages", "produce", "household", "frozen", "bakery", "meat", "canned", "personal_care"]),
            ("Great Value", vec!["cereal", "dairy", "snacks", "beverages", "produce", "household", "frozen", "bakery", "meat", "canned", "personal_care", "candy"]),
            ("Simple Truth", vec!["cereal", "dairy", "snacks", "beverages", "produce", "frozen", "bakery", "meat", "canned"]),
            ("Signature Select", vec!["cereal", "dairy", "snacks", "beverages", "produce", "frozen", "bakery", "meat", "canned"]),
            
            // Cereal brands
            ("Kelloggs", vec!["cereal", "snacks", "frozen"]),
            ("General Mills", vec!["cereal", "snacks", "frozen"]),
            ("Quaker", vec!["cereal", "snacks"]),
            
            // Snack/candy brands
            ("Frito-Lay", vec!["snacks"]),
            ("Mondelez", vec!["snacks", "candy"]),
            ("Mars", vec!["candy", "snacks"]),
            ("Hershey", vec!["candy"]),
            
            // Beverage brands
            ("PepsiCo", vec!["beverages", "snacks"]),
            ("Coca-Cola", vec!["beverages"]),
            
            // Food conglomerates
            ("Nestle", vec!["cereal", "candy", "beverages", "frozen"]),
            ("Kraft Heinz", vec!["dairy", "canned", "frozen", "snacks"]),
            ("Campbell Soup", vec!["canned", "snacks", "frozen"]),
            ("ConAgra", vec!["frozen", "canned", "snacks"]),
            
            // Household/personal care
            ("Unilever", vec!["personal_care", "household", "frozen"]),
            ("Procter & Gamble", vec!["personal_care", "household"]),
            
            // Produce
            ("Dole", vec!["produce", "canned", "frozen"]),
            ("Del Monte", vec!["produce", "canned"]),
            
            // Meat
            ("Tyson Foods", vec!["meat", "frozen"]),
            ("Hormel", vec!["meat", "canned"]),
            ("Smithfield", vec!["meat"]),
            ("Perdue", vec!["meat", "frozen"]),
            
            // Dairy
            ("Danone", vec!["dairy"]),
            ("Chobani", vec!["dairy"]),
            
            // Specialty
            ("Blue Diamond", vec!["snacks"]),
            ("Wonderful", vec!["snacks", "produce"]),
            ("Organic Valley", vec!["dairy", "produce"]),
            ("Bobs Red Mill", vec!["cereal", "bakery"]),
            ("Barilla", vec!["canned"]),
            ("B&G Foods", vec!["canned", "snacks"]),
            ("Ocean Spray", vec!["beverages", "canned"]),
            
            // New brands (64-80)
            ("Applegate", vec!["meat"]),
            ("Sabra", vec!["snacks", "canned"]),
            ("Stonyfield", vec!["dairy"]),
            ("Silk", vec!["dairy", "beverages"]),
            ("So Delicious", vec!["dairy", "frozen"]),
            ("Talenti", vec!["frozen"]),
            ("Dove", vec!["personal_care", "candy"]),
            ("Tide", vec!["household"]),
            ("Crest", vec!["personal_care"]),
            ("Colgate", vec!["personal_care"]),
            ("Seventh Generation", vec!["household", "personal_care"]),
            
            // Additional existing brands that weren't in the mapping
            ("Annies Homegrown", vec!["cereal", "snacks", "canned"]),
            ("Horizon Organic", vec!["dairy"]),
            ("Kind", vec!["snacks"]),
            ("Clif Bar", vec!["snacks"]),
            ("Nature Valley", vec!["snacks"]),
            ("Nabisco", vec!["snacks", "candy"]),
            ("Ritz", vec!["snacks"]),
            ("Pepperidge Farm", vec!["snacks", "bakery", "frozen"]),
            ("Hunts", vec!["canned"]),
            ("Progresso", vec!["canned"]),
            ("Swanson", vec!["canned", "frozen"]),
            ("Green Giant", vec!["canned", "frozen"]),
            ("Birds Eye", vec!["frozen"]),
            ("Lean Cuisine", vec!["frozen"]),
            ("Stouffers", vec!["frozen"]),
            ("DiGiorno", vec!["frozen"]),
            ("Haagen-Dazs", vec!["frozen"]),
            ("Ben & Jerrys", vec!["frozen"]),
            ("Breyers", vec!["frozen"]),
            ("Dreyers", vec!["frozen"]),
            ("PolarSprings", vec!["beverages"]),
            ("Dasani", vec!["beverages"]),
            ("Smartwater", vec!["beverages"]),
            ("Fiji", vec!["beverages"]),
            ("Poland Spring", vec!["beverages"]),
            ("Gatorade", vec!["beverages"]),
            ("Powerade", vec!["beverages"]),
            ("Tropicana", vec!["beverages"]),
            ("Simply", vec!["beverages"]),
            ("Minute Maid", vec!["beverages"]),
        ].iter().cloned().collect();

        let sub_categories: HashMap<&str, Vec<&str>> = [
            ("cereal", vec!["oats", "corn_flakes", "granola", "wheat", "rice", "bran"]),
            ("dairy", vec!["milk", "cheese", "yogurt", "butter", "cream", "sour_cream"]),
            ("snacks", vec!["chips", "crackers", "nuts", "pretzels", "popcorn", "trail_mix"]),
            ("beverages", vec!["cola", "juice", "water", "tea", "coffee", "energy_drink"]),
            ("produce", vec!["apples", "bananas", "lettuce", "tomatoes", "carrots", "onions", "berries"]),
            ("household", vec!["paper_towels", "soap", "detergent", "cleaner", "trash_bags"]),
            ("frozen", vec!["ice_cream", "pizza", "vegetables", "meals", "waffles"]),
            ("bakery", vec!["bread", "bagels", "rolls", "muffins", "tortillas"]),
            ("meat", vec!["chicken", "beef", "pork", "turkey", "sausage"]),
            ("canned", vec!["soup", "vegetables", "beans", "pasta", "fruit"]),
            ("personal_care", vec!["shampoo", "toothpaste", "soap", "deodorant", "lotion"]),
            ("candy", vec!["chocolate", "gummies", "hard_candy", "mints"]),
        ].iter().cloned().collect();

        for brand in &self.brands {
            // Get categories this brand can produce
            let allowed_categories = brand_categories.get(brand.name.as_str())
                .cloned()
                .unwrap_or_else(|| vec!["cereal", "snacks", "beverages"]); // Default fallback

            for category in allowed_categories {
                let subs = sub_categories.get(category).unwrap();

                // Generate 8-20 products per brand-category combination for variety
                let num_products = self.rng.gen_range(8..=20);

                for _ in 0..num_products {
                    let sub_category = subs.choose(&mut self.rng).unwrap();

                // Use log-normal distribution for prices (most items cheap, few expensive)
                // Mean of ln(price) = 1.8 gives median ~$6, with long tail to $50+
                // More realistic grocery pricing: $0.99 to $25 range
                // Most items $2-8, some premium items up to $25
                let log_normal = LogNormal::new(1.2, 0.7).unwrap();
                let base_price: f64 = log_normal.sample(&mut self.rng);
                let base_price = base_price.clamp(0.99, 18.0);

                let raw_price = match brand.tier.as_str() {
                    "premium" => (base_price * 1.4).min(25.0),  // Premium capped at $25
                    "value" => (base_price * 0.75).max(0.99),   // Value at least $0.99
                    _ => base_price,
                };

                // Round to realistic retail prices (.99, .49, .95, .89, or .00 for round numbers)
                let list_price = if raw_price < 1.0 {
                    0.99
                } else {
                    let dollars = raw_price.floor();
                    let endings = [0.99, 0.49, 0.95, 0.89, 0.00];
                    let ending = endings[self.rng.gen_range(0..endings.len())];
                    dollars + ending
                };

                // Realistic cost margins vary by category, brand tier, and randomness
                // Category-based margin profiles (lower cost ratio = higher margin)
                let category_cost_ratio = match category {
                    // High margin categories
                    "personal_care" => self.rng.gen_range(0.35..0.50),  // 50-65% margin
                    "household" => self.rng.gen_range(0.40..0.55),      // 45-60% margin
                    "candy" => self.rng.gen_range(0.45..0.60),          // 40-55% margin
                    "snacks" => self.rng.gen_range(0.50..0.65),         // 35-50% margin
                    "beverages" => self.rng.gen_range(0.50..0.65),      // 35-50% margin

                    // Medium margin categories
                    "cereal" => self.rng.gen_range(0.55..0.70),         // 30-45% margin
                    "canned" => self.rng.gen_range(0.55..0.70),         // 30-45% margin
                    "frozen" => self.rng.gen_range(0.58..0.72),         // 28-42% margin
                    "bakery" => self.rng.gen_range(0.60..0.75),         // 25-40% margin

                    // Low margin categories (competitive/perishable)
                    "dairy" => self.rng.gen_range(0.65..0.80),          // 20-35% margin
                    "produce" => self.rng.gen_range(0.70..0.85),        // 15-30% margin
                    "meat" => self.rng.gen_range(0.72..0.87),           // 13-28% margin

                    _ => self.rng.gen_range(0.55..0.70),                // Default 30-45% margin
                };

                // Brand tier adjustment (premium brands often have better margins)
                let tier_adjustment = match brand.tier.as_str() {
                    "premium" => self.rng.gen_range(0.90..0.98),  // Slightly better margins
                    "value" => self.rng.gen_range(1.02..1.10),    // Slightly worse margins
                    _ => 1.0,                                      // No adjustment
                };

                    // Round cost to 4 decimals (internal precision, not customer-facing)
                    let cost = (list_price * category_cost_ratio * tier_adjustment * 10000.0).round() / 10000.0;
                    let brand_code: String = brand.name.chars().filter(|c| c.is_alphanumeric()).take(3).collect::<String>().to_uppercase();
                    let sku = format!("{}-{}-{:04}", brand_code, category.to_uppercase(), product_id);

                    products.push(Product {
                        product_id,
                        sku,
                        brand: brand.name.clone(),
                        category: category.to_string(),
                        sub_category: sub_category.to_string(),
                        size: "1 unit".to_string(),
                        unit_of_measure: "each".to_string(),
                        list_price,
                        cost,
                        launch_date: self.start_date - Duration::days(self.rng.gen_range(0..730)),
                        discontinue_date: None,
                        brand_popularity: brand.popularity,
                        tier: brand.tier.clone(),
                        pareto_weight: 1.0,
                    });

                    product_id += 1;

                    // Stop if we've reached max products
                    if product_id > self.config.scale.max_products as u32 {
                        break;
                    }
                }

                if product_id > self.config.scale.max_products as u32 {
                    break;
                }
            }

            if product_id > self.config.scale.max_products as u32 {
                break;
            }
        }

        let num_products = products.len();
        let top_20_pct = (num_products as f64 * 0.2) as usize;
        let exp_top = Exp::new(0.25).unwrap();
        let exp_bottom = Exp::new(2.0).unwrap();

        let mut weights: Vec<f64> = Vec::new();
        for _ in 0..top_20_pct {
            weights.push(exp_top.sample(&mut self.rng));
        }
        for _ in top_20_pct..num_products {
            weights.push(exp_bottom.sample(&mut self.rng));
        }

        let sum: f64 = weights.iter().sum();
        for w in &mut weights { *w /= sum; }
        weights.shuffle(&mut self.rng);

        for (i, product) in products.iter_mut().enumerate() {
            product.pareto_weight = Self::round_rate(weights[i]);
        }

        self.products = products;
    }

    pub fn generate_stores(&mut self) {
        let mut stores = Vec::new();

        // Store 1: Online store (fulfillment center in Bay Area - Tracy, CA)
        // Tracy is a major logistics hub in the Bay Area, perfect for a West Coast-focused retailer
        // Close to I-580/I-5 interchange, serves entire Bay Area and beyond
        stores.push(Store {
            store_id: 1,
            region: "west_coast".to_string(),
            store_type: "online".to_string(),
            sq_ft: 500000,
            opened_date: self.start_date - Duration::days(1825),
            climate_zone: "controlled".to_string(),
            city: "Tracy, CA (Fulfillment Center)".to_string(),
            latitude: 37.7397,
            longitude: -121.4252,
        });

        // Generate 263 domestic stores distributed across regions
        // Python distribution: 107 urban, 168 suburban, 83 convenience, 46 big_box = 404 total
        // But only 263 are actually created due to population allocation
        // We'll use a simplified but accurate distribution
        let store_distribution = vec![
            ("urban", 107),
            ("suburban", 168),
            ("convenience", 83),
            ("big_box", 46),
        ];

        // West Coast Regional Chain with National Expansion Strategy
        // Core: Bay Area (35%) | California (25%) | Pacific NW (20%) | Southwest (10%) | Strategic National (10%)
        let cities = vec![
            // Bay Area - Core Market (35% of stores) - Founded here, strongest presence
            ("San Francisco, CA", 37.7749, -122.4194, "west_coast", "temperate"),
            ("San Jose, CA", 37.3382, -121.8863, "west_coast", "temperate"),
            ("Oakland, CA", 37.8044, -122.2712, "west_coast", "temperate"),
            ("Berkeley, CA", 37.8715, -122.2730, "west_coast", "temperate"),
            ("Palo Alto, CA", 37.4419, -122.1430, "west_coast", "temperate"),
            ("Mountain View, CA", 37.3861, -122.0839, "west_coast", "temperate"),
            ("Fremont, CA", 37.5485, -121.9886, "west_coast", "temperate"),
            ("San Mateo, CA", 37.5630, -122.3255, "west_coast", "temperate"),
            ("Redwood City, CA", 37.4852, -122.2364, "west_coast", "temperate"),
            ("Sunnyvale, CA", 37.3688, -122.0363, "west_coast", "temperate"),
            ("Santa Clara, CA", 37.3541, -121.9552, "west_coast", "temperate"),
            ("Cupertino, CA", 37.3230, -122.0322, "west_coast", "temperate"),
            ("Daly City, CA", 37.6879, -122.4702, "west_coast", "temperate"),
            ("San Rafael, CA", 37.9735, -122.5311, "west_coast", "temperate"),
            ("Walnut Creek, CA", 37.9101, -122.0652, "west_coast", "temperate"),

            // Greater California - Secondary Markets (25% of stores)
            ("Sacramento, CA", 38.5816, -121.4944, "west_coast", "temperate"),
            ("Los Angeles, CA", 34.0522, -118.2437, "west_coast", "temperate"),
            ("San Diego, CA", 32.7157, -117.1611, "west_coast", "temperate"),
            ("Fresno, CA", 36.7378, -119.7871, "west_coast", "temperate"),
            ("Santa Rosa, CA", 38.4404, -122.7141, "west_coast", "temperate"),
            ("Monterey, CA", 36.6002, -121.8947, "west_coast", "temperate"),
            ("Santa Cruz, CA", 36.9741, -122.0308, "west_coast", "temperate"),
            ("Napa, CA", 38.2975, -122.2869, "west_coast", "temperate"),
            ("Stockton, CA", 37.9577, -121.2908, "west_coast", "temperate"),
            ("Modesto, CA", 37.6391, -120.9969, "west_coast", "temperate"),

            // Pacific Northwest - Strong Expansion (20% of stores)
            ("Seattle, WA", 47.6062, -122.3321, "west_coast", "temperate"),
            ("Portland, OR", 45.5152, -122.6784, "west_coast", "temperate"),
            ("Eugene, OR", 44.0521, -123.0868, "west_coast", "temperate"),
            ("Tacoma, WA", 47.2529, -122.4443, "west_coast", "temperate"),
            ("Bellevue, WA", 47.6101, -122.2015, "west_coast", "temperate"),
            ("Spokane, WA", 47.6588, -117.4260, "west_coast", "temperate"),
            ("Salem, OR", 44.9429, -123.0351, "west_coast", "temperate"),
            ("Bend, OR", 44.0582, -121.3153, "west_coast", "temperate"),

            // Southwest - Regional Expansion (10% of stores)
            ("Phoenix, AZ", 33.4484, -112.0740, "southwest", "hot"),
            ("Las Vegas, NV", 36.1699, -115.1398, "southwest", "hot"),
            ("Reno, NV", 39.5296, -119.8138, "southwest", "temperate"),
            ("Tucson, AZ", 32.2226, -110.9747, "southwest", "hot"),
            ("Denver, CO", 39.7392, -104.9903, "southwest", "temperate"),
            ("Boulder, CO", 40.0150, -105.2705, "southwest", "temperate"),

            // Strategic National Expansion - Testing new markets (10% of stores)
            ("Austin, TX", 30.2672, -97.7431, "expansion", "hot"),
            ("Chicago, IL", 41.8781, -87.6298, "expansion", "cold"),
            ("New York, NY", 40.7128, -74.0060, "expansion", "cold"),
            ("Boston, MA", 42.3601, -71.0589, "expansion", "cold"),
            ("Atlanta, GA", 33.7490, -84.3880, "expansion", "hot"),
            ("Miami, FL", 25.7617, -80.1918, "expansion", "hot"),
        ];

        let mut store_id = 2;
        let mut stores_per_type: std::collections::HashMap<&str, usize> = std::collections::HashMap::new();
        for (store_type, _) in &store_distribution {
            stores_per_type.insert(store_type, 0);
        }

        // Generate domestic stores from config
        for _ in 0..self.config.scale.num_domestic_stores {
            // Pick store type based on remaining quota
            let available_types: Vec<(&str, usize)> = store_distribution.iter()
                .filter(|(t, max)| stores_per_type.get(t).unwrap_or(&0) < max)
                .map(|(t, max)| (*t, *max))
                .collect();

            if available_types.is_empty() {
                break;
            }

            let (store_type, _) = available_types.choose(&mut self.rng).unwrap();
            *stores_per_type.get_mut(store_type).unwrap() += 1;

            // Pick a city
            let (city, lat, lon, region, climate) = cities.choose(&mut self.rng).unwrap();

            // Add small random offset to coordinates (within ~1 mile)
            let lat_offset = self.rng.gen_range(-0.01..0.01);
            let lon_offset = self.rng.gen_range(-0.01..0.01);

            // Determine square footage based on store type
            let sq_ft = match *store_type {
                "urban" => self.rng.gen_range(10000..20000),
                "suburban" => self.rng.gen_range(25000..45000),
                "convenience" => self.rng.gen_range(3000..8000),
                "big_box" => self.rng.gen_range(60000..100000),
                _ => 30000,
            };

            // Realistic expansion timeline starting from 2009
            // Company founded in Bay Area, expanded regionally, then nationally
            // Data range is 2019-2025, so we need stores opening from 2009-2025

            let opened_date = if *region == "west_coast" {
                // Bay Area core: Founded 2009-2012 (oldest stores)
                // California expansion: 2012-2016
                // Pacific NW: 2015-2018
                let days_before_start = self.rng.gen_range(2555..3650); // 7-10 years before 2019
                self.start_date - Duration::days(days_before_start as i64)
            } else if *region == "southwest" {
                // Southwest expansion: 2016-2020 (mix of before and during data range)
                let days_before_start = self.rng.gen_range(365..2920); // 1-8 years before 2019
                self.start_date - Duration::days(days_before_start as i64)
            } else {
                // expansion region (Chicago, NYC, Boston, Atlanta, Miami, Austin)
                // National expansion: 2019-2024 (during data range to show growth)
                let days_after_start = self.rng.gen_range(0..2100); // Throughout 2019-2024
                self.start_date + Duration::days(days_after_start as i64)
            };

            stores.push(Store {
                store_id,
                region: region.to_string(),
                store_type: store_type.to_string(),
                sq_ft,
                opened_date,
                climate_zone: climate.to_string(),
                city: city.to_string(),
                latitude: lat + lat_offset,
                longitude: lon + lon_offset,
            });

            store_id += 1;
        }

        // International expansion - Testing Canadian and UK markets
        // Strategic international expansion during data range (2020-2024)
        // Shows measured, deliberate international growth
        let international_stores = [
            ("Vancouver, BC", 49.2827, -123.1207, "urban", 365),      // Q1 2020 - Natural expansion from Seattle
            ("Vancouver, BC", 49.2827, -123.1207, "suburban", 730),   // Q1 2021 - Second Vancouver location
            ("Toronto, ON", 43.6532, -79.3832, "urban", 1095),        // Q1 2022 - Major Canadian market entry
            ("Montreal, QC", 45.5017, -73.5673, "urban", 1460),       // Q1 2023 - French-Canadian market test
            ("London, UK", 51.5074, -0.1278, "urban", 1825),          // Q1 2024 - European market test
        ];

        // Add international stores from config
        for (city, lat, lon, store_type, days_after_start) in international_stores.iter().take(self.config.scale.num_international_stores) {
            let lat_offset = self.rng.gen_range(-0.005..0.005);
            let lon_offset = self.rng.gen_range(-0.005..0.005);

            let sq_ft = match *store_type {
                "urban" => self.rng.gen_range(12000..18000),
                "suburban" => self.rng.gen_range(28000..40000),
                _ => 25000,
            };

            let climate = if city.contains("Canada") || city.contains("ON") || city.contains("QC") || city.contains("BC") {
                "cold"
            } else {
                "temperate"
            };

            stores.push(Store {
                store_id,
                region: "international".to_string(),
                store_type: store_type.to_string(),
                sq_ft,
                opened_date: self.start_date + Duration::days(*days_after_start as i64),
                climate_zone: climate.to_string(),
                city: city.to_string(),
                latitude: lat + lat_offset,
                longitude: lon + lon_offset,
            });

            store_id += 1;
        }

        println!("Generated {} stores (1 online + domestic + international)", stores.len());
        self.stores = stores;
    }

    /// Create a single customer with their behavior profile.
    /// This is the shared implementation used by both initial and nightly generation.
    ///
    /// Parameters:
    /// - `customer_id`: Unique customer ID
    /// - `signup_date`: The date this customer signed up (used for year-based rates)
    /// - `is_founding`: If true, created_date will be None (founding customers predate tracking)
    /// - `physical_stores`: List of physical stores to assign customers to
    fn create_single_customer(
        &mut self,
        customer_id: u64,
        signup_date: NaiveDate,
        is_founding: bool,
        physical_stores: &[Store],
    ) -> Customer {
        // Demographics - same distribution for all customers
        let age_bracket = self.pick_weighted(&[
            ("18-24", AGE_18_24),
            ("25-34", AGE_25_34),
            ("35-44", AGE_35_44),
            ("45-54", AGE_45_54),
            ("55-64", AGE_55_64),
            ("65+", AGE_65_PLUS),
        ]);

        let household_size = self.pick_weighted_u32(&[
            (1, HOUSEHOLD_SIZE_1),
            (2, HOUSEHOLD_SIZE_2),
            (3, HOUSEHOLD_SIZE_3),
            (4, HOUSEHOLD_SIZE_4),
            (5, HOUSEHOLD_SIZE_5_PLUS),
        ]);

        let income_bracket = self.pick_weighted(&[
            ("low", INCOME_LOW),
            ("medium", INCOME_MEDIUM),
            ("high", INCOME_HIGH),
            ("very_high", INCOME_VERY_HIGH),
        ]);

        let segment = self.pick_weighted(&[
            ("frequent_shopper", SEGMENT_FREQUENT_SHOPPER),
            ("weekly_shopper", SEGMENT_WEEKLY_SHOPPER),
            ("bulk_buyer", SEGMENT_BULK_BUYER),
            ("occasional", SEGMENT_OCCASIONAL),
        ]);

        // Assign to primary store
        let primary_store = physical_stores.choose(&mut self.rng).unwrap().clone();

        // Loyalty membership based on year of signup
        let loyalty_penetration = match signup_date.year() {
            2019 => LOYALTY_PENETRATION_2019,
            2020 => LOYALTY_PENETRATION_2020,
            2021 => LOYALTY_PENETRATION_2021,
            2022 => LOYALTY_PENETRATION_2022,
            2023 => LOYALTY_PENETRATION_2023,
            2024 => LOYALTY_PENETRATION_2024,
            y if y < 2019 => LOYALTY_PENETRATION_2019 * 0.8, // Earlier years had lower adoption
            _ => LOYALTY_PENETRATION_2025,
        };

        let is_loyalty_member = self.rng.gen::<f64>() < loyalty_penetration;

        // Contact info using centralized constants
        let first_name = FIRST_NAMES.choose(&mut self.rng).unwrap().to_string();
        let last_name = LAST_NAMES.choose(&mut self.rng).unwrap().to_string();
        let domain = EMAIL_DOMAINS.choose(&mut self.rng).unwrap();
        let email = format!(
            "{}.{}.{}@{}",
            first_name.to_lowercase(),
            last_name.to_lowercase(),
            customer_id,
            domain
        );

        let area_code = AREA_CODES.choose(&mut self.rng).unwrap();
        let phone = format!(
            "{}-{:03}-{:04}",
            area_code,
            self.rng.gen_range(200..999),
            self.rng.gen_range(1000..9999)
        );

        // Location near primary store (within 1-15 miles)
        let distance_miles = self.rng.gen_range(1.0..15.0);
        let angle = self.rng.gen_range(0.0..std::f64::consts::TAU);
        let lat_offset = (distance_miles / 69.0) * angle.cos();
        let lon_offset = (distance_miles / 54.6) * angle.sin();

        // Shopping preferences
        let preferred_shopping_time = self.pick_weighted(&[
            ("morning", 0.25),
            ("afternoon", 0.30),
            ("evening", 0.35),
            ("weekend", 0.10),
        ]);

        let price_sensitivity = match income_bracket.as_str() {
            "low" => "high",
            "medium" => "medium",
            "high" | "very_high" => "low",
            _ => "medium",
        };

        // Created date
        let created_date = if is_founding { None } else { Some(signup_date) };

        // Loyalty join date - NULL for founding customers (we don't know when they joined)
        let loyalty_join_date = if is_loyalty_member {
            match created_date {
                Some(d) => Some(d + Duration::days(self.rng.gen_range(0..30))),
                None => None,  // Founding customers: unknown join date
            }
        } else {
            None
        };

        // Online behavior rates based on signup year
        let signup_year = signup_date.year();
        let online_account_rate = self.get_online_account_rate_for_year(signup_year);
        let online_preference_rate = self.get_online_preference_rate_for_year(signup_year);

        Customer {
            customer_id,
            email,
            phone,
            first_name,
            last_name,
            age_bracket,
            household_size,
            income_bracket: income_bracket.clone(),
            primary_store_id: primary_store.store_id,
            primary_city: primary_store.city.clone(),
            home_latitude: primary_store.latitude + lat_offset,
            home_longitude: primary_store.longitude + lon_offset,
            loyalty_member: is_loyalty_member,
            loyalty_join_date,
            preferred_shopping_time,
            price_sensitivity: price_sensitivity.to_string(),
            customer_segment: segment.clone(),
            created_date,
            has_online_account: self.rng.gen::<f64>() < online_account_rate,
            prefers_online: self.rng.gen::<f64>() < online_preference_rate,
        }
    }

    pub fn generate_customers(&mut self) {
        let base_customers = self.config.customers.num_customers;

        // Calculate organic growth: ~3-5% ANNUAL growth rate (varying per year)
        // Uses the same rate table as nightly mode for consistency
        let total_days = (self.end_date - self.start_date).num_days();
        let years = total_days as f64 / 365.0;

        // Calculate growth year-by-year using the deterministic rate table
        let mut total_growth = 0.0;
        let mut current_base = base_customers as f64;
        let mut current_date = self.start_date;
        let mut year_rates: Vec<(i32, f64)> = Vec::new();

        while current_date <= self.end_date {
            let year = current_date.year();
            let annual_rate = self.get_annual_growth_rate_for_year(year);

            // Calculate end of this year chunk (end of calendar year or end_date, whichever is first)
            let year_end = NaiveDate::from_ymd_opt(year, 12, 31).unwrap();
            let chunk_end = if year_end < self.end_date { year_end } else { self.end_date };

            let days_in_chunk = (chunk_end - current_date).num_days() + 1;
            let year_fraction = days_in_chunk as f64 / 365.0;

            // Growth for this chunk (compounding)
            let chunk_growth = current_base * annual_rate * year_fraction;
            total_growth += chunk_growth;
            current_base += chunk_growth;

            year_rates.push((year, annual_rate));
            current_date = chunk_end + Duration::days(1);
        }

        let total_growth = total_growth as usize;
        let avg_rate = year_rates.iter().map(|(_, r)| r).sum::<f64>() / year_rates.len() as f64;

        let num_customers = base_customers + total_growth;

        // === FOUNDING CUSTOMERS vs ORGANIC GROWTH ===
        // Base customers are "founding" customers - they existed before we started tracking.
        // They get NULL created_date (we don't know when they joined).
        // Only organic growth customers (added during simulation) get actual signup dates.
        // This avoids unrealistic signup spikes and matches the nightly script's variable rate.

        println!("Generating {} customers ({} founding + {} organic growth @ 3-5% annual over {:.2} years)...",
                 num_customers, base_customers, total_growth, years);
        println!("  Year-by-year rates: {:?}", year_rates.iter().map(|(y, r)| format!("{}: {:.1}%", y, r * 100.0)).collect::<Vec<_>>());
        println!("  Average rate: {:.2}%", avg_rate * 100.0);
        println!("  Founding customers: NULL created_date (pre-existing)");
        println!("  Organic growth: spread from {} to {} (~{:.0}/month)",
                 self.start_date, self.end_date, total_growth as f64 / (years * 12.0));

        // Build weighted date distribution for organic growth customers
        // Each day gets a weight based on day-of-week, seasonal, and holiday factors
        let total_sim_days = (self.end_date - self.start_date).num_days() as usize;
        let mut date_weights: Vec<(NaiveDate, f64)> = Vec::with_capacity(total_sim_days + 1);
        let mut total_weight = 0.0;

        for day_offset in 0..=total_sim_days {
            let date = self.start_date + Duration::days(day_offset as i64);
            let weight = self.get_signup_weight(date);
            total_weight += weight;
            date_weights.push((date, weight));
        }

        // Build cumulative distribution for sampling organic growth signup dates
        let mut cumulative_weights: Vec<f64> = Vec::with_capacity(date_weights.len());
        let mut cumsum = 0.0;
        for (_, weight) in &date_weights {
            cumsum += weight / total_weight;
            cumulative_weights.push(cumsum);
        }

        // Pre-compute physical stores list (excludes online/fulfillment center)
        let physical_stores: Vec<Store> = self.stores.iter()
            .filter(|s| s.store_type != "online")
            .cloned()
            .collect();

        let mut customers = Vec::new();

        // Add hardcoded VIP customers FIRST (they get IDs 1, 2, 3, ...)
        let num_vip = self.add_hardcoded_customers(&mut customers);
        println!("  Added {} VIP customers (IDs 1-{})", num_vip, num_vip);

        // Regular customers start after VIP customers
        let first_regular_id = num_vip as u64 + 1;
        for customer_id in first_regular_id..=(num_customers as u64 + num_vip as u64) {
            // Determine if this is a founding customer or organic growth
            let is_founding = customer_id <= base_customers as u64;

            // Determine signup date:
            // - Founding customers: use start_date for rate calculations (they predate tracking)
            // - Organic growth: sample from weighted date distribution
            let signup_date = if is_founding {
                // Use a date before start for founding customers (for rate calculations)
                self.start_date - Duration::days(365)
            } else {
                // Sample from weighted distribution
                let r = self.rng.gen::<f64>();
                let idx = cumulative_weights.iter()
                    .position(|&cw| r <= cw)
                    .unwrap_or(cumulative_weights.len() - 1);
                date_weights[idx].0
            };

            // Use shared customer creation function
            let customer = self.create_single_customer(
                customer_id,
                signup_date,
                is_founding,
                &physical_stores,
            );

            customers.push(customer);
        }

        self.customers = customers;

        println!("  Generated {} customers", self.customers.len());

        // Generate customer addresses (1-2 per customer)
        self.generate_customer_addresses();
    }

    /// Add hardcoded VIP customers (called at the START of customer generation)
    /// Returns the number of VIP customers added (so regular customers start at ID num_vip + 1)
    fn add_hardcoded_customers(
        &self,
        customers: &mut Vec<Customer>,
    ) -> usize {
        // Find San Francisco store, or fall back to first Bay Area store
        let sf_store = self.stores.iter()
            .find(|s| s.city.contains("San Francisco"))
            .or_else(|| self.stores.iter().find(|s| s.city.contains("Berkeley")))
            .or_else(|| self.stores.iter().find(|s| s.city.contains("Oakland")))
            .unwrap_or(&self.stores[0]);

        let adam = Customer {
            customer_id: 1,
            email: "adam@promptql.io".to_string(),
            phone: "628-588-1234".to_string(),
            first_name: "Adam".to_string(),
            last_name: "Malone".to_string(),
            age_bracket: "35-44".to_string(),
            household_size: 1,
            income_bracket: "high".to_string(),
            primary_store_id: sf_store.store_id,
            primary_city: "San Francisco, CA".to_string(),
            home_latitude: 37.785834,
            home_longitude: -122.396736,
            loyalty_member: true,
            loyalty_join_date: Some(self.start_date),
            preferred_shopping_time: "morning".to_string(),
            price_sensitivity: "low".to_string(),
            customer_segment: "frequent_shopper".to_string(),
            created_date: Some(self.start_date),
            has_online_account: true,
            prefers_online: true,
        };

        customers.push(adam);

        1 // Return count of VIP customers
    }

    /// Generate 1-2 addresses for a single customer.
    /// This is the shared implementation used by both initial and nightly generation.
    fn generate_addresses_for_customer(&mut self, customer: &Customer, signup_date: NaiveDate) {
        // VIP customer #1 (Adam) gets a hardcoded address
        if customer.customer_id == 1 {
            let address_id = self.customer_addresses.len() as u64 + 1;
            let address = CustomerAddress {
                address_id,
                customer_id: 1,
                address_type: "work".to_string(),
                is_default: true,
                street_address: "576 Folsom St".to_string(),
                apartment_unit: None,
                city: "San Francisco".to_string(),
                state: "CA".to_string(),
                zip_code: "94105".to_string(),
                latitude: 37.785834,
                longitude: -122.396736,
                delivery_instructions: Some("PromptQL HQ - ring buzzer".to_string()),
                has_doorman: true,
                requires_signature: false,
                created_at: signup_date.and_hms_opt(10, 0, 0).unwrap(),
            };
            self.customer_addresses.push(address);
            return;
        }

        // Each customer gets 1-2 addresses (70% have 1, 30% have 2)
        let num_addresses = if self.rng.gen::<f64>() < 0.70 { 1 } else { 2 };

        for addr_num in 0..num_addresses {
            let address_type = if addr_num == 0 { "home" } else { "work" };
            let is_default = addr_num == 0;

            // Generate address near customer's home location (within 2 miles)
            let distance = self.rng.gen_range(0.0..2.0);
            let angle = self.rng.gen_range(0.0..std::f64::consts::TAU);
            let latitude = customer.home_latitude + (distance / 69.0) * angle.cos();
            let longitude = customer.home_longitude + (distance / 54.6) * angle.sin();

            // Generate street address using centralized constants
            let street_num = self.rng.gen_range(100..9999);
            let street_name = STREET_NAMES.choose(&mut self.rng).unwrap();
            let street_address = format!("{} {}", street_num, street_name);

            // 40% have apartment/unit numbers
            let apartment_unit = if self.rng.gen::<f64>() < 0.40 {
                let apt_type = APARTMENT_TYPES.choose(&mut self.rng).unwrap();
                let apt_num = self.rng.gen_range(1..500);
                Some(format!("{} {}", apt_type, apt_num))
            } else {
                None
            };

            // Zip code based on customer's city
            let zip_code = get_zip_for_city(&customer.primary_city, &mut self.rng);

            // Delivery instructions for some addresses
            let delivery_instructions = if self.rng.gen::<f64>() < 0.30 {
                Some(self.pick_weighted(&[
                    ("Leave at door", 0.40),
                    ("Ring doorbell", 0.25),
                    ("Call on arrival", 0.20),
                    ("Leave with concierge", 0.15),
                ]))
            } else {
                None
            };

            // Urban addresses more likely to have doorman
            let has_doorman = customer.primary_city.contains("New York") && self.rng.gen::<f64>() < 0.25;

            // High-value items or apartments might require signature
            let requires_signature = self.rng.gen::<f64>() < 0.15;

            let address_id = self.customer_addresses.len() as u64 + 1;
            let address = CustomerAddress {
                address_id,
                customer_id: customer.customer_id,
                address_type: address_type.to_string(),
                is_default,
                street_address,
                apartment_unit,
                city: customer.primary_city.clone(),
                state: get_state_from_city(&customer.primary_city),
                zip_code,
                latitude,
                longitude,
                delivery_instructions,
                has_doorman,
                requires_signature,
                created_at: signup_date.and_hms_opt(12, 0, 0).unwrap(),
            };

            self.customer_addresses.push(address);
        }
    }

    pub fn generate_customer_addresses(&mut self) {
        if self.customers.is_empty() {
            println!("  Skipping customer address generation (no customers)");
            return;
        }

        println!("Generating customer addresses...");

        let customers_clone = self.customers.clone();
        for customer in &customers_clone {
            // Use the customer's signup date, or a date before start_date for founding customers
            let signup_date = customer.created_date
                .unwrap_or(self.start_date - Duration::days(self.rng.gen_range(30..365)));

            self.generate_addresses_for_customer(customer, signup_date);
        }

        println!("  Generated {} customer addresses", self.customer_addresses.len());
    }

    /// Check if date is in lead-up to a major holiday (returns multiplier)
    fn get_holiday_signup_boost(&self, date: NaiveDate) -> f64 {
        let year = date.year() as u32;

        // Check US holidays (primary market)
        if let Some(year_holidays) = self.holidays.get("us").and_then(|h| h.get(&year)) {
            // Major shopping holidays with lead-up signup boosts
            let boost_holidays = [
                ("Black Friday", 7, 2.0),      // 7 days before, 2x boost
                ("Thanksgiving", 14, 1.5),     // 14 days before, 1.5x boost
                ("Christmas", 21, 1.4),        // 3 weeks before, 1.4x boost
                ("Super Bowl Sunday", 7, 1.3), // Week before Super Bowl
                ("Easter", 7, 1.2),            // Week before Easter
                ("Memorial Day", 5, 1.2),      // 5 days before
                ("Independence Day", 5, 1.2),  // 5 days before July 4th
                ("Labor Day", 5, 1.2),         // 5 days before
            ];

            for (holiday_name, lead_days, boost) in boost_holidays {
                if let Some(&holiday_date) = year_holidays.get(holiday_name) {
                    let days_until = (holiday_date - date).num_days();
                    if days_until > 0 && days_until <= lead_days as i64 {
                        // Boost increases as we get closer to the holiday
                        let proximity_factor = 1.0 - (days_until as f64 / (lead_days as f64 + 1.0));
                        return 1.0 + (boost - 1.0) * proximity_factor;
                    }
                }
            }
        }
        1.0 // No holiday boost
    }

    /// Calculate the signup weight for a given date (used by both main and nightly generators)
    /// Returns a multiplier based on day-of-week, seasonal, and holiday factors
    fn get_signup_weight(&self, date: NaiveDate) -> f64 {
        // Day-of-week patterns: more signups on weekends
        let day_of_week = date.weekday().num_days_from_monday();
        let dow_multiplier = match day_of_week {
            5 | 6 => 1.25,  // Saturday/Sunday: 25% more signups
            4 => 1.1,       // Friday: slight boost
            0 => 0.9,       // Monday: slight dip
            _ => 1.0,
        };

        // Seasonal patterns: New Year resolutions, holiday shopping, summer lull
        let month = date.month();
        let seasonal_multiplier = match month {
            1 => 1.3,       // January: New Year resolutions
            11 => 1.15,     // November: pre-holiday
            12 => 1.2,      // December: holiday shopping
            7 | 8 => 0.85,  // Summer: slight slowdown
            _ => 1.0,
        };

        // Holiday lead-up boost
        let holiday_multiplier = self.get_holiday_signup_boost(date);

        dow_multiplier * seasonal_multiplier * holiday_multiplier
    }

    /// Calculate the driver hire weight for a given date (used by both main and nightly generators)
    /// Returns a multiplier based on day-of-week and seasonal factors
    /// Drivers are typically hired on Mondays, with seasonal patterns for holiday/summer rush
    fn get_driver_hire_weight(&self, date: NaiveDate) -> f64 {
        let day_of_week = date.weekday().num_days_from_monday();
        let month = date.month();

        // Drivers typically hired on Mondays, occasionally Fridays
        let day_multiplier = match day_of_week {
            0 => 1.0,  // Monday
            4 => 0.3,  // Friday
            _ => 0.0,  // No hiring other days
        };

        if day_multiplier == 0.0 {
            return 0.0;
        }

        // Seasonal hiring patterns
        let seasonal_multiplier = match month {
            11 | 12 => 2.0,  // Holiday rush
            1 => 0.5,        // Post-holiday slowdown
            6..=8 => 1.3, // Summer busy season
            _ => 1.0,
        };

        day_multiplier * seasonal_multiplier
    }

    /// Get the annual growth rate for a given year (deterministic, 3-5% range)
    /// Pre-computed rates for 2000-2030 ensure consistency between batch and nightly modes
    ///
    /// Year rates (for reference):
    /// Customer growth rates by year (3-5% range)
    /// 2015: 3.7%, 2016: 4.3%, 2017: 3.5%
    /// 2018: 4.8%, 2019: 3.2%, 2020: 3.9%, 2021: 4.5%, 2022: 3.6%, 2023: 4.1%
    /// 2024: 3.8%, 2025: 4.4%, 2026: 3.3%, 2027: 4.7%, 2028: 3.5%, 2029: 4.0%, 2030: 3.9%
    fn get_annual_growth_rate_for_year(&self, year: i32) -> f64 {
        match year {
            2015 => 0.037,
            2016 => 0.043,
            2017 => 0.035,
            2018 => 0.048,
            2019 => 0.032,
            2020 => 0.039,
            2021 => 0.045,
            2022 => 0.036,
            2023 => 0.041,
            2024 => 0.038,
            2025 => 0.044,
            2026 => 0.033,
            2027 => 0.047,
            2028 => 0.035,
            2029 => 0.040,
            2030 => 0.039,
            // Fallback for years outside the table: use 4% average
            _ => 0.040,
        }
    }

    /// Online adoption acceleration rate by year
    /// Reflects the shift toward ecommerce/delivery over time
    /// 2015-2018: Early adoption phase (~3-4%)
    /// 2019: Pre-pandemic growth (~5%)
    /// 2020-2021: Pandemic surge (~8%)
    /// 2022-2023: Normalization (~4%)
    /// 2024+: Mature but still growing (~3%)
    fn get_online_acceleration_rate_for_year(&self, year: i32) -> f64 {
        match year {
            2015 => 0.030,
            2016 => 0.035,
            2017 => 0.038,
            2018 => 0.042,
            2019 => 0.050,
            2020 => 0.080,
            2021 => 0.080,
            2022 => 0.045,
            2023 => 0.040,
            2024 => 0.035,
            2025 => 0.032,
            2026 => 0.030,
            2027 => 0.028,
            2028 => 0.027,
            2029 => 0.025,
            2030 => 0.025,
            // Fallback: mature market rate
            _ => 0.030,
        }
    }

    /// Driver growth rate = customer growth + online adoption acceleration
    /// This ties driver demand to actual business drivers
    fn get_driver_growth_rate_for_year(&self, year: i32) -> f64 {
        self.get_annual_growth_rate_for_year(year) + self.get_online_acceleration_rate_for_year(year)
    }

    /// Online preference rate by year - what % of customers prefer online shopping
    /// Based on US grocery ecommerce penetration trends
    /// Pre-2019: Early adopters only (~10-12%)
    /// 2020-2021: Pandemic surge (~20-25%)
    /// 2022+: Stabilized at higher baseline (~18-22%)
    fn get_online_preference_rate_for_year(&self, year: i32) -> f64 {
        match year {
            2015 => 0.08,
            2016 => 0.09,
            2017 => 0.10,
            2018 => 0.11,
            2019 => 0.13,
            2020 => 0.22,  // Pandemic surge
            2021 => 0.25,  // Peak pandemic behavior
            2022 => 0.20,  // Some reversion
            2023 => 0.19,
            2024 => 0.20,
            2025 => 0.21,
            2026 => 0.22,  // Steady state
            2027 => 0.24,  // Quick commerce boom
            2028 => 0.23,  // Pullback as delivery fees rise
            2029 => 0.25,  // Recovery with improved unit economics
            2030 => 0.27,  // Autonomous delivery pilots expand
            // Fallback: early adoption rate
            _ => 0.10,
        }
    }

    /// Online account creation rate by year - what % of customers create online accounts
    /// Higher than online preference since many create accounts but still shop in-store
    /// Tracks general ecommerce account creation trends
    fn get_online_account_rate_for_year(&self, year: i32) -> f64 {
        match year {
            2015 => 0.25,
            2016 => 0.28,
            2017 => 0.32,
            2018 => 0.35,
            2019 => 0.40,
            2020 => 0.65,  // Pandemic forced many to create accounts
            2021 => 0.70,  // Peak pandemic behavior
            2022 => 0.60,  // New signups revert somewhat
            2023 => 0.58,
            2024 => 0.60,
            2025 => 0.62,
            2026 => 0.64,
            2027 => 0.66,
            2028 => 0.68,
            2029 => 0.70,
            2030 => 0.72,
            // Fallback
            _ => 0.35,
        }
    }

    /// Annual grocery inflation rate by year
    /// Based on US Bureau of Labor Statistics CPI-Food data
    /// Note: Grocery inflation often differs from headline CPI
    fn get_inflation_rate_for_year(&self, year: i32) -> f64 {
        match year {
            2015 => 0.012,  // 1.2% - low inflation era
            2016 => 0.002,  // 0.2% - deflationary pressure
            2017 => 0.009,  // 0.9%
            2018 => 0.014,  // 1.4%
            2019 => 0.018,  // 1.8%
            2020 => 0.035,  // 3.5% - supply chain disruption
            2021 => 0.039,  // 3.9% - inflation starting
            2022 => 0.099,  // 9.9% - peak food inflation
            2023 => 0.051,  // 5.1% - moderating
            2024 => 0.024,  // 2.4% - normalizing
            2025 => 0.022,  // 2.2% - projected
            2026 => 0.021,  // 2.1% - slightly above Fed 2.0% target
            2027 => 0.028,  // 2.8% - supply chain disruption event
            2028 => 0.034,  // 3.4% - elevated food costs linger
            2029 => 0.025,  // 2.5% - moderating
            2030 => 0.019,  // 1.9% - back to normal
            // Fallback: historical average
            _ => 0.025,
        }
    }

    /// Generate new customers for a specific date (used in nightly mode)
    /// Returns the number of new customers created
    pub fn generate_new_customers_for_date(&mut self, date: NaiveDate) -> usize {
        // Calculate daily customer acquisition rate from 3-5% annual growth
        // Use config.customers.num_customers (the founding customer count from config.toml)
        // NOT self.customers.len() which grows over time and would compound the growth rate
        //
        // The annual rate is deterministic per calendar year (derived from year as seed)
        // This ensures consistency: all days in 2024 use the same base rate
        let annual_growth_rate = self.get_annual_growth_rate_for_year(date.year());
        let base_customers = self.config.customers.num_customers as f64;
        let daily_rate = base_customers * annual_growth_rate / 365.0;

        // Apply day-of-week, seasonal, and holiday multipliers (same as initial generator)
        let weight = self.get_signup_weight(date);

        // Combine with base randomness (0.7x to 1.3x)
        let today_rate = daily_rate * weight * self.rng.gen_range(0.7..1.3);
        let num_new = today_rate.round() as usize;

        if num_new == 0 {
            return 0;
        }

        let next_customer_id = self.customers.iter().map(|c| c.customer_id).max().unwrap_or(0) + 1;

        let physical_stores: Vec<Store> = self.stores.iter()
            .filter(|s| s.store_type != "online")
            .cloned()
            .collect();

        for i in 0..num_new {
            let customer_id = next_customer_id + i as u64;

            // Use shared customer creation function (is_founding=false for nightly customers)
            let customer = self.create_single_customer(
                customer_id,
                date,
                false, // Not a founding customer
                &physical_stores,
            );

            self.customers.push(customer.clone());

            // Generate addresses for new customer using shared function
            self.generate_addresses_for_customer(&customer, date);
        }

        num_new
    }

    /// Create a single driver with consistent logic for both initial and nightly generation.
    /// `is_founding` controls whether the driver has historical metrics or starts fresh.
    fn create_single_driver(&mut self, driver_id: u64, hire_date: NaiveDate, is_founding: bool) -> DeliveryDriver {
        let hire_month = hire_date.month();

        // Holiday hires (Nov/Dec) are more likely contractors
        let driver_type = if hire_month == 11 || hire_month == 12 {
            self.pick_weighted(&[("employee", 0.30), ("contractor", 0.50), ("third_party", 0.20)])
        } else {
            self.pick_weighted(&[
                ("employee", EMPLOYEE_DRIVER_PCT),
                ("contractor", CONTRACTOR_DRIVER_PCT),
                ("third_party", THIRD_PARTY_DRIVER_PCT),
            ])
        };

        // Assign to a random physical store as home base
        let home_store = self.stores.iter()
            .filter(|s| s.store_type != "online")
            .choose(&mut self.rng)
            .unwrap()
            .clone();

        // Generate driver details using centralized constants
        let first_name = FIRST_NAMES.choose(&mut self.rng).unwrap().to_string();
        let last_name = LAST_NAMES.choose(&mut self.rng).unwrap().to_string();

        // Realistic US phone numbers
        let area_code = AREA_CODES.choose(&mut self.rng).unwrap();
        let phone = format!("{}-{:03}-{:04}",
            area_code,
            self.rng.gen_range(200..999),
            self.rng.gen_range(1000..9999));

        // Vehicle type distribution
        let vehicle_type = self.pick_weighted(&[
            ("car", 0.60),
            ("suv", 0.25),
            ("van", 0.10),
            ("bike", 0.05),
        ]);

        // Vehicle capacity based on type
        let vehicle_capacity_items = match vehicle_type.as_str() {
            "van" => self.rng.gen_range(80..120),
            "suv" => self.rng.gen_range(50..80),
            "car" => self.rng.gen_range(30..50),
            "bike" => self.rng.gen_range(10..20),
            _ => 40,
        };

        // Employment status
        let employment_status = if driver_type == "employee" {
            "full_time"
        } else if driver_type == "contractor" {
            "part_time"
        } else {
            "gig"
        };

        // Service radius based on driver type
        let service_radius_miles = match driver_type.as_str() {
            "employee" => self.rng.gen_range(15.0..25.0),
            "contractor" => self.rng.gen_range(10.0..20.0),
            _ => self.rng.gen_range(5.0..15.0),
        };

        // Calculate service cities from nearby stores
        let mut service_cities_list = vec![home_store.city.clone()];
        for other_store in &self.stores {
            if other_store.store_id != home_store.store_id {
                let lat_diff = (home_store.latitude - other_store.latitude).abs();
                let lon_diff = (home_store.longitude - other_store.longitude).abs();
                let approx_distance = ((lat_diff * 69.0).powi(2) + (lon_diff * 54.6).powi(2)).sqrt();
                if approx_distance <= service_radius_miles && !service_cities_list.contains(&other_store.city) {
                    service_cities_list.push(other_store.city.clone());
                }
            }
        }
        let service_cities = service_cities_list.join(",");

        // Email generation by driver type
        let email = match driver_type.as_str() {
            "employee" => {
                format!("{}.{}@shelfwise.com", first_name.to_lowercase(), last_name.to_lowercase())
            },
            "third_party" => {
                let platforms = ["doordash.com", "uber.com", "instacart.com", "postmates.com"];
                let platform = platforms.choose(&mut self.rng).unwrap();
                format!("{}.{}@{}", first_name.to_lowercase(), last_name.to_lowercase(), platform)
            },
            _ => {
                let domain = EMAIL_DOMAINS.choose(&mut self.rng).unwrap();
                if self.rng.gen::<f64>() < 0.4 {
                    format!("{}.{}{}@{}", first_name.to_lowercase(), last_name.to_lowercase(), self.rng.gen_range(1..99), domain)
                } else {
                    format!("{}.{}@{}", first_name.to_lowercase(), last_name.to_lowercase(), domain)
                }
            },
        };

        // Compensation
        let base_pay_per_delivery = Self::round_currency(match driver_type.as_str() {
            "employee" => self.rng.gen_range(8.0..12.0),
            "contractor" => self.rng.gen_range(6.0..10.0),
            _ => self.rng.gen_range(4.0..8.0),
        });
        let mileage_rate = 0.625; // IRS standard mileage rate

        // Acceptance rate is a driver trait (willingness to take orders)
        let accept_beta = Beta::new(8.0, 2.0).unwrap();
        let accept_sample: f64 = accept_beta.sample(&mut self.rng);
        let acceptance_rate = Self::round_rate((accept_sample * 0.30 + 0.70).clamp(0.65, 0.99));

        // Availability depends on founding status
        let is_available = if is_founding {
            self.rng.gen::<f64>() < 0.75
        } else {
            true // New drivers start available
        };

        // Current location (near home store for founding, at store for new)
        let (current_latitude, current_longitude, last_location_update) = if is_founding {
            let angle = self.rng.gen_range(0.0..std::f64::consts::TAU);
            let distance = self.rng.gen_range(0.0..5.0);
            (
                home_store.latitude + (distance / 69.0) * angle.cos(),
                home_store.longitude + (distance / 54.6) * angle.sin(),
                self.start_date.and_hms_opt(12, 0, 0).unwrap()
            )
        } else {
            (home_store.latitude, home_store.longitude, hire_date.and_hms_opt(8, 0, 0).unwrap())
        };

        DeliveryDriver {
            driver_id,
            first_name,
            last_name,
            phone,
            email,
            driver_type,
            employment_status: employment_status.to_string(),
            primary_store_id: home_store.store_id,
            service_radius_miles: Self::round_rate(service_radius_miles),
            service_cities,
            vehicle_type,
            vehicle_capacity_items,
            has_insulated_bags: self.rng.gen::<f64>() < 0.85,
            acceptance_rate,
            is_available,
            current_latitude,
            current_longitude,
            last_location_update,
            hire_date,
            base_pay_per_delivery,
            mileage_rate,
        }
    }

    /// Generate new delivery drivers for a specific date (used in nightly mode)
    /// Drivers are typically hired on Mondays with seasonal patterns
    pub fn generate_new_drivers_for_date(&mut self, date: NaiveDate) -> usize {
        // Apply day-of-week and seasonal multipliers
        let weight = self.get_driver_hire_weight(date);

        if weight == 0.0 {
            return 0;
        }

        // Calculate daily hiring rate from driver growth (customer growth + online acceleration)
        let annual_growth_rate = self.get_driver_growth_rate_for_year(date.year());
        let current_driver_count = self.delivery_drivers.len() as f64;
        let base_daily_rate = current_driver_count * annual_growth_rate / 365.0;
        let adjusted_rate = base_daily_rate * weight;

        // Probabilistic hiring
        let num_new = if self.rng.gen::<f64>() < adjusted_rate {
            self.rng.gen_range(1..=2)
        } else {
            0
        };

        if num_new == 0 {
            return 0;
        }

        let next_driver_id = self.delivery_drivers.iter().map(|d| d.driver_id).max().unwrap_or(0) + 1;

        for i in 0..num_new {
            let driver_id = next_driver_id + i as u64;
            let driver = self.create_single_driver(driver_id, date, false); // false = new hire, not founding
            self.delivery_drivers.push(driver);
        }

        num_new
    }

    // Helper method for weighted selection
    fn pick_weighted(&mut self, options: &[(&str, f64)]) -> String {
        Self::pick_weighted_static(&mut self.rng, options)
    }

    // Static version for use in static methods
    fn pick_weighted_static(rng: &mut StdRng, options: &[(&str, f64)]) -> String {
        let rand = rng.gen::<f64>();
        let mut cumulative = 0.0;

        for (value, prob) in options {
            cumulative += prob;
            if rand < cumulative {
                return value.to_string();
            }
        }
        options.last().unwrap().0.to_string()
    }

    fn pick_weighted_u32(&mut self, options: &[(u32, f64)]) -> u32 {
        let rand = self.rng.gen::<f64>();
        let mut cumulative = 0.0;

        for (value, prob) in options {
            cumulative += prob;
            if rand < cumulative {
                return *value;
            }
        }
        options.last().unwrap().0
    }

    pub fn generate_store_economics(&mut self) {
        let mut store_economics = HashMap::new();

        // Count stores per city for competitive intensity
        let mut city_store_counts: HashMap<String, usize> = HashMap::new();
        for store in &self.stores {
            *city_store_counts.entry(store.city.clone()).or_insert(0) += 1;
        }

        // Assign performance tiers (20% high, 60% medium, 20% low)
        let num_stores = self.stores.len();
        let mut performance_assignments: Vec<String> = Vec::new();
        for i in 0..num_stores {
            let tier = if i < num_stores / 5 {
                "high"
            } else if i < (num_stores * 4) / 5 {
                "medium"
            } else {
                "low"
            };
            performance_assignments.push(tier.to_string());
        }
        performance_assignments.shuffle(&mut self.rng);

        for (idx, store) in self.stores.iter().enumerate() {
            // Store maturity factor
            let years_open = (self.start_date - store.opened_date).num_days() as f64 / 365.0;
            let maturity_factor = if years_open < 0.0 {
                // Store opens during data range
                let years_from_now = years_open.abs();
                if years_from_now < 1.0 {
                    1.15  // Brand new
                } else if years_from_now < 2.0 {
                    1.10
                } else {
                    1.05
                }
            } else {
                // Store already open at start
                if years_open < 2.0 {
                    1.08
                } else if years_open < 4.0 {
                    1.00
                } else if years_open < 7.0 {
                    0.95
                } else {
                    0.92  // Very mature, highly efficient
                }
            };

            // Shrinkage rate (theft, damage, spoilage)
            let base_shrinkage = match store.store_type.as_str() {
                "urban" => 0.030,      // Higher theft in urban areas
                "convenience" => 0.025, // Higher due to less security
                "suburban" => 0.018,
                "big_box" => 0.015,
                "online" => 0.012,     // Lowest, controlled environment
                _ => 0.020,
            };
            let shrinkage_rate = base_shrinkage * self.rng.gen_range(0.90..1.10);

            // Competitive intensity (based on store density in city)
            let store_count_in_city = *city_store_counts.get(&store.city).unwrap_or(&1);
            let competitive_intensity = if store_count_in_city > 5 {
                self.rng.gen_range(1.08..1.12)  // High competition
            } else if store_count_in_city > 2 {
                self.rng.gen_range(1.02..1.06)  // Moderate competition
            } else {
                self.rng.gen_range(0.95..1.00)  // Low competition (market leader)
            };

            // Price premium index
            let price_premium_index = match store.store_type.as_str() {
                "convenience" => self.rng.gen_range(1.08..1.15),  // Convenience premium
                "urban" => self.rng.gen_range(1.03..1.10),        // Urban premium
                "online" => self.rng.gen_range(0.97..1.02),       // Competitive online
                "big_box" => self.rng.gen_range(0.95..0.98),      // Discount positioning
                "suburban" => self.rng.gen_range(0.98..1.03),     // Neutral
                _ => 1.00,
            };

            // Volume discount tier (better COGS for high-volume stores)
            let volume_discount_tier = match store.store_type.as_str() {
                "online" => self.rng.gen_range(0.92..0.94),    // Best terms
                "big_box" => self.rng.gen_range(0.94..0.96),   // Very good terms
                "suburban" => self.rng.gen_range(0.97..0.99),  // Good terms
                "urban" => self.rng.gen_range(0.99..1.01),     // Standard terms
                "convenience" => self.rng.gen_range(1.01..1.03), // Worst terms (low volume)
                _ => 1.00,
            };

            // Performance tier
            let store_performance_tier = performance_assignments[idx].clone();

            // Category mix factors by store type
            let mut category_mix_factors = HashMap::new();
            match store.store_type.as_str() {
                "urban" => {
                    category_mix_factors.insert("beverages".to_string(), 1.3);
                    category_mix_factors.insert("snacks".to_string(), 1.4);
                    category_mix_factors.insert("personal_care".to_string(), 1.2);
                    category_mix_factors.insert("produce".to_string(), 0.7);
                    category_mix_factors.insert("meat".to_string(), 0.6);
                    category_mix_factors.insert("household".to_string(), 0.9);
                }
                "suburban" => {
                    category_mix_factors.insert("dairy".to_string(), 1.3);
                    category_mix_factors.insert("meat".to_string(), 1.4);
                    category_mix_factors.insert("produce".to_string(), 1.3);
                    category_mix_factors.insert("household".to_string(), 1.2);
                    category_mix_factors.insert("snacks".to_string(), 1.1);
                    category_mix_factors.insert("frozen".to_string(), 1.2);
                }
                "convenience" => {
                    category_mix_factors.insert("beverages".to_string(), 1.5);
                    category_mix_factors.insert("snacks".to_string(), 1.6);
                    category_mix_factors.insert("candy".to_string(), 1.3);
                    category_mix_factors.insert("produce".to_string(), 0.5);
                    category_mix_factors.insert("meat".to_string(), 0.4);
                }
                "big_box" => {
                    category_mix_factors.insert("household".to_string(), 1.3);
                    category_mix_factors.insert("frozen".to_string(), 1.2);
                    category_mix_factors.insert("canned".to_string(), 1.2);
                    category_mix_factors.insert("personal_care".to_string(), 1.1);
                }
                "online" => {
                    category_mix_factors.insert("household".to_string(), 1.5);
                    category_mix_factors.insert("personal_care".to_string(), 1.4);
                    category_mix_factors.insert("canned".to_string(), 1.3);
                    category_mix_factors.insert("frozen".to_string(), 1.2);
                    category_mix_factors.insert("produce".to_string(), 0.5);
                    category_mix_factors.insert("meat".to_string(), 0.6);
                    category_mix_factors.insert("dairy".to_string(), 0.7);
                }
                _ => {}
            }

            store_economics.insert(store.store_id, StoreEconomics {
                maturity_factor,
                shrinkage_rate,
                competitive_intensity,
                price_premium_index,
                volume_discount_tier,
                store_performance_tier,
                category_mix_factors,
            });
        }

        self.store_economics = store_economics;
        println!("Generated store economics for {} stores", self.stores.len());
    }

    pub fn generate_delivery_zones(&mut self) {
        println!("Generating delivery zones...");

        let mut zones = Vec::new();
        let mut zone_id = 1u64;

        // Create zones for each physical store (not online)
        for store in &self.stores {
            if store.store_type == "online" {
                continue;
            }

            // Each store gets 2-4 delivery zones radiating outward
            let num_zones = self.rng.gen_range(2..=4);

            for zone_num in 1..=num_zones {
                let zone_name = format!("{} Zone {}", store.city, zone_num);

                // Zones get progressively larger and farther from store
                let (_min_radius, max_radius) = match zone_num {
                    1 => (0.0, 3.0),      // Inner zone: 0-3 miles
                    2 => (3.0, 7.0),      // Middle zone: 3-7 miles
                    3 => (7.0, 12.0),     // Outer zone: 7-12 miles
                    _ => (12.0, 20.0),    // Extended zone: 12-20 miles
                };

                // Delivery fee increases with distance
                let base_delivery_fee = match zone_num {
                    1 => 2.99,
                    2 => 4.99,
                    3 => 7.99,
                    _ => 9.99,
                };

                // Minimum order increases with distance
                let min_order_amount = match zone_num {
                    1 => 25.0,
                    2 => 35.0,
                    3 => 50.0,
                    _ => 75.0,
                };

                // Estimated delivery time increases with distance
                let avg_delivery_time_minutes = match zone_num {
                    1 => self.rng.gen_range(25..35),
                    2 => self.rng.gen_range(35..50),
                    3 => self.rng.gen_range(50..70),
                    _ => self.rng.gen_range(70..90),
                };

                // Zone is active if store supports delivery
                let is_active = true; // All zones active by default

                let zone = DeliveryZone {
                    zone_id: zone_id as u32,
                    zone_name,
                    store_id: store.store_id,
                    center_latitude: store.latitude,
                    center_longitude: store.longitude,
                    radius_miles: max_radius,
                    delivery_fee: base_delivery_fee,
                    min_order_amount,
                    free_delivery_threshold: min_order_amount * 2.0,
                    estimated_delivery_time_minutes: avg_delivery_time_minutes,
                    is_active,
                    service_hours_start: "08:00".to_string(),
                    service_hours_end: "22:00".to_string(),
                    avg_daily_orders: self.rng.gen_range(10..50),
                    peak_hours: "17,18,19".to_string(),
                };

                zones.push(zone);
                zone_id += 1;
            }
        }

        self.delivery_zones = zones;
        println!("  Generated {} delivery zones", self.delivery_zones.len());
    }

    pub fn generate_delivery_drivers(&mut self) {
        // Calculate base drivers needed based on store count
        let base_drivers = self.stores.iter()
            .map(|s| match s.store_type.as_str() {
                "urban" => DRIVERS_PER_STORE_URBAN,
                "suburban" => DRIVERS_PER_STORE_SUBURBAN,
                "big_box" => DRIVERS_PER_STORE_BIG_BOX,
                "convenience" => DRIVERS_PER_STORE_CONVENIENCE,
                "online" => DRIVERS_FULFILLMENT_CENTER,
                _ => 2,
            })
            .sum::<usize>();

        // Calculate driver growth year-by-year using customer growth + online acceleration
        // This ties driver demand to actual business drivers
        let total_days = (self.end_date - self.start_date).num_days();
        let years = total_days as f64 / 365.0;

        let mut total_growth = 0.0;
        let mut current_base = base_drivers as f64;
        let mut current_date = self.start_date;
        let mut year_rates: Vec<(i32, f64)> = Vec::new();

        while current_date <= self.end_date {
            let year = current_date.year();
            let annual_rate = self.get_driver_growth_rate_for_year(year);

            // Calculate end of this year chunk
            let year_end = NaiveDate::from_ymd_opt(year, 12, 31).unwrap();
            let chunk_end = if year_end < self.end_date { year_end } else { self.end_date };

            let days_in_chunk = (chunk_end - current_date).num_days() + 1;
            let year_fraction = days_in_chunk as f64 / 365.0;

            // Growth for this chunk (compounding)
            let chunk_growth = current_base * annual_rate * year_fraction;
            total_growth += chunk_growth;
            current_base += chunk_growth;

            year_rates.push((year, annual_rate));
            current_date = chunk_end + Duration::days(1);
        }

        let total_growth = total_growth as usize;
        let avg_rate = year_rates.iter().map(|(_, r)| r).sum::<f64>() / year_rates.len() as f64;

        let num_drivers = base_drivers + total_growth;

        println!("Generating {} delivery drivers ({} base + {} net hiring over {:.2} years)...",
                 num_drivers, base_drivers, total_growth, years);
        println!("  Year-by-year rates (customer + online): {:?}",
                 year_rates.iter().map(|(y, r)| format!("{}: {:.1}%", y, r * 100.0)).collect::<Vec<_>>());
        println!("  Average rate: {:.2}%", avg_rate * 100.0);

        // Build weighted date distribution for driver hiring (Mondays/Fridays with seasonal patterns)
        let total_sim_days = (self.end_date - self.start_date).num_days() as usize;
        let mut hire_date_weights: Vec<(NaiveDate, f64)> = Vec::new();
        let mut total_hire_weight = 0.0;

        for day_offset in 0..=total_sim_days {
            let date = self.start_date + Duration::days(day_offset as i64);
            let weight = self.get_driver_hire_weight(date);
            if weight > 0.0 {
                total_hire_weight += weight;
                hire_date_weights.push((date, weight));
            }
        }

        // Build cumulative distribution for sampling
        let mut hire_cumulative_weights: Vec<f64> = Vec::with_capacity(hire_date_weights.len());
        let mut cumsum = 0.0;
        for (_, weight) in &hire_date_weights {
            cumsum += weight / total_hire_weight;
            hire_cumulative_weights.push(cumsum);
        }

        let mut drivers = Vec::new();

        for driver_id in 1..=num_drivers as u64 {
            // Determine hire_date first:
            // - First base_drivers: existing drivers (hired before start_date) - founding drivers
            // - Remaining drivers: sampled from weighted distribution (Mondays/Fridays, seasonal)
            let (hire_date, is_founding) = if driver_id <= base_drivers as u64 {
                // Existing driver: hired 30-1095 days before start_date
                (self.start_date - Duration::days(self.rng.gen_range(30..1095)), true)
            } else {
                // New hire: sample from weighted distribution
                let r = self.rng.gen::<f64>();
                let idx = hire_cumulative_weights.iter()
                    .position(|&cw| r <= cw)
                    .unwrap_or(hire_cumulative_weights.len() - 1);
                (hire_date_weights[idx].0, true) // Still founding (has historical metrics)
            };

            let driver = self.create_single_driver(driver_id, hire_date, is_founding);
            drivers.push(driver);
        }

        self.delivery_drivers = drivers;
        println!("  Generated {} delivery drivers", self.delivery_drivers.len());
    }

    pub fn generate_calendar(&mut self) {
        for date in &self.dates {
            let dow = date.weekday().num_days_from_monday();
            let month = date.month();
            let season = match month {
                3..=5 => "spring",
                6..=8 => "summer",
                9..=11 => "fall",
                _ => "winter",
            };

            self.calendar.insert(*date, Calendar {
                date: *date,
                dow,
                is_weekend: dow >= 5,
                is_holiday_us: false,
                is_holiday_canada: false,
                is_holiday_uk: false,
                month,
                week_of_year: date.iso_week().week(),
                season: season.to_string(),
                event_name_us: None,
                event_name_canada: None,
                event_name_uk: None,
            });
        }
    }

    pub fn generate_ground_truth_events(&mut self) {
        self.ground_truth_events = vec![
            // COVID-19 Pandemic Events
            GroundTruthEvent {
                event_id: 1,
                start_date: NaiveDate::from_ymd_opt(2020, 3, 15).unwrap(),
                end_date: NaiveDate::from_ymd_opt(2020, 4, 15).unwrap(),
                region: None,
                sku: None,
                label: "covid_panic_buying".to_string(),
                magnitude: 0.8,
                notes: "COVID-19 panic buying - toilet paper, canned goods, cleaning supplies".to_string(),
            },
            GroundTruthEvent {
                event_id: 2,
                start_date: NaiveDate::from_ymd_opt(2020, 4, 16).unwrap(),
                end_date: NaiveDate::from_ymd_opt(2021, 6, 30).unwrap(),
                region: None,
                sku: None,
                label: "covid_lockdown".to_string(),
                magnitude: 0.6,
                notes: "COVID-19 lockdowns - increased at-home consumption".to_string(),
            },
            // Supply Chain Crisis
            GroundTruthEvent {
                event_id: 3,
                start_date: NaiveDate::from_ymd_opt(2021, 7, 1).unwrap(),
                end_date: NaiveDate::from_ymd_opt(2022, 6, 30).unwrap(),
                region: None,
                sku: None,
                label: "supply_chain_crisis".to_string(),
                magnitude: 0.7,
                notes: "Global supply chain disruptions - port congestion, shipping delays".to_string(),
            },
            // Inflation Surge
            GroundTruthEvent {
                event_id: 4,
                start_date: NaiveDate::from_ymd_opt(2021, 9, 1).unwrap(),
                end_date: NaiveDate::from_ymd_opt(2023, 6, 30).unwrap(),
                region: None,
                sku: None,
                label: "inflation_surge".to_string(),
                magnitude: 0.5,
                notes: "High inflation period - rising food and energy costs".to_string(),
            },
            // Labor Shortage
            GroundTruthEvent {
                event_id: 5,
                start_date: NaiveDate::from_ymd_opt(2021, 6, 1).unwrap(),
                end_date: NaiveDate::from_ymd_opt(2022, 12, 31).unwrap(),
                region: None,
                sku: None,
                label: "labor_shortage".to_string(),
                magnitude: 0.4,
                notes: "Labor shortage affecting retail operations and service levels".to_string(),
            },
            // Ukraine War Impact
            GroundTruthEvent {
                event_id: 6,
                start_date: NaiveDate::from_ymd_opt(2022, 2, 24).unwrap(),
                end_date: NaiveDate::from_ymd_opt(2023, 12, 31).unwrap(),
                region: None,
                sku: None,
                label: "ukraine_war_impact".to_string(),
                magnitude: 0.3,
                notes: "Ukraine war impact on grain prices and supply".to_string(),
            },
            // Recession Fears
            GroundTruthEvent {
                event_id: 7,
                start_date: NaiveDate::from_ymd_opt(2022, 6, 1).unwrap(),
                end_date: NaiveDate::from_ymd_opt(2023, 3, 31).unwrap(),
                region: None,
                sku: None,
                label: "recession_fears".to_string(),
                magnitude: 0.4,
                notes: "Economic recession fears - consumers trading down to value brands".to_string(),
            },
            // Post-COVID Normalization
            GroundTruthEvent {
                event_id: 8,
                start_date: NaiveDate::from_ymd_opt(2023, 4, 1).unwrap(),
                end_date: NaiveDate::from_ymd_opt(2024, 12, 31).unwrap(),
                region: None,
                sku: None,
                label: "normalization".to_string(),
                magnitude: 0.15,
                notes: "Post-pandemic normalization - return to pre-COVID patterns".to_string(),
            },
            // AI/Automation Era
            GroundTruthEvent {
                event_id: 9,
                start_date: NaiveDate::from_ymd_opt(2024, 1, 1).unwrap(),
                end_date: NaiveDate::from_ymd_opt(2025, 11, 30).unwrap(),
                region: None,
                sku: None,
                label: "ai_automation".to_string(),
                magnitude: 0.2,
                notes: "AI and automation improving efficiency and online shopping experience".to_string(),
            },
        ];
    }

    pub fn generate_promotions(&mut self) {
        let mut promotions = Vec::new();
        let mut promo_products: Vec<_> = self.products.iter().collect();
        promo_products.sort_by(|a, b| b.pareto_weight.partial_cmp(&a.pareto_weight).unwrap());

        for (promo_id, product) in promo_products.iter().take(50).enumerate() {
            // Handle case where dates range is too small (e.g., continue mode with single date)
            // Ensure we have a valid range by using max(1, len - 15) for the upper bound
            let max_start_day = self.dates.len().saturating_sub(15).max(1);
            let start_day = if max_start_day > 0 {
                self.rng.gen_range(0..max_start_day)
            } else {
                0
            };

            promotions.push(Promotion {
                promo_id: (promo_id + 1) as u32,
                sku: product.sku.clone(),
                start_date: self.dates[start_day],
                end_date: self.dates[start_day] + Duration::days(14),
                promo_type: Self::get_promotion_type_codes().choose(&mut self.rng).unwrap().clone(),
                discount_pct: 20,
                ad_feature: false,
                display_type: "none".to_string(),
                expected_uplift: 1.2,
                supplier_funding_usd: 0.0,
            });
        }
        self.promotions = promotions;
    }

    pub fn generate_assortment(&mut self) {
        let mut assortment = Vec::new();
        for store in &self.stores {
            // Use coverage constants
            let coverage = match store.store_type.as_str() {
                "online" => ONLINE_COVERAGE,
                "big_box" => BIG_BOX_COVERAGE,
                "suburban" => SUBURBAN_COVERAGE,
                "urban" => URBAN_COVERAGE,
                "convenience" => CONVENIENCE_COVERAGE,
                _ => 0.7, // Default fallback
            };
            let num_skus = (self.products.len() as f64 * coverage) as usize;

            for product in self.products.iter().take(num_skus) {
                // Facings based on product popularity (pareto_weight)
                // High popularity (top 20%): 3-4 facings
                // Medium popularity (next 30%): 2-3 facings
                // Low popularity (bottom 50%): 1-2 facings
                let facings = if product.pareto_weight > 0.01 {
                    self.rng.gen_range(3..=4)
                } else if product.pareto_weight > 0.001 {
                    self.rng.gen_range(2..=3)
                } else {
                    self.rng.gen_range(1..=2)
                };

                // Shelf height varies by category
                let shelf_height = match product.category.as_str() {
                    "cereal" | "snacks" | "canned" => self.rng.gen_range(180.0..220.0), // Eye level
                    "beverages" => self.rng.gen_range(120.0..180.0), // Lower (heavy items)
                    "dairy" | "frozen" => self.rng.gen_range(80.0..160.0), // Refrigerated cases
                    "produce" => self.rng.gen_range(60.0..120.0), // Low displays
                    "meat" => self.rng.gen_range(80.0..140.0), // Refrigerated cases
                    "bakery" => self.rng.gen_range(100.0..160.0), // Mid-level
                    "personal_care" | "household" => self.rng.gen_range(140.0..200.0), // Upper shelves
                    _ => self.rng.gen_range(120.0..180.0), // Default mid-range
                };

                assortment.push(Assortment {
                    store_id: store.store_id,
                    sku: product.sku.clone(),
                    active_from: self.start_date,
                    active_to: None,
                    planogram_facings: facings,
                    shelf_height_cm: Self::round_rate(shelf_height), // Round to 4 decimals
                });
            }
        }
        self.assortment = assortment;
    }

    // Static helper that doesn't borrow self
    fn maybe_link_customer_static(
        rng: &mut StdRng,
        store: &Store,
        store_type: &str,
        store_to_customers: &HashMap<u32, Vec<&Customer>>,
        city_to_customers: &HashMap<&str, Vec<&Customer>>,
        all_customers: &[Customer],
    ) -> (Option<u64>, bool, u32, u32) {
        if all_customers.is_empty() {
            return (None, false, 0, 0);
        }

        // Determine tracking probability based on store type
        let tracking_prob = match store_type {
            "online" => 0.95,  // 95% of online orders tracked
            "big_box" => 0.43,
            "suburban" => 0.38,
            "urban" => 0.35,
            "convenience" => 0.28,
            _ => 0.38,
        };

        if rng.gen::<f64>() > tracking_prob {
            return (None, false, 0, 0);
        }

        // Use pre-built indexes for fast lookup
        let eligible_customers: Vec<&Customer> = store_to_customers
            .get(&store.store_id).cloned()
            .or_else(|| city_to_customers.get(store.city.as_str()).cloned())
            .unwrap_or_default();

        if eligible_customers.is_empty() {
            // Fallback to any customer
            if let Some(customer) = all_customers.choose(rng) {
                let loyalty_points = if customer.loyalty_member {
                    rng.gen_range(5..50)
                } else {
                    0
                };

                return (
                    Some(customer.customer_id),
                    customer.loyalty_member,
                    loyalty_points,
                    0,
                );
            }
            return (None, false, 0, 0);
        }

        // Pick a customer with store affinity
        if let Some(customer) = eligible_customers.choose(rng) {
            let loyalty_points = if customer.loyalty_member {
                rng.gen_range(5..50)
            } else {
                0
            };

            (
                Some(customer.customer_id),
                customer.loyalty_member,
                loyalty_points,
                0,
            )
        } else {
            (None, false, 0, 0)
        }
    }

    fn create_delivery_assignment_static(
        rng: &mut StdRng,
        writers: &mut StreamingWriters,
        transaction_id: u64,
        store_id: u32,
        _fulfillment_type: &str,
        date: &NaiveDate,
        timestamp: &str,
        _delivery_time_minutes: u32,
        order_value: f64,
        delivery_drivers: &[DeliveryDriver],
        stores: &[Store],
    ) -> Result<()> {
        if delivery_drivers.is_empty() {
            return Ok(());
        }

        // Find active drivers for this store's city
        let store = stores.iter().find(|s| s.store_id == store_id);
        if store.is_none() {
            return Ok(());
        }
        let store = store.unwrap();

        // Add temporal variation to driver availability
        let day_of_week = date.weekday().num_days_from_monday();
        let is_weekend = day_of_week >= 5;
        let month = date.month();

        // Seasonal availability patterns
        let seasonal_availability_multiplier = match month {
            11 | 12 => 1.3,  // Holiday season - more drivers active
            6..=8 => 1.1, // Summer - slightly more active
            1 | 2 => 0.9,     // Winter slowdown
            _ => 1.0,
        };

        // Weekend patterns - more drivers available
        let weekend_multiplier = if is_weekend { 1.2 } else { 1.0 };

        let eligible_drivers: Vec<DeliveryDriver> = delivery_drivers.iter()
            .filter(|d| {
                // Dynamic availability based on day/season
                let base_availability = if d.is_available { 0.75 } else { 0.15 };
                let adjusted_availability = base_availability * seasonal_availability_multiplier * weekend_multiplier;

                // Driver must serve this city and be "available" for this specific day
                d.service_cities.contains(&store.city) && rng.gen::<f64>() < adjusted_availability
            })
            .cloned()
            .collect();

        if eligible_drivers.is_empty() {
            return Ok(());
        }

        let driver = eligible_drivers.choose(rng).unwrap().clone();

        // Parse timestamp to calculate pickup/delivery times
        let order_time = NaiveDateTime::parse_from_str(timestamp, "%Y-%m-%d %H:%M:%S")
            .unwrap_or_else(|_| date.and_hms_opt(12, 0, 0).unwrap());

        let hour = order_time.hour();

        // Time-of-day affects acceptance and pickup times
        let is_peak_hours = (11..=13).contains(&hour) || (17..=19).contains(&hour);
        let is_late_night = hour >= 22 || hour <= 5;

        let assigned_at = order_time;

        // Acceptance time varies by time of day
        let acceptance_delay = if is_peak_hours {
            rng.gen_range(2..8)  // Busier during peak
        } else if is_late_night {
            rng.gen_range(5..15) // Slower at night
        } else {
            rng.gen_range(1..5)
        };
        let accepted_at = Some(order_time + Duration::minutes(acceptance_delay as i64));

        // Pickup time also varies
        let pickup_delay = if is_peak_hours {
            rng.gen_range(15..30) // Store is busier
        } else {
            rng.gen_range(10..20)
        };
        let picked_up_at = Some(order_time + Duration::minutes(pickup_delay as i64));

        let distance_miles = Self::round_rate(rng.gen_range(1.0..12.0));

        // Traffic patterns affect delivery time
        let traffic_multiplier = if is_peak_hours {
            rng.gen_range(1.3..1.6) // Rush hour traffic
        } else if is_late_night {
            rng.gen_range(0.8..0.9) // Light traffic
        } else if is_weekend {
            rng.gen_range(0.9..1.1) // Moderate weekend traffic
        } else {
            rng.gen_range(1.0..1.2) // Normal traffic
        };

        let base_duration = (distance_miles / 25.0 * 60.0) as u32;
        let estimated_duration_minutes = (base_duration as f64 * traffic_multiplier) as u32 + rng.gen_range(5..15);

        // Weather/seasonal delays
        let seasonal_delay = match month {
            12 | 1 | 2 => rng.gen_range(0..10), // Winter weather delays
            _ => 0,
        };

        let actual_duration_minutes = if rng.gen::<f64>() < 0.92 {
            // On time - within estimate
            Some(estimated_duration_minutes + rng.gen_range(0..10) + seasonal_delay)
        } else {
            // Late
            Some(estimated_duration_minutes + rng.gen_range(10..30) + seasonal_delay)
        };

        let delivered_at = picked_up_at.map(|p| p + Duration::minutes(actual_duration_minutes.unwrap_or(estimated_duration_minutes) as i64));

        let assignment_status = if rng.gen::<f64>() < 0.97 {
            "delivered"
        } else if rng.gen::<f64>() < 0.5 {
            "cancelled"
        } else {
            "in_progress"
        };

        let cancelled_at = if assignment_status == "cancelled" {
            Some(order_time + Duration::minutes(rng.gen_range(5..30) as i64))
        } else {
            None
        };

        let cancellation_reason = if assignment_status == "cancelled" {
            Some(Self::pick_weighted_static(rng, &[
                ("customer_request", 0.40),
                ("driver_unavailable", 0.30),
                ("address_issue", 0.20),
                ("other", 0.10),
            ]))
        } else {
            None
        };

        // Calculate compensation with temporal variation
        let driver_pay = Self::round_currency(driver.base_pay_per_delivery + (distance_miles * driver.mileage_rate));

        // Tipping varies by time and season
        let tip_likelihood = if is_weekend {
            0.80 // Better tips on weekends
        } else if month == 12 {
            0.85 // Holiday generosity
        } else if is_late_night {
            0.70 // Fewer tips late night
        } else {
            0.75
        };

        let tip_percentage = if is_weekend || month == 12 {
            rng.gen_range(0.12..0.22) // Higher tips
        } else {
            rng.gen_range(0.10..0.20)
        };

        let driver_tip = Self::round_currency(if assignment_status == "delivered" && rng.gen::<f64>() < tip_likelihood {
            order_value * tip_percentage
        } else if assignment_status == "delivered" {
            order_value * rng.gen_range(0.0..0.10)
        } else {
            0.0
        });
        let driver_total_earnings = Self::round_currency(driver_pay + driver_tip);

        // Customer rating (1-5 stars, mostly 4-5)
        let customer_rating = if assignment_status == "delivered" {
            // Customer ratings heavily skewed toward 5 stars
            // 70% give 5 stars, 20% give 4 stars, 10% give 1-3 stars
            let rating_rand = rng.gen::<f64>();
            Some(if rating_rand < 0.70 {
                5
            } else if rating_rand < 0.90 {
                4
            } else if rating_rand < 0.95 {
                3
            } else if rating_rand < 0.98 {
                2
            } else {
                1
            })
        } else {
            None
        };

        let estimated_pickup_time = order_time + Duration::minutes(15);
        let actual_pickup_time = picked_up_at;
        let estimated_delivery_time = estimated_pickup_time + Duration::minutes(estimated_duration_minutes as i64);
        let actual_delivery_time = delivered_at;

        let assignment = DeliveryAssignment {
            assignment_id: transaction_id,
            transaction_id,
            driver_id: driver.driver_id,
            assigned_at,
            accepted_at,
            picked_up_at,
            delivered_at,
            cancelled_at,
            assignment_status: assignment_status.to_string(),
            cancellation_reason,
            pickup_store_id: store_id,
            estimated_pickup_time,
            actual_pickup_time,
            estimated_delivery_time,
            actual_delivery_time,
            distance_miles,
            estimated_duration_minutes,
            actual_duration_minutes,
            driver_pay,
            driver_tip,
            driver_total_earnings,
            customer_rating,
            driver_notes: None,
            customer_feedback: None,
        };

        writers.write_delivery_assignment(&assignment)?;

        Ok(())
    }

    pub fn save_data(&mut self, output_dir: &str, continue_mode: bool, reference_dir: Option<&str>) -> Result<()> {
        println!("============================================================");
        println!("ShelfWise Data Generator - Rust COMPLETE VERSION");
        println!("============================================================\n");

        // Load reference data from directory if provided (for nightly imports)
        if let Some(ref_dir) = reference_dir {
            self.load_reference_from_dir(ref_dir)?;
        }

        // Generate any data that wasn't loaded
        if self.products.is_empty() { self.generate_products(); }
        if self.stores.is_empty() { self.generate_stores(); }
        if self.store_economics.is_empty() { self.generate_store_economics(); }
        if self.customers.is_empty() { self.generate_customers(); }
        if self.customer_addresses.is_empty() { self.generate_customer_addresses(); }
        if self.delivery_zones.is_empty() { self.generate_delivery_zones(); }
        if self.delivery_drivers.is_empty() { self.generate_delivery_drivers(); }
        if self.calendar.is_empty() { self.generate_calendar(); }
        if self.ground_truth_events.is_empty() { self.generate_ground_truth_events(); }
        if self.promotions.is_empty() { self.generate_promotions(); }
        if self.assortment.is_empty() { self.generate_assortment(); }

        // Always ensure output directory exists, even in continue mode
        std::fs::create_dir_all(output_dir)?;

        // In nightly/continue mode with reference data, generate new customers/drivers
        // ONLY for dates after the max created_date/hire_date in reference data
        if continue_mode && reference_dir.is_some() {
            // Find the max created_date from loaded customers (the "end" of pre-generated data)
            // Note: founding customers have None, so we filter those out
            let max_customer_date = self.customers.iter()
                .filter_map(|c| c.created_date)
                .max()
                .unwrap_or(self.start_date);

            let max_driver_date = self.delivery_drivers.iter()
                .map(|d| d.hire_date)
                .max()
                .unwrap_or(self.start_date);

            println!("\n📈 Checking organic growth for date range...");
            println!("   Reference data covers customers through: {}", max_customer_date);
            println!("   Reference data covers drivers through: {}", max_driver_date);

            let mut total_new_customers = 0;
            let mut total_new_drivers = 0;

            for date in self.dates.clone() {
                // Only generate new customers for dates AFTER the pre-generated data
                if date > max_customer_date {
                    total_new_customers += self.generate_new_customers_for_date(date);
                }
                // Only generate new drivers for dates AFTER the pre-generated data
                if date > max_driver_date {
                    total_new_drivers += self.generate_new_drivers_for_date(date);
                }
            }

            if total_new_customers > 0 || total_new_drivers > 0 {
                println!("  Created {} new customers (for dates after {})", total_new_customers, max_customer_date);
                println!("  Hired {} new drivers (for dates after {})", total_new_drivers, max_driver_date);
            } else {
                println!("  No new customers/drivers needed (dates already covered by reference data)");
            }
        }

        if !continue_mode {
            println!("Saving reference data...");
            self.save_reference_data(output_dir)?;
        }

        println!("\nGenerating daily data with ALL operational data...");
        self.generate_daily_data_complete(output_dir, continue_mode)?;

        println!("\n============================================================");
        println!("COMPLETE! All operational data generated.");
        println!("============================================================");
        Ok(())
    }

    fn save_reference_data(&self, output_dir: &str) -> Result<()> {
        // Write seed reference data (regions, categories, etc.)
        crate::reference_data::write_reference_data_csvs(output_dir)?;

        let mut wtr = csv::Writer::from_path(Path::new(output_dir).join("products.csv"))?;
        for p in &self.products { wtr.serialize(p)?; }
        wtr.flush()?;

        let mut wtr = csv::Writer::from_path(Path::new(output_dir).join("stores.csv"))?;
        for s in &self.stores { wtr.serialize(s)?; }
        wtr.flush()?;

        let mut wtr = csv::Writer::from_path(Path::new(output_dir).join("promotions.csv"))?;
        for p in &self.promotions { wtr.serialize(p)?; }
        wtr.flush()?;

        let mut wtr = csv::Writer::from_path(Path::new(output_dir).join("assortment.csv"))?;
        for a in &self.assortment { wtr.serialize(a)?; }
        wtr.flush()?;

        // Write customer data - founding customers (NULL date) + customers created before or on start_date
        // (New customers created during the date range will be added by nightly imports)
        if !self.customers.is_empty() {
            let mut wtr = csv::Writer::from_path(Path::new(output_dir).join("customers.csv"))?;
            let existing_customers: Vec<&Customer> = self.customers.iter()
                .filter(|c| c.created_date.is_none_or(|d| d <= self.start_date))
                .collect();

            println!("  Writing {} existing customers (founding or created <= {})",
                     existing_customers.len(), self.start_date);
            println!("  {} future customers will be added during nightly imports",
                     self.customers.len() - existing_customers.len());

            for c in existing_customers { wtr.serialize(c)?; }
            wtr.flush()?;
        }

        // Write customer addresses - ONLY for existing customers
        if !self.customer_addresses.is_empty() {
            let existing_customer_ids: std::collections::HashSet<u64> = self.customers.iter()
                .filter(|c| c.created_date.is_none_or(|d| d <= self.start_date))
                .map(|c| c.customer_id)
                .collect();

            let mut wtr = csv::Writer::from_path(Path::new(output_dir).join("customer_addresses.csv"))?;
            let existing_addresses: Vec<&CustomerAddress> = self.customer_addresses.iter()
                .filter(|a| existing_customer_ids.contains(&a.customer_id))
                .collect();

            println!("  Writing {} existing customer addresses", existing_addresses.len());

            for a in existing_addresses { wtr.serialize(a)?; }
            wtr.flush()?;
        }

        // Write delivery zones
        if !self.delivery_zones.is_empty() {
            let mut wtr = csv::Writer::from_path(Path::new(output_dir).join("delivery_zones.csv"))?;
            for z in &self.delivery_zones { wtr.serialize(z)?; }
            wtr.flush()?;
        }

        // Write delivery drivers - ONLY drivers hired before or on start_date
        // (New drivers hired during the date range will be added by nightly imports)
        if !self.delivery_drivers.is_empty() {
            let mut wtr = csv::Writer::from_path(Path::new(output_dir).join("delivery_drivers.csv"))?;
            let existing_drivers: Vec<&DeliveryDriver> = self.delivery_drivers.iter()
                .filter(|d| d.hire_date <= self.start_date)
                .collect();

            println!("  Writing {} existing drivers (hired <= {})",
                     existing_drivers.len(), self.start_date);
            println!("  {} future drivers will be added during nightly imports",
                     self.delivery_drivers.len() - existing_drivers.len());

            for d in existing_drivers { wtr.serialize(d)?; }
            wtr.flush()?;
        }

        Ok(())
    }

    fn generate_daily_data_complete(&mut self, output_dir: &str, continue_mode: bool) -> Result<()> {
        let mut writers = StreamingWriters::with_batch_size(
            output_dir,
            continue_mode,
            self.config.performance.batch_size
        )?;
        // Track inventory with proper supply chain state
        // (store_id, sku) -> (on_hand, on_order, pending_orders: Vec<(delivery_date, quantity)>)
        let mut inventory: HashMap<(u32, &str), (u32, u32, Vec<(NaiveDate, u32)>)> = HashMap::new();

        // Track demand history for calculating reorder points
        // (store_id, sku) -> Vec<daily_demand> (last 30 days)
        let mut demand_history: HashMap<(u32, &str), Vec<u32>> = HashMap::new();
        let mut shipment_id = 1;
        let mut waste_id = 1;
        let mut ticket_id = 1;
        let mut change_id = 1;
        let mut global_txn_id = 1;

        let total_days = self.dates.len();
        println!("  Generating data for {} days ({} to {})",
                 total_days,
                 self.dates.first().unwrap(),
                 self.dates.last().unwrap());
        println!("  Estimated records: ~{} million",
                 (total_days * self.stores.len() * self.products.len() * 7 / 10) / 1_000_000);

        // Pre-build indexes for faster lookups (one-time cost, huge speedup in loops)
        println!("  Building lookup indexes and caching reference data...");

        // Cache reference data (called millions of times otherwise)
        let return_reasons = Self::get_return_reason_codes();

        let waste_reasons = Self::get_waste_reason_codes();
        let perishable_waste_reasons: Vec<String> = waste_reasons.iter()
            .filter(|r| r.as_str() == "expired" || r.as_str() == "temperature_abuse")
            .cloned()
            .collect();

        let payment_methods = Self::get_payment_method_codes();

        // Index: store_id -> Vec<Assortment>
        let mut store_assortment: HashMap<u32, Vec<&Assortment>> = HashMap::new();
        for assort in &self.assortment {
            store_assortment.entry(assort.store_id).or_default().push(assort);
        }

        // Index: sku -> Product (avoid linear search)
        let mut sku_to_product: HashMap<&str, &Product> = HashMap::new();
        for product in &self.products {
            sku_to_product.insert(&product.sku, product);
        }

        // Index: sku -> Vec<&Promotion> (avoid filtering all promotions every time)
        let mut sku_to_promotions: HashMap<&str, Vec<&Promotion>> = HashMap::new();
        for promo in &self.promotions {
            sku_to_promotions.entry(promo.sku.as_str()).or_default().push(promo);
        }

        // Index: store_id -> Vec<&Customer> (for faster customer linking)
        let mut store_to_customers: HashMap<u32, Vec<&Customer>> = HashMap::new();
        for customer in &self.customers {
            store_to_customers.entry(customer.primary_store_id).or_default().push(customer);
        }

        // Index: city -> Vec<&Customer> (fallback for customer linking)
        let mut city_to_customers: HashMap<&str, Vec<&Customer>> = HashMap::new();
        for customer in &self.customers {
            city_to_customers.entry(customer.primary_city.as_str()).or_default().push(customer);
        }

        println!("  Indexes built. Starting generation...");

        let dates_clone = self.dates.clone();
        let stores_clone = self.stores.clone();

        // Create demand calculator once per day instead of per store
        let demand_calc = DemandCalculator {
            categories: &self.categories,
            holidays: &self.holidays,
            calendar: &self.calendar,
            ground_truth_events: &self.ground_truth_events,
        };

        // Pre-create Normal distributions (expensive to create repeatedly)
        let normal_high = Normal::new(1.20, 0.03).unwrap();
        let normal_medium = Normal::new(1.00, 0.03).unwrap();
        let normal_low = Normal::new(0.78, 0.04).unwrap();

        // Create progress bar
        let pb = ProgressBar::new(total_days as u64);
        pb.set_style(
            ProgressStyle::default_bar()
                .template("[{elapsed_precise}] {bar:40.cyan/blue} {pos}/{len} {msg}")
                .unwrap()
                .progress_chars("=>-")
        );

        for (idx, date) in dates_clone.iter().enumerate() {
            let day_start = std::time::Instant::now();

            // Update progress bar
            pb.set_message(format!("{} ({:.1}%)",
                date,
                (idx as f64 / total_days as f64) * 100.0
            ));
            pb.set_position(idx as u64);

            // Flush periodically to prevent excessive memory usage
            let should_flush = (idx + 1) % self.config.performance.flush_interval_days == 0;

            let mut inventory_time = std::time::Duration::ZERO;
            let _transaction_time = std::time::Duration::ZERO;
            let _aggregation_time = std::time::Duration::ZERO;

            for store in &stores_clone {
                let store_start = std::time::Instant::now();
                // Skip stores that haven't opened yet
                if *date < store.opened_date {
                    continue;
                }

                // Get store economics
                let store_econ = self.store_economics.get(&store.store_id).unwrap();

                // NEW APPROACH: Track available products with their demand-driven quantities
                // This will be used to generate transactions, which will then be aggregated to sales_daily
                let mut available_products: Vec<(String, u32, f64, f64, Option<u32>, f64, f64)> = Vec::new();
                // (sku, units_available, regular_price, net_price, promo_id, discount_per_unit, cost)

                // Use pre-built index instead of filtering
                if let Some(store_assortments) = store_assortment.get(&store.store_id) {
                    for assort in store_assortments {
                        // Use pre-built index instead of linear search
                        if let Some(&product) = sku_to_product.get(assort.sku.as_str()) {
                            // Use pre-built index and only filter by date - keep as references!
                            let active_promos: Vec<&Promotion> = sku_to_promotions
                                .get(product.sku.as_str())
                                .map(|promos| promos.iter()
                                    .filter(|p| p.start_date <= *date && p.end_date >= *date)
                                    .copied()
                                    .collect())
                                .unwrap_or_default();

                        // Apply category mix factor to demand
                        let category_mix_factor = store_econ.category_mix_factors
                            .get(&product.category)
                            .copied()
                            .unwrap_or(1.0);

                        // Pass promotion references - no cloning!
                        let base_demand = demand_calc.calculate_demand(*date, store, product, &active_promos, 85.0, &mut self.rng);

                        // Adjust demand by category mix and store performance
                        // Store performance uses normal distribution within tiers (pre-created distributions)
                        let performance_multiplier: f64 = match store_econ.store_performance_tier.as_str() {
                            "high" => normal_high.sample(&mut self.rng),
                            "low" => normal_low.sample(&mut self.rng),
                            _ => normal_medium.sample(&mut self.rng),
                        };
                        let performance_multiplier = match store_econ.store_performance_tier.as_str() {
                            "high" => performance_multiplier.clamp(1.12, 1.28),
                            "low" => performance_multiplier.clamp(0.68, 0.88),
                            _ => performance_multiplier.clamp(0.92, 1.08),
                        };

                        let demand = (base_demand as f64 * category_mix_factor * performance_multiplier) as u32;

                        // Use &str to avoid cloning SKU
                        let inv_key = (store.store_id, product.sku.as_str());

                        // Initialize inventory with realistic starting levels
                        if let std::collections::hash_map::Entry::Vacant(e) = inventory.entry(inv_key) {
                            let supplier_id = (product.product_id % 30) + 1;
                            let supplier = self.suppliers.iter().find(|s| s.supplier_id == supplier_id).unwrap();

                            let initial_stock = crate::inventory::calculate_initial_inventory(
                                product,
                                demand,
                                supplier.lead_time_days,
                                &mut self.rng
                            );

                            e.insert((initial_stock, 0, Vec::new()));
                            demand_history.insert(inv_key, Vec::new());
                        }

                        // Get current inventory state (avoid cloning pending_orders Vec)
                        let (on_hand, on_order, pending_orders) = inventory.get(&inv_key).unwrap();
                        let mut on_hand = *on_hand;
                        let mut on_order = *on_order;
                        let mut pending_orders = pending_orders.clone();

                        // Update demand history (keep last 30 days) - use drain instead of remove(0)
                        let history = demand_history.get_mut(&inv_key).unwrap();
                        history.push(demand);
                        if history.len() > 30 {
                            history.drain(0..history.len()-30);
                        }

                        // Check for arriving shipments
                        let mut arrived_today = 0;
                        pending_orders.retain(|(delivery_date, quantity)| {
                            if *delivery_date == *date {
                                arrived_today += *quantity;
                                false
                            } else {
                                true
                            }
                        });

                        // REALISTIC SHIPMENT GENERATION:
                        // Even if no pending orders, simulate realistic delivery schedules
                        // High-velocity products get regular deliveries (2-3x per week)
                        // Low-velocity products get occasional deliveries
                        let is_high_velocity = product.pareto_weight > 0.001; // Top ~20% of products
                        let day_of_week = date.weekday().num_days_from_monday();

                        // Delivery days: Monday, Wednesday, Friday are common delivery days
                        let is_delivery_day = day_of_week == 0 || day_of_week == 2 || day_of_week == 4;

                        // Generate realistic shipments even without pending orders
                        // Shipment probability scales with demand - more demand = more frequent restocking
                        if arrived_today == 0 && is_delivery_day {
                            // Base probability by product velocity
                            let base_shipment_probability = if is_high_velocity {
                                0.15 // 15% chance for high-velocity items on delivery days
                            } else {
                                0.03 // 3% chance for low-velocity items
                            };

                            // Scale by demand relative to average (demand of ~3 is typical)
                            // High demand days (holidays, events) trigger more frequent shipments
                            let demand_multiplier = (demand as f64 / 3.0).clamp(0.5, 2.5);
                            let shipment_probability = base_shipment_probability * demand_multiplier;

                            if self.rng.gen::<f64>() < shipment_probability {
                                // Calculate realistic shipment quantity based on demand
                                let avg_daily_demand = if !history.is_empty() {
                                    history.iter().sum::<u32>() as f64 / history.len() as f64
                                } else {
                                    demand as f64
                                };

                                // Order enough for 3-7 days of demand
                                let days_of_supply = self.rng.gen_range(3..=7);
                                arrived_today = ((avg_daily_demand * days_of_supply as f64).ceil() as u32).max(1);
                            }
                        }

                        if arrived_today > 0 {
                            on_hand += arrived_today;
                            on_order = on_order.saturating_sub(arrived_today);

                            // Record shipment
                            let supplier_id = (product.product_id % 30) + 1;
                            let supplier = self.suppliers.iter()
                                .find(|s| s.supplier_id == supplier_id)
                                .unwrap();

                            let lead_time_variance = self.rng.gen_range(-1..=2);
                            let actual_lead_time = (supplier.lead_time_days as i64 + lead_time_variance).max(1);
                            let shipment_date = *date - Duration::days(actual_lead_time);

                            let on_time = self.rng.gen::<f64>() < supplier.reliability_score;
                            let (delivery_date, shipment_status) = if on_time {
                                (*date, "delivered".to_string())
                            } else {
                                let delay_days = self.rng.gen_range(1..=3);
                                (*date + Duration::days(delay_days), "delayed".to_string())
                            };

                            let damage_rate = 1.0 - (self.rng.gen_range(0.0..0.05));
                            let quantity_received = (arrived_today as f64 * damage_rate).round() as u32;
                            let po_number = format!("PO-{:06}", shipment_id);

                            writers.write_shipment(&SupplierShipment {
                                shipment_id,
                                shipment_date,
                                delivery_date,
                                store_id: store.store_id,
                                sku: product.sku.clone(),
                                quantity_shipped: arrived_today,
                                quantity_received,
                                supplier_name: supplier.supplier_name.clone(),
                                po_number,
                                shipment_status,
                            })?;
                            shipment_id += 1;
                        }

                        // Calculate reorder point and check if we need to order
                        let supplier_id = (product.product_id % 30) + 1;
                        let supplier = self.suppliers.iter().find(|s| s.supplier_id == supplier_id).unwrap();

                        let reorder_point = crate::inventory::calculate_reorder_point(
                            history,
                            supplier.lead_time_days as f64,
                            demand
                        );

                        // Apply seasonal buildup multiplier
                        let seasonal_multiplier = crate::inventory::needs_seasonal_buildup(date, product);
                        let adjusted_reorder_point = (reorder_point as f64 * seasonal_multiplier) as u32;

                        // Check if we need to reorder (inventory position < reorder point)
                        let inventory_position = on_hand + on_order;
                        if inventory_position < adjusted_reorder_point && on_order == 0 {
                            // Calculate order quantity
                            let avg_daily_demand = if !history.is_empty() {
                                history.iter().sum::<u32>() as f64 / history.len() as f64
                            } else {
                                demand as f64
                            };

                            let order_qty = crate::inventory::calculate_order_quantity(
                                product,
                                avg_daily_demand,
                                &mut self.rng
                            );

                            // Apply seasonal multiplier to order quantity
                            let final_order_qty = (order_qty as f64 * seasonal_multiplier) as u32;

                            on_order += final_order_qty;

                            // Calculate delivery date
                            let lead_time_variance = self.rng.gen_range(-1..=2);
                            let actual_lead_time = (supplier.lead_time_days as i64 + lead_time_variance).max(1);
                            let delivery_date = *date + Duration::days(actual_lead_time);

                            pending_orders.push((delivery_date, final_order_qty));

                            // Save updated inventory state with new order
                            inventory.insert(inv_key, (on_hand, on_order, pending_orders.clone()));
                        }

                        // Calculate demand-driven available quantity (what could be sold)
                        let units_available = demand.min(on_hand);

                        // DON'T update on_hand yet - we'll do that after transactions are generated
                        // This ensures transactions drive inventory changes
                        // But we DO need to save on_order updates from reordering logic above

                        // Apply store-specific pricing
                        let store_adjusted_price = product.list_price
                            * store_econ.price_premium_index
                            * (1.0 / store_econ.competitive_intensity);

                        let regular_price = store_adjusted_price;
                        let (discount_pct, net_price, promo_id) = if let Some(promo) = active_promos.first() {
                            let net = regular_price * (1.0 - promo.discount_pct as f64 / 100.0);
                            (promo.discount_pct, net, Some(promo.promo_id))
                        } else {
                            (0, regular_price, None)
                        };

                        // Apply store-specific cost structure
                        let store_adjusted_cost = product.cost
                            * store_econ.volume_discount_tier
                            * store_econ.maturity_factor;

                        // Track available products for transaction generation
                        if units_available > 0 {
                            let discount_amount_per_unit = if discount_pct > 0 {
                                regular_price - net_price
                            } else {
                                0.0
                            };
                            available_products.push((
                                product.sku.clone(),
                                units_available,
                                Self::round_currency(regular_price),
                                Self::round_currency(net_price),
                                promo_id,
                                Self::round_currency(discount_amount_per_unit),
                                Self::round_currency(store_adjusted_cost),
                            ));
                        }

                        // Get current inventory state for reporting
                        let (current_on_hand, current_on_order, pending) = inventory.get(&inv_key).unwrap();

                        // Calculate in_transit (orders not yet delivered)
                        let in_transit: u32 = pending.iter()
                            .filter(|(delivery_date, _)| delivery_date > date)
                            .map(|(_, qty)| qty)
                            .sum();

                        // Calculate realistic safety stock
                        let supplier_id = (product.product_id % 30) + 1;
                        let supplier = self.suppliers.iter().find(|s| s.supplier_id == supplier_id).unwrap();

                        let reorder_point = crate::inventory::calculate_reorder_point(
                            history,
                            supplier.lead_time_days as f64,
                            demand
                        );

                        // Safety stock is part of reorder point calculation
                        let avg_demand = if !history.is_empty() {
                            history.iter().sum::<u32>() as f64 / history.len() as f64
                        } else {
                            demand as f64
                        };
                        let safety_stock = reorder_point.saturating_sub((avg_demand * supplier.lead_time_days as f64) as u32);

                        // Calculate in-stock hours (0 if stockout)
                        let in_stock_hours = if *current_on_hand > 0 {
                            if store.store_type == "online" { 24.0 } else { 12.0 }
                        } else {
                            0.0
                        };

                        // SPARSE: Only write inventory records if there's inventory activity
                        if *current_on_hand > 0 || *current_on_order > 0 || in_transit > 0 {
                            writers.write_inventory(&InventoryDaily {
                            date: *date,
                            store_id: store.store_id,
                            sku: product.sku.clone(),
                            on_hand: *current_on_hand,
                            on_order: *current_on_order,
                            in_transit,
                            safety_stock,
                            last_scan_ts: NaiveDateTime::new(*date, chrono::NaiveTime::from_hms_opt(12, 0, 0).unwrap()),
                            system_on_hand: *current_on_hand,
                            available_to_promise: current_on_hand.saturating_sub(0), // Could reserve for online orders
                            open_hours: if store.store_type == "online" { 24 } else { 12 },
                            in_stock_hours,
                            dc_allocated_qty: 0,
                            quarantine_hold: 0,
                            })?;
                        }

                        // Returns are now generated separately from actual transaction line items
                        // This happens after all transactions are written, so we can pick from real line items

                        if matches!(product.category.as_str(), "dairy" | "produce" | "meat") && self.rng.gen::<f64>() < 0.02 {
                            let recorded_by = format!("emp_{}", self.rng.gen_range(100..999));

                            writers.write_waste(&WasteSpoilage {
                                waste_id,
                                date: *date,
                                store_id: store.store_id,
                                sku: product.sku.clone(),
                                quantity_wasted: self.rng.gen_range(1..5),
                                waste_reason: perishable_waste_reasons.choose(&mut self.rng).unwrap().clone(),
                                waste_value: Self::round_cost(product.cost),
                                recorded_by,
                            })?;
                            waste_id += 1;
                        }

                        // Generate various types of tickets (not just stockouts)
                        // Realistic ticket generation: ~0.5% probability per product per day
                        let ticket_prob = 0.005;

                        if self.rng.gen::<f64>() < ticket_prob {
                            let hour = self.rng.gen_range(8..18);
                            let minute = self.rng.gen_range(0..60);
                            let created_at = format!("{} {:02}:{:02}:00", date, hour, minute);

                            // 70% of tickets get resolved same day
                            let resolved_at = if self.rng.gen::<f64>() < 0.7 {
                                let resolve_hour = hour + self.rng.gen_range(1..4);
                                Some(format!("{} {:02}:{:02}:00", date, resolve_hour.min(20), self.rng.gen_range(0..60)))
                            } else {
                                None
                            };

                            // Different ticket types with realistic probabilities
                            let ticket_type_roll = self.rng.gen::<f64>();
                            let (issue_type, description, root_cause) = if on_hand == 0 && demand > 0 {
                                // Stockout (higher priority if actually out of stock)
                                ("stockout".to_string(),
                                 "Product out of stock".to_string(),
                                 Some("supplier_delay".to_string()))
                            } else if ticket_type_roll < 0.25 {
                                // Quality issues (25%)
                                ("quality_issue".to_string(),
                                 "Customer reported damaged/expired product".to_string(),
                                 Some("handling_damage".to_string()))
                            } else if ticket_type_roll < 0.45 {
                                // Pricing discrepancies (20%)
                                ("pricing_error".to_string(),
                                 "Price mismatch between shelf and register".to_string(),
                                 Some("label_not_updated".to_string()))
                            } else if ticket_type_roll < 0.60 {
                                // Inventory discrepancies (15%)
                                ("inventory_discrepancy".to_string(),
                                 "Physical count doesn't match system".to_string(),
                                 Some("shrinkage".to_string()))
                            } else if ticket_type_roll < 0.75 {
                                // Display/merchandising issues (15%)
                                ("display_issue".to_string(),
                                 "Product not on shelf despite inventory".to_string(),
                                 Some("backroom_overflow".to_string()))
                            } else if ticket_type_roll < 0.85 {
                                // Customer complaints (10%)
                                ("customer_complaint".to_string(),
                                 "Customer service issue reported".to_string(),
                                 Some("product_quality".to_string()))
                            } else {
                                // System/technical issues (15%)
                                ("system_issue".to_string(),
                                 "Barcode scan error or system glitch".to_string(),
                                 Some("technical_error".to_string()))
                            };

                            writers.write_ticket(&Ticket {
                                ticket_id,
                                created_at,
                                resolved_at: resolved_at.clone(),
                                store_id: store.store_id,
                                sku: product.sku.clone(),
                                issue_type,
                                description,
                                root_cause,
                                resolved: resolved_at.is_some(),
                            })?;
                            ticket_id += 1;
                        }

                        // Price changes tied to macroeconomic inflation
                        // Higher inflation years see more frequent price increases
                        let inflation_rate = self.get_inflation_rate_for_year(date.year());
                        // Base probability scales with inflation (0.001 at 2% -> 0.005 at 10%)
                        let price_change_prob = 0.0005 + (inflation_rate * 0.04);

                        if self.rng.gen::<f64>() < price_change_prob {
                            // Price increase magnitude tied to inflation
                            // Some items increase more than inflation, some less
                            let increase_multiplier = 1.0 + inflation_rate * self.rng.gen_range(0.5..1.5);
                            writers.write_price_change(&PriceChange {
                                change_id,
                                date: *date,
                                store_id: store.store_id,
                                sku: product.sku.clone(),
                                new_regular_price: Self::round_currency(regular_price * increase_multiplier),
                                reason: "cost_increase".to_string(),
                            })?;
                            change_id += 1;
                        }
                    }
                } // end if let Some(store_assortments)
                } // end for assort

                inventory_time += store_start.elapsed();
                let _txn_start = std::time::Instant::now();

                // NEW APPROACH: Generate transactions FIRST from available products
                // Track all line items to aggregate into sales_daily later
                let mut all_line_items_for_store_day: Vec<TransactionLineItem> = Vec::new();

                // ALWAYS generate transactions based on store type, even if inventory is low
                // Realistic transaction counts based on store type
                let (_avg_basket_size, base_txns_min, base_txns_max) = match store.store_type.as_str() {
                    "online" => (20, 950, 1050),        // Larger baskets
                    "big_box" => (15, 750, 850),        // Stock-up trips
                    "suburban" => (10, 475, 525),       // Weekly shopping
                    "urban" => (5, 380, 420),           // Quick trips
                    "convenience" => (3, 190, 210),     // Very small purchases
                    _ => (10, 475, 525),
                };

                // Generate target number of transactions regardless of inventory
                let num_transactions = self.rng.gen_range(base_txns_min..=base_txns_max);

                if !available_products.is_empty() {
                    // We have inventory - generate full transactions

                    // Pre-generate transaction data to avoid borrow conflicts
                    let mut transaction_data = Vec::new();
                    for _ in 0..num_transactions {
                        let hour = self.rng.gen_range(8..22);
                        let minute = self.rng.gen_range(0..60);
                        let rand_customer = self.rng.gen::<f64>();
                        let rand_fulfillment = self.rng.gen::<f64>();
                        let rand_delivery_fee = self.rng.gen_range(0.0..1.0);
                        let rand_tip = self.rng.gen::<f64>();
                        let rand_tip_amount = self.rng.gen_range(0.0..1.0);
                        let rand_status = self.rng.gen::<f64>();
                        let rand_time_offset1 = self.rng.gen_range(30..90);
                        let rand_time_offset2 = self.rng.gen_range(35..95);

                        transaction_data.push((
                            hour,
                            minute,
                            rand_customer,
                            rand_fulfillment,
                            rand_delivery_fee,
                            rand_tip,
                            rand_tip_amount,
                            rand_status,
                            rand_time_offset1,
                            rand_time_offset2,
                        ));
                    }

                    // Now generate transactions using pre-generated random values
                    for (hour, minute, _rand_customer, rand_fulfillment,
                         rand_delivery_fee, rand_tip, rand_tip_amount, rand_status, _time_off1, _time_off2) in transaction_data {
                        let timestamp = format!("{} {:02}:{:02}:00", date.format("%Y-%m-%d"), hour, minute);

                        // Just capture store_id - no need to clone entire Store struct
                        let store_id = store.store_id;
                        let store_type = &store.store_type;

                        // Determine customer linkage using indexed lookup
                        let (customer_id, is_loyalty_transaction, loyalty_points_earned, loyalty_points_redeemed) =
                            Self::maybe_link_customer_static(&mut self.rng, store, store_type, &store_to_customers, &city_to_customers, &self.customers);

                        // Determine fulfillment type using pre-generated random
                        let fulfillment_type = if store.store_type == "online" {
                            Some(if rand_fulfillment < 0.65 { "delivery".to_string() } else { "pickup".to_string() })
                        } else if customer_id.is_some() && rand_fulfillment < 0.15 {
                            Some(if rand_fulfillment < 0.105 { "in_store".to_string() }
                                 else if rand_fulfillment < 0.135 { "pickup".to_string() }
                                 else { "delivery".to_string() })
                        } else {
                            Some("in_store".to_string())
                        };

                        // Generate transaction line items from available products
                        let (actual_total_amount, actual_total_items, line_items_buffer) = if !available_products.is_empty() {
                            let mut line_items_buffer: Vec<TransactionLineItem> = Vec::new();

                            // Weighted basket size distribution - heavily favor small purchases
                            // Real retail: 60% are 1-3 items, 30% are 4-10 items, 10% are 11+ items
                            let basket_category: f64 = self.rng.gen();
                            let num_items = if basket_category < 0.60 {
                                // 60%: Quick purchases (1-3 items) - convenience, urban quick trips
                                self.rng.gen_range(1..=3)
                            } else if basket_category < 0.90 {
                                // 30%: Medium trips (4-10 items) - suburban, urban weekly
                                match store.store_type.as_str() {
                                    "convenience" => self.rng.gen_range(1..=4),
                                    "urban" => self.rng.gen_range(3..=8),
                                    _ => self.rng.gen_range(4..=10),
                                }
                            } else {
                                // 10%: Large trips (11-25 items) - big box, online, suburban stock-up
                                match store.store_type.as_str() {
                                    "online" => self.rng.gen_range(15..=25),
                                    "big_box" => self.rng.gen_range(12..=25),
                                    "suburban" => self.rng.gen_range(11..=18),
                                    "urban" => self.rng.gen_range(8..=15),
                                    "convenience" => self.rng.gen_range(4..=8),
                                    _ => self.rng.gen_range(11..=20),
                                }
                            };
                            let num_items = num_items.min(available_products.len() as u32);
                            let selected_products: Vec<_> = available_products
                                .choose_multiple(&mut self.rng, num_items as usize)
                                .collect();

                            // Generate line items with random quantities
                            for (line_number, (sku, units_available, _regular_price, unit_price, promo_id, discount_per_unit, _cost)) in selected_products.iter().enumerate() {
                                // Random quantity between 1-3, constrained by availability
                                let quantity = self.rng.gen_range(1..=3).min(*units_available);

                                // Calculate line total
                                let line_total = Self::round_currency(*unit_price * quantity as f64);
                                let rounded_discount = Self::round_currency(discount_per_unit * quantity as f64);

                                line_items_buffer.push(TransactionLineItem {
                                    transaction_id: global_txn_id,
                                    line_number: (line_number + 1) as u32,
                                    sku: sku.clone(),
                                    quantity,
                                    unit_price: *unit_price,
                                    line_total,
                                    promo_id: *promo_id,
                                    discount_amount: rounded_discount,
                                });
                            }

                            // Calculate actual transaction total from line items
                            let actual_total: f64 = line_items_buffer.iter()
                                .map(|item| item.line_total)
                                .sum();
                            let rounded_total = Self::round_currency(actual_total);
                            let actual_items = line_items_buffer.len() as u32;

                            (rounded_total, actual_items, line_items_buffer)
                        } else {
                            (0.0, 0, Vec::new())
                        };

                        // Delivery/pickup fields using pre-generated randoms and actual transaction total
                        let (delivery_fee, tip_amount, order_status, delivery_address_id, requested_time, actual_time) =
                            if fulfillment_type.as_ref().is_some_and(|f| f == "delivery" || f == "pickup") {
                                let fee = Self::round_currency(if fulfillment_type.as_ref().unwrap() == "pickup" { 0.0 } else {
                                    match store.store_type.as_str() {
                                        "online" => 4.99 + rand_delivery_fee * 5.0,
                                        _ => 2.99 + rand_delivery_fee * 5.0,
                                    }
                                });

                                let tip = Self::round_currency(if rand_tip < 0.7 {
                                    actual_total_amount * (0.10 + rand_tip_amount * 0.10)
                                } else {
                                    actual_total_amount * (rand_tip_amount * 0.10)
                                });

                                let status = Some(if rand_status < 0.92 { "delivered".to_string() }
                                                 else if rand_status < 0.97 { "pending".to_string() }
                                                 else { "cancelled".to_string() });

                                let order_time = NaiveDateTime::parse_from_str(&timestamp, "%Y-%m-%d %H:%M:%S")
                                    .unwrap_or_else(|_| date.and_hms_opt(12, 0, 0).unwrap());

                                let req_time = Some(order_time + Duration::minutes(self.rng.gen_range(30..90) as i64));
                                let act_time = Some(order_time + Duration::minutes(self.rng.gen_range(35..95) as i64));

                                (fee, tip, status, customer_id, req_time, act_time)
                            } else {
                                (0.0, 0.0, None, None, None, None)
                            };

                        // Now create transaction with ACTUAL total from line items
                        let transaction = Transaction {
                            transaction_id: global_txn_id,
                            date: *date,
                            store_id: store.store_id,
                            timestamp: timestamp.clone(),
                            total_items: actual_total_items,
                            payment_method: payment_methods.choose(&mut self.rng).unwrap().clone(),
                            customer_type: "regular".to_string(),
                            total_amount: actual_total_amount,
                            customer_id,
                            is_loyalty_transaction,
                            loyalty_points_earned,
                            loyalty_points_redeemed,
                            fulfillment_type,
                            order_status,
                            fulfillment_store_id: Some(store.store_id),
                            delivery_address_id,
                            delivery_fee,
                            tip_amount,
                            delivery_instructions: None,
                            requested_delivery_time: requested_time,
                            actual_delivery_time: actual_time,
                        };

                        writers.write_transaction(&transaction)?;

                        // Write line items and collect for aggregation
                        for item in &line_items_buffer {
                            writers.write_transaction_line_item(item)?;
                            all_line_items_for_store_day.push(item.clone());
                        }

                        // Generate returns for TODAY from historical purchases (1-30 days ago)
                        // This ensures nightly runs always have some returns data
                        // Realistic return rate: ~1-2% of transactions, weighted by recency
                        let return_probability_base = 0.015; // 1.5% base return rate

                        for days_ago in 1..=30 {
                            let purchase_date = *date - chrono::Duration::days(days_ago);

                            // Only generate returns for purchases within our date range
                            if purchase_date < *self.dates.first().unwrap() {
                                continue;
                            }

                            // Return probability decreases with age (most returns happen 3-7 days after purchase)
                            let recency_weight = if days_ago <= 3 {
                                0.3 // 30% of returns happen in first 3 days
                            } else if days_ago <= 7 {
                                0.4 // 40% of returns happen days 4-7
                            } else if days_ago <= 14 {
                                0.2 // 20% of returns happen days 8-14
                            } else {
                                0.1 // 10% of returns happen days 15-30
                            };

                            let adjusted_return_prob = return_probability_base * recency_weight / 30.0;

                            // Generate returns for a sample of line items from that day
                            if self.rng.gen::<f64>() < adjusted_return_prob {
                                // Simulate a return from a historical transaction
                                // Use current transaction's line items as a template
                                for item in &line_items_buffer {
                                    if self.rng.gen::<f64>() < 0.05 { // 5% of items from selected transactions get returned
                                        // Return partial or full quantity
                                        let return_qty = if item.quantity > 1 && self.rng.gen::<f64>() < 0.3 {
                                            self.rng.gen_range(1..item.quantity) // Partial return
                                        } else {
                                            item.quantity // Full return
                                        };

                                        let refund_value = Self::round_currency(return_qty as f64 * item.unit_price);
                                        let reason = return_reasons.choose(&mut self.rng).unwrap().clone();

                                        // Create a virtual transaction ID from the past
                                        let virtual_txn_id = global_txn_id.saturating_sub((days_ago * 100) as u64);

                                        writers.write_return(&ReturnDaily {
                                            date: *date, // Return happens TODAY
                                            store_id,
                                            sku: item.sku.clone(),
                                            units_returned: return_qty,
                                            reason_code: reason,
                                            refund_value,
                                            transaction_id: virtual_txn_id,
                                            line_number: item.line_number,
                                        })?;
                                    }
                                }
                            }
                        }

                        // Create delivery assignment if needed (now works because demand_calc is dropped)
                        if transaction.fulfillment_type.as_ref().is_some_and(|f| f == "delivery" || f == "pickup") &&
                           transaction.order_status.as_ref().is_some_and(|s| s == "delivered") {
                            let fulfillment_str = transaction.fulfillment_type.as_ref().unwrap().clone();
                            Self::create_delivery_assignment_static(
                                &mut self.rng,
                                &mut writers,
                                global_txn_id,
                                store_id,
                                &fulfillment_str,
                                date,
                                &timestamp,
                                45,
                                actual_total_amount,
                                &self.delivery_drivers,
                                &self.stores,
                            )?;
                        }

                        global_txn_id += 1;
                    }

                    // AGGREGATE TRANSACTIONS TO SALES_DAILY
                    // Group line items by SKU and aggregate
                    let mut sku_aggregates: HashMap<String, (u32, f64, Option<u32>, f64, f64)> = HashMap::new();
                    // (units_sold, revenue, promo_id, regular_price, net_price)

                    for line_item in &all_line_items_for_store_day {
                        let entry = sku_aggregates.entry(line_item.sku.clone()).or_insert((0, 0.0, line_item.promo_id, 0.0, 0.0));
                        entry.0 += line_item.quantity;
                        entry.1 += line_item.line_total;
                        // Keep first promo_id encountered
                        if entry.2.is_none() {
                            entry.2 = line_item.promo_id;
                        }
                        // Track prices (will use for calculating discount_pct)
                        if entry.3 == 0.0 {
                            entry.3 = line_item.unit_price + line_item.discount_amount / line_item.quantity as f64;
                            entry.4 = line_item.unit_price;
                        }
                    }

                    // Write sales_daily records from aggregated transactions
                    for (sku, (units_sold, revenue, promo_id, _regular_price, _net_price)) in sku_aggregates {
                        // Find product info from available_products
                        if let Some((_, _, reg_price, net_pr, promo, _, cost)) = available_products.iter()
                            .find(|(s, _, _, _, _, _, _)| s == &sku) {

                            let discount_pct = if promo.is_some() {
                                (((reg_price - net_pr) / reg_price) * 100.0).round() as u32
                            } else {
                                0
                            };

                            let cogs_c = Self::round_currency(units_sold as f64 * cost);
                            let shrinkage_cost = cogs_c * store_econ.shrinkage_rate;
                            let cogs_s = cogs_c * (1.0 + store_econ.shrinkage_rate);

                            // Get product for category check
                            let product = sku_to_product.get(sku.as_str());
                            let is_perishable = product.is_some_and(|p| matches!(p.category.as_str(), "dairy" | "produce" | "meat"));

                            writers.write_sales(&SalesDaily {
                                date: *date,
                                store_id: store.store_id,
                                sku: sku.clone(),
                                units_sold,
                                gross_revenue: Self::round_currency(revenue),
                                promo_id,
                                regular_price: Self::round_currency(*reg_price),
                                net_price: Self::round_currency(*net_pr),
                                revenue: Self::round_currency(revenue),
                                supplier_rebate_amt: Self::round_currency(if self.rng.gen::<f64>() < 0.3 { revenue * 0.02 } else { 0.0 }),
                                spoilage_cost: Self::round_currency(if is_perishable {
                                    cogs_c * self.rng.gen_range(0.005..0.015)
                                } else {
                                    shrinkage_cost
                                }),
                                promo_funding_received: Self::round_currency(if promo.is_some() {
                                    // Estimate promo funding based on discount
                                    revenue * 0.05
                                } else {
                                    0.0
                                }),
                                gross_margin_pct: Self::round_currency(if revenue > 0.0 {
                                    ((revenue - cogs_c) / revenue) * 100.0
                                } else {
                                    0.0
                                }),
                                discount_pct,
                                cogs_c: Self::round_currency(cogs_c),
                                cogs_s: Self::round_currency(cogs_s),
                                sales_date: *date,
                                posting_date: *date + Duration::days(7),
                            })?;

                            // NOW update inventory based on actual sales from transactions
                            // Need to find the inventory entry - iterate to find matching SKU
                            let mut inv_entries_to_update = Vec::new();
                            for (key, value) in inventory.iter() {
                                if key.0 == store.store_id && key.1 == sku.as_str() {
                                    inv_entries_to_update.push((*key, value.clone()));
                                }
                            }
                            for (key, (mut on_hand, on_order, pending)) in inv_entries_to_update {
                                on_hand = on_hand.saturating_sub(units_sold);
                                inventory.insert(key, (on_hand, on_order, pending));
                            }
                        }
                    }
                }
            }

            // Flush every N days instead of every day for better performance
            if should_flush {
                writers.flush_all()?;
            }

            // Print timing for first few days to diagnose slowness
            if idx < 5 {
                let day_elapsed = day_start.elapsed();
                pb.println(format!("    Day {} completed in {:.2}s", idx + 1, day_elapsed.as_secs_f64()));
            }
        }

        // Finish progress bar
        pb.finish_with_message("Complete!");

        // Final flush to ensure all data is written
        writers.flush_all()?;

        // Write ALL customers and drivers to CSV (including future ones)
        // This allows nightly imports to extract new customers/drivers by ID
        println!("\nWriting complete customer and driver datasets for nightly extraction...");

        if !self.customers.is_empty() {
            let mut wtr = csv::Writer::from_path(Path::new(output_dir).join("customers.csv"))?;
            for c in &self.customers { wtr.serialize(c)?; }
            wtr.flush()?;
            println!("  Wrote {} total customers", self.customers.len());
        }

        if !self.customer_addresses.is_empty() {
            let mut wtr = csv::Writer::from_path(Path::new(output_dir).join("customer_addresses.csv"))?;
            for a in &self.customer_addresses { wtr.serialize(a)?; }
            wtr.flush()?;
            println!("  Wrote {} total customer addresses", self.customer_addresses.len());
        }

        if !self.delivery_drivers.is_empty() {
            let mut wtr = csv::Writer::from_path(Path::new(output_dir).join("delivery_drivers.csv"))?;
            for d in &self.delivery_drivers { wtr.serialize(d)?; }
            wtr.flush()?;
            println!("  Wrote {} total delivery drivers", self.delivery_drivers.len());
        }

        Ok(())
    }
}
