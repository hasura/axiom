use crate::models::Product;
use chrono::{NaiveDate, Datelike};
use rand::Rng;

/// Calculate reorder point based on demand history and lead time
/// Scaled for realistic grocery basket sizes (actual sales are ~4x demand estimate)
pub fn calculate_reorder_point(
    demand_history: &[u32],
    lead_time_days: f64,
    current_demand: u32,
) -> u32 {
    // Basket size multiplier: actual sales are ~4x demand-based estimates
    let basket_multiplier = 4.0;

    let avg_daily_demand = if !demand_history.is_empty() {
        demand_history.iter().sum::<u32>() as f64 / demand_history.len() as f64
    } else {
        current_demand as f64
    };

    // Scale demand for basket size effect
    let adjusted_demand = avg_daily_demand * basket_multiplier;

    // Calculate demand variability (standard deviation)
    let demand_std_dev = if demand_history.len() > 1 {
        let mean = avg_daily_demand;
        let variance = demand_history.iter()
            .map(|&d| {
                let diff = d as f64 - mean;
                diff * diff
            })
            .sum::<f64>() / (demand_history.len() - 1) as f64;
        variance.sqrt() * basket_multiplier
    } else {
        adjusted_demand * 0.3 // Assume 30% variability initially
    };

    // Calculate safety stock (Z-score * std_dev * sqrt(lead_time))
    // Using Z=2.05 for 98% service level (reduced from 95% to lower stockouts)
    let safety_stock = (2.05 * demand_std_dev * lead_time_days.sqrt()).ceil() as u32;

    // Reorder point = (avg demand * lead time) + safety stock
    // Add extra buffer (1.5x) to trigger reorders earlier
    (((adjusted_demand * lead_time_days).ceil() as u32) + safety_stock) * 3 / 2
}

/// Calculate order quantity based on product category and demand
/// Scaled for realistic grocery basket sizes and replenishment cycles
pub fn calculate_order_quantity<R: Rng>(
    product: &Product,
    avg_daily_demand: f64,
    rng: &mut R,
) -> u32 {
    // Scale demand estimate by basket multiplier (actual sales are ~4x demand estimate with weighted selection)
    let adjusted_demand = avg_daily_demand * 4.0;

    let base_quantity = match product.category.as_str() {
        // Perishables: order frequently, larger quantities (5-7 days worth)
        "dairy" | "produce" | "meat" | "bakery" => {
            (adjusted_demand * rng.gen_range(5.0..7.0)).ceil() as u32
        },
        // Fast movers: order 10-18 days worth
        "beverages" | "snacks" | "candy" => {
            (adjusted_demand * rng.gen_range(10.0..18.0)).ceil() as u32
        },
        // Medium movers: order 14-28 days worth
        "cereal" | "canned" | "frozen" => {
            (adjusted_demand * rng.gen_range(14.0..28.0)).ceil() as u32
        },
        // Slow movers: order 21-42 days worth
        _ => {
            (adjusted_demand * rng.gen_range(21.0..42.0)).ceil() as u32
        }
    };

    base_quantity.max(20) // Minimum order of 20 units
}

/// Calculate initial inventory based on lead time and expected demand
/// Scaled for realistic grocery basket sizes (12-18 items avg)
pub fn calculate_initial_inventory<R: Rng>(
    product: &Product,
    demand: u32,
    lead_time_days: u32,
    rng: &mut R,
) -> u32 {
    // Review period (how often we check inventory)
    let review_period = match product.category.as_str() {
        "dairy" | "produce" | "meat" | "bakery" => 1, // Daily review
        "beverages" | "snacks" => 2, // Every 2 days
        _ => 3, // Every 3 days
    };

    // Safety stock days - scaled up for weighted selection where popular products
    // get selected disproportionately often. Need larger buffer to handle demand spikes.
    // Real grocery stores carry 2-4 weeks of inventory for most items
    let safety_stock_days = match product.category.as_str() {
        "dairy" | "produce" | "meat" | "bakery" => 10,  // 10 days for perishables
        "beverages" | "snacks" => 18, // 18 days for fast movers
        _ => 21, // 21 days for shelf-stable
    };

    // Basket size multiplier: with weighted selection, popular products appear
    // in ~4-5x more baskets than demand estimate suggests
    // Target: 5-10% stockout rate (realistic for well-managed grocery)
    let basket_multiplier = 5.0;

    // Initial stock = (lead time + review period + safety stock) * expected demand * basket factor
    // Use at least 1 unit of demand to avoid zero initialization
    let effective_demand = demand.max(1);
    let base_stock = effective_demand * (lead_time_days + review_period + safety_stock_days);
    let initial_stock = (base_stock as f64 * basket_multiplier) as u32;

    // Add some randomness (90-110%) and ensure minimum stock
    let final_stock = (initial_stock as f64 * rng.gen_range(0.9..1.1)) as u32;

    // Minimum stock ensures all products start with some inventory
    // With weighted selection, popular products have higher demand-based initial stock
    // so minimum mainly affects low-demand "long tail" products
    let min_stock = match product.category.as_str() {
        "dairy" | "produce" | "meat" | "bakery" => 30,  // Perishables - lower min
        "beverages" | "snacks" => 50, // Fast movers
        _ => 40, // Shelf-stable
    };

    final_stock.max(min_stock)
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