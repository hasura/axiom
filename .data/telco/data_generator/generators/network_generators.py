"""
Network Data Generators

This module contains functions to generate data for network-related tables in the telco schema.
"""

import random
import datetime
from faker import Faker
from typing import Dict, List, Any

# Initialize Faker
fake = Faker()

# Constants
TECHNOLOGIES = ["2G", "3G", "4G", "5G"]
TERRAIN_TYPES = ["Urban", "Suburban", "Rural", "Mountainous", "Coastal", "Desert", "Forest"]
EQUIPMENT_TYPES = ["Base Station", "Antenna", "Router", "Switch", "Repeater", "Power Supply", "Cooling System"]
MANUFACTURERS = ["Ericsson", "Nokia", "Huawei", "Cisco", "Samsung", "ZTE", "Juniper Networks"]
EQUIPMENT_STATUSES = ["active", "maintenance", "offline", "decommissioned"]
FREQUENCY_BANDS = ["700 MHz", "850 MHz", "900 MHz", "1800 MHz", "1900 MHz", "2100 MHz", "2300 MHz", "2600 MHz", "3500 MHz", "28 GHz", "39 GHz"]
GEOGRAPHIC_AREAS = ["National", "Regional", "Metropolitan", "Rural", "Coastal", "Border"]
REGULATORY_AUTHORITIES = ["FCC", "OFCOM", "ACMA", "CRTC", "TRAI", "ETSI", "ITU"]
OUTAGE_SEVERITIES = ["minor", "major", "critical"]
OUTAGE_CAUSES = [
    "Hardware Failure", "Software Bug", "Power Outage", "Natural Disaster", 
    "Scheduled Maintenance", "Fiber Cut", "Capacity Overload", "Configuration Error",
    "Cyber Attack", "Human Error", "Third-party Service Disruption"
]

def generate_coverage_areas(network_nodes: List[Dict]) -> List[Dict]:
    """Generate network coverage areas data."""
    coverage_areas = []
    coverage_id = 1
    
    for node in network_nodes:
        node_id = node["node_id"]
        
        # Each node can have multiple technology coverages
        num_technologies = random.randint(1, 4)  # 1 to 4 technologies per node
        selected_technologies = random.sample(TECHNOLOGIES, num_technologies)
        
        for tech in selected_technologies:
            # Coverage radius depends on technology
            if tech == "2G":
                radius = random.uniform(5.0, 15.0)
            elif tech == "3G":
                radius = random.uniform(3.0, 10.0)
            elif tech == "4G":
                radius = random.uniform(2.0, 8.0)
            else:  # 5G
                radius = random.uniform(0.5, 3.0)
                
            # Signal strength depends on technology
            if tech == "2G":
                signal_strength = random.randint(-110, -90)
            elif tech == "3G":
                signal_strength = random.randint(-105, -85)
            elif tech == "4G":
                signal_strength = random.randint(-100, -80)
            else:  # 5G
                signal_strength = random.randint(-95, -75)
                
            # Population covered based on radius and terrain
            terrain = random.choice(TERRAIN_TYPES)
            if terrain in ["Urban", "Suburban"]:
                population_factor = random.uniform(5000, 20000)
            else:
                population_factor = random.uniform(100, 5000)
                
            population_covered = int(radius * radius * population_factor)
            
            # Last upgraded date
            if tech == "5G":
                last_upgraded = fake.date_time_between(start_date="-1y", end_date="now").date()
            elif tech == "4G":
                last_upgraded = fake.date_time_between(start_date="-5y", end_date="-1y").date()
            elif tech == "3G":
                last_upgraded = fake.date_time_between(start_date="-10y", end_date="-5y").date()
            else:  # 2G
                last_upgraded = fake.date_time_between(start_date="-20y", end_date="-10y").date()
            
            coverage_areas.append({
                "coverage_id": coverage_id,
                "node_id": node_id,
                "technology": tech,
                "coverage_radius_km": round(radius, 2),
                "population_covered": population_covered,
                "terrain_type": terrain,
                "signal_strength_dbm": signal_strength,
                "last_upgraded": last_upgraded.isoformat()
            })
            
            coverage_id += 1
    
    return coverage_areas

def generate_equipment(network_nodes: List[Dict]) -> List[Dict]:
    """Generate network equipment data."""
    equipment_list = []
    equipment_id = 1
    
    for node in network_nodes:
        node_id = node["node_id"]
        
        # Each node has multiple equipment pieces
        num_equipment = random.randint(3, 8)  # 3 to 8 equipment pieces per node
        
        for _ in range(num_equipment):
            equipment_type = random.choice(EQUIPMENT_TYPES)
            manufacturer = random.choice(MANUFACTURERS)
            
            # Model depends on manufacturer and type
            model = f"{manufacturer[:3].upper()}-{equipment_type[:3].upper()}{random.randint(1000, 9999)}"
            
            # Serial number
            serial_number = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=12))
            
            # Installation date
            installation_date = fake.date_time_between(start_date="-10y", end_date="-1m").date()
            
            # Last maintenance date
            last_maintenance_date = fake.date_time_between(start_date=installation_date, end_date="now").date()
            
            # Firmware version
            firmware_version = f"{random.randint(1, 9)}.{random.randint(0, 9)}.{random.randint(0, 9)}"
            
            # Status
            status = random.choice(EQUIPMENT_STATUSES)
            
            # Capacity depends on equipment type
            if equipment_type in ["Base Station", "Router", "Switch"]:
                capacity = random.randint(1000, 10000)
            else:
                capacity = random.randint(100, 1000)
                
            # Power consumption
            power_consumption = random.randint(50, 500)
            
            equipment_list.append({
                "equipment_id": equipment_id,
                "node_id": node_id,
                "equipment_type": equipment_type,
                "manufacturer": manufacturer,
                "model": model,
                "serial_number": serial_number,
                "installation_date": installation_date.isoformat(),
                "last_maintenance_date": last_maintenance_date.isoformat(),
                "firmware_version": firmware_version,
                "status": status,
                "capacity_mbps": capacity,
                "power_consumption_watts": power_consumption
            })
            
            equipment_id += 1
    
    return equipment_list

def generate_spectrum_licenses() -> List[Dict]:
    """Generate spectrum licenses data."""
    licenses = []
    license_id = 1
    
    # Generate 10-20 spectrum licenses
    num_licenses = random.randint(10, 20)
    
    for _ in range(num_licenses):
        frequency_band = random.choice(FREQUENCY_BANDS)
        
        # Bandwidth depends on frequency band
        if "GHz" in frequency_band:
            bandwidth = round(random.uniform(50.0, 800.0), 2)
        else:
            bandwidth = round(random.uniform(5.0, 40.0), 2)
            
        geographic_area = random.choice(GEOGRAPHIC_AREAS)
        
        # Acquisition date
        acquisition_date = fake.date_time_between(start_date="-15y", end_date="-1y").date()
        
        # Expiration date (10-15 years after acquisition)
        years_valid = random.randint(10, 15)
        expiration_date = datetime.date(
            acquisition_date.year + years_valid,
            acquisition_date.month,
            acquisition_date.day
        )
        
        # Cost depends on bandwidth and frequency
        if "GHz" in frequency_band:
            cost_factor = random.uniform(0.5, 2.0)
        else:
            cost_factor = random.uniform(2.0, 10.0)
            
        cost = round(bandwidth * cost_factor, 2)
        
        # Regulatory authority
        regulatory_authority = random.choice(REGULATORY_AUTHORITIES)
        
        # License number
        license_number = f"LIC-{regulatory_authority}-{random.randint(10000, 99999)}"
        
        licenses.append({
            "license_id": license_id,
            "frequency_band": frequency_band,
            "bandwidth_mhz": bandwidth,
            "geographic_area": geographic_area,
            "acquisition_date": acquisition_date.isoformat(),
            "expiration_date": expiration_date.isoformat(),
            "cost_million_usd": cost,
            "regulatory_authority": regulatory_authority,
            "license_number": license_number
        })
        
        license_id += 1
    
    return licenses

def generate_outages(network_nodes: List[Dict]) -> List[Dict]:
    """Generate network outages data."""
    outages = []
    outage_id = 1
    
    for node in network_nodes:
        node_id = node["node_id"]
        
        # Each node has 0-3 outages
        num_outages = random.randint(0, 3)
        
        for _ in range(num_outages):
            # Start time within the last year
            start_time = fake.date_time_between(start_date="-1y", end_date="now")
            
            # Severity
            severity = random.choice(OUTAGE_SEVERITIES)
            
            # Duration depends on severity
            if severity == "minor":
                duration_hours = random.uniform(0.5, 4.0)
            elif severity == "major":
                duration_hours = random.uniform(4.0, 12.0)
            else:  # critical
                duration_hours = random.uniform(12.0, 48.0)
                
            # End time (some recent outages might still be ongoing)
            if start_time > datetime.datetime.now() - datetime.timedelta(days=2) and random.random() < 0.3:
                end_time = None
            else:
                end_time = start_time + datetime.timedelta(hours=duration_hours)
            
            # Cause
            cause = random.choice(OUTAGE_CAUSES)
            
            # Affected customers
            if severity == "minor":
                affected_customers = random.randint(10, 500)
            elif severity == "major":
                affected_customers = random.randint(500, 5000)
            else:  # critical
                affected_customers = random.randint(5000, 50000)
                
            # Resolution
            if end_time:
                if cause == "Hardware Failure":
                    resolution = f"Replaced faulty {random.choice(EQUIPMENT_TYPES).lower()}. Performed system diagnostics to verify fix."
                elif cause == "Software Bug":
                    resolution = f"Applied emergency patch {random.randint(1, 9)}.{random.randint(0, 9)}.{random.randint(0, 9)}. Scheduled comprehensive update."
                elif cause == "Power Outage":
                    resolution = "Restored main power supply. Improved backup power systems to prevent future incidents."
                elif cause == "Fiber Cut":
                    resolution = "Repaired damaged fiber optic cable. Implemented redundant routing to minimize future impact."
                elif cause == "Configuration Error":
                    resolution = "Rolled back to previous working configuration. Updated change management procedures."
                else:
                    resolution = fake.paragraph(nb_sentences=1)
            else:
                resolution = "Ongoing investigation. Technicians dispatched to site."
            
            outages.append({
                "outage_id": outage_id,
                "node_id": node_id,
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat() if end_time else None,
                "affected_customers": affected_customers,
                "severity": severity,
                "cause": cause,
                "resolution": resolution
            })
            
            outage_id += 1
    
    return outages