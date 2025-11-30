use crate::demand::DemandCalculator;
use crate::holidays::generate_all_holidays;
use crate::models::*;
use crate::streaming::StreamingWriters;
use anyhow::Result;
use chrono::{Datelike, Duration, NaiveDate, NaiveDateTime};
use rand::prelude::*;
use rand_distr::{Distribution, Exp};
use std::collections::HashMap;
use std::path::Path;

// Full historical data: February 1, 2019 to November 30, 2025
// This captures ~7 years including pre-COVID, COVID, and recovery periods
const START_DATE: (i32, u32, u32) = (2019, 2, 1);
const END_DATE: (i32, u32, u32) = (2025, 11, 30);

pub struct ShelfWiseDataGenerator {
    rng: StdRng,
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
}

impl ShelfWiseDataGenerator {
    pub fn new(seed: u64) -> Self {
        let rng = StdRng::seed_from_u64(seed);
        let start_date = NaiveDate::from_ymd_opt(START_DATE.0, START_DATE.1, START_DATE.2).unwrap();
        let end_date = NaiveDate::from_ymd_opt(END_DATE.0, END_DATE.1, END_DATE.2).unwrap();
        
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
        }
    }

    fn init_categories() -> HashMap<String, CategoryConfig> {
        let mut categories = HashMap::new();
        categories.insert("cereal".to_string(), CategoryConfig { elasticity: -0.6, seasonality: "steady".to_string(), dow_effect: 0.05 });
        categories.insert("dairy".to_string(), CategoryConfig { elasticity: -0.8, seasonality: "steady".to_string(), dow_effect: 0.10 });
        categories.insert("snacks".to_string(), CategoryConfig { elasticity: -1.0, seasonality: "event_driven".to_string(), dow_effect: 0.15 });
        categories.insert("beverages".to_string(), CategoryConfig { elasticity: -1.2, seasonality: "summer".to_string(), dow_effect: 0.12 });
        categories.insert("produce".to_string(), CategoryConfig { elasticity: -0.9, seasonality: "steady".to_string(), dow_effect: 0.08 });
        categories.insert("household".to_string(), CategoryConfig { elasticity: -0.4, seasonality: "steady".to_string(), dow_effect: -0.05 });
        categories.insert("frozen".to_string(), CategoryConfig { elasticity: -0.7, seasonality: "winter".to_string(), dow_effect: 0.06 });
        categories.insert("bakery".to_string(), CategoryConfig { elasticity: -0.8, seasonality: "steady".to_string(), dow_effect: 0.12 });
        categories.insert("meat".to_string(), CategoryConfig { elasticity: -0.9, seasonality: "event_driven".to_string(), dow_effect: 0.18 });
        categories.insert("canned".to_string(), CategoryConfig { elasticity: -0.5, seasonality: "winter".to_string(), dow_effect: 0.03 });
        categories.insert("personal_care".to_string(), CategoryConfig { elasticity: -0.6, seasonality: "steady".to_string(), dow_effect: 0.02 });
        categories.insert("candy".to_string(), CategoryConfig { elasticity: -1.1, seasonality: "event_driven".to_string(), dow_effect: 0.10 });
        categories
    }

    fn init_brands() -> Vec<BrandInfo> {
        vec![
            // ShelfWise Private Label Brands
            BrandInfo { name: "ShelfWise Select".to_string(), tier: "premium".to_string(), popularity: 1.1 },
            BrandInfo { name: "ShelfWise Basics".to_string(), tier: "value".to_string(), popularity: 1.25 },
            BrandInfo { name: "ShelfWise Organic".to_string(), tier: "premium".to_string(), popularity: 0.9 },
            BrandInfo { name: "ShelfWise Fresh".to_string(), tier: "mid".to_string(), popularity: 1.15 },
            
            // Major CPG Manufacturers
            BrandInfo { name: "Kelloggs".to_string(), tier: "premium".to_string(), popularity: 1.2 },
            BrandInfo { name: "General Mills".to_string(), tier: "premium".to_string(), popularity: 1.15 },
            BrandInfo { name: "Nestle".to_string(), tier: "mid".to_string(), popularity: 1.1 },
            BrandInfo { name: "Kraft Heinz".to_string(), tier: "mid".to_string(), popularity: 1.3 },
            BrandInfo { name: "PepsiCo".to_string(), tier: "mid".to_string(), popularity: 1.2 },
            BrandInfo { name: "Coca-Cola".to_string(), tier: "mid".to_string(), popularity: 1.25 },
            BrandInfo { name: "Unilever".to_string(), tier: "premium".to_string(), popularity: 1.0 },
            BrandInfo { name: "Procter & Gamble".to_string(), tier: "premium".to_string(), popularity: 1.05 },
            BrandInfo { name: "Campbell Soup".to_string(), tier: "mid".to_string(), popularity: 0.95 },
            BrandInfo { name: "ConAgra".to_string(), tier: "mid".to_string(), popularity: 0.9 },
            BrandInfo { name: "Mondelez".to_string(), tier: "mid".to_string(), popularity: 1.1 },
            BrandInfo { name: "Mars".to_string(), tier: "premium".to_string(), popularity: 1.05 },
            BrandInfo { name: "Hershey".to_string(), tier: "mid".to_string(), popularity: 1.0 },
            BrandInfo { name: "Frito-Lay".to_string(), tier: "mid".to_string(), popularity: 1.35 },
            BrandInfo { name: "Quaker".to_string(), tier: "mid".to_string(), popularity: 1.0 },
            BrandInfo { name: "Dole".to_string(), tier: "mid".to_string(), popularity: 0.95 },
            BrandInfo { name: "Del Monte".to_string(), tier: "mid".to_string(), popularity: 0.9 },
            BrandInfo { name: "Tyson Foods".to_string(), tier: "mid".to_string(), popularity: 1.1 },
            BrandInfo { name: "Hormel".to_string(), tier: "mid".to_string(), popularity: 0.95 },
            BrandInfo { name: "Smithfield".to_string(), tier: "value".to_string(), popularity: 0.9 },
            BrandInfo { name: "Perdue".to_string(), tier: "mid".to_string(), popularity: 0.95 },
            BrandInfo { name: "Danone".to_string(), tier: "premium".to_string(), popularity: 0.85 },
            BrandInfo { name: "Chobani".to_string(), tier: "premium".to_string(), popularity: 0.9 },
            BrandInfo { name: "Blue Diamond".to_string(), tier: "premium".to_string(), popularity: 0.8 },
            BrandInfo { name: "Wonderful".to_string(), tier: "premium".to_string(), popularity: 0.85 },
            BrandInfo { name: "Annies Homegrown".to_string(), tier: "premium".to_string(), popularity: 0.85 },
            BrandInfo { name: "Organic Valley".to_string(), tier: "premium".to_string(), popularity: 0.8 },
            BrandInfo { name: "Horizon Organic".to_string(), tier: "premium".to_string(), popularity: 0.75 },
            BrandInfo { name: "Bobs Red Mill".to_string(), tier: "premium".to_string(), popularity: 0.7 },
            BrandInfo { name: "Kind".to_string(), tier: "premium".to_string(), popularity: 0.85 },
            BrandInfo { name: "Clif Bar".to_string(), tier: "premium".to_string(), popularity: 0.8 },
            BrandInfo { name: "Nature Valley".to_string(), tier: "mid".to_string(), popularity: 1.05 },
            BrandInfo { name: "Nabisco".to_string(), tier: "mid".to_string(), popularity: 1.15 },
            BrandInfo { name: "Ritz".to_string(), tier: "mid".to_string(), popularity: 1.1 },
            BrandInfo { name: "Pepperidge Farm".to_string(), tier: "premium".to_string(), popularity: 0.95 },
            BrandInfo { name: "Barilla".to_string(), tier: "mid".to_string(), popularity: 1.0 },
            BrandInfo { name: "Hunts".to_string(), tier: "value".to_string(), popularity: 0.95 },
            BrandInfo { name: "Progresso".to_string(), tier: "mid".to_string(), popularity: 0.9 },
            BrandInfo { name: "Swanson".to_string(), tier: "value".to_string(), popularity: 0.85 },
            BrandInfo { name: "Green Giant".to_string(), tier: "mid".to_string(), popularity: 0.95 },
            BrandInfo { name: "Birds Eye".to_string(), tier: "mid".to_string(), popularity: 0.9 },
            BrandInfo { name: "Lean Cuisine".to_string(), tier: "mid".to_string(), popularity: 0.85 },
            BrandInfo { name: "Stouffers".to_string(), tier: "mid".to_string(), popularity: 0.95 },
            BrandInfo { name: "DiGiorno".to_string(), tier: "premium".to_string(), popularity: 1.0 },
            BrandInfo { name: "Haagen-Dazs".to_string(), tier: "premium".to_string(), popularity: 0.9 },
            BrandInfo { name: "Ben & Jerrys".to_string(), tier: "premium".to_string(), popularity: 0.95 },
            BrandInfo { name: "Breyers".to_string(), tier: "mid".to_string(), popularity: 1.0 },
            BrandInfo { name: "Dreyers".to_string(), tier: "mid".to_string(), popularity: 0.95 },
            BrandInfo { name: "PolarSprings".to_string(), tier: "mid".to_string(), popularity: 1.0 },
            BrandInfo { name: "Dasani".to_string(), tier: "mid".to_string(), popularity: 0.95 },
            BrandInfo { name: "Smartwater".to_string(), tier: "premium".to_string(), popularity: 0.85 },
            BrandInfo { name: "Fiji".to_string(), tier: "premium".to_string(), popularity: 0.8 },
            BrandInfo { name: "Poland Spring".to_string(), tier: "value".to_string(), popularity: 1.1 },
            BrandInfo { name: "Gatorade".to_string(), tier: "mid".to_string(), popularity: 1.15 },
            BrandInfo { name: "Powerade".to_string(), tier: "mid".to_string(), popularity: 0.95 },
            BrandInfo { name: "Tropicana".to_string(), tier: "premium".to_string(), popularity: 1.05 },
            BrandInfo { name: "Simply".to_string(), tier: "premium".to_string(), popularity: 0.95 },
            BrandInfo { name: "Minute Maid".to_string(), tier: "mid".to_string(), popularity: 1.0 },
            BrandInfo { name: "Ocean Spray".to_string(), tier: "mid".to_string(), popularity: 0.9 },
        ]
    }

    pub fn generate_products(&mut self) {
        let mut products = Vec::new();
        let mut product_id = 1;

        let sub_categories: HashMap<&str, Vec<&str>> = [
            ("cereal", vec!["oats", "corn_flakes", "granola"]),
            ("dairy", vec!["milk", "cheese", "yogurt"]),
            ("snacks", vec!["chips", "crackers", "nuts"]),
            ("beverages", vec!["cola", "juice", "water"]),
            ("produce", vec!["apples", "bananas", "lettuce"]),
            ("household", vec!["paper_towels", "soap"]),
            ("frozen", vec!["ice_cream", "pizza"]),
            ("bakery", vec!["bread", "bagels"]),
            ("meat", vec!["chicken", "beef"]),
            ("canned", vec!["soup", "vegetables"]),
            ("personal_care", vec!["shampoo", "toothpaste"]),
            ("candy", vec!["chocolate", "gummies"]),
        ].iter().cloned().collect();

        for brand in &self.brands {
            for (category, subs) in &sub_categories {
                let sub_category = subs.choose(&mut self.rng).unwrap();
                let base_price = self.rng.gen_range(2.0..20.0);
                let list_price = match brand.tier.as_str() {
                    "premium" => base_price * 1.5,
                    "value" => base_price * 0.8,
                    _ => base_price,
                };
                
                // Realistic cost margins vary by category, brand tier, and randomness
                // Category-based margin profiles (lower cost ratio = higher margin)
                let category_cost_ratio = match *category {
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
                    size: "medium".to_string(),
                    unit_of_measure: "each".to_string(),
                    list_price: ((list_price * 100.0) as f64).round() / 100.0,
                    cost: ((cost * 100.0) as f64).round() / 100.0,
                    launch_date: self.start_date,
                    discontinue_date: None,
                    brand_popularity: brand.popularity,
                    tier: brand.tier.clone(),
                    pareto_weight: 0.0,
                });
                
                product_id += 1;
                // Reduced product count: 400 products for manageable data size
                // Still realistic for a focused grocery category
                if product_id > 400 { break; }
            }
            if product_id > 400 { break; }
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

        // Generate 100 domestic stores - represents a strong regional/national chain
        // Distribution: ~40 urban, ~63 suburban, ~20 convenience, ~14 big_box
        for _ in 0..100 {
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

        // Add 5 international stores - all opened during data range (2020-2024)
        for (city, lat, lon, store_type, days_after_start) in international_stores.iter() {
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
                promo_type: "price_cut".to_string(),
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
            let num_skus = match store.store_type.as_str() {
                "online" => self.products.len(),
                "big_box" => (self.products.len() as f64 * 0.9) as usize,
                _ => (self.products.len() as f64 * 0.7) as usize,
            };

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

    pub fn save_data(&mut self, output_dir: &str, continue_mode: bool) -> Result<()> {
        println!("============================================================");
        println!("ShelfWise Data Generator - Rust COMPLETE VERSION");
        println!("============================================================\n");

        if self.products.is_empty() { self.generate_products(); }
        if self.stores.is_empty() { self.generate_stores(); }
        if self.store_economics.is_empty() { self.generate_store_economics(); }
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

        Ok(())
    }

    fn generate_daily_data_complete(&mut self, output_dir: &str, continue_mode: bool) -> Result<()> {
        let mut writers = StreamingWriters::new(output_dir, continue_mode)?;
        let mut inventory: HashMap<(u32, String), u32> = HashMap::new();
        let mut shipment_id = 1;
        let mut waste_id = 1;
        let mut ticket_id = 1;
        let mut change_id = 1;
        let mut global_txn_id = 1;
        
        let demand_calc = DemandCalculator {
            categories: &self.categories,
            holidays: &self.holidays,
            calendar: &self.calendar,
            ground_truth_events: &self.ground_truth_events,
        };

        let total_days = self.dates.len();
        println!("  Generating data for {} days ({} to {})",
                 total_days,
                 self.dates.first().unwrap(),
                 self.dates.last().unwrap());
        println!("  Estimated records: ~{} million",
                 (total_days * self.stores.len() * self.products.len() * 7 / 10) / 1_000_000);
        
        for (idx, date) in self.dates.iter().enumerate() {
            if idx % 50 == 0 {
                println!("  Day {}/{} ({:.1}%) - {}",
                         idx + 1,
                         total_days,
                         (idx as f64 / total_days as f64) * 100.0,
                         date);
            }

            for store in &self.stores {
                // Skip stores that haven't opened yet
                if *date < store.opened_date {
                    continue;
                }
                
                // Get store economics
                let store_econ = self.store_economics.get(&store.store_id).unwrap();
                
                let mut store_daily_revenue = 0.0;
                for assort in self.assortment.iter().filter(|a| a.store_id == store.store_id) {
                    if let Some(product) = self.products.iter().find(|p| p.sku == assort.sku) {
                        let active_promos: Vec<_> = self.promotions.iter()
                            .filter(|p| p.sku == product.sku && p.start_date <= *date && p.end_date >= *date)
                            .collect();

                        // Apply category mix factor to demand
                        let category_mix_factor = store_econ.category_mix_factors
                            .get(&product.category)
                            .copied()
                            .unwrap_or(1.0);
                        
                        let active_promos_slice: Vec<Promotion> = active_promos.iter().map(|p| (*p).clone()).collect();
                        let base_demand = demand_calc.calculate_demand(*date, store, product, &active_promos_slice, 85.0, &mut self.rng);
                        
                        // Adjust demand by category mix and store performance
                        let performance_multiplier = match store_econ.store_performance_tier.as_str() {
                            "high" => self.rng.gen_range(1.15..1.25),
                            "low" => self.rng.gen_range(0.70..0.85),
                            _ => self.rng.gen_range(0.95..1.05),
                        };
                        
                        let demand = (base_demand as f64 * category_mix_factor * performance_multiplier) as u32;
                        
                        let inv_key = (store.store_id, product.sku.clone());
                        if !inventory.contains_key(&inv_key) {
                            let base = match store.store_type.as_str() {
                                "online" => demand * 14,
                                "big_box" => demand * 10,
                                _ => demand * 7,
                            };
                            inventory.insert(inv_key.clone(), (base as f64 * self.rng.gen_range(0.8..1.2)) as u32);
                        }
                        
                        let mut on_hand = *inventory.get(&inv_key).unwrap();
                        
                        let delivery_chance = match store.store_type.as_str() {
                            "online" => 0.6,
                            "big_box" => 0.4,
                            _ => 0.25,
                        };
                        
                        if self.rng.gen::<f64>() < delivery_chance {
                            let delivered = match store.store_type.as_str() {
                                "online" => self.rng.gen_range(500..2000),
                                "big_box" => self.rng.gen_range(200..800),
                                _ => self.rng.gen_range(50..300),
                            };
                            on_hand += delivered;
                            inventory.insert(inv_key.clone(), on_hand);
                            
                            writers.write_shipment(&SupplierShipment {
                                shipment_id,
                                shipment_date: *date - Duration::days(self.rng.gen_range(1..3)),
                                delivery_date: *date,
                                store_id: store.store_id,
                                sku: product.sku.clone(),
                                quantity_shipped: delivered,
                                quantity_received: delivered,
                                supplier_name: format!("{} Supplier", product.brand),
                                po_number: format!("PO-{:06}", shipment_id),
                                shipment_status: "delivered".to_string(),
                            })?;
                            shipment_id += 1;
                        }
                        
                        let units_sold = demand.min(on_hand);
                        inventory.insert(inv_key.clone(), on_hand.saturating_sub(units_sold));
                        
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
                        
                        writers.write_inventory(&InventoryDaily {
                            date: *date,
                            store_id: store.store_id,
                            sku: product.sku.clone(),
                            on_hand: *inventory.get(&inv_key).unwrap(),
                            on_order: 0,
                            in_transit: 0,
                            safety_stock: demand * 3,
                            last_scan_ts: NaiveDateTime::new(*date, chrono::NaiveTime::from_hms_opt(12, 0, 0).unwrap()),
                            system_on_hand: *inventory.get(&inv_key).unwrap(),
                            available_to_promise: on_hand,
                            open_hours: if store.store_type == "online" { 24 } else { 12 },
                            in_stock_hours: 12.0,
                            dc_allocated_qty: 0,
                            quarantine_hold: 0,
                        })?;
                        
                        if units_sold > 0 && self.rng.gen::<f64>() < 0.01 {
                            writers.write_return(&ReturnDaily {
                                date: *date,
                                store_id: store.store_id,
                                sku: product.sku.clone(),
                                units_returned: self.rng.gen_range(1..=units_sold.min(3)),
                                reason_code: ["defective", "wrong_item"].choose(&mut self.rng).unwrap().to_string(),
                                refund_value: net_price,
                            })?;
                        }
                        
                        if matches!(product.category.as_str(), "dairy" | "produce" | "meat") && self.rng.gen::<f64>() < 0.02 {
                            writers.write_waste(&WasteSpoilage {
                                waste_id,
                                date: *date,
                                store_id: store.store_id,
                                sku: product.sku.clone(),
                                quantity_wasted: self.rng.gen_range(1..5),
                                waste_reason: "expired".to_string(),
                                waste_value: product.cost,
                                recorded_by: format!("emp_{}", self.rng.gen_range(100..999)),
                            })?;
                            waste_id += 1;
                        }
                        
                        if on_hand == 0 && demand > 0 && self.rng.gen::<f64>() < 0.1 {
                            writers.write_ticket(&Ticket {
                                ticket_id,
                                created_at: format!("{} 10:00:00", date),
                                resolved_at: if self.rng.gen::<f64>() < 0.7 { Some(format!("{} 14:00:00", date)) } else { None },
                                store_id: store.store_id,
                                sku: product.sku.clone(),
                                issue_type: "stockout".to_string(),
                                description: format!("Out of stock"),
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
                }
                
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
                    
                    let day_seed = (store.store_id as u64 * 1000) + idx as u64;
                    let mut day_rng = StdRng::seed_from_u64(day_seed);
                    let target_txn_value = day_rng.gen_range(txn_value_min..txn_value_max);
                    let max_txns = day_rng.gen_range(max_txns_min..=max_txns_max);
                    
                    let num_transactions = (store_daily_revenue / target_txn_value).ceil() as u32;
                    let num_transactions = num_transactions.min(max_txns);
                    let num_transactions = num_transactions.max(1);
                    
                    // Generate varied basket values that sum to store_daily_revenue
                    let mut basket_values = Vec::new();
                    let mut total_allocated = 0.0;
                    
                    for i in 0..num_transactions {
                        let basket_items = day_rng.gen_range(basket_min..=basket_max);
                        
                        if i == num_transactions - 1 {
                            // Last transaction gets the remainder to ensure exact match
                            basket_values.push((basket_items, store_daily_revenue - total_allocated));
                        } else {
                            // Vary basket value with randomness, but track total
                            let base_basket_value = store_daily_revenue / num_transactions as f64;
                            let basket_value = base_basket_value * day_rng.gen_range(0.7..1.3);
                            total_allocated += basket_value;
                            basket_values.push((basket_items, basket_value));
                        }
                    }
                    
                    for (basket_items, basket_value) in basket_values {
                        let hour = self.rng.gen_range(8..22);
                        let minute = self.rng.gen_range(0..60);
                        let timestamp = format!("{} {:02}:{:02}:00", date.format("%Y-%m-%d"), hour, minute);
                        
                        writers.write_transaction(&Transaction {
                            transaction_id: global_txn_id,
                            date: *date,
                            store_id: store.store_id,
                            timestamp,
                            total_items: basket_items,
                            payment_method: "credit".to_string(),
                            customer_type: "regular".to_string(),
                            total_amount: basket_value,
                        })?;
                        
                        global_txn_id += 1;
                    }
                }
            }
            writers.flush_all()?;
        }

        Ok(())
    }
}
