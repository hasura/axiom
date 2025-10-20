# FinIQ MongoDB Integration

This directory contains MongoDB integration for the FinIQ project, providing complementary unstructured data to enhance the PostgreSQL transactional data.

## Overview

The MongoDB database contains the following collections:

- **customer_profiles**: Customer profile documents with personal information and spending patterns
- **merchant_risk_profiles**: Merchant risk assessment profiles with compliance and fraud metrics  
- **fraud_alerts**: Fraud detection alerts and investigation status
- **transaction_notes**: Investigation notes and comments related to transactions
- **audit_logs**: System audit logs and user activity tracking

## Files

- `generate_mongo_data.py` - Python script to generate sample MongoDB data
- `load_mongo_data.py` - Python script to load JSON data into MongoDB
- `init/01-init-db.js` - MongoDB initialization script

## Setup Instructions

### Automatic Data Loading (Recommended)

The MongoDB service now automatically loads sample data during container initialization, similar to PostgreSQL:

1. **Ensure JSON data files exist** (pre-generated and included):
   ```
   mongodb/data/
   ├── customer_profiles.json
   ├── merchant_risk_profiles.json
   ├── fraud_alerts.json
   ├── transaction_notes.json
   └── audit_logs.json
   ```

2. **Start MongoDB service** - data loads automatically:
   ```bash
   cd /path/to/demos/FinIQ
   docker compose up mongodb -d
   ```

### Manual Data Generation (Optional)

If you need to regenerate sample data:

```bash
cd .data/finiq/mongodb
python3 generate_mongo_data.py
```

### Legacy Manual Loading (Not Required)

The old manual process is no longer needed but still available:

```bash
pip install pymongo
python3 load_mongo_data.py
```

## Data Schema

### Customer Profiles
- Customer personal information
- Card details (last 4 digits)
- Address and contact information
- Spending patterns and preferences
- Risk scoring

### Merchant Risk Profiles
- Risk assessment metrics
- Chargeback and fraud statistics
- Compliance status
- Historical risk assessments

### Fraud Alerts
- Transaction-based fraud detection
- Alert severity and status
- Investigation workflow
- Metadata for analysis

### Transaction Notes
- Investigation notes and comments
- Multi-user collaboration
- Priority and status tracking
- Tagged categorization

### Audit Logs
- System activity tracking
- User action logging
- Resource access monitoring
- Performance metrics

## Connection Details

- **Host**: localhost
- **Port**: 27017
- **Database**: finiq
- **Authentication**: admin/finiq123
- **Connection URI**: `mongodb://admin:finiq123@localhost:27017/finiq?authSource=admin`

## Hasura Connector

The MongoDB data is accessible through Hasura DDN via the `fin_intel_mongo` connector:

- **Connector Port**: 4649
- **GraphQL Endpoint**: Available through the main engine at port 3281

## Sample Queries

Once the system is running, you can query MongoDB collections through the GraphQL API alongside PostgreSQL data for comprehensive financial intelligence analysis.

## Troubleshooting

1. **Connection Issues**: Ensure MongoDB is running and accessible at port 27017
2. **Data Loading**: Verify PostgreSQL data exists before generating MongoDB data (for foreign key references)
3. **Permissions**: Make sure the `finiq_app` user has proper read/write permissions
4. **Indexes**: The initialization script creates indexes automatically for optimal performance

## Environment Variables

Key environment variables for MongoDB integration:

```
MONGO_INITDB_ROOT_USERNAME=admin
MONGO_INITDB_ROOT_PASSWORD=finiq123
MONGO_INITDB_DATABASE=finiq
APP_FIN_INTEL_MONGO_DATABASE_URI=mongodb://admin:finiq123@host.docker.internal:27017/finiq?authSource=admin