# ShelfWise Generator

Rust-based synthetic data generator for the ShelfWise grocery demo. Generates realistic retail data including customers, transactions, inventory, deliveries, and support tickets.

## Build

Requires Rust 1.70+. Install via https://rustup.rs if you don't have it.

```bash
cd .data/shelfwise/generator
cargo build --release
```

Binary ends up at `target/release/shelfwise-generator`.

## Quick Start

```bash
cd .data/shelfwise/generator

# Full generation (uses config.toml)
cargo run --release

# Test run (smaller dataset, 3 months)
cargo run --release -- --config config.test.toml
```

Output goes to `../postgres/` by default.

## Nightly Updates

For incremental daily data generation:

```bash
cargo run --release -- \
  --reference-dir ../postgres \
  --start-date 2025-12-15 \
  --end-date 2025-12-15 \
  --output ../postgres/nightly \
  --continue
```

This loads existing customers/drivers from CSV, generates transactions for that day, and outputs any new customers/drivers whose `created_date` or `hire_date` matches the target date.

There's a wrapper script that handles everything automatically:

```bash
../scripts/nightly-import.sh
```

It detects missing dates, runs the generator, and imports to Postgres. Add to cron:

```
0 6 * * * /path/to/shelfwise/scripts/nightly-import.sh >> /path/to/logs/cron.log 2>&1
```

## CLI Options

```
-o, --output <DIR>        Output directory (default: ../postgres)
-s, --seed <N>            Random seed for reproducibility (default: 42)
    --config <FILE>       Config file (default: config.toml)
    --start-date <DATE>   Override config start date (YYYY-MM-DD)
    --end-date <DATE>     Override config end date (YYYY-MM-DD)
    --reference-dir <DIR> Load customers/drivers from existing CSVs
    --continue            Append mode - skip regenerating reference tables
```

## Config

Edit `config.toml` to adjust:

- Date range
- Number of products/customers/stores
- Growth rates
- Store distribution

See `config.test.toml` for a minimal example.

## What Gets Generated

**Reference data** (generated once):
- Products, brands, categories
- Stores, regions, store types
- Suppliers, promotions
- Customers, delivery drivers

**Daily data** (per day in range):
- Transactions + line items
- Inventory levels
- Deliveries
- Returns, waste/spoilage
- Support tickets
- Price changes
- Supplier shipments (Mon/Wed/Fri only)

## Notes

- Shipments only generate on Mon/Wed/Fri (realistic delivery schedule)
- Returns reference historical purchases, so first few days of a fresh run have fewer returns
- New customers/drivers are created organically based on growth rates in config
- The `--continue` flag with `--reference-dir` is designed for nightly cron jobs

