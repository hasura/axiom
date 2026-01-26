# ShelfWise Generator

Rust-based synthetic data generator for the ShelfWise grocery demo. Generates realistic retail data including customers, transactions, inventory, deliveries, and support tickets.

## Target Metrics (Industry Benchmarks 2025/26)

The generator produces data calibrated to match these U.S. grocery industry benchmarks:

| Metric | Target | Source |
|--------|--------|--------|
| Average Basket Value (ABV) | $45-65 | Progressive Grocer 2024 |
| Items per transaction | 8-12 | FMI State of Food Retailing |
| Price per item | $4.50-6.50 | NielsenIQ Scanner Data |
| Weekly transactions/store | 10,000-15,000 | IGD Retail Analysis |
| Loyalty penetration | 70-80% | McKinsey Grocery Insights |
| Delivery basket premium | 1.3-1.5x in-store | Brick Meets Click 2024 |
| Weekend transaction lift | +20% | Placer.ai Foot Traffic |
| Return rate | 2-4% of transactions | NRF Consumer Returns |
| Online/delivery share | 10-15% of revenue | eMarketer Grocery |
| Stockout rate | 2-8% of SKU-days | IHL Group Retail |

### Basket Size Distribution
- **35%**: Quick trips (2-5 items) - forgot-something, lunch runs
- **50%**: Regular shopping (6-12 items) - weekly grocery run
- **15%**: Stock-up trips (14-24 items) - monthly big shop

### Fulfillment Multipliers
- **Delivery orders**: +40% basket size vs in-store
- **Pickup orders**: +20% basket size vs in-store
- **Saturday**: +25% basket size
- **Sunday**: +18% basket size

### Validation Queries

Quick SQL queries to validate metrics after loading data:

```sql
-- ABV & items per transaction (target: $45-65, 8-12 items)
SELECT ROUND(AVG(total_amount)::numeric, 2) AS abv,
       ROUND(AVG(total_items)::numeric, 1) AS items_per_txn,
       '$45-65 / 8-12' AS target
FROM transactions;

-- Price per item (target: $4.50-6.50)
SELECT ROUND((SUM(total_amount) / SUM(total_items))::numeric, 2) AS price_per_item,
       '$4.50-6.50' AS target
FROM transactions;

-- Weekly transactions per store (target: 10,000-15,000)
SELECT ROUND(COUNT(*)::numeric / COUNT(DISTINCT store_id) /
       ((MAX(date) - MIN(date)) / 7.0), 0) AS weekly_txns_per_store,
       '10k-15k' AS target
FROM transactions;

-- Stockout rate (target: 2-8%)
SELECT ROUND(100.0 * COUNT(*) FILTER (WHERE on_hand = 0) / COUNT(*), 2) AS stockout_pct,
       '2-8%' AS target
FROM inventory_daily;

-- Loyalty penetration (target: 70-80%)
SELECT ROUND(100.0 * COUNT(*) FILTER (WHERE is_loyalty_transaction) / COUNT(*), 1) AS loyalty_pct,
       '70-80%' AS target
FROM transactions;

-- Delivery premium (target: 1.3-1.5x)
SELECT ROUND(AVG(total_amount) FILTER (WHERE fulfillment_type = 'delivery') /
             AVG(total_amount) FILTER (WHERE fulfillment_type = 'in_store'), 2) AS delivery_premium,
       '1.3-1.5x' AS target
FROM transactions;

-- Online/delivery share (target: 10-15%)
SELECT ROUND(100.0 * SUM(total_amount) FILTER (WHERE fulfillment_type IN ('delivery', 'pickup'))
             / SUM(total_amount), 1) AS online_share_pct,
       '10-15%' AS target
FROM transactions;

-- Return rate (target: 2-4%)
SELECT ROUND(100.0 * (SELECT COUNT(*) FROM returns_daily) / COUNT(*), 2) AS return_rate_pct,
       '2-4%' AS target
FROM transactions;

-- Weekend lift (target: +20%)
SELECT ROUND(100.0 * (AVG(total_amount) FILTER (WHERE EXTRACT(dow FROM date) IN (0, 6)) /
             AVG(total_amount) FILTER (WHERE EXTRACT(dow FROM date) NOT IN (0, 6)) - 1), 0) AS weekend_lift_pct,
       '+20%' AS target
FROM transactions;
```

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

## Inventory & Stockout Behavior

The generator simulates realistic inventory management with self-regulating stockout rates:

### Stockout Rate Pattern (1-year validation)
- **Weeks 1-2**: ~5-6% (initial buffer depletion)
- **Weeks 3-4**: ~0.5% (reorder overcorrection)
- **Weeks 5-17**: 0.8-2.4% (system settling)
- **Weeks 18-31**: 2-5% (stable equilibrium)
- **High-demand periods**: 6-8% (summer, holidays)
- **Recovery periods**: 3-5% (post-spike)

### Self-Regulation Mechanism
The inventory system uses a rolling 30-day sales history with a bootstrap floor:
- When history is available: uses actual sales average
- When history is empty or polluted: falls back to demand estimate × popularity multiplier (3.5-5x)
- This prevents permanent depletion and enables recovery after stress periods

### Key Parameters (in `inventory.rs`)
- **Service level**: Z=1.65 (95% target, allows 2-5% natural stockouts)
- **Reorder buffer**: 1.5x (triggers orders with lead time cushion)
- **Bootstrap multipliers**: 3.5x-5.0x based on product popularity
- **Initial inventory**: 3-7 days safety stock depending on category

## Notes

- Shipments only generate on Mon/Wed/Fri (realistic delivery schedule)
- Returns reference historical purchases, so first few days of a fresh run have fewer returns
- New customers/drivers are created organically based on growth rates in config
- The `--continue` flag with `--reference-dir` is designed for nightly cron jobs

