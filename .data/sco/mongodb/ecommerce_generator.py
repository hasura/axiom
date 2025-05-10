# MongoDB schema and data generator for shoe company customer orders
# Requires: pymongo, faker

from pymongo import MongoClient
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()

client = MongoClient("mongodb://local.hasura.dev:27017/")
db = client["ecommerce"]
orders = db["customer_orders"]

# Clean previous entries
orders.delete_many({})

SHOE_MODELS = [
    {"model_id": f"SHOE-{i:03d}", "name": fake.word().capitalize() + " Runner", "category": random.choice(["Running", "Casual", "Hiking"])}
    for i in range(1, 21)
]

PAYMENT_METHODS = ["Credit Card", "PayPal", "Apple Pay", "Google Pay"]
SHIPPING_METHODS = ["Standard", "Express", "Overnight"]
ORDER_STATUS = ["Pending", "Processing", "Shipped", "Delivered", "Cancelled"]

# Generate customer orders
def generate_order():
    customer = {
        "customer_id": fake.uuid4(),
        "name": fake.name(),
        "email": fake.email(),
        "phone": fake.phone_number(),
        "address": {
            "street": fake.street_address(),
            "city": fake.city(),
            "state": fake.state(),
            "zip": fake.zipcode(),
            #"country": fake.country()
            "country": "US"
        }
    }

    order_date = fake.date_time_between(start_date="-1w", end_date="now")
    items = []
    total_price = 0

    for _ in range(random.randint(1, 3)):
        product = random.choice(SHOE_MODELS)
        quantity = random.randint(1, 2)
        unit_price = round(random.uniform(60.0, 180.0), 2)
        items.append({
            "model_id": product["model_id"],
            "name": product["name"],
            "category": product["category"],
            "quantity": quantity,
            "unit_price": unit_price,
            "subtotal": round(unit_price * quantity, 2)
        })
        total_price += unit_price * quantity

    order = {
        "order_id": fake.uuid4(),
        "customer": customer,
        "order_date": order_date,
        "status": random.choice(ORDER_STATUS),
        "items": items,
        "total_price": round(total_price, 2),
        "payment_method": random.choice(PAYMENT_METHODS),
        "shipping_method": random.choice(SHIPPING_METHODS),
        "shipping_cost": round(random.uniform(5.0, 20.0), 2),
        "expected_delivery": order_date + timedelta(days=random.randint(2, 10)),
        "last_updated": datetime.now()
    }

    return order

# Generate and insert orders
for _ in range(1200):
    orders.insert_one(generate_order())

print("Customer order data inserted into MongoDB.")
