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

// Loyalty tier distribution
const LOYALTY_TIER_BRONZE: f64 = 0.50;
const LOYALTY_TIER_SILVER: f64 = 0.30;
const LOYALTY_TIER_GOLD: f64 = 0.15;
const LOYALTY_TIER_PLATINUM: f64 = 0.05;

// Transaction tracking rates by store type
// Loyalty program penetration over time
const LOYALTY_PENETRATION_2019: f64 = 0.10;
const LOYALTY_PENETRATION_2020: f64 = 0.20;
const LOYALTY_PENETRATION_2021: f64 = 0.28;
const LOYALTY_PENETRATION_2022: f64 = 0.33;
const LOYALTY_PENETRATION_2023: f64 = 0.36;
const LOYALTY_PENETRATION_2024: f64 = 0.38;
const LOYALTY_PENETRATION_2025: f64 = 0.38;

// Customer behavior parameters (shopping frequency in days)
const FREQ_FREQUENT_SHOPPER: u32 = 3;
const FREQ_WEEKLY_SHOPPER: u32 = 7;
const FREQ_BULK_BUYER: u32 = 21;
const FREQ_OCCASIONAL: u32 = 30;

// Average basket sizes by segment
const BASKET_FREQUENT_SHOPPER: u32 = 12;
const BASKET_WEEKLY_SHOPPER: u32 = 25;
const BASKET_BULK_BUYER: u32 = 45;
const BASKET_OCCASIONAL: u32 = 18;

// Brand loyalty scores by income
const BRAND_LOYALTY_PREMIUM: f64 = 0.75;
const BRAND_LOYALTY_MID: f64 = 0.65;
const BRAND_LOYALTY_VALUE: f64 = 0.50;

// Delivery configuration
const DRIVERS_PER_STORE_URBAN: usize = 6;
const DRIVERS_PER_STORE_SUBURBAN: usize = 5;
const DRIVERS_PER_STORE_BIG_BOX: usize = 8;
const DRIVERS_PER_STORE_CONVENIENCE: usize = 2;
const DRIVERS_FULFILLMENT_CENTER: usize = 50;

const EMPLOYEE_DRIVER_PCT: f64 = 0.30;
const CONTRACTOR_DRIVER_PCT: f64 = 0.60;
const THIRD_PARTY_DRIVER_PCT: f64 = 0.10;

pub struct ShelfWiseDataGenerator {
    rng: StdRng,
    config: Config,
    start_date: NaiveDate,
    #[allow(dead_code)]
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

    // Customer data
    customers: Vec<Customer>,
    customer_addresses: Vec<CustomerAddress>,
    customer_behaviors: HashMap<u64, CustomerBehavior>,

    // Delivery data
    delivery_drivers: Vec<DeliveryDriver>,
    delivery_zones: Vec<DeliveryZone>,
}

impl ShelfWiseDataGenerator {
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
        let end_date = NaiveDate::parse_from_str(&config.date_range.end_date, "%Y-%m-%d")
            .expect("Invalid end_date format in config.toml");

        let mut dates = Vec::new();
        let mut current = start_date;
        while current <= end_date {
            dates.push(current);
            current += Duration::days(1);
        }

        let holidays = generate_all_holidays();
        let categories = Self::init_categories();
        let brands = Self::init_brands();

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
            customers: Vec::new(),
            customer_addresses: Vec::new(),
            customer_behaviors: HashMap::new(),
            delivery_drivers: Vec::new(),
            delivery_zones: Vec::new(),
        }
    }

    fn init_categories() -> HashMap<String, CategoryConfig> {
        let mut categories = HashMap::new();

        // Load from reference data and add generation-specific parameters
        for cat in crate::reference_data::init_categories() {
            let seasonality = match cat.category_name.as_str() {
                "snacks" | "meat" | "candy" => "event_driven",
                "beverages" => "summer",
                "frozen" | "canned" => "winter",
                _ => "steady",
            };

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
                    seasonality: seasonality.to_string(),
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
                let log_normal = LogNormal::new(1.8, 0.8).unwrap();
                let base_price = (log_normal.sample(&mut self.rng) as f64).clamp(1.5, 50.0);

                let list_price = match brand.tier.as_str() {
                    "premium" => base_price * 1.5,
                    "value" => base_price * 0.8,
                    _ => base_price,
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

                    let cost = list_price * category_cost_ratio * tier_adjustment;
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
            product.pareto_weight = weights[i];
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
        let international_stores = vec![
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

    pub fn generate_customers(&mut self) {
        let num_customers = self.config.customers.num_customers;
        println!("Generating {} customers...", num_customers);

        let mut customers = Vec::new();
        let mut customer_behaviors = HashMap::new();

        // Simple name lists for generation
        let first_names = vec!["James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda",
            "William", "Barbara", "David", "Elizabeth", "Richard", "Susan", "Joseph", "Jessica", "Thomas", "Sarah",
            "Charles", "Karen", "Christopher", "Nancy", "Daniel", "Lisa", "Matthew", "Betty", "Anthony", "Margaret"];
        let last_names = vec!["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
            "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor",
            "Moore", "Jackson", "Martin", "Lee", "Thompson", "White", "Harris", "Sanchez", "Clark", "Lewis"];

        for customer_id in 1..=num_customers as u64 {
            // Pick demographics using weighted distribution
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

            // Pick customer segment
            let segment = self.pick_weighted(&[
                ("frequent_shopper", SEGMENT_FREQUENT_SHOPPER),
                ("weekly_shopper", SEGMENT_WEEKLY_SHOPPER),
                ("bulk_buyer", SEGMENT_BULK_BUYER),
                ("occasional", SEGMENT_OCCASIONAL),
            ]);

            // Assign to primary store (only physical stores, not online/fulfillment center)
            let physical_stores: Vec<Store> = self.stores.iter()
                .filter(|s| s.store_type != "online")
                .cloned()
                .collect();
            let primary_store = physical_stores.choose(&mut self.rng).unwrap().clone();

            // Determine loyalty membership
            let year = self.start_date.year();
            let loyalty_penetration = match year {
                2019 => LOYALTY_PENETRATION_2019,
                2020 => LOYALTY_PENETRATION_2020,
                2021 => LOYALTY_PENETRATION_2021,
                2022 => LOYALTY_PENETRATION_2022,
                2023 => LOYALTY_PENETRATION_2023,
                2024 => LOYALTY_PENETRATION_2024,
                _ => LOYALTY_PENETRATION_2025,
            };

            let is_loyalty_member = self.rng.gen::<f64>() < loyalty_penetration;

            let loyalty_tier = if is_loyalty_member {
                Some(self.pick_weighted(&[
                    ("bronze", LOYALTY_TIER_BRONZE),
                    ("silver", LOYALTY_TIER_SILVER),
                    ("gold", LOYALTY_TIER_GOLD),
                    ("platinum", LOYALTY_TIER_PLATINUM),
                ]))
            } else {
                None
            };

            // Generate realistic contact info
            let first_name = first_names.choose(&mut self.rng).unwrap().to_string();
            let last_name = last_names.choose(&mut self.rng).unwrap().to_string();

            // Realistic email domains
            let email_domains = vec!["gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "icloud.com", "aol.com"];
            let domain = email_domains.choose(&mut self.rng).unwrap();

            // Ensure unique email by using customer_id
            // Format: firstname.lastname.ID@domain or firstname.lastname@domain (for low IDs)
            let email = if customer_id <= 100 {
                // First 100 customers get clean emails (no numbers)
                format!("{}.{}@{}",
                    first_name.to_lowercase(),
                    last_name.to_lowercase(),
                    domain)
            } else {
                // Rest get customer_id appended to ensure uniqueness
                format!("{}.{}.{}@{}",
                    first_name.to_lowercase(),
                    last_name.to_lowercase(),
                    customer_id,
                    domain)
            };

            // Realistic US phone numbers (not 555)
            let area_codes = vec![415, 510, 650, 408, 925, 707, 209, 559, 916, 530]; // CA area codes
            let area_code = area_codes.choose(&mut self.rng).unwrap();
            let phone = format!("{}-{:03}-{:04}",
                area_code,
                self.rng.gen_range(200..999),
                self.rng.gen_range(1000..9999));

            // Set location near primary store (within 5-15 miles)
            let distance_miles = self.rng.gen_range(1.0..15.0);
            let angle = self.rng.gen_range(0.0..std::f64::consts::TAU);
            let lat_offset = (distance_miles / 69.0) * angle.cos();
            let lon_offset = (distance_miles / 54.6) * angle.sin();

            // Determine shopping preferences
            let preferred_shopping_time = self.pick_weighted(&[
                ("morning", 0.25),
                ("afternoon", 0.30),
                ("evening", 0.35),
                ("weekend", 0.10),
            ]);

            let avg_basket_size = match segment.as_str() {
                "frequent_shopper" => BASKET_FREQUENT_SHOPPER as f64,
                "weekly_shopper" => BASKET_WEEKLY_SHOPPER as f64,
                "bulk_buyer" => BASKET_BULK_BUYER as f64,
                "occasional" => BASKET_OCCASIONAL as f64,
                _ => 20.0,
            };

            let price_sensitivity = match income_bracket.as_str() {
                "low" => "high",
                "medium" => "medium",
                "high" | "very_high" => "low",
                _ => "medium",
            };

            let customer = Customer {
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
                loyalty_tier,
                loyalty_join_date: if is_loyalty_member {
                    Some(self.start_date + Duration::days(self.rng.gen_range(0..365)))
                } else {
                    None
                },
                loyalty_points: 0,
                preferred_shopping_time,
                avg_basket_size,
                price_sensitivity: price_sensitivity.to_string(),
                customer_segment: segment.clone(),
                created_date: self.start_date - Duration::days(self.rng.gen_range(0..730)),
                last_purchase_date: None,
                total_lifetime_value: 0.0,
                total_visits: 0,
                has_online_account: self.rng.gen::<f64>() < 0.4,
                prefers_online: self.rng.gen::<f64>() < 0.15,
            };

            // Create behavior profile
            let shopping_frequency_days = match segment.as_str() {
                "frequent_shopper" => FREQ_FREQUENT_SHOPPER,
                "weekly_shopper" => FREQ_WEEKLY_SHOPPER,
                "bulk_buyer" => FREQ_BULK_BUYER,
                "occasional" => FREQ_OCCASIONAL,
                _ => 7,
            };

            let brand_loyalty_score = match income_bracket.as_str() {
                "low" | "medium" => BRAND_LOYALTY_VALUE,
                "high" => BRAND_LOYALTY_MID,
                "very_high" => BRAND_LOYALTY_PREMIUM,
                _ => 0.65,
            };

            // Pick 2-4 preferred categories
            let all_categories = vec!["cereal", "dairy", "snacks", "beverages", "produce",
                "household", "frozen", "bakery", "meat", "canned", "personal_care", "candy"];
            let num_preferred = self.rng.gen_range(2..=4);
            let preferred_categories: Vec<String> = all_categories
                .choose_multiple(&mut self.rng, num_preferred)
                .map(|s| s.to_string())
                .collect();

            // Pick 3-6 preferred brands
            let num_preferred_brands = self.rng.gen_range(3..=6);
            let preferred_brands: Vec<String> = self.brands
                .choose_multiple(&mut self.rng, num_preferred_brands)
                .map(|b| b.name.clone())
                .collect();

            let behavior = CustomerBehavior {
                customer_id,
                segment: segment.clone(),
                shopping_frequency_days,
                avg_basket_size: avg_basket_size as u32,
                brand_loyalty_score,
                price_sensitivity: if price_sensitivity == "high" { 0.8 } else if price_sensitivity == "low" { 0.3 } else { 0.5 },
                preferred_categories,
                preferred_brands,
                last_visit_date: None,
            };

            customers.push(customer);
            customer_behaviors.insert(customer_id, behavior);
        }

        self.customers = customers;
        self.customer_behaviors = customer_behaviors;

        println!("  Generated {} customers", self.customers.len());

        // Generate customer addresses (1-2 per customer)
        self.generate_customer_addresses();
    }

    pub fn generate_customer_addresses(&mut self) {
        if self.customers.is_empty() {
            println!("  Skipping customer address generation (no customers)");
            return;
        }

        println!("Generating customer addresses...");

        let mut addresses = Vec::new();
        let mut address_id = 1u64;

        let street_names = vec!["Main St", "Oak Ave", "Maple Dr", "Pine Rd", "Cedar Ln", "Elm St",
            "Washington Blvd", "Park Ave", "Broadway", "Market St", "1st St", "2nd Ave"];
        let apartment_types = vec!["Apt", "Unit", "Suite", "#"];

        let customers_clone = self.customers.clone();
        for customer in &customers_clone {
            // Each customer gets 1-2 addresses (70% have 1, 30% have 2)
            let num_addresses = if self.rng.gen::<f64>() < 0.70 { 1 } else { 2 };

            for addr_num in 0..num_addresses {
                let address_type = if addr_num == 0 { "home" } else { "work" };
                let is_default = addr_num == 0;

                // Generate address near customer's home location
                let distance = self.rng.gen_range(0.0..2.0); // Within 2 miles
                let angle = self.rng.gen_range(0.0..std::f64::consts::TAU);
                let latitude = customer.home_latitude + (distance / 69.0) * angle.cos();
                let longitude = customer.home_longitude + (distance / 54.6) * angle.sin();

                // Generate street address
                let street_num = self.rng.gen_range(100..9999);
                let street_name = street_names.choose(&mut self.rng).unwrap();
                let street_address = format!("{} {}", street_num, street_name);

                // 40% have apartment/unit numbers
                let apartment_unit = if self.rng.gen::<f64>() < 0.40 {
                    let apt_type = apartment_types.choose(&mut self.rng).unwrap();
                    let apt_num = self.rng.gen_range(1..500);
                    Some(format!("{} {}", apt_type, apt_num))
                } else {
                    None
                };

                // Zip code based on city (simplified)
                let zip_code = format!("{:05}", self.rng.gen_range(10000..99999));

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

                let created_at = customer.created_date.and_hms_opt(12, 0, 0).unwrap();

                let address = CustomerAddress {
                    address_id,
                    customer_id: customer.customer_id,
                    address_type: address_type.to_string(),
                    is_default,
                    street_address,
                    apartment_unit,
                    city: customer.primary_city.clone(),
                    state: "CA".to_string(), // Simplified - could map cities to states
                    zip_code,
                    latitude,
                    longitude,
                    delivery_instructions,
                    has_doorman,
                    requires_signature,
                    created_at,
                    last_used_at: None,
                    delivery_count: 0,
                };

                addresses.push(address);
                address_id += 1;
            }
        }

        self.customer_addresses = addresses;
        println!("  Generated {} customer addresses", self.customer_addresses.len());
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
            // Regional labor cost index
            let labor_cost_index = if store.city.contains("San Francisco") || store.city.contains("San Jose") ||
                                      store.city.contains("Oakland") || store.city.contains("Palo Alto") ||
                                      store.city.contains("Mountain View") || store.city.contains("Berkeley") {
                self.rng.gen_range(1.30..1.40)  // Bay Area highest
            } else if store.city.contains("New York") || store.city.contains("Boston") {
                self.rng.gen_range(1.25..1.35)  // NYC/Boston
            } else if store.city.contains("Seattle") || store.city.contains("Portland") {
                self.rng.gen_range(1.15..1.25)  // Pacific NW
            } else if store.city.contains("Los Angeles") || store.city.contains("San Diego") {
                self.rng.gen_range(1.10..1.20)  // Southern CA
            } else if store.city.contains("London") {
                self.rng.gen_range(1.20..1.30)  // UK
            } else if store.city.contains("Toronto") || store.city.contains("Vancouver") {
                self.rng.gen_range(1.05..1.15)  // Canada
            } else if store.city.contains("Denver") || store.city.contains("Phoenix") || store.city.contains("Las Vegas") {
                self.rng.gen_range(1.00..1.10)  // Southwest
            } else if store.city.contains("Chicago") {
                self.rng.gen_range(1.10..1.20)  // Chicago
            } else {
                self.rng.gen_range(0.90..1.05)  // Other/lower cost areas
            };

            // Rent cost index by store type and location
            let base_rent_multiplier = match store.store_type.as_str() {
                "urban" => 1.30,
                "suburban" => 1.00,
                "convenience" => 1.10,
                "big_box" => 0.85,
                "online" => 0.70,
                _ => 1.00,
            };

            let location_rent_multiplier = if store.city.contains("San Francisco") || store.city.contains("New York") {
                1.15
            } else if store.city.contains("Los Angeles") || store.city.contains("Seattle") || store.city.contains("Boston") {
                1.10
            } else if store.city.contains("London") {
                1.12
            } else {
                1.00
            };

            let rent_cost_index = base_rent_multiplier * location_rent_multiplier * self.rng.gen_range(0.95..1.05);

            // Utility cost index (climate-based)
            let utility_cost_index = match store.climate_zone.as_str() {
                "hot" => self.rng.gen_range(1.10..1.20),      // High AC costs
                "cold" => self.rng.gen_range(1.05..1.15),     // High heating costs
                "temperate" => self.rng.gen_range(0.90..1.00), // Moderate
                "controlled" => self.rng.gen_range(1.15..1.25), // Fulfillment center (24/7 climate control)
                _ => 1.00,
            };

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

            // Labor efficiency
            let labor_efficiency = if years_open < 0.0 {
                self.rng.gen_range(0.90..0.95)  // New stores less efficient
            } else if years_open > 5.0 {
                self.rng.gen_range(1.05..1.10)  // Mature stores more efficient
            } else {
                self.rng.gen_range(0.98..1.02)  // Average
            };

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

            // Market share estimate
            let market_share_estimate = match store_performance_tier.as_str() {
                "high" => self.rng.gen_range(0.18..0.25),
                "medium" => self.rng.gen_range(0.10..0.18),
                "low" => self.rng.gen_range(0.05..0.10),
                _ => 0.12,
            };

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
                labor_cost_index,
                rent_cost_index,
                utility_cost_index,
                maturity_factor,
                shrinkage_rate,
                labor_efficiency,
                competitive_intensity,
                price_premium_index,
                volume_discount_tier,
                store_performance_tier,
                market_share_estimate,
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
        // Calculate total drivers needed based on store count
        let num_drivers = self.stores.iter()
            .map(|s| match s.store_type.as_str() {
                "urban" => DRIVERS_PER_STORE_URBAN,
                "suburban" => DRIVERS_PER_STORE_SUBURBAN,
                "big_box" => DRIVERS_PER_STORE_BIG_BOX,
                "convenience" => DRIVERS_PER_STORE_CONVENIENCE,
                "online" => DRIVERS_FULFILLMENT_CENTER,
                _ => 2,
            })
            .sum::<usize>();

        println!("Generating {} delivery drivers...", num_drivers);

        let mut drivers = Vec::new();

        let first_names = vec!["Alex", "Jordan", "Taylor", "Morgan", "Casey", "Riley", "Avery", "Quinn",
            "Skylar", "Dakota", "Reese", "Peyton", "Cameron", "Sage", "River", "Phoenix"];
        let last_names = vec!["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
            "Martinez", "Lopez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson"];

        for driver_id in 1..=num_drivers as u64 {
            // Assign driver type based on config percentages
            let driver_type = self.pick_weighted(&[
                ("employee", EMPLOYEE_DRIVER_PCT),
                ("contractor", CONTRACTOR_DRIVER_PCT),
                ("third_party", THIRD_PARTY_DRIVER_PCT),
            ]);

            // Assign to a random physical store as home base
            let home_store = self.stores.iter()
                .filter(|s| s.store_type != "online")
                .choose(&mut self.rng)
                .unwrap()
                .clone();

            // Generate driver details
            let first_name = first_names.choose(&mut self.rng).unwrap().to_string();
            let last_name = last_names.choose(&mut self.rng).unwrap().to_string();

            // Realistic US phone numbers (not 555)
            let area_codes = vec![415, 510, 650, 408, 925, 707, 209, 559, 916, 530]; // CA area codes
            let area_code = area_codes.choose(&mut self.rng).unwrap();
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

            // Hire date within last 1-3 years
            let hire_date = self.start_date - Duration::days(self.rng.gen_range(30..1095));

            // Employment status
            let employment_status = if driver_type == "employee" {
                "full_time"
            } else if driver_type == "contractor" {
                "part_time"
            } else {
                "gig"
            };

            // Service area
            let service_radius_miles = match driver_type.as_str() {
                "employee" => self.rng.gen_range(15.0..25.0),
                "contractor" => self.rng.gen_range(10.0..20.0),
                _ => self.rng.gen_range(5.0..15.0),
            };

            // Drivers can serve their home city plus nearby cities within their service radius
            let mut service_cities_list = vec![home_store.city.clone()];

            // Add nearby cities based on service radius
            for other_store in &self.stores {
                if other_store.store_id != home_store.store_id {
                    // Calculate approximate distance (simplified lat/lon distance)
                    let lat_diff = (home_store.latitude - other_store.latitude).abs();
                    let lon_diff = (home_store.longitude - other_store.longitude).abs();
                    let approx_distance = ((lat_diff * 69.0).powi(2) + (lon_diff * 54.6).powi(2)).sqrt();

                    if approx_distance <= service_radius_miles && !service_cities_list.contains(&other_store.city) {
                        service_cities_list.push(other_store.city.clone());
                    }
                }
            }

            let service_cities = service_cities_list.join(",");

            // Performance metrics - use realistic distributions
            let is_available = self.rng.gen::<f64>() < 0.75;

            // Total deliveries follows power law - few stars, many average
            let delivery_log_normal = LogNormal::new(5.0, 1.2).unwrap();
            let total_deliveries = if is_available {
                (delivery_log_normal.sample(&mut self.rng) as f64).round() as u32
            } else {
                ((delivery_log_normal.sample(&mut self.rng) as f64) * 0.1).round() as u32
            }.clamp(10, 5000);

            // Rating uses Beta distribution - heavily skewed toward high ratings
            // Beta(8, 2) gives mean ~0.8, heavily weighted toward 1.0
            let rating_beta = Beta::new(8.0, 2.0).unwrap();
            let avg_rating = ((rating_beta.sample(&mut self.rng) as f64) * 1.0 + 4.0).clamp(3.5, 5.0);

            // On-time delivery also uses Beta - most drivers are good
            let ontime_beta = Beta::new(9.0, 2.0).unwrap();
            let on_time_delivery_pct = ((ontime_beta.sample(&mut self.rng) as f64) * 0.25 + 0.75).clamp(0.70, 0.99);

            // Acceptance rate - Beta distribution
            let accept_beta = Beta::new(8.0, 2.0).unwrap();
            let acceptance_rate = ((accept_beta.sample(&mut self.rng) as f64) * 0.30 + 0.70).clamp(0.65, 0.99);

            // Cancellation rate - Beta with reverse skew (most have low cancellation)
            let cancel_beta = Beta::new(2.0, 8.0).unwrap();
            let cancellation_rate = ((cancel_beta.sample(&mut self.rng) as f64) * 0.15).clamp(0.01, 0.15);

            // Current location (near home store)
            let angle = self.rng.gen_range(0.0..std::f64::consts::TAU);
            let distance = self.rng.gen_range(0.0..5.0);
            let current_latitude = home_store.latitude + (distance / 69.0) * angle.cos();
            let current_longitude = home_store.longitude + (distance / 54.6) * angle.sin();
            let last_location_update = self.start_date.and_hms_opt(12, 0, 0).unwrap();

            // Last delivery date
            let last_delivery_date = if total_deliveries > 0 {
                Some(self.start_date - Duration::days(self.rng.gen_range(0..30)))
            } else {
                None
            };

            // Compensation
            let base_pay_per_delivery = match driver_type.as_str() {
                "employee" => self.rng.gen_range(8.0..12.0),
                "contractor" => self.rng.gen_range(6.0..10.0),
                _ => self.rng.gen_range(4.0..8.0),
            };

            let mileage_rate = 0.625; // IRS standard mileage rate
            let avg_tips_per_delivery = self.rng.gen_range(3.0..8.0);

            // Generate email based on driver type
            let email = match driver_type.as_str() {
                "employee" => {
                    // Employees get company email
                    format!("{}.{}@shelfwise.com",
                        first_name.to_lowercase(),
                        last_name.to_lowercase())
                },
                "third_party" => {
                    // Third party drivers get gig platform emails
                    let platforms = vec!["doordash.com", "uber.com", "instacart.com", "postmates.com"];
                    let platform = platforms.choose(&mut self.rng).unwrap();
                    format!("{}.{}@{}",
                        first_name.to_lowercase(),
                        last_name.to_lowercase(),
                        platform)
                },
                _ => {
                    // Contractors use personal email
                    let email_domains = vec!["gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "icloud.com"];
                    let domain = email_domains.choose(&mut self.rng).unwrap();
                    if self.rng.gen::<f64>() < 0.4 {
                        format!("{}.{}{}@{}",
                            first_name.to_lowercase(),
                            last_name.to_lowercase(),
                            self.rng.gen_range(1..99),
                            domain)
                    } else {
                        format!("{}.{}@{}",
                            first_name.to_lowercase(),
                            last_name.to_lowercase(),
                            domain)
                    }
                }
            };

            let driver = DeliveryDriver {
                driver_id,
                first_name,
                last_name,
                phone,
                email,
                driver_type,
                employment_status: employment_status.to_string(),
                primary_store_id: home_store.store_id,
                service_radius_miles,
                service_cities,
                vehicle_type,
                vehicle_capacity_items,
                has_insulated_bags: self.rng.gen::<f64>() < 0.85,
                total_deliveries,
                avg_rating,
                on_time_delivery_pct,
                acceptance_rate,
                cancellation_rate,
                is_available,
                current_latitude,
                current_longitude,
                last_location_update,
                hire_date,
                last_delivery_date,
                base_pay_per_delivery,
                mileage_rate,
                avg_tips_per_delivery,
            };

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
            let start_day = self.rng.gen_range(0..self.dates.len().saturating_sub(15));
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
                assortment.push(Assortment {
                    store_id: store.store_id,
                    sku: product.sku.clone(),
                    active_from: self.start_date,
                    active_to: None,
                    planogram_facings: 2,
                    shelf_height_cm: 150.0,
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
            .get(&store.store_id)
            .map(|customers| customers.clone())
            .or_else(|| city_to_customers.get(store.city.as_str()).map(|customers| customers.clone()))
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
            6 | 7 | 8 => 1.1, // Summer - slightly more active
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

        let distance_miles = rng.gen_range(1.0..12.0);

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
        let driver_pay = driver.base_pay_per_delivery + (distance_miles * driver.mileage_rate);

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

        let driver_tip = if assignment_status == "delivered" && rng.gen::<f64>() < tip_likelihood {
            order_value * tip_percentage
        } else if assignment_status == "delivered" {
            order_value * rng.gen_range(0.0..0.10)
        } else {
            0.0
        };
        let driver_total_earnings = driver_pay + driver_tip;

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

    pub fn save_data(&mut self, output_dir: &str, continue_mode: bool) -> Result<()> {
        println!("============================================================");
        println!("ShelfWise Data Generator - Rust COMPLETE VERSION");
        println!("============================================================\n");

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

        // Write customer data
        if !self.customers.is_empty() {
            let mut wtr = csv::Writer::from_path(Path::new(output_dir).join("customers.csv"))?;
            for c in &self.customers { wtr.serialize(c)?; }
            wtr.flush()?;
        }

        // Write customer addresses
        if !self.customer_addresses.is_empty() {
            let mut wtr = csv::Writer::from_path(Path::new(output_dir).join("customer_addresses.csv"))?;
            for a in &self.customer_addresses { wtr.serialize(a)?; }
            wtr.flush()?;
        }

        // Write delivery zones
        if !self.delivery_zones.is_empty() {
            let mut wtr = csv::Writer::from_path(Path::new(output_dir).join("delivery_zones.csv"))?;
            for z in &self.delivery_zones { wtr.serialize(z)?; }
            wtr.flush()?;
        }

        // Write delivery drivers
        if !self.delivery_drivers.is_empty() {
            let mut wtr = csv::Writer::from_path(Path::new(output_dir).join("delivery_drivers.csv"))?;
            for d in &self.delivery_drivers { wtr.serialize(d)?; }
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
        let common_return_reasons: Vec<String> = return_reasons.iter()
            .filter(|r| r.as_str() == "defective" || r.as_str() == "wrong_item")
            .cloned()
            .collect();

        let waste_reasons = Self::get_waste_reason_codes();
        let perishable_waste_reasons: Vec<String> = waste_reasons.iter()
            .filter(|r| r.as_str() == "expired" || r.as_str() == "temperature_abuse")
            .cloned()
            .collect();

        let payment_methods = Self::get_payment_method_codes();

        // Index: store_id -> Vec<Assortment>
        let mut store_assortment: HashMap<u32, Vec<&Assortment>> = HashMap::new();
        for assort in &self.assortment {
            store_assortment.entry(assort.store_id).or_insert_with(Vec::new).push(assort);
        }

        // Index: sku -> Product (avoid linear search)
        let mut sku_to_product: HashMap<&str, &Product> = HashMap::new();
        for product in &self.products {
            sku_to_product.insert(&product.sku, product);
        }

        // Index: sku -> Vec<&Promotion> (avoid filtering all promotions every time)
        let mut sku_to_promotions: HashMap<&str, Vec<&Promotion>> = HashMap::new();
        for promo in &self.promotions {
            sku_to_promotions.entry(promo.sku.as_str()).or_insert_with(Vec::new).push(promo);
        }

        // Index: store_id -> Vec<&Customer> (for faster customer linking)
        let mut store_to_customers: HashMap<u32, Vec<&Customer>> = HashMap::new();
        for customer in &self.customers {
            store_to_customers.entry(customer.primary_store_id).or_insert_with(Vec::new).push(customer);
        }

        // Index: city -> Vec<&Customer> (fallback for customer linking)
        let mut city_to_customers: HashMap<&str, Vec<&Customer>> = HashMap::new();
        for customer in &self.customers {
            city_to_customers.entry(customer.primary_city.as_str()).or_insert_with(Vec::new).push(customer);
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

        for (idx, date) in dates_clone.iter().enumerate() {
            // Use configured progress interval from config.toml
            if idx % self.config.performance.progress_interval_days == 0 {
                println!("  Day {}/{} ({:.1}%) - {}",
                         idx + 1,
                         total_days,
                         (idx as f64 / total_days as f64) * 100.0,
                         date);
            }

            // Flush periodically to prevent excessive memory usage
            let should_flush = (idx + 1) % self.config.performance.flush_interval_days == 0;

            for store in &stores_clone {
                // Skip stores that haven't opened yet
                if *date < store.opened_date {
                    continue;
                }

                // Get store economics
                let store_econ = self.store_economics.get(&store.store_id).unwrap();

                let mut store_daily_revenue = 0.0;

                // Use pre-built index instead of filtering
                if let Some(store_assortments) = store_assortment.get(&store.store_id) {
                    for assort in store_assortments {
                        // Use pre-built index instead of linear search
                        if let Some(&product) = sku_to_product.get(assort.sku.as_str()) {
                            // Use pre-built index and only filter by date
                            let active_promos: Vec<_> = sku_to_promotions
                                .get(product.sku.as_str())
                                .map(|promos| promos.iter()
                                    .filter(|p| p.start_date <= *date && p.end_date >= *date)
                                    .copied()
                                    .collect())
                                .unwrap_or_else(Vec::new);

                        // Apply category mix factor to demand
                        let category_mix_factor = store_econ.category_mix_factors
                            .get(&product.category)
                            .copied()
                            .unwrap_or(1.0);

                        // Convert to owned only when needed for demand calculation
                        let active_promos_owned: Vec<Promotion> = active_promos.iter().map(|&p| p.clone()).collect();
                        let base_demand = demand_calc.calculate_demand(*date, store, product, &active_promos_owned, 85.0, &mut self.rng);

                        // Adjust demand by category mix and store performance
                        // Store performance uses normal distribution within tiers
                        let performance_multiplier = match store_econ.store_performance_tier.as_str() {
                            "high" => {
                                let normal = Normal::new(1.20, 0.03).unwrap();
                                (normal.sample(&mut self.rng) as f64).clamp(1.12, 1.28)
                            },
                            "low" => {
                                let normal = Normal::new(0.78, 0.04).unwrap();
                                (normal.sample(&mut self.rng) as f64).clamp(0.68, 0.88)
                            },
                            _ => {
                                let normal = Normal::new(1.00, 0.03).unwrap();
                                (normal.sample(&mut self.rng) as f64).clamp(0.92, 1.08)
                            },
                        };

                        let demand = (base_demand as f64 * category_mix_factor * performance_multiplier) as u32;

                        // Use &str to avoid cloning SKU
                        let inv_key = (store.store_id, product.sku.as_str());

                        // Initialize inventory with realistic starting levels
                        if !inventory.contains_key(&inv_key) {
                            let suppliers = crate::reference_data::init_suppliers();
                            let supplier_id = (product.product_id % 30) + 1;
                            let supplier = suppliers.iter().find(|s| s.supplier_id == supplier_id).unwrap();

                            let initial_stock = crate::inventory::calculate_initial_inventory(
                                product,
                                demand,
                                supplier.lead_time_days,
                                &mut self.rng
                            );

                            inventory.insert(inv_key, (initial_stock, 0, Vec::new()));
                            demand_history.insert(inv_key, Vec::new());
                        }

                        // Get current inventory state
                        let (mut on_hand, mut on_order, mut pending_orders) = inventory.get(&inv_key).unwrap().clone();

                        // Update demand history (keep last 30 days)
                        let history = demand_history.get_mut(&inv_key).unwrap();
                        history.push(demand);
                        if history.len() > 30 {
                            history.remove(0);
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

                        if arrived_today > 0 {
                            on_hand += arrived_today;
                            on_order = on_order.saturating_sub(arrived_today);

                            // Record shipment
                            let supplier_id = (product.product_id % 30) + 1;
                            let suppliers = crate::reference_data::init_suppliers();
                            let supplier = suppliers.iter()
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
                        let suppliers = crate::reference_data::init_suppliers();
                        let supplier_id = (product.product_id % 30) + 1;
                        let supplier = suppliers.iter().find(|s| s.supplier_id == supplier_id).unwrap();

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
                        }

                        // Sell units (stockout if not enough inventory)
                        let units_sold = demand.min(on_hand);
                        on_hand = on_hand.saturating_sub(units_sold);

                        // Update inventory state
                        inventory.insert(inv_key, (on_hand, on_order, pending_orders));

                        // Apply store-specific pricing
                        let store_adjusted_price = product.list_price
                            * store_econ.price_premium_index
                            * (1.0 / store_econ.competitive_intensity);  // Higher competition = lower prices

                        let regular_price = store_adjusted_price;
                        let (discount_pct, net_price, promo_id, promo_funding) = if let Some(promo) = active_promos.first() {
                            let net = regular_price * (1.0 - promo.discount_pct as f64 / 100.0);
                            (promo.discount_pct, net, Some(promo.promo_id), promo.supplier_funding_usd * units_sold as f64 / 100.0)
                        } else {
                            (0, regular_price, None, 0.0)
                        };

                        // Apply store-specific cost structure
                        let store_adjusted_cost = product.cost
                            * store_econ.volume_discount_tier
                            * store_econ.maturity_factor;

                        let revenue = units_sold as f64 * net_price;
                        let cogs_c = units_sold as f64 * store_adjusted_cost;
                        let cogs_s = cogs_c * 1.02;

                        // Apply store-specific shrinkage
                        let shrinkage_cost = cogs_c * store_econ.shrinkage_rate;

                        writers.write_sales(&SalesDaily {
                            date: *date,
                            store_id: store.store_id,
                            sku: product.sku.clone(),
                            units_sold,
                            gross_revenue: revenue,
                            promo_id,
                            regular_price,
                            net_price,
                            revenue,
                            supplier_rebate_amt: if self.rng.gen::<f64>() < 0.3 { revenue * 0.02 } else { 0.0 },
                            spoilage_cost: if matches!(product.category.as_str(), "dairy" | "produce" | "meat") {
                                cogs_c * self.rng.gen_range(0.005..0.015)
                            } else {
                                shrinkage_cost
                            },
                            promo_funding_received: promo_funding,
                            gross_margin_pct: if revenue > 0.0 {
                                ((revenue - cogs_c - shrinkage_cost) / revenue) * 100.0
                            } else {
                                0.0
                            },
                            discount_pct,
                            cogs_c,
                            cogs_s,
                            sales_date: *date,
                            posting_date: *date + Duration::days(7),
                        })?;

                        store_daily_revenue += revenue;

                        // Get current inventory state for reporting
                        let (current_on_hand, current_on_order, pending) = inventory.get(&inv_key).unwrap();

                        // Calculate in_transit (orders not yet delivered)
                        let in_transit: u32 = pending.iter()
                            .filter(|(delivery_date, _)| delivery_date > date)
                            .map(|(_, qty)| qty)
                            .sum();

                        // Calculate realistic safety stock
                        let suppliers = crate::reference_data::init_suppliers();
                        let supplier_id = (product.product_id % 30) + 1;
                        let supplier = suppliers.iter().find(|s| s.supplier_id == supplier_id).unwrap();

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

                        if units_sold > 0 && self.rng.gen::<f64>() < 0.01 {
                            writers.write_return(&ReturnDaily {
                                date: *date,
                                store_id: store.store_id,
                                sku: product.sku.clone(),
                                units_returned: self.rng.gen_range(1..=units_sold.min(3)),
                                reason_code: common_return_reasons.choose(&mut self.rng).unwrap().clone(),
                                refund_value: net_price,
                            })?;
                        }

                        if matches!(product.category.as_str(), "dairy" | "produce" | "meat") && self.rng.gen::<f64>() < 0.02 {
                            let recorded_by = format!("emp_{}", self.rng.gen_range(100..999));

                            writers.write_waste(&WasteSpoilage {
                                waste_id,
                                date: *date,
                                store_id: store.store_id,
                                sku: product.sku.clone(),
                                quantity_wasted: self.rng.gen_range(1..5),
                                waste_reason: perishable_waste_reasons.choose(&mut self.rng).unwrap().clone(),
                                waste_value: product.cost,
                                recorded_by,
                            })?;
                            waste_id += 1;
                        }

                        if on_hand == 0 && demand > 0 && self.rng.gen::<f64>() < 0.1 {
                            let created_at = format!("{} 10:00:00", date);
                            let resolved_at = if self.rng.gen::<f64>() < 0.7 {
                                Some(format!("{} 14:00:00", date))
                            } else {
                                None
                            };

                            writers.write_ticket(&Ticket {
                                ticket_id,
                                created_at,
                                resolved_at,
                                store_id: store.store_id,
                                sku: product.sku.clone(),
                                issue_type: "stockout".to_string(),
                                description: "Out of stock".to_string(),
                                root_cause: Some("supplier_delay".to_string()),
                                resolved: true,
                            })?;
                            ticket_id += 1;
                        }

                        if self.rng.gen::<f64>() < 0.002 {
                            writers.write_price_change(&PriceChange {
                                change_id,
                                date: *date,
                                store_id: store.store_id,
                                sku: product.sku.clone(),
                                new_regular_price: regular_price * 1.05,
                                reason: "cost_increase".to_string(),
                            })?;
                            change_id += 1;
                        }
                    }
                } // end if let Some(store_assortments)
                } // end for assort

                // Generate transactions for this store-day
                if store_daily_revenue > 0.0 {
                    let (txn_value_min, txn_value_max, max_txns_min, max_txns_max, basket_min, basket_max) = match store.store_type.as_str() {
                        "online" => (80.0, 180.0, 950, 1050, 20, 50),
                        "big_box" => (65.0, 95.0, 750, 850, 25, 45),
                        "suburban" => (45.0, 75.0, 475, 525, 12, 25),
                        "urban" => (30.0, 50.0, 380, 420, 8, 18),
                        "convenience" => (15.0, 30.0, 190, 210, 1, 5),
                        _ => (50.0, 80.0, 475, 525, 12, 25),
                    };

                    // Use main RNG for more variability instead of deterministic day seed
                    let target_txn_value = self.rng.gen_range(txn_value_min..txn_value_max);
                    let max_txns = self.rng.gen_range(max_txns_min..=max_txns_max);

                    let num_transactions = (store_daily_revenue / target_txn_value).ceil() as u32;
                    let num_transactions = num_transactions.min(max_txns);
                    let num_transactions = num_transactions.max(1);

                    // Generate varied basket values that sum to store_daily_revenue
                    let mut basket_values = Vec::new();
                    let mut total_allocated = 0.0;

                    for i in 0..num_transactions {
                        let basket_items = self.rng.gen_range(basket_min..=basket_max);

                        if i == num_transactions - 1 {
                            // Last transaction gets the remainder to ensure exact match
                            basket_values.push((basket_items, store_daily_revenue - total_allocated));
                        } else {
                            // Vary basket value with randomness, but track total
                            let base_basket_value = store_daily_revenue / num_transactions as f64;
                            let basket_value = base_basket_value * self.rng.gen_range(0.7..1.3);
                            total_allocated += basket_value;
                            basket_values.push((basket_items, basket_value));
                        }
                    }

                    // Pre-generate transaction data to avoid borrow conflicts with demand_calc
                    let mut transaction_data = Vec::new();
                    for (basket_items, basket_value) in basket_values {
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
                            basket_items,
                            basket_value,
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
                    for (basket_items, basket_value, hour, minute, _rand_customer, rand_fulfillment,
                         rand_delivery_fee, rand_tip, rand_tip_amount, rand_status, _time_off1, _time_off2) in transaction_data {
                        let timestamp = format!("{} {:02}:{:02}:00", date.format("%Y-%m-%d"), hour, minute);

                        // Clone store data
                        let store_clone = store.clone();
                        let store_type = store.store_type.clone();

                        // Determine customer linkage using indexed lookup
                        let (customer_id, is_loyalty_transaction, loyalty_points_earned, loyalty_points_redeemed) =
                            Self::maybe_link_customer_static(&mut self.rng, &store_clone, &store_type, &store_to_customers, &city_to_customers, &self.customers);

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

                        // Delivery/pickup fields using pre-generated randoms
                        let (delivery_fee, tip_amount, order_status, delivery_address_id, requested_time, actual_time) =
                            if fulfillment_type.as_ref().map_or(false, |f| f == "delivery" || f == "pickup") {
                                let fee = if fulfillment_type.as_ref().unwrap() == "pickup" { 0.0 } else {
                                    match store.store_type.as_str() {
                                        "online" => 4.99 + rand_delivery_fee * 5.0,
                                        _ => 2.99 + rand_delivery_fee * 5.0,
                                    }
                                };

                                let tip = if rand_tip < 0.7 {
                                    basket_value * (0.10 + rand_tip_amount * 0.10)
                                } else {
                                    basket_value * (rand_tip_amount * 0.10)
                                };

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

                        let transaction = Transaction {
                            transaction_id: global_txn_id,
                            date: *date,
                            store_id: store.store_id,
                            timestamp: timestamp.clone(),
                            total_items: basket_items,
                            payment_method: payment_methods.choose(&mut self.rng).unwrap().clone(),
                            customer_type: "regular".to_string(),
                            total_amount: basket_value,
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

                        // Create delivery assignment if needed (now works because demand_calc is dropped)
                        if transaction.fulfillment_type.as_ref().map_or(false, |f| f == "delivery" || f == "pickup") &&
                           transaction.order_status.as_ref().map_or(false, |s| s == "delivered") {
                            let fulfillment_str = transaction.fulfillment_type.as_ref().unwrap().clone();
                            Self::create_delivery_assignment_static(
                                &mut self.rng,
                                &mut writers,
                                global_txn_id,
                                store_clone.store_id,
                                &fulfillment_str,
                                date,
                                &timestamp,
                                45,
                                basket_value,
                                &self.delivery_drivers,
                                &self.stores,
                            )?;
                        }

                        global_txn_id += 1;
                    }
                }
            }

            // Flush every N days instead of every day for better performance
            if should_flush {
                writers.flush_all()?;
            }
        }

        // Final flush to ensure all data is written
        writers.flush_all()?;

        Ok(())
    }
}
