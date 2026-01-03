#!/bin/bash
# ShelfWise Nightly Data Import - Simple Version
#
# This script runs automatically via cron to add daily data.
# NO PARAMETERS REQUIRED - designed for crontab use.
#
# Usage:
#   ./nightly-import.sh              # Auto-detect and fill gaps (default)
#   ./nightly-import.sh --date YYYY-MM-DD  # Generate specific date (testing)
#
# The script will:
# 1. Export customers/drivers from database
# 2. Detect missing dates (last_date+1 to yesterday)
# 3. Run generator with --reference-dir to load existing customers
# 4. Import generated daily data + new customers/drivers
#
# For crontab, add:
#   0 2 * * * /path/to/shelfwise/scripts/nightly-import.sh >> /path/to/shelfwise/logs/cron.log 2>&1

set -e  # Exit on any error
set -o pipefail  # Catch errors in pipes

# ============================================================================
# CONFIGURATION
# ============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SHELFWISE_HOME="$(dirname "$SCRIPT_DIR")"
GENERATOR_DIR="$SHELFWISE_HOME/generator"
REFERENCE_DIR="$SHELFWISE_HOME/postgres/reference"
OUTPUT_DIR="$SHELFWISE_HOME/postgres/nightly"
LOG_DIR="${LOG_DIR:-$SHELFWISE_HOME/logs}"
LOG_FILE="${LOG_FILE:-$LOG_DIR/nightly-import.log}"
# Generator config - MUST match the config used for initial data load
GENERATOR_CONFIG="${GENERATOR_CONFIG:-$GENERATOR_DIR/config.toml}"

mkdir -p "$LOG_DIR" "$REFERENCE_DIR" "$OUTPUT_DIR"

# Load database credentials from .env
if [ -f "$SHELFWISE_HOME/.env" ]; then
    source "$SHELFWISE_HOME/.env"
else
    echo "ERROR: .env file not found at $SHELFWISE_HOME/.env"
    exit 1
fi

export PGHOST="${POSTGRES_HOST:-localhost}"
export PGPORT="${POSTGRES_PORT:-5432}"
export PGDATABASE="${POSTGRES_DB:-shelfwise}"
export PGUSER="${POSTGRES_USER:-postgres}"
export PGPASSWORD="${POSTGRES_PASSWORD}"

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

log() {
    local message="[$(date '+%Y-%m-%d %H:%M:%S')] $*"
    echo "$message" | tee -a "$LOG_FILE"
}

error_exit() {
    log "ERROR: $1"
    exit 1
}

# ============================================================================
# PREREQUISITES CHECK
# ============================================================================

log "ShelfWise Nightly Import Starting"

# Check database connection
if ! psql -c "SELECT 1" >/dev/null 2>&1; then
    error_exit "Cannot connect to database. Check credentials in .env"
fi

# Check generator
if [ ! -f "$GENERATOR_DIR/Cargo.toml" ]; then
    error_exit "Generator not found: $GENERATOR_DIR"
fi

# ============================================================================
# PARSE COMMAND LINE ARGUMENTS
# ============================================================================

SPECIFIC_DATE=""
while [[ $# -gt 0 ]]; do
    case "$1" in
        --date)
            SPECIFIC_DATE="$2"
            shift 2
            ;;
        --config)
            GENERATOR_CONFIG="$2"
            shift 2
            ;;
        --help|-h)
            echo "Usage: $0 [--date YYYY-MM-DD] [--config /path/to/config.toml]"
            echo "  --date    Specific date to generate (default: auto-detect gaps)"
            echo "  --config  Generator config file (default: generator/config.toml)"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Make config path absolute if relative
if [[ ! "$GENERATOR_CONFIG" = /* ]]; then
    GENERATOR_CONFIG="$(pwd)/$GENERATOR_CONFIG"
fi

# ============================================================================
# DETERMINE TARGET DATE(S)
# ============================================================================

if [ -n "$SPECIFIC_DATE" ]; then
    log "Manual mode: Generating data for $SPECIFIC_DATE"
    DATES_TO_GENERATE=("$SPECIFIC_DATE")
else
    # Auto mode: detect gaps
    if date -v-1d >/dev/null 2>&1; then
        YESTERDAY=$(date -v-1d +%Y-%m-%d)
    else
        YESTERDAY=$(date -d "yesterday" +%Y-%m-%d)
    fi

    LAST_DATE=$(psql -t -c "SELECT MAX(date) FROM sales_daily;" 2>/dev/null | xargs)

    if [ -z "$LAST_DATE" ]; then
        error_exit "No data in database. Run initial load first."
    fi

    log "Last date: $LAST_DATE, Target: $YESTERDAY"

    if [[ ! "$LAST_DATE" < "$YESTERDAY" ]]; then
        log "✓ Database is up to date."
        exit 0
    fi

    # Get missing dates
    DATES_TO_GENERATE=()
    while IFS= read -r d; do
        [ -n "$d" ] && DATES_TO_GENERATE+=("$d")
    done < <(psql -t -c "SELECT TO_CHAR(date, 'YYYY-MM-DD') FROM generate_series('$LAST_DATE'::date + 1, '$YESTERDAY'::date, '1 day'::interval) date;" | xargs -n1)

    if [ ${#DATES_TO_GENERATE[@]} -eq 0 ]; then
        log "✓ No dates to generate."
        exit 0
    fi

    log "Missing dates: ${DATES_TO_GENERATE[*]}"
fi

# ============================================================================
# GENERATE AND IMPORT EACH DATE
# ============================================================================

for TARGET_DATE in "${DATES_TO_GENERATE[@]}"; do
    log "Processing $TARGET_DATE..."

    # Export reference data INSIDE loop so each day sees customers from previous day
    rm -rf "$REFERENCE_DIR"/* 2>/dev/null || true
    mkdir -p "$REFERENCE_DIR"

    # Export products and stores (static reference data - ensures generator uses same SKUs/store_ids)
    psql -q -c "\COPY products TO '$REFERENCE_DIR/products.csv' WITH CSV HEADER"
    psql -q -c "\COPY stores TO '$REFERENCE_DIR/stores.csv' WITH CSV HEADER"

    # Export with boolean conversion (PostgreSQL outputs t/f, Rust expects true/false)
    psql -q -c "\COPY (SELECT customer_id, email, phone, first_name, last_name, age_bracket, household_size, income_bracket, primary_store_id, primary_city, home_latitude, home_longitude, CASE WHEN loyalty_member THEN 'true' ELSE 'false' END as loyalty_member, loyalty_tier, loyalty_join_date, loyalty_points, preferred_shopping_time, avg_basket_size, price_sensitivity, customer_segment, created_date, last_purchase_date, total_lifetime_value, total_visits, CASE WHEN has_online_account THEN 'true' ELSE 'false' END as has_online_account, CASE WHEN prefers_online THEN 'true' ELSE 'false' END as prefers_online FROM customers) TO '$REFERENCE_DIR/customers.csv' WITH CSV HEADER"
    psql -q -c "\COPY (SELECT address_id, customer_id, address_type, CASE WHEN is_default THEN 'true' ELSE 'false' END as is_default, street_address, apartment_unit, city, state, zip_code, latitude, longitude, delivery_instructions, CASE WHEN has_doorman THEN 'true' ELSE 'false' END as has_doorman, CASE WHEN requires_signature THEN 'true' ELSE 'false' END as requires_signature, REPLACE(created_at::text, ' ', 'T') as created_at, REPLACE(last_used_at::text, ' ', 'T') as last_used_at, delivery_count FROM customer_addresses) TO '$REFERENCE_DIR/customer_addresses.csv' WITH CSV HEADER"
    psql -q -c "\COPY (SELECT driver_id, first_name, last_name, phone, email, driver_type, employment_status, primary_store_id, service_radius_miles, service_cities, vehicle_type, vehicle_capacity_items, CASE WHEN has_insulated_bags THEN 'true' ELSE 'false' END as has_insulated_bags, total_deliveries, avg_rating, on_time_delivery_pct, acceptance_rate, cancellation_rate, CASE WHEN is_available THEN 'true' ELSE 'false' END as is_available, current_latitude, current_longitude, REPLACE(last_location_update::text, ' ', 'T') as last_location_update, hire_date, last_delivery_date, base_pay_per_delivery, mileage_rate, avg_tips_per_delivery FROM delivery_drivers) TO '$REFERENCE_DIR/delivery_drivers.csv' WITH CSV HEADER"

    # Clean output directory
    rm -rf "$OUTPUT_DIR"/* 2>/dev/null || true
    mkdir -p "$OUTPUT_DIR"

    # Run generator with --reference-dir (loads existing customers/drivers)
    cd "$GENERATOR_DIR"

    GEN_LOG="$LOG_DIR/generator-$TARGET_DATE.log"
    if ! cargo run --release -- \
        --config "$GENERATOR_CONFIG" \
        --reference-dir "$REFERENCE_DIR" \
        --start-date "$TARGET_DATE" \
        --end-date "$TARGET_DATE" \
        --output "$OUTPUT_DIR" \
        --continue > "$GEN_LOG" 2>&1; then

        log "Generator failed. See $GEN_LOG for details:"
        tail -20 "$GEN_LOG" | tee -a "$LOG_FILE"
        error_exit "Generator failed for $TARGET_DATE"
    fi

    cd "$SHELFWISE_HOME"
    log "  Generator complete, offsetting IDs..."

    # Offset IDs to avoid conflicts with existing data

    # Get all max IDs ONCE before any offsets
    MAX_TXN_ID=$(psql -t -c "SELECT COALESCE(MAX(transaction_id), 0) FROM transactions;" 2>/dev/null | xargs)
    MAX_WASTE_ID=$(psql -t -c "SELECT COALESCE(MAX(waste_id), 0) FROM waste_spoilage;" 2>/dev/null | xargs)
    MAX_TICKET_ID=$(psql -t -c "SELECT COALESCE(MAX(ticket_id), 0) FROM tickets;" 2>/dev/null | xargs)
    MAX_SHIPMENT_ID=$(psql -t -c "SELECT COALESCE(MAX(shipment_id), 0) FROM supplier_shipments;" 2>/dev/null | xargs)
    MAX_CHANGE_ID=$(psql -t -c "SELECT COALESCE(MAX(change_id), 0) FROM price_changes;" 2>/dev/null | xargs)
    MAX_ASSIGN_ID=$(psql -t -c "SELECT COALESCE(MAX(assignment_id), 0) FROM delivery_assignments;" 2>/dev/null | xargs)

    log "  Max IDs: txn=$MAX_TXN_ID waste=$MAX_WASTE_ID ticket=$MAX_TICKET_ID"

    # Use a single Python script to offset all files (handles quoted commas correctly)
    # NOTE: Generator outputs CSVs WITH headers, but we use column indices as backup
    python3 - "$OUTPUT_DIR" "${MAX_TXN_ID:-0}" "${MAX_WASTE_ID:-0}" "${MAX_TICKET_ID:-0}" "${MAX_SHIPMENT_ID:-0}" "${MAX_CHANGE_ID:-0}" "${MAX_ASSIGN_ID:-0}" << 'PYEOF'
import csv
import sys
import os

output_dir = sys.argv[1]
max_txn = int(sys.argv[2])
max_waste = int(sys.argv[3])
max_ticket = int(sys.argv[4])
max_shipment = int(sys.argv[5])
max_change = int(sys.argv[6])
max_assign = int(sys.argv[7])

def offset_csv_by_index(filepath, col_indices, offsets):
    """Apply offsets to columns by index (0-based). Handles CSVs with or without headers."""
    if not os.path.exists(filepath):
        return False

    with open(filepath, 'r', newline='') as f:
        reader = csv.reader(f)
        rows = list(reader)

    if not rows:
        return False

    # Check if first row looks like a header (first value is not numeric)
    has_header = False
    try:
        int(rows[0][col_indices[0]])
    except (ValueError, IndexError):
        has_header = True

    start_row = 1 if has_header else 0
    modified = 0

    for row in rows[start_row:]:
        for col_idx, offset in zip(col_indices, offsets):
            if col_idx < len(row) and row[col_idx]:
                try:
                    row[col_idx] = str(int(row[col_idx]) + offset)
                    modified += 1
                except (ValueError, TypeError):
                    pass

    with open(filepath, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    return modified > 0

# Apply offsets - column 0 is the ID for most files
# transactions.csv: col 0 = transaction_id
offset_csv_by_index(os.path.join(output_dir, 'transactions.csv'), [0], [max_txn])

# transaction_line_items.csv: col 0 = transaction_id
offset_csv_by_index(os.path.join(output_dir, 'transaction_line_items.csv'), [0], [max_txn])

# waste_spoilage.csv: col 0 = waste_id
offset_csv_by_index(os.path.join(output_dir, 'waste_spoilage.csv'), [0], [max_waste])

# tickets.csv: col 0 = ticket_id
offset_csv_by_index(os.path.join(output_dir, 'tickets.csv'), [0], [max_ticket])

# supplier_shipments.csv: col 0 = shipment_id
offset_csv_by_index(os.path.join(output_dir, 'supplier_shipments.csv'), [0], [max_shipment])

# price_changes.csv: col 0 = change_id
offset_csv_by_index(os.path.join(output_dir, 'price_changes.csv'), [0], [max_change])

# delivery_assignments.csv: col 0 = assignment_id, col 1 = transaction_id
offset_csv_by_index(os.path.join(output_dir, 'delivery_assignments.csv'), [0, 1], [max_assign, max_txn])
PYEOF

    log "  ID offsets applied, extracting new customers/drivers/addresses..."

    # Extract NEW customers/drivers/addresses (IDs greater than max in database)
    NEW_CUST=0
    NEW_ADDRS=0
    NEW_DRIVERS=0

    if [ -f "$OUTPUT_DIR/customers.csv" ]; then
        MAX_CUST_ID=$(psql -t -c "SELECT COALESCE(MAX(customer_id), 0) FROM customers;" 2>/dev/null | xargs)
        MAX_CUST_ID=${MAX_CUST_ID:-0}
        head -1 "$OUTPUT_DIR/customers.csv" > "$OUTPUT_DIR/customers_import.csv"
        awk -F',' -v max="$MAX_CUST_ID" 'NR>1 && $1 > max' "$OUTPUT_DIR/customers.csv" >> "$OUTPUT_DIR/customers_import.csv"
        NEW_CUST=$(tail -n +2 "$OUTPUT_DIR/customers_import.csv" 2>/dev/null | wc -l | xargs)
        log "    Found $NEW_CUST new customers (max ID was $MAX_CUST_ID)"
    fi

    # Extract NEW customer_addresses (transactions reference delivery_address_id)
    if [ -f "$OUTPUT_DIR/customer_addresses.csv" ]; then
        MAX_ADDR_ID=$(psql -t -c "SELECT COALESCE(MAX(address_id), 0) FROM customer_addresses;" 2>/dev/null | xargs)
        MAX_ADDR_ID=${MAX_ADDR_ID:-0}
        head -1 "$OUTPUT_DIR/customer_addresses.csv" > "$OUTPUT_DIR/addresses_import.csv"
        awk -F',' -v max="$MAX_ADDR_ID" 'NR>1 && $1 > max' "$OUTPUT_DIR/customer_addresses.csv" >> "$OUTPUT_DIR/addresses_import.csv"
        NEW_ADDRS=$(tail -n +2 "$OUTPUT_DIR/addresses_import.csv" 2>/dev/null | wc -l | xargs)
        log "    Found $NEW_ADDRS new addresses (max ID was $MAX_ADDR_ID)"
    fi

    if [ -f "$OUTPUT_DIR/delivery_drivers.csv" ]; then
        MAX_DRIVER_ID=$(psql -t -c "SELECT COALESCE(MAX(driver_id), 0) FROM delivery_drivers;" 2>/dev/null | xargs)
        MAX_DRIVER_ID=${MAX_DRIVER_ID:-0}

        head -1 "$OUTPUT_DIR/delivery_drivers.csv" > "$OUTPUT_DIR/drivers_import.csv"
        awk -F',' -v max="$MAX_DRIVER_ID" 'NR>1 && $1 > max' "$OUTPUT_DIR/delivery_drivers.csv" >> "$OUTPUT_DIR/drivers_import.csv"
        NEW_DRIVERS=$(tail -n +2 "$OUTPUT_DIR/drivers_import.csv" 2>/dev/null | wc -l | xargs)
        log "    Found $NEW_DRIVERS new drivers (max ID was $MAX_DRIVER_ID)"
    fi

    # Import to database
    log "  Importing to database..."

    # Import new customers FIRST (transactions reference them)
    if [ -f "$OUTPUT_DIR/customers_import.csv" ] && [ $(wc -l < "$OUTPUT_DIR/customers_import.csv") -gt 1 ]; then
        log "    Importing customers..."
        if ! psql -q -c "\COPY customers FROM '$OUTPUT_DIR/customers_import.csv' WITH CSV HEADER" 2>&1; then
            log "    WARNING: Customer import failed"
        fi
    fi

    # Import new addresses AFTER customers but BEFORE transactions (transactions reference delivery_address_id)
    if [ -f "$OUTPUT_DIR/addresses_import.csv" ] && [ $(wc -l < "$OUTPUT_DIR/addresses_import.csv") -gt 1 ]; then
        log "    Importing addresses..."
        if ! psql -q -c "\COPY customer_addresses FROM '$OUTPUT_DIR/addresses_import.csv' WITH CSV HEADER" 2>&1; then
            log "    WARNING: Address import failed"
        fi
    fi

    # Import new drivers BEFORE delivery_assignments
    if [ -f "$OUTPUT_DIR/drivers_import.csv" ] && [ $(wc -l < "$OUTPUT_DIR/drivers_import.csv") -gt 1 ]; then
        log "    Importing drivers..."
        if ! psql -q -c "\COPY delivery_drivers FROM '$OUTPUT_DIR/drivers_import.csv' WITH CSV HEADER" 2>&1; then
            log "    WARNING: Driver import failed"
        fi
    fi

    # Import daily data (after customers/drivers are in place)
    TABLES_IMPORTED=0
    for table in sales_daily inventory_daily transactions transaction_line_items \
                 returns_daily delivery_assignments waste_spoilage tickets \
                 supplier_shipments price_changes; do
        csv_file="$OUTPUT_DIR/${table}.csv"
        if [ -f "$csv_file" ] && [ $(wc -l < "$csv_file") -gt 0 ]; then
            first_field=$(head -1 "$csv_file" | cut -d',' -f1)
            if [[ "$first_field" =~ ^[0-9]+$ ]]; then
                if ! psql -q -c "\COPY $table FROM '$csv_file' WITH CSV" 2>&1; then
                    log "    WARNING: Failed to import $table"
                fi
            else
                if ! psql -q -c "\COPY $table FROM '$csv_file' WITH CSV HEADER" 2>&1; then
                    log "    WARNING: Failed to import $table (with header)"
                fi
            fi
            TABLES_IMPORTED=$((TABLES_IMPORTED + 1))
        fi
    done

    log "  ✓ $TARGET_DATE: ${TABLES_IMPORTED} tables, ${NEW_CUST} new customers, ${NEW_ADDRS} new addresses, ${NEW_DRIVERS} new drivers"
done

# ============================================================================
# CLEANUP AND SUMMARY
# ============================================================================

rm -rf "$OUTPUT_DIR" "$REFERENCE_DIR" 2>/dev/null || true

log "✓ Completed ${#DATES_TO_GENERATE[@]} date(s)"

exit 0