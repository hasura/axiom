use chrono::{NaiveDate, NaiveDateTime};
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Product {
    pub product_id: u32,
    pub sku: String,
    pub brand: String,
    pub category: String,
    pub sub_category: String,
    pub size: String,
    pub unit_of_measure: String,
    pub list_price: f64,
    pub cost: f64,
    pub launch_date: NaiveDate,
    pub discontinue_date: Option<NaiveDate>,
    pub brand_popularity: f64,
    pub tier: String,
    pub pareto_weight: f64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Store {
    pub store_id: u32,
    pub region: String,
    pub store_type: String,
    pub sq_ft: u32,
    pub opened_date: NaiveDate,
    pub climate_zone: String,
    pub city: String,
    pub latitude: f64,
    pub longitude: f64,
}

#[derive(Debug, Clone)]
pub struct StoreEconomics {
    // Cost structure multipliers (for future operational cost modeling)
    #[allow(dead_code)]
    pub labor_cost_index: f64,        // 0.85-1.35 (midwest=0.85, SF/NYC=1.35)
    #[allow(dead_code)]
    pub rent_cost_index: f64,          // 0.80-1.50 (rural=0.80, urban=1.50)
    #[allow(dead_code)]
    pub utility_cost_index: f64,       // 0.90-1.20 (climate-based)
    
    // Operational efficiency
    pub maturity_factor: f64,          // 0.92-1.15 (new=1.15 costs, mature=0.92)
    pub shrinkage_rate: f64,           // 0.01-0.04 (varies by type/location)
    #[allow(dead_code)]
    pub labor_efficiency: f64,         // 0.90-1.10 (affects operating costs)
    
    // Market dynamics
    pub competitive_intensity: f64,    // 0.90-1.10 (affects pricing power)
    pub price_premium_index: f64,      // 0.95-1.15 (urban/convenience higher)
    pub volume_discount_tier: f64,     // 0.92-1.00 (big stores get better COGS)
    
    // Performance
    pub store_performance_tier: String, // "high", "medium", "low"
    #[allow(dead_code)]
    pub market_share_estimate: f64,     // 0.05-0.25 (affects volume)
    
    // Category mix adjustments
    pub category_mix_factors: std::collections::HashMap<String, f64>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Calendar {
    pub date: NaiveDate,
    pub dow: u32,
    pub is_weekend: bool,
    pub is_holiday_us: bool,
    pub is_holiday_canada: bool,
    pub is_holiday_uk: bool,
    pub month: u32,
    pub week_of_year: u32,
    pub season: String,
    pub event_name_us: Option<String>,
    pub event_name_canada: Option<String>,
    pub event_name_uk: Option<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Promotion {
    pub promo_id: u32,
    pub sku: String,
    pub start_date: NaiveDate,
    pub end_date: NaiveDate,
    pub promo_type: String,
    pub discount_pct: u32,
    pub ad_feature: bool,
    pub display_type: String,
    pub expected_uplift: f64,
    pub supplier_funding_usd: f64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Assortment {
    pub store_id: u32,
    pub sku: String,
    pub active_from: NaiveDate,
    pub active_to: Option<NaiveDate>,
    pub planogram_facings: u32,
    pub shelf_height_cm: f64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GroundTruthEvent {
    pub event_id: u32,
    pub start_date: NaiveDate,
    pub end_date: NaiveDate,
    pub region: Option<String>,
    pub sku: Option<String>,
    pub label: String,
    pub magnitude: f64,
    pub notes: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SalesDaily {
    pub date: NaiveDate,
    pub store_id: u32,
    pub sku: String,
    pub units_sold: u32,
    pub gross_revenue: f64,
    pub promo_id: Option<u32>,
    pub regular_price: f64,
    pub net_price: f64,
    pub revenue: f64,
    pub supplier_rebate_amt: f64,
    pub spoilage_cost: f64,
    pub promo_funding_received: f64,
    pub gross_margin_pct: f64,
    pub discount_pct: u32,
    pub cogs_c: f64,
    pub cogs_s: f64,
    pub sales_date: NaiveDate,
    pub posting_date: NaiveDate,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct InventoryDaily {
    pub date: NaiveDate,
    pub store_id: u32,
    pub sku: String,
    pub on_hand: u32,
    pub on_order: u32,
    pub in_transit: u32,
    pub safety_stock: u32,
    pub last_scan_ts: NaiveDateTime,
    pub system_on_hand: u32,
    pub available_to_promise: u32,
    pub open_hours: u32,
    pub in_stock_hours: f64,
    pub dc_allocated_qty: u32,
    pub quarantine_hold: u32,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ReturnDaily {
    pub date: NaiveDate,
    pub store_id: u32,
    pub sku: String,
    pub units_returned: u32,
    pub reason_code: String,
    pub refund_value: f64,
}


#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SupplierShipment {
    pub shipment_id: u32,
    pub shipment_date: NaiveDate,
    pub delivery_date: NaiveDate,
    pub store_id: u32,
    pub sku: String,
    pub quantity_shipped: u32,
    pub quantity_received: u32,
    pub supplier_name: String,
    pub po_number: String,
    pub shipment_status: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct WasteSpoilage {
    pub waste_id: u32,
    pub date: NaiveDate,
    pub store_id: u32,
    pub sku: String,
    pub quantity_wasted: u32,
    pub waste_reason: String,
    pub waste_value: f64,
    pub recorded_by: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Ticket {
    pub ticket_id: u32,
    pub created_at: String,
    pub resolved_at: Option<String>,
    pub store_id: u32,
    pub sku: String,
    pub issue_type: String,
    pub description: String,
    pub root_cause: Option<String>,
    pub resolved: bool,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PriceChange {
    pub change_id: u32,
    pub date: NaiveDate,
    pub store_id: u32,
    pub sku: String,
    pub new_regular_price: f64,
    pub reason: String,
}

#[allow(dead_code)]
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Transaction {
    pub transaction_id: u32,
    pub date: NaiveDate,
    pub store_id: u32,
    pub timestamp: String,
    pub total_items: u32,
    pub payment_method: String,
    pub customer_type: String,
    pub total_amount: f64,
}

#[allow(dead_code)]
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TransactionItem {
    pub transaction_id: u32,
    pub sku: String,
    pub unit_price: f64,
    pub promo_id: Option<u32>,
    pub quantity: u32,
    pub line_total: f64,
}

#[derive(Debug, Clone)]
pub struct BrandInfo {
    pub name: String,
    pub tier: String,
    pub popularity: f64,
}

#[derive(Debug, Clone)]
pub struct CategoryConfig {
    pub elasticity: f64,
    #[allow(dead_code)]
    pub seasonality: String,
    pub dow_effect: f64,
}

// Reference data structures for seed data
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Region {
    pub region_id: u32,
    pub region_code: String,
    pub region_name: String,
    pub country: String,
    pub timezone: String,
    pub description: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Category {
    pub category_id: u32,
    pub category_name: String,
    pub category_group: String,
    pub margin_target_pct: f64,
    pub is_perishable: bool,
    pub elasticity: f64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct StoreType {
    pub store_type_id: u32,
    pub store_type_code: String,
    pub store_type_name: String,
    pub typical_sq_ft_min: u32,
    pub typical_sq_ft_max: u32,
    pub typical_sku_count: u32,
    pub operating_hours: u32,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Brand {
    pub brand_id: u32,
    pub brand_name: String,
    pub brand_tier: String,
    pub manufacturer: String,
    pub is_private_label: bool,
    pub brand_popularity: f64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Supplier {
    pub supplier_id: u32,
    pub supplier_name: String,
    pub supplier_type: String,
    pub lead_time_days: u32,
    pub reliability_score: f64,
    pub payment_terms: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PaymentMethod {
    pub payment_method_id: u32,
    pub payment_method_code: String,
    pub payment_method_name: String,
    pub processing_fee_pct: f64,
    pub is_active: bool,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PromotionType {
    pub promo_type_id: u32,
    pub promo_type_code: String,
    pub promo_type_name: String,
    pub typical_discount_pct: u32,
    pub typical_duration_days: u32,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ReturnReason {
    pub return_reason_id: u32,
    pub return_reason_code: String,
    pub return_reason_name: String,
    pub is_quality_issue: bool,
    pub is_preventable: bool,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct WasteReason {
    pub waste_reason_id: u32,
    pub waste_reason_code: String,
    pub waste_reason_name: String,
    pub is_preventable: bool,
}
