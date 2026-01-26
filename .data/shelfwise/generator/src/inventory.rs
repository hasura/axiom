use crate::models::Product;
use chrono::{NaiveDate, Datelike};
use rand::Rng;

/// Calculate reorder point based on demand history and lead time
/// Uses actual sales data when available, but never below bootstrap estimate
/// popularity_factor = product.pareto_weight * product.brand_popularity
pub fn calculate_reorder_point(
    demand_history: &[u32],
    lead_time_days: f64,
    current_demand: u32,
    popularity_factor: f64,
) -> u32 {
    // Bootstrap multiplier based on product popularity
    // Tuned to achieve stable 2-3% stockout rate (industry standard for grocery)
    // Lower multipliers allow natural stockout rate to emerge
    let bootstrap_multiplier = if popularity_factor > 1.5 {
        5.0  // Very popular products
    } else if popularity_factor > 1.0 {
        4.5  // Popular products
    } else if popularity_factor > 0.5 {
        4.0  // Average products
    } else {
        3.5  // Low popularity
    };
    let bootstrap_avg = current_demand as f64 * bootstrap_multiplier;

    // When we have history, use the MAXIMUM of:
    // 1. Actual sales average from history
    // 2. Bootstrap estimate
    // This prevents under-ordering when history is polluted with constrained sales
    let (avg_daily_sales, demand_std_dev) = if !demand_history.is_empty() {
        let history_avg = demand_history.iter().sum::<u32>() as f64 / demand_history.len() as f64;
        // Use the higher of history average or bootstrap estimate
        let avg = history_avg.max(bootstrap_avg);
        let std_dev = if demand_history.len() > 1 {
            let variance = demand_history.iter()
                .map(|&d| {
                    let diff = d as f64 - avg;
                    diff * diff
                })
                .sum::<f64>() / (demand_history.len() - 1) as f64;
            variance.sqrt()
        } else {
            avg * 0.30 // Assume 30% variability initially
        };
        (avg, std_dev)
    } else {
        // No history: use bootstrap estimate
        (bootstrap_avg, bootstrap_avg * 0.30)
    };

    // Calculate safety stock (Z-score * std_dev * sqrt(lead_time))
    // Using Z=1.65 for 95% service level (targets ~2-5% stockout rate)
    let safety_stock = (1.65 * demand_std_dev * lead_time_days.sqrt()).ceil() as u32;

    // Reorder point = (avg daily sales * lead time) + safety stock
    // Buffer of 1.5x provides cushion to cap stockouts around 5%
    (((avg_daily_sales * lead_time_days).ceil() as u32) + safety_stock) * 3 / 2
}

/// Calculate order quantity based on product category and actual sales
/// avg_daily_sales should be from demand_history (actual sales), not demand estimates
pub fn calculate_order_quantity<R: Rng>(
    product: &Product,
    avg_daily_sales: f64,
    rng: &mut R,
) -> u32 {
    // avg_daily_sales is actual sales from history - use directly, no multiplier needed
    // Order enough to cover the replenishment cycle plus safety buffer
    let base_quantity = match product.category.as_str() {
        // Perishables: order frequently, 7-10 days worth (accounts for lead time + buffer)
        "dairy" | "produce" | "meat" | "bakery" => {
            (avg_daily_sales * rng.gen_range(7.0..10.0)).ceil() as u32
        },
        // Fast movers: order 14-21 days worth
        "beverages" | "snacks" | "candy" => {
            (avg_daily_sales * rng.gen_range(14.0..21.0)).ceil() as u32
        },
        // Medium movers: order 21-28 days worth
        "cereal" | "canned" | "frozen" => {
            (avg_daily_sales * rng.gen_range(21.0..28.0)).ceil() as u32
        },
        // Slow movers: order 28-42 days worth
        _ => {
            (avg_daily_sales * rng.gen_range(28.0..42.0)).ceil() as u32
        }
    };

    // Minimum order of one case - allows natural stockout dynamics
    base_quantity.max(24)
}

/// Calculate initial inventory based on lead time and expected demand
/// Tuned to achieve 2-3% stockout rate from the start (industry standard)
pub fn calculate_initial_inventory<R: Rng>(
    product: &Product,
    demand: u32,
    lead_time_days: u32,
    rng: &mut R,
) -> u32 {
    // Review period (how often we check inventory)
    let review_period = match product.category.as_str() {
        "dairy" | "produce" | "meat" | "bakery" => 1,
        "beverages" | "snacks" => 2,
        _ => 3,
    };

    // Safety stock days - reduced to allow natural 2-3% stockout rate
    let safety_stock_days = match product.category.as_str() {
        "dairy" | "produce" | "meat" | "bakery" => 3,  // Perishables
        "beverages" | "snacks" => 5,  // Fast movers
        _ => 7,  // Shelf-stable
    };

    // Basket multiplier - matches reorder logic (3.5-5x range)
    let basket_multiplier = 4.0;

    // Initial stock = (lead time + review period + safety stock) * demand * basket factor
    let effective_demand = demand.max(1);
    let base_stock = effective_demand * (lead_time_days + review_period + safety_stock_days);
    let initial_stock = (base_stock as f64 * basket_multiplier) as u32;

    // Add randomness (85-115%) - wider range creates natural variance in stockout timing
    let final_stock = (initial_stock as f64 * rng.gen_range(0.85..1.15)) as u32;

    // Lower minimums to allow stockouts on slow movers
    let min_stock = match product.category.as_str() {
        "dairy" | "produce" | "meat" | "bakery" => 15,
        "beverages" | "snacks" => 20,
        _ => 18,
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