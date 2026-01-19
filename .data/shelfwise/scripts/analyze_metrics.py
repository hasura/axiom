#!/usr/bin/env python3
"""
Analyze ShelfWise generated data against industry benchmark metrics.
Usage: python3 analyze_metrics.py <output_directory>
"""
import csv
import sys
from collections import defaultdict
from datetime import datetime

if len(sys.argv) < 2:
    print("Usage: python3 analyze_metrics.py <output_directory>")
    print("Example: python3 analyze_metrics.py .data/shelfwise/generator/output")
    sys.exit(1)

data_dir = sys.argv[1]

print(f"Analyzing data in: {data_dir}")
print("Loading data...")
txns = list(csv.DictReader(open(f"{data_dir}/transactions.csv")))
print(f"Transactions: {len(txns):,}")

# ABV
basket_values = [float(t['total_amount']) for t in txns]
avg_bv = sum(basket_values) / len(basket_values)
print(f"\n=== BASKET METRICS ===")
print(f"Average Basket Value: ${avg_bv:.2f} (target $45-65)")

# Store metrics
sales_by_store = defaultdict(float)
txns_by_store = defaultdict(int)
dates_seen = set()
for t in txns:
    sales_by_store[t['store_id']] += float(t['total_amount'])
    txns_by_store[t['store_id']] += 1
    dates_seen.add(t['date'])

total_revenue = sum(sales_by_store.values())
num_stores = len(sales_by_store)
num_days = len(dates_seen)
weeks = num_days / 7

print(f"\n=== STORE METRICS ===")
print(f"Date range: {num_days} days ({weeks:.1f} weeks)")
print(f"Total Revenue: ${total_revenue:,.0f}")
print(f"Stores: {num_stores}")
print(f"Weekly Revenue/Store: ${total_revenue/num_stores/weeks:,.0f} (target $450K-950K)")
print(f"Weekly Txns/Store: {len(txns)/num_stores/weeks:,.0f} (target 10K-15K)")

# Loyalty
loyalty_txns = sum(1 for t in txns if t['is_loyalty_transaction'] == 'true')
print(f"\n=== CUSTOMER METRICS ===")
print(f"Loyalty Penetration: {loyalty_txns/len(txns)*100:.1f}% (target 70-85%)")

# Fulfillment
delivery = sum(1 for t in txns if t['fulfillment_type'] in ('delivery', 'pickup'))
print(f"Online/Delivery: {delivery/len(txns)*100:.1f}% (target 10-15%)")

# Delivery basket vs instore
instore = [t for t in txns if t['fulfillment_type'] == 'in_store']
deliv = [t for t in txns if t['fulfillment_type'] in ('delivery', 'pickup')]
avg_instore = sum(float(t['total_amount']) for t in instore) / len(instore) if instore else 0
avg_deliv = sum(float(t['total_amount']) for t in deliv) / len(deliv) if deliv else 0
print(f"In-store Basket: ${avg_instore:.2f}")
print(f"Delivery Basket: ${avg_deliv:.2f} (ratio: {avg_deliv/avg_instore:.2f}x)")

# Weekend vs weekday
print(f"\n=== WEEKEND ANALYSIS ===")
weekend = [t for t in txns if datetime.strptime(t['date'], '%Y-%m-%d').weekday() >= 5]
weekday = [t for t in txns if datetime.strptime(t['date'], '%Y-%m-%d').weekday() < 5]
avg_weekend = sum(float(t['total_amount']) for t in weekend) / len(weekend) if weekend else 0
avg_weekday = sum(float(t['total_amount']) for t in weekday) / len(weekday) if weekday else 0
premium = ((avg_weekend - avg_weekday) / avg_weekday * 100) if avg_weekday else 0
print(f"Weekend Basket: ${avg_weekend:.2f}")
print(f"Weekday Basket: ${avg_weekday:.2f}")
print(f"Weekend Premium: {premium:+.1f}% (target +20%)")

print("\n=== DONE ===")

