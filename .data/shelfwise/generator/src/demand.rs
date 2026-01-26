use crate::models::*;
use chrono::{Datelike, NaiveDate};
use rand::Rng;
use std::collections::HashMap;
use std::sync::OnceLock;

// Cache holiday lifts as static data (built once, used millions of times)
static US_HOLIDAY_LIFTS: OnceLock<HashMap<&'static str, HashMap<&'static str, f64>>> = OnceLock::new();
static CANADA_HOLIDAY_LIFTS: OnceLock<HashMap<&'static str, HashMap<&'static str, f64>>> = OnceLock::new();
static UK_HOLIDAY_LIFTS: OnceLock<HashMap<&'static str, HashMap<&'static str, f64>>> = OnceLock::new();

pub struct DemandCalculator<'a> {
    pub categories: &'a HashMap<String, CategoryConfig>,
    pub holidays: &'a HashMap<String, HashMap<u32, HashMap<String, NaiveDate>>>,
    pub calendar: &'a HashMap<NaiveDate, Calendar>,
    pub ground_truth_events: &'a [GroundTruthEvent],
}

impl<'a> DemandCalculator<'a> {
    /// Calculate realistic transaction volume multiplier based on day-of-week, holidays, and seasonality
    /// This affects how many customers visit the store on a given day
    pub fn calculate_transaction_volume_multiplier(
        &self,
        date: NaiveDate,
        store: &Store,
    ) -> f64 {
        let mut multiplier: f64 = 1.0;

        // Day of week effect - biggest driver of daily variation
        let dow = date.weekday().num_days_from_monday();

        if store.store_type == "online" {
            // Online stores: weekdays busier (people shopping at work)
            // Monday-Thursday peak, Friday-Sunday slower
            match dow {
                0 => multiplier *= 1.15,  // Monday - strong start
                1 => multiplier *= 1.20,  // Tuesday - peak
                2 => multiplier *= 1.18,  // Wednesday - peak
                3 => multiplier *= 1.12,  // Thursday - good
                4 => multiplier *= 0.95,  // Friday - winding down
                5 => multiplier *= 0.85,  // Saturday - weekend
                6 => multiplier *= 0.80,  // Sunday - lowest
                _ => {}
            }
        } else {
            // Physical stores: weekends much busier
            // Saturday is peak, Sunday strong, weekdays lighter
            match dow {
                0 => multiplier *= 0.75,  // Monday - slowest weekday
                1 => multiplier *= 0.85,  // Tuesday
                2 => multiplier *= 0.90,  // Wednesday
                3 => multiplier *= 0.95,  // Thursday
                4 => multiplier *= 1.05,  // Friday - picking up
                5 => multiplier *= 1.45,  // Saturday - PEAK
                6 => multiplier *= 1.25,  // Sunday - strong
                _ => {}
            }

            // Store type modifiers
            match store.store_type.as_str() {
                "convenience" => {
                    // Convenience stores more consistent, less weekend spike
                    if dow >= 5 {
                        multiplier = (multiplier - 1.0) * 0.5 + 1.0; // Dampen weekend effect
                    }
                }
                "urban" => {
                    // Urban stores: weekday lunch rush, less weekend spike
                    if dow < 5 {
                        multiplier *= 1.10; // Weekday boost
                    } else {
                        multiplier = (multiplier - 1.0) * 0.7 + 1.0; // Smaller weekend spike
                    }
                }
                _ => {}
            }
        }

        // Holiday effects - major traffic drivers
        if let Some(cal) = self.calendar.get(&date) {
            let event = if store.region == "international" {
                if store.city.contains("ON") || store.city.contains("BC") ||
                   store.city.contains("QC") || store.city.contains("Toronto") ||
                   store.city.contains("Vancouver") || store.city.contains("Montreal") {
                    cal.event_name_canada.as_ref()
                } else if store.city.contains("UK") || store.city.contains("London") {
                    cal.event_name_uk.as_ref()
                } else {
                    None
                }
            } else {
                cal.event_name_us.as_ref()
            };

            if let Some(event_name) = event {
                match event_name.as_str() {
                    // Major shopping holidays
                    "Black Friday" => multiplier *= 2.8,
                    "Cyber Monday" => {
                        if store.store_type == "online" {
                            multiplier *= 3.5;
                        } else {
                            multiplier *= 0.7; // Physical stores quieter
                        }
                    }
                    "Christmas Eve" => multiplier *= 2.2,
                    "Christmas Week" => multiplier *= 1.6,
                    "Thanksgiving Week" => multiplier *= 1.8,
                    "Day Before Thanksgiving" => multiplier *= 2.5,

                    // Other holidays
                    "Super Bowl Sunday" => multiplier *= 1.4,
                    "Halloween" => multiplier *= 1.3,
                    "Easter" => multiplier *= 1.2,
                    "Independence Day" => multiplier *= 1.3,
                    "Memorial Day" => multiplier *= 1.2,
                    "Labor Day" => multiplier *= 1.2,

                    // Canadian holidays
                    "Boxing Day" => multiplier *= 2.0,
                    "Canada Day" => multiplier *= 1.3,
                    "Victoria Day" => multiplier *= 1.2,

                    // UK holidays
                    "Summer Bank Holiday" => multiplier *= 1.2,
                    "Spring Bank Holiday" => multiplier *= 1.2,

                    // Days when stores are closed or very quiet
                    "Christmas Day" => multiplier *= 0.1,
                    "New Year's Day" => multiplier *= 0.3,

                    _ => {}
                }
            }
        }

        // Seasonal patterns - monthly variation
        let month = date.month();
        match month {
            1 => multiplier *= 0.85,  // January - post-holiday slump
            2 => multiplier *= 0.90,  // February - still slow
            3 => multiplier *= 1.00,  // March - normal
            4 => multiplier *= 1.05,  // April - spring pickup
            5 => multiplier *= 1.10,  // May - strong
            6 => multiplier *= 1.05,  // June - summer starts
            7 => multiplier *= 1.00,  // July - vacation season
            8 => multiplier *= 1.05,  // August - back to school prep
            9 => multiplier *= 1.10,  // September - back to school
            10 => multiplier *= 1.15, // October - Halloween
            11 => multiplier *= 1.25, // November - Thanksgiving + Black Friday
            12 => multiplier *= 1.30, // December - Christmas shopping
            _ => {}
        }

        multiplier.max(0.1) // Never go below 10% of base traffic
    }

    pub fn calculate_demand<R: Rng>(
        &self,
        date: NaiveDate,
        store: &Store,
        product: &Product,
        active_promos: &[&Promotion],
        compliance_score: f64,
        rng: &mut R,
    ) -> u32 {
        // Base demand calculation
        let brand_pop = product.brand_popularity;
        let category_pop = if product.category == "beverages" || product.category == "snacks" {
            1.2
        } else {
            1.0
        };

        // Store type factors
        let store_type_factor = match store.store_type.as_str() {
            "online" => 12.0,
            "big_box" => 5.0,
            "suburban" => 3.0,
            "urban" => 2.0,
            "convenience" => 0.8,
            _ => 1.0,
        };

        // Region factors
        let region_factor = match store.region.as_str() {
            "west" => 1.15,
            "southwest" => 1.10,
            "midwest" => 1.0,
            "northeast" => 1.20,
            "southeast" => 0.95,
            "nationwide" => 1.3,
            "international" => 1.25,
            _ => 1.0,
        };

        // Price elasticity
        let price_elastic = 1.0 - (product.list_price - 10.0) * 0.01;

        // Base units
        let units_base = brand_pop * category_pop * store_type_factor
            * region_factor * price_elastic * product.pareto_weight * 1200.0;

        let mut multiplier = 1.0;

        // Seasonality
        let month = date.month();
        let climate = &store.climate_zone;
        let category = &product.category;

        if category == "beverages" {
            if (climate == "hot" || climate == "temperate") && (6..=8).contains(&month) {
                multiplier *= 1.4;
            } else if climate == "cold" && (month == 12 || month == 1 || month == 2) {
                multiplier *= 0.8;
            }
        } else if category == "canned" || category == "frozen" {
            if climate == "cold" && (month >= 11 || month <= 2) {
                multiplier *= 1.3;
            }
        } else if category == "candy" {
            if month == 10 {
                multiplier *= 2.5;
            } else if month == 3 {
                multiplier *= 1.8;
            }
        } else if category == "snacks" && store.region != "international" {
            // Check for Super Bowl Sunday
            if let Some(us_holidays) = self.holidays.get("us") {
                if let Some(year_holidays) = us_holidays.get(&(date.year() as u32)) {
                    if let Some(super_bowl) = year_holidays.get("Super Bowl Sunday") {
                        if date == *super_bowl {
                            multiplier *= 2.0;
                        }
                    }
                }
            }
        }

        // Day of week effect
        let dow = date.weekday().num_days_from_monday();
        if let Some(cat_config) = self.categories.get(category) {
            let dow_effect = cat_config.dow_effect;

            if store.store_type == "online" {
                if dow >= 5 {
                    multiplier *= 0.9;
                } else {
                    multiplier *= 1.1;
                }

                // Cyber Monday boost
                if let Some(cal) = self.calendar.get(&date) {
                    if store.region == "international" {
                        // Check Canadian/UK holidays
                        if store.city.contains("ON") || store.city.contains("BC") ||
                           store.city.contains("QC") || store.city.contains("Toronto") ||
                           store.city.contains("Vancouver") || store.city.contains("Montreal") {
                            if let Some(event) = &cal.event_name_canada {
                                if event == "Cyber Monday" {
                                    multiplier *= 2.5;
                                }
                            }
                        } else if store.city.contains("UK") || store.city.contains("London") {
                            if let Some(event) = &cal.event_name_uk {
                                if event == "Cyber Monday" {
                                    multiplier *= 2.5;
                                }
                            }
                        }
                    } else if let Some(event) = &cal.event_name_us {
                        if event == "Cyber Monday" {
                            multiplier *= 2.5;
                        }
                    }
                }
            } else if dow >= 5 {
                multiplier *= 1.0 + dow_effect;
            } else if store.store_type == "urban" && category == "snacks" {
                multiplier *= 1.0 - dow_effect * 0.5;
            }
        }

        // Holiday lift (using cached static data)
        if let Some(cal) = self.calendar.get(&date) {
            let (event, holiday_lifts) = if store.region == "international" {
                if store.city.contains("ON") || store.city.contains("BC") ||
                   store.city.contains("QC") || store.city.contains("Toronto") ||
                   store.city.contains("Vancouver") || store.city.contains("Montreal") {
                    (cal.event_name_canada.as_ref(), CANADA_HOLIDAY_LIFTS.get_or_init(build_canada_holiday_lifts))
                } else if store.city.contains("UK") || store.city.contains("London") {
                    (cal.event_name_uk.as_ref(), UK_HOLIDAY_LIFTS.get_or_init(build_uk_holiday_lifts))
                } else {
                    (None, &HashMap::new())
                }
            } else {
                (cal.event_name_us.as_ref(), US_HOLIDAY_LIFTS.get_or_init(build_us_holiday_lifts))
            };

            if let Some(event_name) = event {
                if let Some(category_lifts) = holiday_lifts.get(event_name.as_str()) {
                    if let Some(&lift) = category_lifts.get(category.as_str()) {
                        multiplier *= lift;
                    }
                }
            }
        }

        // Promotion uplift
        if let Some(promo) = active_promos.first() {
            if promo.discount_pct > 0 {
                if let Some(cat_config) = self.categories.get(category) {
                    let elasticity = cat_config.elasticity.abs();
                    multiplier *= 1.0 + (promo.discount_pct as f64 / 100.0) * elasticity;
                }
            }

            match promo.display_type.as_str() {
                "endcap" => multiplier *= 1.3,
                "aisle" => multiplier *= 1.15,
                "checkout" => multiplier *= 1.4,
                _ => {}
            }

            if promo.ad_feature {
                multiplier *= 1.2;
            }
        }

        // Planogram compliance effect
        if compliance_score < 70.0 {
            multiplier *= 0.6 + compliance_score / 175.0;
        }

        // Ground truth macroeconomic events
        for event in self.ground_truth_events {
            if date >= event.start_date && date <= event.end_date {
                match event.label.as_str() {
                    "covid_panic_buying" => {
                        if matches!(category.as_str(), "household" | "canned" | "frozen" | "personal_care") {
                            multiplier *= 1.0 + event.magnitude * 1.5;
                        } else if matches!(category.as_str(), "produce" | "dairy" | "meat") {
                            multiplier *= 1.0 + event.magnitude * 0.8;
                        } else {
                            multiplier *= 1.0 + event.magnitude * 0.3;
                        }
                    }
                    "covid_lockdown" => {
                        if matches!(category.as_str(), "candy" | "snacks" | "beverages") {
                            multiplier *= 1.1;
                        } else if category == "personal_care" {
                            multiplier *= 0.6;
                        } else {
                            multiplier *= 1.0 + event.magnitude;
                        }
                    }
                    "supply_chain_crisis" => {
                        if rng.gen::<f64>() < 0.15 {
                            multiplier *= 0.3;
                        } else {
                            multiplier *= 0.95;
                        }
                    }
                    "inflation_surge" => {
                        if let Some(cat_config) = self.categories.get(category) {
                            let elasticity = cat_config.elasticity.abs();
                            let days_elapsed = (date - event.start_date).num_days() as f64;
                            let price_increase = event.magnitude * days_elapsed / 365.0;
                            multiplier *= 1.0 - price_increase * elasticity * 0.3;
                        }
                    }
                    "labor_shortage" => {
                        if store.store_type != "online" {
                            multiplier *= 0.92;
                        }
                    }
                    "ukraine_war_impact" => {
                        if matches!(category.as_str(), "bakery" | "cereal" | "snacks") {
                            multiplier *= 0.85;
                        }
                    }
                    "recession_fears" => {
                        if product.brand == "ShelfWise Basics" {
                            multiplier *= 1.25;
                        } else if product.tier == "premium" {
                            multiplier *= 0.75;
                        } else {
                            multiplier *= 0.90;
                        }
                    }
                    "normalization" => {
                        multiplier *= 1.0 + event.magnitude;
                    }
                    "ai_automation" => {
                        if store.store_type == "online" {
                            multiplier *= 1.15;
                        } else {
                            multiplier *= 1.08;
                        }
                    }
                    _ => {}
                }
            }
        }

        // Add small noise (max 3%)
        let noise: f64 = rng.gen_range(0.97..1.03);
        multiplier *= noise.clamp(0.5, 2.0);

        // Calculate final demand
        let daily_demand = units_base * multiplier;
        daily_demand.max(0.0) as u32
    }
}

fn build_us_holiday_lifts() -> HashMap<&'static str, HashMap<&'static str, f64>> {
    let mut lifts = HashMap::new();

    let mut thanksgiving = HashMap::new();
    thanksgiving.insert("meat", 1.8);
    thanksgiving.insert("produce", 1.5);
    thanksgiving.insert("bakery", 1.6);
    lifts.insert("Thanksgiving Week", thanksgiving);

    let mut christmas = HashMap::new();
    christmas.insert("candy", 1.7);
    christmas.insert("beverages", 1.3);
    christmas.insert("snacks", 1.4);
    lifts.insert("Christmas Week", christmas);

    let mut super_bowl = HashMap::new();
    super_bowl.insert("snacks", 2.0);
    super_bowl.insert("beverages", 1.6);
    super_bowl.insert("meat", 1.4);
    lifts.insert("Super Bowl Sunday", super_bowl);

    let mut halloween = HashMap::new();
    halloween.insert("candy", 2.5);
    lifts.insert("Halloween", halloween);

    let mut easter = HashMap::new();
    easter.insert("candy", 1.8);
    easter.insert("meat", 1.3);
    lifts.insert("Easter", easter);

    let mut july4 = HashMap::new();
    july4.insert("meat", 1.6);
    july4.insert("beverages", 1.4);
    july4.insert("snacks", 1.3);
    lifts.insert("Independence Day", july4);

    let mut memorial = HashMap::new();
    memorial.insert("meat", 1.5);
    memorial.insert("beverages", 1.3);
    lifts.insert("Memorial Day", memorial);

    let mut labor = HashMap::new();
    labor.insert("meat", 1.4);
    labor.insert("beverages", 1.2);
    lifts.insert("Labor Day", labor);

    lifts
}

fn build_canada_holiday_lifts() -> HashMap<&'static str, HashMap<&'static str, f64>> {
    let mut lifts = HashMap::new();

    let mut thanksgiving = HashMap::new();
    thanksgiving.insert("meat", 1.6);
    thanksgiving.insert("produce", 1.4);
    thanksgiving.insert("bakery", 1.5);
    lifts.insert("Thanksgiving", thanksgiving);

    let mut christmas = HashMap::new();
    christmas.insert("candy", 1.7);
    christmas.insert("beverages", 1.3);
    christmas.insert("snacks", 1.4);
    lifts.insert("Christmas Week", christmas);

    let mut boxing = HashMap::new();
    boxing.insert("snacks", 1.3);
    boxing.insert("beverages", 1.2);
    lifts.insert("Boxing Day", boxing);

    let mut canada_day = HashMap::new();
    canada_day.insert("meat", 1.5);
    canada_day.insert("beverages", 1.4);
    canada_day.insert("snacks", 1.3);
    lifts.insert("Canada Day", canada_day);

    let mut victoria = HashMap::new();
    victoria.insert("meat", 1.4);
    victoria.insert("beverages", 1.3);
    lifts.insert("Victoria Day", victoria);

    let mut easter = HashMap::new();
    easter.insert("candy", 1.8);
    easter.insert("meat", 1.3);
    lifts.insert("Easter", easter);

    let mut easter_mon = HashMap::new();
    easter_mon.insert("candy", 1.5);
    lifts.insert("Easter Monday", easter_mon);

    lifts
}

fn build_uk_holiday_lifts() -> HashMap<&'static str, HashMap<&'static str, f64>> {
    let mut lifts = HashMap::new();

    let mut christmas = HashMap::new();
    christmas.insert("candy", 1.6);
    christmas.insert("beverages", 1.3);
    christmas.insert("snacks", 1.3);
    lifts.insert("Christmas Week", christmas);

    let mut boxing = HashMap::new();
    boxing.insert("snacks", 1.4);
    boxing.insert("beverages", 1.2);
    lifts.insert("Boxing Day", boxing);

    let mut easter = HashMap::new();
    easter.insert("candy", 1.7);
    easter.insert("meat", 1.2);
    lifts.insert("Easter", easter);

    let mut easter_mon = HashMap::new();
    easter_mon.insert("candy", 1.4);
    lifts.insert("Easter Monday", easter_mon);

    let mut summer = HashMap::new();
    summer.insert("meat", 1.3);
    summer.insert("beverages", 1.3);
    summer.insert("snacks", 1.2);
    lifts.insert("Summer Bank Holiday", summer);

    let mut spring = HashMap::new();
    spring.insert("meat", 1.2);
    spring.insert("beverages", 1.2);
    lifts.insert("Spring Bank Holiday", spring);

    lifts
}