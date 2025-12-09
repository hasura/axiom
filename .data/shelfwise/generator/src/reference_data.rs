
use crate::models::*;

/// Initialize regions reference data
pub fn init_regions() -> Vec<Region> {
    vec![
        Region {
            region_id: 1,
            region_code: "west_coast".to_string(),
            region_name: "West Coast".to_string(),
            country: "USA".to_string(),
            timezone: "America/Los_Angeles".to_string(),
            description: "Bay Area core market - company founded here".to_string(),
        },
        Region {
            region_id: 2,
            region_code: "southwest".to_string(),
            region_name: "Southwest".to_string(),
            country: "USA".to_string(),
            timezone: "America/Phoenix".to_string(),
            description: "Arizona, Nevada, Colorado expansion".to_string(),
        },
        Region {
            region_id: 3,
            region_code: "expansion".to_string(),
            region_name: "National Expansion".to_string(),
            country: "USA".to_string(),
            timezone: "America/Chicago".to_string(),
            description: "Strategic national markets - Austin, Chicago, NYC, Boston, Atlanta, Miami".to_string(),
        },
        Region {
            region_id: 4,
            region_code: "international".to_string(),
            region_name: "International".to_string(),
            country: "Multiple".to_string(),
            timezone: "UTC".to_string(),
            description: "Canada and UK test markets".to_string(),
        },
        Region {
            region_id: 5,
            region_code: "nationwide".to_string(),
            region_name: "Nationwide Online".to_string(),
            country: "USA".to_string(),
            timezone: "America/Los_Angeles".to_string(),
            description: "Online fulfillment center".to_string(),
        },
    ]
}

/// Initialize categories reference data
pub fn init_categories() -> Vec<Category> {
    vec![
        Category {
            category_id: 1,
            category_name: "cereal".to_string(),
            category_group: "dry_goods".to_string(),
            margin_target_pct: 35.00,
            is_perishable: false,
            elasticity: -0.6,
        },
        Category {
            category_id: 2,
            category_name: "dairy".to_string(),
            category_group: "refrigerated".to_string(),
            margin_target_pct: 25.00,
            is_perishable: true,
            elasticity: -0.8,
        },
        Category {
            category_id: 3,
            category_name: "snacks".to_string(),
            category_group: "dry_goods".to_string(),
            margin_target_pct: 42.00,
            is_perishable: false,
            elasticity: -1.0,
        },
        Category {
            category_id: 4,
            category_name: "beverages".to_string(),
            category_group: "dry_goods".to_string(),
            margin_target_pct: 40.00,
            is_perishable: false,
            elasticity: -1.2,
        },
        Category {
            category_id: 5,
            category_name: "produce".to_string(),
            category_group: "fresh".to_string(),
            margin_target_pct: 22.00,
            is_perishable: true,
            elasticity: -0.9,
        },
        Category {
            category_id: 6,
            category_name: "household".to_string(),
            category_group: "non_food".to_string(),
            margin_target_pct: 52.00,
            is_perishable: false,
            elasticity: -0.4,
        },
        Category {
            category_id: 7,
            category_name: "frozen".to_string(),
            category_group: "frozen".to_string(),
            margin_target_pct: 32.00,
            is_perishable: false,
            elasticity: -0.7,
        },
        Category {
            category_id: 8,
            category_name: "bakery".to_string(),
            category_group: "fresh".to_string(),
            margin_target_pct: 30.00,
            is_perishable: true,
            elasticity: -0.8,
        },
        Category {
            category_id: 9,
            category_name: "meat".to_string(),
            category_group: "fresh".to_string(),
            margin_target_pct: 20.00,
            is_perishable: true,
            elasticity: -0.9,
        },
        Category {
            category_id: 10,
            category_name: "canned".to_string(),
            category_group: "dry_goods".to_string(),
            margin_target_pct: 35.00,
            is_perishable: false,
            elasticity: -0.5,
        },
        Category {
            category_id: 11,
            category_name: "personal_care".to_string(),
            category_group: "non_food".to_string(),
            margin_target_pct: 55.00,
            is_perishable: false,
            elasticity: -0.6,
        },
        Category {
            category_id: 12,
            category_name: "candy".to_string(),
            category_group: "dry_goods".to_string(),
            margin_target_pct: 45.00,
            is_perishable: false,
            elasticity: -1.1,
        },
    ]
}

/// Initialize store types reference data
pub fn init_store_types() -> Vec<StoreType> {
    vec![
        StoreType {
            store_type_id: 1,
            store_type_code: "online".to_string(),
            store_type_name: "Online Fulfillment Center".to_string(),
            typical_sq_ft_min: 400000,
            typical_sq_ft_max: 600000,
            typical_sku_count: 400,
            operating_hours: 24,
        },
        StoreType {
            store_type_id: 2,
            store_type_code: "big_box".to_string(),
            store_type_name: "Big Box Store".to_string(),
            typical_sq_ft_min: 60000,
            typical_sq_ft_max: 100000,
            typical_sku_count: 360,
            operating_hours: 14,
        },
        StoreType {
            store_type_id: 3,
            store_type_code: "suburban".to_string(),
            store_type_name: "Suburban Store".to_string(),
            typical_sq_ft_min: 25000,
            typical_sq_ft_max: 45000,
            typical_sku_count: 280,
            operating_hours: 12,
        },
        StoreType {
            store_type_id: 4,
            store_type_code: "urban".to_string(),
            store_type_name: "Urban Store".to_string(),
            typical_sq_ft_min: 10000,
            typical_sq_ft_max: 20000,
            typical_sku_count: 280,
            operating_hours: 14,
        },
        StoreType {
            store_type_id: 5,
            store_type_code: "convenience".to_string(),
            store_type_name: "Convenience Store".to_string(),
            typical_sq_ft_min: 3000,
            typical_sq_ft_max: 8000,
            typical_sku_count: 280,
            operating_hours: 16,
        },
    ]
}

/// Initialize brands reference data
pub fn init_brands_reference() -> Vec<Brand> {
    vec![
        // ShelfWise Private Label
        Brand {
            brand_id: 1,
            brand_name: "ShelfWise Select".to_string(),
            brand_tier: "premium".to_string(),
            manufacturer: "ShelfWise".to_string(),
            is_private_label: true,
            brand_popularity: 1.1,
        },
        Brand {
            brand_id: 2,
            brand_name: "ShelfWise Basics".to_string(),
            brand_tier: "value".to_string(),
            manufacturer: "ShelfWise".to_string(),
            is_private_label: true,
            brand_popularity: 1.25,
        },
        Brand {
            brand_id: 3,
            brand_name: "ShelfWise Organic".to_string(),
            brand_tier: "premium".to_string(),
            manufacturer: "ShelfWise".to_string(),
            is_private_label: true,
            brand_popularity: 0.9,
        },
        Brand {
            brand_id: 4,
            brand_name: "ShelfWise Fresh".to_string(),
            brand_tier: "mid".to_string(),
            manufacturer: "ShelfWise".to_string(),
            is_private_label: true,
            brand_popularity: 1.15,
        },
        // Major CPG Manufacturers
        Brand {
            brand_id: 5,
            brand_name: "Kelloggs".to_string(),
            brand_tier: "premium".to_string(),
            manufacturer: "Kellogg Company".to_string(),
            is_private_label: false,
            brand_popularity: 1.2,
        },
        Brand {
            brand_id: 6,
            brand_name: "General Mills".to_string(),
            brand_tier: "premium".to_string(),
            manufacturer: "General Mills Inc".to_string(),
            is_private_label: false,
            brand_popularity: 1.15,
        },
        Brand {
            brand_id: 7,
            brand_name: "Nestle".to_string(),
            brand_tier: "mid".to_string(),
            manufacturer: "Nestle SA".to_string(),
            is_private_label: false,
            brand_popularity: 1.1,
        },
        Brand {
            brand_id: 8,
            brand_name: "Kraft Heinz".to_string(),
            brand_tier: "mid".to_string(),
            manufacturer: "Kraft Heinz Company".to_string(),
            is_private_label: false,
            brand_popularity: 1.3,
        },
        Brand {
            brand_id: 9,
            brand_name: "PepsiCo".to_string(),
            brand_tier: "mid".to_string(),
            manufacturer: "PepsiCo Inc".to_string(),
            is_private_label: false,
            brand_popularity: 1.2,
        },
        Brand {
            brand_id: 10,
            brand_name: "Coca-Cola".to_string(),
            brand_tier: "mid".to_string(),
            manufacturer: "The Coca-Cola Company".to_string(),
            is_private_label: false,
            brand_popularity: 1.25,
        },
        Brand {
            brand_id: 11,
            brand_name: "Unilever".to_string(),
            brand_tier: "premium".to_string(),
            manufacturer: "Unilever PLC".to_string(),
            is_private_label: false,
            brand_popularity: 1.0,
        },
        Brand {
            brand_id: 12,
            brand_name: "Procter & Gamble".to_string(),
            brand_tier: "premium".to_string(),
            manufacturer: "Procter & Gamble Co".to_string(),
            is_private_label: false,
            brand_popularity: 1.05,
        },
        Brand {
            brand_id: 13,
            brand_name: "Campbell Soup".to_string(),
            brand_tier: "mid".to_string(),
            manufacturer: "Campbell Soup Company".to_string(),
            is_private_label: false,
            brand_popularity: 0.9,
        },
        Brand {
            brand_id: 14,
            brand_name: "ConAgra".to_string(),
            brand_tier: "mid".to_string(),
            manufacturer: "Conagra Brands Inc".to_string(),
            is_private_label: false,
            brand_popularity: 0.9,
        },
        Brand {
            brand_id: 15,
            brand_name: "Mondelez".to_string(),
            brand_tier: "mid".to_string(),
            manufacturer: "Mondelez International".to_string(),
            is_private_label: false,
            brand_popularity: 1.1,
        },
        Brand {
            brand_id: 16,
            brand_name: "Mars".to_string(),
            brand_tier: "premium".to_string(),
            manufacturer: "Mars Inc".to_string(),
            is_private_label: false,
            brand_popularity: 1.05,
        },
        Brand {
            brand_id: 17,
            brand_name: "Hershey".to_string(),
            brand_tier: "mid".to_string(),
            manufacturer: "The Hershey Company".to_string(),
            is_private_label: false,
            brand_popularity: 1.0,
        },
        Brand {
            brand_id: 18,
            brand_name: "Frito-Lay".to_string(),
            brand_tier: "mid".to_string(),
            manufacturer: "PepsiCo Inc".to_string(),
            is_private_label: false,
            brand_popularity: 1.35,
        },
        Brand {
            brand_id: 19,
            brand_name: "Quaker".to_string(),
            brand_tier: "mid".to_string(),
            manufacturer: "PepsiCo Inc".to_string(),
            is_private_label: false,
            brand_popularity: 1.0,
        },
        Brand {
            brand_id: 20,
            brand_name: "Dole".to_string(),
            brand_tier: "mid".to_string(),
            manufacturer: "Dole Food Company".to_string(),
            is_private_label: false,
            brand_popularity: 0.95,
        },
        Brand {
            brand_id: 21,
            brand_name: "Del Monte".to_string(),
            brand_tier: "mid".to_string(),
            manufacturer: "Del Monte Foods".to_string(),
            is_private_label: false,
            brand_popularity: 0.9,
        },
        Brand {
            brand_id: 22,
            brand_name: "Tyson Foods".to_string(),
            brand_tier: "mid".to_string(),
            manufacturer: "Tyson Foods Inc".to_string(),
            is_private_label: false,
            brand_popularity: 1.1,
        },
        Brand {
            brand_id: 23,
            brand_name: "Hormel".to_string(),
            brand_tier: "mid".to_string(),
            manufacturer: "Hormel Foods Corp".to_string(),
            is_private_label: false,
            brand_popularity: 0.95,
        },
        Brand {
            brand_id: 24,
            brand_name: "Smithfield".to_string(),
            brand_tier: "value".to_string(),
            manufacturer: "Smithfield Foods".to_string(),
            is_private_label: false,
            brand_popularity: 0.9,
        },
        Brand {
            brand_id: 25,
            brand_name: "Perdue".to_string(),
            brand_tier: "mid".to_string(),
            manufacturer: "Perdue Farms".to_string(),
            is_private_label: false,
            brand_popularity: 0.95,
        },
        Brand {
            brand_id: 26,
            brand_name: "Danone".to_string(),
            brand_tier: "premium".to_string(),
            manufacturer: "Danone SA".to_string(),
            is_private_label: false,
            brand_popularity: 0.85,
        },
        Brand {
            brand_id: 27,
            brand_name: "Chobani".to_string(),
            brand_tier: "premium".to_string(),
            manufacturer: "Chobani LLC".to_string(),
            is_private_label: false,
            brand_popularity: 0.9,
        },
        Brand {
            brand_id: 28,
            brand_name: "Blue Diamond".to_string(),
            brand_tier: "premium".to_string(),
            manufacturer: "Blue Diamond Growers".to_string(),
            is_private_label: false,
            brand_popularity: 0.8,
        },
        Brand {
            brand_id: 29,
            brand_name: "Wonderful".to_string(),
            brand_tier: "premium".to_string(),
            manufacturer: "The Wonderful Company".to_string(),
            is_private_label: false,
            brand_popularity: 0.85,
        },
        Brand {
            brand_id: 30,
            brand_name: "Annies Homegrown".to_string(),
            brand_tier: "premium".to_string(),
            manufacturer: "General Mills Inc".to_string(),
            is_private_label: false,
            brand_popularity: 0.85,
        },
        Brand {
            brand_id: 31,
            brand_name: "Organic Valley".to_string(),
            brand_tier: "premium".to_string(),
            manufacturer: "Organic Valley".to_string(),
            is_private_label: false,
            brand_popularity: 0.8,
        },
        Brand {
            brand_id: 32,
            brand_name: "Horizon Organic".to_string(),
            brand_tier: "premium".to_string(),
            manufacturer: "Danone SA".to_string(),
            is_private_label: false,
            brand_popularity: 0.75,
        },
        Brand {
            brand_id: 33,
            brand_name: "Bobs Red Mill".to_string(),
            brand_tier: "premium".to_string(),
            manufacturer: "Bob's Red Mill".to_string(),
            is_private_label: false,
            brand_popularity: 0.7,
        },
        Brand {
            brand_id: 34,
            brand_name: "Kind".to_string(),
            brand_tier: "premium".to_string(),
            manufacturer: "Mars Inc".to_string(),
            is_private_label: false,
            brand_popularity: 0.85,
        },
        Brand {
            brand_id: 35,
            brand_name: "Clif Bar".to_string(),
            brand_tier: "premium".to_string(),
            manufacturer: "Mondelez International".to_string(),
            is_private_label: false,
            brand_popularity: 0.85,
        },
        Brand {
            brand_id: 36,
            brand_name: "Nature Valley".to_string(),
            brand_tier: "mid".to_string(),
            manufacturer: "General Mills Inc".to_string(),
            is_private_label: false,
            brand_popularity: 1.05,
        },
        Brand {
            brand_id: 37,
            brand_name: "Nabisco".to_string(),
            brand_tier: "mid".to_string(),
            manufacturer: "Mondelez International".to_string(),
            is_private_label: false,
            brand_popularity: 1.15,
        },
        Brand {
            brand_id: 38,
            brand_name: "Ritz".to_string(),
            brand_tier: "mid".to_string(),
            manufacturer: "Mondelez International".to_string(),
            is_private_label: false,
            brand_popularity: 1.1,
        },
        Brand {
            brand_id: 39,
            brand_name: "Pepperidge Farm".to_string(),
            brand_tier: "premium".to_string(),
            manufacturer: "Campbell Soup Company".to_string(),
            is_private_label: false,
            brand_popularity: 0.95,
        },
        Brand {
            brand_id: 40,
            brand_name: "Barilla".to_string(),
            brand_tier: "mid".to_string(),
            manufacturer: "Barilla Group".to_string(),
            is_private_label: false,
            brand_popularity: 1.0,
        },
        Brand {
            brand_id: 41,
            brand_name: "Hunts".to_string(),
            brand_tier: "value".to_string(),
            manufacturer: "Conagra Brands Inc".to_string(),
            is_private_label: false,
            brand_popularity: 0.95,
        },
        Brand {
            brand_id: 42,
            brand_name: "Progresso".to_string(),
            brand_tier: "mid".to_string(),
            manufacturer: "General Mills Inc".to_string(),
            is_private_label: false,
            brand_popularity: 0.9,
        },
        Brand {
            brand_id: 43,
            brand_name: "Swanson".to_string(),
            brand_tier: "value".to_string(),
            manufacturer: "Campbell Soup Company".to_string(),
            is_private_label: false,
            brand_popularity: 0.85,
        },
        Brand {
            brand_id: 44,
            brand_name: "Green Giant".to_string(),
            brand_tier: "mid".to_string(),
            manufacturer: "B&G Foods".to_string(),
            is_private_label: false,
            brand_popularity: 0.95,
        },
        Brand {
            brand_id: 45,
            brand_name: "Birds Eye".to_string(),
            brand_tier: "mid".to_string(),
            manufacturer: "Conagra Brands Inc".to_string(),
            is_private_label: false,
            brand_popularity: 0.9,
        },
        Brand {
            brand_id: 46,
            brand_name: "Lean Cuisine".to_string(),
            brand_tier: "mid".to_string(),
            manufacturer: "Nestle SA".to_string(),
            is_private_label: false,
            brand_popularity: 0.85,
        },
        Brand {
            brand_id: 47,
            brand_name: "Stouffers".to_string(),
            brand_tier: "mid".to_string(),
            manufacturer: "Nestle SA".to_string(),
            is_private_label: false,
            brand_popularity: 0.95,
        },
        Brand {
            brand_id: 48,
            brand_name: "DiGiorno".to_string(),
            brand_tier: "premium".to_string(),
            manufacturer: "Nestle SA".to_string(),
            is_private_label: false,
            brand_popularity: 1.0,
        },
        Brand {
            brand_id: 49,
            brand_name: "Haagen-Dazs".to_string(),
            brand_tier: "premium".to_string(),
            manufacturer: "General Mills Inc".to_string(),
            is_private_label: false,
            brand_popularity: 0.9,
        },
        Brand {
            brand_id: 50,
            brand_name: "Ben & Jerrys".to_string(),
            brand_tier: "premium".to_string(),
            manufacturer: "Unilever PLC".to_string(),
            is_private_label: false,
            brand_popularity: 0.95,
        },
        Brand {
            brand_id: 51,
            brand_name: "Breyers".to_string(),
            brand_tier: "mid".to_string(),
            manufacturer: "Unilever PLC".to_string(),
            is_private_label: false,
            brand_popularity: 1.0,
        },
        Brand {
            brand_id: 52,
            brand_name: "Dreyers".to_string(),
            brand_tier: "mid".to_string(),
            manufacturer: "Nestle SA".to_string(),
            is_private_label: false,
            brand_popularity: 0.95,
        },
        Brand {
            brand_id: 53,
            brand_name: "PolarSprings".to_string(),
            brand_tier: "mid".to_string(),
            manufacturer: "Nestle SA".to_string(),
            is_private_label: false,
            brand_popularity: 1.0,
        },
        Brand {
            brand_id: 54,
            brand_name: "Dasani".to_string(),
            brand_tier: "mid".to_string(),
            manufacturer: "The Coca-Cola Company".to_string(),
            is_private_label: false,
            brand_popularity: 0.95,
        },
        Brand {
            brand_id: 55,
            brand_name: "Smartwater".to_string(),
            brand_tier: "premium".to_string(),
            manufacturer: "The Coca-Cola Company".to_string(),
            is_private_label: false,
            brand_popularity: 0.85,
        },
        Brand {
            brand_id: 56,
            brand_name: "Fiji".to_string(),
            brand_tier: "premium".to_string(),
            manufacturer: "The Wonderful Company".to_string(),
            is_private_label: false,
            brand_popularity: 0.8,
        },
        Brand {
            brand_id: 57,
            brand_name: "Poland Spring".to_string(),
            brand_tier: "value".to_string(),
            manufacturer: "Nestle SA".to_string(),
            is_private_label: false,
            brand_popularity: 1.1,
        },
        Brand {
            brand_id: 58,
            brand_name: "Gatorade".to_string(),
            brand_tier: "mid".to_string(),
            manufacturer: "PepsiCo Inc".to_string(),
            is_private_label: false,
            brand_popularity: 1.15,
        },
        Brand {
            brand_id: 59,
            brand_name: "Powerade".to_string(),
            brand_tier: "mid".to_string(),
            manufacturer: "The Coca-Cola Company".to_string(),
            is_private_label: false,
            brand_popularity: 0.95,
        },
        Brand {
            brand_id: 60,
            brand_name: "Tropicana".to_string(),
            brand_tier: "premium".to_string(),
            manufacturer: "PepsiCo Inc".to_string(),
            is_private_label: false,
            brand_popularity: 1.05,
        },
        Brand {
            brand_id: 61,
            brand_name: "Simply".to_string(),
            brand_tier: "premium".to_string(),
            manufacturer: "The Coca-Cola Company".to_string(),
            is_private_label: false,
            brand_popularity: 0.95,
        },
        Brand {
            brand_id: 62,
            brand_name: "Minute Maid".to_string(),
            brand_tier: "mid".to_string(),
            manufacturer: "The Coca-Cola Company".to_string(),
            is_private_label: false,
            brand_popularity: 1.0,
        },
        Brand {
            brand_id: 63,
            brand_name: "Ocean Spray".to_string(),
            brand_tier: "mid".to_string(),
            manufacturer: "Ocean Spray Cranberries".to_string(),
            is_private_label: false,
            brand_popularity: 0.9,
        },
    ]
}

/// Initialize suppliers reference data
pub fn init_suppliers() -> Vec<Supplier> {
    vec![
        Supplier {
            supplier_id: 1,
            supplier_name: "Kellogg Company Supplier".to_string(),
            supplier_type: "manufacturer".to_string(),
            lead_time_days: 5,
            reliability_score: 0.95,
            payment_terms: "Net 30".to_string(),
        },
        Supplier {
            supplier_id: 2,
            supplier_name: "General Mills Inc Supplier".to_string(),
            supplier_type: "manufacturer".to_string(),
            lead_time_days: 5,
            reliability_score: 0.96,
            payment_terms: "Net 30".to_string(),
        },
        Supplier {
            supplier_id: 3,
            supplier_name: "Nestle SA Supplier".to_string(),
            supplier_type: "manufacturer".to_string(),
            lead_time_days: 7,
            reliability_score: 0.94,
            payment_terms: "Net 45".to_string(),
        },
        Supplier {
            supplier_id: 4,
            supplier_name: "Kraft Heinz Company Supplier".to_string(),
            supplier_type: "manufacturer".to_string(),
            lead_time_days: 6,
            reliability_score: 0.93,
            payment_terms: "Net 30".to_string(),
        },
        Supplier {
            supplier_id: 5,
            supplier_name: "PepsiCo Inc Supplier".to_string(),
            supplier_type: "manufacturer".to_string(),
            lead_time_days: 4,
            reliability_score: 0.97,
            payment_terms: "Net 30".to_string(),
        },
        Supplier {
            supplier_id: 6,
            supplier_name: "The Coca-Cola Company Supplier".to_string(),
            supplier_type: "manufacturer".to_string(),
            lead_time_days: 4,
            reliability_score: 0.98,
            payment_terms: "Net 30".to_string(),
        },
        Supplier {
            supplier_id: 7,
            supplier_name: "Unilever PLC Supplier".to_string(),
            supplier_type: "manufacturer".to_string(),
            lead_time_days: 8,
            reliability_score: 0.92,
            payment_terms: "Net 45".to_string(),
        },
        Supplier {
            supplier_id: 8,
            supplier_name: "Procter & Gamble Co Supplier".to_string(),
            supplier_type: "manufacturer".to_string(),
            lead_time_days: 7,
            reliability_score: 0.94,
            payment_terms: "Net 45".to_string(),
        },
        Supplier {
            supplier_id: 9,
            supplier_name: "Campbell Soup Company Supplier".to_string(),
            supplier_type: "manufacturer".to_string(),
            lead_time_days: 6,
            reliability_score: 0.91,
            payment_terms: "Net 30".to_string(),
        },
        Supplier {
            supplier_id: 10,
            supplier_name: "Conagra Brands Inc Supplier".to_string(),
            supplier_type: "manufacturer".to_string(),
            lead_time_days: 6,
            reliability_score: 0.90,
            payment_terms: "Net 30".to_string(),
        },
        Supplier {
            supplier_id: 11,
            supplier_name: "Mondelez International Supplier".to_string(),
            supplier_type: "manufacturer".to_string(),
            lead_time_days: 7,
            reliability_score: 0.93,
            payment_terms: "Net 45".to_string(),
        },
        Supplier {
            supplier_id: 12,
            supplier_name: "Mars Inc Supplier".to_string(),
            supplier_type: "manufacturer".to_string(),
            lead_time_days: 8,
            reliability_score: 0.91,
            payment_terms: "Net 45".to_string(),
        },
        Supplier {
            supplier_id: 13,
            supplier_name: "The Hershey Company Supplier".to_string(),
            supplier_type: "manufacturer".to_string(),
            lead_time_days: 5,
            reliability_score: 0.95,
            payment_terms: "Net 30".to_string(),
        },
        Supplier {
            supplier_id: 14,
            supplier_name: "Tyson Foods Inc Supplier".to_string(),
            supplier_type: "manufacturer".to_string(),
            lead_time_days: 3,
            reliability_score: 0.89,
            payment_terms: "Net 15".to_string(),
        },
        Supplier {
            supplier_id: 15,
            supplier_name: "Hormel Foods Corp Supplier".to_string(),
            supplier_type: "manufacturer".to_string(),
            lead_time_days: 4,
            reliability_score: 0.90,
            payment_terms: "Net 15".to_string(),
        },
        Supplier {
            supplier_id: 16,
            supplier_name: "Smithfield Foods Supplier".to_string(),
            supplier_type: "manufacturer".to_string(),
            lead_time_days: 3,
            reliability_score: 0.88,
            payment_terms: "Net 15".to_string(),
        },
        Supplier {
            supplier_id: 17,
            supplier_name: "Perdue Farms Supplier".to_string(),
            supplier_type: "manufacturer".to_string(),
            lead_time_days: 3,
            reliability_score: 0.89,
            payment_terms: "Net 15".to_string(),
        },
        Supplier {
            supplier_id: 18,
            supplier_name: "Danone SA Supplier".to_string(),
            supplier_type: "manufacturer".to_string(),
            lead_time_days: 4,
            reliability_score: 0.92,
            payment_terms: "Net 21".to_string(),
        },
        Supplier {
            supplier_id: 19,
            supplier_name: "Chobani LLC Supplier".to_string(),
            supplier_type: "manufacturer".to_string(),
            lead_time_days: 3,
            reliability_score: 0.94,
            payment_terms: "Net 21".to_string(),
        },
        Supplier {
            supplier_id: 20,
            supplier_name: "Blue Diamond Growers Supplier".to_string(),
            supplier_type: "manufacturer".to_string(),
            lead_time_days: 6,
            reliability_score: 0.91,
            payment_terms: "Net 30".to_string(),
        },
        Supplier {

            supplier_id: 21,
            supplier_name: "The Wonderful Company Supplier".to_string(),
            supplier_type: "manufacturer".to_string(),
            lead_time_days: 5,
            reliability_score: 0.93,
            payment_terms: "Net 30".to_string(),
        },
        Supplier {
            supplier_id: 22,
            supplier_name: "Organic Valley Supplier".to_string(),
            supplier_type: "manufacturer".to_string(),
            lead_time_days: 4,
            reliability_score: 0.90,
            payment_terms: "Net 21".to_string(),
        },
        Supplier {
            supplier_id: 23,
            supplier_name: "Bob's Red Mill Supplier".to_string(),
            supplier_type: "manufacturer".to_string(),
            lead_time_days: 7,
            reliability_score: 0.89,
            payment_terms: "Net 30".to_string(),
        },
        Supplier {
            supplier_id: 24,
            supplier_name: "Barilla Group Supplier".to_string(),
            supplier_type: "manufacturer".to_string(),
            lead_time_days: 10,
            reliability_score: 0.87,
            payment_terms: "Net 45".to_string(),
        },
        Supplier {
            supplier_id: 25,
            supplier_name: "B&G Foods Supplier".to_string(),
            supplier_type: "manufacturer".to_string(),
            lead_time_days: 8,
            reliability_score: 0.88,
            payment_terms: "Net 30".to_string(),
        },
        Supplier {
            supplier_id: 26,
            supplier_name: "Ocean Spray Cranberries Supplier".to_string(),
            supplier_type: "manufacturer".to_string(),
            lead_time_days: 5,
            reliability_score: 0.92,
            payment_terms: "Net 30".to_string(),
        },
        Supplier {
            supplier_id: 27,
            supplier_name: "ShelfWise Private Label Supplier".to_string(),
            supplier_type: "private_label".to_string(),
            lead_time_days: 6,
            reliability_score: 0.94,
            payment_terms: "Net 30".to_string(),
        },
        Supplier {
            supplier_id: 28,
            supplier_name: "Regional Produce Distributor".to_string(),
            supplier_type: "distributor".to_string(),
            lead_time_days: 2,
            reliability_score: 0.85,
            payment_terms: "Net 7".to_string(),
        },
        Supplier {
            supplier_id: 29,
            supplier_name: "Regional Dairy Distributor".to_string(),
            supplier_type: "distributor".to_string(),
            lead_time_days: 2,
            reliability_score: 0.87,
            payment_terms: "Net 7".to_string(),
        },
        Supplier {
            supplier_id: 30,
            supplier_name: "Regional Meat Distributor".to_string(),
            supplier_type: "distributor".to_string(),
            lead_time_days: 1,
            reliability_score: 0.86,
            payment_terms: "Net 7".to_string(),
        },
    ]
}

/// Initialize payment methods reference data
pub fn init_payment_methods() -> Vec<PaymentMethod> {
    vec![
        PaymentMethod {
            payment_method_id: 1,
            payment_method_code: "credit".to_string(),
            payment_method_name: "Credit Card".to_string(),
            processing_fee_pct: 2.500,
            is_active: true,
        },
        PaymentMethod {
            payment_method_id: 2,
            payment_method_code: "debit".to_string(),
            payment_method_name: "Debit Card".to_string(),
            processing_fee_pct: 1.500,
            is_active: true,
        },
        PaymentMethod {
            payment_method_id: 3,
            payment_method_code: "cash".to_string(),
            payment_method_name: "Cash".to_string(),
            processing_fee_pct: 0.000,
            is_active: true,
        },
        PaymentMethod {
            payment_method_id: 4,
            payment_method_code: "mobile_pay".to_string(),
            payment_method_name: "Mobile Payment".to_string(),
            processing_fee_pct: 2.200,
            is_active: true,
        },
        PaymentMethod {
            payment_method_id: 5,
            payment_method_code: "gift_card".to_string(),
            payment_method_name: "Gift Card".to_string(),
            processing_fee_pct: 0.000,
            is_active: true,
        },
        PaymentMethod {
            payment_method_id: 6,
            payment_method_code: "ebt".to_string(),
            payment_method_name: "EBT/SNAP".to_string(),
            processing_fee_pct: 0.500,
            is_active: true,
        },
        PaymentMethod {
            payment_method_id: 7,
            payment_method_code: "check".to_string(),
            payment_method_name: "Check".to_string(),
            processing_fee_pct: 0.750,
            is_active: false,
        },
        PaymentMethod {
            payment_method_id: 8,
            payment_method_code: "crypto".to_string(),
            payment_method_name: "Cryptocurrency".to_string(),
            processing_fee_pct: 1.000,
            is_active: false,
        },
    ]
}

/// Initialize promotion types reference data
pub fn init_promotion_types() -> Vec<PromotionType> {
    vec![
        PromotionType {
            promo_type_id: 1,
            promo_type_code: "price_cut".to_string(),
            promo_type_name: "Price Reduction".to_string(),
            typical_discount_pct: 20,
            typical_duration_days: 14,
        },
        PromotionType {
            promo_type_id: 2,
            promo_type_code: "bogo".to_string(),
            promo_type_name: "Buy One Get One".to_string(),
            typical_discount_pct: 50,
            typical_duration_days: 7,
        },
        PromotionType {
            promo_type_id: 3,
            promo_type_code: "bundle".to_string(),
            promo_type_name: "Bundle Deal".to_string(),
            typical_discount_pct: 15,
            typical_duration_days: 14,
        },
        PromotionType {
            promo_type_id: 4,
            promo_type_code: "loyalty".to_string(),
            promo_type_name: "Loyalty Member Exclusive".to_string(),
            typical_discount_pct: 10,
            typical_duration_days: 30,
        },
        PromotionType {
            promo_type_id: 5,
            promo_type_code: "clearance".to_string(),
            promo_type_name: "Clearance Sale".to_string(),
            typical_discount_pct: 40,
            typical_duration_days: 30,
        },
        PromotionType {
            promo_type_id: 6,
            promo_type_code: "seasonal".to_string(),
            promo_type_name: "Seasonal Promotion".to_string(),
            typical_discount_pct: 25,
            typical_duration_days: 21,
        },
        PromotionType {
            promo_type_id: 7,
            promo_type_code: "flash_sale".to_string(),
            promo_type_name: "Flash Sale".to_string(),
            typical_discount_pct: 30,
            typical_duration_days: 3,
        },
        PromotionType {
            promo_type_id: 8,
            promo_type_code: "new_product".to_string(),
            promo_type_name: "New Product Introduction".to_string(),
            typical_discount_pct: 15,
            typical_duration_days: 14,
        },
    ]
}

/// Initialize return reasons reference data
pub fn init_return_reasons() -> Vec<ReturnReason> {
    vec![
        ReturnReason {
            return_reason_id: 1,
            return_reason_code: "defective".to_string(),
            return_reason_name: "Defective Product".to_string(),
            is_quality_issue: true,
            is_preventable: true,
        },
        ReturnReason {
            return_reason_id: 2,
            return_reason_code: "wrong_item".to_string(),
            return_reason_name: "Wrong Item Received".to_string(),
            is_quality_issue: false,
            is_preventable: true,
        },
        ReturnReason {
            return_reason_id: 3,
            return_reason_code: "expired".to_string(),
            return_reason_name: "Expired Product".to_string(),
            is_quality_issue: true,
            is_preventable: true,
        },
        ReturnReason {
            return_reason_id: 4,
            return_reason_code: "damaged".to_string(),
            return_reason_name: "Damaged in Transit".to_string(),
            is_quality_issue: true,
            is_preventable: true,
        },
        ReturnReason {
            return_reason_id: 5,
            return_reason_code: "changed_mind".to_string(),
            return_reason_name: "Customer Changed Mind".to_string(),
            is_quality_issue: false,
            is_preventable: false,
        },
        ReturnReason {
            return_reason_id: 6,
            return_reason_code: "not_as_described".to_string(),
            return_reason_name: "Not As Described".to_string(),
            is_quality_issue: false,
            is_preventable: true,
        },
        ReturnReason {
            return_reason_id: 7,
            return_reason_code: "allergic_reaction".to_string(),
            return_reason_name: "Allergic Reaction".to_string(),
            is_quality_issue: false,
            is_preventable: false,
        },
        ReturnReason {
            return_reason_id: 8,
            return_reason_code: "duplicate_purchase".to_string(),
            return_reason_name: "Duplicate Purchase".to_string(),
            is_quality_issue: false,
            is_preventable: false,
        },
        ReturnReason {
            return_reason_id: 9,
            return_reason_code: "gift_return".to_string(),
            return_reason_name: "Gift Return".to_string(),
            is_quality_issue: false,
            is_preventable: false,
        },
        ReturnReason {
            return_reason_id: 10,
            return_reason_code: "price_match".to_string(),
            return_reason_name: "Price Match Request".to_string(),
            is_quality_issue: false,
            is_preventable: false,
        },
    ]
}

/// Initialize waste reasons reference data
pub fn init_waste_reasons() -> Vec<WasteReason> {
    vec![
        WasteReason {
            waste_reason_id: 1,
            waste_reason_code: "expired".to_string(),
            waste_reason_name: "Expired/Past Sell-By Date".to_string(),
            is_preventable: true,
        },
        WasteReason {
            waste_reason_id: 2,
            waste_reason_code: "damaged".to_string(),
            waste_reason_name: "Damaged Product".to_string(),
            is_preventable: true,
        },
        WasteReason {
            waste_reason_id: 3,
            waste_reason_code: "recalled".to_string(),
            waste_reason_name: "Product Recall".to_string(),
            is_preventable: false,
        },
        WasteReason {
            waste_reason_id: 4,
            waste_reason_code: "overstocked".to_string(),
            waste_reason_name: "Overstocked/Slow Moving".to_string(),
            is_preventable: true,
        },
        WasteReason {
            waste_reason_id: 5,
            waste_reason_code: "display_damage".to_string(),
            waste_reason_name: "Display/Shelf Damage".to_string(),
            is_preventable: true,
        },
        WasteReason {
            waste_reason_id: 6,
            waste_reason_code: "temperature_abuse".to_string(),
            waste_reason_name: "Temperature Abuse".to_string(),
            is_preventable: true,
        },
        WasteReason {
            waste_reason_id: 7,
            waste_reason_code: "pest_contamination".to_string(),
            waste_reason_name: "Pest Contamination".to_string(),
            is_preventable: true,
        },
        WasteReason {
            waste_reason_id: 8,
            waste_reason_code: "customer_damage".to_string(),
            waste_reason_name: "Customer Damaged".to_string(),
            is_preventable: false,
        },
    ]
}

use anyhow::Result;
use csv::Writer;
use std::path::Path;

/// Write all reference data CSVs to the specified output directory
pub fn write_reference_data_csvs(output_dir: &str) -> Result<()> {
    std::fs::create_dir_all(output_dir)?;

    write_regions_csv(output_dir)?;
    write_categories_csv(output_dir)?;
    write_store_types_csv(output_dir)?;
    write_brands_csv(output_dir)?;
    write_suppliers_csv(output_dir)?;
    write_payment_methods_csv(output_dir)?;
    write_promotion_types_csv(output_dir)?;
    write_return_reasons_csv(output_dir)?;
    write_waste_reasons_csv(output_dir)?;

    println!("✓ Reference data CSVs written to {}", output_dir);
    Ok(())
}

fn write_regions_csv(output_dir: &str) -> Result<()> {
    let mut writer = Writer::from_path(Path::new(output_dir).join("regions.csv"))?;

    for region in init_regions() {
        writer.serialize(region)?;
    }
    writer.flush()?;
    Ok(())
}

fn write_categories_csv(output_dir: &str) -> Result<()> {
    let mut writer = Writer::from_path(Path::new(output_dir).join("categories.csv"))?;

    for category in init_categories() {
        writer.serialize(category)?;
    }
    writer.flush()?;
    Ok(())
}

fn write_store_types_csv(output_dir: &str) -> Result<()> {
    let mut writer = Writer::from_path(Path::new(output_dir).join("store_types.csv"))?;

    for store_type in init_store_types() {
        writer.serialize(store_type)?;
    }
    writer.flush()?;
    Ok(())
}

fn write_brands_csv(output_dir: &str) -> Result<()> {
    let mut writer = Writer::from_path(Path::new(output_dir).join("brands.csv"))?;

    for brand in init_brands_reference() {
        writer.serialize(brand)?;
    }
    writer.flush()?;
    Ok(())
}

fn write_suppliers_csv(output_dir: &str) -> Result<()> {
    let mut writer = Writer::from_path(Path::new(output_dir).join("suppliers.csv"))?;

    for supplier in init_suppliers() {
        writer.serialize(supplier)?;
    }
    writer.flush()?;
    Ok(())
}

fn write_payment_methods_csv(output_dir: &str) -> Result<()> {
    let mut writer = Writer::from_path(Path::new(output_dir).join("payment_methods.csv"))?;

    for payment_method in init_payment_methods() {
        writer.serialize(payment_method)?;
    }
    writer.flush()?;
    Ok(())
}

fn write_promotion_types_csv(output_dir: &str) -> Result<()> {
    let mut writer = Writer::from_path(Path::new(output_dir).join("promotion_types.csv"))?;

    for promo_type in init_promotion_types() {
        writer.serialize(promo_type)?;
    }
    writer.flush()?;
    Ok(())
}

fn write_return_reasons_csv(output_dir: &str) -> Result<()> {
    let mut writer = Writer::from_path(Path::new(output_dir).join("return_reasons.csv"))?;

    for return_reason in init_return_reasons() {
        writer.serialize(return_reason)?;
    }
    writer.flush()?;
    Ok(())
}

fn write_waste_reasons_csv(output_dir: &str) -> Result<()> {
    let mut writer = Writer::from_path(Path::new(output_dir).join("waste_reasons.csv"))?;

    for waste_reason in init_waste_reasons() {
        writer.serialize(waste_reason)?;
    }
    writer.flush()?;
    Ok(())
}
