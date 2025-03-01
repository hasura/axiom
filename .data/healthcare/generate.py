import csv
import random
from datetime import datetime, timedelta
import uuid
from faker import Faker
import os

fake = Faker()
OUTPUT_DIR = "postgres"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load HCPCS codes
def load_hcpcs_codes(file_path=f"{OUTPUT_DIR}/ref_procedure_codes.csv"):
    with open(file_path, "r") as f:
        reader = csv.DictReader(f)
        return [(row["ref.hcpc"], row["ref.category"], int(row["ref.avg_duration_minutes"])) for row in reader]

# Generate Patients and Insurance Plans
def generate_patients_and_insurance(num_patients=1000):
    with open(f"{OUTPUT_DIR}/patient_patients.csv", "w", newline="") as f:
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

    with open(f"{OUTPUT_DIR}/patient_insurance_plans.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["patient.plan_id", "patient.plan_name", "patient.payer_name"])
        for i in range(5):
            writer.writerow([
                f"PLAN{i+1:03d}", fake.company() + " Plan", 
                random.choice(["UnitedHealthcare", "Aetna", "Cigna"])
            ])

# Generate Operators and Schedule with Variance
def generate_operators_and_schedule():
    with open(f"{OUTPUT_DIR}/ops_operators.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["ops.operator_id", "ops.full_name", "ops.region", "ops.specialty"])
        for i in range(10):
            writer.writerow([f"OP{i:03d}", fake.name(), "Region1", 
                            random.choice(["Radiology", "Cardiology", "Orthopedics"])])

    busy_operators = ["OP000", "OP001", "OP002"]  # 30% busier
    start_date = datetime(2025, 3, 1)
    
    with open(f"{OUTPUT_DIR}/ops_operator_schedule.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["ops.operator_id", "ops.work_date", "ops.booked_minutes", "ops.max_minutes"])
        for i in range(10):
            op_id = f"OP{i:03d}"
            for day in range(14):
                work_date = start_date + timedelta(days=day)
                booked = random.randint(200, 400) if op_id in busy_operators else random.randint(0, 150)
                writer.writerow([op_id, work_date.date().isoformat(), booked, 480])

# Generate Cases with Variance
def generate_cases(num_cases=1000):
    hcpcs_codes = load_hcpcs_codes()
    patients = [row["patient.patient_id"] for row in csv.DictReader(open(f"{OUTPUT_DIR}/patient_patients.csv"))]
    operators = [row["ops.operator_id"] for row in csv.DictReader(open(f"{OUTPUT_DIR}/ops_operators.csv"))]
    start_date = datetime(2025, 3, 1)
    
    with open(f"{OUTPUT_DIR}/ops_cases.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["ops.patient_id", "ops.clinic_id", "ops.procedure_code", "ops.urgency_level", 
                         "ops.recommended_date", "ops.status", "ops.operator_id", "ops.region", "ops.created_at"])
        
        for _ in range(num_cases):
            hcpc, category, duration = random.choice(hcpcs_codes)
            urgency = random.choice(["urgent", "normal"])
            rec_date = start_date + timedelta(days=random.randint(0, 13))
            status_roll = random.random()
            if status_roll < 0.6:
                status, op_id = "pending", ""
            elif status_roll < 0.9:
                status, op_id = "assigned", random.choice(operators[:3])  # Busier operators
            else:
                status, op_id = "completed", random.choice(operators)
            
            writer.writerow([
                random.choice(patients), "CL001", hcpc, urgency, rec_date.date().isoformat(),
                status, op_id, "Region1", datetime.now().isoformat()
            ])

if __name__ == "__main__":
    print("Generating patients and insurance...")
    generate_patients_and_insurance()
    print("Generating operators and schedule...")
    generate_operators_and_schedule()
    print("Generating cases...")
    generate_cases()
    print(f"Data generation complete. Files saved in {OUTPUT_DIR}/")