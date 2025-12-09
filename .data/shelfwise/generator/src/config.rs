use serde::Deserialize;
use anyhow::Result;
use std::fs;

#[derive(Debug, Deserialize, Clone)]
pub struct Config {
    pub date_range: DateRange,
    pub scale: Scale,
    pub customers: Customers,
    pub performance: Performance,
}

#[derive(Debug, Deserialize, Clone)]
pub struct DateRange {
    pub start_date: String,
    pub end_date: String,
}

#[derive(Debug, Deserialize, Clone)]
pub struct Scale {
    pub max_products: usize,
    pub num_domestic_stores: usize,
    pub num_international_stores: usize,
}

#[derive(Debug, Deserialize, Clone)]
pub struct Customers {
    pub num_customers: usize,
}

#[derive(Debug, Deserialize, Clone)]
pub struct Performance {
    pub progress_interval_days: usize,
    pub flush_interval_days: usize,
    #[serde(default = "default_batch_size")]
    pub batch_size: usize,
}

fn default_batch_size() -> usize {
    2000  // Optimized for high-performance systems
}

impl Config {
    pub fn load(path: &str) -> Result<Self> {
        let contents = fs::read_to_string(path)?;
        let config: Config = toml::from_str(&contents)?;
        Ok(config)
    }
}