#!/usr/bin/env python3
"""
Due Diligence Demo Data Generator
--------------------------------
Generates realistic financial and operational data for a manufacturing company
with built-in seasonality, growth trends, and realistic patterns.
"""

import os
import csv
import random
import datetime
import math
import numpy as np
import pandas as pd
from faker import Faker

# Set random seed for reproducibility
random.seed(42)
np.random.seed(42)
fake = Faker()
Faker.seed(42)

# Configuration
OUTPUT_DIR = "postgres"
START_DATE = datetime.date(2022, 1, 1)
END_DATE = datetime.date(2024, 12, 31)
COMPANY_NAME = "TechManufacture Inc."  # A mid-sized manufacturing company

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Utility functions
def generate_date_series(start_date, end_date, frequency='D'):
    """Generate a series of dates with the given frequency."""
    return pd.date_range(start=start_date, end=end_date, freq=frequency)

def add_trend(data, trend_strength=0.05):
    """Add a growth trend to the data."""
    trend = np.linspace(1, 1 + trend_strength * len(data), len(data))
    return data * trend

def add_seasonality(data, period=365, amplitude=0.2):
    """Add seasonal fluctuations to the data."""
    seasonal_component = amplitude * np.sin(2 * np.pi * np.arange(len(data)) / period)
    return data * (1 + seasonal_component)

def add_monthly_pattern(data, pattern):
    """Add monthly patterns - e.g., higher at month end."""
    result = data.copy()
    for i, value in enumerate(data):
        day_of_month = (i % 30) + 1
        multiplier = pattern.get(day_of_month, 1.0)
        result[i] = value * multiplier
    return result

def add_noise(data, noise_level=0.05):
    """Add random noise to data."""
    noise = np.random.normal(1, noise_level, len(data))
    return data * noise

def generate_realistic_timeseries(base_value, num_points, trend=0.1, 
                                 seasonality=0.15, seasonality_period=365,
                                 noise=0.03, monthly_pattern=None):
    """Generate a realistic time series with trend, seasonality, and noise."""
    # Start with constant base value
    data = np.ones(num_points) * base_value
    
    # Add trend
    if trend:
        data = add_trend(data, trend)
    
    # Add seasonality
    if seasonality:
        data = add_seasonality(data, seasonality_period, seasonality)
    
    # Add monthly patterns
    if monthly_pattern:
        data = add_monthly_pattern(data, monthly_pattern)
    
    # Add noise
    if noise:
        data = add_noise(data, noise)
    
    return data

# Financial data patterns
# The company experienced strong growth in 2022, followed by 
# market challenges in 2023, and is now in recovery mode in 2024
# These patterns will be reflected in the financial data

# Generate regions
def generate_regions():
    regions = [
        (1, "North America", "USA", "USD"),
        (2, "North America", "Canada", "CAD"),
        (3, "Europe", "Germany", "EUR"),
        (4, "Europe", "UK", "GBP"),
        (5, "Asia Pacific", "Japan", "JPY"),
        (6, "Asia Pacific", "Australia", "AUD"),
        (7, "LATAM", "Brazil", "BRL"),
        (8, "MEA", "UAE", "AED")
    ]
    
    with open(f"{OUTPUT_DIR}/regions.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["region_id", "region_name", "country", "currency_code"])
        writer.writerows(regions)
    
    return {r[0]: r for r in regions}

# Generate business units
def generate_business_units(regions):
    business_units = [
        (1, "Industrial Products", "IND", 1, "Sarah Johnson", True, "2010-05-15"),
        (2, "Consumer Electronics", "CONS", 1, "Michael Chen", True, "2012-08-22"),
        (3, "European Operations", "EUR", 3, "Anna Mueller", True, "2015-03-10"),
        (4, "Asia-Pacific Division", "APAC", 5, "Hiroshi Tanaka", True, "2018-11-05"),
        (5, "LATAM Division", "LATAM", 7, "Carlos Rodriguez", True, "2019-07-18"),
        (6, "R&D Division", "RND", 1, "Dr. Elizabeth Taylor", True, "2014-01-30")
    ]
    
    with open(f"{OUTPUT_DIR}/business_units.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["unit_id", "unit_name", "unit_code", "region_id", "director", "is_active", "established_date"])
        writer.writerows(business_units)
    
    return {bu[0]: bu for bu in business_units}

# Generate chart of accounts
def generate_chart_of_accounts():
    accounts = [
        # Assets
        ("1000", "Cash and Cash Equivalents", "Asset", "Current Asset", "Cash, checking accounts, and highly liquid investments", True),
        ("1100", "Accounts Receivable", "Asset", "Current Asset", "Amounts owed to the company by customers", True),
        ("1200", "Inventory", "Asset", "Current Asset", "Value of goods held for sale", True),
        ("1300", "Prepaid Expenses", "Asset", "Current Asset", "Expenses paid in advance", True),
        ("1400", "Property, Plant & Equipment", "Asset", "Fixed Asset", "Tangible long-term assets", True),
        ("1410", "Buildings", "Asset", "Fixed Asset", "Company-owned buildings", True),
        ("1420", "Machinery & Equipment", "Asset", "Fixed Asset", "Production machinery and equipment", True),
        ("1430", "Vehicles", "Asset", "Fixed Asset", "Company vehicles", True),
        ("1440", "Office Equipment", "Asset", "Fixed Asset", "Office furniture and equipment", True),
        ("1450", "Computer Equipment", "Asset", "Fixed Asset", "Computers, servers, and IT infrastructure", True),
        ("1500", "Accumulated Depreciation", "Asset", "Fixed Asset", "Accumulated depreciation on fixed assets", True),
        ("1600", "Intangible Assets", "Asset", "Intangible Asset", "Non-physical assets like patents and trademarks", True),
        ("1700", "Long-term Investments", "Asset", "Investment", "Investments held for more than one year", True),
        
        # Liabilities
        ("2000", "Accounts Payable", "Liability", "Current Liability", "Amounts owed to suppliers", True),
        ("2100", "Accrued Expenses", "Liability", "Current Liability", "Expenses incurred but not yet paid", True),
        ("2200", "Short-term Loans", "Liability", "Current Liability", "Loans due within one year", True),
        ("2300", "Income Tax Payable", "Liability", "Current Liability", "Income taxes owed to government", True),
        ("2400", "Long-term Debt", "Liability", "Long-term Liability", "Loans and financing due beyond one year", True),
        ("2500", "Bond Payable", "Liability", "Long-term Liability", "Bonds issued by the company", True),
        ("2600", "Lease Obligations", "Liability", "Long-term Liability", "Long-term lease commitments", True),
        ("2700", "Deferred Tax Liabilities", "Liability", "Long-term Liability", "Future tax obligations", True),
        
        # Equity
        ("3000", "Common Stock", "Equity", "Capital", "Common shares issued", True),
        ("3100", "Preferred Stock", "Equity", "Capital", "Preferred shares issued", True),
        ("3200", "Additional Paid-in Capital", "Equity", "Capital", "Amount paid in excess of par value", True),
        ("3300", "Retained Earnings", "Equity", "Earnings", "Accumulated earnings retained in the business", True),
        ("3400", "Treasury Stock", "Equity", "Capital", "Company's own stock that has been repurchased", True),
        ("3500", "Accumulated Other Comprehensive Income", "Equity", "Earnings", "Unrealized gains/losses not in income statement", True),
        
        # Revenue
        ("4000", "Product Sales - Industrial", "Revenue", "Operating Revenue", "Revenue from industrial product sales", True),
        ("4100", "Product Sales - Consumer", "Revenue", "Operating Revenue", "Revenue from consumer product sales", True),
        ("4200", "Service Revenue", "Revenue", "Operating Revenue", "Revenue from services provided", True),
        ("4300", "Licensing Revenue", "Revenue", "Operating Revenue", "Revenue from licensing intellectual property", True),
        ("4400", "Subscription Revenue", "Revenue", "Operating Revenue", "Revenue from subscription services", True),
        ("4500", "International Sales", "Revenue", "Operating Revenue", "Revenue from international markets", True),
        ("4900", "Sales Returns & Allowances", "Revenue", "Revenue Adjustment", "Reduction for customer returns and allowances", True),
        ("4950", "Sales Discounts", "Revenue", "Revenue Adjustment", "Reduction for early payment discounts", True),
        
        # Expenses
        ("5000", "Cost of Goods Sold", "Expense", "Direct Cost", "Direct costs of producing goods sold", True),
        ("5100", "Direct Materials", "Expense", "Direct Cost", "Raw materials used in production", True),
        ("5200", "Direct Labor", "Expense", "Direct Cost", "Labor directly involved in production", True),
        ("5300", "Manufacturing Overhead", "Expense", "Indirect Cost", "Indirect costs of production", True),
        ("5400", "Freight & Shipping", "Expense", "Selling Expense", "Costs of shipping products to customers", True),
        ("6000", "Salaries & Wages", "Expense", "Operating Expense", "Employee compensation", True),
        ("6100", "Employee Benefits", "Expense", "Operating Expense", "Health insurance and other benefits", True),
        ("6200", "Rent Expense", "Expense", "Operating Expense", "Office and facility rent", True),
        ("6300", "Utilities", "Expense", "Operating Expense", "Electricity, water, and other utilities", True),
        ("6400", "Office Supplies", "Expense", "Operating Expense", "Office consumables and supplies", True),
        ("6500", "Professional Services", "Expense", "Operating Expense", "Legal, accounting, and consulting fees", True),
        ("6600", "Marketing & Advertising", "Expense", "Selling Expense", "Promotion and advertising costs", True),
        ("6700", "Travel & Entertainment", "Expense", "Operating Expense", "Business travel and client entertainment", True),
        ("6800", "R&D Expenses", "Expense", "Operating Expense", "Research and development costs", True),
        ("6900", "Depreciation Expense", "Expense", "Non-cash Expense", "Allocation of asset costs over useful life", True),
        ("7000", "Amortization Expense", "Expense", "Non-cash Expense", "Allocation of intangible asset costs", True),
        ("7100", "Interest Expense", "Expense", "Financing Expense", "Interest on loans and debt", True),
        ("7200", "Income Tax Expense", "Expense", "Tax Expense", "Corporate income taxes", True),
        ("7300", "Insurance Expense", "Expense", "Operating Expense", "Business insurance premiums", True),
        ("7400", "Bad Debt Expense", "Expense", "Operating Expense", "Provision for uncollectible accounts", True),
        ("7500", "Foreign Exchange Loss", "Expense", "Other Expense", "Losses from currency exchange rate changes", True),
        ("8000", "Other Income", "Revenue", "Non-operating Income", "Income from sources other than main operations", True),
        ("8100", "Interest Income", "Revenue", "Non-operating Income", "Interest earned on investments", True),
        ("8200", "Dividend Income", "Revenue", "Non-operating Income", "Dividends received from investments", True),
        ("8300", "Gain on Sale of Assets", "Revenue", "Non-operating Income", "Gains from selling assets above book value", True),
        ("9000", "Other Expenses", "Expense", "Non-operating Expense", "Expenses not related to main operations", True),
        ("9100", "Loss on Sale of Assets", "Expense", "Non-operating Expense", "Losses from selling assets below book value", True),
        ("9200", "Restructuring Charges", "Expense", "Non-operating Expense", "Costs associated with reorganization", True),
        ("9900", "Prior Period Adjustments", "Expense", "Adjustment", "Corrections to prior period accounting", True),
    ]
    
    with open(f"{OUTPUT_DIR}/chart_of_accounts.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["account_number", "account_name", "account_type", "account_subtype", "description", "is_active"])
        writer.writerows(accounts)
    
    # Create a mapping of account names to their IDs for later use
    account_ids = {}
    for i, account in enumerate(accounts, 1):
        account_ids[account[1]] = i
    
    return account_ids

# Generate product categories
def generate_product_categories():
    categories = [
        (1, "Industrial Equipment", None, "Heavy machinery and industrial equipment"),
        (2, "Manufacturing Tools", None, "Tools used in manufacturing processes"),
        (3, "Electrical Components", None, "Electrical parts and components"),
        (4, "Consumer Electronics", None, "Electronics for consumer use"),
        (5, "Heavy Machinery", 1, "Large industrial machinery"),
        (6, "Assembly Line Equipment", 1, "Equipment for assembly lines"),
        (7, "Precision Tools", 2, "High-precision manufacturing tools"),
        (8, "Hand Tools", 2, "Manual tools for manufacturing"),
        (9, "Power Tools", 2, "Power-operated tools"),
        (10, "Circuit Components", 3, "Components for electrical circuits"),
        (11, "Wiring Systems", 3, "Electrical wiring and related components"),
        (12, "Control Systems", 3, "Systems to control electrical equipment"),
        (13, "Audio Equipment", 4, "Consumer audio devices"),
        (14, "Computer Peripherals", 4, "External devices for computers"),
        (15, "Smart Home Devices", 4, "Connected devices for home use")
    ]
    
    with open(f"{OUTPUT_DIR}/product_categories.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["category_id", "category_name", "parent_category_id", "description"])
        writer.writerows(categories)
    
    return {c[0]: c for c in categories}

# Generate products
def generate_products(categories, business_units):
    products = []
    product_id = 1
    
    # Industrial Equipment products (unit 1)
    industrial_products = [
        ("IND-1001", "Industrial Conveyor System", 5, 1, "Heavy-duty conveyor system for manufacturing", "2020-03-15", 12500.00, 18750.00, "Active", 1, 5, 10, 45),
        ("IND-1002", "Hydraulic Press Machine", 5, 1, "Precision hydraulic press for metalworking", "2020-05-20", 8900.00, 13500.00, "Active", 1, 3, 7, 60),
        ("IND-1003", "CNC Milling Machine", 5, 1, "Computer-controlled precision milling machine", "2021-02-10", 35000.00, 52500.00, "Active", 1, 2, 4, 75),
        ("IND-1004", "Automated Packaging System", 6, 1, "End-of-line packaging automation system", "2021-08-22", 18700.00, 28050.00, "Active", 1, 2, 5, 50),
        ("IND-1005", "Robotic Arm Assembly", 6, 1, "Programmable robotic arm for assembly operations", "2022-04-15", 42000.00, 63000.00, "Active", 1, 1, 3, 90),
        ("IND-1006", "Industrial Air Compressor", 5, 1, "High-capacity air compressor system", "2020-11-05", 7800.00, 11700.00, "Active", 2, 4, 8, 30),
        ("IND-1007", "Material Handling Robot", 6, 1, "Autonomous robot for material transport", "2023-01-18", 55000.00, 82500.00, "Development", 1, 1, 2, 120),
        ("IND-1008", "Industrial Laser Cutter", 5, 1, "Precision laser cutting system", "2022-09-30", 65000.00, 97500.00, "Active", 1, 1, 2, 60),
    ]
    products.extend(industrial_products)
    product_id += len(industrial_products)
    
    # Manufacturing Tools (unit 1)
    tool_products = [
        ("TOOL-2001", "Precision Caliper Set", 7, 1, "Digital precision measurement calipers", "2020-04-18", 180.00, 270.00, "Active", 10, 50, 100, 15),
        ("TOOL-2002", "Industrial Drill Set", 9, 1, "Heavy-duty drill set for manufacturing", "2020-06-12", 450.00, 675.00, "Active", 5, 20, 40, 20),
        ("TOOL-2003", "Pneumatic Screwdriver", 9, 1, "Air-powered precision screwdriver", "2021-03-25", 220.00, 330.00, "Active", 10, 30, 60, 15),
        ("TOOL-2004", "Digital Torque Wrench", 7, 1, "Programmable digital torque wrench", "2021-09-08", 380.00, 570.00, "Active", 5, 15, 30, 25),
        ("TOOL-2005", "Precision Measurement Kit", 7, 1, "Comprehensive measurement tools kit", "2022-02-20", 850.00, 1275.00, "Active", 3, 10, 20, 30),
        ("TOOL-2006", "Handheld Diagnostic Device", 7, 1, "Electronic diagnostic tool for equipment", "2022-11-15", 1200.00, 1800.00, "Active", 2, 8, 15, 45),
    ]
    products.extend(tool_products)
    product_id += len(tool_products)
    
    # Electrical Components (unit 1 and 2)
    electrical_products = [
        ("ELEC-3001", "Industrial Circuit Board", 10, 1, "Heavy-duty circuit board for industrial use", "2020-05-10", 120.00, 180.00, "Active", 20, 100, 200, 15),
        ("ELEC-3002", "Power Distribution Unit", 11, 1, "Industrial power distribution system", "2020-08-15", 950.00, 1425.00, "Active", 5, 15, 30, 30),
        ("ELEC-3003", "Programmable Logic Controller", 12, 1, "Advanced PLC for automation systems", "2021-04-20", 1800.00, 2700.00, "Active", 3, 10, 20, 45),
        ("ELEC-3004", "Motor Control Center", 12, 1, "Centralized motor control system", "2021-11-05", 4500.00, 6750.00, "Active", 1, 5, 10, 60),
        ("ELEC-3005", "Industrial Sensors Pack", 10, 1, "Set of various industrial sensors", "2022-05-25", 350.00, 525.00, "Active", 10, 30, 60, 20),
        ("ELEC-3006", "Smart Switch Panel", 12, 2, "IoT-enabled industrial switch panel", "2022-12-10", 750.00, 1125.00, "Active", 5, 15, 30, 25),
        ("ELEC-3007", "Industrial IoT Gateway", 12, 2, "Connectivity gateway for industrial IoT", "2023-03-18", 980.00, 1470.00, "Active", 3, 10, 20, 35),
    ]
    products.extend(electrical_products)
    product_id += len(electrical_products)
    
    # Consumer Products (unit 2)
    consumer_products = [
        ("CONS-4001", "Wireless Earbuds", 13, 2, "Premium wireless earbuds with noise cancellation", "2021-06-15", 45.00, 89.99, "Active", 50, 200, 500, 20),
        ("CONS-4002", "Smart Speaker System", 13, 2, "Voice-controlled smart speaker", "2021-09-22", 75.00, 149.99, "Active", 25, 100, 250, 25),
        ("CONS-4003", "Mechanical Keyboard", 14, 2, "High-performance mechanical keyboard", "2022-01-10", 55.00, 109.99, "Active", 20, 80, 160, 15),
        ("CONS-4004", "Wireless Mouse", 14, 2, "Ergonomic wireless mouse", "2022-03-20", 18.00, 39.99, "Active", 50, 150, 300, 10),
        ("CONS-4005", "Smart Home Hub", 15, 2, "Central controller for smart home devices", "2022-07-08", 85.00, 169.99, "Active", 15, 50, 100, 30),
        ("CONS-4006", "Security Camera System", 15, 2, "Wireless security cameras with monitoring", "2022-10-15", 120.00, 249.99, "Active", 10, 30, 60, 25),
        ("CONS-4007", "Smart Thermostat", 15, 2, "Energy-saving smart thermostat", "2023-02-05", 65.00, 129.99, "Active", 20, 60, 120, 15),
        ("CONS-4008", "Wireless Charging Pad", 14, 2, "Fast wireless charging pad for multiple devices", "2023-05-12", 25.00, 49.99, "Active", 30, 100, 200, 10),
        ("CONS-4009", "Bluetooth Headphones", 13, 2, "Over-ear Bluetooth headphones", "2023-08-20", 70.00, 139.99, "Active", 20, 80, 150, 20),
        ("CONS-4010", "Smart Light Bulb Kit", 15, 2, "Set of 4 color-changing smart bulbs", "2023-11-15", 40.00, 79.99, "Active", 25, 75, 150, 15),
    ]
    products.extend(consumer_products)
    product_id += len(consumer_products)
    
    # European Products (unit 3)
    european_products = [
        ("EUR-5001", "Industrial Control Panel", 12, 3, "EU-standard industrial control panel", "2021-05-10", 3200.00, 4800.00, "Active", 2, 5, 10, 40),
        ("EUR-5002", "European Manufacturing Kit", 7, 3, "Specialized tools for European standards", "2021-10-18", 1100.00, 1650.00, "Active", 3, 10, 20, 30),
        ("EUR-5003", "European Smart Home System", 15, 3, "Integrated smart home system for EU market", "2022-04-22", 550.00, 825.00, "Active", 5, 15, 30, 25),
        ("EUR-5004", "EU Industrial Sensor Array", 10, 3, "Comprehensive sensor system for EU factories", "2022-11-30", 1800.00, 2700.00, "Active", 2, 8, 15, 35),
    ]
    products.extend(european_products)
    product_id += len(european_products)
    
    # Asia-Pacific Products (unit 4)
    apac_products = [
        ("APAC-6001", "Precision Manufacturing Tools", 7, 4, "Specialized tools for Asian manufacturing", "2021-07-15", 1250.00, 1875.00, "Active", 3, 10, 20, 45),
        ("APAC-6002", "APAC Industrial Control System", 12, 4, "Control system for Asian industrial standards", "2022-01-20", 2800.00, 4200.00, "Active", 2, 5, 10, 60),
        ("APAC-6003", "APAC Smart Electronics Kit", 14, 4, "Consumer electronics customized for Asian market", "2022-08-10", 380.00, 570.00, "Active", 10, 30, 60, 25),
    ]
    products.extend(apac_products)
    product_id += len(apac_products)
    
    # Write to CSV
    with open(f"{OUTPUT_DIR}/products.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["product_id", "product_code", "product_name", "category_id", "unit_id", 
                         "description", "launch_date", "base_cost", "list_price", "status", 
                         "minimum_order_quantity", "reorder_point", "target_inventory_level", "lead_time_days"])
        for i, product in enumerate(products, 1):
            writer.writerow([i] + list(product))
    
    # Create a mapping of product details
    product_details = {}
    for i, product in enumerate(products, 1):
        product_details[i] = {
            "code": product[0],
            "name": product[1],
            "category_id": product[2],
            "unit_id": product[3],
            "description": product[4],
            "launch_date": product[5],
            "base_cost": product[6],
            "list_price": product[7],
            "status": product[8],
            "min_order_qty": product[9],
            "reorder_point": product[10],
            "target_inventory": product[11],
            "lead_time_days": product[12]
        }
    
    return product_details

# Generate customers
def generate_customers(regions):
    industries = [
        "Manufacturing", "Technology", "Healthcare", "Retail", "Construction", 
        "Energy", "Transportation", "Telecommunications", "Finance", "Education"
    ]
    
    business_types = ["B2B", "B2C", "Government", "Non-profit"]
    
    payment_terms = [
        "Net 30", "Net 45", "Net 60", "2/10 Net 30", "COD"
    ]
    
    # Generate larger customers first (will have higher order volumes)
    strategic_customers = [
        ("Global Manufacturing Corp", "Manufacturing", "B2B", 1, "2020-05-12", "John Williams", 1000000, "Net 45", True, 3750000),
        ("TechSolutions Inc", "Technology", "B2B", 1, "2020-08-23", "Sarah Martinez", 750000, "Net 30", True, 2800000),
        ("European Industries GmbH", "Manufacturing", "B2B", 3, "2021-02-15", "Hans Mueller", 850000, "Net 45", True, 2500000),
        ("Pacific Electronics Ltd", "Technology", "B2B", 5, "2021-05-08", "Yuki Tanaka", 600000, "Net 30", True, 1900000),
        ("National Healthcare Systems", "Healthcare", "Government", 1, "2020-11-30", "Robert Chen", 1200000, "Net 60", True, 3200000),
        ("Retail Solutions Group", "Retail", "B2B", 2, "2021-09-17", "Emma Wilson", 500000, "2/10 Net 30", True, 1500000),
        ("Construction Enterprises", "Construction", "B2B", 4, "2022-01-25", "James Baker", 850000, "Net 45", True, 2100000),
        ("Energy Innovations Co", "Energy", "B2B", 6, "2022-03-14", "Olivia Brown", 700000, "Net 30", True, 1800000),
        ("Transport & Logistics Inc", "Transportation", "B2B", 1, "2022-06-30", "David Martinez", 550000, "Net 45", True, 1600000),
        ("Global Communications Corp", "Telecommunications", "B2B", 7, "2022-10-12", "Sofia Rodriguez", 900000, "Net 30", True, 2200000)
    ]
    
    # Generate medium and smaller customers
    customers = strategic_customers.copy()
    for i in range(11, 51):
        industry = random.choice(industries)
        business_type = random.choice(business_types)
        region_id = random.randint(1, len(regions))
        acquisition_date = fake.date_between(start_date=START_DATE - datetime.timedelta(days=365*2), end_date=END_DATE - datetime.timedelta(days=90))
        account_manager = fake.name()
        
        # Scale credit limits and lifetime value based on how long they've been a customer
        days_as_customer = (END_DATE - acquisition_date).days
        base_credit = random.randint(50000, 300000)
        credit_limit = base_credit * (0.5 + (days_as_customer / 1000))
        
        lifetime_value = credit_limit * random.uniform(1.5, 3.0)
        
        customer = (
            fake.company(),
            industry,
            business_type,
            region_id,
            acquisition_date.strftime("%Y-%m-%d"),
            account_manager,
            round(credit_limit, 2),
            random.choice(payment_terms),
            random.random() > 0.05,  # 5% inactive
            round(lifetime_value, 2)
        )
        customers.append(customer)
    
    # Write to CSV
    with open(f"{OUTPUT_DIR}/customers.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["customer_id", "business_name", "industry", "business_type", 
                        "region_id", "acquisition_date", "account_manager", 
                        "credit_limit", "payment_terms", "is_active", "total_lifetime_value"])
        for i, customer in enumerate(customers, 1):
            writer.writerow([i] + list(customer))
    
    return {i+1: customer for i, customer in enumerate(customers)}

# Generate customer contacts
def generate_customer_contacts(customers):
    contacts = []
    for customer_id in range(1, len(customers) + 1):
        # Generate 1-3 contacts per customer
        num_contacts = random.randint(1, 3)
        has_primary = False
        
        for j in range(num_contacts):
            is_primary = (j == 0) or (not has_primary and random.random() > 0.7)
            if is_primary:
                has_primary = True
            
            first_name = fake.first_name()
            last_name = fake.last_name()
            job_title = random.choice([
                "CEO", "CFO", "CTO", "COO", "Purchasing Manager", 
                "Operations Director", "Supply Chain Manager", "Finance Director",
                "VP of Operations", "Procurement Specialist"
            ])
            
            contact = (
                customer_id,
                first_name,
                last_name,
                job_title,
                f"{first_name.lower()}.{last_name.lower()}@{fake.domain_name()}",
                fake.phone_number(),
                is_primary
            )
            contacts.append(contact)
    
    # Write to CSV
    with open(f"{OUTPUT_DIR}/customer_contacts.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["contact_id", "customer_id", "first_name", "last_name", 
                        "job_title", "email", "phone", "is_primary"])
        for i, contact in enumerate(contacts, 1):
            writer.writerow([i] + list(contact))

# Generate suppliers
def generate_suppliers():
    categories = [
        "Raw Materials", "Electronics Components", "Packaging Materials", 
        "Industrial Parts", "Office Supplies", "Chemicals", "Metal Products",
        "Plastic Components", "Machinery Parts", "Electrical Supplies"
    ]
    
    payment_terms = ["Net 30", "Net 45", "Net 60", "2/10 Net 30", "COD"]
    
    countries = ["USA", "China", "Germany", "Japan", "UK", "Canada", "Mexico", 
                "France", "Italy", "South Korea", "Taiwan", "Malaysia"]
    
    suppliers = []
    for i in range(1, 31):
        supplier_name = fake.company()
        contact_name = fake.name()
        contact_email = f"{contact_name.lower().replace(' ', '.')}@{supplier_name.lower().replace(' ', '')}.com"
        contact_phone = fake.phone_number()
        address = fake.address().replace('\n', ', ')
        country = random.choice(countries)
        supplier_rating = random.randint(2, 5)  # 2-5 rating
        primary_category = random.choice(categories)
        payment_term = random.choice(payment_terms)
        lead_time_days = random.randint(7, 90)
        is_active = random.random() > 0.1  # 10% inactive
        
        supplier = (
            supplier_name,
            contact_name,
            contact_email,
            contact_phone,
            address,
            country,
            supplier_rating,
            primary_category,
            payment_term,
            lead_time_days,
            is_active
        )
        suppliers.append(supplier)
    
    # Write to CSV
    with open(f"{OUTPUT_DIR}/suppliers.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["supplier_id", "supplier_name", "contact_name", "contact_email", 
                        "contact_phone", "address", "country", "supplier_rating", 
                        "primary_category", "payment_terms", "lead_time_days", "is_active"])
        for i, supplier in enumerate(suppliers, 1):
            writer.writerow([i] + list(supplier))
    
    return {i+1: supplier for i, supplier in enumerate(suppliers)}

# Generate inventory
def generate_inventory(products):
    warehouse_locations = [
        "Main Warehouse - Chicago", 
        "East Coast Warehouse - New Jersey", 
        "West Coast Warehouse - California",
        "European Distribution Center - Germany",
        "Asia-Pacific Center - Singapore"
    ]
    
    inventory_items = []
    for product_id in products:
        # Some products in multiple warehouses
        num_warehouses = min(random.randint(1, 3), len(warehouse_locations))
        warehouses = random.sample(warehouse_locations, num_warehouses)
        
        for warehouse in warehouses:
            product_code = products[product_id]["code"]
            product_name = products[product_id]["name"]
            base_cost = products[product_id]["base_cost"]
            list_price = products[product_id]["list_price"]
            unit_id = products[product_id]["unit_id"]
            target_level = products[product_id]["target_inventory"]
            restock_threshold = products[product_id]["reorder_point"]
            
            # Target inventory proportional to product value (inverse relationship)
            # More expensive products have lower inventory levels
            value_factor = 10000 / max(list_price, 100)
            #target_level = products[product_id][11]  # Using target_inventory_level from product data
            
            # Current quantity fluctuates around target level
            quantity_on_hand = int(target_level * random.uniform(0.7, 1.3))
            
            # Some items allocated
            quantity_allocated = int(quantity_on_hand * random.uniform(0, 0.3))
            
            # Restock threshold
            #restock_threshold = products[product_id][10]  # Using reorder_point from product data
            
            # Recent restock date
            last_restock_date = fake.date_between(
                start_date=END_DATE - datetime.timedelta(days=90), 
                end_date=END_DATE
            ).strftime("%Y-%m-%d")
            
            # Next restock
            next_restock_date = fake.date_between(
                start_date=END_DATE, 
                end_date=END_DATE + datetime.timedelta(days=90)
            ).strftime("%Y-%m-%d")
            
            inventory_item = (
                product_id,
                warehouse,
                quantity_on_hand,
                quantity_allocated,
                restock_threshold,
                last_restock_date,
                next_restock_date
            )
            inventory_items.append(inventory_item)
    
    # Write to CSV
    with open(f"{OUTPUT_DIR}/inventory.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["inventory_id", "product_id", "warehouse_location", 
                        "quantity_on_hand", "quantity_allocated", 
                        "restock_threshold", "last_restock_date", "next_restock_date"])
        for i, item in enumerate(inventory_items, 1):
            writer.writerow([i] + list(item))
    
    return {i+1: item for i, item in enumerate(inventory_items)}

# Generate inventory movements
def generate_inventory_movements(inventory):
    movements = []
    
    # Generate movement history
    date_range = pd.date_range(start=START_DATE, end=END_DATE, freq='D')
    
    for inventory_id, inventory_item in inventory.items():
        product_id = inventory_item[0]
        
        # Number of movements depends on product turnover
        # Some products move more frequently than others
        num_movements = random.randint(5, 25)
        movement_dates = sorted(random.sample(list(date_range), num_movements))
        
        for movement_date in movement_dates:
            # Transaction types with different probabilities
            transaction_type = random.choices(
                ["Restock", "Sale", "Return", "Adjustment", "Transfer"],
                weights=[0.3, 0.5, 0.1, 0.05, 0.05],
                k=1
            )[0]
            
            # Quantity depends on transaction type
            if transaction_type == "Restock":
                quantity = random.randint(10, 100)
            elif transaction_type == "Sale":
                quantity = -random.randint(1, 20)
            elif transaction_type == "Return":
                quantity = random.randint(1, 5)
            elif transaction_type == "Adjustment":
                quantity = random.randint(-10, 10)
            else:  # Transfer
                quantity = -random.randint(5, 30)
            
            # Reference document
            if transaction_type == "Restock":
                ref_doc = f"PO-{fake.random_number(digits=6)}"
            elif transaction_type == "Sale":
                ref_doc = f"SO-{fake.random_number(digits=6)}"
            elif transaction_type == "Return":
                ref_doc = f"RET-{fake.random_number(digits=6)}"
            elif transaction_type == "Adjustment":
                ref_doc = f"ADJ-{fake.random_number(digits=6)}"
            else:  # Transfer
                ref_doc = f"TRF-{fake.random_number(digits=6)}"
            
            notes = f"Inventory {transaction_type.lower()} for product ID {product_id}"
            
            movement = (
                inventory_id,
                movement_date.strftime("%Y-%m-%d %H:%M:%S"),
                transaction_type,
                quantity,
                ref_doc,
                notes
            )
            movements.append(movement)
    
    # Write to CSV
    with open(f"{OUTPUT_DIR}/inventory_movements.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["movement_id", "inventory_id", "transaction_date", 
                        "transaction_type", "quantity", "reference_document", "notes"])
        for i, movement in enumerate(movements, 1):
            writer.writerow([i] + list(movement))

# Generate departments
def generate_departments():
    departments = [
        (1, "Executive", "EXEC", "Robert Thompson", False, None),
        (2, "Finance", "FIN", "Jennifer Wilson", True, 1),
        (3, "Operations", "OPS", "Michael Harris", True, 1),
        (4, "Sales & Marketing", "SALES", "Patricia Garcia", True, 1),
        (5, "Research & Development", "RND", "Dr. James Anderson", True, 1),
        (6, "Human Resources", "HR", "Elizabeth Taylor", True, 1),
        (7, "Information Technology", "IT", "David Wright", True, 1),
        (8, "Customer Service", "CS", "Susan Martinez", True, 4),
        (9, "Manufacturing", "MFG", "Richard Johnson", True, 3),
        (10, "Quality Control", "QC", "Laura Brown", True, 9),
        (11, "Supply Chain", "SC", "Thomas Davis", True, 3),
        (12, "Product Development", "PD", "Jessica Wilson", True, 5),
        (13, "Marketing", "MKT", "Daniel Miller", True, 4),
        (14, "Accounting", "ACCT", "Rebecca Jones", True, 2),
        (15, "Treasury", "TRSY", "William Lee", True, 2),
        (16, "Legal", "LEGAL", "Samantha White", True, 1),
        (17, "Purchasing", "PURCH", "Jonathan Clark", True, 11),
        (18, "Logistics", "LOG", "Emily Rodriguez", True, 11),
        (19, "Facilities", "FAC", "Christopher Evans", True, 3),
        (20, "International Sales", "INTL", "Sophia Chen", True, 4)
    ]
    
    # Write to CSV
    with open(f"{OUTPUT_DIR}/departments.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["department_id", "department_name", "department_code", 
                        "manager_name", "cost_center", "parent_department_id"])
        writer.writerows(departments)
    
    return {d[0]: d for d in departments}

# Generate general ledger entries
def generate_general_ledger(account_ids):
    """Generate general ledger entries with realistic patterns for due diligence."""
    # Get list of dates for the period
    date_range = pd.date_range(start=START_DATE, end=END_DATE, freq='D')
    
    # Define patterns for various metrics
    # Our company had:
    # - Strong growth in 2022
    # - Challenges in mid-2023 (with cost-cutting efforts)
    # - Recovery beginning in late 2023
    # - Stabilization in 2024
    
    # Pattern for base revenue trends (annual growth + seasonality)
    # Different revenue patterns for different years
    revenue_2022 = generate_realistic_timeseries(
        base_value=250000, 
        num_points=365,  # 2022
        trend=0.15,      # Good growth
        seasonality=0.15,
        seasonality_period=90,  # Quarterly seasonality
        noise=0.05
    )
    
    revenue_2023 = generate_realistic_timeseries(
        base_value=revenue_2022[-1] * 0.9,  # Slight drop at start of 2023
        num_points=365,  # 2023
        trend=0.05,      # Slower growth during challenges
        seasonality=0.15,
        seasonality_period=90,
        noise=0.07       # More volatility
    )
    
    revenue_2024 = generate_realistic_timeseries(
        base_value=revenue_2023[-1] * 1.05,  # Slight recovery
        num_points=366,  # 2024 (leap year)
        trend=0.08,      # Moderate growth in recovery
        seasonality=0.15,
        seasonality_period=90,
        noise=0.04       # Stabilizing
    )
    
    # Combine the revenues
    revenue_pattern = np.concatenate([revenue_2022, revenue_2023, revenue_2024])
    
    # COGS is roughly 60% of revenue with slight efficiency improvements over time
    cogs_ratio_2022 = np.linspace(0.62, 0.60, 365)  # Slight improvement
    cogs_ratio_2023 = np.linspace(0.60, 0.58, 365)  # More improvement during cost-cutting
    cogs_ratio_2024 = np.linspace(0.58, 0.57, 366)  # Continued improvement
    cogs_ratio = np.concatenate([cogs_ratio_2022, cogs_ratio_2023, cogs_ratio_2024])
    cogs_pattern = revenue_pattern * cogs_ratio
    
    # Operating expenses (excluding COGS) show cost-cutting in 2023
    opex_2022 = generate_realistic_timeseries(
        base_value=80000, 
        num_points=365,
        trend=0.08,      # Growing with company
        seasonality=0.05,
        seasonality_period=30,  # Monthly pattern
        noise=0.03
    )
    
    opex_2023_start = opex_2022[-1] * 1.02
    opex_2023 = generate_realistic_timeseries(
        base_value=opex_2023_start,
        num_points=365,
        trend=-0.05,     # Cost-cutting efforts
        seasonality=0.05,
        seasonality_period=30,
        noise=0.04
    )
    
    opex_2024_start = opex_2023[-1] * 0.99
    opex_2024 = generate_realistic_timeseries(
        base_value=opex_2024_start,
        num_points=366,
        trend=0.02,      # Slight increases with growth
        seasonality=0.05,
        seasonality_period=30,
        noise=0.03
    )
    
    opex_pattern = np.concatenate([opex_2022, opex_2023, opex_2024])
    
    # Generate general ledger entries
    entries = []
    
    # Map of account names to IDs
    revenue_accounts = [
        account_ids["Product Sales - Industrial"],
        account_ids["Product Sales - Consumer"],
        account_ids["Service Revenue"],
        account_ids["International Sales"]
    ]
    
    cogs_accounts = [
        account_ids["Cost of Goods Sold"],
        account_ids["Direct Materials"],
        account_ids["Direct Labor"],
        account_ids["Manufacturing Overhead"]
    ]
    
    opex_accounts = [
        account_ids["Salaries & Wages"],
        account_ids["Employee Benefits"],
        account_ids["Rent Expense"],
        account_ids["Utilities"],
        account_ids["Office Supplies"],
        account_ids["Professional Services"],
        account_ids["Marketing & Advertising"],
        account_ids["Travel & Entertainment"],
        account_ids["R&D Expenses"],
        account_ids["Depreciation Expense"],
        account_ids["Insurance Expense"]
    ]
    
    # Daily entries
    for i, date in enumerate(date_range):
        day_of_month = date.day
        month = date.month
        year = date.year
        quarter = (month - 1) // 3 + 1
        
        # Set fiscal year, quarter, month (assuming calendar fiscal year)
        fiscal_year = year
        fiscal_quarter = quarter
        fiscal_month = month
        
        # Daily revenue entry (split between accounts)
        day_revenue = revenue_pattern[i]
        # Distribute revenue across revenue accounts based on product mix
        # Product mix changes over time - more consumer products later
        if year == 2022:
            revenue_weights = [0.6, 0.2, 0.1, 0.1]  # More industrial focus
        elif year == 2023:
            revenue_weights = [0.55, 0.25, 0.1, 0.1]  # Shift toward consumer
        else:  # 2024
            revenue_weights = [0.5, 0.3, 0.1, 0.1]  # More balanced
        
        # Add monthly pattern (higher at month end)
        month_end_factor = 1.0
        if day_of_month >= 28:
            month_end_factor = 1.3  # 30% higher at month end
        elif day_of_month <= 5:
            month_end_factor = 0.8  # 20% lower at month start
        
        # Quarter end is even higher
        if month in [3, 6, 9, 12] and day_of_month >= 28:
            month_end_factor *= 1.2  # Additional 20% at quarter end
        
        day_revenue *= month_end_factor
        
        for idx, account_id in enumerate(revenue_accounts):
            account_revenue = day_revenue * revenue_weights[idx]
            if account_revenue > 0:
                # For each revenue account, create a debit to cash and credit to revenue
                # First, the debit to cash
                cash_entry = (
                    date.strftime("%Y-%m-%d"),
                    account_ids["Cash and Cash Equivalents"],
                    account_revenue,  # Debit
                    0,               # Credit
                    f"REV-{date.strftime('%Y%m%d')}-{idx+1}",
                    f"Daily revenue - {date.strftime('%Y-%m-%d')}",
                    fiscal_year,
                    fiscal_quarter,
                    fiscal_month,
                    "Sales System"
                )
                entries.append(cash_entry)
                
                # Then, the credit to revenue
                revenue_entry = (
                    date.strftime("%Y-%m-%d"),
                    account_id,
                    0,               # Debit
                    account_revenue, # Credit
                    f"REV-{date.strftime('%Y%m%d')}-{idx+1}",
                    f"Daily revenue - {date.strftime('%Y-%m-%d')}",
                    fiscal_year,
                    fiscal_quarter,
                    fiscal_month,
                    "Sales System"
                )
                entries.append(revenue_entry)
        
        # Daily COGS entry
        day_cogs = cogs_pattern[i]
        # Distribute COGS across COGS accounts
        cogs_weights = [0.7, 0.15, 0.1, 0.05]  # Distribution of COGS
        
        for idx, account_id in enumerate(cogs_accounts):
            account_cogs = day_cogs * cogs_weights[idx]
            if account_cogs > 0:
                # For each COGS account, create a debit to COGS and credit to inventory
                # First, the debit to COGS
                cogs_debit_entry = (
                    date.strftime("%Y-%m-%d"),
                    account_id,
                    account_cogs,    # Debit
                    0,               # Credit
                    f"COGS-{date.strftime('%Y%m%d')}-{idx+1}",
                    f"Daily COGS - {date.strftime('%Y-%m-%d')}",
                    fiscal_year,
                    fiscal_quarter,
                    fiscal_month,
                    "Inventory System"
                )
                entries.append(cogs_debit_entry)
                
                # Then, the credit to inventory
                cogs_credit_entry = (
                    date.strftime("%Y-%m-%d"),
                    account_ids["Inventory"],
                    0,               # Debit
                    account_cogs,    # Credit
                    f"COGS-{date.strftime('%Y%m%d')}-{idx+1}",
                    f"Daily COGS - {date.strftime('%Y-%m-%d')}",
                    fiscal_year,
                    fiscal_quarter,
                    fiscal_month,
                    "Inventory System"
                )
                entries.append(cogs_credit_entry)
        
        # Operating expense entries - typically recorded periodically, not daily
        # We'll do these on specific days of the month for realism
        
        # Payroll biweekly (1st and 15th)
        if day_of_month in [1, 15]:
            # Salaries and wages
            payroll_factor = 2.0  # Biweekly, so 2x the daily value
            payroll_amount = (opex_pattern[i] * 0.5) * payroll_factor  # 50% of opex is payroll
            
            # Debit to salaries expense
            payroll_debit_entry = (
                date.strftime("%Y-%m-%d"),
                account_ids["Salaries & Wages"],
                payroll_amount,  # Debit
                0,               # Credit
                f"PAY-{date.strftime('%Y%m%d')}",
                f"Biweekly payroll - {date.strftime('%Y-%m-%d')}",
                fiscal_year,
                fiscal_quarter,
                fiscal_month,
                "Payroll System"
            )
            entries.append(payroll_debit_entry)
            
            # Credit to cash
            payroll_credit_entry = (
                date.strftime("%Y-%m-%d"),
                account_ids["Cash and Cash Equivalents"],
                0,               # Debit
                payroll_amount,  # Credit
                f"PAY-{date.strftime('%Y%m%d')}",
                f"Biweekly payroll - {date.strftime('%Y-%m-%d')}",
                fiscal_year,
                fiscal_quarter,
                fiscal_month,
                "Payroll System"
            )
            entries.append(payroll_credit_entry)
            
            # Benefits paid with payroll
            benefits_amount = payroll_amount * 0.25  # 25% of salary
            
            # Debit to benefits expense
            benefits_debit_entry = (
                date.strftime("%Y-%m-%d"),
                account_ids["Employee Benefits"],
                benefits_amount,  # Debit
                0,                # Credit
                f"BEN-{date.strftime('%Y%m%d')}",
                f"Employee benefits - {date.strftime('%Y-%m-%d')}",
                fiscal_year,
                fiscal_quarter,
                fiscal_month,
                "Payroll System"
            )
            entries.append(benefits_debit_entry)
            
            # Credit to cash
            benefits_credit_entry = (
                date.strftime("%Y-%m-%d"),
                account_ids["Cash and Cash Equivalents"],
                0,                # Debit
                benefits_amount,  # Credit
                f"BEN-{date.strftime('%Y%m%d')}",
                f"Employee benefits - {date.strftime('%Y-%m-%d')}",
                fiscal_year,
                fiscal_quarter,
                fiscal_month,
                "Payroll System"
            )
            entries.append(benefits_credit_entry)
        
        # Monthly expenses on the 1st
        if day_of_month == 1:
            # Monthly factor is ~30 days
            monthly_factor = 30.0
            
            # Rent payment
            rent_amount = (opex_pattern[i] * 0.12) * monthly_factor  # 12% of opex
            rent_debit_entry = (
                date.strftime("%Y-%m-%d"),
                account_ids["Rent Expense"],
                rent_amount,  # Debit
                0,            # Credit
                f"RENT-{date.strftime('%Y%m')}",
                f"Monthly rent - {date.strftime('%Y-%m')}",
                fiscal_year,
                fiscal_quarter,
                fiscal_month,
                "AP System"
            )
            entries.append(rent_debit_entry)
            
            rent_credit_entry = (
                date.strftime("%Y-%m-%d"),
                account_ids["Cash and Cash Equivalents"],
                0,            # Debit
                rent_amount,  # Credit
                f"RENT-{date.strftime('%Y%m')}",
                f"Monthly rent - {date.strftime('%Y-%m')}",
                fiscal_year,
                fiscal_quarter,
                fiscal_month,
                "AP System"
            )
            entries.append(rent_credit_entry)
            
            # Utilities
            utilities_amount = (opex_pattern[i] * 0.05) * monthly_factor  # 5% of opex
            utilities_debit_entry = (
                date.strftime("%Y-%m-%d"),
                account_ids["Utilities"],
                utilities_amount,  # Debit
                0,                 # Credit
                f"UTIL-{date.strftime('%Y%m')}",
                f"Monthly utilities - {date.strftime('%Y-%m')}",
                fiscal_year,
                fiscal_quarter,
                fiscal_month,
                "AP System"
            )
            entries.append(utilities_debit_entry)
            
            utilities_credit_entry = (
                date.strftime("%Y-%m-%d"),
                account_ids["Cash and Cash Equivalents"],
                0,                 # Debit
                utilities_amount,  # Credit
                f"UTIL-{date.strftime('%Y%m')}",
                f"Monthly utilities - {date.strftime('%Y-%m')}",
                fiscal_year,
                fiscal_quarter,
                fiscal_month,
                "AP System"
            )
            entries.append(utilities_credit_entry)
            
            # Insurance
            insurance_amount = (opex_pattern[i] * 0.04) * monthly_factor  # 4% of opex
            insurance_debit_entry = (
                date.strftime("%Y-%m-%d"),
                account_ids["Insurance Expense"],
                insurance_amount,  # Debit
                0,                 # Credit
                f"INS-{date.strftime('%Y%m')}",
                f"Monthly insurance - {date.strftime('%Y-%m')}",
                fiscal_year,
                fiscal_quarter,
                fiscal_month,
                "AP System"
            )
            entries.append(insurance_debit_entry)
            
            insurance_credit_entry = (
                date.strftime("%Y-%m-%d"),
                account_ids["Cash and Cash Equivalents"],
                0,                 # Debit
                insurance_amount,  # Credit
                f"INS-{date.strftime('%Y%m')}",
                f"Monthly insurance - {date.strftime('%Y-%m')}",
                fiscal_year,
                fiscal_quarter,
                fiscal_month,
                "AP System"
            )
            entries.append(insurance_credit_entry)
        
        # Marketing expenses - higher at quarter start
        if day_of_month <= 5 and month in [1, 4, 7, 10]:
            # Marketing campaigns for the quarter
            marketing_amount = (opex_pattern[i] * 0.08) * 90  # 8% of opex for the quarter
            marketing_debit_entry = (
                date.strftime("%Y-%m-%d"),
                account_ids["Marketing & Advertising"],
                marketing_amount,  # Debit
                0,                 # Credit
                f"MKT-{fiscal_year}Q{fiscal_quarter}",
                f"Quarterly marketing budget - Q{fiscal_quarter} {fiscal_year}",
                fiscal_year,
                fiscal_quarter,
                fiscal_month,
                "AP System"
            )
            entries.append(marketing_debit_entry)
            
            marketing_credit_entry = (
                date.strftime("%Y-%m-%d"),
                account_ids["Cash and Cash Equivalents"],
                0,                 # Debit
                marketing_amount,  # Credit
                f"MKT-{fiscal_year}Q{fiscal_quarter}",
                f"Quarterly marketing budget - Q{fiscal_quarter} {fiscal_year}",
                fiscal_year,
                fiscal_quarter,
                fiscal_month,
                "AP System"
            )
            entries.append(marketing_credit_entry)
        
        # R&D - quarterly expenses
        if day_of_month == 15 and month in [1, 4, 7, 10]:
            # R&D investments 
            # Increasing over time despite cost-cutting elsewhere
            if year == 2022:
                rd_factor = 1.0
            elif year == 2023:
                rd_factor = 1.05  # Increased despite other cost-cutting
            else:  # 2024
                rd_factor = 1.12  # Further increase as part of recovery
                
            rd_amount = (opex_pattern[i] * 0.15) * 90 * rd_factor  # 15% of opex for the quarter
            rd_debit_entry = (
                date.strftime("%Y-%m-%d"),
                account_ids["R&D Expenses"],
                rd_amount,  # Debit
                0,          # Credit
                f"RND-{fiscal_year}Q{fiscal_quarter}",
                f"Quarterly R&D budget - Q{fiscal_quarter} {fiscal_year}",
                fiscal_year,
                fiscal_quarter,
                fiscal_month,
                "AP System"
            )
            entries.append(rd_debit_entry)
            
            rd_credit_entry = (
                date.strftime("%Y-%m-%d"),
                account_ids["Cash and Cash Equivalents"],
                0,          # Debit
                rd_amount,  # Credit
                f"RND-{fiscal_year}Q{fiscal_quarter}",
                f"Quarterly R&D budget - Q{fiscal_quarter} {fiscal_year}",
                fiscal_year,
                fiscal_quarter,
                fiscal_month,
                "AP System"
            )
            entries.append(rd_credit_entry)
        
        # Depreciation - monthly
        if day_of_month == 28:
            # Depreciation increases with asset base
            if year == 2022:
                dep_base = 35000  # Monthly base
                dep_growth = 0.004  # Monthly growth
            elif year == 2023:
                dep_base = 45000
                dep_growth = 0.003
            else:  # 2024
                dep_base = 52000
                dep_growth = 0.002
                
            # Calculate month number since start
            month_num = (year - START_DATE.year) * 12 + month
            dep_amount = dep_base * (1 + dep_growth) ** month_num
            
            dep_debit_entry = (
                date.strftime("%Y-%m-%d"),
                account_ids["Depreciation Expense"],
                dep_amount,  # Debit
                0,           # Credit
                f"DEP-{date.strftime('%Y%m')}",
                f"Monthly depreciation - {date.strftime('%Y-%m')}",
                fiscal_year,
                fiscal_quarter,
                fiscal_month,
                "GL System"
            )
            entries.append(dep_debit_entry)
            
            dep_credit_entry = (
                date.strftime("%Y-%m-%d"),
                account_ids["Accumulated Depreciation"],
                0,           # Debit
                dep_amount,  # Credit
                f"DEP-{date.strftime('%Y%m')}",
                f"Monthly depreciation - {date.strftime('%Y-%m')}",
                fiscal_year,
                fiscal_quarter,
                fiscal_month,
                "GL System"
            )
            entries.append(dep_credit_entry)

        if day_of_month == 10:  # Pick a day in the month that doesn't conflict with other entries
            # Other operating expenses (5% of monthly opex)
            other_opex_amount = (opex_pattern[i] * 0.05) * 30  # 5% of monthly opex
            
            # Debit to other expense
            other_opex_debit_entry = (
                date.strftime("%Y-%m-%d"),
                account_ids["Office Supplies"],  # Use as a proxy for "Other Operating Expenses"
                other_opex_amount,  # Debit
                0,                 # Credit
                f"OTHR-{date.strftime('%Y%m')}",
                f"Monthly other expenses - {date.strftime('%Y-%m')}",
                fiscal_year,
                fiscal_quarter,
                fiscal_month,
                "AP System"
            )
            entries.append(other_opex_debit_entry)
            
            # Credit to cash
            other_opex_credit_entry = (
                date.strftime("%Y-%m-%d"),
                account_ids["Cash and Cash Equivalents"],
                0,                 # Debit
                other_opex_amount,  # Credit
                f"OTHR-{date.strftime('%Y%m')}",
                f"Monthly other expenses - {date.strftime('%Y-%m')}",
                fiscal_year,
                fiscal_quarter,
                fiscal_month,
                "AP System"
            )
            entries.append(other_opex_credit_entry)

        # Interest expense - quarterly
        if day_of_month == 15 and month in [3, 6, 9, 12]:
            # Interest rates increased in 2023
            if year == 2022:
                int_rate = 0.045  # 4.5% annual
            elif year == 2023:
                int_rate = 0.055  # 5.5% annual
            else:  # 2024
                int_rate = 0.06   # 6.0% annual
                
            # Outstanding debt
            if year == 2022:
                debt_balance = 5000000 - (quarter - 1) * 100000  # Paying down debt
            elif year == 2023:
                debt_balance = 4600000 + (quarter - 1) * 50000  # Taking on some debt during challenges
            else:  # 2024
                debt_balance = 4800000 - (quarter - 1) * 75000  # Paying down again
                
            int_amount = debt_balance * (int_rate / 4)  # Quarterly interest
            
            int_debit_entry = (
                date.strftime("%Y-%m-%d"),
                account_ids["Interest Expense"],
                int_amount,  # Debit
                0,           # Credit
                f"INT-{fiscal_year}Q{fiscal_quarter}",
                f"Quarterly interest - Q{fiscal_quarter} {fiscal_year}",
                fiscal_year,
                fiscal_quarter,
                fiscal_month,
                "GL System"
            )
            entries.append(int_debit_entry)
            
            int_credit_entry = (
                date.strftime("%Y-%m-%d"),
                account_ids["Cash and Cash Equivalents"],
                0,           # Debit
                int_amount,  # Credit
                f"INT-{fiscal_year}Q{fiscal_quarter}",
                f"Quarterly interest - Q{fiscal_quarter} {fiscal_year}",
                fiscal_year,
                fiscal_quarter,
                fiscal_month,
                "GL System"
            )
            entries.append(int_credit_entry)
    
    # Write to CSV
    with open(f"{OUTPUT_DIR}/general_ledger.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["entry_id", "entry_date", "account_id", "debit_amount", "credit_amount", 
                        "reference_number", "description", "fiscal_year", "fiscal_quarter", 
                        "fiscal_month", "entry_source"])
        for i, entry in enumerate(entries, 1):
            writer.writerow([i] + list(entry))

# Generate financial statements
def generate_financial_statements(account_ids):
    """Generate quarterly and annual financial statements."""
    statements = []
    statement_id = 1
    
    # Generate for each year and quarter
    years = [2022, 2023, 2024]
    
    for year in years:
        # Annual statements
        statements.append((
            "Income Statement", year, None, None, True, 
            "Jennifer Wilson, CFO", "Robert Thompson, CEO"
        ))
        statements.append((
            "Balance Sheet", year, None, None, True, 
            "Jennifer Wilson, CFO", "Robert Thompson, CEO"
        ))
        statements.append((
            "Cash Flow Statement", year, None, None, True, 
            "Jennifer Wilson, CFO", "Robert Thompson, CEO"
        ))
        
        # Quarterly statements
        for quarter in range(1, 5):
            # Skip future quarters for current year
            if year == datetime.date.today().year and quarter > ((datetime.date.today().month - 1) // 3 + 1):
                continue
                
            statements.append((
                "Income Statement", year, quarter, None, False, 
                "Rebecca Jones, Controller", "Jennifer Wilson, CFO"
            ))
            statements.append((
                "Balance Sheet", year, quarter, None, False, 
                "Rebecca Jones, Controller", "Jennifer Wilson, CFO"
            ))
            statements.append((
                "Cash Flow Statement", year, quarter, None, False, 
                "Rebecca Jones, Controller", "Jennifer Wilson, CFO"
            ))
            
            # Monthly statements (less formal, not all are audited)
            for month in range(1 + (quarter-1)*3, 1 + quarter*3):
                statements.append((
                    "Income Statement", year, quarter, month, False, 
                    "William Lee, Accounting Manager", "Rebecca Jones, Controller"
                ))
                statements.append((
                    "Balance Sheet", year, quarter, month, False, 
                    "William Lee, Accounting Manager", "Rebecca Jones, Controller"
                ))
    
    # Write to CSV
    with open(f"{OUTPUT_DIR}/financial_statements.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["statement_id", "statement_type", "fiscal_year", "fiscal_quarter", 
                         "fiscal_month", "is_audited", "prepared_by", "approved_by"])
        for i, statement in enumerate(statements, 1):
            writer.writerow([i] + list(statement))
    
    # Generate financial statement items (simplified - just a few sample line items)
    # In a real system, these would be calculated from the general ledger
    
    # For simplicity, we'll just create a few key line items for the annual statements
    statement_items = []
    item_id = 1
    
    # Function to add an item
    def add_item(statement_id, account_id, name, value, order, parent=None):
        nonlocal item_id
        item = (statement_id, account_id, name, value, order, parent)
        statement_items.append(item)
        current_id = item_id
        item_id += 1
        return current_id
    
    # Annual Income Statements - create line items for each year
    # These values reflect our scenario: growth in 2022, challenges in 2023, recovery in 2024
    annual_is_data = {
        2022: {
            "Revenue": 89500000,
            "COGS": 53700000,
            "Gross Profit": 35800000,
            "Operating Expenses": 28400000,
            "Operating Income": 7400000,
            "Interest Expense": 225000,
            "Income Before Tax": 7175000,
            "Income Tax": 1794000,
            "Net Income": 5381000
        },
        2023: {
            "Revenue": 92200000,
            "COGS": 53476000,
            "Gross Profit": 38724000,
            "Operating Expenses": 31348000,
            "Operating Income": 7376000,
            "Interest Expense": 264000,
            "Income Before Tax": 7112000,
            "Income Tax": 1778000,
            "Net Income": 5334000
        },
        2024: {
            "Revenue": 99800000,
            "COGS": 56886000,
            "Gross Profit": 42914000,
            "Operating Expenses": 32936000,
            "Operating Income": 9978000,
            "Interest Expense": 288000,
            "Income Before Tax": 9690000,
            "Income Tax": 2423000,
            "Net Income": 7267000
        }
    }
    
    # Find the statement IDs for annual income statements
    annual_is_ids = {}
    for i, stmt in enumerate(statements):
        if stmt[0] == "Income Statement" and stmt[2] is None and stmt[3] is None:
            annual_is_ids[stmt[1]] = i + 1  # statement_id
    
    # Add line items for annual income statements
    for year, stmt_id in annual_is_ids.items():
        data = annual_is_data[year]
        
        # Top-level Revenue
        rev_id = add_item(stmt_id, account_ids["Product Sales - Industrial"], "Revenue", data["Revenue"], 1)
        
        # Revenue components (children of Revenue)
        add_item(stmt_id, account_ids["Product Sales - Industrial"], "Product Sales - Industrial", data["Revenue"] * 0.55, 2, rev_id)
        add_item(stmt_id, account_ids["Product Sales - Consumer"], "Product Sales - Consumer", data["Revenue"] * 0.25, 3, rev_id)
        add_item(stmt_id, account_ids["Service Revenue"], "Service Revenue", data["Revenue"] * 0.1, 4, rev_id)
        add_item(stmt_id, account_ids["International Sales"], "International Sales", data["Revenue"] * 0.1, 5, rev_id)
        
        # COGS
        cogs_id = add_item(stmt_id, account_ids["Cost of Goods Sold"], "Cost of Goods Sold", data["COGS"], 6)
        
        # COGS components
        add_item(stmt_id, account_ids["Direct Materials"], "Direct Materials", data["COGS"] * 0.65, 7, cogs_id)
        add_item(stmt_id, account_ids["Direct Labor"], "Direct Labor", data["COGS"] * 0.25, 8, cogs_id)
        add_item(stmt_id, account_ids["Manufacturing Overhead"], "Manufacturing Overhead", data["COGS"] * 0.1, 9, cogs_id)
        
        # Gross Profit
        add_item(stmt_id, None, "Gross Profit", data["Gross Profit"], 10)
        
        # Operating Expenses
        opex_id = add_item(stmt_id, None, "Operating Expenses", data["Operating Expenses"], 11)
        
        # Operating Expense components
        add_item(stmt_id, account_ids["Salaries & Wages"], "Salaries & Wages", data["Operating Expenses"] * 0.45, 12, opex_id)
        add_item(stmt_id, account_ids["Employee Benefits"], "Employee Benefits", data["Operating Expenses"] * 0.12, 13, opex_id)
        add_item(stmt_id, account_ids["Rent Expense"], "Rent Expense", data["Operating Expenses"] * 0.08, 14, opex_id)
        add_item(stmt_id, account_ids["Marketing & Advertising"], "Marketing & Advertising", data["Operating Expenses"] * 0.1, 15, opex_id)
        add_item(stmt_id, account_ids["R&D Expenses"], "R&D Expenses", data["Operating Expenses"] * 0.15, 16, opex_id)
        add_item(stmt_id, account_ids["Depreciation Expense"], "Depreciation Expense", data["Operating Expenses"] * 0.05, 17, opex_id)
        add_item(stmt_id, None, "Other Operating Expenses", data["Operating Expenses"] * 0.05, 18, opex_id)
        
        # Operating Income
        add_item(stmt_id, None, "Operating Income", data["Operating Income"], 19)
        
        # Non-operating items
        add_item(stmt_id, account_ids["Interest Expense"], "Interest Expense", data["Interest Expense"], 20)
        
        # Income Before Tax
        add_item(stmt_id, None, "Income Before Tax", data["Income Before Tax"], 21)
        
        # Income Tax
        add_item(stmt_id, account_ids["Income Tax Expense"], "Income Tax Expense", data["Income Tax"], 22)
        
        # Net Income
        add_item(stmt_id, None, "Net Income", data["Net Income"], 23)
    
    # Write to CSV
    with open(f"{OUTPUT_DIR}/financial_statement_items.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["item_id", "statement_id", "account_id", "line_item_name", 
                         "line_item_value", "line_item_order", "parent_item_id"])
        for i, item in enumerate(statement_items, 1):
            writer.writerow([i] + list(item))

# Generate budget plans and actuals
def generate_budget_vs_actual(account_ids):
    """Generate budget plans and actual results."""
    # Budget plans for each year
    budget_plans = [
        (f"Annual Budget {year}", year, f"Comprehensive annual budget for fiscal year {year}", 
         "Approved", "Jennifer Wilson, CFO", "Robert Thompson, CEO")
        for year in [2022, 2023, 2024]
    ]
    
    # Write budget plans to CSV
    with open(f"{OUTPUT_DIR}/budget_plans.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["budget_id", "budget_name", "fiscal_year", "description", 
                         "status", "prepared_by", "approved_by"])
        for i, plan in enumerate(budget_plans, 1):
            writer.writerow([i] + list(plan))
    
    # Generate budget vs actual data
    # Key accounts to track - focus on most important for a DD
    tracked_accounts = [
        # Revenue accounts
        account_ids["Product Sales - Industrial"],
        account_ids["Product Sales - Consumer"],
        account_ids["Service Revenue"],
        account_ids["International Sales"],
        
        # COGS accounts
        account_ids["Cost of Goods Sold"],
        account_ids["Direct Materials"],
        account_ids["Direct Labor"],
        
        # Operating expense accounts
        account_ids["Salaries & Wages"],
        account_ids["Marketing & Advertising"],
        account_ids["R&D Expenses"]
    ]
    
    # Budget vs Actual patterns
    # 2022: Slightly exceeded revenue targets, close to budget on expenses
    # 2023: Missed revenue targets, exceeded expense budgets
    # 2024: Exceeding revenue targets, close to expense budgets
    
    budget_actuals = []
    
    # Annual revenue and expense patterns (total company)
    annual_patterns = {
        2022: {
            "revenue_budget": 88000000,
            "revenue_actual": 89500000,  # Beat budget
            "revenue_variance": 0.017,   # +1.7%
            
            "cogs_budget": 53240000,    # 60.5% of revenue budget
            "cogs_actual": 53700000,    # 60.0% of actual revenue
            "cogs_variance": 0.009,     # +0.9% (slight overspend)
            
            "opex_budget": 28160000,    # 32% of revenue budget
            "opex_actual": 28400000,    # 31.7% of actual revenue
            "opex_variance": 0.009      # +0.9% (slight overspend)
        },
        2023: {
            "revenue_budget": 95000000,
            "revenue_actual": 92200000,  # Missed budget
            "revenue_variance": -0.029,  # -2.9%
            
            "cogs_budget": 55575000,     # 58.5% of revenue budget
            "cogs_actual": 53476000,     # 58.0% of actual revenue (efficiency improvements)
            "cogs_variance": -0.038,     # -3.8% (underspent due to lower volume)
            
            "opex_budget": 30400000,     # 32% of revenue budget
            "opex_actual": 31348000,     # 34% of actual revenue
            "opex_variance": 0.031       # +3.1% (overspent)
        },
        2024: {
            "revenue_budget": 97000000,
            "revenue_actual": 99800000,  # Beat budget
            "revenue_variance": 0.029,   # +2.9%
            
            "cogs_budget": 56245000,     # 58.0% of revenue budget
            "cogs_actual": 56886000,     # 57.0% of actual revenue (efficiency improvements)
            "cogs_variance": 0.011,      # +1.1% (slightly over due to higher volume)
            
            "opex_budget": 31040000,     # 32% of revenue budget
            "opex_actual": 32936000,     # 33% of actual revenue
            "opex_variance": 0.061       # +6.1% (overspent for growth)
        }
    }
    
    # Revenue distribution across accounts
    revenue_distribution = {
        2022: [0.60, 0.20, 0.10, 0.10],  # Industrial, Consumer, Service, International
        2023: [0.55, 0.25, 0.10, 0.10],
        2024: [0.50, 0.30, 0.10, 0.10]
    }
    
    # COGS distribution
    cogs_distribution = [0.70, 0.20, 0.10]  # Total COGS, Direct Materials, Direct Labor
    
    # OPEX distribution 
    opex_distribution = [0.45, 0.10, 0.15]  # Salaries, Marketing, R&D
    
    # Generate quarterly and monthly data
    for year in [2022, 2023, 2024]:
        budget_id = year - 2021  # Budget ID matches the year
        
        annual_data = annual_patterns[year]
        rev_dist = revenue_distribution[year]
        
        # Quarterly seasonality for this industry
        # Q1: 20%, Q2: 25%, Q3: 25%, Q4: 30%
        quarterly_factors = [0.20, 0.25, 0.25, 0.30]
        
        for quarter in range(1, 5):
            # Skip future quarters for current year
            if year == datetime.date.today().year and quarter > ((datetime.date.today().month - 1) // 3 + 1):
                continue
                
            # Quarterly factors with some variance between budget and actual
            q_budget_factor = quarterly_factors[quarter-1]
            
            # Actuals have some variance from plan by quarter
            # 2022: Q1-Q3 on track, Q4 exceeds
            # 2023: Q1 on track, Q2-Q3 below plan, Q4 slightly below
            # 2024: Q1-Q2 above plan, Q3-Q4 projected to be on plan
            if year == 2022:
                if quarter == 4:
                    q_actual_factor = quarterly_factors[quarter-1] * 1.05  # Q4 outperformed
                else:
                    q_actual_factor = quarterly_factors[quarter-1] * 1.00  # On plan
            elif year == 2023:
                if quarter == 1:
                    q_actual_factor = quarterly_factors[quarter-1] * 1.00  # Q1 on plan
                elif quarter in [2, 3]:
                    q_actual_factor = quarterly_factors[quarter-1] * 0.92  # Q2-Q3 below plan
                else:
                    q_actual_factor = quarterly_factors[quarter-1] * 0.96  # Q4 slightly below
            else:  # 2024
                if quarter in [1, 2]:
                    q_actual_factor = quarterly_factors[quarter-1] * 1.06  # Q1-Q2 above plan
                else:
                    q_actual_factor = quarterly_factors[quarter-1] * 1.00  # On plan (projections)
                    
            # Monthly distribution within quarter (month 1: 30%, month 2: 30%, month 3: 40%)
            monthly_factors = [0.30, 0.30, 0.40]
            
            for month_idx, month_factor in enumerate(monthly_factors):
                month = 3 * (quarter - 1) + month_idx + 1
                
                # Skip future months for current year/quarter
                if (year == datetime.date.today().year and 
                    ((quarter - 1) * 3 + month_idx + 1) > datetime.date.today().month):
                    continue
                
                # Calculate budget and actual for each account
                for i, account_id in enumerate(tracked_accounts):
                    # Determine which category and distribution to use
                    if i < 4:  # Revenue accounts
                        # For each revenue account
                        category = "revenue"
                        dist_factor = rev_dist[i]
                    elif i < 7:  # COGS accounts
                        category = "cogs"
                        if i == 4:  # Total COGS
                            dist_factor = 1.0  # This is already the total
                        else:
                            dist_factor = cogs_distribution[i-5]
                    else:  # Operating expense accounts
                        category = "opex"
                        dist_factor = opex_distribution[i-7]
                    
                    # Calculate budget amount
                    budget_base = annual_data[f"{category}_budget"] * dist_factor
                    budget_amount = budget_base * q_budget_factor * month_factor
                    
                    # Calculate actual amount
                    actual_base = annual_data[f"{category}_actual"] * dist_factor
                    actual_amount = actual_base * q_actual_factor * month_factor
                    
                    # Add some noise to make it realistic
                    budget_amount *= random.uniform(0.99, 1.01)
                    actual_amount *= random.uniform(0.98, 1.02)
                    
                    # Calculate variance
                    variance_amount = actual_amount - budget_amount
                    variance_percentage = (variance_amount / budget_amount) * 100 if budget_amount != 0 else 0
                    
                    # Handle future months
                    is_future = (year > datetime.date.today().year or 
                                (year == datetime.date.today().year and month > datetime.date.today().month))
                    
                    if is_future:
                        actual_amount = None
                        variance_amount = None
                        variance_percentage = None
                    
                    budget_actual = (
                        budget_id,
                        account_id,
                        year,
                        quarter,
                        month,
                        round(budget_amount, 2),
                        None if is_future else round(actual_amount, 2),
                        None if is_future else round(variance_amount, 2),
                        None if is_future else round(variance_percentage, 2)
                    )
                    budget_actuals.append(budget_actual)
    
    # Write to CSV
    with open(f"{OUTPUT_DIR}/budget_vs_actual.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "budget_id", "account_id", "fiscal_year", "fiscal_quarter", 
                         "fiscal_month", "budget_amount", "actual_amount", 
                         "variance_amount", "variance_percentage"])
        for i, ba in enumerate(budget_actuals, 1):
            writer.writerow([i] + list(ba))

# Generate cash flow
def generate_cash_flow(account_ids):
    """Generate cash flow data."""
    cash_flows = []
    date_range = pd.date_range(start=START_DATE, end=END_DATE, freq='D')
    
    # Annual patterns
    # 2022: Strong operating cash flow, moderate investing, some financing outflows
    # 2023: Reduced operating cash flow, minimal investing, some financing inflows
    # 2024: Improving operating cash flow, increased investing, financing outflows
    
    annual_patterns = {
        2022: {
            # Reduce the base daily values to prevent inflation
            "operating_daily": 5000,  # Reduced from 20000
            "operating_growth": 0.0001,  # Reduced from 0.001 to prevent exponential growth
            "operating_noise": 0.2,
            "investing_monthly": -100000,  # Reduced from -400000
            "investing_noise": 0.3,
            "financing_quarterly": -200000  # Reduced from -800000
        },
        2023: {
            "operating_daily": 4500,  # Reduced from 18000
            "operating_growth": -0.00005,  # Reduced from -0.0005
            "operating_noise": 0.25,
            "investing_monthly": -50000,  # Reduced from -200000
            "investing_noise": 0.3,
            "financing_quarterly": 125000  # Reduced from 500000
        },
        2024: {
            "operating_daily": 5500,  # Reduced from 22000
            "operating_growth": 0.00008,  # Reduced from 0.0008
            "operating_noise": 0.15,
            "investing_monthly": -125000,  # Reduced from -500000
            "investing_noise": 0.25,
            "financing_quarterly": -150000  # Reduced from -600000
        }
    }
    
    # Accounts for each cash flow category
    operating_accounts = [
        account_ids["Cash and Cash Equivalents"]
    ]
    
    investing_accounts = [
        account_ids["Property, Plant & Equipment"],
        account_ids["Long-term Investments"]
    ]
    
    financing_accounts = [
        account_ids["Short-term Loans"],
        account_ids["Long-term Debt"]
    ]
    
    # Generate daily operating cash flows
    daily_flows = []
    
    for i, date in enumerate(date_range):
        year = date.year
        month = date.month
        day = date.day
        quarter = (month - 1) // 3 + 1
        
        # Skip if year not in patterns
        if year not in annual_patterns:
            continue
            
        pattern = annual_patterns[year]
        
        # Operating cash flows - daily entries
        # Base amount with growth and seasonality
        base_amount = pattern["operating_daily"]
        growth_factor = (1 + pattern["operating_growth"]) ** i
        
        # Add seasonality - higher at month and quarter end
        seasonal_factor = 1.0
        if day >= 28:  # Month end
            seasonal_factor = 1.5
        if month in [3, 6, 9, 12] and day >= 28:  # Quarter end
            seasonal_factor = 2.0
            
        # Add some weekly patterns - higher mid-week
        weekday = date.weekday()
        if weekday in [1, 2, 3]:  # Tuesday to Thursday
            seasonal_factor *= 1.2
        elif weekday in [5, 6]:  # Weekend
            seasonal_factor *= 0.4
            
        # Calculate final amount with noise
        amount = base_amount * growth_factor * seasonal_factor
        noise_factor = 1 + random.uniform(-pattern["operating_noise"], pattern["operating_noise"])
        amount *= noise_factor
        
        # Adjust sign based on if it's a collection or payment
        # For operating cash flows, let's say 60% are inflows (collections)
        flow_type = "Inflow" if random.random() < 0.6 else "Outflow"
        if flow_type == "Outflow":
            amount = -amount
            
        # Create the cash flow entry
        daily_flow = (
            date.strftime("%Y-%m-%d"),
            random.choice(operating_accounts),
            abs(amount),  # Store as positive amount
            "Inflow" if amount > 0 else "Outflow",
            "Operating",
            f"Daily operating cash flow on {date.strftime('%Y-%m-%d')}",
            f"OPCF-{date.strftime('%Y%m%d')}",
            year,
            quarter,
            month
        )
        daily_flows.append(daily_flow)
        
        # Investing cash flows - monthly entries, typically outflows for capex
        if day == 15:  # Mid-month investments
            # Base investing amount
            invest_amount = pattern["investing_monthly"]
            
            # Add some variance
            invest_noise = 1 + random.uniform(-pattern["investing_noise"], pattern["investing_noise"])
            invest_amount *= invest_noise
            
            # Investing outflows (negative amounts)
            investing_flow = (
                date.strftime("%Y-%m-%d"),
                random.choice(investing_accounts),
                abs(invest_amount),  # Store as positive amount
                "Outflow",  # Typically outflows for investing
                "Investing",
                f"Capital expenditure for {date.strftime('%Y-%m')}",
                f"INVCF-{date.strftime('%Y%m')}",
                year,
                quarter,
                month
            )
            daily_flows.append(investing_flow)
        
        # Financing cash flows - quarterly entries
        if month in [3, 6, 9, 12] and day == 20:  # Quarterly financing activities
            # Base financing amount
            finance_amount = pattern["financing_quarterly"]
            
            # Add some variance (but less than other categories)
            finance_noise = 1 + random.uniform(-0.1, 0.1) 
            finance_amount *= finance_noise
            
            # Financing can be inflows (borrowing) or outflows (repayments)
            # Based on our scenario: 2022 (repayments), 2023 (borrowing), 2024 (repayments)
            flow_type = "Outflow" if finance_amount < 0 else "Inflow"
            
            financing_flow = (
                date.strftime("%Y-%m-%d"),
                random.choice(financing_accounts),
                abs(finance_amount),  # Store as positive amount
                flow_type,
                "Financing",
                f"{'Debt repayment' if flow_type == 'Outflow' else 'Debt financing'} for Q{quarter} {year}",
                f"FINCF-{year}Q{quarter}",
                year,
                quarter,
                month
            )
            daily_flows.append(financing_flow)
    
    # Write to CSV
    with open(f"{OUTPUT_DIR}/cash_flow.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["cash_flow_id", "transaction_date", "account_id", "amount", 
                        "flow_type", "category", "description", "reference_number", 
                        "fiscal_year", "fiscal_quarter", "fiscal_month"])
        for i, flow in enumerate(daily_flows, 1):
            writer.writerow([i] + list(flow))
    
    return daily_flows

# Generate capital expenditures
def generate_capital_expenditures():
    """Generate capital expenditure data."""
    # Asset types
    asset_types = [
        "Building", "Machinery", "Equipment", "Vehicle", "Office Equipment",
        "Computer Hardware", "Computer Software", "Land", "Leasehold Improvements"
    ]
    
    # Depreciation methods
    depreciation_methods = ["Straight Line", "Double Declining Balance", "Units of Production"]
    
    # Departments
    departments = ["Manufacturing", "Administration", "Sales", "R&D", "Logistics", "IT"]
    
    # Project managers
    project_managers = [
        "Richard Johnson", "Michael Harris", "Thomas Davis", "Christopher Evans",
        "David Wright", "Jessica Wilson", "Daniel Miller", "Patricia Garcia",
        "Jennifer Wilson", "Elizabeth Taylor"
    ]
    
    # Statuses with weights
    statuses = ["Planned", "In Progress", "Completed", "Cancelled"]
    status_weights = [0.1, 0.15, 0.7, 0.05]  # Most are completed
    
    # Planned capital expenditures
    # Our story: 
    # 2022: Normal capex
    # 2023: Reduced capex during challenges
    # 2024: Increased capex for growth
    
    capex_records = []
    
    # 2022 - Normal capex program
    for i in range(1, 16):
        purchase_date = fake.date_between(
            start_date=datetime.date(2022, 1, 1),
            end_date=datetime.date(2022, 12, 31)
        )
        
        asset_type = random.choice(asset_types)
        useful_life = get_useful_life(asset_type)
        cost = get_asset_cost(asset_type, 2022)
        depr_method = get_depreciation_method(asset_type)
        annual_depr = get_annual_depreciation(cost, useful_life, depr_method)
        
        # Accumulate depreciation based on time since purchase
        days_since_purchase = (END_DATE - purchase_date).days
        years_since_purchase = days_since_purchase / 365.0
        accum_depr = min(annual_depr * years_since_purchase, cost)
        
        # Calculate net book value
        nbv = cost - accum_depr
        
        # Approval date is typically before purchase
        approval_date = (purchase_date - datetime.timedelta(days=random.randint(30, 90))).strftime("%Y-%m-%d")
        
        # Project status (most 2022 projects are completed)
        status = random.choices(statuses, weights=[0.0, 0.05, 0.9, 0.05], k=1)[0]
        
        capex_record = (
            f"2022 {asset_type} Project {i}",
            asset_type,
            purchase_date.strftime("%Y-%m-%d"),
            cost,
            useful_life,
            depr_method,
            annual_depr,
            accum_depr,
            nbv,
            random.choice(departments),
            random.choice(project_managers),
            approval_date,
            status
        )
        capex_records.append(capex_record)
    
    # 2023 - Reduced capex during challenging year
    for i in range(1, 9):  # Fewer projects
        purchase_date = fake.date_between(
            start_date=datetime.date(2023, 1, 1),
            end_date=datetime.date(2023, 12, 31)
        )
        
        asset_type = random.choice(asset_types)
        useful_life = get_useful_life(asset_type)
        cost = get_asset_cost(asset_type, 2023) * 0.85  # Lower cost due to budget constraints
        depr_method = get_depreciation_method(asset_type)
        annual_depr = get_annual_depreciation(cost, useful_life, depr_method)
        
        # Accumulate depreciation based on time since purchase
        days_since_purchase = (END_DATE - purchase_date).days
        years_since_purchase = days_since_purchase / 365.0
        accum_depr = min(annual_depr * years_since_purchase, cost)
        
        # Calculate net book value
        nbv = cost - accum_depr
        
        # Approval date is typically before purchase
        approval_date = (purchase_date - datetime.timedelta(days=random.randint(30, 90))).strftime("%Y-%m-%d")
        
        # Project status (mix of completed and in progress for 2023)
        status = random.choices(statuses, weights=[0.0, 0.2, 0.75, 0.05], k=1)[0]
        
        capex_record = (
            f"2023 {asset_type} Project {i}",
            asset_type,
            purchase_date.strftime("%Y-%m-%d"),
            cost,
            useful_life,
            depr_method,
            annual_depr,
            accum_depr,
            nbv,
            random.choice(departments),
            random.choice(project_managers),
            approval_date,
            status
        )
        capex_records.append(capex_record)
    
    # 2024 - Increased capex for growth
    for i in range(1, 20):  # More projects as company recovers
        purchase_date = fake.date_between(
            start_date=datetime.date(2024, 1, 1),
            end_date=datetime.date(2024, 12, 31)
        )
        
        # For dates in the future, adjust to be "planned"
        if purchase_date > datetime.date.today():
            actual_purchase_date = None
            status = "Planned"
        else:
            actual_purchase_date = purchase_date
            # Mix of statuses for 2024 projects
            status = random.choices(statuses, weights=[0.2, 0.3, 0.45, 0.05], k=1)[0]
        
        asset_type = random.choice(asset_types)
        useful_life = get_useful_life(asset_type)
        cost = get_asset_cost(asset_type, 2024) * 1.1  # Higher investments
        depr_method = get_depreciation_method(asset_type)
        annual_depr = get_annual_depreciation(cost, useful_life, depr_method)
        
        # Accumulate depreciation only if purchased
        if actual_purchase_date:
            days_since_purchase = (END_DATE - actual_purchase_date).days
            years_since_purchase = days_since_purchase / 365.0
            accum_depr = min(annual_depr * years_since_purchase, cost)
            nbv = cost - accum_depr
        else:
            accum_depr = 0
            nbv = cost
        
        # Approval date is typically before purchase
        if status == "Planned":
            approval_date = (datetime.date.today() - datetime.timedelta(days=random.randint(10, 60))).strftime("%Y-%m-%d")
            purchase_date_str = None
        else:
            approval_date = (purchase_date - datetime.timedelta(days=random.randint(30, 90))).strftime("%Y-%m-%d")
            purchase_date_str = purchase_date.strftime("%Y-%m-%d")
        
        capex_record = (
            f"2024 {asset_type} Project {i}",
            asset_type,
            purchase_date_str,
            cost,
            useful_life,
            depr_method,
            annual_depr,
            accum_depr,
            nbv,
            random.choice(departments),
            random.choice(project_managers),
            approval_date,
            status
        )
        capex_records.append(capex_record)
    
    # Write to CSV
    with open(f"{OUTPUT_DIR}/capital_expenditures.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["capex_id", "project_name", "asset_type", "purchase_date", 
                        "acquisition_cost", "expected_useful_life_years", "depreciation_method", 
                        "annual_depreciation", "accumulated_depreciation", "net_book_value", 
                        "department", "project_manager", "approval_date", "status"])
        for i, capex in enumerate(capex_records, 1):
            writer.writerow([i] + list(capex))

# Helper functions for capital expenditures
def get_useful_life(asset_type):
    """Return realistic useful life for different asset types."""
    useful_life_ranges = {
        "Building": (20, 40),
        "Machinery": (7, 15),
        "Equipment": (5, 10),
        "Vehicle": (3, 7),
        "Office Equipment": (5, 10),
        "Computer Hardware": (3, 5),
        "Computer Software": (3, 5),
        "Land": (0, 0),  # Land doesn't depreciate
        "Leasehold Improvements": (5, 15)
    }
    
    range_for_type = useful_life_ranges.get(asset_type, (5, 10))
    return random.randint(*range_for_type)

def get_asset_cost(asset_type, year):
    """Return realistic cost ranges for different asset types."""
    # Base cost ranges
    cost_ranges = {
        "Building": (500000, 5000000),
        "Machinery": (50000, 500000),
        "Equipment": (10000, 100000),
        "Vehicle": (25000, 75000),
        "Office Equipment": (5000, 50000),
        "Computer Hardware": (2000, 20000),
        "Computer Software": (10000, 150000),
        "Land": (200000, 2000000),
        "Leasehold Improvements": (20000, 200000)
    }
    
    # Apply year-specific modifiers
    year_modifiers = {
        2022: 1.0,     # Base year
        2023: 0.9,     # Cost-cutting
        2024: 1.15     # Growth investments
    }
    
    range_for_type = cost_ranges.get(asset_type, (10000, 100000))
    base_cost = random.uniform(*range_for_type)
    return base_cost * year_modifiers.get(year, 1.0)

def get_depreciation_method(asset_type):
    """Return appropriate depreciation method for asset type."""
    # Different asset types use different depreciation methods with different probabilities
    depreciation_probs = {
        "Building": [0.8, 0.15, 0.05],            # Mostly straight line
        "Machinery": [0.4, 0.5, 0.1],             # Mix of methods
        "Equipment": [0.5, 0.4, 0.1],             # Mix of methods
        "Vehicle": [0.3, 0.6, 0.1],               # Mostly declining balance
        "Office Equipment": [0.7, 0.25, 0.05],    # Mostly straight line
        "Computer Hardware": [0.6, 0.35, 0.05],   # Mostly straight line
        "Computer Software": [0.9, 0.1, 0.0],     # Almost always straight line
        "Land": [1.0, 0.0, 0.0],                  # Land doesn't depreciate
        "Leasehold Improvements": [0.95, 0.05, 0.0]  # Almost always straight line
    }
    
    methods = ["Straight Line", "Double Declining Balance", "Units of Production"]
    probs = depreciation_probs.get(asset_type, [0.6, 0.3, 0.1])  # Default probabilities
    
    return random.choices(methods, weights=probs, k=1)[0]

def get_annual_depreciation(cost, useful_life, method):
    """Calculate annual depreciation amount based on method."""
    if method == "Straight Line":
        return cost / useful_life if useful_life > 0 else 0
    elif method == "Double Declining Balance":
        # Simplified DDB
        return (cost * 2) / useful_life if useful_life > 0 else 0
    else:  # Units of Production
        # Simplified approximation
        return cost / (useful_life * 0.8) if useful_life > 0 else 0

# Generate debt instruments
def generate_debt_instruments():
    """Generate debt instruments data."""
    # Types of debt instruments
    instrument_types = ["Term Loan", "Revolving Credit", "Bond", "Note Payable", "Lease"]
    
    # Lenders
    lenders = [
        "First National Bank", "Global Financial Group", "Industrial Lenders Inc.",
        "Pacific Investment Trust", "Atlantic Capital Partners", "Eastern Credit Union",
        "Mountain State Bank", "Midwest Financing Corp", "Southern Trust & Investments"
    ]
    
    # Payment frequencies
    payment_freqs = ["Monthly", "Quarterly", "Semi-Annual", "Annual"]
    
    # Our debt story:
    # 2022: Steady debt repayment
    # 2023: Additional financing during challenges
    # 2024: Returning to debt reduction
    
    debt_records = []
    
    # Long-term debt from before our period
    legacy_debts = [
        # Term loans for equipment
        ("Manufacturing Equipment Loan", "Term Loan", "First National Bank", 3000000,
         0.045, "Fixed", "2019-06-15", "2026-06-15", "Monthly", 42500, 1650000,
         True, "Manufacturing equipment", "Debt/EBITDA < 3.0, Current ratio > 1.2"),
        
        # Bond issuance
        ("2020 Corporate Bond", "Bond", "Global Financial Group", 10000000,
         0.052, "Fixed", "2020-03-20", "2030-03-20", "Semi-Annual", 260000, 10000000,
         False, None, "Debt/EBITDA < 3.5, Interest coverage > 2.5"),
        
        # Revolving credit facility
        ("Revolving Credit Facility", "Revolving Credit", "Industrial Lenders Inc.", 5000000,
         0.048, "Variable", "2021-01-10", "2025-01-10", "Monthly", None, 2700000,
         True, "Accounts receivable", "Debt/EBITDA < 3.0, Current ratio > 1.2"),
        
        # Building mortgage
        ("Headquarters Mortgage", "Term Loan", "Pacific Investment Trust", 8500000,
         0.043, "Fixed", "2018-11-05", "2038-11-05", "Monthly", 39500, 7200000,
         True, "Headquarters building", "Debt/EBITDA < 3.5, Current ratio > 1.0")
    ]
    debt_records.extend(legacy_debts)
    
    # 2022 new debt - mostly equipment financing
    debt_2022 = [
        ("2022 Equipment Lease", "Lease", "Atlantic Capital Partners", 850000,
         0.047, "Fixed", "2022-04-12", "2027-04-12", "Monthly", 16500, 680000,
         True, "Production equipment", "None"),
        
        ("Warehouse Expansion Loan", "Term Loan", "Mountain State Bank", 1200000,
         0.049, "Fixed", "2022-08-22", "2032-08-22", "Monthly", 12700, 1100000,
         True, "Warehouse property", "Debt/EBITDA < 3.5")
    ]
    debt_records.extend(debt_2022)
    
    # 2023 new debt - additional financing during challenges
    debt_2023 = [
        ("2023 Working Capital Loan", "Term Loan", "Midwest Financing Corp", 2000000,
         0.058, "Variable", "2023-05-18", "2026-05-18", "Monthly", 60800, 1750000,
         True, "Inventory and receivables", "Current ratio > 1.0, Quick ratio > 0.6"),
        
        ("2023 Refinancing Bond", "Bond", "Southern Trust & Investments", 5000000,
         0.056, "Fixed", "2023-09-30", "2030-09-30", "Semi-Annual", 140000, 5000000,
         False, None, "Debt/EBITDA < 3.5, Interest coverage > 2.0")
    ]
    debt_records.extend(debt_2023)
    
    # 2024 new debt - strategic investments for growth
    debt_2024 = [
        ("2024 Technology Infrastructure", "Term Loan", "Eastern Credit Union", 1500000,
         0.062, "Fixed", "2024-02-15", "2029-02-15", "Monthly", 29100, 1450000,
         True, "Technology assets", "Debt/EBITDA < 3.0"),
        
        ("R&D Facility Expansion", "Term Loan", "First National Bank", 2800000,
         0.059, "Fixed", "2024-06-22", "2034-06-22", "Monthly", 27500, 2800000,
         True, "R&D facility", "Debt/EBITDA < 3.5, Interest coverage > 2.5")
    ]
    debt_records.extend(debt_2024)
    
    # Write to CSV
    with open(f"{OUTPUT_DIR}/debt_instruments.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["debt_id", "instrument_name", "instrument_type", "lender_name", 
                        "principal_amount", "interest_rate", "interest_type", 
                        "origination_date", "maturity_date", "payment_frequency", 
                        "payment_amount", "outstanding_balance", "is_secured", 
                        "collateral_description", "covenant_details"])
        for i, debt in enumerate(debt_records, 1):
            writer.writerow([i] + list(debt))

# Generate purchase orders
def generate_purchase_orders(suppliers, products):
    """Generate purchase order data."""
    # Generate POs for the period
    purchase_orders = []
    po_items = []
    
    po_id = 1
    po_item_id = 1
    
    # Number of POs per year reflects our story:
    # 2022: Normal operations
    # 2023: Reduced purchasing during challenges
    # 2024: Increased purchasing for growth
    
    po_counts = {
        2022: 150,
        2023: 120,
        2024: 170
    }
    
    supplier_ids = list(suppliers.keys())
    product_ids = list(products.keys())
    
    for year in [2022, 2023, 2024]:
        # Generate POs for this year
        num_pos = po_counts[year]
        
        # Distribute throughout the year, with some seasonality
        # Q1: 20%, Q2: 25%, Q3: 25%, Q4: 30%
        q_pcts = [0.2, 0.25, 0.25, 0.3]
        
        for quarter in range(1, 5):
            # Skip future quarters
            if year == datetime.date.today().year and quarter > ((datetime.date.today().month - 1) // 3 + 1):
                continue
                
            # Number of POs for this quarter
            q_pos = int(num_pos * q_pcts[quarter-1])
            
            # Generate dates for this quarter
            quarter_start = datetime.date(year, 1 + (quarter-1)*3, 1)
            quarter_end_month = min(quarter*3, 12)  # Ensure month isn't > 12
            if quarter_end_month == 12:
                quarter_end = datetime.date(year, quarter_end_month, 31)
            else:
                next_month = quarter_end_month + 1
                next_month_year = year + (next_month // 13)  # In case we need to roll to next year
                next_month = ((next_month - 1) % 12) + 1  # Ensure month is 1-12
                quarter_end = datetime.date(next_month_year, next_month, 1) - datetime.timedelta(days=1)
            
            # Skip if end date is in the future
            if quarter_end > datetime.date.today():
                continue
                
            po_dates = [fake.date_between(start_date=quarter_start, end_date=quarter_end) for _ in range(q_pos)]
            po_dates.sort()  # Ensure dates are in order
            
            for po_date in po_dates:
                supplier_id = random.choice(supplier_ids)
                supplier = suppliers[supplier_id]
                
                # PO details
                po_number = f"PO-{year}{quarter:02d}-{po_id:04d}"
                
                # Expected delivery depends on supplier lead time
                lead_time = supplier[9]  # lead_time_days from supplier data
                expected_delivery = po_date + datetime.timedelta(days=lead_time)
                
                # Actual delivery is usually close to expected, but can vary
                delivery_variance = random.randint(-5, 10)  # -5 to +10 days
                actual_delivery = expected_delivery + datetime.timedelta(days=delivery_variance)
                
                # Determine status based on dates
                if po_date > datetime.date.today():
                    status = "Draft"
                    actual_delivery = None
                elif expected_delivery > datetime.date.today():
                    status = random.choice(["Submitted", "Approved", "Shipped"])
                    actual_delivery = None
                else:
                    status = "Received"
                
                # Payment status
                if status == "Received":
                    payment_status = random.choices(
                        ["Unpaid", "Partially Paid", "Paid"],
                        weights=[0.1, 0.2, 0.7],
                        k=1
                    )[0]
                else:
                    payment_status = "Unpaid"
                
                # Generate 1-5 items for this PO
                num_items = random.randint(1, 5)
                po_products = random.sample(product_ids, num_items)
                
                total_amount = 0
                for product_id in po_products:
                    product_code = products[product_id]["code"]
                    product_name = products[product_id]["name"]
                    base_cost = products[product_id]["base_cost"]
                    list_price = products[product_id]["list_price"]
                    unit_id = products[product_id]["unit_id"]
                    
                    # Quantity and pricing
                    quantity = random.randint(1, 10)
                    # Unit price is typically between 90-105% of base cost
                    unit_price = base_cost * random.uniform(0.9, 1.05)
                    line_total = quantity * unit_price
                    total_amount += line_total
                    
                    # Received quantity depends on status
                    if status == "Received":
                        # Most orders received in full, but some not
                        if random.random() < 0.9:
                            received_quantity = quantity
                        else:
                            received_quantity = random.randint(0, quantity)
                    else:
                        received_quantity = 0
                    
                    po_item = (
                        po_id,
                        product_id,
                        quantity,
                        unit_price,
                        line_total,
                        received_quantity
                    )
                    po_items.append(po_item)
                    po_item_id += 1
                
                # Create the PO record
                po = (
                    po_number,
                    supplier_id,
                    po_date.strftime("%Y-%m-%d"),
                    expected_delivery.strftime("%Y-%m-%d"),
                    actual_delivery.strftime("%Y-%m-%d") if actual_delivery else None,
                    total_amount,
                    status,
                    payment_status,
                    f"Order for {num_items} product(s)"
                )
                purchase_orders.append(po)
                po_id += 1
    
    # Write to CSV
    with open(f"{OUTPUT_DIR}/purchase_orders.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["po_id", "po_number", "supplier_id", "order_date", 
                        "expected_delivery_date", "actual_delivery_date", 
                        "total_amount", "status", "payment_status", "notes"])
        for i, po in enumerate(purchase_orders, 1):
            writer.writerow([i] + list(po))
    
    with open(f"{OUTPUT_DIR}/po_items.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["item_id", "po_id", "product_id", "quantity", 
                        "unit_price", "line_total", "received_quantity"])
        for i, item in enumerate(po_items, 1):
            writer.writerow([i] + list(item))
    
    return purchase_orders, po_items

# Generate sales orders
def generate_sales_orders(customers, products, business_units):
    """Generate sales order data."""
    # Generate orders for the period
    orders = []
    order_items = []
    
    order_id = 1
    item_id = 1
    
    # Number of orders per year reflects our story:
    # 2022: Strong growth
    # 2023: Challenges
    # 2024: Recovery
    
    order_counts = {
        2022: 300,
        2023: 280,
        2024: 320
    }
    
    customer_ids = list(customers.keys())
    product_ids = list(products.keys())
    unit_ids = list(business_units.keys())
    
    # Shipping methods
    shipping_methods = ["Standard", "Express", "Freight", "International", "Customer Pickup"]
    
    # Sales reps
    sales_reps = [
        "Patricia Garcia", "Sophia Chen", "David Martinez", "William Johnson",
        "Emily Rodriguez", "Michael Thompson", "Jessica Wilson", "Robert Davis",
        "Sarah Martinez", "James Baker"
    ]
    
    for year in [2022, 2023, 2024]:
        # Generate orders for this year
        num_orders = order_counts[year]
        
        # Distribute throughout the year, with some seasonality
        # Q1: 20%, Q2: 25%, Q3: 25%, Q4: 30%
        q_pcts = [0.2, 0.25, 0.25, 0.3]
        
        for quarter in range(1, 5):
            # Skip future quarters
            if year == datetime.date.today().year and quarter > ((datetime.date.today().month - 1) // 3 + 1):
                continue
                
            # Number of orders for this quarter
            q_orders = int(num_orders * q_pcts[quarter-1])
            
            # Generate dates for this quarter
            quarter_start = datetime.date(year, 1 + (quarter-1)*3, 1)
            quarter_end_month = min(quarter*3, 12)  # Ensure month isn't > 12
            if quarter_end_month == 12:
                quarter_end = datetime.date(year, quarter_end_month, 31)
            else:
                next_month = quarter_end_month + 1
                next_month_year = year + (next_month // 13)
                next_month = ((next_month - 1) % 12) + 1
                quarter_end = datetime.date(next_month_year, next_month, 1) - datetime.timedelta(days=1)
            
            # Skip if end date is in the future
            if quarter_end > datetime.date.today():
                continue
                
            order_dates = [fake.date_between(start_date=quarter_start, end_date=quarter_end) for _ in range(q_orders)]
            order_dates.sort()  # Ensure dates are in order
            
            for order_date in order_dates:
                customer_id = random.choice(customer_ids)
                customer = customers[customer_id]
                unit_id = random.choice(unit_ids)
                
                # Order details
                order_number = f"SO-{year}{quarter:02d}-{order_id:04d}"
                
                # Required date is typically 10-30 days after order
                required_date = order_date + datetime.timedelta(days=random.randint(10, 30))
                
                # Shipped date depends on required date
                if required_date <= datetime.date.today():
                    # 90% on time, 10% late
                    if random.random() < 0.9:
                        days_to_ship = random.randint(5, (required_date - order_date).days)
                    else:
                        days_to_ship = (required_date - order_date).days + random.randint(1, 10)
                    
                    shipped_date = order_date + datetime.timedelta(days=days_to_ship)
                    
                    # Status based on shipped date
                    if shipped_date <= datetime.date.today() - datetime.timedelta(days=7):
                        status = "Delivered"
                    else:
                        status = "Shipped"
                else:
                    # Future order
                    if order_date <= datetime.date.today():
                        status = random.choice(["New", "Processing"])
                    else:
                        status = "New"
                    shipped_date = None
                
                # Payment status
                if status == "Delivered":
                    payment_status = random.choices(
                        ["Unpaid", "Partially Paid", "Paid"],
                        weights=[0.05, 0.15, 0.8],
                        k=1
                    )[0]
                elif status == "Shipped":
                    payment_status = random.choices(
                        ["Unpaid", "Partially Paid", "Paid"],
                        weights=[0.3, 0.5, 0.2],
                        k=1
                    )[0]
                else:
                    payment_status = "Unpaid"
                
                # Shipping info
                shipping_method = random.choice(shipping_methods)
                shipping_cost = random.uniform(50, 500) if shipping_method != "Customer Pickup" else 0
                
                # Generate 1-5 items for this order
                num_items = random.randint(1, 5)
                order_products = random.sample(product_ids, num_items)
                
                subtotal = 0
                for product_id in order_products:
                    product_code = products[product_id]["code"]
                    product_name = products[product_id]["name"]
                    base_cost = products[product_id]["base_cost"]
                    list_price = products[product_id]["list_price"]
                    product_unit_id = products[product_id]["unit_id"]
                    
                    # Only include products from this business unit or general products
                    if product_unit_id not in [1, 2, unit_id]:
                        continue
                    
                    # Quantity and pricing
                    quantity = random.randint(1, 5)
                    
                    # Potential discount
                    discount_pct = 0
                    if random.random() < 0.3:  # 30% chance of discount
                        discount_pct = random.uniform(0.05, 0.2)  # 5-20% discount
                    
                    # Final price
                    unit_price = list_price * (1 - discount_pct)
                    line_total = quantity * unit_price
                    subtotal += line_total
                    
                    order_item = (
                        order_id,
                        product_id,
                        quantity,
                        unit_price,
                        discount_pct * 100,  # Convert to percentage
                        line_total
                    )
                    order_items.append(order_item)
                    item_id += 1
                
                # If no valid items were added (due to unit filtering), skip this order
                if len(order_items) == 0:
                    continue
                
                # Add tax and calculate total
                tax_rate = 0.07  # 7% tax
                tax_amount = subtotal * tax_rate
                discount_amount = 0
                if random.random() < 0.1:  # 10% chance of order-level discount
                    discount_amount = subtotal * random.uniform(0.02, 0.1)
                
                total_amount = subtotal + tax_amount - discount_amount + shipping_cost
                
                # Ship to address
                ship_to_address = fake.address().replace('\n', ', ')
                
                # Sales rep
                sales_rep = random.choice(sales_reps)
                
                # Create the order record
                order = (
                    order_number,
                    customer_id,
                    order_date.strftime("%Y-%m-%d"),
                    required_date.strftime("%Y-%m-%d"),
                    shipped_date.strftime("%Y-%m-%d") if shipped_date else None,
                    ship_to_address,
                    shipping_method,
                    shipping_cost,
                    sales_rep,
                    unit_id,
                    subtotal,
                    tax_amount,
                    discount_amount,
                    total_amount,
                    status,
                    payment_status
                )
                orders.append(order)
                order_id += 1
    
    # Write to CSV
    with open(f"{OUTPUT_DIR}/sales_orders.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["order_id", "order_number", "customer_id", "order_date", 
                        "required_date", "shipped_date", "ship_to_address", 
                        "shipping_method", "shipping_cost", "sales_rep", "unit_id", 
                        "subtotal", "tax_amount", "discount_amount", "total_amount", 
                        "status", "payment_status"])
        for i, order in enumerate(orders, 1):
            writer.writerow([i] + list(order))
    
    with open(f"{OUTPUT_DIR}/order_items.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["item_id", "order_id", "product_id", "quantity", 
                        "unit_price", "discount_percentage", "line_total"])
        for i, item in enumerate(order_items, 1):
            writer.writerow([i] + list(item))
    
    return orders, order_items

# Generate marketing campaigns
def generate_marketing_campaigns(regions):
    """Generate marketing campaign data."""
    # Campaign types
    campaign_types = [
        "Product Launch", "Brand Awareness", "Trade Show", "Direct Mail",
        "Email Campaign", "Social Media", "Content Marketing", "Webinar",
        "Digital Advertising", "Customer Retention"
    ]
    
    # Target audiences
    target_audiences = [
        "Industrial Manufacturers", "Construction Companies", "Technology Firms",
        "Healthcare Facilities", "Retail Chains", "Small Businesses",
        "Enterprise Clients", "Government Contractors", "Educational Institutions"
    ]
    
    # Target products (simplified - just use descriptions)
    target_products = [
        "Industrial Equipment", "Manufacturing Tools", "Electrical Components",
        "Consumer Electronics", "Smart Home Products", "All Products"
    ]
    
    # Campaign patterns per year
    # 2022: Normal marketing spend
    # 2023: Reduced marketing during challenges
    # 2024: Increased strategic marketing for growth
    
    campaigns = []
    
    # 2022 Campaigns
    for i in range(1, 16):
        # Campaign duration 30-90 days
        start_date = fake.date_between(
            start_date=datetime.date(2022, 1, 1),
            end_date=datetime.date(2022, 10, 31)  # Allow campaigns to end in 2022
        )
        duration = random.randint(30, 90)
        end_date = start_date + datetime.timedelta(days=duration)
        
        campaign_type = random.choice(campaign_types)
        budget = get_campaign_budget(campaign_type, 2022)
        
        # 2022 campaigns were mostly completed and successful
        status = "Completed"
        
        # Actual spend is close to budget
        spend_factor = random.uniform(0.9, 1.05)
        actual_spend = budget * spend_factor
        
        # Expected and actual revenue
        expected_revenue = budget * random.uniform(2.5, 4.0)  # Expected ROI 2.5-4x
        actual_revenue = actual_spend * random.uniform(2.2, 3.8)  # Actual ROI 2.2-3.8x
        
        # ROI calculation
        roi = ((actual_revenue - actual_spend) / actual_spend) * 100 if actual_spend > 0 else 0
        
        region_id = random.choice(list(regions.keys()))
        
        campaign = (
            f"2022 {campaign_type} Campaign {i}",
            campaign_type,
            start_date.strftime("%Y-%m-%d"),
            end_date.strftime("%Y-%m-%d"),
            budget,
            actual_spend,
            random.choice(target_audiences),
            region_id,
            random.choice(target_products),
            expected_revenue,
            actual_revenue,
            roi,
            status
        )
        campaigns.append(campaign)
    
    # 2023 Campaigns - fewer campaigns with lower budgets
    for i in range(1, 10):
        start_date = fake.date_between(
            start_date=datetime.date(2023, 1, 1),
            end_date=datetime.date(2023, 10, 31)
        )
        duration = random.randint(30, 90)
        end_date = start_date + datetime.timedelta(days=duration)
        
        campaign_type = random.choice(campaign_types)
        budget = get_campaign_budget(campaign_type, 2023) * 0.8  # Reduced budgets
        
        # 2023 campaigns were mostly completed but with mixed results
        status = "Completed"
        
        # Tighter control on spending during challenging year
        spend_factor = random.uniform(0.85, 1.0)
        actual_spend = budget * spend_factor
        
        # Expected and actual revenue - lower ROI during challenging year
        expected_revenue = budget * random.uniform(2.0, 3.5)
        actual_revenue = actual_spend * random.uniform(1.8, 3.0)
        
        # ROI calculation
        roi = ((actual_revenue - actual_spend) / actual_spend) * 100 if actual_spend > 0 else 0
        
        region_id = random.choice(list(regions.keys()))
        
        campaign = (
            f"2023 {campaign_type} Campaign {i}",
            campaign_type,
            start_date.strftime("%Y-%m-%d"),
            end_date.strftime("%Y-%m-%d"),
            budget,
            actual_spend,
            random.choice(target_audiences),
            region_id,
            random.choice(target_products),
            expected_revenue,
            actual_revenue,
            roi,
            status
        )
        campaigns.append(campaign)
    
    # 2024 Campaigns - more strategic campaigns with higher budgets
    for i in range(1, 20):
        start_date = fake.date_between(
            start_date=datetime.date(2024, 1, 1),
            end_date=datetime.date(2024, 10, 31)
        )
        duration = random.randint(30, 90)
        end_date = start_date + datetime.timedelta(days=duration)
        
        # Handle future campaigns
        is_future = start_date > datetime.date.today()
        is_ongoing = start_date <= datetime.date.today() and end_date >= datetime.date.today()
        
        campaign_type = random.choice(campaign_types)
        budget = get_campaign_budget(campaign_type, 2024) * 1.2  # Increased budgets for growth
        
        # Status depends on dates
        if is_future:
            status = "Planning"
            actual_spend = None
            actual_revenue = None
            roi = None
        elif is_ongoing:
            status = "Active"
            # Partial spend for ongoing campaigns
            days_active = (datetime.date.today() - start_date).days
            total_days = (end_date - start_date).days
            spend_pct = days_active / total_days if total_days > 0 else 0
            actual_spend = budget * spend_pct * random.uniform(0.9, 1.05)
            actual_revenue = None  # Still calculating
            roi = None
        else:
            status = "Completed"
            spend_factor = random.uniform(0.95, 1.02)
            actual_spend = budget * spend_factor
            # Better ROI in 2024 as strategy improves
            actual_revenue = actual_spend * random.uniform(2.5, 4.2)
            roi = ((actual_revenue - actual_spend) / actual_spend) * 100 if actual_spend > 0 else 0
        
        # Expected revenue 
        expected_revenue = budget * random.uniform(2.8, 4.5)  # Higher expectations for 2024
        
        region_id = random.choice(list(regions.keys()))
        
        campaign = (
            f"2024 {campaign_type} Campaign {i}",
            campaign_type,
            start_date.strftime("%Y-%m-%d"),
            end_date.strftime("%Y-%m-%d"),
            budget,
            actual_spend,
            random.choice(target_audiences),
            region_id,
            random.choice(target_products),
            expected_revenue,
            actual_revenue,
            roi,
            status
        )
        campaigns.append(campaign)
    
    # Write to CSV
    with open(f"{OUTPUT_DIR}/marketing_campaigns.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["campaign_id", "campaign_name", "campaign_type", 
                        "start_date", "end_date", "budget", "actual_spend", 
                        "target_audience", "target_region", "target_products", 
                        "expected_revenue", "actual_revenue", "roi_percentage", "status"])
        for i, campaign in enumerate(campaigns, 1):
            writer.writerow([i] + list(campaign))

# Helper for marketing campaigns
def get_campaign_budget(campaign_type, year):
    """Return a realistic budget range based on campaign type and year."""
    # Base budget ranges by campaign type
    budget_ranges = {
        "Product Launch": (75000, 250000),
        "Brand Awareness": (50000, 150000),
        "Trade Show": (25000, 100000),
        "Direct Mail": (15000, 50000),
        "Email Campaign": (5000, 25000),
        "Social Media": (10000, 75000),
        "Content Marketing": (15000, 60000),
        "Webinar": (8000, 30000),
        "Digital Advertising": (20000, 120000),
        "Customer Retention": (10000, 40000)
    }
    
    # Year modifiers to reflect our story
    year_modifiers = {
        2022: 1.0,    # Base year
        2023: 0.75,   # Reduced marketing during challenges
        2024: 1.15    # Increased marketing for growth
    }
    
    range_for_type = budget_ranges.get(campaign_type, (10000, 50000))
    base_budget = random.uniform(*range_for_type)
    return base_budget * year_modifiers.get(year, 1.0)

# Main function
def main():
    print("Generating due diligence demo data...")
    
    # Create data in the correct order (respecting dependencies)
    print("Generating regions data...")
    regions = generate_regions()
    
    print("Generating business units data...")
    business_units = generate_business_units(regions)
    
    print("Generating chart of accounts...")
    account_ids = generate_chart_of_accounts()
    
    print("Generating product categories...")
    categories = generate_product_categories()
    
    print("Generating products...")
    products = generate_products(categories, business_units)
    
    print("Generating customers...")
    customers = generate_customers(regions)
    
    print("Generating customer contacts...")
    generate_customer_contacts(customers)
    
    print("Generating suppliers...")
    suppliers = generate_suppliers()
    
    print("Generating inventory...")
    inventory = generate_inventory(products)
    
    print("Generating inventory movements...")
    generate_inventory_movements(inventory)
    
    print("Generating departments...")
    generate_departments()
    
    print("Generating general ledger entries...")
    generate_general_ledger(account_ids)
    
    print("Generating financial statements...")
    generate_financial_statements(account_ids)
    
    print("Generating budget vs actual data...")
    generate_budget_vs_actual(account_ids)
    
    print("Generating cash flow data...")
    generate_cash_flow(account_ids)
    
    print("Generating capital expenditures...")
    generate_capital_expenditures()
    
    print("Generating debt instruments...")
    generate_debt_instruments()
    
    print("Generating purchase orders...")
    generate_purchase_orders(suppliers, products)
    
    print("Generating sales orders...")
    generate_sales_orders(customers, products, business_units)
    
    print("Generating marketing campaigns...")
    generate_marketing_campaigns(regions)
    
    print("Data generation complete!")

if __name__ == "__main__":
    main()