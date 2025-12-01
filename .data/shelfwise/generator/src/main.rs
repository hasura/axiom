mod config;
mod generator;
mod models;
mod holidays;
mod demand;
mod streaming;
mod reference_data;

use anyhow::Result;
use clap::Parser;
use config::Config;
use generator::ShelfWiseDataGenerator;

#[derive(Parser, Debug)]
#[command(
    name = "shelfwise-generator",
    about = "Generate ShelfWise synthetic dataset with streaming (constant RAM usage)",
    long_about = "Examples:\n\
    # Generate fresh dataset for November 2025\n\
    cargo run --release\n\n\
    # Generate January 2025, then continue with February\n\
    # First, edit START_DATE and END_DATE to January 2025\n\
    cargo run --release\n\n\
    # Then edit to February 2025 and use --continue\n\
    cargo run --release -- --continue"
)]
struct Args {
    /// Output directory for CSV files
    #[arg(short, long, default_value = "../postgres")]
    output: String,

    /// Random seed for reproducibility
    #[arg(short, long, default_value_t = 42)]
    seed: u64,

    /// Continue mode: append to existing data without regenerating reference tables
    #[arg(short, long)]
    continue_mode: bool,

    /// Path to configuration file
    #[arg(long, default_value = "config.toml")]
    config: String,
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
    let config = Config::load(&args.config)?;
    println!("📋 Loaded configuration from {}", args.config);
    println!("   Date range: {} to {}", config.date_range.start_date, config.date_range.end_date);
    println!("   Products: {}", config.scale.max_products);
    println!("   Stores: {} domestic + {} international",
             config.scale.num_domestic_stores,
             config.scale.num_international_stores);

    let mut generator = ShelfWiseDataGenerator::new(args.seed, config);
    generator.save_data(&args.output, args.continue_mode)?;

    Ok(())
}