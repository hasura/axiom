use crate::models::*;
use chrono::{Datelike, NaiveDate};
use rand::Rng;
use std::collections::HashMap;

pub struct DemandCalculator<'a> {
    pub categories: &'a HashMap<String, CategoryConfig>,
    pub holidays: &'a HashMap<String, HashMap<u32, HashMap<String, NaiveDate>>>,
    pub calendar: &'a HashMap<NaiveDate, Calendar>,
    pub ground_truth_events: &'a [GroundTruthEvent],
}

impl<'a> DemandCalculator<'a> {
    pub fn calculate_demand<R: Rng>(
        &self,
        date: NaiveDate,
        store: &Store,
        product: &Product,
        active_promos: &[Promotion],
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
            if (climate == "hot" || climate == "temperate") && (month >= 6 && month <= 8) {
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

        // Holiday lift
        if let Some(cal) = self.calendar.get(&date) {
            let (event, holiday_lifts) = if store.region == "international" {
                if store.city.contains("ON") || store.city.contains("BC") || 
                   store.city.contains("QC") || store.city.contains("Toronto") ||
                   store.city.contains("Vancouver") || store.city.contains("Montreal") {
                    let lifts = get_canada_holiday_lifts();
                    (cal.event_name_canada.as_ref(), lifts)
                } else if store.city.contains("UK") || store.city.contains("London") {
                    let lifts = get_uk_holiday_lifts();
                    (cal.event_name_uk.as_ref(), lifts)
                } else {
                    (None, HashMap::new())
                }
            } else {
                let lifts = get_us_holiday_lifts();
                (cal.event_name_us.as_ref(), lifts)
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

fn get_us_holiday_lifts() -> HashMap<&'static str, HashMap<&'static str, f64>> {
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

fn get_canada_holiday_lifts() -> HashMap<&'static str, HashMap<&'static str, f64>> {
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

fn get_uk_holiday_lifts() -> HashMap<&'static str, HashMap<&'static str, f64>> {
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