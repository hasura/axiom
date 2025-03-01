import csv
import random
from datetime import datetime, timedelta
import uuid
from faker import Faker
import os

fake = Faker()
OUTPUT_DIR = "postgres"
CURRENT_DATE = datetime.today()
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Define better region names
regions = [
    "Northeast", "Midwest", "South", "West"]

# Load HCPCS codes
def load_hcpcs_codes(file_path=f"{OUTPUT_DIR}/procedure_codes.csv"):
    with open(file_path, "r") as f:
        reader = csv.DictReader(f)
        return [(row["ref.hcpc"], row["ref.category"], int(row["ref.avg_duration_minutes"])) for row in reader]

# Generate Patients and Insurance Plans
def generate_patients_and_insurance(num_patients=1000):
    with open(f"{OUTPUT_DIR}/patients.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["patient.patient_id", "patient.first_name", "patient.last_name", 
                         "patient.date_of_birth", "patient.insurance_plan_id"])
        for _ in range(num_patients):
            pid = fake.uuid4()[:20]
            writer.writerow([
                pid, fake.first_name(), fake.last_name(), 
                fake.date_of_birth(minimum_age=18, maximum_age=90).isoformat(),
                f"PLAN{random.randint(1, 5):03d}"
            ])

    with open(f"{OUTPUT_DIR}/insurance_plans.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["patient.plan_id", "patient.plan_name", "patient.payer_name"])
        for i in range(10):
            writer.writerow([
                f"PLAN{i+1:03d}", fake.company() + " Plan", 
                random.choice([
                    "UnitedHealthcare", "Aetna", "Cigna", "Blue Cross Blue Shield", 
                    "Humana", "Kaiser Permanente", "Anthem", "Molina Healthcare", 
                    "Health Net", "WellCare", "Centene", "Ambetter", "Oscar Health",
                    "Medica", "Priority Health", "Highmark", "Florida Blue", 
                    "Empire BlueCross", "Regence BlueShield", "Premera Blue Cross"
                ])
            ])

# Generate Operators and Schedule with Variance
def generate_operators_and_schedule(num_operators=10):
    with open(f"{OUTPUT_DIR}/operators.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["ops.operator_id", "ops.full_name", "ops.region", "ops.specialty"])
        for i in range(num_operators):
            writer.writerow([f"OP{i:03d}", fake.name(), random.choice(regions),
                            random.choice(["Radiology"])])

    busy_operators = ["OP000", "OP001", "OP002"]  # 30% busier
    start_date = CURRENT_DATE
    
    with open(f"{OUTPUT_DIR}/operator_schedule.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["ops.operator_id", "ops.work_date", "ops.booked_minutes", "ops.max_minutes"])
        over_capacity_operators = ["OP000", "OP001", "OP002", "OP003", "OP004"]
        for i in range(num_operators):
            op_id = f"OP{i:03d}"
            for day in range(14):
                work_date = start_date + timedelta(days=day)
                if op_id in over_capacity_operators:
                    booked = random.randint(500, 600)  # Over 480 max capacity
                else:
                    booked = random.randint(200, 450)  # Everyone is busier
                writer.writerow([op_id, work_date.date().isoformat(), booked, 480])

# Generate Cases with Variance
def generate_cases(num_cases=1000):
    hcpcs_codes = load_hcpcs_codes()
    patients = [row["patient.patient_id"] for row in csv.DictReader(open(f"{OUTPUT_DIR}/patients.csv"))]
    operators = [row["ops.operator_id"] for row in csv.DictReader(open(f"{OUTPUT_DIR}/operators.csv"))]
    start_date = CURRENT_DATE
    
    with open(f"{OUTPUT_DIR}/cases.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["ops.patient_id", "ops.clinic_id", "ops.procedure_code", "ops.urgency_level", 
                         "ops.recommended_date", "ops.status", "ops.operator_id", "ops.region", "ops.created_at"])
        
        for _ in range(num_cases):
            hcpc, category, duration = random.choice(hcpcs_codes)
            urgency = random.choices(
                ["critical", "emergency", "urgent", "semi-urgent", "routine"],
                weights=[15, 25, 30, 15, 15]
            )[0]
            rec_date = start_date + timedelta(days=random.randint(0, 13))
            status_roll = random.random()
            if status_roll < 0.4:
                status, op_id = "pending", ""
            elif status_roll < 0.85:
                status, op_id = "assigned", random.choice(operators)
            else:
                status, op_id = "completed", random.choice(operators)
            
            writer.writerow([
                random.choice(patients), "CL001", hcpc, urgency, rec_date.date().isoformat(),
                status, op_id, random.choice(regions), datetime.now().isoformat()
            ])

if __name__ == "__main__":
    print("Generating patients and insurance...")
    generate_patients_and_insurance(2000)
    print("Generating operators and schedule...")
    generate_operators_and_schedule(8)
    print("Generating cases...")
    generate_cases(8000)
    print(f"Data generation complete. Files saved in {OUTPUT_DIR}/")
