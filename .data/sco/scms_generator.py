## PYTHON DATA GENERATOR SCRIPT
import random
from datetime import datetime, timedelta
from faker import Faker
import psycopg2

fake = Faker()

conn = psycopg2.connect("dbname=scms user=user password=password host=local.hasura.dev port=5432")
cursor = conn.cursor()

# Set default schema for this session
cursor.execute("SET search_path TO us")

# Insert suppliers
for _ in range(40):
    cursor.execute(
        "INSERT INTO Suppliers (name, contact_email, country) VALUES (%s, %s, %s)",
        #(fake.company(), fake.company_email(), fake.country())
        (fake.company(), fake.company_email(), "US")
    )

# Insert raw materials
materials = ["Rubber", "Leather", "Foam", "Mesh", "Glue", "Cotton", "Plastic"]
for mat in materials:
    cursor.execute(
        "INSERT INTO RawMaterials (name, unit, cost_per_unit) VALUES (%s, %s, %s)",
        (mat, "kg", round(random.uniform(1.0, 20.0), 2))
    )

# Link suppliers and materials
for _ in range(80):
    cursor.execute(
        "INSERT INTO SupplierMaterials (supplier_id, material_id, lead_time_days) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING",
        (random.randint(1, 10), random.randint(1, len(materials)), random.randint(3, 30))
    )

# Insert factories
for _ in range(5):
    cursor.execute(
        "INSERT INTO Factories (name, location, capacity) VALUES (%s, %s, %s)",
        (fake.company(), fake.city(), random.randint(5000, 20000))
    )

# Insert shoes
for _ in range(20):
    cursor.execute(
        "INSERT INTO Shoes (model_name, category, release_date) VALUES (%s, %s, %s)",
        (fake.word().capitalize() + " Runner", random.choice(["Running", "Casual", "Hiking"]), fake.date_between(start_date="-2y", end_date="today")))

# Bill of Materials
for shoe_id in range(1, 21):
    used_materials = random.sample(range(1, len(materials)+1), k=3)
    for mat_id in used_materials:
        cursor.execute(
            "INSERT INTO BillOfMaterials (shoe_id, material_id, quantity_required) VALUES (%s, %s, %s)",
            (shoe_id, mat_id, round(random.uniform(0.1, 2.0), 2))
        )

# Insert production orders
for _ in range(150):
    shoe_id = random.randint(1, 20)
    factory_id = random.randint(1, 5)
    start_date = fake.date_between(start_date="-1y", end_date="today")
    duration = random.randint(10, 60)
    cursor.execute(
        "INSERT INTO ProductionOrders (shoe_id, factory_id, quantity, start_date, expected_completion) VALUES (%s, %s, %s, %s, %s)",
        (shoe_id, factory_id, random.randint(100, 5000), start_date, start_date + timedelta(days=duration))
    )

# Insert warehouses
for _ in range(5):
    cursor.execute(
        "INSERT INTO Warehouses (name, location) VALUES (%s, %s)",
        (fake.company(), fake.city())
    )

# Insert shipments
for _ in range(100):
    order_id = random.randint(1, 50)
    warehouse_id = random.randint(1, 5)
    ship_date = fake.date_between(start_date="-1y", end_date="today")
    arrival_date = ship_date + timedelta(days=random.randint(1, 15))
    cursor.execute(
        "INSERT INTO Shipments (order_id, warehouse_id, shipped_date, arrival_date, quantity) VALUES (%s, %s, %s, %s, %s)",
        (order_id, warehouse_id, ship_date, arrival_date, random.randint(50, 2000))
    )

conn.commit()
cursor.close()
conn.close()
print("Data generation complete.")
