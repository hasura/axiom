#!/usr/bin/env python3
"""
Telco Data Generator

This script generates realistic, semantically accurate data for a telco database
and outputs it to CSV files that can be loaded into the database schemas.
"""

import os
import csv
import json
import random
import datetime
import argparse
from faker import Faker

# Import generator modules
from generators.postgres_generators import (
    generate_auth_users,
    generate_customers,
    generate_plans,
    generate_devices,
    generate_network_nodes,
    generate_customer_plans,
    generate_customer_plan_devices,
    generate_customer_network,
    generate_billing,
    generate_credit_cards,
    generate_customer_link,
    generate_deals,
    generate_calls,
    generate_texts,
    generate_service_interactions,
    generate_interactions,
    generate_number_portability,
    generate_voip_services,
    generate_iot_devices,
    generate_referrals,
    generate_device_upgrades,
    generate_family_plans,
    generate_loyalty_rewards,
    generate_campaigns,
    generate_feedback
)
from generators.mongodb_generators import (
    generate_user_profiles,
    generate_customer_preferences
)
from generators.clickhouse_generators import (
    generate_cdr_data,
    generate_network_performance,
    generate_data_usage
)
from generators.pgvector_generators import (
    generate_documents,
    generate_document_embeddings
)
from generators.network_generators import (
    generate_coverage_areas,
    generate_equipment,
    generate_spectrum_licenses,
    generate_outages
)

# Data volume presets
DATA_VOLUMES = {
    "tiny": {
        "customers": 100,
        "plans": 10,
        "devices": 10,
        "network_nodes": 50,
        "calls_per_customer": 20,
        "texts_per_customer": 30,
        "billing_entries_per_customer": 6,
        "deals": 3,
        "clickhouse_months_back": 1,
        "clickhouse_records_per_customer": 10
    },
    "small": {
        "customers": 500,
        "plans": 8,
        "devices": 30,
        "network_nodes": 50,
        "calls_per_customer": 30,
        "texts_per_customer": 50,
        "billing_entries_per_customer": 12,
        "deals": 5,
        "clickhouse_months_back": 3,
        "clickhouse_records_per_customer": 30
    },
    "medium": {
        "customers": 5000,
        "plans": 15,
        "devices": 50,
        "network_nodes": 200,
        "calls_per_customer": 60,
        "texts_per_customer": 100,
        "billing_entries_per_customer": 24,
        "deals": 10,
        "clickhouse_months_back": 6,
        "clickhouse_records_per_customer": 60
    },
    "large": {
        "customers": 100000,
        "plans": 30,
        "devices": 100,
        "network_nodes": 10000,
        "calls_per_customer": 100,
        "texts_per_customer": 200,
        "billing_entries_per_customer": 60,
        "deals": 50,
        "clickhouse_months_back": 12,
        "clickhouse_records_per_customer": 120
    },
    "enterprise": {
        "customers": 1000000,
        "plans": 100,
        "devices": 50000,
        "network_nodes": 100000,
        "calls_per_customer": 300,
        "texts_per_customer": 1000,
        "billing_entries_per_customer": 120,
        "deals": 100,
        "clickhouse_months_back": 24,
        "clickhouse_records_per_customer": 300
    }
}

# Initialize Faker
fake = Faker()
Faker.seed(69)  # For reproducibility
random.seed(69)

# Default constants (will be overridden based on volume)
NUM_CUSTOMERS = 1000
NUM_PLANS = 10
NUM_DEVICES = 50
NUM_NETWORK_NODES = 100
NUM_CALLS_PER_CUSTOMER = 20
NUM_TEXTS_PER_CUSTOMER = 30
NUM_BILLING_ENTRIES_PER_CUSTOMER = 12
NUM_DEALS = 5
CLICKHOUSE_MONTHS_BACK = 6
CLICKHOUSE_RECORDS_PER_CUSTOMER = 50
OUTPUT_DIR = "generated_data"  # Default output directory

def write_csv(data, filename, directory="postgres"):
    """Write data to a CSV file."""
    if not data:
        print(f"No data to write for {filename}")
        return

    filepath = f"{OUTPUT_DIR}/{directory}/{filename}"
    with open(filepath, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    print(f"Generated {len(data)} records in {filepath}")

def write_json(data, filename, directory="mongo_seed"):
    """Write data to a JSON file."""
    if not data:
        print(f"No data to write for {filename}")
        return

    filepath = f"{OUTPUT_DIR}/{directory}/{filename}"
    with open(filepath, 'w') as jsonfile:
        json.dump(data, jsonfile, indent=2)
    print(f"Generated {len(data)} records in {filepath}")

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Generate telco data with configurable volume")
    parser.add_argument(
        "--volume",
        choices=["tiny", "small", "medium", "large", "enterprise"],
        default="tiny",
        help="Data volume to generate (tiny, small, medium, large, enterprise)"
    )
    parser.add_argument(
        "--output-dir",
        default="generated_data",
        help="Directory to output generated data"
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=69,
        help="Random seed for reproducibility"
    )
    parser.add_argument(
        "--generate-summary",
        action="store_true",
        help="Generate a summary JSON file with data volume information"
    )
    parser.add_argument(
        "--clickhouse-months-back",
        type=int,
        help="Number of months to go back for ClickHouse data (overrides volume setting)"
    )
    parser.add_argument(
        "--clickhouse-records",
        type=int,
        help="Number of records per customer for ClickHouse data (overrides volume setting)"
    )
    return parser.parse_args()

def main():
    # Parse command-line arguments
    args = parse_arguments()
    
    # Set random seed
    Faker.seed(args.seed)
    random.seed(args.seed)
    
    # Set data volume
    volume = args.volume
    print(f"Generating telco data with {volume} volume...")
    
    # Set constants based on volume
    global NUM_CUSTOMERS, NUM_PLANS, NUM_DEVICES, NUM_NETWORK_NODES
    global NUM_CALLS_PER_CUSTOMER, NUM_TEXTS_PER_CUSTOMER
    global NUM_BILLING_ENTRIES_PER_CUSTOMER, NUM_DEALS
    global CLICKHOUSE_MONTHS_BACK, CLICKHOUSE_RECORDS_PER_CUSTOMER

    NUM_CUSTOMERS = DATA_VOLUMES[volume]["customers"]
    NUM_PLANS = DATA_VOLUMES[volume]["plans"]
    NUM_DEVICES = DATA_VOLUMES[volume]["devices"]
    NUM_NETWORK_NODES = DATA_VOLUMES[volume]["network_nodes"]
    NUM_CALLS_PER_CUSTOMER = DATA_VOLUMES[volume]["calls_per_customer"]
    NUM_TEXTS_PER_CUSTOMER = DATA_VOLUMES[volume]["texts_per_customer"]
    NUM_BILLING_ENTRIES_PER_CUSTOMER = DATA_VOLUMES[volume]["billing_entries_per_customer"]
    NUM_DEALS = DATA_VOLUMES[volume]["deals"]
    CLICKHOUSE_MONTHS_BACK = DATA_VOLUMES[volume]["clickhouse_months_back"]
    CLICKHOUSE_RECORDS_PER_CUSTOMER = DATA_VOLUMES[volume]["clickhouse_records_per_customer"]

    # Override ClickHouse parameters if specified via command line
    if args.clickhouse_months_back is not None:
        CLICKHOUSE_MONTHS_BACK = args.clickhouse_months_back
        print(f"Overriding ClickHouse months back to {CLICKHOUSE_MONTHS_BACK}")

    if args.clickhouse_records is not None:
        CLICKHOUSE_RECORDS_PER_CUSTOMER = args.clickhouse_records
        print(f"Overriding ClickHouse records per customer to {CLICKHOUSE_RECORDS_PER_CUSTOMER}")

    # Create output directory
    global OUTPUT_DIR
    OUTPUT_DIR = args.output_dir
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(f"{OUTPUT_DIR}/postgres", exist_ok=True)
    os.makedirs(f"{OUTPUT_DIR}/mongo_seed", exist_ok=True)
    os.makedirs(f"{OUTPUT_DIR}/clickhouse/csv", exist_ok=True)
    os.makedirs(f"{OUTPUT_DIR}/pgvector", exist_ok=True)

    # Generate PostgreSQL data
    print("\nGenerating PostgreSQL data...")
    auth_users = generate_auth_users(NUM_CUSTOMERS)
    write_csv(auth_users, "auth_users.csv")

    customers = generate_customers(auth_users)
    write_csv(customers, "customers.csv")

    plans = generate_plans(NUM_PLANS)
    write_csv(plans, "plans.csv")

    devices = generate_devices(NUM_DEVICES)
    write_csv(devices, "devices.csv")

    network_nodes = generate_network_nodes(NUM_NETWORK_NODES)
    write_csv(network_nodes, "network_nodes.csv")

    customer_plans = generate_customer_plans(customers, plans)
    write_csv(customer_plans, "customer_plans.csv")

    customer_plan_devices = generate_customer_plan_devices(customer_plans, devices)
    write_csv(customer_plan_devices, "customer_plan_devices.csv")

    customer_network = generate_customer_network(customers, network_nodes)
    write_csv(customer_network, "customer_network.csv")

    billing = generate_billing(customers, customer_plans, plans)
    write_csv(billing, "billing.csv")

    credit_cards = generate_credit_cards(customers)
    write_csv(credit_cards, "credit_cards.csv")

    customer_link = generate_customer_link(customers)
    write_csv(customer_link, "customer_link.csv")

    deals = generate_deals(NUM_DEALS)
    write_csv(deals, "deals.csv")

    calls = generate_calls(customer_plans, network_nodes)
    write_csv(calls, "calls.csv")

    texts = generate_texts(customer_plans, network_nodes)
    write_csv(texts, "texts.csv")

    # Generate service interactions and customer feedback data
    service_interactions = generate_service_interactions(customers)
    write_csv(service_interactions, "service_interactions.csv")

    interactions = generate_interactions(customers)
    write_csv(interactions, "interactions.csv")

    number_portability = generate_number_portability(customers)
    write_csv(number_portability, "number_portability.csv")

    voip_services = generate_voip_services(customers)
    write_csv(voip_services, "voip_services.csv")

    iot_devices = generate_iot_devices(customers, plans)
    write_csv(iot_devices, "iot_devices.csv")

    referrals = generate_referrals(customers)
    write_csv(referrals, "referrals.csv")

    device_upgrades = generate_device_upgrades(customers, devices)
    write_csv(device_upgrades, "device_upgrades.csv")

    family_plans, family_plan_members = generate_family_plans(customers)
    write_csv(family_plans, "family_plans.csv")
    write_csv(family_plan_members, "family_plan_members.csv")

    loyalty_rewards = generate_loyalty_rewards(customers)
    write_csv(loyalty_rewards, "loyalty_rewards.csv")

    campaigns = generate_campaigns(NUM_DEALS * 2)
    write_csv(campaigns, "campaigns.csv")

    feedback = generate_feedback(customers)
    write_csv(feedback, "feedback.csv")

    # Generate additional network data
    print("\nGenerating additional network data...")
    coverage_areas = generate_coverage_areas(network_nodes)
    write_csv(coverage_areas, "coverage_areas.csv")

    equipment = generate_equipment(network_nodes)
    write_csv(equipment, "equipment.csv")

    spectrum_licenses = generate_spectrum_licenses()
    write_csv(spectrum_licenses, "spectrum_licenses.csv")

    outages = generate_outages(network_nodes)
    write_csv(outages, "outages.csv")

    # Generate MongoDB data
    print("\nGenerating MongoDB data...")
    user_profiles = generate_user_profiles(customers, customer_link)
    write_json(user_profiles, "user_profiles.json", "mongo_seed")

    customer_preferences = generate_customer_preferences(customer_link)
    write_json(customer_preferences, "customer_preferences.json", "mongo_seed")

    # Generate ClickHouse data
    print("\nGenerating ClickHouse data...")
    print(f"Using months_back={CLICKHOUSE_MONTHS_BACK}, records_per_customer={CLICKHOUSE_RECORDS_PER_CUSTOMER}")

    cdr_data = generate_cdr_data(customer_link, calls,
                               months_back=CLICKHOUSE_MONTHS_BACK,
                               records_per_customer=CLICKHOUSE_RECORDS_PER_CUSTOMER)
    write_csv(cdr_data, "cdr.csv", "clickhouse/csv")

    network_perf = generate_network_performance(customer_link,
                                              months_back=CLICKHOUSE_MONTHS_BACK,
                                              records_per_customer=CLICKHOUSE_RECORDS_PER_CUSTOMER)
    write_csv(network_perf, "network_performance.csv", "clickhouse/csv")

    data_usage = generate_data_usage(customer_link,
                                   months_back=CLICKHOUSE_MONTHS_BACK,
                                   records_per_customer=CLICKHOUSE_RECORDS_PER_CUSTOMER)
    write_csv(data_usage, "data_usage.csv", "clickhouse/csv")

    # Generate PGVector data
    print("\nGenerating PGVector data...")
    documents = generate_documents()
    write_csv(documents, "documents.csv", "pgvector")

    if "OPENAI_API_KEY" in os.environ:
        document_embeddings = generate_document_embeddings(documents)
        write_csv(document_embeddings, "document_embeddings.csv", "pgvector")

    # Write a summary file with data volume information only if flag is set
    if args.generate_summary:
        print("\nGenerating summary file...")
        with open(f"{OUTPUT_DIR}/generation_summary.json", 'w') as f:
            summary = {
                "volume": volume,
                "timestamp": datetime.datetime.now().isoformat(),
                "counts": {
                    "customers": NUM_CUSTOMERS,
                    "plans": NUM_PLANS,
                    "devices": NUM_DEVICES,
                    "network_nodes": NUM_NETWORK_NODES,
                    "calls": len(calls),
                    "texts": len(texts),
                    "billing_entries": len(billing),
                    "deals": NUM_DEALS,
                    "documents": len(documents),
                    "coverage_areas": len(coverage_areas),
                    "equipment": len(equipment),
                    "spectrum_licenses": len(spectrum_licenses),
                    "outages": len(outages),
                    "service_interactions": len(service_interactions),
                    "interactions": len(interactions),
                    "number_portability": len(number_portability),
                    "voip_services": len(voip_services),
                    "iot_devices": len(iot_devices),
                    "referrals": len(referrals),
                    "device_upgrades": len(device_upgrades),
                    "family_plans": len(family_plans),
                    "family_plan_members": len(family_plan_members),
                    "loyalty_rewards": len(loyalty_rewards),
                    "campaigns": len(campaigns),
                    "feedback": len(feedback),
                    "clickhouse": {
                        "cdr_data": len(cdr_data),
                        "network_performance": len(network_perf),
                        "data_usage": len(data_usage),
                        "months_back": CLICKHOUSE_MONTHS_BACK,
                        "records_per_customer": CLICKHOUSE_RECORDS_PER_CUSTOMER
                    }
                }
            }
            json.dump(summary, f, indent=2)
        print(f"Summary written to {OUTPUT_DIR}/generation_summary.json")

    print("\nData generation complete!")
    print(f"CSV files have been written to the {OUTPUT_DIR} directory")
    print("You can now load these files into your database using the appropriate import commands")

if __name__ == "__main__":
    main()