"""
MongoDB Data Generators - Enhanced for Realistic Patterns

This module contains functions to generate data for MongoDB collections in the telco schema
with realistic patterns that enable meaningful insights and trend analysis.
"""

import random
import uuid
import hashlib
import datetime
import math
from faker import Faker
from typing import Dict, List, Any

# Initialize Faker
fake = Faker()

# Constants
ID_TYPES = ["Passport", "Driver's License", "National ID", "Residence Permit"]
NETWORK_TYPES = ["4G", "5G", "Auto"]

# Popular apps with realistic market share and demographic appeal
POPULAR_APPS = {
    "social": {
        "Facebook": {"share": 0.25, "age_appeal": {"18-24": 0.5, "25-34": 0.7, "35-44": 0.8, "45-64": 0.7, "65+": 0.5}},
        "Instagram": {"share": 0.3, "age_appeal": {"18-24": 0.9, "25-34": 0.8, "35-44": 0.6, "45-64": 0.4, "65+": 0.2}},
        "TikTok": {"share": 0.15, "age_appeal": {"18-24": 0.9, "25-34": 0.6, "35-44": 0.3, "45-64": 0.1, "65+": 0.05}},
        "Twitter": {"share": 0.1, "age_appeal": {"18-24": 0.7, "25-34": 0.7, "35-44": 0.6, "45-64": 0.5, "65+": 0.3}},
        "LinkedIn": {"share": 0.05, "age_appeal": {"18-24": 0.4, "25-34": 0.8, "35-44": 0.7, "45-64": 0.6, "65+": 0.3}},
        "Snapchat": {"share": 0.1, "age_appeal": {"18-24": 0.8, "25-34": 0.5, "35-44": 0.2, "45-64": 0.1, "65+": 0.05}},
        "Pinterest": {"share": 0.05, "age_appeal": {"18-24": 0.4, "25-34": 0.6, "35-44": 0.6, "45-64": 0.5, "65+": 0.3}}
    },
    "entertainment": {
        "YouTube": {"share": 0.3, "age_appeal": {"18-24": 0.9, "25-34": 0.9, "35-44": 0.8, "45-64": 0.7, "65+": 0.5}},
        "Netflix": {"share": 0.25, "age_appeal": {"18-24": 0.8, "25-34": 0.8, "35-44": 0.8, "45-64": 0.7, "65+": 0.4}},
        "Spotify": {"share": 0.15, "age_appeal": {"18-24": 0.9, "25-34": 0.8, "35-44": 0.6, "45-64": 0.4, "65+": 0.2}},
        "Disney+": {"share": 0.1, "age_appeal": {"18-24": 0.6, "25-34": 0.7, "35-44": 0.8, "45-64": 0.6, "65+": 0.3}},
        "Amazon Prime": {"share": 0.1, "age_appeal": {"18-24": 0.6, "25-34": 0.7, "35-44": 0.8, "45-64": 0.7, "65+": 0.4}},
        "HBO Max": {"share": 0.05, "age_appeal": {"18-24": 0.6, "25-34": 0.7, "35-44": 0.7, "45-64": 0.6, "65+": 0.3}},
        "Twitch": {"share": 0.05, "age_appeal": {"18-24": 0.8, "25-34": 0.5, "35-44": 0.2, "45-64": 0.1, "65+": 0.05}}
    },
    "messaging": {
        "WhatsApp": {"share": 0.35, "age_appeal": {"18-24": 0.8, "25-34": 0.8, "35-44": 0.7, "45-64": 0.6, "65+": 0.4}},
        "Messenger": {"share": 0.25, "age_appeal": {"18-24": 0.7, "25-34": 0.7, "35-44": 0.7, "45-64": 0.6, "65+": 0.4}},
        "Telegram": {"share": 0.15, "age_appeal": {"18-24": 0.7, "25-34": 0.6, "35-44": 0.5, "45-64": 0.3, "65+": 0.1}},
        "Signal": {"share": 0.05, "age_appeal": {"18-24": 0.5, "25-34": 0.6, "35-44": 0.5, "45-64": 0.3, "65+": 0.1}},
        "Discord": {"share": 0.1, "age_appeal": {"18-24": 0.8, "25-34": 0.5, "35-44": 0.3, "45-64": 0.1, "65+": 0.05}},
        "Zoom": {"share": 0.05, "age_appeal": {"18-24": 0.7, "25-34": 0.8, "35-44": 0.8, "45-64": 0.7, "65+": 0.5}},
        "Teams": {"share": 0.05, "age_appeal": {"18-24": 0.6, "25-34": 0.8, "35-44": 0.8, "45-64": 0.7, "65+": 0.4}}
    }
}

# Communication preferences by customer segment
SEGMENT_CONTACT_PREFS = {
    "Premium": {"email": 0.6, "phone": 0.3, "SMS": 0.1},
    "Standard": {"email": 0.4, "phone": 0.3, "SMS": 0.3},
    "Budget": {"email": 0.3, "phone": 0.2, "SMS": 0.5},
    "Business": {"email": 0.7, "phone": 0.25, "SMS": 0.05},
    "Family": {"email": 0.5, "phone": 0.3, "SMS": 0.2}
}

# Marketing opt-in rates by segment
SEGMENT_MARKETING_PREFS = {
    "Premium": 0.6,    # 60% opt-in
    "Standard": 0.5,   # 50% opt-in
    "Budget": 0.4,     # 40% opt-in
    "Business": 0.3,   # 30% opt-in
    "Family": 0.7      # 70% opt-in
}

# Social media usage by age group (probability of having an account)
AGE_SOCIAL_MEDIA_USAGE = {
    "18-24": {"facebook": 0.7, "twitter": 0.8, "instagram": 0.9, "linkedin": 0.6, "tiktok": 0.8},
    "25-34": {"facebook": 0.8, "twitter": 0.7, "instagram": 0.8, "linkedin": 0.8, "tiktok": 0.5},
    "35-44": {"facebook": 0.8, "twitter": 0.6, "instagram": 0.7, "linkedin": 0.7, "tiktok": 0.3},
    "45-54": {"facebook": 0.7, "twitter": 0.5, "instagram": 0.5, "linkedin": 0.6, "tiktok": 0.1},
    "55-64": {"facebook": 0.6, "twitter": 0.3, "instagram": 0.3, "linkedin": 0.5, "tiktok": 0.05},
    "65+": {"facebook": 0.5, "twitter": 0.2, "instagram": 0.2, "linkedin": 0.3, "tiktok": 0.02}
}

# Support ticket categories
SUPPORT_CATEGORIES = {
    "Network Issues": {
        "frequency": 0.3,
        "issues": [
            "Poor signal strength",
            "No network connection",
            "Slow data speeds",
            "Network outage in area",
            "Call drops",
            "Unable to make calls",
            "Unable to send texts",
            "No data connection",
            "WiFi calling not working",
            "Roaming issues"
        ],
        "resolution_time": {"min": 1, "max": 7},  # days
        "complexity": "medium"
    },
    "Billing Issues": {
        "frequency": 0.25,
        "issues": [
            "Bill higher than expected",
            "Unknown charges",
            "Disputed charges",
            "Payment not applied",
            "Automatic payment failure",
            "Proration questions",
            "Discount not applied",
            "Tax calculation error",
            "Missing statement",
            "Refund request"
        ],
        "resolution_time": {"min": 1, "max": 5},  # days
        "complexity": "medium"
    },
    "Account Issues": {
        "frequency": 0.15,
        "issues": [
            "Password reset",
            "Account access",
            "Profile update",
            "Security concerns",
            "Preferences update",
            "Login problems",
            "Two-factor authentication",
            "Notification settings",
            "Privacy settings",
            "Account closure request"
        ],
        "resolution_time": {"min": 0, "max": 3},  # days
        "complexity": "low"
    },
    "Device Issues": {
        "frequency": 0.2,
        "issues": [
            "Device activation",
            "SIM card issues",
            "Phone not working",
            "Software update problems",
            "Device replacement",
            "Battery problems",
            "Screen damage",
            "Water damage",
            "Warranty inquiry",
            "Device compatibility"
        ],
        "resolution_time": {"min": 1, "max": 10},  # days
        "complexity": "high"
    },
    "Plan Changes": {
        "frequency": 0.1,
        "issues": [
            "Plan upgrade request",
            "Plan downgrade request",
            "International add-on",
            "Data plan change",
            "Family plan setup",
            "Business plan inquiry",
            "Switch to prepaid",
            "Switch to postpaid",
            "Plan comparison",
            "Special promotion inquiry"
        ],
        "resolution_time": {"min": 0, "max": 2},  # days
        "complexity": "low"
    }
}

def get_age_bracket(age):
    """Determine age bracket for a given age."""
    if age < 25:
        return "18-24"
    elif age < 35:
        return "25-34"
    elif age < 45:
        return "35-44"
    elif age < 55:
        return "45-54"
    elif age < 65:
        return "55-64"
    else:
        return "65+"

def calculate_app_appeal(app_info, age_bracket):
    """Calculate how appealing an app is to a specific age bracket."""
    return app_info.get("age_appeal", {}).get(age_bracket, 0.5)

def select_apps_for_customer(age, segment):
    """Select realistic apps used by a customer based on age and segment."""
    age_bracket = get_age_bracket(age)
    selected_apps = []
    
    # Different segments have different app category preferences
    category_weights = {
        "Premium": {"social": 0.3, "entertainment": 0.4, "messaging": 0.3},
        "Standard": {"social": 0.35, "entertainment": 0.35, "messaging": 0.3},
        "Budget": {"social": 0.4, "entertainment": 0.3, "messaging": 0.3},
        "Business": {"social": 0.2, "entertainment": 0.2, "messaging": 0.6},
        "Family": {"social": 0.35, "entertainment": 0.45, "messaging": 0.2}
    }
    
    # Default weights if segment not in mapping
    weights = category_weights.get(segment, {"social": 0.33, "entertainment": 0.33, "messaging": 0.34})
    
    # Select category count - more for premium users
    if segment == "Premium" or segment == "Business":
        category_count = random.choices([2, 3], weights=[0.3, 0.7])[0]
    else:
        category_count = random.choices([1, 2, 3], weights=[0.2, 0.5, 0.3])[0]
    
    # Select categories
    categories = random.choices(
        list(weights.keys()),
        weights=list(weights.values()),
        k=category_count
    )
    categories = set(categories)  # Remove duplicates
    
    # For each selected category, choose apps
    for category in categories:
        # Number of apps from this category
        if segment == "Premium":
            # Premium users use more apps
            app_count = random.randint(2, 4)
        elif segment == "Budget":
            # Budget users tend to use fewer apps
            app_count = random.randint(1, 3)
        else:
            app_count = random.randint(1, 3)
            
        # Get apps from this category
        category_apps = POPULAR_APPS.get(category, {})
        
        if not category_apps:
            continue
            
        # Calculate app probabilities based on general popularity and age appeal
        app_probabilities = {}
        for app_name, app_info in category_apps.items():
            # Base probability from market share
            base_prob = app_info.get("share", 0.1)
            
            # Age factor
            age_appeal = calculate_app_appeal(app_info, age_bracket)
            
            # Final probability
            app_probabilities[app_name] = base_prob * age_appeal
            
        # Normalize probabilities
        total_prob = sum(app_probabilities.values())
        if total_prob > 0:
            normalized_probs = {app: prob/total_prob for app, prob in app_probabilities.items()}
            
            # Select apps based on normalized probabilities
            apps = random.choices(
                list(normalized_probs.keys()),
                weights=list(normalized_probs.values()),
                k=min(app_count, len(normalized_probs))
            )
            
            # Remove potential duplicates
            apps = list(set(apps))
            
            # Add to selected apps
            selected_apps.extend(apps)
    
    # Ensure reasonable number of apps (3-7)
    if len(selected_apps) < 3:
        # Add some random popular apps to reach minimum
        all_apps = []
        for category in POPULAR_APPS.values():
            all_apps.extend(list(category.keys()))
            
        additional_needed = 3 - len(selected_apps)
        available_apps = [app for app in all_apps if app not in selected_apps]
        
        if available_apps and additional_needed > 0:
            selected_apps.extend(random.sample(available_apps, min(additional_needed, len(available_apps))))
            
    elif len(selected_apps) > 7:
        # Trim to maximum
        selected_apps = random.sample(selected_apps, 7)
    
    return selected_apps

def generate_data_usage(apps, segment, months=12):
    """Generate realistic data usage patterns."""
    # Base monthly usage by segment (in GB)
    base_usage = {
        "Premium": {"min": 8, "max": 20, "yearly_growth": 1.5},
        "Standard": {"min": 5, "max": 15, "yearly_growth": 1.3},
        "Budget": {"min": 2, "max": 8, "yearly_growth": 1.2},
        "Business": {"min": 10, "max": 25, "yearly_growth": 1.4},
        "Family": {"min": 15, "max": 30, "yearly_growth": 1.3}
    }
    
    # Get range for this segment
    usage_range = base_usage.get(segment, {"min": 5, "max": 15, "yearly_growth": 1.3})
    
    # Calculate base monthly usage
    base_monthly = random.uniform(usage_range["min"], usage_range["max"])
    
    # Generate monthly pattern with seasonal variations
    # People tend to use more data in winter and during holidays
    monthly_factors = [
        1.0,  # January (winter)
        0.9,  # February
        0.95, # March
        1.0,  # April (spring break)
        1.05, # May
        1.1,  # June (summer begins)
        1.2,  # July (vacation)
        1.15, # August (vacation)
        1.0,  # September (back to school)
        0.95, # October
        1.05, # November (Thanksgiving)
        1.15  # December (holidays)
    ]
    
    # Generate monthly usage with seasonal patterns
    monthly_usage = []
    for i in range(months):
        month_index = i % 12
        
        # Base for this month with seasonal factor
        month_base = base_monthly * monthly_factors[month_index]
        
        # Add random variation (±20%)
        variation = random.uniform(0.8, 1.2)
        
        # Calculate usage for this month
        month_usage = round(month_base * variation, 2)
        monthly_usage.append(month_usage)
    
    # Calculate total data usage over the period
    total_data = sum(monthly_usage)
    
    # Current month is the last month in the sequence
    current_month_data = monthly_usage[-1]
    
    # Generate app usage distribution
    # Calculate how much data per app based on type
    app_usage = []
    
    # Categorize apps
    high_usage_apps = ['YouTube', 'Netflix', 'Disney+', 'HBO Max', 'Amazon Prime', 'Twitch']
    medium_usage_apps = ['TikTok', 'Instagram', 'Facebook', 'Zoom', 'Teams']
    low_usage_apps = ['WhatsApp', 'Messenger', 'Twitter', 'Telegram', 'Signal', 'LinkedIn', 'Pinterest']
    
    # Distribute current month usage among apps
    remaining_data = current_month_data
    
    for app in apps:
        # Determine usage category
        if app in high_usage_apps:
            # High usage apps get 40-60% of data
            pct = random.uniform(0.1, 0.3)
        elif app in medium_usage_apps:
            # Medium usage apps get 10-30% of data
            pct = random.uniform(0.05, 0.15)
        else:
            # Low usage apps get 5-15% of data
            pct = random.uniform(0.02, 0.08)
            
        # Adjust for number of apps to ensure realistic distribution
        pct = pct * (5 / max(len(apps), 1))
        
        # Calculate app data usage
        app_data = round(current_month_data * pct, 2)
        
        # Keep track of remaining data to ensure we don't exceed total
        remaining_data -= app_data
        
        # Add to app usage list
        app_usage.append({"name": app, "usage": f"{app_data}GB"})
    
    # If there's remaining data, distribute it among apps
    if remaining_data > 0 and app_usage:
        # Add remaining to the highest usage app
        app_usage.sort(key=lambda x: float(x["usage"].replace("GB", "")), reverse=True)
        highest_app = app_usage[0]
        current_usage = float(highest_app["usage"].replace("GB", ""))
        highest_app["usage"] = f"{round(current_usage + remaining_data, 2)}GB"
    
    return {
        "total": f"{round(total_data, 2)}GB",
        "currentMonth": f"{round(current_month_data, 2)}GB",
        "appUsage": app_usage
    }

def generate_call_stats(segment, age):
    """Generate realistic call statistics based on customer segment and age."""
    # Base monthly minutes by segment
    base_minutes = {
        "Premium": {"min": 300, "max": 800},
        "Standard": {"min": 200, "max": 500},
        "Budget": {"min": 100, "max": 300},
        "Business": {"min": 500, "max": 1200},
        "Family": {"min": 400, "max": 1000}
    }
    
    # Age factors - different age groups have different calling habits
    age_factors = {
        "18-24": 0.7,  # Younger people call less, text more
        "25-34": 0.9,
        "35-44": 1.0,
        "45-54": 1.2,
        "55-64": 1.3,
        "65+": 1.4     # Older people tend to make more calls
    }
    
    # Get range for this segment
    minutes_range = base_minutes.get(segment, {"min": 200, "max": 500})
    
    # Calculate base monthly minutes
    base_monthly = random.uniform(minutes_range["min"], minutes_range["max"])
    
    # Apply age factor
    age_bracket = get_age_bracket(age)
    age_factor = age_factors.get(age_bracket, 1.0)
    
    monthly_minutes = base_monthly * age_factor
    
    # Calculate total minutes (assume 10 months of history)
    total_minutes = int(monthly_minutes * 10)
    
    # International minutes as a percentage of total
    # Premium and Business customers make more international calls
    if segment in ["Premium", "Business"]:
        intl_pct = random.uniform(0.05, 0.3)  # 5-30%
    else:
        intl_pct = random.uniform(0.01, 0.1)  # 1-10%
        
    international_minutes = int(total_minutes * intl_pct)
    
    return {
        "totalMinutes": total_minutes,
        "internationalMinutes": international_minutes
    }

def generate_support_ticket(customer_id, issue_category=None, status=None, ticket_date=None):
    """Generate a realistic support ticket."""
    # Select a category if not provided
    if not issue_category:
        categories = list(SUPPORT_CATEGORIES.keys())
        weights = [info["frequency"] for info in SUPPORT_CATEGORIES.values()]
        issue_category = random.choices(categories, weights=weights)[0]
    
    # Get issues for this category
    category_info = SUPPORT_CATEGORIES[issue_category]
    issues = category_info["issues"]
    
    # Select a specific issue
    issue = random.choice(issues)
    
    # Generate a ticket date if not provided
    if not ticket_date:
        # More recent tickets are more likely
        days_ago = random.choices(
            [7, 30, 90, 180, 365],
            weights=[0.4, 0.3, 0.15, 0.1, 0.05]
        )[0]
        ticket_date = fake.date_time_between(start_date=f"-{days_ago}d", end_date="now").strftime("%Y-%m-%d")
    
    # Generate ticket ID
    ticket_id = f"TKT-{random.randint(10000, 99999)}"
    
    # Determine status if not provided
    if not status:
        # Status probabilities dependent on ticket age and complexity
        ticket_datetime = datetime.datetime.strptime(ticket_date, "%Y-%m-%d")
        days_since_creation = (datetime.datetime.now() - ticket_datetime).days
        
        if days_since_creation < 1:
            # Very recent ticket, likely new
            status_weights = {"New": 0.7, "Open": 0.2, "In Progress": 0.1}
        elif days_since_creation < 3:
            # Few days old
            status_weights = {"Open": 0.3, "In Progress": 0.5, "Resolved": 0.2}
        else:
            # Older tickets likely resolved
            resolution_time = category_info["resolution_time"]
            expected_resolution_days = random.randint(resolution_time["min"], resolution_time["max"])
            
            if days_since_creation < expected_resolution_days:
                # Still within expected resolution time
                status_weights = {"In Progress": 0.6, "Resolved": 0.3, "Escalated": 0.1}
            else:
                # Beyond expected resolution time
                status_weights = {"Resolved": 0.8, "Closed": 0.15, "Escalated": 0.05}
                
        status = random.choices(
            list(status_weights.keys()),
            weights=list(status_weights.values())
        )[0]
    
    # Generate description
    descriptions = {
        "Network Issues": [
            f"Customer reports {issue.lower()} at home address.",
            f"Customer experiencing {issue.lower()} in multiple locations.",
            f"Customer noticed {issue.lower()} since yesterday.",
            f"Consistent {issue.lower()} for the past week."
        ],
        "Billing Issues": [
            f"Customer has questions about {issue.lower()}.",
            f"Customer noticed {issue.lower()} on most recent statement.",
            f"Customer requesting assistance with {issue.lower()}.",
            f"Inquiry regarding {issue.lower()} on account."
        ],
        "Account Issues": [
            f"Customer needs help with {issue.lower()}.",
            f"Customer unable to complete {issue.lower()} online.",
            f"Assistance requested for {issue.lower()}.",
            f"Customer tried self-service for {issue.lower()} but encountered problems."
        ],
        "Device Issues": [
            f"Customer experiencing {issue.lower()} with their device.",
            f"New device has {issue.lower()}.",
            f"Customer requesting support for {issue.lower()}.",
            f"Technical help needed for {issue.lower()}."
        ],
        "Plan Changes": [
            f"Customer interested in {issue.lower()}.",
            f"Customer inquiring about {issue.lower()}.",
            f"Customer wants information on {issue.lower()}.",
            f"Customer comparing options for {issue.lower()}."
        ]
    }
    
    category_descriptions = descriptions.get(issue_category, ["Customer needs assistance."])
    description = random.choice(category_descriptions)
    
    # Generate resolution notes based on status
    if status in ["Resolved", "Closed"]:
        resolutions = {
            "Network Issues": [
                "Confirmed tower maintenance was affecting service. Issue now resolved.",
                "Troubleshooting steps resolved connectivity issues. Signal strength now normal.",
                f"Dispatched technician who identified and fixed {issue.lower()}.",
                "Reset network settings remotely. Customer confirmed issue is resolved."
            ],
            "Billing Issues": [
                f"Explained {issue.lower()} to customer. Adjusted bill as appropriate.",
                "Reviewed account history and billing details with customer. Issue clarified.",
                "Applied appropriate credits to account. Customer satisfied with resolution.",
                "Updated billing preferences as requested. Confirmed on next statement."
            ],
            "Account Issues": [
                f"Helped customer complete {issue.lower()}. Verified account is working properly.",
                "Reset customer credentials and verified access restored.",
                "Updated profile information as requested. Changes confirmed.",
                "Walked customer through security settings. Issue resolved."
            ],
            "Device Issues": [
                f"Troubleshooting steps resolved {issue.lower()}. Device now functioning normally.",
                "Processed device replacement. New device activated successfully.",
                "Software update resolved the issue. Customer confirmed functionality.",
                "Reset device settings and restored normal operation."
            ],
            "Plan Changes": [
                f"Processed {issue.lower()} as requested. Changes effective immediately.",
                "Updated plan details. Explained new features to customer.",
                "Compared options with customer. Made recommended changes to account.",
                "Changes completed and confirmed with customer. New billing cycle updated."
            ]
        }
        
        category_resolutions = resolutions.get(issue_category, ["Issue successfully resolved."])
        resolution_notes = random.choice(category_resolutions)
    elif status == "Escalated":
        resolution_notes = "Issue escalated to specialized support team for further assistance."
    elif status == "In Progress":
        resolution_notes = "Support agent working with customer to resolve the issue."
    elif status == "Open":
        resolution_notes = "Ticket assigned to support agent. Initial assessment in progress."
    else:  # New
        resolution_notes = "Ticket created. Awaiting assignment to support agent."
    
    # Create the ticket
    ticket = {
        "ticketId": ticket_id,
        "date": ticket_date,
        "issue": issue,
        "category": issue_category,
        "description": description,
        "status": status,
        "resolutionNotes": resolution_notes
    }
    
    return ticket

def generate_user_profiles(customers: List[Dict], customer_links: List[Dict]) -> List[Dict]:
    """Generate MongoDB user profiles with realistic patterns."""
    user_profiles = []
    
    for customer, link in zip(customers, customer_links):
        customer_id = customer["customer_id"]
        segment = customer.get("segment", "Standard")
        age = customer.get("age", 35)  # Default to 35 if age not available
        satisfaction = customer.get("satisfaction_score", 7)  # Default to 7 if not available
        
        # Generate identification with country-appropriate patterns
        country = customer.get("country", "United States")
        # Different countries have different ID preferences
        if country == "United States":
            id_weights = {"Driver's License": 0.7, "Passport": 0.2, "National ID": 0.05, "Residence Permit": 0.05}
        elif country == "United Kingdom":
            id_weights = {"Passport": 0.4, "Driver's License": 0.4, "National ID": 0.1, "Residence Permit": 0.1}
        elif country == "Canada":
            id_weights = {"Driver's License": 0.6, "Passport": 0.3, "National ID": 0.05, "Residence Permit": 0.05}
        else:
            id_weights = {"National ID": 0.4, "Passport": 0.3, "Driver's License": 0.2, "Residence Permit": 0.1}
            
        id_type = random.choices(
            list(id_weights.keys()),
            weights=list(id_weights.values())
        )[0]
        
        # ID number format based on type
        if id_type == "Passport":
            id_number = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=2)) + ''.join(random.choices('0123456789', k=7))
        elif id_type == "Driver's License":
            id_number = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=1)) + ''.join(random.choices('0123456789', k=12))
        else:
            id_number = ''.join(random.choices('0123456789ABCDEF', k=8))
            
        # ID expiry date - 1-10 years in future
        id_expiry = fake.date_time_between(start_date="+1y", end_date="+10y").strftime("%Y-%m-%d")
        
        # Generate account details
        account_number = f"ACC-{random.randint(100000, 999999)}"
        
        # Registration date - newer for newer customers, old for old customers
        if customer_id < len(customers) * 0.3:  # Oldest 30% of customers
            registration_date = fake.date_time_between(start_date="-5y", end_date="-3y").strftime("%Y-%m-%d")
        elif customer_id < len(customers) * 0.7:  # Middle 40% of customers
            registration_date = fake.date_time_between(start_date="-3y", end_date="-1y").strftime("%Y-%m-%d")
        else:  # Newest 30% of customers
            registration_date = fake.date_time_between(start_date="-1y", end_date="-1m").strftime("%Y-%m-%d")
        
        # Generate preferences with segment and age correlations
        # Email updates preference - business and premium users more likely to want emails
        if segment in ["Premium", "Business"]:
            email_updates = random.random() < 0.7  # 70% yes
        else:
            email_updates = random.random() < 0.5  # 50% yes
            
        # SMS notifications - younger users more likely to want these
        age_bracket = get_age_bracket(age)
        if age_bracket in ["18-24", "25-34"]:
            sms_notifications = random.random() < 0.7  # 70% yes
        elif age_bracket in ["35-44", "45-54"]:
            sms_notifications = random.random() < 0.5  # 50% yes
        else:
            sms_notifications = random.random() < 0.3  # 30% yes
            
        # App notifications - younger users more likely to use apps
        if age_bracket in ["18-24", "25-34"]:
            app_notifications_enabled = random.random() < 0.8  # 80% yes
            app_frequency_weights = {"Daily": 0.7, "Weekly": 0.2, "Monthly": 0.1}
        elif age_bracket in ["35-44", "45-54"]:
            app_notifications_enabled = random.random() < 0.6  # 60% yes
            app_frequency_weights = {"Daily": 0.5, "Weekly": 0.3, "Monthly": 0.2}
        else:
            app_notifications_enabled = random.random() < 0.4  # 40% yes
            app_frequency_weights = {"Daily": 0.3, "Weekly": 0.4, "Monthly": 0.3}
            
        app_frequency = random.choices(
            list(app_frequency_weights.keys()),
            weights=list(app_frequency_weights.values())
        )[0]
        
        # Generate favorite locations (1-3) based on customer's country and state
        num_locations = random.randint(1, 3)
        favorite_locations = []
        customer_state = customer.get("state", "")
        
        # First location is often home area
        home_location = {
            "name": customer.get("city", fake.city()),
            "coordinates": {
                "lat": float(fake.latitude()),
                "long": float(fake.longitude())
            }
        }
        favorite_locations.append(home_location)
        
        # Add additional locations
        for _ in range(num_locations - 1):
            location = {
                "name": fake.city(),
                "coordinates": {
                    "lat": float(fake.latitude()),
                    "long": float(fake.longitude())
                }
            }
            favorite_locations.append(location)
        
        # Network settings - Premium users more likely to prefer 5G
        if segment == "Premium":
            preferred_network_weights = {"5G": 0.7, "4G": 0.2, "Auto": 0.1}
        elif segment == "Budget":
            preferred_network_weights = {"4G": 0.6, "Auto": 0.3, "5G": 0.1}
        else:
            preferred_network_weights = {"Auto": 0.5, "4G": 0.3, "5G": 0.2}
            
        preferred_network = random.choices(
            list(preferred_network_weights.keys()),
            weights=list(preferred_network_weights.values())
        )[0]
        
        # Data saver - Budget users more likely to enable this
        if segment == "Budget":
            data_saver = random.random() < 0.7  # 70% yes
        elif segment == "Premium":
            data_saver = random.random() < 0.3  # 30% yes
        else:
            data_saver = random.random() < 0.5  # 50% yes
            
        # Privacy settings - younger users more privacy conscious
        if age_bracket in ["18-24", "25-34"]:
            share_data = random.random() < 0.3  # 30% yes
            ad_personalization = random.random() < 0.3  # 30% yes
        elif segment == "Premium":  # Premium users value privacy
            share_data = random.random() < 0.4  # 40% yes
            ad_personalization = random.random() < 0.4  # 40% yes
        else:
            share_data = random.random() < 0.5  # 50% yes
            ad_personalization = random.random() < 0.5  # 50% yes
            
        # App usage based on age and segment
        selected_apps = select_apps_for_customer(age, segment)
        
        # Generate usage data
        usage_data = generate_data_usage(selected_apps, segment)
        
        # Generate call stats
        call_stats = generate_call_stats(segment, age)
        
        # Support history - correlate with satisfaction
        # Lower satisfaction = more support tickets
        support_history = []
        
        # Special case for Alexis Smith (customer ID 7)
        if customer_id == 7:
            # Ensure Alexis has a ticket about activating her iPhone
            support_history.append({
                "ticketId": f"TKT-{random.randint(10000, 99999)}",
                "date": datetime.datetime.today().strftime("%Y-%m-%d"),
                "issue": "iPhone activation trouble",
                "category": "Device Issues",
                "description": "Alexis is unable to activate her iPhone. Escalated for urgent assistance.",
                "status": "New",
                "resolutionNotes": "Escalated to Tier 2 support for immediate attention."
            })
            
            # Add network issues ticket
            network_issue_ticket = generate_support_ticket(
                customer_id=7,
                issue_category="Network Issues",
                status="Resolved",
                ticket_date=fake.date_time_between(start_date="-6m", end_date="-4m").strftime("%Y-%m-%d")
            )
            support_history.append(network_issue_ticket)
            
            # Add billing inquiry ticket
            billing_inquiry_ticket = generate_support_ticket(
                customer_id=7,
                issue_category="Billing Issues",
                status="Resolved",
                ticket_date=fake.date_time_between(start_date="-8m", end_date="-7m").strftime("%Y-%m-%d")
            )
            support_history.append(billing_inquiry_ticket)
            
            # Add data usage ticket
            data_usage_ticket = generate_support_ticket(
                customer_id=7,
                issue_category="Billing Issues",
                status="Open",
                ticket_date=fake.date_time_between(start_date="-1m", end_date="now").strftime("%Y-%m-%d")
            )
            data_usage_ticket["issue"] = "Data usage"
            data_usage_ticket["description"] = "Customer inquired about high data usage"
            support_history.append(data_usage_ticket)
            
            # Add plan upgrade ticket
            plan_upgrade_ticket = generate_support_ticket(
                customer_id=7,
                issue_category="Plan Changes",
                status="Resolved",
                ticket_date=fake.date_time_between(start_date="-10m", end_date="-9m").strftime("%Y-%m-%d")
            )
            plan_upgrade_ticket["issue"] = "Plan upgrade"
            plan_upgrade_ticket["description"] = "Customer interested in upgrading to a premium plan"
            support_history.append(plan_upgrade_ticket)
        else:
            # Regular customers - ticket count based on satisfaction
            if satisfaction <= 3:  # Very dissatisfied
                ticket_count = random.randint(3, 6)
            elif satisfaction <= 6:  # Neutral
                ticket_count = random.randint(1, 3)
            else:  # Satisfied
                ticket_count = random.randint(0, 2)
                
            # Generate specific tickets
            for _ in range(ticket_count):
                ticket = generate_support_ticket(customer_id)
                support_history.append(ticket)
        
        # Notes - content varies based on customer characteristics
        # High-value or complex customers get more detailed notes
        if segment in ["Premium", "Business"] or satisfaction <= 4:
            notes_probability = 0.8  # 80% chance of notes
        else:
            notes_probability = 0.3  # 30% chance of notes
            
        if random.random() < notes_probability:
            # Special case for Alexis
            if customer_id == 7:
                notes = "Tech-savvy customer who prefers digital communication. Knowledgeable about devices and services. Interested in new technology offerings. Good candidate for beta testing programs."
            elif segment == "Premium":
                premium_notes = [
                    f"High-value customer since {registration_date[:4]}. Prefers premium service options.",
                    "Customer expects priority support. Has provided valuable feedback on services.",
                    "Consider for premium loyalty program. History of upgrading devices regularly.",
                    "Interested in exclusive promotions. Values quality over price."
                ]
                notes = random.choice(premium_notes)
            elif segment == "Business":
                business_notes = [
                    "Business account requiring specialized attention. Multiple lines under management.",
                    "Decision maker for company telecom services. Relationship management important.",
                    "Price sensitive but values reliability. Requires detailed billing.",
                    "Interested in consolidated reporting. Consider for business loyalty program."
                ]
                notes = random.choice(business_notes)
            elif satisfaction <= 4:
                low_satisfaction_notes = [
                    "Customer has expressed dissatisfaction with service quality. Requires follow-up.",
                    "History of service issues. Consider proactive outreach to improve satisfaction.",
                    "Price sensitive and has mentioned competitor offers. Retention risk.",
                    "Experienced multiple technical issues. Needs special attention to improve experience."
                ]
                notes = random.choice(low_satisfaction_notes)
            else:
                general_notes = [
                    "Regular account in good standing.",
                    "Customer prefers self-service options when available.",
                    "Responsive to promotional offers.",
                    "Generally satisfied with service quality."
                ]
                notes = random.choice(general_notes)
        else:
            notes = ""
        
        # Create the profile
        profile = {
            "_id": hashlib.md5(str(customer_id).encode()).hexdigest(),
            "customer_id": customer_id,
            "identification": {
                "type": id_type,
                "number": id_number,
                "issuedBy": customer["country"],
                "expiryDate": id_expiry
            },
            "accountDetails": {
                "accountNumber": account_number,
                "registrationDate": registration_date
            },
            "preferences": {
                "communication": {
                    "emailUpdates": email_updates,
                    "smsNotifications": sms_notifications,
                    "appNotifications": {
                        "enabled": app_notifications_enabled,
                        "frequency": app_frequency
                    }
                },
                "servicePreferences": {
                    "favoriteLocations": favorite_locations,
                    "networkSettings": {
                        "preferredNetworkType": preferred_network,
                        "dataSaverMode": data_saver
                    }
                },
                "privacySettings": {
                    "shareDataForImprovements": share_data,
                    "adPersonalization": ad_personalization
                }
            },
            "usageStats": {
                "dataUsage": {
                    "total": usage_data["total"],
                    "currentMonth": usage_data["currentMonth"]
                },
                "callStats": {
                    "totalMinutes": call_stats["totalMinutes"],
                    "internationalMinutes": call_stats["internationalMinutes"]
                },
                "appUsage": usage_data["appUsage"]
            },
            "supportHistory": support_history,
            "notes": notes,
            "memberID": str(uuid.uuid4())
        }
        
        user_profiles.append(profile)
    
    return user_profiles

def generate_customer_preferences(customers: List[Dict], customer_links: List[Dict]) -> List[Dict]:
    """Generate MongoDB customer preferences with realistic patterns."""
    customer_preferences = []
    
    # Create customer lookup for efficient access
    customer_lookup = {c["customer_id"]: c for c in customers}
    
    for link in customer_links:
        customer_id = link["customer_id"]  # Get the customer ID from the link
        customer_guid = link["customer_guid"]
        
        # Get customer details from lookup
        customer = customer_lookup.get(customer_id, {})
        segment = customer.get("segment", "Standard")
        age = customer.get("age", 35)  # Default to 35 if not available
        
        # Get age bracket for further correlations
        age_bracket = get_age_bracket(age)
        
        # Special case for Alexis Smith (customer ID 7)
        if customer_id == 7:
            # Tech-savvy preferences for Alexis
            contact_method = "email"  # Tech-savvy users often prefer email
            marketing_opt_in = True  # Interested in new tech offerings
            
            # Social media presence for a tech-savvy user
            social_media = {
                "facebook": f"https://facebook.com/alexis.smith.tech",
                "twitter": f"https://twitter.com/alexis_tech",
                "linkedin": f"https://linkedin.com/in/alexis-smith-tech",
                "instagram": f"https://instagram.com/alexis.tech.life"
            }
            
            # Behavioral data showing active engagement
            last_website = fake.date_time_between(start_date="-1w", end_date="now").isoformat()
            last_app_login = fake.date_time_between(start_date="-2d", end_date="now").isoformat()
            
            # Customer notes reflecting tech-savvy nature
            customer_notes = [
                {
                    "author": "Sarah Johnson",
                    "date": fake.date_time_between(start_date="-6m", end_date="-5m").isoformat(),
                    "content": "Customer is very knowledgeable about our services and devices. Provided valuable feedback on our mobile app."
                },
                {
                    "author": "Michael Chen",
                    "date": fake.date_time_between(start_date="-3m", end_date="-2m").isoformat(),
                    "content": "Ms. Smith requested information about our upcoming 5G rollout. She's interested in being among the first to upgrade."
                },
                {
                    "author": "Jessica Williams",
                    "date": fake.date_time_between(start_date="-1m", end_date="now").isoformat(),
                    "content": "Customer reported a minor bug in our billing portal. IT team confirmed the issue and it has been added to the next sprint for fixing."
                }
            ]
        else:
            # Contact method based on segment preferences
            segment_contact_weights = SEGMENT_CONTACT_PREFS.get(segment, {"email": 0.4, "phone": 0.3, "SMS": 0.3})
            contact_method = random.choices(
                list(segment_contact_weights.keys()),
                weights=list(segment_contact_weights.values())
            )[0]
            
            # Marketing opt-in based on segment
            opt_in_rate = SEGMENT_MARKETING_PREFS.get(segment, 0.5)
            marketing_opt_in = random.random() < opt_in_rate
            
            # Social media presence based on age
            social_media = {}
            
            # Get social media probabilities for this age bracket
            sm_probs = AGE_SOCIAL_MEDIA_USAGE.get(age_bracket, {
                "facebook": 0.5, 
                "twitter": 0.3, 
                "instagram": 0.4, 
                "linkedin": 0.3, 
                "tiktok": 0.2
            })
            
            # Based on probabilities, determine which platforms this customer uses
            if random.random() < sm_probs.get("facebook", 0.5):
                username = fake.user_name().lower()
                social_media["facebook"] = f"https://facebook.com/{username}"
                
            if random.random() < sm_probs.get("twitter", 0.3):
                username = fake.user_name().lower()
                social_media["twitter"] = f"https://twitter.com/{username}"
                
            if random.random() < sm_probs.get("instagram", 0.4):
                username = fake.user_name().lower().replace(".", "_")
                social_media["instagram"] = f"https://instagram.com/{username}"
                
            if random.random() < sm_probs.get("linkedin", 0.3):
                name_parts = [p.lower() for p in fake.name().split()]
                if len(name_parts) >= 2:
                    linkedin_username = f"{name_parts[0]}-{name_parts[-1]}"
                    social_media["linkedin"] = f"https://linkedin.com/in/{linkedin_username}"
                    
            if random.random() < sm_probs.get("tiktok", 0.2):
                username = fake.user_name().lower()
                social_media["tiktok"] = f"https://tiktok.com/@{username}"
            
            # Behavioral data - more active for higher satisfaction
            satisfaction = customer.get("satisfaction_score", 7)
            
            # More satisfied customers engage more frequently
            if satisfaction >= 8:  # Very satisfied
                website_days_ago = random.randint(1, 14)  # 1-14 days
                app_days_ago = random.randint(1, 7)       # 1-7 days
            elif satisfaction >= 5:  # Moderately satisfied
                website_days_ago = random.randint(7, 30)  # 7-30 days
                app_days_ago = random.randint(3, 14)      # 3-14 days
            else:  # Dissatisfied
                website_days_ago = random.randint(14, 60) # 14-60 days
                app_days_ago = random.randint(7, 30)      # 7-30 days
                
            # Premium customers check more frequently
            if segment == "Premium":
                website_days_ago = max(1, int(website_days_ago * 0.7))
                app_days_ago = max(1, int(app_days_ago * 0.7))
                
            last_website = fake.date_time_between(start_date=f"-{website_days_ago}d", end_date="now").isoformat()
            last_app_login = fake.date_time_between(start_date=f"-{app_days_ago}d", end_date="now").isoformat()
            
            # Notes vary by customer characteristics
            # Number of notes correlates with customer value and issues
            if segment in ["Premium", "Business"] or satisfaction <= 4:
                notes_count = random.randint(1, 3)  # 1-3 notes
            else:
                notes_count = random.randint(0, 1)  # 0-1 notes
                
            customer_notes = []
            for _ in range(notes_count):
                # Author from a pool of agents
                authors = [
                    "Sarah Johnson", "Michael Chen", "Jessica Williams", 
                    "David Rodriguez", "Emily Thompson", "James Wilson",
                    "Maria Garcia", "Robert Smith", "Lisa Brown"
                ]
                author = random.choice(authors)
                
                # Note date
                note_date = fake.date_time_between(start_date="-1y", end_date="now").isoformat()
                
                # Content based on segment and satisfaction
                if segment == "Premium":
                    content_options = [
                        "Premium customer with high expectations. Provides valuable feedback on services.",
                        "Customer appreciates personal attention. Responsive to exclusive promotions.",
                        "Interested in latest device offerings. Consider for early upgrade offers.",
                        "Values quality and service over price. Good candidate for premium services."
                    ]
                elif segment == "Business":
                    content_options = [
                        "Business account requiring specialized attention. Decision maker for company services.",
                        "Prefers detailed reporting and predictable billing. Cost-conscious but values reliability.",
                        "Multiple lines under management. Appreciates efficiency in service interactions.",
                        "Interested in business-specific features and enterprise solutions."
                    ]
                elif satisfaction <= 4:
                    content_options = [
                        "Customer has experienced service issues. Requires proactive follow-up.",
                        "Price sensitive and has mentioned competitor offers. Retention risk.",
                        "Has expressed dissatisfaction with recent bill. Detailed explanation provided.",
                        "Multiple interactions required to resolve recent issue. Extra attention needed."
                    ]
                else:
                    content_options = [
                        "Regular account in good standing. No significant issues noted.",
                        "Customer prefers self-service options when available.",
                        "Responsive to promotional offers that match usage patterns.",
                        "Generally satisfied with current services and pricing."
                    ]
                    
                content = random.choice(content_options)
                
                customer_notes.append({
                    "author": author,
                    "date": note_date,
                    "content": content
                })
        
        preferences = {
            "customer_guid": customer_guid,
            "preferences": {
                "contactMethod": contact_method,
                "marketingOptIn": marketing_opt_in
            },
            "socialMedia": social_media,
            "behavioralData": {
                "lastWebsiteVisit": last_website,
                "lastAppLogin": last_app_login
            },
            "customerNotes": customer_notes
        }
        
        customer_preferences.append(preferences)
    
    return customer_preferences