# C360 Retail Fashion Database Setup

Complete standalone database setup for the C360 Retail Fashion analytics platform.

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose installed
- At least 4GB available RAM
- Port 5433 and 8080 available (connects to existing axiomretailfashion_postgres)

### 1. Start the Database
```bash
cd .data/c360-retail-fashion
docker-compose up -d
```

This will:
- ✅ Connect to existing PostgreSQL database on port `5433` (axiomretailfashion_postgres)
- ✅ Reference the `retail_fashion` database with complete schema and data
- ✅ Start PgAdmin web interface on port `8080`

### 2. Access the Database

**Direct PostgreSQL Connection:**
```bash
# Connect via psql (to existing database)
psql -h localhost -p 5433 -U postgres -d retail_fashion

# Connection details:
Host: localhost
Port: 5433
Database: retail_fashion
Username: postgres
Password: hbGciOiJIUzI1NiIsInR5cCI6IkpX (from existing setup)
```

**Web Interface (PgAdmin):**
- URL: http://localhost:8080
- Email: admin@admin.com
- Password: admin

## 📊 Database Contents

### Core Tables (with data)
- `brands` - Fashion brands (30-50 records)
- `categories` - Product categories with hierarchy
- `products` - Product catalog (500-1000 products)
- `product_variants` - Size/color variants (3k-6k records)
- `customers` - Customer profiles (50,000 customers)
- `customer_addresses` - Customer shipping addresses
- `orders` - Order transactions (120k-150k orders)
- `order_items` - Line items for orders
- `returns` - Return requests and processing
- `return_items` - Individual returned items
- `reviews` - Product reviews with ratings
- `social_mentions` - Social media interactions
- `website_sessions` - Web analytics sessions
- `style_similarity_matches` - ML recommendation data

### Analytics Views
```sql
-- View table row counts
SELECT * FROM table_row_counts;

-- Sample queries
SELECT COUNT(*) FROM customers WHERE account_status = 'active';
SELECT brand, COUNT(*) FROM products GROUP BY brand ORDER BY count DESC;
SELECT * FROM style_similarity_matches LIMIT 10;
```

## 🔄 Data Generation

### Generate Fresh Data
```bash
# Generate new dataset (optional)
cd .data/c360-retail-fashion
python3 generate_complete_dataset.py

# Restart database to load new data
docker-compose down
docker-compose up -d
```

### Manual Data Loading
```bash
# If you need to reload data manually
docker exec -i axiomretailfashion_postgres psql -U postgres -d retail_fashion < sql/load_data.sql
```

## 🛠️ Customization

### Change Database Credentials
Edit `compose.yaml`:
```yaml
environment:
  POSTGRES_DB: your_database_name
  POSTGRES_USER: your_username
  POSTGRES_PASSWORD: your_password
```

### Add Custom Tables
1. Add schema to `sql/schema.sql`
2. Add data loading to `sql/load_data.sql`
3. Restart: `docker-compose down && docker-compose up -d`

### External Database Server
Use the SQL files with any PostgreSQL server:
```bash
# On your PostgreSQL server
createdb retail_fashion
psql -d retail_fashion -f sql/schema.sql
psql -d retail_fashion -f sql/load_data.sql
```

## 📁 File Structure
```
.data/c360-retail-fashion/
├── compose.yaml              # Docker Compose setup
├── sql/
│   ├── schema.sql            # Complete database schema
│   └── load_data.sql         # Data loading script
├── postgres/                 # CSV data files
│   ├── brands.csv
│   ├── customers.csv
│   ├── products.csv
│   └── ... (all data files)
├── generate_complete_dataset.py  # Data generator
└── README.md                 # This file
```

## 🔧 Troubleshooting

### Database Won't Start
```bash
# Check if port 5433 is available
lsof -i :5433

# View logs
docker-compose logs postgres
```

### Data Loading Issues
```bash
# Check data loading logs
docker-compose logs postgres | grep COPY

# Manual verification
docker exec -it axiomretailfashion_postgres psql -U postgres -d retail_fashion -c "SELECT * FROM table_row_counts;"
```

### Reset Everything
```bash
# Complete reset
docker-compose down -v  # Removes volumes
docker-compose up -d    # Fresh start
```

## 📈 Performance Optimization

The database includes optimized indexes:
- Product searches: `brand`, `category_l1`
- Customer lookups: `email`
- Order queries: `customer_id`, `order_date`
- Analytics: `style_similarity_matches` indexes
- Review analysis: `customer_id`, `product_id`

## 🔐 Security Notes

**⚠️ This is a development setup with default credentials!**

For production:
1. Change all default passwords
2. Use environment variables for credentials
3. Enable SSL/TLS connections
4. Restrict network access
5. Regular backups

## 💾 Backup & Restore

### Backup
```bash
# Full database backup
docker exec axiomretailfashion_postgres pg_dump -U postgres retail_fashion > backup.sql

# Data-only backup
docker exec axiomretailfashion_postgres pg_dump -U postgres --data-only retail_fashion > data_backup.sql
```

### Restore
```bash
# Restore from backup
docker exec -i axiomretailfashion_postgres psql -U postgres retail_fashion < backup.sql
```

## 📞 Support

This database setup provides a complete C360 retail analytics platform with:
- ✅ 28 tables with proper relationships
- ✅ 700k+ total records across all tables
- ✅ ML recommendation system data
- ✅ Complete customer journey tracking
- ✅ Social media and web analytics
- ✅ Returns and review management

Perfect for development, testing, demos, and analytics experimentation!