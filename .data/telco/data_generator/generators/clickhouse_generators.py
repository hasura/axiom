"""
ClickHouse Data Generators

This module contains functions to generate data for ClickHouse tables in the telco schema.
Supports variable data volumes through two parameters: months_back and records_per_customer.
Optimized for high performance with large datasets using vectorization and parallel processing.
"""

import random
import datetime
import time
import multiprocessing
import os
import itertools
from concurrent.futures import ProcessPoolExecutor
import numpy as np
from faker import Faker
from typing import Dict, List, Any, Tuple, Callable, Generator, Iterator
from functools import partial

# Initialize Faker with seed for reproducibility
random.seed(42)
np.random.seed(42)
fake = Faker()
fake.seed_instance(42)

# Default data generation parameters
DEFAULT_MONTHS_BACK = 6
DEFAULT_RECORDS_PER_CUSTOMER = 50

# Performance tuning parameters
NUM_PROCESSES = max(1, min(32, multiprocessing.cpu_count() - 1))  # Cap at reasonable number
CHUNK_SIZE = 10000  # Optimal chunk size for ProcessPoolExecutor
# Adjust batch size based on available memory and CPU cores
MEMORY_PER_CORE_GB = 2  # Estimated memory per core in GB
BATCH_SIZE_FACTOR = int(os.environ.get('BATCH_SIZE_FACTOR', '2'))  # Can be tuned via env var

def _vectorized_timestamps(start_date_timestamp: float, days_per_record: float,
                          count: int) -> List[Tuple[datetime.datetime, int, int]]:
    """
    Generate timestamps in a vectorized way using NumPy.
    
    Args:
        start_date_timestamp: Start date as timestamp
        days_per_record: Days between records
        count: Number of timestamps to generate
        
    Returns:
        List of (timestamp, hour, weekday) tuples
    """
    # Create evenly spaced days
    days = np.arange(count) * days_per_record
    
    # Generate random hours and minutes
    hours = np.random.randint(0, 24, count)
    minutes = np.random.randint(0, 60, count)
    
    # Convert to datetime objects
    start_date = datetime.datetime.fromtimestamp(start_date_timestamp)
    timestamps = []
    
    # Vectorized calculation
    for i in range(count):
        ts = start_date + datetime.timedelta(days=int(days[i]),
                                            hours=int(hours[i]),
                                            minutes=int(minutes[i]))
        timestamps.append((ts, hours[i], ts.weekday()))
    
    return timestamps

def _process_cdr_batch(batch_args: Tuple) -> List[Dict]:
    """
    Process a batch of customers for CDR data generation.
    
    Args:
        batch_args: Tuple containing batch parameters
        
    Returns:
        List of CDR data dictionaries for this batch
    """
    (batch_customer_ids, customer_id_to_guid, call_templates,
     start_date_timestamp, days_per_record, call_types, records_per_customer) = batch_args
    
    # Pre-allocate result array for better memory efficiency
    batch_size = len(batch_customer_ids) * records_per_customer
    batch_data = []
    batch_data.reserve(batch_size) if hasattr(list, 'reserve') else None  # Reserve if available
    
    # Process customers in chunks for better cache locality
    for chunk_start in range(0, len(batch_customer_ids), 100):
        chunk_end = min(chunk_start + 100, len(batch_customer_ids))
        chunk_customer_ids = batch_customer_ids[chunk_start:chunk_end]
        
        for customer_id in chunk_customer_ids:
            guid = customer_id_to_guid[customer_id]
            call_template = call_templates.get(customer_id)
            
            # Pre-determine call characteristics for this customer
            if call_template:
                base_call_duration = call_template["Duration"]
                base_call_type = call_template["CallType"]
            else:
                base_call_duration = random.randint(10, 1800)  # 10s to 30min
                base_call_type = random.choice(call_types)
            
            # Use NumPy for vectorized random generation - much faster for large arrays
            days_to_add = np.arange(records_per_customer) * days_per_record
            hours = np.random.randint(0, 24, records_per_customer)
            minutes = np.random.randint(0, 60, records_per_customer)
            duration_adjustments = np.random.randint(-60, 61, records_per_customer)
            call_type_randoms = np.random.random(records_per_customer)
            
            # Convert timestamp back to datetime for processing
            start_date = datetime.datetime.fromtimestamp(start_date_timestamp)
            
            # Generate all records for this customer
            for i in range(records_per_customer):
                # Calculate timestamp (distribute evenly over the time range)
                timestamp = start_date + datetime.timedelta(days=int(days_to_add[i]),
                                                          hours=int(hours[i]),
                                                          minutes=int(minutes[i]))
                
                # Add some variability to call duration
                call_duration = max(0, base_call_duration + int(duration_adjustments[i]))
                
                # Occasionally vary call type
                call_type = base_call_type if call_type_randoms[i] < 0.8 else random.choice(call_types)
                
                batch_data.append({
                    "CUID": customer_id,
                    "GUID": guid,
                    "Call_Duration": call_duration,
                    "Call_Type": call_type,
                    "Timestamp": timestamp.isoformat()
                })
    
    return batch_data

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
    start_time = time.time()
    
    # Determine configuration parameters
    _months_back = months_back if months_back is not None else DEFAULT_MONTHS_BACK
    _records_per_customer = records_per_customer if records_per_customer is not None else DEFAULT_RECORDS_PER_CUSTOMER
    
    print(f"Generating CDR data for {len(customer_links)} customers with {_records_per_customer} records each...")
    
    # Create a mapping from customer_id to GUID - use dictionary comprehension for efficiency
    customer_id_to_guid = {link["customer_id"]: link["customer_guid"] for link in customer_links}
    
    # Create a mapping from customer_id to call template - optimize with a single pass through calls
    customer_id_set = set(customer_id_to_guid.keys())
    
    # Group calls by customer ID for faster lookup - use dictionary comprehension
    calls_by_customer = {}
    # Use a more efficient approach for large call volumes
    if len(calls) > 100000:
        # Create index for faster lookup
        customer_id_to_idx = {cid: i for i, cid in enumerate(customer_id_set)}
        # Pre-allocate array
        call_matches = [None] * len(customer_id_set)
        
        for call in calls:
            customer_id = call["CustomerID"]
            if customer_id in customer_id_to_idx and call_matches[customer_id_to_idx[customer_id]] is None:
                call_matches[customer_id_to_idx[customer_id]] = call
        
        # Convert back to dictionary
        calls_by_customer = {cid: call_matches[customer_id_to_idx[cid]]
                            for cid in customer_id_set
                            if call_matches[customer_id_to_idx[cid]] is not None}
    else:
        # Original approach for smaller datasets
        for call in calls:
            customer_id = call["CustomerID"]
            if customer_id in customer_id_set and customer_id not in calls_by_customer:
                calls_by_customer[customer_id] = call
    
    # Pre-calculate common values
    start_date = datetime.datetime.now() - datetime.timedelta(days=30 * _months_back)
    start_date_timestamp = start_date.timestamp()  # Convert to timestamp for serialization
    days_per_record = (30 * _months_back) / _records_per_customer
    call_types = ["Outgoing", "Incoming", "Missed", "Conference", "Video"]
    
    # Calculate optimal batch size based on available memory and CPU cores
    available_memory_gb = MEMORY_PER_CORE_GB * NUM_PROCESSES
    records_per_batch = min(
        10000,  # Cap at 10,000 customers per batch
        max(1000, int(available_memory_gb * 1e9 / (_records_per_customer * 200 * BATCH_SIZE_FACTOR)))
    )
    
    batch_size = max(1000, min(records_per_batch, len(customer_id_to_guid) // (NUM_PROCESSES * 2)))
    num_customers = len(customer_id_to_guid)
    num_batches = (num_customers + batch_size - 1) // batch_size
    
    customer_ids = list(customer_id_to_guid.keys())
    
    # Prepare batch arguments for parallel processing
    batch_args = []
    for batch_idx in range(num_batches):
        start_idx = batch_idx * batch_size
        end_idx = min((batch_idx + 1) * batch_size, num_customers)
        batch_customer_ids = customer_ids[start_idx:end_idx]
        
        # Create a subset of call templates for this batch
        batch_call_templates = {cid: calls_by_customer.get(cid) for cid in batch_customer_ids}
        
        batch_args.append((
            batch_customer_ids,
            customer_id_to_guid,
            batch_call_templates,
            start_date_timestamp,
            days_per_record,
            call_types,
            _records_per_customer
        ))
    
    # Process batches in parallel with optimized chunksize
    cdr_data = []
    with ProcessPoolExecutor(max_workers=NUM_PROCESSES) as executor:
        # Use chunksize parameter for better performance with many small tasks
        results = executor.map(_process_cdr_batch, batch_args, chunksize=1)
        
        for batch_idx, batch_result in enumerate(results):
            if batch_idx % max(1, num_batches // 20) == 0:  # Show progress ~20 times
                elapsed = time.time() - start_time
                print(f"CDR: Processing batch {batch_idx+1}/{num_batches} ({(batch_idx+1)/num_batches*100:.1f}%) - Elapsed: {elapsed:.1f}s")
            cdr_data.extend(batch_result)
    
    elapsed = time.time() - start_time
    print(f"CDR data generation complete. Generated {len(cdr_data)} records in {elapsed:.1f} seconds")
    return cdr_data

def _process_network_batch(batch_args: Tuple) -> List[Dict]:
    """
    Process a batch of customers for network performance data generation.
    
    Args:
        batch_args: Tuple containing batch parameters
        
    Returns:
        List of network performance dictionaries for this batch
    """
    (batch_links, start_date_timestamp, days_per_record,
     total_customers, records_per_customer) = batch_args
    
    # Convert timestamp back to datetime for processing
    start_date = datetime.datetime.fromtimestamp(start_date_timestamp)
    
    # Pre-allocate result array for better memory efficiency
    batch_size = len(batch_links) * records_per_customer
    batch_data = []
    batch_data.reserve(batch_size) if hasattr(list, 'reserve') else None  # Reserve if available
    
    # Process customers in chunks for better cache locality
    for chunk_start in range(0, len(batch_links), 100):
        chunk_end = min(chunk_start + 100, len(batch_links))
        chunk_links = batch_links[chunk_start:chunk_end]
        
        for link in chunk_links:
            customer_id = link["customer_id"]
            guid = link["customer_guid"]
            
            # Pre-calculate customer-specific factors
            urban_factor = max(0.5, min(1.5, 1.0 - (customer_id / (total_customers * 2))))
            base_download = random.uniform(5.0, 150.0) * urban_factor
            base_upload = random.uniform(1.0, 50.0) * urban_factor
            base_latency = random.randint(10, 200) * (2 - urban_factor)
            
            # Use NumPy for vectorized random generation - much faster for large arrays
            days_to_add = np.arange(records_per_customer) * days_per_record
            hours = np.random.randint(0, 24, records_per_customer)
            minutes = np.random.randint(0, 60, records_per_customer)
            download_factors = np.random.uniform(0.8, 1.2, records_per_customer)
            upload_factors = np.random.uniform(0.8, 1.2, records_per_customer)
            latency_factors = np.random.uniform(0.9, 1.1, records_per_customer)
            
            # Generate all timestamps at once using vectorized function
            timestamps = _vectorized_timestamps(start_date_timestamp, days_per_record, records_per_customer)
            
            # Generate all records for this customer
            for i, (timestamp, hour, weekday) in enumerate(timestamps):
                # Add variability to base metrics
                download_speed = base_download * download_factors[i]
                upload_speed = base_upload * upload_factors[i]
                latency = base_latency * latency_factors[i]
                
                # Time of day affects performance (peak hours have slower speeds)
                if 17 <= hour <= 22:  # Evening peak
                    download_speed *= 0.7
                    upload_speed *= 0.7
                    latency *= 1.3
                
                batch_data.append({
                    "CUID": customer_id,
                    "GUID": guid,
                    "Download_Speed": round(download_speed, 2),
                    "Upload_Speed": round(upload_speed, 2),
                    "Latency": int(latency),
                    "Timestamp": timestamp.isoformat()
                })
    
    return batch_data

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
    start_time = time.time()
    
    # Determine configuration parameters
    _months_back = months_back if months_back is not None else DEFAULT_MONTHS_BACK
    _records_per_customer = records_per_customer if records_per_customer is not None else DEFAULT_RECORDS_PER_CUSTOMER
    
    print(f"Generating network performance data for {len(customer_links)} customers with {_records_per_customer} records each...")
    
    # Pre-calculate common values
    start_date = datetime.datetime.now() - datetime.timedelta(days=30 * _months_back)
    start_date_timestamp = start_date.timestamp()  # Convert to timestamp for serialization
    days_per_record = (30 * _months_back) / _records_per_customer
    total_customers = len(customer_links)
    
    # Calculate optimal batch size based on available memory and CPU cores
    available_memory_gb = MEMORY_PER_CORE_GB * NUM_PROCESSES
    records_per_batch = min(
        10000,  # Cap at 10,000 customers per batch
        max(1000, int(available_memory_gb * 1e9 / (_records_per_customer * 200 * BATCH_SIZE_FACTOR)))
    )
    
    batch_size = max(1000, min(records_per_batch, len(customer_links) // (NUM_PROCESSES * 2)))
    num_customers = len(customer_links)
    num_batches = (num_customers + batch_size - 1) // batch_size
    
    # Prepare batch arguments for parallel processing
    batch_args = []
    for batch_idx in range(num_batches):
        start_idx = batch_idx * batch_size
        end_idx = min((batch_idx + 1) * batch_size, num_customers)
        batch_links = customer_links[start_idx:end_idx]
        
        batch_args.append((
            batch_links,
            start_date_timestamp,
            days_per_record,
            total_customers,
            _records_per_customer
        ))
    
    # Process batches in parallel with optimized chunksize
    network_performance = []
    with ProcessPoolExecutor(max_workers=NUM_PROCESSES) as executor:
        # Use chunksize parameter for better performance with many small tasks
        results = executor.map(_process_network_batch, batch_args, chunksize=1)
        
        for batch_idx, batch_result in enumerate(results):
            if batch_idx % max(1, num_batches // 20) == 0:  # Show progress ~20 times
                elapsed = time.time() - start_time
                print(f"Network: Processing batch {batch_idx+1}/{num_batches} ({(batch_idx+1)/num_batches*100:.1f}%) - Elapsed: {elapsed:.1f}s")
            network_performance.extend(batch_result)
    
    elapsed = time.time() - start_time
    print(f"Network performance data generation complete. Generated {len(network_performance)} records in {elapsed:.1f} seconds")
    return network_performance

def _process_data_usage_batch(batch_args: Tuple) -> List[Dict]:
    """
    Process a batch of customers for data usage generation.
    
    Args:
        batch_args: Tuple containing batch parameters
        
    Returns:
        List of data usage dictionaries for this batch
    """
    (batch_links, start_date_timestamp, days_per_record, records_per_customer) = batch_args
    
    # Convert timestamp back to datetime for processing
    start_date = datetime.datetime.fromtimestamp(start_date_timestamp)
    
    # Pre-allocate result array for better memory efficiency
    batch_size = len(batch_links) * records_per_customer
    batch_data = []
    batch_data.reserve(batch_size) if hasattr(list, 'reserve') else None  # Reserve if available
    
    # Process customers in chunks for better cache locality
    for chunk_start in range(0, len(batch_links), 100):
        chunk_end = min(chunk_start + 100, len(batch_links))
        chunk_links = batch_links[chunk_start:chunk_end]
        
        for link in chunk_links:
            customer_id = link["customer_id"]
            guid = link["customer_guid"]
            
            # Generate a usage pattern for this customer
            usage_multiplier = random.uniform(0.2, 3.0)
            
            # Use NumPy for vectorized random generation - much faster for large arrays
            days_to_add = np.arange(records_per_customer) * days_per_record
            hours = np.random.randint(0, 24, records_per_customer)
            minutes = np.random.randint(0, 60, records_per_customer)
            base_usages = np.random.uniform(0.01, 5.0, records_per_customer)
            
            # Generate all timestamps at once using vectorized function
            timestamps = _vectorized_timestamps(start_date_timestamp, days_per_record, records_per_customer)
            
            # Generate all records for this customer
            for i, (timestamp, hour, weekday) in enumerate(timestamps):
                # Base data usage in GB (0.01 to 5 GB per record)
                base_usage = base_usages[i]
                
                # Apply customer's usage pattern
                data_usage_gb = base_usage * usage_multiplier
                
                # Time of day affects usage
                if 17 <= hour <= 23:  # Evening usage is higher
                    data_usage_gb *= 1.5
                elif 0 <= hour <= 6:  # Night usage is lower
                    data_usage_gb *= 0.3
                
                # Weekend usage differs
                if weekday >= 5:  # Weekend
                    data_usage_gb *= 1.3
                
                batch_data.append({
                    "CUID": customer_id,
                    "GUID": guid,
                    "Data_Usage": round(data_usage_gb, 2),
                    "Timestamp": timestamp.isoformat()
                })
    
    return batch_data

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
    start_time = time.time()
    
    # Determine configuration parameters
    _months_back = months_back if months_back is not None else DEFAULT_MONTHS_BACK
    _records_per_customer = records_per_customer if records_per_customer is not None else DEFAULT_RECORDS_PER_CUSTOMER
    
    print(f"Generating data usage for {len(customer_links)} customers with {_records_per_customer} records each...")
    
    # Pre-calculate common values
    start_date = datetime.datetime.now() - datetime.timedelta(days=30 * _months_back)
    start_date_timestamp = start_date.timestamp()  # Convert to timestamp for serialization
    days_per_record = (30 * _months_back) / _records_per_customer
    
    # Calculate optimal batch size based on available memory and CPU cores
    available_memory_gb = MEMORY_PER_CORE_GB * NUM_PROCESSES
    records_per_batch = min(
        10000,  # Cap at 10,000 customers per batch
        max(1000, int(available_memory_gb * 1e9 / (_records_per_customer * 200 * BATCH_SIZE_FACTOR)))
    )
    
    batch_size = max(1000, min(records_per_batch, len(customer_links) // (NUM_PROCESSES * 2)))
    num_customers = len(customer_links)
    num_batches = (num_customers + batch_size - 1) // batch_size
    
    # Prepare batch arguments for parallel processing
    batch_args = []
    for batch_idx in range(num_batches):
        start_idx = batch_idx * batch_size
        end_idx = min((batch_idx + 1) * batch_size, num_customers)
        batch_links = customer_links[start_idx:end_idx]
        
        batch_args.append((
            batch_links,
            start_date_timestamp,
            days_per_record,
            _records_per_customer
        ))
    
    # Process batches in parallel with optimized chunksize
    data_usage = []
    with ProcessPoolExecutor(max_workers=NUM_PROCESSES) as executor:
        # Use chunksize parameter for better performance with many small tasks
        results = executor.map(_process_data_usage_batch, batch_args, chunksize=1)
        
        for batch_idx, batch_result in enumerate(results):
            if batch_idx % max(1, num_batches // 20) == 0:  # Show progress ~20 times
                elapsed = time.time() - start_time
                print(f"Data Usage: Processing batch {batch_idx+1}/{num_batches} ({(batch_idx+1)/num_batches*100:.1f}%) - Elapsed: {elapsed:.1f}s")
            data_usage.extend(batch_result)
    
    elapsed = time.time() - start_time
    print(f"Data usage generation complete. Generated {len(data_usage)} records in {elapsed:.1f} seconds")
    return data_usage