# C360 Retail Fashion Database - Enterprise Scale Complete Solution

This directory contains a comprehensive, production-ready solution for generating a realistic **50,000 customer enterprise dataset** with contextually accurate reviews and creating a fully functional C360 Retail Fashion database.

## 📁 Files

- **`generate_complete_dataset.py`** - **UNIFIED** enterprise-scale data generator (50k customers + reviews)
- **`schema_alignment_and_load_v3.sql`** - Complete database setup, loading, and constraint implementation
- **`requirements.txt`** - Python dependencies
- **`postgres/`** - Generated CSV data files (23 files total)

## 🚀 Quick Start - Enterprise Scale (50K Customers)

### Step 1: Install Dependencies
```bash
pip3 install -r requirements.txt
```

### Step 2: Generate Complete Enterprise Dataset
```bash
cd .data/c360-retail-fashion
python3 generate_complete_dataset.py
```
This creates:
- All CSV files in `postgres/` directory with foreign key compatibility
- **50,000 customers** with **~700K total records** across all tables
- **91k+ contextually accurate reviews** as CSV data

### Step 3: Load into Database
```bash
# Load all data including reviews
psql -d your_database -f schema_alignment_and_load_v3.sql
```

**Complete Setup**: Schema alignment, data loading, foreign keys, data quality constraints, and reviews with full verification.

## 📊 Generated Data Overview - Large Scale Dataset

### Core Database Tables (11)
- **Brands** (30-50): Fashion brands with tiers and metadata
- **Categories** (10-20): Product categories with hierarchy
- **Products** (500-1000): Fashion products with realistic attributes
- **Product Variants** (3-6 per product): Size/color variations with inventory
- **Customers** (50,000): Realistic demographic profiles - **10x Scale**
- **Customer Addresses** (75,000+): US geographic distribution (1-2 per customer)
- **Orders** (120,000-150,000): E-commerce transactions - **10x Scale**
- **Order Items** (300,000+): Line items with proper pricing - **10x Scale**
- **Returns** (13,000+): Return processing workflow (10-12% of orders)
- **Return Items** (18,000+): Individual returned item tracking (1-2 per return)
- **Reviews** (91,000+): Contextually accurate customer reviews with sentiment analysis

### Additional Analytics Files (12)
- Campaign responses and marketing data
- Customer service interactions
- Email engagement metrics
- Loyalty program activities and profiles
- Website sessions and customer journey data
- Social mentions and feedback data

## ✨ Key Features

### 🔗 Complete Database Implementation
- **8 Foreign Key Constraints**: Full referential integrity
- **6 Data Quality Constraints**: Business rule enforcement
- **Primary Keys**: Auto-increment and unique identification
- **Data Type Alignment**: Foreign key compatibility guaranteed

### 📈 Realistic Data Generation - Enterprise Scale
- **Large Scale Dataset**: 50,000 customers with 120K-150K orders
- **Retail-Appropriate Catalog**: Limited brands/products serving many customers
- **Statistical Distributions**: Match real-world e-commerce patterns
- **Demographic Accuracy**: Realistic customer age, gender, acquisition channels
- **Temporal Consistency**: Logical date relationships across all entities
- **Business Logic**: Returns only from delivered orders, proper pricing calculations

### 🎯 Data Quality Assurance
- **Zero Orphaned Records**: All foreign keys reference valid parent records
- **Reproducible Results**: Seeded randomization (seed=42)
- **Comprehensive Validation**: Built-in integrity checks and violation reporting
- **Production Ready**: Handles edge cases and data quality issues

## 📁 Generated Files Structure

After running the generator, you'll find:

### Core Database Files (11)
```
postgres/
├── brands.csv                    # Brand master data
├── categories.csv               # Product categories
├── products.csv                 # Product catalog
├── product_variants.csv         # Size/color/inventory
├── customers.csv               # Customer profiles
├── customer_addresses.csv      # Customer locations
├── orders.csv                  # Order transactions
├── order_items.csv            # Order line items
├── returns.csv                # Return requests
├── return_items.csv           # Individual returns
└── reviews.csv                # Customer reviews (91k+ records)
```

### Analytics & Extended Data Files (12)
```
postgres/
├── campaign_responses.csv         # Marketing campaign results
├── campaigns.csv                  # Marketing campaigns
├── customer_service_interactions.csv  # Support tickets
├── email_engagement.csv           # Email marketing metrics
├── loyalty_activities.csv         # Loyalty program actions
├── loyalty_profiles.csv          # Customer loyalty data
├── session_summary.csv           # Website session aggregates
├── social_mentions.csv           # Social media references
├── staging_customer_sessions.csv  # Raw session data
├── staging_order_items_simple.csv # Simplified order data
└── website_sessions.csv          # Individual website visits
```

## 🔧 Technical Specifications

### Foreign Key Relationships Implemented
- `orders.customer_id` → `customers.customer_id`
- `returns.customer_id` → `customers.customer_id`
- `returns.order_id` → `orders.order_id`
- `order_items.order_id` → `orders.order_id`
- `order_items.product_id` → `products.product_id`
- `customer_addresses.customer_id` → `customers.customer_id`
- `return_items.order_item_id` → `order_items.order_item_id`
- `product_variants.product_id` → `products.product_id`

### Data Quality Constraints
- Positive amounts and quantities across all financial fields
- Valid sustainability scores (0-100)
- Non-negative stock quantities and pricing
- Referential integrity maintained throughout

## 💡 Usage Examples

### Generate Fresh Data
```bash
# Generate new dataset including reviews
python generate_complete_dataset.py

# Load into PostgreSQL with full constraints including reviews
psql -d ecommerce_db -f schema_alignment_and_load_v3.sql
```

### Verify Data Quality
The loading script automatically runs verification checks and reports:
- Row counts for all tables
- Foreign key constraint status
- Data integrity violation counts (should all be zero)

## 📋 Requirements

- **Python 3.7+** with faker and numpy libraries
- **PostgreSQL 10+** for database operations
- **~500MB disk space** for generated CSV files (50K customer dataset)

## 🎯 Production Ready Features

This solution is designed for production use with:
- **Enterprise Scale**: 50,000+ customers with proportional transaction volume
- **Realistic Retail Model**: Limited catalog serving large customer base
- Comprehensive error handling and validation
- Detailed logging and progress reporting
- Scalable data generation (easily adjust volumes)
- Complete database constraint implementation
- Ready for integration with analytics tools and BI platforms

---

**Total Database Coverage**: 11 core tables with 8 foreign keys, 6 data quality constraints, and 22 CSV datasets for comprehensive retail analytics.
**Scale**: 50,000 customers generating ~700,000 total records across all tables with realistic retail catalog proportions including 91k+ contextual reviews.