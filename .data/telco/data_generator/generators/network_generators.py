"""
Network Data Generators - Modified for Realistic Patterns

This module contains functions to generate data for network-related tables in the telco schema
with realistic patterns that can be analyzed for insights and trends.
"""

import random
import datetime
import math
from faker import Faker
from typing import Dict, List, Any

# Initialize Faker
fake = Faker()

# Constants with realistic distributions
TECHNOLOGIES = ["2G", "3G", "4G", "5G"]
TERRAIN_TYPES = ["Urban", "Suburban", "Rural", "Mountainous", "Coastal", "Desert", "Forest"]
EQUIPMENT_TYPES = ["Base Station", "Antenna", "Router", "Switch", "Repeater", "Power Supply", "Cooling System"]
MANUFACTURERS = {
    "Ericsson": 0.25,    # 25% market share
    "Nokia": 0.2,        # 20% market share
    "Huawei": 0.2,       # 20% market share
    "Cisco": 0.15,       # 15% market share
    "Samsung": 0.1,      # 10% market share
    "ZTE": 0.07,         # 7% market share
    "Juniper Networks": 0.03  # 3% market share
}
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

# Technology rollout phases
TECHNOLOGY_ROLLOUT = {
    "5G": {
        "Urban": 0.85,      # 85% of urban areas have 5G
        "Suburban": 0.6,    # 60% of suburban areas
        "Rural": 0.2,       # 20% of rural areas
        "Mountainous": 0.15, # 15% of mountainous regions
        "Coastal": 0.4,     # 40% of coastal areas
        "Desert": 0.1,      # 10% of desert regions
        "Forest": 0.1       # 10% of forested regions
    },
    "4G": {
        "Urban": 0.98,      # 98% of urban areas have 4G
        "Suburban": 0.95,   # 95% of suburban areas
        "Rural": 0.8,       # 80% of rural areas
        "Mountainous": 0.7, # 70% of mountainous regions
        "Coastal": 0.9,     # 90% of coastal areas
        "Desert": 0.6,      # 60% of desert regions
        "Forest": 0.7       # 70% of forested regions
    },
    "3G": {
        "Urban": 0.9,       # 90% of urban areas maintain 3G
        "Suburban": 0.95,   # 95% of suburban areas
        "Rural": 0.9,       # 90% of rural areas
        "Mountainous": 0.85, # 85% of mountainous regions
        "Coastal": 0.9,     # 90% of coastal areas
        "Desert": 0.8,      # 80% of desert regions
        "Forest": 0.85      # 85% of forested regions
    },
    "2G": {
        "Urban": 0.5,       # 50% of urban areas still have 2G (being phased out)
        "Suburban": 0.6,    # 60% of suburban areas
        "Rural": 0.9,       # 90% of rural areas still depend on 2G
        "Mountainous": 0.85, # 85% of mountainous regions
        "Coastal": 0.7,     # 70% of coastal areas
        "Desert": 0.8,      # 80% of desert regions
        "Forest": 0.85      # 85% of forested regions
    }
}

# Equipment reliability by manufacturer (higher is better)
MANUFACTURER_RELIABILITY = {
    "Ericsson": 0.95,
    "Nokia": 0.94,
    "Huawei": 0.93,
    "Cisco": 0.94,
    "Samsung": 0.92,
    "ZTE": 0.9,
    "Juniper Networks": 0.93
}

# Regional weather patterns affecting outages
REGIONAL_WEATHER_RISK = {
    "Urban": 0.05,      # 5% weather-related risk
    "Suburban": 0.07,   # 7% weather-related risk
    "Rural": 0.1,       # 10% weather-related risk
    "Mountainous": 0.2, # 20% weather-related risk
    "Coastal": 0.15,    # 15% weather-related risk (storms)
    "Desert": 0.08,     # 8% weather-related risk (heat)
    "Forest": 0.12      # 12% weather-related risk
}

# Equipment age vs. failure rate model
def calculate_failure_rate(age_years):
    """Calculate realistic failure rate based on equipment age."""
    # Bathtub curve model: higher failure rates when very new or very old
    if age_years < 0.5:
        # Early life failures
        return 0.05 - 0.06 * age_years  # Starts at 5%, decreases to 2%
    elif age_years < 5:
        # Stable middle life
        return 0.02
    else:
        # Wear-out phase - exponential increase in failure rate
        return 0.02 * math.exp(0.3 * (age_years - 5))  # Exponential growth after 5 years

def determine_node_quality(node):
    """Determine node quality based on location and capacity."""
    # Urban and higher capacity nodes typically have better quality
    base_quality = 0.5
    
    # Factor in latitude/longitude - approximating that nodes in certain areas are newer/better maintained
    lat, lon = node["latitude"], node["longitude"]
    
    # Simple geographic quality patterns (this is a simplification - in reality,
    # you'd have more complex geographic patterns)
    geographic_factor = (math.sin(lat * 0.1) + math.cos(lon * 0.1)) * 0.1
    
    # Capacity factor - higher capacity often means newer equipment
    capacity_factor = min(0.3, node["capacity"] / 10000 * 0.3)
    
    # Status factor
    status_factor = 0.2 if node["status"] == "Active" else -0.2
    
    # Combine factors
    quality = max(0.1, min(0.9, base_quality + geographic_factor + capacity_factor + status_factor))
    
    return quality

def generate_coverage_areas(network_nodes: List[Dict]) -> List[Dict]:
    """Generate network coverage areas data with realistic patterns."""
    coverage_areas = []
    coverage_id = 1
    
    # Create node lookup for efficiency
    node_lookup = {node["node_id"]: node for node in network_nodes}
    
    # Track which nodes have which technologies
    node_technologies = {}
    
    for node in network_nodes:
        node_id = node["node_id"]
        node_technologies[node_id] = []
        
        # Determine terrain type for this node
        # Use node coordinates to approximate terrain
        lat, lon = node["latitude"], node["longitude"]
        
        # Simple terrain approximation based on coordinates
        if abs(lat - 40) < 1 and abs(lon - (-74)) < 1:
            # New York area - Urban
            terrain = "Urban"
        elif abs(lat - 34) < 1 and abs(lon - (-118)) < 1:
            # Los Angeles area - Urban
            terrain = "Urban"
        elif abs(lat - 41) < 1 and abs(lon - (-87)) < 1:
            # Chicago area - Urban
            terrain = "Urban"
        elif abs(lat - 39) < 5 and abs(lon - (-98)) < 10:
            # Central US - Rural
            terrain = "Rural"
        elif abs(lat - 36) < 3 and abs(lon - (-81)) < 3:
            # Appalachian - Mountainous
            terrain = "Mountainous"
        elif abs(lon - (-122)) < 2 and lat > 32 and lat < 49:
            # West Coast - Coastal
            terrain = "Coastal"
        elif abs(lat - 35) < 5 and abs(lon - (-115)) < 10:
            # Southwest - Desert
            terrain = "Desert"
        elif abs(lat - 45) < 3 and abs(lon - (-93)) < 5:
            # Northern forests - Forest
            terrain = "Forest"
        else:
            # Default to suburban for other areas
            terrain = "Suburban"
        
        # Node quality affects technology presence
        node_quality = determine_node_quality(node)
        
        # Determine which technologies this node supports based on terrain and quality
        for tech in TECHNOLOGIES:
            # Base probability from technology rollout pattern
            terrain_prob = TECHNOLOGY_ROLLOUT[tech].get(terrain, 0.5)
            
            # Adjust by node quality - higher quality nodes more likely to have newer tech
            if tech == "5G":
                adjusted_prob = terrain_prob * (1 + node_quality)
            elif tech == "4G":
                adjusted_prob = terrain_prob * (1 + 0.5 * node_quality)
            elif tech == "3G":
                adjusted_prob = terrain_prob
            else:  # 2G
                # 2G being phased out, especially in high-quality nodes
                adjusted_prob = terrain_prob * (1 - node_quality)
                
            # Cap probability at 1.0
            adjusted_prob = min(1.0, adjusted_prob)
            
            if random.random() < adjusted_prob:
                node_technologies[node_id].append(tech)
        
        # Ensure each node has at least one technology
        if not node_technologies[node_id]:
            # Default to 3G if nothing else
            node_technologies[node_id].append("3G")
        
        # Generate coverage data for each technology
        for tech in node_technologies[node_id]:
            # Coverage radius depends on technology and terrain
            # Realistic coverage areas in km
            base_radius = {
                "5G": 0.8,   # 0.8 km for 5G (shorter range, high frequency)
                "4G": 5.0,   # 5 km for 4G
                "3G": 8.0,   # 8 km for 3G
                "2G": 15.0   # 15 km for 2G (better penetration, lower frequency)
            }
            
            # Terrain factors affect radius
            terrain_factor = {
                "Urban": 0.6,       # Buildings block signals
                "Suburban": 0.8,    # Some obstruction
                "Rural": 1.2,       # Clear line of sight
                "Mountainous": 0.5, # Significant obstruction
                "Coastal": 1.1,     # Good propagation over water
                "Desert": 1.3,      # Very clear line of sight
                "Forest": 0.7       # Trees block signals
            }
            
            # Calculate coverage radius with some randomness
            radius = base_radius[tech] * terrain_factor.get(terrain, 1.0) * random.uniform(0.9, 1.1)
            
            # Signal strength depends on technology, terrain, and node quality
            # Base values in dBm (decibel-milliwatts)
            base_signal = {
                "5G": -85,  # 5G typically -85 dBm
                "4G": -95,  # 4G typically -95 dBm
                "3G": -100, # 3G typically -100 dBm
                "2G": -105  # 2G typically -105 dBm
            }
            
            # Terrain affects signal strength
            signal_terrain_factor = {
                "Urban": -5,        # Urban interference
                "Suburban": -2,     # Some interference
                "Rural": 0,         # Baseline
                "Mountainous": -10, # Significant interference
                "Coastal": -1,      # Slight interference
                "Desert": 2,        # Good conditions
                "Forest": -7        # Significant interference
            }
            
            # Node quality affects signal strength
            quality_signal_boost = int(node_quality * 10)  # 0-9 dBm boost
            
            # Calculate signal strength with some randomness
            signal_strength = base_signal[tech] + signal_terrain_factor.get(terrain, 0) + quality_signal_boost + random.randint(-3, 3)
            
            # Population covered based on radius, terrain, and technology
            # Population density varies by terrain (people per sq km)
            pop_density = {
                "Urban": 5000,      # 5000 people per sq km
                "Suburban": 1000,   # 1000 people per sq km
                "Rural": 50,        # 50 people per sq km
                "Mountainous": 10,  # 10 people per sq km
                "Coastal": 500,     # Varies but often developed
                "Desert": 5,        # Very sparse
                "Forest": 20        # Sparse
            }
            
            # Calculate coverage area in sq km (πr²)
            coverage_area = math.pi * radius * radius
            
            # Calculate population with some randomness
            base_population = int(coverage_area * pop_density.get(terrain, 500))
            population_covered = max(1, int(base_population * random.uniform(0.8, 1.2)))
            
            # Last upgraded date depends on technology
            current_year = datetime.datetime.now().year
            if tech == "5G":
                # 5G is recent
                upgrade_year = random.randint(current_year - 3, current_year)
            elif tech == "4G":
                # 4G rollout was ~2010-2018
                upgrade_year = random.randint(2010, 2018)
            elif tech == "3G":
                # 3G rollout was ~2002-2010
                upgrade_year = random.randint(2002, 2010)
            else:  # 2G
                # 2G rollout was ~1992-2002
                upgrade_year = random.randint(1992, 2002)
                
            # Random month and day
            upgrade_month = random.randint(1, 12)
            upgrade_day = random.randint(1, 28)  # Avoiding month-end issues
            
            last_upgraded = datetime.date(upgrade_year, upgrade_month, upgrade_day)
            
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
    """Generate network equipment data with realistic patterns."""
    equipment_list = []
    equipment_id = 1
    
    # Create node lookup for efficiency
    node_lookup = {node["node_id"]: node for node in network_nodes}
    
    # Track equipment types and ages for later correlation with outages
    node_equipment = {}
    
    for node in network_nodes:
        node_id = node["node_id"]
        node_equipment[node_id] = []
        
        # Node quality affects equipment quantity and age
        node_quality = determine_node_quality(node)
        
        # Technologies deployed at this node affect equipment needs
        # (This would ideally be taken from the coverage_areas function results)
        has_5g = random.random() < (0.3 + 0.5 * node_quality)  # Higher quality nodes more likely to have 5G
        has_4g = random.random() < 0.9  # Most nodes have 4G
        has_3g = random.random() < 0.8  # Many nodes have 3G
        has_2g = random.random() < (0.6 - 0.3 * node_quality)  # Lower quality nodes more likely to still have 2G
        
        # Determine required equipment based on technologies
        required_equipment = {}
        
        # All nodes need these
        required_equipment["Power Supply"] = 1
        required_equipment["Cooling System"] = 1
        
        # Base stations and antennas depend on technologies
        if has_5g:
            required_equipment["Base Station"] = required_equipment.get("Base Station", 0) + 1
            required_equipment["Antenna"] = required_equipment.get("Antenna", 0) + random.randint(2, 4)  # 5G often uses MIMO with multiple antennas
            
        if has_4g:
            required_equipment["Base Station"] = required_equipment.get("Base Station", 0) + 1
            required_equipment["Antenna"] = required_equipment.get("Antenna", 0) + random.randint(1, 2)
            
        if has_3g or has_2g:
            required_equipment["Base Station"] = required_equipment.get("Base Station", 0) + 1
            required_equipment["Antenna"] = required_equipment.get("Antenna", 0) + 1
            
        # Networking equipment
        required_equipment["Router"] = random.randint(1, 2)
        required_equipment["Switch"] = random.randint(1, 3)
        
        # Repeaters for challenging terrain
        terrain = node_lookup[node_id].get("terrain_type", random.choice(TERRAIN_TYPES))
        if terrain in ["Mountainous", "Urban", "Forest"]:
            required_equipment["Repeater"] = random.randint(1, 3)
            
        # Generate equipment for this node
        for equip_type, count in required_equipment.items():
            for _ in range(count):
                # Select manufacturer (weighted by market share)
                manufacturer = random.choices(
                    list(MANUFACTURERS.keys()),
                    weights=list(MANUFACTURERS.values())
                )[0]
                
                # Model depends on manufacturer, type, and generation
                # More recent deployments have newer generation equipment
                if node_quality > 0.7:
                    generation = random.choice(["X", "Pro", "Next", "Ultra"])
                    model_num = random.randint(8000, 9999)
                elif node_quality > 0.4:
                    generation = random.choice(["", "Plus", "Advanced", ""])
                    model_num = random.randint(5000, 7999)
                else:
                    generation = random.choice(["", "Basic", "Standard", ""])
                    model_num = random.randint(1000, 4999)
                    
                model = f"{manufacturer[:3].upper()}-{equip_type[:3].upper()}{model_num}{generation}"
                
                # Serial number
                serial_number = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=12))
                
                # Installation date - correlates with node quality
                # Higher quality nodes have newer equipment
                current_year = datetime.datetime.now().year
                
                if node_quality > 0.7:
                    # High-quality nodes - newer equipment
                    install_year = random.randint(current_year - 5, current_year - 1)
                elif node_quality > 0.4:
                    # Medium-quality nodes - mix of old and new
                    install_year = random.randint(current_year - 10, current_year - 3)
                else:
                    # Low-quality nodes - older equipment
                    install_year = random.randint(current_year - 15, current_year - 8)
                    
                # Random month and day
                install_month = random.randint(1, 12)
                install_day = random.randint(1, 28)  # Avoiding month-end issues
                
                installation_date = datetime.date(install_year, install_month, install_day)
                
                # Age of equipment in years
                equipment_age = (datetime.date.today() - installation_date).days / 365.25
                
                # Last maintenance date - more recent for newer or critical equipment
                if equipment_age < 2 or equip_type in ["Base Station", "Router"]:
                    # Newer or critical equipment - maintained in last year
                    days_since_maintenance = random.randint(30, 365)
                elif equipment_age < 5:
                    # Middle-aged equipment - maintained in last 1-2 years
                    days_since_maintenance = random.randint(180, 730)
                else:
                    # Older equipment - maintained less frequently
                    days_since_maintenance = random.randint(365, 1095)  # 1-3 years
                    
                last_maintenance_date = datetime.date.today() - datetime.timedelta(days=days_since_maintenance)
                
                # Firmware version - newer equipment has newer firmware
                if equipment_age < 2:
                    # Newer equipment - recent firmware
                    major = random.randint(4, 6)
                    minor = random.randint(0, 9)
                    patch = random.randint(0, 9)
                elif equipment_age < 5:
                    # Middle-aged equipment - middle firmware
                    major = random.randint(2, 4)
                    minor = random.randint(0, 9)
                    patch = random.randint(0, 9)
                else:
                    # Older equipment - older firmware
                    major = random.randint(1, 3)
                    minor = random.randint(0, 9)
                    patch = random.randint(0, 9)
                    
                firmware_version = f"{major}.{minor}.{patch}"
                
                # Status - depends on age, quality, and manufacturer reliability
                # Calculate failure probability
                failure_rate = calculate_failure_rate(equipment_age)
                
                # Adjust based on manufacturer reliability
                reliability_factor = MANUFACTURER_RELIABILITY.get(manufacturer, 0.9)
                adjusted_failure_rate = failure_rate * (1 / reliability_factor)
                
                # Randomly assign status based on failure rate
                if random.random() < adjusted_failure_rate * 0.5:
                    status = "offline"  # Critical failure
                elif random.random() < adjusted_failure_rate:
                    status = "maintenance"  # Needs maintenance
                elif equipment_age > 10 and random.random() < 0.3:
                    status = "decommissioned"  # Old equipment being phased out
                else:
                    status = "active"  # Normal operation
                
                # Capacity depends on equipment type, age, and quality
                if equip_type in ["Base Station", "Router", "Switch"]:
                    # Base capacity depends on type
                    if equip_type == "Base Station":
                        base_capacity = 5000
                    elif equip_type == "Router":
                        base_capacity = 8000
                    else:  # Switch
                        base_capacity = 10000
                        
                    # Adjust for age - newer equipment has higher capacity
                    age_factor = max(0.5, 1.0 - (equipment_age / 20))  # Ranges from 0.5 to 1.0
                    
                    # Adjust for quality
                    quality_factor = 0.7 + (node_quality * 0.6)  # Ranges from 0.7 to 1.3
                    
                    # Calculate final capacity
                    capacity = int(base_capacity * age_factor * quality_factor * random.uniform(0.9, 1.1))
                else:
                    # Other equipment types have lower, more fixed capacities
                    capacity_ranges = {
                        "Antenna": (300, 800),
                        "Repeater": (200, 500),
                        "Power Supply": (100, 300),
                        "Cooling System": (50, 150)
                    }
                    capacity_range = capacity_ranges.get(equip_type, (100, 500))
                    capacity = random.randint(*capacity_range)
                
                # Power consumption - newer equipment is often more efficient
                if equipment_age < 3:
                    # Newer equipment - more efficient
                    efficiency_factor = 0.8
                elif equipment_age < 7:
                    # Middle-aged equipment - standard efficiency
                    efficiency_factor = 1.0
                else:
                    # Older equipment - less efficient
                    efficiency_factor = 1.2
                    
                # Base consumption by type
                consumption_ranges = {
                    "Base Station": (150, 300),
                    "Antenna": (50, 100),
                    "Router": (80, 150),
                    "Switch": (60, 120),
                    "Repeater": (40, 80),
                    "Power Supply": (20, 50),
                    "Cooling System": (200, 400)
                }
                
                base_consumption_range = consumption_ranges.get(equip_type, (50, 100))
                base_consumption = random.randint(*base_consumption_range)
                
                power_consumption = int(base_consumption * efficiency_factor * random.uniform(0.9, 1.1))
                
                # Store equipment data for the node
                node_equipment[node_id].append({
                    "equipment_id": equipment_id,
                    "type": equip_type,
                    "age": equipment_age,
                    "manufacturer": manufacturer,
                    "status": status,
                    "failure_rate": adjusted_failure_rate
                })
                
                equipment_list.append({
                    "equipment_id": equipment_id,
                    "node_id": node_id,
                    "equipment_type": equip_type,
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
    
    return equipment_list, node_equipment

def generate_spectrum_licenses() -> List[Dict]:
    """Generate spectrum licenses data with realistic patterns."""
    licenses = []
    license_id = 1
    
    # Spectrum allocation patterns
    # Low frequency bands (sub-1GHz): Better coverage, widely used for 2G/3G/4G
    # Mid-range bands (1-6GHz): Balance of coverage and capacity, widely used for 4G
    # High bands (mmWave, >24GHz): Very high capacity, limited range, used for 5G
    
    # Technology to frequency band mapping
    tech_to_bands = {
        "2G": ["700 MHz", "850 MHz", "900 MHz"],
        "3G": ["850 MHz", "900 MHz", "1900 MHz", "2100 MHz"],
        "4G": ["700 MHz", "850 MHz", "1800 MHz", "1900 MHz", "2100 MHz", "2600 MHz"],
        "5G": ["700 MHz", "3500 MHz", "28 GHz", "39 GHz"]
    }
    
    # License acquisition patterns - most high bands are newer
    band_acquisition_patterns = {
        "700 MHz": (2008, 2012),  # Digital dividend auctions
        "850 MHz": (1995, 2005),  # Early cellular
        "900 MHz": (1995, 2005),  # Early cellular
        "1800 MHz": (2000, 2010), # 2G/4G
        "1900 MHz": (2000, 2010), # 3G
        "2100 MHz": (2005, 2010), # 3G
        "2300 MHz": (2010, 2015), # 4G
        "2600 MHz": (2010, 2015), # 4G
        "3500 MHz": (2018, 2022), # 5G mid-band
        "28 GHz": (2018, 2022),   # 5G mmWave
        "39 GHz": (2019, 2022)    # 5G mmWave
    }
    
    # Bandwidth patterns by band
    band_bandwidth_patterns = {
        "700 MHz": (5, 20),     # Typically ~10MHz
        "850 MHz": (5, 15),     # Typically ~10MHz
        "900 MHz": (5, 15),     # Typically ~10MHz
        "1800 MHz": (10, 30),   # Typically ~20MHz
        "1900 MHz": (10, 30),   # Typically ~20MHz
        "2100 MHz": (15, 40),   # Typically ~20-30MHz
        "2300 MHz": (20, 60),   # Typically ~40MHz
        "2600 MHz": (20, 80),   # Typically ~40-60MHz
        "3500 MHz": (50, 200),  # Typically ~100MHz for 5G
        "28 GHz": (200, 800),   # Large bandwidths for mmWave
        "39 GHz": (200, 800)    # Large bandwidths for mmWave
    }
    
    # Cost patterns by band ($ million per MHz)
    band_cost_patterns = {
        "700 MHz": (0.5, 2.0),    # Low frequency highly valuable
        "850 MHz": (0.4, 1.8),    # Low frequency valuable
        "900 MHz": (0.4, 1.8),    # Low frequency valuable
        "1800 MHz": (0.3, 1.2),   # Mid-band moderate value
        "1900 MHz": (0.3, 1.2),   # Mid-band moderate value
        "2100 MHz": (0.2, 1.0),   # Mid-band moderate value
        "2300 MHz": (0.1, 0.8),   # Higher frequency less valuable
        "2600 MHz": (0.1, 0.6),   # Higher frequency less valuable
        "3500 MHz": (0.05, 0.4),  # Higher frequency but valuable for 5G
        "28 GHz": (0.01, 0.1),    # mmWave much less valuable per MHz
        "39 GHz": (0.005, 0.05)   # mmWave least valuable per MHz
    }
    
    # License lifetime patterns
    license_lifetimes = {
        # Older licenses had shorter terms
        (1990, 2000): (10, 15),   # 10-15 years
        (2001, 2010): (15, 20),   # 15-20 years
        (2011, 2020): (15, 25),   # 15-25 years
        (2021, 2025): (20, 30)    # 20-30 years (newer licenses longer terms)
    }
    
    # Generate licenses for each frequency band
    for frequency_band in FREQUENCY_BANDS:
        # Multiple licenses possible for popular bands
        if frequency_band in ["700 MHz", "850 MHz", "1800 MHz", "2100 MHz", "3500 MHz"]:
            num_licenses = random.randint(1, 3)  # 1-3 licenses for popular bands
        else:
            num_licenses = 1  # 1 license for other bands
            
        for _ in range(num_licenses):
            # Determine geographic area - lower bands tend to be national
            if "MHz" in frequency_band and int(frequency_band.split()[0]) < 1000:
                # Lower bands (<1GHz) often national
                area_weights = {"National": 0.6, "Regional": 0.3, "Metropolitan": 0.1}
            elif "GHz" in frequency_band:
                # mmWave bands often metropolitan
                area_weights = {"National": 0.1, "Regional": 0.3, "Metropolitan": 0.6}
            else:
                # Mid-bands mixed
                area_weights = {"National": 0.3, "Regional": 0.4, "Metropolitan": 0.3}
                
            geographic_area = random.choices(
                list(area_weights.keys()),
                weights=list(area_weights.values())
            )[0]
            
            # Bandwidth based on band patterns
            bandwidth_range = band_bandwidth_patterns.get(frequency_band, (10, 50))
            bandwidth = round(random.uniform(*bandwidth_range), 2)
            
            # Acquisition date based on band patterns
            year_range = band_acquisition_patterns.get(frequency_band, (2000, 2020))
            acquisition_year = random.randint(*year_range)
            
            # Random month and day
            acquisition_month = random.randint(1, 12)
            acquisition_day = random.randint(1, 28)  # Avoiding month-end issues
            
            acquisition_date = datetime.date(acquisition_year, acquisition_month, acquisition_day)
            
            # License lifetime
            for year_range, lifetime_range in license_lifetimes.items():
                if year_range[0] <= acquisition_year <= year_range[1]:
                    lifetime_years = random.randint(*lifetime_range)
                    break
            else:
                lifetime_years = random.randint(15, 20)  # Default
                
            # Calculate expiration date
            expiration_date = datetime.date(
                acquisition_year + lifetime_years,
                acquisition_month,
                acquisition_day
            )
            
            # Cost depends on bandwidth and frequency band
            cost_per_mhz_range = band_cost_patterns.get(frequency_band, (0.1, 0.5))
            cost_per_mhz = random.uniform(*cost_per_mhz_range)
            
            # Adjust cost based on geographic area
            if geographic_area == "National":
                area_factor = 1.0
            elif geographic_area == "Regional":
                area_factor = 0.3
            else:  # Metropolitan
                area_factor = 0.1
                
            total_cost = round(bandwidth * cost_per_mhz * area_factor, 2)
            
            # Regulatory authority - depends on year and region
            if acquisition_year < 2000:
                # Older licenses, simpler options
                regulatory_options = ["FCC", "OFCOM", "ACMA", "CRTC"]
            else:
                # All options for newer licenses
                regulatory_options = REGULATORY_AUTHORITIES
                
            regulatory_authority = random.choice(regulatory_options)
            
            # License number
            license_number = f"LIC-{regulatory_authority}-{frequency_band.split()[0]}-{random.randint(1000, 9999)}"
            
            licenses.append({
                "license_id": license_id,
                "frequency_band": frequency_band,
                "bandwidth_mhz": bandwidth,
                "geographic_area": geographic_area,
                "acquisition_date": acquisition_date.isoformat(),
                "expiration_date": expiration_date.isoformat(),
                "cost_million_usd": total_cost,
                "regulatory_authority": regulatory_authority,
                "license_number": license_number
            })
            
            license_id += 1
    
    return licenses

def generate_outages(network_nodes: List[Dict], node_equipment: Dict) -> List[Dict]:
    """Generate network outages data with realistic patterns."""
    outages = []
    outage_id = 1
    
    # Weather events that create regional outages
    # Define a few major weather events that would affect multiple nodes
    major_events = [
        {
            "name": "Hurricane Florence",
            "date": datetime.date(2022, 9, 15),
            "duration_hours": random.uniform(36, 72),
            "affected_region": {"lat_range": (32, 38), "lon_range": (-81, -75)},
            "severity": "critical",
            "cause": "Natural Disaster"
        },
        {
            "name": "California Wildfires",
            "date": datetime.date(2022, 8, 1),
            "duration_hours": random.uniform(72, 120),
            "affected_region": {"lat_range": (34, 41), "lon_range": (-123, -119)},
            "severity": "major",
            "cause": "Natural Disaster"
        },
        {
            "name": "Midwest Derecho",
            "date": datetime.date(2022, 6, 10),
            "duration_hours": random.uniform(24, 48),
            "affected_region": {"lat_range": (40, 45), "lon_range": (-95, -85)},
            "severity": "major",
            "cause": "Natural Disaster"
        },
        {
            "name": "Northeast Ice Storm",
            "date": datetime.date(2023, 1, 15),
            "duration_hours": random.uniform(48, 96),
            "affected_region": {"lat_range": (40, 45), "lon_range": (-80, -70)},
            "severity": "major",
            "cause": "Natural Disaster"
        },
        {
            "name": "Major Software Update Failure",
            "date": datetime.date(2022, 11, 8),
            "duration_hours": random.uniform(6, 24),
            "affected_region": None,  # Not geographically bound
            "severity": "major",
            "cause": "Software Bug"
        }
    ]
    
    # Track outages by node to avoid duplicates during same time period
    node_outage_periods = {}
    
    # Process major events first
    for event in major_events:
        event_start = datetime.datetime.combine(event["date"], datetime.time())
        event_end = event_start + datetime.timedelta(hours=event["duration_hours"])
        
        for node in network_nodes:
            node_id = node["node_id"]
            
            # Initialize tracking for this node
            if node_id not in node_outage_periods:
                node_outage_periods[node_id] = []
            
            # Check if this node is affected by the event
            is_affected = False
            
            if event["affected_region"]:
                # Geographic event
                lat, lon = node["latitude"], node["longitude"]
                lat_range = event["affected_region"]["lat_range"]
                lon_range = event["affected_region"]["lon_range"]
                
                if lat_range[0] <= lat <= lat_range[1] and lon_range[0] <= lon <= lon_range[1]:
                    # Node in affected region - high chance of outage
                    is_affected = random.random() < 0.8
            else:
                # Non-geographic event (e.g., software)
                # Affects random set of nodes
                is_affected = random.random() < 0.2
            
            if is_affected:
                # Check for overlap with existing outages
                has_overlap = False
                for period in node_outage_periods[node_id]:
                    if not (event_end <= period["start"] or event_start >= period["end"]):
                        has_overlap = True
                        break
                
                if not has_overlap:
                    # Create the outage
                    # Vary start and end slightly for each node
                    start_variation = random.uniform(-2, 2)  # Hours
                    duration_variation = random.uniform(0.8, 1.2)  # Multiplier
                    
                    start_time = event_start + datetime.timedelta(hours=start_variation)
                    duration_hours = event["duration_hours"] * duration_variation
                    end_time = start_time + datetime.timedelta(hours=duration_hours)
                    
                    # Calculate affected customers based on node coverage
                    if event["severity"] == "critical":
                        affected_customers = random.randint(5000, 50000)
                    elif event["severity"] == "major":
                        affected_customers = random.randint(1000, 20000)
                    else:
                        affected_customers = random.randint(100, 5000)
                    
                    # Resolution details
                    if event["cause"] == "Natural Disaster":
                        if "Hurricane" in event["name"]:
                            resolution = random.choice([
                                "Restored service after hurricane damage repairs. Deployed emergency generators to critical sites.",
                                "Repaired multiple damaged cell sites. Implemented temporary microwave backhaul.",
                                "Power restored to affected areas. Replaced damaged equipment at multiple sites."
                            ])
                        elif "Wildfire" in event["name"]:
                            resolution = random.choice([
                                "Restored service after wildfire damage assessment and fiber repairs.",
                                "Deployed COWs (Cell on Wheels) to replace damaged infrastructure. Reconnected backhaul.",
                                "Installed emergency power systems and repaired damaged sites after fire containment."
                            ])
                        elif "Ice Storm" in event["name"]:
                            resolution = random.choice([
                                "Cleared ice from equipment and restored power connections.",
                                "Repaired damaged antennas and transmission lines affected by ice accumulation.",
                                "Deployed emergency crews to restore service after power was re-established."
                            ])
                        else:
                            resolution = "Restored service after natural disaster damage assessment and repairs."
                    elif event["cause"] == "Software Bug":
                        resolution = random.choice([
                            "Reverted to previous software version. Implemented patched update after testing.",
                            "Identified and fixed configuration issue in core network elements.",
                            "Applied emergency patch to address critical bug in network management system."
                        ])
                    else:
                        resolution = "Issue resolved after technical intervention and repairs."
                    
                    outages.append({
                        "outage_id": outage_id,
                        "node_id": node_id,
                        "start_time": start_time.isoformat(),
                        "end_time": end_time.isoformat(),
                        "affected_customers": affected_customers,
                        "severity": event["severity"],
                        "cause": event["cause"],
                        "resolution": resolution
                    })
                    
                    # Track this outage period
                    node_outage_periods[node_id].append({
                        "start": start_time,
                        "end": end_time
                    })
                    
                    outage_id += 1
    
    # Now generate individual outages for nodes based on equipment reliability
    for node in network_nodes:
        node_id = node["node_id"]
        
        # Skip nodes that don't have equipment data
        if node_id not in node_equipment:
            continue
            
        # Initialize tracking if needed
        if node_id not in node_outage_periods:
            node_outage_periods[node_id] = []
            
        # Equipment-based outages
        node_equipment_list = node_equipment[node_id]
        
        # Each node can get up to 3 additional individual outages
        max_additional = 3
        additional_count = 0
        
        # More attempts for nodes with problematic equipment
        attempts = 0
        max_attempts = 10
        
        while additional_count < max_additional and attempts < max_attempts:
            attempts += 1
            
            # Randomly select equipment failure or other cause
            if node_equipment_list and random.random() < 0.7:  # 70% equipment-related
                # Equipment failure
                equipment = random.choice(node_equipment_list)
                equipment_type = equipment["type"]
                equipment_age = equipment["age"]
                equipment_status = equipment["status"]
                failure_rate = equipment["failure_rate"]
                
                # Only generate outage if equipment has reasonable failure probability
                # and is not already offline or decommissioned
                if equipment_status not in ["offline", "decommissioned"] and random.random() < failure_rate * 2:
                    # Equipment failed - generate outage
                    # More recent outages for equipment in worse condition
                    if equipment_status == "maintenance":
                        max_days_ago = 90  # Within last 3 months
                    elif equipment_age > 7:
                        max_days_ago = 180  # Within last 6 months
                    else:
                        max_days_ago = 365  # Within last year
                        
                    # Generate random start time
                    days_ago = random.randint(1, max_days_ago)
                    start_time = datetime.datetime.now() - datetime.timedelta(days=days_ago)
                    
                    # Outage severity based on equipment type and failure rate
                    if equipment_type in ["Base Station", "Power Supply"] or failure_rate > 0.2:
                        severity = random.choices(
                            ["critical", "major", "minor"],
                            weights=[0.3, 0.5, 0.2]
                        )[0]
                    else:
                        severity = random.choices(
                            ["critical", "major", "minor"],
                            weights=[0.1, 0.3, 0.6]
                        )[0]
                    
                    # Duration based on severity and equipment type
                    if severity == "critical":
                        base_duration = random.uniform(8.0, 48.0)
                    elif severity == "major":
                        base_duration = random.uniform(4.0, 24.0)
                    else:
                        base_duration = random.uniform(1.0, 8.0)
                        
                    # Critical equipment takes longer to fix
                    if equipment_type in ["Base Station", "Power Supply", "Cooling System"]:
                        duration_factor = 1.5
                    else:
                        duration_factor = 1.0
                        
                    duration_hours = base_duration * duration_factor
                    end_time = start_time + datetime.timedelta(hours=duration_hours)
                    
                    # Check for overlap with existing outages
                    has_overlap = False
                    for period in node_outage_periods[node_id]:
                        if not (end_time <= period["start"] or start_time >= period["end"]):
                            has_overlap = True
                            break
                    
                    if not has_overlap:
                        # Affected customers based on severity
                        if severity == "critical":
                            affected_customers = random.randint(1000, 10000)
                        elif severity == "major":
                            affected_customers = random.randint(500, 2000)
                        else:
                            affected_customers = random.randint(50, 500)
                        
                        # Cause based on equipment type
                        if equipment_type == "Power Supply":
                            cause = "Power Outage"
                        elif equipment_type in ["Router", "Switch"]:
                            cause = random.choice(["Hardware Failure", "Software Bug", "Configuration Error"])
                        elif equipment_type == "Cooling System":
                            cause = random.choice(["Hardware Failure", "Power Outage"])
                        else:
                            cause = "Hardware Failure"
                        
                        # Resolution text
                        if cause == "Hardware Failure":
                            resolution = f"Replaced faulty {equipment_type.lower()}. Restored service after testing."
                        elif cause == "Software Bug":
                            resolution = f"Updated firmware on {equipment_type.lower()} from {random.randint(1, 9)}.{random.randint(0, 9)} to latest version. Verified proper operation."
                        elif cause == "Power Outage":
                            resolution = "Restored main power supply and verified backup systems function correctly."
                        elif cause == "Configuration Error":
                            resolution = f"Corrected configuration settings on {equipment_type.lower()} and implemented validation checks to prevent recurrence."
                        else:
                            resolution = f"Technical team resolved the issue with the {equipment_type.lower()}."
                        
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
                        
                        # Track this outage period
                        node_outage_periods[node_id].append({
                            "start": start_time,
                            "end": end_time
                        })
                        
                        outage_id += 1
                        additional_count += 1
            else:
                # Non-equipment related outage (fiber cut, capacity, etc.)
                # Random time in past year
                start_time = datetime.datetime.now() - datetime.timedelta(days=random.randint(1, 365))
                
                # Random cause that's not hardware failure
                cause_options = [c for c in OUTAGE_CAUSES if c != "Hardware Failure"]
                cause = random.choice(cause_options)
                
                # Severity based on cause
                if cause in ["Fiber Cut", "Power Outage", "Natural Disaster", "Cyber Attack"]:
                    severity_weights = {"critical": 0.3, "major": 0.5, "minor": 0.2}
                elif cause in ["Capacity Overload", "Third-party Service Disruption"]:
                    severity_weights = {"critical": 0.1, "major": 0.4, "minor": 0.5}
                else:  # Scheduled Maintenance, Configuration Error, etc.
                    severity_weights = {"critical": 0.05, "major": 0.25, "minor": 0.7}
                    
                severity = random.choices(
                    list(severity_weights.keys()),
                    weights=list(severity_weights.values())
                )[0]
                
                # Duration based on severity and cause
                if severity == "critical":
                    base_duration = random.uniform(12.0, 48.0)
                elif severity == "major":
                    base_duration = random.uniform(6.0, 24.0)
                else:
                    base_duration = random.uniform(1.0, 8.0)
                    
                # Adjust duration based on cause
                if cause == "Scheduled Maintenance":
                    duration_factor = 0.8  # Planned, so shorter
                elif cause in ["Fiber Cut", "Natural Disaster"]:
                    duration_factor = 1.5  # Physical damage takes longer
                else:
                    duration_factor = 1.0
                    
                duration_hours = base_duration * duration_factor
                end_time = start_time + datetime.timedelta(hours=duration_hours)
                
                # Check for overlap with existing outages
                has_overlap = False
                for period in node_outage_periods[node_id]:
                    if not (end_time <= period["start"] or start_time >= period["end"]):
                        has_overlap = True
                        break
                
                if not has_overlap:
                    # Affected customers based on severity
                    if severity == "critical":
                        affected_customers = random.randint(1000, 10000)
                    elif severity == "major":
                        affected_customers = random.randint(500, 2000)
                    else:
                        affected_customers = random.randint(50, 500)
                    
                    # Resolution text based on cause
                    if cause == "Fiber Cut":
                        resolution = "Repaired damaged fiber optic cable. Implemented redundant routing to improve resilience."
                    elif cause == "Power Outage":
                        resolution = "Service restored after power company addressed the regional outage. Backup power systems maintained critical functions."
                    elif cause == "Scheduled Maintenance":
                        resolution = "Completed planned system upgrades and verified normal operation after maintenance window."
                    elif cause == "Capacity Overload":
                        resolution = "Added additional capacity and optimized traffic management to address congestion issues."
                    elif cause == "Configuration Error":
                        resolution = "Corrected configuration settings and implemented verification procedures to prevent future occurrences."
                    elif cause == "Cyber Attack":
                        resolution = "Mitigated security threat, patched vulnerabilities, and conducted comprehensive security review."
                    elif cause == "Natural Disaster":
                        resolution = "Repaired damaged infrastructure after weather event and restored normal operations."
                    else:
                        resolution = "Technical team resolved the service disruption and implemented preventive measures."
                    
                    outages.append({
                        "outage_id": outage_id,
                        "node_id": node_id,
                        "start_time": start_time.isoformat(),
                        "end_time": end_time.isoformat(),
                        "affected_customers": affected_customers,
                        "severity": severity,
                        "cause": cause,
                        "resolution": resolution
                    })
                    
                    # Track this outage period
                    node_outage_periods[node_id].append({
                        "start": start_time,
                        "end": end_time
                    })
                    
                    outage_id += 1
                    additional_count += 1
    
    return outages