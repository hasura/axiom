import random
from datetime import datetime, timedelta
from faker import Faker
import uuid
import csv
from typing import List, Dict, Optional, Tuple
import numpy as np
import os

# Initialize Faker
fake = Faker()

# Constants
CURRENT_DATE = datetime.now()
START_DATE = CURRENT_DATE - timedelta(days=365)

# ============================================================================
# CONFIGURATION - Modify these values to change the amount of data generated
# ============================================================================
CONFIG = {
    'num_accounts': 500,        # Number of accounts to generate
    'num_contacts': 2000,       # Number of contacts to generate
    'num_campaigns': 50,        # Number of campaigns to generate
    'num_campaign_members': 1000, # Number of campaign members to generate
    'num_opportunities': 750,   # Number of opportunities to generate
    'num_tasks': 3000,         # Number of tasks to generate
    'num_calls': 1000          # Number of calls to generate
}
# ============================================================================

# Sales pipeline constants
SALES_STAGES = ['Discovery', 'Qualification', 'Meeting', 'Proposal', 'Negotiation', 'Closed Won', 'Closed Lost']
# Using NumPy for more realistic stage probabilities with a log-normal distribution
STAGE_PROBABILITIES = {
    'Discovery': 0.15,
    'Qualification': 0.20,
    'Meeting': 0.25,
    'Proposal': 0.20,
    'Negotiation': 0.10,
    'Closed Won': 0.05,
    'Closed Lost': 0.05
}

# Industry-specific data
INDUSTRIES = ['Finance', 'Healthcare', 'Retail', 'Manufacturing', 'Technology']
# Using NumPy for more realistic revenue ranges with log-normal distribution
INDUSTRY_ARR_RANGES = {
    'Finance': (100000, 2000000),
    'Healthcare': (75000, 1500000),
    'Retail': (50000, 1000000),
    'Manufacturing': (100000, 2500000),
    'Technology': (150000, 3000000)
}

# Account tiers and their characteristics
ACCOUNT_TIERS = ['Tier 1', 'Tier 2', 'Tier 3']
TIER_PROBABILITIES = [0.2, 0.5, 0.3]  # 20% Tier 1, 50% Tier 2, 30% Tier 3

# Contact roles and their influence on deals
CONTACT_ROLES = ['Decision Maker', 'Influencer', 'Evaluator', 'Champion', 'Blocker']
ROLE_INFLUENCE = {
    'Decision Maker': 0.9,
    'Champion': 0.8,
    'Influencer': 0.6,
    'Evaluator': 0.4,
    'Blocker': 0.2
}

# Campaign types and their effectiveness
CAMPAIGN_TYPES = ['Webinar', 'Event', 'Email', 'Direct Mail', 'Social']
CAMPAIGN_EFFECTIVENESS = {
    'Webinar': 0.7,
    'Event': 0.8,
    'Email': 0.4,
    'Direct Mail': 0.3,
    'Social': 0.5
}

# Task types and their completion rates
TASK_TYPES = ['Call', 'Email', 'Meeting', 'Follow-up']
TASK_COMPLETION_RATES = {
    'Call': 0.8,
    'Email': 0.9,
    'Meeting': 0.95,
    'Follow-up': 0.7
}

def format_date(dt: datetime) -> str:
    return dt.strftime('%Y-%m-%d')

def format_datetime(dt: datetime) -> str:
    return dt.strftime('%Y-%m-%d %H:%M:%S')

def weighted_choice(choices: List, weights: List[float]) -> str:
    """Make a weighted random choice from a list of options."""
    # Normalize weights to sum to 1
    total = sum(weights)
    normalized_weights = [w/total for w in weights]
    # Using NumPy's random choice for better distribution
    return np.random.choice(choices, p=normalized_weights)

def generate_detailed_call_summary(account, opp, include_metrics, include_econ_buyer,
                                 include_decision_criteria, include_decision_process,
                                 include_paper_process, include_pain, include_champion,
                                 include_competition):
    """Generate a detailed call summary with rich MEDDPICC information."""
    
    # Base summary starts with the account and opportunity context
    summary = f"Call with {account['name']} regarding {opp['name']}. "
    
    # Add detailed information about each MEDDPICC element that was discussed
    
    # Metrics
    if include_metrics:
        metrics_details = [
            f"Customer needs to reduce API development time by 50-60%.",
            f"Target is to improve query performance by 70-80%, reducing response times from 800ms to under 200ms.",
            f"Goal to ship features 40% faster by implementing a more flexible data access layer.",
            f"Looking to reduce infrastructure costs by 30% while improving scalability.",
            f"Aiming for 99.99% uptime for critical services, current system achieves only 99.9%."
        ]
        summary += f"{random.choice(metrics_details)} "
    
    # Economic Buyer
    if include_econ_buyer:
        buyer_details = [
            f"CTO has final sign-off authority on all technology purchases over $50K.",
            f"VP of Engineering controls the budget for all developer tools and infrastructure.",
            f"Chief Data Officer will make the final decision and has expressed support for the initiative.",
            f"CEO is personally involved in this decision due to its strategic importance.",
            f"CFO requires ROI analysis before approving the purchase."
        ]
        summary += f"{random.choice(buyer_details)} "
    
    # Decision Criteria
    if include_decision_criteria:
        criteria_details = [
            f"Key evaluation criteria: performance (40%), security features (30%), ease of integration (30%).",
            f"Primary requirements: developer experience, documentation quality, and enterprise support.",
            f"Decision matrix focuses on scalability, compliance with security policies, and TCO.",
            f"Evaluation scorecard weights: technical capabilities (50%), support (25%), pricing (25%).",
            f"Must-have features: role-based access control, audit logging, and real-time subscriptions."
        ]
        summary += f"{random.choice(criteria_details)} "
    
    # Decision Process
    if include_decision_process:
        process_details = [
            f"3-phase evaluation: technical POC (2 weeks), security review (1 week), architecture board approval (1 week).",
            f"Decision timeline: technical evaluation by June 1, business case review by June 15, final decision by July 1.",
            f"Process involves technical team validation, followed by director approval and C-level sign-off.",
            f"Weekly steering committee meetings to review progress, with final decision expected in 4-6 weeks.",
            f"Evaluation team will present findings to leadership on the 15th, with decision expected within 10 days."
        ]
        summary += f"{random.choice(process_details)} "
    
    # Paper Process
    if include_paper_process:
        paper_details = [
            f"Procurement process: legal review (2 weeks), security assessment (1 week), PO processing (1 week).",
            f"Vendor onboarding requires security questionnaire, SOC2 report, and MSA negotiation.",
            f"Standard 45-day procurement cycle with security, legal, and finance approvals required.",
            f"Legal team needs to review all contracts; typical turnaround is 5-10 business days.",
            f"Procurement portal submission required, followed by three levels of internal approval."
        ]
        summary += f"{random.choice(paper_details)} "
    
    # Identified Pain
    if include_pain:
        pain_details = [
            f"Current pain: developers spending 40% of time writing boilerplate API code instead of business logic.",
            f"Performance issues with existing solution causing customer complaints and affecting NPS scores.",
            f"Access control management across microservices creating security risks and compliance issues.",
            f"Current architecture doesn't scale; each new data source requires 3-4 weeks of integration work.",
            f"Existing solution costs increasing by 15% annually while performance degrades."
        ]
        summary += f"{random.choice(pain_details)} "
    
    # Champion
    if include_champion:
        champion_details = [
            f"Lead architect will champion the implementation and has already created internal presentations.",
            f"Director of Engineering is advocating strongly for Hasura and has executive relationships.",
            f"Data Platform Lead has been researching GraphQL solutions for months and prefers Hasura.",
            f"VP of Product is driving this initiative and has budget authority for the project.",
            f"Technical Lead has built a prototype using Hasura and demonstrated it to the team."
        ]
        summary += f"{random.choice(champion_details)} "
    
    # Competition
    if include_competition:
        competition_details = [
            f"Also evaluating Apollo GraphQL and considering building an in-house solution.",
            f"Comparing Hasura with AWS AppSync and two other GraphQL implementations.",
            f"Currently using a custom REST API layer but also looking at Apollo as an alternative.",
            f"Considering both commercial options and open-source alternatives with support contracts.",
            f"Evaluating Hasura against continuing with their current solution and accepting limitations."
        ]
        summary += f"{random.choice(competition_details)} "
    
    # Add next steps
    next_steps = [
        f"Next steps: follow-up with technical documentation and ROI analysis.",
        f"Action items: schedule technical deep dive and provide reference customers.",
        f"Follow-up: send security whitepaper and arrange call with solution architect.",
        f"Next meeting scheduled for next week to continue evaluation.",
        f"Customer requested pricing proposal and implementation timeline."
    ]
    summary += f"{random.choice(next_steps)}"
    
    return summary

def generate_auth_data(num_users: int = 38) -> List[Dict]:
    users = []
    user_roles = {
        'executive': 3,        # C-level execs
        'business_analyst': 10, # Data-driven decision makers
        'data_steward': 5,     # Manage data quality
        'ai_ops': 5,          # AI operations team
        'customer_success': 5, # Support enterprise clients
        'sales_lead': 5       # Sales to business leaders
    }
    
    initial_users = [
        {'id': 1, 'email': 'emma.exec@hasura.io', 'roles': 'executive'},
        {'id': 2, 'email': 'liam.analyst@hasura.io', 'roles': 'business_analyst'},
        {'id': 3, 'email': 'sophia.data@hasura.io', 'roles': 'data_steward'},
        {'id': 4, 'email': 'noah.ai@hasura.io', 'roles': 'ai_ops'},
        {'id': 5, 'email': 'olivia.cs@hasura.io', 'roles': 'customer_success'},
        {'id': 6, 'email': 'eleanor.cs@hasura.io', 'roles': 'customer_success'},
        {'id': 7, 'email': 'julian.mayorga@hasura.io', 'roles': 'sales_lead'}
    ]
    
    users.extend([{
        'id': u['id'],
        'email': u['email'],
        'password': '$2a$10$DSRHAPZP0fuEFioGOPOdW.kgFWZvQgmMihaBYsUs8rO4cdHFFK7cS',
        'roles': u['roles'],
        'created_at': format_datetime(CURRENT_DATE - timedelta(days=random.randint(0, 365))),
        'updated_at': format_datetime(CURRENT_DATE)
    } for u in initial_users])

    user_id = 8
    for role, count in user_roles.items():
        remaining = max(0, count - len([u for u in initial_users if u['roles'] == role]))
        for _ in range(remaining):
            first_name = fake.first_name()
            last_name = fake.last_name()
            users.append({
                'id': user_id,
                'email': f"{first_name.lower()}.{last_name.lower()}.{role}@hasura.io",
                'password': '$2a$10$DSRHAPZP0fuEFioGOPOdW.kgFWZvQgmMihaBYsUs8rO4cdHFFK7cS',
                'roles': role,
                'created_at': format_datetime(CURRENT_DATE - timedelta(days=random.randint(0, 365))),
                'updated_at': format_datetime(CURRENT_DATE)
            })
            user_id += 1

    return users

def generate_salesforce_data(users: List[Dict], config: Dict[str, int] = CONFIG) -> Dict[str, List[Dict]]:
    sf_data = {
        'accounts': [],
        'contacts': [],
        'campaigns': [],
        'campaign_members': [],
        'opportunities': [],
        'opportunity_contact_roles': [],
        'tasks': []
    }

    # Generate accounts (50 accounts)
    for i in range(config['num_accounts']):
        account_id = f"001{i:04d}"
        industry = random.choice(INDUSTRIES)
        account_name = fake.company()
        account_tier = weighted_choice(ACCOUNT_TIERS, TIER_PROBABILITIES)
        
        # Set owner_id = 7 for the first account for authz
        owner_id = 7 if i == 0 else random.choice([u['id'] for u in users if u['roles'] in ['sales_lead', 'customer_success']])
        
        # Determine account type based on tier
        account_type = 'Enterprise' if account_tier == 'Tier 1' else 'Mid-Market' if account_tier == 'Tier 2' else 'SMB'
        
        # Determine if it's a named account based on tier
        named_account = 'Yes' if account_tier == 'Tier 1' else 'No' if account_tier == 'Tier 3' else 'Yes' if random.random() < 0.3 else 'No'
        
        # Generate realistic annual revenue based on industry and tier using log-normal distribution
        min_rev, max_rev = INDUSTRY_ARR_RANGES[industry]
        if account_tier == 'Tier 1':
            # Log-normal distribution for Tier 1 accounts
            annual_revenue = int(np.random.lognormal(mean=np.log(max_rev/2), sigma=0.5))
            annual_revenue = min(max(annual_revenue, max_rev // 2), max_rev)
        elif account_tier == 'Tier 2':
            # Log-normal distribution for Tier 2 accounts
            annual_revenue = int(np.random.lognormal(mean=np.log(min_rev), sigma=0.5))
            annual_revenue = min(max(annual_revenue, min_rev), max_rev // 2)
        else:
            # Log-normal distribution for Tier 3 accounts
            annual_revenue = int(np.random.lognormal(mean=np.log(min_rev/2), sigma=0.5))
            annual_revenue = min(max(annual_revenue, min_rev // 2), min_rev)
        
        # Generate customer status based on tier and named account status
        customer_status = 'Customer' if random.random() < (0.8 if account_tier == 'Tier 1' else 0.6 if account_tier == 'Tier 2' else 0.4) else 'Prospect'
        
        # Generate NPS score with realistic distribution (higher for customers, lower for prospects)
        if customer_status == 'Customer':
            # Using normal distribution for NPS scores
            nps_score = int(np.random.normal(loc=85 if account_tier == 'Tier 1' else 75, scale=5))
            nps_score = min(max(nps_score, 70), 100) if account_tier == 'Tier 1' else min(max(nps_score, 60), 90)
        else:
            nps_score = int(np.random.normal(loc=55, scale=5))
            nps_score = min(max(nps_score, 40), 70)
        
        # Generate churn score (lower for Tier 1, higher for Tier 3)
        churn_score = int(np.random.normal(loc=15 if account_tier == 'Tier 1' else 25 if account_tier == 'Tier 2' else 35, scale=5))
        churn_score = min(max(churn_score, 10), 40)
        
        # Generate usage metrics based on account tier and customer status
        if customer_status == 'Customer':
            # Using log-normal distribution for usage metrics
            instances = int(np.random.lognormal(mean=np.log(5 if account_tier == 'Tier 1' else 3 if account_tier == 'Tier 2' else 2), sigma=0.5))
            instances = min(max(instances, 3 if account_tier == 'Tier 1' else 2 if account_tier == 'Tier 2' else 1), 
                          10 if account_tier == 'Tier 1' else 5 if account_tier == 'Tier 2' else 3)
            
            pings = int(np.random.lognormal(mean=np.log(1000 if account_tier == 'Tier 1' else 500 if account_tier == 'Tier 2' else 200), sigma=0.5))
            pings = min(max(pings, 500 if account_tier == 'Tier 1' else 200 if account_tier == 'Tier 2' else 50), 
                       2000 if account_tier == 'Tier 1' else 800 if account_tier == 'Tier 2' else 300)
            
            api_calls = int(np.random.lognormal(mean=np.log(50000 if account_tier == 'Tier 1' else 10000 if account_tier == 'Tier 2' else 2000), sigma=0.5))
            api_calls = min(max(api_calls, 20000 if account_tier == 'Tier 1' else 5000 if account_tier == 'Tier 2' else 1000), 
                           100000 if account_tier == 'Tier 1' else 20000 if account_tier == 'Tier 2' else 5000)
            
            data_gb = int(np.random.lognormal(mean=np.log(100 if account_tier == 'Tier 1' else 50 if account_tier == 'Tier 2' else 10), sigma=0.5))
            data_gb = min(max(data_gb, 50 if account_tier == 'Tier 1' else 20 if account_tier == 'Tier 2' else 5), 
                         200 if account_tier == 'Tier 1' else 80 if account_tier == 'Tier 2' else 20)
        else:
            instances = random.randint(1, 2)
            pings = random.randint(10, 100)
            api_calls = random.randint(100, 1000)
            data_gb = random.randint(1, 10)
        
        # Generate subscription dates
        if customer_status == 'Customer':
            became_customer_date = fake.date_time_between(start_date=START_DATE)
            subscription_start = became_customer_date
            subscription_end = subscription_start + timedelta(days=365)
        else:
            became_customer_date = None
            subscription_start = None
            subscription_end = None
        
        sf_data['accounts'].append({
            'id': account_id,
            'account_buying_stage_6_sense_c': random.choice(['Awareness', 'Consideration', 'Decision']),
            'account_intent_score_6_sense_c': str(random.randint(50, 90)),
            'account_tier_c': account_tier,
            'annual_revenue': str(annual_revenue),
            'became_customer_date_c': format_date(became_customer_date) if became_customer_date else '',
            'billing_city': fake.city(),
            'billing_country': 'United States',
            'billing_state': fake.state_abbr(),
            'billing_street': fake.street_address(),
            'csm_owner_c': random.choice([u['id'] for u in users if u['roles'] == 'customer_success']),
            'customer_subscription_end_date_c': format_date(subscription_end) if subscription_end else '',
            'customer_subscription_initial_start_date_c': format_date(subscription_start) if subscription_start else '',
            'customer_support_tier_c': 'Premium' if account_tier == 'Tier 1' else 'Standard',
            'customer_type_c': account_type,
            'geo_c': random.choice(['NA', 'EMEA', 'APAC']),
            'industry': industry,
            'name': account_name,
            'named_account_c': named_account,
            'nps_score_c': str(nps_score),
            'oss_last_ping_date_c': format_date(fake.date_time_this_month()),
            'oss_total_instances_c': str(instances),
            'oss_total_pings_c': str(pings),
            'oss_usage_last_updated_c': format_date(fake.date_time_this_year()),
            'oss_user_c': fake.user_name(),
            'owner_id': owner_id,
            'primary_churn_score_c': str(churn_score),
            'projects_on_annual_plan_c': str(random.randint(1, 5)),
            'projects_on_monthly_plan_c': str(random.randint(0, 3)),
            'purchased_models_v_2_c': str(random.randint(1, 10)),
            'record_type_id': f"012{random.randint(1000, 9999)}",
            'region_c': random.choice(['NA', 'EMEA', 'APAC']),
            'saasoptics_arr_at_end_of_month_c': str(random.randint(100000, 5000000)),
            'type': customer_status,
            'ultimate_parent_c': '' if random.random() < 0.9 else account_id,
            'usage_annual_prod_models_v_2_c': str(random.randint(1, 10)),
            'usage_annual_v_2_api_last_month_c': str(api_calls),
            'usage_annual_v_2_api_yesterday_c': str(api_calls // 30),
            'usage_annual_v_2_data_gb_last_month_c': str(data_gb),
            'usage_annual_v_2_data_gb_yesterday_c': str(data_gb // 30),
            'usage_payg_last_invoiced_amount_c': str(random.randint(1000, 10000)),
            'usage_payg_models_c': str(random.randint(1, 5)),
            'website': f"https://{account_name.lower().replace(' ', '')}.com"
        })

    # Generate contacts (200 contacts)
    for i in range(config['num_contacts']):
        contact_id = f"003{i:04d}"
        account = random.choice(sf_data['accounts'])
        first_name = fake.first_name()
        last_name = fake.last_name()
        
        # Determine contact role based on account tier with more executives
        if account['account_tier_c'] == 'Tier 1':
            contact_role = weighted_choice(CONTACT_ROLES, [0.5, 0.3, 0.1, 0.1, 0.0])  # 50% decision makers
        elif account['account_tier_c'] == 'Tier 2':
            contact_role = weighted_choice(CONTACT_ROLES, [0.4, 0.3, 0.2, 0.1, 0.0])  # 40% decision makers
        else:
            contact_role = weighted_choice(CONTACT_ROLES, [0.3, 0.3, 0.2, 0.1, 0.1])  # 30% decision makers
        
        # Determine contact grade based on role
        if contact_role == 'Decision Maker':
            contact_grade = 'A'
        elif contact_role in ['Champion', 'Influencer']:
            contact_grade = 'B'
        else:
            contact_grade = 'C'
        
        # Determine contact status based on account type
        contact_status = 'Active' if account['type'] == 'Customer' and random.random() < 0.8 else 'Inactive'
        
        # Determine if discovery call completed based on contact role and status
        discovery_call_completed = 'Yes' if contact_role in ['Decision Maker', 'Champion'] and contact_status == 'Active' and random.random() < 0.7 else 'No'
        
        # Generate contact intent score based on role and status
        if contact_role == 'Decision Maker' and contact_status == 'Active':
            intent_score = random.randint(80, 95)
        elif contact_role in ['Champion', 'Influencer'] and contact_status == 'Active':
            intent_score = random.randint(70, 85)
        elif contact_status == 'Active':
            intent_score = random.randint(60, 75)
        else:
            intent_score = random.randint(40, 60)
        
        # Generate MQL counter based on contact role and status
        if contact_role == 'Decision Maker' and contact_status == 'Active':
            mql_counter = random.randint(2, 5)
        elif contact_status == 'Active':
            mql_counter = random.randint(1, 3)
        else:
            mql_counter = random.randint(0, 1)
        
        # Generate appropriate title based on role
        if contact_role == 'Decision Maker':
            title = random.choice(['CFO', 'COO', 'VP of Operations', 'Head of Analytics', 'Chief Data Officer'])
        elif contact_role == 'Champion':
            title = random.choice(['Director of Data', 'Head of Engineering', 'VP of Product'])
        elif contact_role == 'Influencer':
            title = random.choice(['Senior Data Scientist', 'Lead Engineer', 'Product Manager'])
        elif contact_role == 'Evaluator':
            title = random.choice(['Data Analyst', 'Software Engineer', 'Business Analyst'])
        else:
            title = random.choice(['Data Engineer', 'Analytics Manager', 'Technical Lead'])
        
        sf_data['contacts'].append({
            'id': contact_id,
            'account_id': account['id'],
            'cloud_user_activated_date_c': format_date(fake.date_time_this_year()) if account['type'] == 'Customer' and random.random() < 0.7 else '',
            'cloud_user_id_c': str(uuid.uuid4()) if account['type'] == 'Customer' and random.random() < 0.7 else '',
            'contact_grade_6_sense_c': contact_grade,
            'contact_intent_score_6_sense_c': str(intent_score),
            'contact_requested_date_c': format_date(fake.date_time_between(start_date=START_DATE)),
            'contact_roles_c': contact_role,
            'contact_status_c': contact_status,
            'ddn_advanced_trial_end_date_c': format_date(fake.future_datetime()) if account['type'] == 'Customer' and random.random() < 0.5 else '',
            'ddn_advanced_trial_start_date_c': format_date(fake.date_time_this_year()) if account['type'] == 'Customer' and random.random() < 0.5 else '',
            'ddn_base_trial_end_date_c': format_date(fake.future_datetime()) if account['type'] == 'Customer' and random.random() < 0.5 else '',
            'ddn_base_trial_start_date_c': format_date(fake.date_time_this_year()) if account['type'] == 'Customer' and random.random() < 0.5 else '',
            'ddn_signup_date_c': format_date(fake.date_time_between(start_date=START_DATE)) if account['type'] == 'Customer' and random.random() < 0.5 else '',
            'discovery_call_completed_c': discovery_call_completed,
            'discovery_call_notes_c': fake.paragraph() if discovery_call_completed == 'Yes' else '',
            'ead_successful_touch_channel_c': random.choice(['Email', 'Phone']),
            'email': fake.email(),
            'first_name': first_name,
            'free_email_domain_c': 'No' if '@' in account['website'] else 'Yes',
            'groove_last_touch_c': format_date(fake.date_time_this_month()) if contact_status == 'Active' else '',
            'groove_last_touch_type_c': random.choice(['Email', 'Call']),
            'last_activity_by_c': random.choice([u['id'] for u in users]),
            'last_activity_date_c': format_date(fake.date_time_this_month()) if contact_status == 'Active' else '',
            'last_discovery_call_c': format_date(fake.date_time_this_year()) if discovery_call_completed == 'Yes' else '',
            'last_mql_date_c': format_date(fake.date_time_this_year()) if mql_counter > 0 else '',
            'last_name': last_name,
            'last_successful_touch_channel_c': random.choice(['Email', 'Call']),
            'last_successful_touch_date_c': format_date(fake.date_time_this_month()) if contact_status == 'Active' else '',
            'last_successful_touch_family_c': random.choice(['Sales', 'Support']),
            'last_successful_touch_program_detail_c': random.choice(['Campaign', 'Outreach']),
            'last_successful_touch_type_c': random.choice(['Outbound', 'Inbound']),
            'last_working_date_c': format_date(fake.date_time_this_year()) if contact_status == 'Active' else '',
            'lead_source': random.choice(['Website', 'Referral', 'Event', 'Partner']),
            'lead_source_channel_c': random.choice(['Organic', 'Paid']),
            'lead_source_detail_c': random.choice(['Direct', 'Partner']),
            'middle_name': fake.first_name() if random.random() < 0.2 else '',
            'mkto_si_last_interesting_moment_date_c': format_date(fake.date_time_this_month()) if contact_status == 'Active' else '',
            'mkto_si_last_interesting_moment_desc_c': fake.sentence() if contact_status == 'Active' else '',
            'mql_counter_c': str(mql_counter),
            'mql_source_c': random.choice(['Webinar', 'Email', 'Event', 'Partner']),
            'name': f"{first_name} {last_name}",
            'owner_id': random.choice([u['id'] for u in users if u['roles'] in ['sales_lead', 'customer_success']]),
            'person_city_c': fake.city(),
            'person_country_c': 'United States',
            'person_geo_c': random.choice(['NA', 'EMEA', 'APAC']),
            'person_state_c': fake.state_abbr(),
            'prompt_ql_activated_c': 'Yes' if account['type'] == 'Customer' and random.random() < 0.6 else 'No',
            'prompt_ql_signup_date_c': format_date(fake.date_time_this_year()) if account['type'] == 'Customer' and random.random() < 0.6 else '',
            'status_reason_c': 'Active' if contact_status == 'Active' else 'No Response',
            'title': title,
            'trial_end_date_c': format_date(fake.future_datetime()) if account['type'] == 'Customer' and random.random() < 0.5 else '',
            'trial_start_date_c': format_date(fake.date_time_this_year()) if account['type'] == 'Customer' and random.random() < 0.5 else '',
            'v_3_user_c': 'Yes' if account['type'] == 'Customer' and random.random() < 0.7 else 'No'
        })

    # Generate campaigns (10 campaigns)
    campaign_ids = []
    for i in range(config['num_campaigns']):
        campaign_id = f"701{i:04d}"
        campaign_ids.append(campaign_id)
        campaign_type = weighted_choice(list(CAMPAIGN_TYPES), list(CAMPAIGN_EFFECTIVENESS.values()))
        sf_data['campaigns'].append({
            'id': campaign_id,
            'name': f"Q{random.randint(1, 4)} {random.choice(['AI Insights Summit', 'Data Strategy Webinar', 'Exec Roundtable'])}",
            'type': campaign_type
        })

    # Generate campaign members (100 members)
    for i in range(config['num_campaign_members']):
        campaign = random.choice(sf_data['campaigns'])
        contact = random.choice(sf_data['contacts'])
        account = next((a for a in sf_data['accounts'] if a['id'] == contact['account_id']), None)
        
        # Determine status based on campaign type and contact role
        if campaign['type'] in ['Webinar', 'Event']:
            if contact['contact_roles_c'] == 'Decision Maker':
                status = 'Attended' if random.random() < 0.7 else 'Responded'
            elif contact['contact_roles_c'] in ['Champion', 'Influencer']:
                status = 'Attended' if random.random() < 0.5 else 'Responded'
            else:
                status = 'Sent' if random.random() < 0.7 else 'Responded'
        else:
            if contact['contact_roles_c'] == 'Decision Maker':
                status = 'Responded' if random.random() < 0.6 else 'Sent'
            elif contact['contact_roles_c'] in ['Champion', 'Influencer']:
                status = 'Responded' if random.random() < 0.4 else 'Sent'
            else:
                status = 'Sent' if random.random() < 0.8 else 'Responded'
        
        # Determine if this is a net new lead
        net_new_lead = 'Yes' if contact['mql_counter_c'] == '0' and status in ['Responded', 'Attended'] else 'No'
        
        sf_data['campaign_members'].append({
            'id': f"00m{i:04d}",
            'campaign_id': campaign['id'],
            'company_or_account': account['name'] if account else '',
            'contact_id': contact['id'],
            'created_date': format_date(fake.date_time_this_year()),
            'lead_id': '',
            'net_new_lead_c': net_new_lead,
            'status': status
        })

    # Generate opportunities (75 opportunities)
    # First, create a list to track which accounts have executive contacts
    account_executive_contacts = {}
    for account in sf_data['accounts']:
        account_contacts = [c for c in sf_data['contacts'] if c['account_id'] == account['id']]
        executive_contacts = [c for c in account_contacts if c['contact_roles_c'] == 'Decision Maker']
        account_executive_contacts[account['id']] = executive_contacts
    
    for i in range(config['num_opportunities']):
        account = random.choice(sf_data['accounts'])
        opp_id = f"006{i:04d}"
        
        # Set owner_id = 7 for the first opportunity for authz
        owner_id = 7 if i == 0 else random.choice([u['id'] for u in users if u['roles'] == 'sales_lead'])
        
        # Determine stage based on weighted probabilities and executive alignment
        # This creates a stronger correlation between executive contacts and win rates
        has_executive_contacts = len(account_executive_contacts[account['id']]) > 0
        
        if has_executive_contacts:
            # Much higher probability of winning with executive alignment
            stage_weights = [0.05, 0.10, 0.15, 0.20, 0.20, 0.35, 0.05]  # 35% Closed Won, 5% Closed Lost
        else:
            # Lower probability of winning without executive alignment
            stage_weights = [0.15, 0.20, 0.25, 0.20, 0.10, 0.05, 0.05]  # 5% Closed Won, 5% Closed Lost
        
        stage = weighted_choice(SALES_STAGES, stage_weights)
        
        # Determine probability based on stage and executive alignment
        if stage == 'Discovery':
            probability = random.randint(20, 30)
        elif stage == 'Qualification':
            probability = random.randint(30, 40)
        elif stage == 'Meeting':
            probability = random.randint(40, 60)
        elif stage == 'Proposal':
            probability = random.randint(60, 75)
        elif stage == 'Negotiation':
            probability = random.randint(75, 85)
        elif stage == 'Closed Won':
            probability = 100
        else:  # Closed Lost
            probability = 0
        
        # Determine amount based on account tier, industry, and executive alignment
        min_arr, max_arr = INDUSTRY_ARR_RANGES[account['industry']]
        if account['account_tier_c'] == 'Tier 1':
            base_amount = random.randint(max_arr // 4, max_arr // 2)
        elif account['account_tier_c'] == 'Tier 2':
            base_amount = random.randint(min_arr // 2, max_arr // 4)
        else:
            base_amount = random.randint(min_arr // 4, min_arr // 2)
        
        # Increase amount if there's executive alignment
        # This creates a stronger correlation between executive contacts and deal size
        if has_executive_contacts:
            amount = int(base_amount * 2.5)  # 150% higher with executive alignment
        else:
            amount = base_amount
        
        # Determine close date based on stage
        if stage in ['Closed Won', 'Closed Lost']:
            close_date = fake.date_time_between(start_date=START_DATE, end_date=CURRENT_DATE)
        elif stage == 'Negotiation':
            close_date = fake.date_time_between(start_date=CURRENT_DATE, end_date=CURRENT_DATE + timedelta(days=30))
        elif stage == 'Proposal':
            close_date = fake.date_time_between(start_date=CURRENT_DATE + timedelta(days=30), end_date=CURRENT_DATE + timedelta(days=90))
        else:
            close_date = fake.date_time_between(start_date=CURRENT_DATE + timedelta(days=90), end_date=CURRENT_DATE + timedelta(days=180))
        
        # Generate MEDDPICC fields with realistic gaps
        # Not all opportunities will have all fields filled in
        
        # Metrics - quantifiable outcomes the customer is targeting
        metrics = None
        if random.random() < 0.7:  # 70% chance to have metrics
            metrics_options = [
                f"Reduce infrastructure cost by {random.randint(20, 40)}%",
                f"Improve time-to-market by {random.randint(30, 60)} days",
                f"Increase developer productivity by {random.randint(20, 50)}%",
                f"Reduce API latency by {random.randint(40, 80)}%",
                f"Cut data processing time by {random.randint(30, 70)}%",
                f"Achieve {random.randint(99, 100)}.{random.randint(0, 99)}% uptime for critical services",
                f"Decrease time to deploy new features by {random.randint(30, 70)}%"
            ]
            metrics = random.choice(metrics_options)
        
        # Economic Buyer - person with final sign-off power
        economic_buyer = None
        if random.random() < 0.6:  # 60% chance to have economic buyer identified
            # Check if there are executive contacts for this account
            executive_contacts = account_executive_contacts[account['id']]
            if executive_contacts:
                exec_contact = random.choice(executive_contacts)
                economic_buyer = exec_contact['id']
        
        # Decision Criteria - factors used to evaluate vendors
        decision_criteria = None
        if random.random() < 0.65:  # 65% chance to have decision criteria
            criteria_options = [
                "Performance, security, and ease of integration",
                "Cost efficiency, scalability, and enterprise support",
                "Developer experience, documentation, and community",
                "Compliance with regulatory requirements and data sovereignty",
                "Integration capabilities with existing tech stack",
                "Total cost of ownership and ROI timeline"
            ]
            decision_criteria = random.choice(criteria_options)
        
        # Decision Process - how the decision will be made
        decision_process = None
        if random.random() < 0.55:  # 55% chance to have decision process
            process_options = [
                "Technical evaluation followed by executive review and procurement approval",
                "POC with success criteria, followed by security review and contract negotiation",
                "Vendor comparison matrix, technical validation, and executive sign-off",
                "Internal champion presentation to steering committee for final approval",
                "Technical team evaluation, followed by business case presentation to leadership"
            ]
            decision_process = random.choice(process_options)
        
        # Paper Process - internal procurement steps
        paper_process = None
        if random.random() < 0.45:  # 45% chance to have paper process
            process_options = [
                "Legal review (2 weeks), procurement approval (1 week), vendor onboarding (1 week)",
                "Security assessment required before contract signing, 30-day payment terms",
                "MSA already in place, only SOW approval needed through procurement portal",
                "Requires three levels of approval: manager, director, and VP of Engineering",
                "Procurement team handles all vendor contracts with 45-day standard process"
            ]
            paper_process = random.choice(process_options)
        
        # Identified Pain - core business pain driving the evaluation
        identified_pain = None
        if random.random() < 0.75:  # 75% chance to have identified pain
            pain_options = [
                "Slow application delivery causing missed market opportunities",
                "Rising cloud costs from inefficient data processing",
                "Developer bottlenecks due to complex API management",
                "Data silos preventing unified customer view",
                "Security concerns with current GraphQL implementation",
                "Performance issues with existing data access layer",
                "Difficulty scaling current architecture to meet growth"
            ]
            identified_pain = random.choice(pain_options)
        
        # Champion - internal advocate with influence
        champion = None
        if random.random() < 0.6:  # 60% chance to have champion
            # Look for champions in the contacts
            champion_contacts = [c for c in sf_data['contacts']
                               if c['account_id'] == account['id'] and c['contact_roles_c'] == 'Champion']
            if champion_contacts:
                champ_contact = random.choice(champion_contacts)
                champion = champ_contact['id']
        
        # Competition - who else is being evaluated
        competition = None
        if random.random() < 0.5:  # 50% chance to have competition info
            competition_options = [
                "Apollo GraphQL, considering building in-house solution",
                "Evaluating Apollo and considering DIY GraphQL implementation",
                "Currently using REST APIs, evaluating multiple GraphQL solutions",
                "Legacy system with custom middleware, also looking at Apollo",
                "Considering both Hasura and building their own solution",
                "Evaluating Hasura against AWS AppSync and Apollo"
            ]
            competition = random.choice(competition_options)
        
        sf_data['opportunities'].append({
            'id': opp_id,
            'account_id': account['id'],
            'name': f"{account['name']} - {random.choice(['AI Data Expansion', 'Enterprise Renewal', 'New Data Layer'])}",
            'amount': str(amount),
            'stage': stage,
            'probability': probability,
            'close_date': format_date(close_date),
            'owner_id': owner_id,
            'created_date': format_date(fake.date_time_between(start_date=START_DATE, end_date=close_date)),
            'metrics_c': metrics,
            'economic_buyer_c': economic_buyer,
            'decision_criteria_c': decision_criteria,
            'decision_process_c': decision_process,
            'paper_process_c': paper_process,
            'identified_pain_c': identified_pain,
            'champion_c': champion,
            'competition_c': competition
        })

        # Add opportunity contact roles for this opportunity
        # If there are executive contacts, make sure to add them with appropriate roles
        account_contacts = [c for c in sf_data['contacts'] if c['account_id'] == account['id']]
        executive_contacts = account_executive_contacts[account['id']]
        non_executive_contacts = [c for c in account_contacts if c not in executive_contacts]

        # Add executive contacts first if they exist
        for exec_contact in executive_contacts:
            sf_data['opportunity_contact_roles'].append({
                'id': f"00r{len(sf_data['opportunity_contact_roles']):04d}",
                'contact_id': exec_contact['id'],
                'is_primary': 'Yes',
                'opportunity_id': opp_id,
                'role': 'Decision Maker'
            })

        # Add other contacts with different roles
        for contact in random.sample(non_executive_contacts, min(len(non_executive_contacts), 2)):
            sf_data['opportunity_contact_roles'].append({
                'id': f"00r{len(sf_data['opportunity_contact_roles']):04d}",
                'contact_id': contact['id'],
                'is_primary': 'No',
                'opportunity_id': opp_id,
                'role': contact['contact_roles_c']
            })

    # Generate tasks (300 tasks)
    for i in range(config['num_tasks']):
        task_type = weighted_choice(list(TASK_TYPES), list(TASK_COMPLETION_RATES.values()))
        
        # Determine completion status based on task type
        if task_type == 'Meeting':
            status = 'Completed' if random.random() < 0.95 else 'In Progress'
        elif task_type == 'Call':
            status = 'Completed' if random.random() < 0.8 else 'In Progress'
        elif task_type == 'Email':
            status = 'Completed' if random.random() < 0.9 else 'In Progress'
        else:  # Follow-up
            status = 'Completed' if random.random() < 0.7 else 'In Progress'
        
        # Determine call disposition if it's a call
        if task_type == 'Call':
            call_disposition = 'Connected' if random.random() < 0.7 else 'No Answer'
            call_type = 'Outbound' if random.random() < 0.6 else 'Inbound'
        else:
            call_disposition = ''
            call_type = ''
        
        # Determine completion date based on status
        if status == 'Completed':
            completed_date = format_datetime(fake.date_time_between(start_date=START_DATE, end_date=CURRENT_DATE))
        else:
            completed_date = ''
        
        sf_data['tasks'].append({
            'id': f"00T{i:04d}",
            'activity_date': format_date(fake.date_time_between(start_date=START_DATE, end_date="+30d")),
            'call_disposition': call_disposition,
            'call_type': call_type,
            'completed_date_time': completed_date,
            'description': fake.paragraph(),
            'owner_id': random.choice([u['id'] for u in users]),
            'status': status,
            'subject': random.choice(['Data Strategy Review', 'PromptQL Demo', 'Contract Discussion']),
            'task_subtype': task_type,
            'type': 'Task',
            'what_id': random.choice(sf_data['accounts'])['id'],
            'who_id': random.choice(sf_data['contacts'])['id']
        })

    return sf_data

def generate_clari_data(sf_data: Dict[str, List[Dict]], users: List[Dict], config: Dict[str, int] = CONFIG) -> Dict[str, List[Dict]]:
    clari_data = {
        'calls': [],
        'call_participants': [],
        'call_transcriptions': [],
        'call_action_items': [],
        'call_topics': []
    }

    # Generate calls (100 calls)
    for i in range(config['num_calls']):
        account = random.choice(sf_data['accounts'])
        account_opportunities = [o for o in sf_data['opportunities'] if o['account_id'] == account['id']]
        opp = random.choice(account_opportunities) if account_opportunities else None
        
        if not opp:
            opp_id = f"006999{i:04d}"
            fallback_opp = {
                'id': opp_id,
                'account_id': account['id'],
                'name': f"{account['name']} - Data Layer Exploration",
                'amount': str(random.randint(50000, 500000)),
                'stage': 'Discovery',
                'probability': random.randint(20, 50),
                'close_date': format_date(fake.date_time_between(start_date=START_DATE, end_date="+1y")),
                'owner_id': random.choice([u['id'] for u in users if u['roles'] == 'sales_lead']),
                'created_date': format_date(fake.date_time_this_year())
            }
            sf_data['opportunities'].append(fallback_opp)
            opp = fallback_opp

        # Determine call time based on opportunity stage
        if opp['stage'] in ['Closed Won', 'Closed Lost']:
            call_time = fake.date_time_between(start_date=START_DATE, end_date=CURRENT_DATE - timedelta(days=30))
        elif opp['stage'] == 'Negotiation':
            call_time = fake.date_time_between(start_date=CURRENT_DATE - timedelta(days=30), end_date=CURRENT_DATE)
        else:
            call_time = fake.date_time_between(start_date=START_DATE, end_date=CURRENT_DATE + timedelta(days=30))
        
        call_id = f"call{i:04d}"
        
        # Determine call type based on opportunity stage
        if opp['stage'] == 'Discovery':
            call_type = 'strategy_call'
        elif opp['stage'] in ['Qualification', 'Meeting']:
            call_type = 'demo'
        else:
            call_type = 'review'
        
        # Generate call topics based on opportunity stage
        if opp['stage'] == 'Discovery':
            topics = "Data Strategy, Pain Points, Business Goals"
        elif opp['stage'] == 'Qualification':
            topics = "Requirements, Budget, Timeline"
        elif opp['stage'] == 'Meeting':
            topics = "Product Demo, Use Cases, Integration"
        elif opp['stage'] == 'Proposal':
            topics = "Pricing, ROI, Implementation Plan"
        elif opp['stage'] == 'Negotiation':
            topics = "Contract Terms, Legal Review, Next Steps"
        else:
            topics = "Project Status, Success Metrics, Future Plans"
        
        # Get account contacts and identify executive contacts
        account_contacts = [c for c in sf_data['contacts'] if c['account_id'] == account['id']]
        executive_contacts = [c for c in account_contacts if c['contact_roles_c'] == 'Decision Maker']
        non_executive_contacts = [c for c in account_contacts if c not in executive_contacts]
        
        # Determine if this is a won opportunity
        is_won = opp['stage'] == 'Closed Won'
        
        # For won opportunities, ensure we have at least one executive contact
        # but don't automatically add them to calls
        if is_won and not executive_contacts:
            # Create an executive contact for this account
            exec_id = f"003{len(sf_data['contacts']):04d}"
            exec_first_name = fake.first_name()
            exec_last_name = fake.last_name()
            exec_title = random.choice(['CEO', 'CTO', 'CFO', 'Chief Data Officer', 'VP of Engineering', 'President'])
            
            new_exec = {
                'id': exec_id,
                'account_id': account['id'],
                'first_name': exec_first_name,
                'last_name': exec_last_name,
                'email': f"{exec_first_name.lower()}.{exec_last_name.lower()}@{account['website'].replace('https://', '')}",
                'title': exec_title,
                'contact_roles_c': 'Decision Maker',
                'contact_status_c': 'Active',
                'contact_grade_6_sense_c': 'A',
                'contact_intent_score_6_sense_c': str(random.randint(80, 95)),
                'mql_counter_c': str(random.randint(2, 5)),
                'discovery_call_completed_c': 'Yes',
                'discovery_call_notes_c': fake.paragraph(),
                'name': f"{exec_first_name} {exec_last_name}"
            }
            
            sf_data['contacts'].append(new_exec)
            executive_contacts.append(new_exec)
        
        # Determine if an executive should participate based on opportunity outcome
        # This creates a stronger correlation between executive participation and wins
        should_include_exec = False
        if is_won:
            should_include_exec = random.random() < 0.9  # 90% chance for won opportunities
        else:
            should_include_exec = random.random() < 0.3  # 30% chance for lost opportunities
        
        # Create a list of contact IDs for the call
        contact_ids = []
        
        # Add executive if needed and available
        if should_include_exec and executive_contacts:
            exec_contact = random.choice(executive_contacts)
            contact_ids.append(exec_contact['id'])
        
        # Add remaining participants
        num_participants = random.randint(2, 5)
        remaining_slots = num_participants - len(contact_ids)
        
        if remaining_slots > 0:
            # For won opportunities, prioritize non-executive contacts from the same account
            if is_won and non_executive_contacts:
                selected_contacts = random.sample(non_executive_contacts, min(remaining_slots, len(non_executive_contacts)))
            else:
                # For other opportunities, mix account contacts with random contacts
                account_contacts_pool = non_executive_contacts if non_executive_contacts else []
                all_contacts = account_contacts_pool + [c for c in sf_data['contacts'] if c not in account_contacts_pool]
                selected_contacts = random.sample(all_contacts, min(remaining_slots, len(all_contacts)))
            
            for contact in selected_contacts:
                contact_ids.append(contact['id'])
        
        # Generate realistic transcriptions that could be used for MEDDPICC analysis
        # Create a list of participants for this call
        participants = []
        for j, contact_id in enumerate(contact_ids):
            contact = next((c for c in sf_data['contacts'] if c['id'] == contact_id), None)
            if contact:
                participants.append({
                    'id': j,
                    'name': f"{contact['first_name']} {contact['last_name']}",
                    'role': contact['contact_roles_c'],
                    'company': 'Hasura' if j == 0 else account['name'],
                    'title': contact['title']
                })
        
        # Add a Hasura rep if not already included
        if not any(p['company'] == 'Hasura' for p in participants):
            hasura_rep = {
                'id': len(participants),
                'name': random.choice(['Emma Johnson', 'Michael Chen', 'Sarah Williams', 'David Rodriguez']),
                'role': 'Sales Representative',
                'company': 'Hasura',
                'title': random.choice(['Account Executive', 'Solutions Engineer', 'Customer Success Manager'])
            }
            participants.append(hasura_rep)
        
        # For the first call of each opportunity, ensure we cover all MEDDPICC elements
        # For subsequent calls, be more selective
        is_first_call = not any(c['salesforce_deal_id'] == opp['id'] for c in clari_data['calls'])
        
        # Determine which MEDDPICC elements to include
        # For the first call, include all elements that aren't already populated
        # For subsequent calls, be more selective but still cover missing elements
        include_metrics = opp.get('metrics_c') is None and (is_first_call or random.random() < 0.7)
        include_econ_buyer = opp.get('economic_buyer_c') is None and (is_first_call or random.random() < 0.6)
        include_decision_criteria = opp.get('decision_criteria_c') is None and (is_first_call or random.random() < 0.65)
        include_decision_process = opp.get('decision_process_c') is None and (is_first_call or random.random() < 0.55)
        include_paper_process = opp.get('paper_process_c') is None and (is_first_call or random.random() < 0.45)
        include_pain = opp.get('identified_pain_c') is None and (is_first_call or random.random() < 0.75)
        include_champion = opp.get('champion_c') is None and (is_first_call or random.random() < 0.6)
        include_competition = opp.get('competition_c') is None and (is_first_call or random.random() < 0.5)
        
        # For the first call, ensure we have at least one of each MEDDPICC element
        if is_first_call:
            include_metrics = True
            include_pain = True
            # Include at least one of economic buyer or champion
            if not include_econ_buyer and not include_champion:
                include_econ_buyer = True
            # Include at least one of decision criteria or process
            if not include_decision_criteria and not include_decision_process:
                include_decision_criteria = True
        
        # Update the call record with the contact IDs
        clari_data['calls'].append({
            'id': call_id,
            'account_name': account['name'],
            'call_action_items_discussed': fake.sentence(),
            'call_action_items_discussed_embedding': '[0,0,0]',  # Placeholder vector
            'call_full_transcript': "This transcript will be populated from the detailed conversation snippets",
            'call_full_transcript_embedding': '[0,0,0]',
            'call_key_takeaways': f"MEDDPICC: " +
                                 (f"M✓ " if include_metrics else "M✗ ") +
                                 (f"E✓ " if include_econ_buyer else "E✗ ") +
                                 (f"D✓ " if include_decision_criteria else "D✗ ") +
                                 (f"D✓ " if include_decision_process else "D✗ ") +
                                 (f"P✓ " if include_paper_process else "P✗ ") +
                                 (f"I✓ " if include_pain else "I✗ ") +
                                 (f"C✓ " if include_champion else "C✗ ") +
                                 (f"C✓" if include_competition else "C✗"),
            'call_key_takeaways_embedding': '[0,0,0]',
            'call_review_page': f"https://clari.com/review/{call_id}",
            'call_summary': generate_detailed_call_summary(account, opp, include_metrics, include_econ_buyer,
                                                         include_decision_criteria, include_decision_process,
                                                         include_paper_process, include_pain, include_champion,
                                                         include_competition),
            'call_summary_embedding': '[0,0,0]',
            'call_topics_discussed': topics,
            'call_topics_discussed_embedding': '[0,0,0]',
            'last_modified_time': format_datetime(call_time + timedelta(minutes=60)),
            'salesforce_account_id': account['id'],
            'salesforce_contact_ids': '{' + ','.join(contact_ids) + '}',
            'salesforce_deal_id': opp['id'],
            'source_id': f"zoom_{random.randint(1000, 9999)}",
            'time': format_datetime(call_time),
            'title': f"{account['name']} - {random.choice(['Data Strategy', 'AI Demo', 'Exec Briefing'])}",
            'type': call_type
        })
        
        # Add call participants
        for j, contact_id in enumerate(contact_ids):
            contact = next((c for c in sf_data['contacts'] if c['id'] == contact_id), None)
            if contact:
                is_executive = contact['contact_roles_c'] == 'Decision Maker'
                clari_data['call_participants'].append({
                    'call_id': call_id,
                    'call_person_id': f"{call_id}_part{j}",
                    'email': contact['email'],
                    'is_organizer': 'True' if (is_executive and random.random() < 0.7) or (j == 0 and random.random() < 0.3) else 'False',
                    'name': f"{contact['first_name']} {contact['last_name']}",
                    'person_id': random.randint(1, 1000),
                    'user_id': random.choice([u['id'] for u in users])
                })

        # Generate conversation snippets based on opportunity stage
        conversation_snippets = []
        
        # Add introduction
        hasura_rep = next(p for p in participants if p['company'] == 'Hasura')
        client_rep = next((p for p in participants if p['company'] != 'Hasura'), None)
        
        conversation_snippets.append({
            'speaker': hasura_rep['name'],
            'text': f"Thanks everyone for joining today's call. I'm {hasura_rep['name']} from Hasura, and I'm excited to discuss how we can help {account['name']} with your data API needs."
        })
        
        if client_rep:
            conversation_snippets.append({
                'speaker': client_rep['name'],
                'text': f"Thanks for having us. We're looking forward to learning more about how Hasura can help us address our challenges."
            })
        
        # Add MEDDPICC-related conversation snippets based on stage
        if opp['stage'] in ['Discovery', 'Qualification']:
            # Pain points discussion
            if include_pain:
                conversation_snippets.append({
                    'speaker': hasura_rep['name'],
                    'text': "Could you tell me more about the challenges you're currently facing with your data access layer?"
                })
                
                pain_responses = [
                    f"Our developers are spending too much time writing custom APIs instead of focusing on business logic. It's really slowing down our release cycles.",
                    f"We're struggling with our current solution's performance. As our data grows, queries are getting slower and it's affecting user experience.",
                    f"Managing access control across all our microservices is becoming a nightmare. We need a more centralized approach.",
                    f"Our current architecture doesn't scale well. Every new data source requires weeks of integration work."
                ]
                
                if client_rep:
                    conversation_snippets.append({
                        'speaker': client_rep['name'],
                        'text': random.choice(pain_responses)
                    })
            
            # Metrics discussion
            if include_metrics:
                conversation_snippets.append({
                    'speaker': hasura_rep['name'],
                    'text': "What specific outcomes are you hoping to achieve with a new solution? Are there any metrics or KPIs you're targeting?"
                })
                
                metrics_responses = [
                    f"We need to reduce our API development time by at least 50%. Right now it takes us about 3 weeks to build and deploy new endpoints.",
                    f"Our goal is to improve query performance by 70%. Current response times are averaging 800ms, and we need to get that down to under 200ms.",
                    f"We want to enable our front-end teams to ship features 40% faster by giving them a more flexible data access layer."
                ]
                
                if client_rep:
                    conversation_snippets.append({
                        'speaker': client_rep['name'],
                        'text': random.choice(metrics_responses)
                    })
        
        elif opp['stage'] in ['Meeting', 'Proposal']:
            # Decision process discussion
            if include_decision_process:
                conversation_snippets.append({
                    'speaker': hasura_rep['name'],
                    'text': "I'd like to understand your evaluation process better. What steps do you typically go through when selecting a new technology like this?"
                })
                
                process_responses = [
                    "We usually start with a technical POC to validate the solution, then do a security review. After that, we present to the architecture review board for final approval.",
                    "Our process involves a technical evaluation first, then a business case review with our leadership team, and finally procurement and legal review.",
                    "We have a three-phase approach: technical validation, integration testing with our existing systems, and then a final review with our CTO's team."
                ]
                
                if client_rep:
                    conversation_snippets.append({
                        'speaker': client_rep['name'],
                        'text': random.choice(process_responses)
                    })
            
            # Decision criteria discussion
            if include_decision_criteria:
                conversation_snippets.append({
                    'speaker': hasura_rep['name'],
                    'text': "What criteria are most important to you when evaluating solutions like Hasura?"
                })
                
                criteria_responses = [
                    "Performance is our top priority, followed by security features and ease of integration with our existing stack.",
                    "We're looking at developer experience, documentation quality, and enterprise support options as our main criteria.",
                    "Our key requirements are scalability, compliance with our security policies, and total cost of ownership."
                ]
                
                if client_rep:
                    conversation_snippets.append({
                        'speaker': client_rep['name'],
                        'text': random.choice(criteria_responses)
                    })
            
            # Competition discussion
            if include_competition:
                conversation_snippets.append({
                    'speaker': hasura_rep['name'],
                    'text': "Are you evaluating any other solutions alongside Hasura?"
                })
                
                competition_responses = [
                    "Yes, we're also looking at Apollo GraphQL and considering building something in-house.",
                    "We're comparing Hasura with AWS AppSync and a couple of other GraphQL implementations.",
                    "We've been using a custom REST API layer, but we're also evaluating Apollo as an alternative to Hasura."
                ]
                
                if client_rep:
                    conversation_snippets.append({
                        'speaker': client_rep['name'],
                        'text': random.choice(competition_responses)
                    })
        
        elif opp['stage'] in ['Negotiation', 'Closed Won']:
            # Economic buyer discussion
            if include_econ_buyer:
                conversation_snippets.append({
                    'speaker': hasura_rep['name'],
                    'text': "Who will be making the final decision on this purchase? Is there anyone else we should include in our discussions?"
                })
                
                buyer_responses = [
                    f"That would be our CTO, Sarah Johnson. She has the final sign-off on all technology purchases over $50K.",
                    f"Our VP of Engineering, Michael Chen, will need to approve this. He manages the budget for all developer tools.",
                    f"The final approval will come from our Chief Data Officer. He's very supportive of this initiative."
                ]
                
                if client_rep:
                    conversation_snippets.append({
                        'speaker': client_rep['name'],
                        'text': random.choice(buyer_responses)
                    })
            
            # Paper process discussion
            if include_paper_process:
                conversation_snippets.append({
                    'speaker': hasura_rep['name'],
                    'text': "Could you walk me through your procurement process? What steps do we need to take to get the contract finalized?"
                })
                
                paper_responses = [
                    "We'll need to go through legal review first, which typically takes 2 weeks. Then procurement will process the PO, which is another week.",
                    "Our procurement process is pretty straightforward. We'll need to get you set up as a vendor in our system, then the contract goes through legal review.",
                    "We have a standard 45-day procurement cycle. It starts with security assessment, then legal review, and finally finance approval."
                ]
                
                if client_rep:
                    conversation_snippets.append({
                        'speaker': client_rep['name'],
                        'text': random.choice(paper_responses)
                    })
            
            # Champion discussion
            if include_champion:
                conversation_snippets.append({
                    'speaker': hasura_rep['name'],
                    'text': "Who on your team will be leading the implementation if you decide to move forward with Hasura?"
                })
                
                champion_responses = [
                    f"I'll be leading the implementation team. I've already started getting the team excited about what we can do with Hasura.",
                    f"Our lead architect, David, will be spearheading this. He's been advocating for a GraphQL solution for months.",
                    f"I'm going to be the project lead. I've already created some internal presentations about how Hasura can solve our challenges."
                ]
                
                if client_rep:
                    conversation_snippets.append({
                        'speaker': client_rep['name'],
                        'text': random.choice(champion_responses)
                    })
        
        # Add closing remarks
        conversation_snippets.append({
            'speaker': hasura_rep['name'],
            'text': f"This has been really helpful. I'll follow up with a summary of our discussion and the next steps we discussed."
        })
        
        if client_rep:
            conversation_snippets.append({
                'speaker': client_rep['name'],
                'text': "Great, looking forward to it. Thanks for your time today."
            })
        
        # Convert conversation snippets to transcriptions
        for j, snippet in enumerate(conversation_snippets):
            speaker_id = next((p['id'] for p in participants if p['name'] == snippet['speaker']), 0)
            start_time = j * 2  # Simple time spacing
            end_time = start_time + 1.5
            
            clari_data['call_transcriptions'].append({
                'call_id': call_id,
                'call_person_id': f"{call_id}_part{speaker_id}",
                'end_time': end_time,
                'person_id': random.randint(1, 1000),
                'start_time': start_time,
                'text': snippet['text'],
                'text_embedding': '[0,0,0]',
                'transcription_id': f"trans_{call_id}_{j}"
            })

        # Generate action items (1-3 per call)
        for j in range(random.randint(1, 3)):
            # For won opportunities, make executives more likely to be action item owners
            if is_won and executive_contacts and random.random() < 0.7:
                contact = random.choice(executive_contacts)
            else:
                contact = random.choice(sf_data['contacts'])
                
            clari_data['call_action_items'].append({
                'action_item': f"Follow up on {random.choice(['data connectors', 'AI insights', 'pricing'])}",
                'call_id': call_id,
                'end_timestamp': (call_time + timedelta(minutes=60)).strftime('%H:%M:%S'),
                'owner_name': f"{contact['first_name']} {contact['last_name']}",
                'reasoning': fake.sentence(),
                'speaker_name': f"{contact['first_name']} {contact['last_name']}",
                'start_timestamp': call_time.strftime('%H:%M:%S'),
                'timeline': random.choice(['Next week', 'By EOM', 'Within 5 days'])
            })

        # Generate topics (2-4 per call)
        for j in range(random.randint(2, 4)):
            clari_data['call_topics'].append({
                'call_id': call_id,
                'end_timestamp': (call_time + timedelta(minutes=60)).strftime('%H:%M:%S'),
                'name': random.choice(['Data Integration', 'AI-Powered Insights', 'Scalability', 'ROI Discussion']),
                'start_timestamp': call_time.strftime('%H:%M:%S'),
                'summary': fake.sentence()
            })

    return clari_data

def write_to_csv(data: List[Dict], filename: str):
    if not data:
        return
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

def main():
    # Create output directories
    output_dir = '.'
    os.makedirs(os.path.join(output_dir, 'postgres'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'pgvector'), exist_ok=True)
    
    # Generate data
    auth_users = generate_auth_data()
    write_to_csv(auth_users, os.path.join(output_dir, 'postgres/auth_users.csv'))

    sf_data = generate_salesforce_data(auth_users, CONFIG)
    for table_name, records in sf_data.items():
        write_to_csv(records, os.path.join(output_dir, f'postgres/salesforce_{table_name}.csv'))

    clari_data = generate_clari_data(sf_data, auth_users, CONFIG)
    for table_name, records in clari_data.items():
        write_to_csv(records, os.path.join(output_dir, f'pgvector/clari_{table_name}.csv'))

    print(f"CSV files have been generated successfully in {output_dir}")
    print("\nGenerated entities:")
    for key, value in CONFIG.items():
        print(f"- {key.replace('_', ' ').title()}: {value}")

if __name__ == "__main__":
    main()