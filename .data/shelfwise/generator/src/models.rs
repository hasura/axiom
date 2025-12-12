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
    pub transaction_id: u64,
    pub line_number: u32,
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
    pub transaction_id: u64,
    pub date: NaiveDate,
    pub store_id: u32,
    pub timestamp: String,
    pub total_items: u32,
    pub payment_method: String,
    pub customer_type: String,
    pub total_amount: f64,

    // Customer tracking (optional - only for tracked transactions)
    pub customer_id: Option<u64>,
    pub is_loyalty_transaction: bool,
    pub loyalty_points_earned: u32,
    pub loyalty_points_redeemed: u32,

    // Delivery/fulfillment (optional - only for online orders)
    pub fulfillment_type: Option<String>,  // 'in_store', 'pickup', 'delivery', 'marketplace'
    pub order_status: Option<String>,      // 'pending', 'picking', 'ready', 'out_for_delivery', 'delivered', 'cancelled'
    pub fulfillment_store_id: Option<u32>, // Which store fulfills this order
    pub delivery_address_id: Option<u64>,
    pub delivery_fee: f64,
    pub tip_amount: f64,
    pub delivery_instructions: Option<String>,
    pub requested_delivery_time: Option<NaiveDateTime>,
    pub actual_delivery_time: Option<NaiveDateTime>,
}

// Transaction line items - detailed product-level transaction data
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TransactionLineItem {
    pub transaction_id: u64,
    pub line_number: u32,
    pub sku: String,
    pub quantity: u32,
    pub unit_price: f64,
    pub line_total: f64,
    pub promo_id: Option<u32>,
    pub discount_amount: f64,
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

// ============================================================================
// CUSTOMER DATA MODELS
// ============================================================================

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Customer {
    pub customer_id: u64,
    pub email: String,
    pub phone: String,
    pub first_name: String,
    pub last_name: String,

    // Demographics
    pub age_bracket: String,
    pub household_size: u32,
    pub income_bracket: String,

    // Geographic affinity
    pub primary_store_id: u32,
    pub primary_city: String,
    pub home_latitude: f64,
    pub home_longitude: f64,

    // Loyalty program
    pub loyalty_member: bool,
    pub loyalty_tier: Option<String>,
    pub loyalty_join_date: Option<NaiveDate>,
    pub loyalty_points: u32,

    // Shopping preferences
    pub preferred_shopping_time: String,
    pub avg_basket_size: f64,
    pub price_sensitivity: String,

    // Behavioral segments
    pub customer_segment: String,

    // Metadata
    pub created_date: NaiveDate,
    pub last_purchase_date: Option<NaiveDate>,
    pub total_lifetime_value: f64,
    pub total_visits: u32,

    // Online behavior
    pub has_online_account: bool,
    pub prefers_online: bool,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CustomerAddress {
    pub address_id: u64,
    pub customer_id: u64,
    pub address_type: String,
    pub is_default: bool,
    pub street_address: String,
    pub apartment_unit: Option<String>,
    pub city: String,
    pub state: String,
    pub zip_code: String,
    pub latitude: f64,
    pub longitude: f64,
    pub delivery_instructions: Option<String>,
    pub has_doorman: bool,
    pub requires_signature: bool,
    pub created_at: NaiveDateTime,
    pub last_used_at: Option<NaiveDateTime>,
    pub delivery_count: u32,
}

// ============================================================================
// DELIVERY & FULFILLMENT MODELS
// ============================================================================

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DeliveryDriver {
    pub driver_id: u64,
    pub first_name: String,
    pub last_name: String,
    pub phone: String,
    pub email: String,

    // Driver type
    pub driver_type: String,
    pub employment_status: String,

    // Service area
    pub primary_store_id: u32,
    pub service_radius_miles: f64,
    pub service_cities: String, // Comma-separated list

    // Vehicle info
    pub vehicle_type: String,
    pub vehicle_capacity_items: u32,
    pub has_insulated_bags: bool,

    // Performance metrics
    pub total_deliveries: u32,
    pub avg_rating: f64,
    pub on_time_delivery_pct: f64,
    pub acceptance_rate: f64,
    pub cancellation_rate: f64,

    // Availability
    pub is_available: bool,
    pub current_latitude: f64,
    pub current_longitude: f64,
    pub last_location_update: NaiveDateTime,

    // Dates
    pub hire_date: NaiveDate,
    pub last_delivery_date: Option<NaiveDate>,

    // Compensation
    pub base_pay_per_delivery: f64,
    pub mileage_rate: f64,
    pub avg_tips_per_delivery: f64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DeliveryAssignment {
    pub assignment_id: u64,
    pub transaction_id: u64,
    pub driver_id: u64,

    // Assignment lifecycle
    pub assigned_at: NaiveDateTime,
    pub accepted_at: Option<NaiveDateTime>,
    pub picked_up_at: Option<NaiveDateTime>,
    pub delivered_at: Option<NaiveDateTime>,
    pub cancelled_at: Option<NaiveDateTime>,

    // Status tracking
    pub assignment_status: String,
    pub cancellation_reason: Option<String>,

    // Logistics
    pub pickup_store_id: u32,
    pub estimated_pickup_time: NaiveDateTime,
    pub actual_pickup_time: Option<NaiveDateTime>,
    pub estimated_delivery_time: NaiveDateTime,
    pub actual_delivery_time: Option<NaiveDateTime>,

    // Distance and time
    pub distance_miles: f64,
    pub estimated_duration_minutes: u32,
    pub actual_duration_minutes: Option<u32>,

    // Compensation
    pub driver_pay: f64,
    pub driver_tip: f64,
    pub driver_total_earnings: f64,

    // Quality
    pub customer_rating: Option<u32>,
    pub driver_notes: Option<String>,
    pub customer_feedback: Option<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DeliveryZone {
    pub zone_id: u32,
    pub zone_name: String,
    pub store_id: u32,

    // Geographic boundary
    pub center_latitude: f64,
    pub center_longitude: f64,
    pub radius_miles: f64,

    // Service parameters
    pub delivery_fee: f64,
    pub min_order_amount: f64,
    pub free_delivery_threshold: f64,
    pub estimated_delivery_time_minutes: u32,

    // Availability
    pub is_active: bool,
    pub service_hours_start: String,
    pub service_hours_end: String,

    // Demand
    pub avg_daily_orders: u32,
    pub peak_hours: String, // Comma-separated
}

// ============================================================================
// INTERNAL HELPER STRUCTURES (not serialized to CSV)
// ============================================================================

#[derive(Debug, Clone)]
#[allow(dead_code)]
pub struct CustomerBehavior {
    pub customer_id: u64,
    pub segment: String,
    pub shopping_frequency_days: u32,
    pub avg_basket_size: u32,
    pub brand_loyalty_score: f64,
    pub price_sensitivity: f64,
    pub preferred_categories: Vec<String>,
    pub preferred_brands: Vec<String>,
    pub last_visit_date: Option<NaiveDate>,
}
