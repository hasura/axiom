"""
MongoDB Data Generators

This module contains functions to generate data for MongoDB collections in the telco schema.
"""

import random
import uuid
import hashlib
import datetime
from faker import Faker
from typing import Dict, List, Any

# Initialize Faker
fake = Faker()

# Constants
ID_TYPES = ["Passport", "Driver's License", "National ID", "Residence Permit"]
NETWORK_TYPES = ["4G", "5G"]
POPULAR_APPS = ["Facebook", "Instagram", "TikTok", "YouTube", "Netflix", "Spotify", "WhatsApp", "Zoom", "Teams"]

def generate_user_profiles(customers: List[Dict], customer_links: List[Dict]) -> List[Dict]:
    """Generate MongoDB user profiles."""
    user_profiles = []
    
    for customer, link in zip(customers, customer_links):
        customer_id = customer["customer_id"]
        
        # Generate identification
        id_type = random.choice(ID_TYPES)
        id_number = ''.join(random.choices('0123456789ABCDEF', k=8))
        id_expiry = fake.date_time_between(start_date="+1y", end_date="+10y").strftime("%Y-%m-%d")
        
        # Generate account details
        account_number = f"ACC-{random.randint(100000, 999999)}"
        registration_date = fake.date_time_between(start_date="-5y", end_date="-1y").strftime("%Y-%m-%d")
        
        # Generate preferences
        email_updates = random.choice([True, False])
        sms_notifications = random.choice([True, False])
        app_notifications_enabled = random.choice([True, False])
        app_frequency = random.choice(["Daily", "Weekly", "Monthly"])
        
        # Generate favorite locations (1-3)
        num_locations = random.randint(1, 3)
        favorite_locations = []
        for _ in range(num_locations):
            location = {
                "name": fake.city(),
                "coordinates": {
                    "lat": float(fake.latitude()),
                    "long": float(fake.longitude())
                }
            }
            favorite_locations.append(location)
        
        # Network settings
        preferred_network = random.choice(NETWORK_TYPES)
        data_saver = random.choice([True, False])
        
        # Privacy settings
        share_data = random.choice([True, False])
        ad_personalization = random.choice([True, False])
        
        # Usage stats
        total_data = f"{random.randint(50, 500)}GB"
        current_month_data = f"{random.randint(1, 20)}GB"
        total_minutes = random.randint(1000, 10000)
        international_minutes = random.randint(0, 500)
        
        # App usage (3-7 apps)
        num_apps = random.randint(3, 7)
        selected_apps = random.sample(POPULAR_APPS, min(num_apps, len(POPULAR_APPS)))
        app_usage = []
        for app in selected_apps:
            usage = f"{random.randint(1, 10)}GB"
            app_usage.append({"name": app, "usage": usage})
        
        # Support history
        support_history = []
        
        # Special case for Alexis Smith (customer ID 7)
        if customer_id == 7:
            # Ensure Alexis has a ticket about activating her iPhone
            iphone_activation_ticket = {
                "ticketId": f"TKT-{random.randint(10000, 99999)}",
                "date": fake.date_time_between(start_date="-3m", end_date="-2m").strftime("%Y-%m-%d"),
                "issue": "Device activation",
                "description": "Customer needs help activating new iPhone device",
                "status": "New",
                "resolutionNotes": "New ticket"
            }
            support_history.append(iphone_activation_ticket)
            
            # Add a few more tickets for Alexis to create an interesting history
            network_issue_ticket = {
                "ticketId": f"TKT-{random.randint(10000, 99999)}",
                "date": fake.date_time_between(start_date="-6m", end_date="-4m").strftime("%Y-%m-%d"),
                "issue": "Network connectivity",
                "description": "Customer reported poor signal strength at home",
                "status": "Resolved",
                "resolutionNotes": "Dispatched technician to check local tower. Signal booster installed at customer's residence. Signal strength improved to acceptable levels."
            }
            support_history.append(network_issue_ticket)
            
            billing_inquiry_ticket = {
                "ticketId": f"TKT-{random.randint(10000, 99999)}",
                "date": fake.date_time_between(start_date="-8m", end_date="-7m").strftime("%Y-%m-%d"),
                "issue": "Billing inquiry",
                "description": "Customer questioned charges on monthly statement",
                "status": "Resolved",
                "resolutionNotes": "Explained international roaming charges from customer's recent trip. Offered one-time courtesy credit of $25 as goodwill gesture."
            }
            support_history.append(billing_inquiry_ticket)
            
            data_usage_ticket = {
                "ticketId": f"TKT-{random.randint(10000, 99999)}",
                "date": fake.date_time_between(start_date="-1m", end_date="now").strftime("%Y-%m-%d"),
                "issue": "Data usage",
                "description": "Customer inquired about high data usage",
                "status": "Open",
                "resolutionNotes": "Reviewing customer's data usage patterns. Preliminary analysis suggests background app refresh may be consuming data. Scheduled follow-up call to discuss data-saving options."
            }
            support_history.append(data_usage_ticket)
            
            plan_upgrade_ticket = {
                "ticketId": f"TKT-{random.randint(10000, 99999)}",
                "date": fake.date_time_between(start_date="-10m", end_date="-9m").strftime("%Y-%m-%d"),
                "issue": "Plan upgrade",
                "description": "Customer interested in upgrading to a premium plan",
                "status": "Resolved",
                "resolutionNotes": "Discussed available premium plans. Customer upgraded to Premium Mobile 50GB plan with unlimited international calls. Set up automatic payment."
            }
            support_history.append(plan_upgrade_ticket)
        else:
            # Regular customers get 0-5 random tickets
            num_tickets = random.randint(0, 5)
            for _ in range(num_tickets):
                ticket_date = fake.date_time_between(start_date="-1y", end_date="now").strftime("%Y-%m-%d")
                issues = ["Network connectivity", "Billing inquiry", "Plan upgrade", "Technical support", "Device issue"]
                statuses = ["Open", "Closed", "In Progress", "Escalated", "Resolved"]
                
                ticket = {
                    "ticketId": f"TKT-{random.randint(10000, 99999)}",
                    "date": ticket_date,
                    "issue": random.choice(issues),
                    "status": random.choice(statuses),
                    "resolutionNotes": fake.paragraph(nb_sentences=2) if random.random() > 0.3 else ""
                }
                support_history.append(ticket)
        
        # Notes - for Alexis, add tech-savvy related notes
        if customer_id == 7:
            notes = "Tech-savvy customer who prefers digital communication. Knowledgeable about devices and services. Interested in new technology offerings. Good candidate for beta testing programs."
        else:
            notes = fake.paragraph(nb_sentences=random.randint(0, 3)) if random.random() > 0.7 else ""
        
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
                    "total": total_data,
                    "currentMonth": current_month_data
                },
                "callStats": {
                    "totalMinutes": total_minutes,
                    "internationalMinutes": international_minutes
                },
                "appUsage": app_usage
            },
            "supportHistory": support_history,
            "notes": notes,
            "memberID": str(uuid.uuid4())
        }
        
        user_profiles.append(profile)
    
    return user_profiles

def generate_customer_preferences(customer_links: List[Dict]) -> List[Dict]:
    """Generate MongoDB customer preferences."""
    customer_preferences = []
    
    for link in customer_links:
        customer_id = link["id"]  # Get the customer ID from the link
        customer_guid = link["customer_guid"]
        
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
            # Regular customer preferences
            contact_method = random.choice(["email", "phone", "SMS"])
            marketing_opt_in = random.choice([True, False])
            
            # Social media (some might be empty)
            social_media = {}
            if random.random() > 0.3:
                social_media["facebook"] = f"https://facebook.com/user{random.randint(1000, 9999)}"
            if random.random() > 0.4:
                social_media["twitter"] = f"https://twitter.com/user{random.randint(1000, 9999)}"
            if random.random() > 0.6:
                social_media["linkedin"] = f"https://linkedin.com/in/user{random.randint(1000, 9999)}"
            
            # Behavioral data
            last_website = fake.date_time_between(start_date="-3m", end_date="now").isoformat()
            last_app_login = fake.date_time_between(start_date="-1m", end_date="now").isoformat()
            
            # Customer notes (0-3)
            num_notes = random.randint(0, 3)
            customer_notes = []
            for _ in range(num_notes):
                note_date = fake.date_time_between(start_date="-1y", end_date="now").isoformat()
                note = {
                    "author": fake.name(),
                    "date": note_date,
                    "content": fake.paragraph(nb_sentences=2)
                }
                customer_notes.append(note)
        
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