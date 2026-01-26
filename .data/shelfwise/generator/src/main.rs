mod config;
mod generator;
mod models;
mod holidays;
mod demand;
mod streaming;
mod reference_data;
mod inventory;

use anyhow::Result;
use clap::Parser;
use config::Config;
use generator::ShelfWiseDataGenerator;

#[derive(Parser, Debug)]
#[command(
    name = "shelfwise-generator",
    about = "Generate ShelfWise synthetic dataset with streaming (constant RAM usage)",
    long_about = "Examples:\n\
    # Generate fresh dataset using config file\n\
    cargo run --release\n\n\
    # Generate specific date range (overrides config)\n\
    cargo run --release -- --start-date 2025-12-15 --end-date 2025-12-15\n\n\
    # Nightly mode: load reference data from CSV, generate single day\n\
    cargo run --release -- --reference-dir ../postgres/nightly --start-date 2025-12-16 --end-date 2025-12-16"
)]
struct Args {
    /// Output directory for CSV files
    #[arg(short, long, default_value = "../postgres")]
    output: String,

    /// Random seed for reproducibility
    #[arg(short, long, default_value_t = 42)]
    seed: u64,

    /// Continue mode: append to existing data without regenerating reference tables
    #[arg(long = "continue")]
    continue_mode: bool,

    /// Path to configuration file
    #[arg(long, default_value = "config.toml")]
    config: String,

    /// Start date (YYYY-MM-DD) - overrides config file
    #[arg(long)]
    start_date: Option<String>,

    /// End date (YYYY-MM-DD) - overrides config file
    #[arg(long)]
    end_date: Option<String>,

    /// Reference directory: load customers/drivers from CSV instead of regenerating
    /// Use this for nightly imports to preserve existing created_date/hire_date values
    #[arg(long)]
    reference_dir: Option<String>,
}

fn main() -> Result<()> {
    let args = Args::parse();

    if args.continue_mode {
        println!("\n🔄 CONTINUE MODE ENABLED");
        println!("This will:");
        println!("  ✓ Load existing reference data (products, stores, promotions)");
        println!("  ✓ Append new transactional data to existing files");
        println!("  ✓ Skip regenerating static reference tables");
        println!();
    }

    // Load configuration from specified file
    let mut config = Config::load(&args.config)?;

    // Override dates from CLI if provided
    if let Some(start_date) = &args.start_date {
        println!("📅 Overriding start_date from CLI: {}", start_date);
        config.date_range.start_date = start_date.clone();
    }
    if let Some(end_date) = &args.end_date {
        println!("📅 Overriding end_date from CLI: {}", end_date);
        config.date_range.end_date = end_date.clone();
    }

    println!("📋 Configuration:");
    println!("   Date range: {} to {}", config.date_range.start_date, config.date_range.end_date);
    println!("   Products: {}", config.scale.max_products);
    println!("   Stores: {} domestic + {} international",
             config.scale.num_domestic_stores,
             config.scale.num_international_stores);

    if let Some(ref_dir) = &args.reference_dir {
        println!("📂 Loading reference data from: {}", ref_dir);
    }

    let mut generator = ShelfWiseDataGenerator::new(args.seed, config);
    generator.save_data(&args.output, args.continue_mode, args.reference_dir.as_deref())?;

    Ok(())
}