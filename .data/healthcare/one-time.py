import csv
import os
from faker import Faker
import random

fake = Faker()
OUTPUT_DIR = "postgres"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Munge NDC Drug Data
def munge_drug_data(input_csv="drugs.csv"):
    drug_ref_data = []
    drug_pkg_data = []
    
    with open("postgres/drugs.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            drug_ref_data.append([
                row["PRODUCTNDC"], row["PROPRIETARYNAME"], row["NONPROPRIETARYNAME"],
                row["DOSAGEFORMNAME"], row["ROUTENAME"], row["LABELERNAME"],
                row["SUBSTANCENAME"], row["ACTIVEINGREDIENTSINFO"]
            ])
            drug_pkg_data.append([
                row["NDCPACKAGECODE"], row["PRODUCTNDC"], row["PACKAGEDESCRIPTION"]
            ])

    with open(f"{OUTPUT_DIR}/ref_drug_reference.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["ref.product_ndc", "ref.proprietary_name", "ref.nonproprietary_name", 
                         "ref.dosage_form_name", "ref.route_name", "ref.labeler_name", 
                         "ref.substance_name", "ref.active_ingredients_info"])
        writer.writerows(drug_ref_data)

    with open(f"{OUTPUT_DIR}/ref_drug_packaging.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["ref.ndc_package_code", "ref.product_ndc", "ref.package_description"])
        writer.writerows(drug_pkg_data)

# Munge HCPCS Unit Codes
def munge_hcpcs_data(input_csv="hcpc.csv"):
    proc_data = []
    
    with open("postgres/hcpc.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            desc = row["LONG DESCRIPTION"].lower()
            category = "Radiology" if "radiologic" in desc or "ct" in desc else random.choice(["Surgery", "Lab"])
            duration = 60 if "ct" in desc or "mri" in desc else (30 if category == "Radiology" else random.randint(15, 120))
            
            proc_data.append([
                row["HCPC"], row["LONG DESCRIPTION"], row["SHORT DESCRIPTION"],
                category, duration
            ])

    with open(f"{OUTPUT_DIR}/ref_procedure_codes.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["ref.hcpc", "ref.long_description", "ref.short_description", 
                         "ref.category", "ref.avg_duration_minutes"])
        writer.writerows(proc_data)

if __name__ == "__main__":
    print("Munging drug data...")
    munge_drug_data("drugs.csv")  # Replace with your actual NDC CSV path
    print("Munging HCPCS data...")
    munge_hcpcs_data("hcpc.csv")  # Replace with your actual HCPCS CSV path
    print(f"Munging complete. Files saved in {OUTPUT_DIR}/")