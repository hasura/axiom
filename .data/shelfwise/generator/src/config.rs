use anyhow::Result;
use serde::Deserialize;
use std::fs;

#[derive(Debug, Deserialize)]
pub struct Config {
    pub date_range: DateRange,
    pub scale: Scale,
    pub assortment: Assortment,
    pub performance: Performance,
}

#[derive(Debug, Deserialize)]
pub struct DateRange {
    pub start_date: String,
    pub end_date: String,
}

#[derive(Debug, Deserialize)]
pub struct Scale {
    pub max_products: usize,
    pub num_domestic_stores: usize,
    pub num_international_stores: usize,
}

#[derive(Debug, Deserialize)]
pub struct Assortment {
    pub online_coverage: f64,
    pub big_box_coverage: f64,
    pub suburban_coverage: f64,
    pub urban_coverage: f64,
    pub convenience_coverage: f64,
}

#[derive(Debug, Deserialize)]
pub struct Performance {
    pub progress_interval_days: usize,
}

impl Config {
    pub fn load(path: &str) -> Result<Self> {
        let contents = fs::read_to_string(path)?;
        let config: Config = toml::from_str(&contents)?;
        Ok(config)
    }
}