import csv
import json
import random
import os
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()

# Helper function for MongoDB date formatting
def format_date_for_mongodb(date_obj):
    """
    Format a datetime object as MongoDB Extended JSON format
    MongoDB requires RFC3339 format with 'Z' at the end for UTC timezone
    """
    # Format to millisecond precision and add 'Z' for UTC timezone
    date_str = date_obj.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    return {"$date": date_str}

# Create output directories
POSTGRES_DIR = "postgres/entrypoint"
MONGODB_DIR = "mongodb"
os.makedirs(POSTGRES_DIR, exist_ok=True)
os.makedirs(MONGODB_DIR, exist_ok=True)

# Common data
SHOE_MODELS = [
    {"model_id": f"SHOE-{i:03d}", "name": fake.word().capitalize() + " Runner", "category": random.choice(["Running", "Casual", "Hiking"])}
    for i in range(1, 21)
]

MATERIALS = ["Rubber", "Leather", "Foam", "Mesh", "Glue", "Cotton", "Plastic"]
PAYMENT_METHODS = ["Credit Card", "PayPal", "Apple Pay", "Google Pay"]
SHIPPING_METHODS = ["Standard", "Express", "Overnight"]
ORDER_STATUS = ["Pending", "Processing", "Shipped", "Delivered", "Cancelled"]

# PostgreSQL data generation functions
def generate_postgres_data():
    # Generate suppliers
    with open(f"{POSTGRES_DIR}/suppliers.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["name", "contact_email", "country"])
        for _ in range(40):
            writer.writerow([
                fake.company(),
                fake.company_email(),
                "US"
            ])

    # Generate raw materials
    with open(f"{POSTGRES_DIR}/raw_materials.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["name", "unit", "cost_per_unit"])
        for mat in MATERIALS:
            writer.writerow([
                mat,
                "kg",
                round(random.uniform(1.0, 20.0), 2)
            ])

    # Generate supplier materials
    with open(f"{POSTGRES_DIR}/supplier_materials.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["supplier_id", "material_id", "lead_time_days"])
        for _ in range(80):
            writer.writerow([
                random.randint(1, 10),
                random.randint(1, len(MATERIALS)),
                random.randint(3, 30)
            ])

    # Generate factories
    with open(f"{POSTGRES_DIR}/factories.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["name", "location", "capacity"])
        for _ in range(5):
            writer.writerow([
                fake.company(),
                fake.city(),
                random.randint(5000, 20000)
            ])

    # Generate shoes
    with open(f"{POSTGRES_DIR}/shoes.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["model_name", "category", "release_date"])
        for model in SHOE_MODELS:
            writer.writerow([
                model["name"],
                model["category"],
                fake.date_between(start_date="-2y", end_date="today").isoformat()
            ])

    # Generate bill of materials
    with open(f"{POSTGRES_DIR}/bill_of_materials.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["shoe_id", "material_id", "quantity_required"])
        for shoe_id in range(1, 21):
            used_materials = random.sample(range(1, len(MATERIALS)+1), k=3)
            for mat_id in used_materials:
                writer.writerow([
                    shoe_id,
                    mat_id,
                    round(random.uniform(0.1, 2.0), 2)
                ])

    # Generate production orders
    with open(f"{POSTGRES_DIR}/production_orders.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["shoe_id", "factory_id", "quantity", "start_date", "expected_completion"])
        for _ in range(150):
            shoe_id = random.randint(1, 20)
            factory_id = random.randint(1, 5)
            start_date = fake.date_between(start_date="-1y", end_date="today")
            duration = random.randint(10, 60)
            writer.writerow([
                shoe_id,
                factory_id,
                random.randint(100, 5000),
                start_date.isoformat(),
                (start_date + timedelta(days=duration)).isoformat()
            ])

    # Generate warehouses
    with open(f"{POSTGRES_DIR}/warehouses.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["name", "location"])
        for _ in range(5):
            writer.writerow([
                fake.company(),
                fake.city()
            ])

    # Generate shipments
    with open(f"{POSTGRES_DIR}/shipments.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["order_id", "warehouse_id", "shipped_date", "arrival_date", "quantity"])
        for _ in range(100):
            order_id = random.randint(1, 50)
            warehouse_id = random.randint(1, 5)
            ship_date = fake.date_between(start_date="-1y", end_date="today")
            arrival_date = ship_date + timedelta(days=random.randint(1, 15))
            writer.writerow([
                order_id,
                warehouse_id,
                ship_date.isoformat(),
                arrival_date.isoformat(),
                random.randint(50, 2000)
            ])

# MongoDB data generation functions
def generate_customer_order():
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
        "order_date": format_date_for_mongodb(order_date),
        "status": random.choice(ORDER_STATUS),
        "items": items,
        "total_price": round(total_price, 2),
        "payment_method": random.choice(PAYMENT_METHODS),
        "shipping_method": random.choice(SHIPPING_METHODS),
        "shipping_cost": round(random.uniform(5.0, 20.0), 2),
        "expected_delivery": format_date_for_mongodb(order_date + timedelta(days=random.randint(2, 10))),
        "last_updated": format_date_for_mongodb(datetime.now())
    }

    return order

def generate_mongodb_data():
    # Generate customer orders
    orders = []
    for _ in range(1200):
        orders.append(generate_customer_order())

    # Write to JSON file
    with open(f"{MONGODB_DIR}/customer_orders.json", "w") as f:
        json.dump(orders, f, indent=2)

if __name__ == "__main__":
    print("Generating PostgreSQL data...")
    generate_postgres_data()
    print(f"PostgreSQL data generation complete. Files saved in {POSTGRES_DIR}/")
    
    print("Generating MongoDB data...")
    generate_mongodb_data()
    print(f"MongoDB data generation complete. Files saved in {MONGODB_DIR}/")
    
    print("All data generation complete!")