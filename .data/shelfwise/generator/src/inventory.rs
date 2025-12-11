use crate::models::Product;
use chrono::{NaiveDate, Datelike};
use rand::rngs::StdRng;
use rand::Rng;

/// Calculate reorder point based on demand history and lead time
pub fn calculate_reorder_point(
    demand_history: &[u32],
    lead_time_days: f64,
    current_demand: u32,
) -> u32 {
    let avg_daily_demand = if !demand_history.is_empty() {
        demand_history.iter().sum::<u32>() as f64 / demand_history.len() as f64
    } else {
        current_demand as f64
    };
    
    // Calculate demand variability (standard deviation)
    let demand_std_dev = if demand_history.len() > 1 {
        let mean = avg_daily_demand;
        let variance = demand_history.iter()
            .map(|&d| {
                let diff = d as f64 - mean;
                diff * diff
            })
            .sum::<f64>() / (demand_history.len() - 1) as f64;
        variance.sqrt()
    } else {
        avg_daily_demand * 0.3 // Assume 30% variability initially
    };
    
    // Calculate safety stock (Z-score * std_dev * sqrt(lead_time))
    // Using Z=1.65 for 95% service level
    let safety_stock = (1.65 * demand_std_dev * lead_time_days.sqrt()).ceil() as u32;
    
    // Reorder point = (avg demand * lead time) + safety stock
    ((avg_daily_demand * lead_time_days).ceil() as u32) + safety_stock
}

/// Calculate order quantity based on product category and demand
pub fn calculate_order_quantity(
    product: &Product,
    avg_daily_demand: f64,
    rng: &mut StdRng,
) -> u32 {
    let base_quantity = match product.category.as_str() {
        // Perishables: order frequently, smaller quantities (2-4 days worth)
        "dairy" | "produce" | "meat" | "bakery" => {
            (avg_daily_demand * rng.gen_range(2.0..4.0)).ceil() as u32
        },
        // Fast movers: order 7-14 days worth
        "beverages" | "snacks" | "candy" => {
            (avg_daily_demand * rng.gen_range(7.0..14.0)).ceil() as u32
        },
        // Medium movers: order 10-21 days worth
        "cereal" | "canned" | "frozen" => {
            (avg_daily_demand * rng.gen_range(10.0..21.0)).ceil() as u32
        },
        // Slow movers: order 14-30 days worth
        _ => {
            (avg_daily_demand * rng.gen_range(14.0..30.0)).ceil() as u32
        }
    };
    
    base_quantity.max(5) // Minimum order of 5 units
}

/// Calculate initial inventory based on lead time and expected demand
pub fn calculate_initial_inventory(
    product: &Product,
    demand: u32,
    lead_time_days: u32,
    rng: &mut StdRng,
) -> u32 {
    // Review period (how often we check inventory)
    let review_period = match product.category.as_str() {
        "dairy" | "produce" | "meat" | "bakery" => 1, // Daily review
        "beverages" | "snacks" => 2, // Every 2 days
        _ => 3, // Every 3 days
    };
    
    // Safety stock days
    let safety_stock_days = match product.category.as_str() {
        "dairy" | "produce" | "meat" | "bakery" => 2, // 2 days safety for perishables
        _ => 5, // 5 days safety for shelf-stable
    };
    
    // Initial stock = (lead time + review period + safety stock) * expected demand
    let initial_stock = demand * (lead_time_days + review_period + safety_stock_days);
    
    // Add some randomness (90-110%)
    (initial_stock as f64 * rng.gen_range(0.9..1.1)) as u32
}

/// Check if seasonal inventory buildup is needed
pub fn needs_seasonal_buildup(
    date: &NaiveDate,
    product: &Product,
) -> f64 {
    let month = date.month();
    
    match product.category.as_str() {
        // Holiday season buildup for candy, snacks, beverages
        "candy" | "snacks" | "beverages" if month >= 11 => 1.5, // 50% more inventory
        
        // Summer buildup for beverages, frozen
        "beverages" | "frozen" if (6..=8).contains(&month) => 1.3, // 30% more
        
        // Back to school for snacks, cereal
        "snacks" | "cereal" if month == 8 => 1.2, // 20% more
        
        _ => 1.0, // No seasonal adjustment
    }
}