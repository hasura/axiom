# C360 Retail Fashion Database - Complete Solution

This directory contains a comprehensive, production-ready solution for generating realistic data and creating a fully functional C360 Retail Fashion database with proper schema, foreign keys, data quality constraints, and verification.

## 📁 Files

- **`generate_realistic_data_v2.py`** - Advanced data generator with foreign key compatibility
- **`schema_alignment_and_load_v3.sql`** - Complete database setup, loading, and constraint implementation
- **`requirements.txt`** - Python dependencies
- **`postgres/`** - Generated CSV data files (22 files total)

## 🚀 Quick Start

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Generate Data
```bash
cd .data/c360-retail-fashion
python generate_realistic_data_v2.py
```
This creates all CSV files in the `postgres/` directory with foreign key compatible data types.

### Step 3: Create Database & Load Data
```bash
psql -d your_database -f schema_alignment_and_load_v3.sql
```
This script handles everything:
- Schema alignment and data type fixes
- Sequential data loading (respecting dependencies)
- Primary key and foreign key constraint implementation
- Data quality constraint enforcement
- Comprehensive verification and reporting

## 📊 Generated Data Overview

### Core Database Tables (10)
- **Brands** (30-50): Fashion brands with tiers and metadata
- **Categories** (10-20): Product categories with hierarchy
- **Products** (500-1000): Fashion products with realistic attributes
- **Product Variants** (3-6 per product): Size/color variations with inventory
- **Customers** (5000): Realistic demographic profiles
- **Customer Addresses** (1-2 per customer): US geographic distribution
- **Orders** (12000-15000): E-commerce transactions
- **Order Items** (25000-35000): Line items with proper pricing
- **Returns** (10-12% of orders): Return processing workflow
- **Return Items** (1-2 per return): Individual returned item tracking

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

### 📈 Realistic Data Generation
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

### Core Database Files (10)
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
└── return_items.csv           # Individual returns
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
# Generate new dataset
python generate_realistic_data_v2.py

# Load into PostgreSQL with full constraints
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
- **~100MB disk space** for generated CSV files

## 🎯 Production Ready Features

This solution is designed for production use with:
- Comprehensive error handling and validation
- Detailed logging and progress reporting
- Scalable data generation (easily adjust volumes)
- Complete database constraint implementation
- Ready for integration with analytics tools and BI platforms

---

**Total Database Coverage**: 10 core tables with 8 foreign keys, 6 data quality constraints, and 22 CSV datasets for comprehensive retail analytics.