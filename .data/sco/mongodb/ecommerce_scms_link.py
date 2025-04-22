# Script to connect customer orders in MongoDB with supply chain data in PostgreSQL
# This links MongoDB orders to existing shoes and creates matching production orders if needed

import psycopg2
from pymongo import MongoClient
from datetime import datetime, timedelta
import random

# Connect to PostgreSQL
pg_conn = psycopg2.connect("dbname=scms user=user password=password host=local.hasura.dev port=5432")
pg_cur = pg_conn.cursor()

# Set default schema for this session
pg_cur.execute("SET search_path TO us")

# Connect to MongoDB
mongo_client = MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client["ecommerce"]
orders_collection = mongo_db["customer_orders"]

# Fetch all existing shoe models from PostgreSQL
pg_cur.execute("SELECT shoe_id, model_name FROM Shoes")
pg_shoes = {f"SHOE-{row[0]:03d}": row[0] for row in pg_cur.fetchall()}

# Fetch existing production orders to avoid duplicates
pg_cur.execute("SELECT shoe_id, SUM(quantity) FROM ProductionOrders GROUP BY shoe_id")
existing_production = dict(pg_cur.fetchall())

# Link orders
linked_count = 0
for order in orders_collection.find():
    for item in order['items']:
        model_id = item['model_id']
        if model_id in pg_shoes:
            shoe_id = pg_shoes[model_id]
            qty_needed = item['quantity']
            # Check if this order is already supported by production
            existing_qty = existing_production.get(shoe_id, 0)
            if existing_qty < 10000:  # simple threshold for demo
                factory_id = random.randint(1, 5)
                start_date = datetime.now().date()
                expected_completion = start_date + timedelta(days=random.randint(10, 30))
                pg_cur.execute(
                    """
                    INSERT INTO ProductionOrders (shoe_id, factory_id, quantity, start_date, expected_completion)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (shoe_id, factory_id, 500, start_date, expected_completion)
                )
                existing_production[shoe_id] = existing_production.get(shoe_id, 0) + 500
                linked_count += 1

pg_conn.commit()
pg_cur.close()
pg_conn.close()
mongo_client.close()

print(f"Linked and synced {linked_count} customer order items with production orders.")

