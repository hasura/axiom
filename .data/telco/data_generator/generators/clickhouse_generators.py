"""
ClickHouse Data Generators

This module contains functions to generate data for ClickHouse tables in the telco schema.
Supports variable data volumes through two parameters: months_back and records_per_customer.
"""

import random
import datetime
from faker import Faker
from typing import Dict, List, Any

# Initialize Faker
fake = Faker()

# Default data generation parameters
DEFAULT_MONTHS_BACK = 6
DEFAULT_RECORDS_PER_CUSTOMER = 50

def generate_cdr_data(customer_links: List[Dict], calls: List[Dict], months_back=None, records_per_customer=None) -> List[Dict]:
    """
    Generate Call Detail Records (CDR) data based on existing call data.

    Args:
        customer_links: List of customer link dictionaries
        calls: List of call dictionaries
        months_back: Number of months to generate data back in time
        records_per_customer: Number of records to generate per customer

    Returns:
        List of CDR data dictionaries
    """
    cdr_data = []

    # Determine configuration parameters
    _months_back = months_back if months_back is not None else DEFAULT_MONTHS_BACK
    _records_per_customer = records_per_customer if records_per_customer is not None else DEFAULT_RECORDS_PER_CUSTOMER

    # Create a mapping from customer_id to GUID
    customer_id_to_guid = {link["customer_id"]: link["customer_guid"] for link in customer_links}

    # Start date based on months_back
    start_date = datetime.datetime.now() - datetime.timedelta(days=30 * _months_back)

    # For each customer, generate the specified number of CDR records
    for customer_id, guid in customer_id_to_guid.items():
        # If we have call data for this customer, use it as a template
        customer_calls = [call for call in calls if call["CustomerID"] == customer_id]
        call_template = customer_calls[0] if customer_calls else None

        for i in range(_records_per_customer):
            # Calculate timestamp (distribute evenly over the time range)
            days_to_add = int((30 * _months_back * i) / _records_per_customer)
            timestamp = start_date + datetime.timedelta(days=days_to_add,
                                                        hours=random.randint(0, 23),
                                                        minutes=random.randint(0, 59))

            if call_template:
                # Use call template for realistic values
                call_duration = call_template["Duration"]
                call_type = call_template["CallType"]
            else:
                # Generate random values
                call_duration = random.randint(10, 1800)  # 10s to 30min
                call_types = ["Outgoing", "Incoming", "Missed", "Conference", "Video"]
                call_type = random.choice(call_types)

            # Add some variability
            call_duration = max(0, call_duration + random.randint(-60, 60))

            cdr_data.append({
                "CUID": customer_id,
                "GUID": guid,
                "Call_Duration": call_duration,
                "Call_Type": call_type,
                "Timestamp": timestamp.isoformat()
            })

    return cdr_data

def generate_network_performance(customer_links: List[Dict], months_back=None, records_per_customer=None) -> List[Dict]:
    """
    Generate network performance data.

    Args:
        customer_links: List of customer link dictionaries
        months_back: Number of months to generate data back in time
        records_per_customer: Number of records to generate per customer

    Returns:
        List of network performance dictionaries
    """
    network_performance = []

    # Determine configuration parameters
    _months_back = months_back if months_back is not None else DEFAULT_MONTHS_BACK
    _records_per_customer = records_per_customer if records_per_customer is not None else DEFAULT_RECORDS_PER_CUSTOMER

    # Start date based on months_back
    start_date = datetime.datetime.now() - datetime.timedelta(days=30 * _months_back)

    for link in customer_links:
        customer_id = link["customer_id"]
        guid = link["customer_guid"]
        
        for i in range(_records_per_customer):
            # Calculate timestamp (distribute evenly over the time range)
            days_to_add = int((30 * _months_back * i) / _records_per_customer)
            timestamp = start_date + datetime.timedelta(days=days_to_add,
                                                        hours=random.randint(0, 23),
                                                        minutes=random.randint(0, 59))

            # Generate realistic network performance metrics
            # Urban areas (lower customer IDs) tend to have better performance
            urban_factor = max(0.5, min(1.5, 1.0 - (customer_id / (len(customer_links) * 2))))

            download_speed = random.uniform(5.0, 150.0) * urban_factor
            upload_speed = random.uniform(1.0, 50.0) * urban_factor
            latency = random.randint(10, 200) * (2 - urban_factor)

            # Time of day affects performance (peak hours have slower speeds)
            hour = timestamp.hour
            if 17 <= hour <= 22:  # Evening peak
                download_speed *= 0.7
                upload_speed *= 0.7
                latency *= 1.3
            
            network_performance.append({
                "CUID": customer_id,
                "GUID": guid,
                "Download_Speed": round(download_speed, 2),
                "Upload_Speed": round(upload_speed, 2),
                "Latency": int(latency),
                "Timestamp": timestamp.isoformat()
            })
    
    return network_performance

def generate_data_usage(customer_links: List[Dict], months_back=None, records_per_customer=None) -> List[Dict]:
    """
    Generate data usage records.

    Args:
        customer_links: List of customer link dictionaries
        months_back: Number of months to generate data back in time
        records_per_customer: Number of records to generate per customer

    Returns:
        List of data usage dictionaries
    """
    data_usage = []

    # Determine configuration parameters
    _months_back = months_back if months_back is not None else DEFAULT_MONTHS_BACK
    _records_per_customer = records_per_customer if records_per_customer is not None else DEFAULT_RECORDS_PER_CUSTOMER

    # Start date based on months_back
    start_date = datetime.datetime.now() - datetime.timedelta(days=30 * _months_back)

    for link in customer_links:
        customer_id = link["customer_id"]
        guid = link["customer_guid"]

        # Generate a usage pattern for this customer
        # Some customers use more data than others
        usage_multiplier = random.uniform(0.2, 3.0)

        for i in range(_records_per_customer):
            # Calculate timestamp (distribute evenly over the time range)
            days_to_add = int((30 * _months_back * i) / _records_per_customer)
            timestamp = start_date + datetime.timedelta(days=days_to_add,
                                                        hours=random.randint(0, 23),
                                                        minutes=random.randint(0, 59))
            
            # Base data usage in GB (0.01 to 5 GB per record)
            base_usage = random.uniform(0.01, 5.0)

            # Apply customer's usage pattern
            data_usage_gb = base_usage * usage_multiplier

            # Time of day affects usage
            hour = timestamp.hour
            if 17 <= hour <= 23:  # Evening usage is higher
                data_usage_gb *= 1.5
            elif 0 <= hour <= 6:  # Night usage is lower
                data_usage_gb *= 0.3

            # Weekend usage differs
            if timestamp.weekday() >= 5:  # Weekend
                data_usage_gb *= 1.3

            data_usage.append({
                "CUID": customer_id,
                "GUID": guid,
                "Data_Usage": round(data_usage_gb, 2),
                "Timestamp": timestamp.isoformat()
            })

    return data_usage