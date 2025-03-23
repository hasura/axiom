import random
from datetime import datetime, timedelta
from faker import Faker
import uuid
import csv
from typing import List, Dict, Optional

# Initialize Faker
fake = Faker()

# Constants
CURRENT_DATE = datetime.now()
START_DATE = CURRENT_DATE - timedelta(days=365)

def format_date(dt: datetime) -> str:
    return dt.strftime('%Y-%m-%d')

def format_datetime(dt: datetime) -> str:
    return dt.strftime('%Y-%m-%d %H:%M:%S')

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
        {'id': 5, 'email': 'olivia.cs@hasura.io', 'roles': 'customer_success'}
    ]
    
    users.extend([{
        'id': u['id'],
        'email': u['email'],
        'password': '$2a$10$DSRHAPZP0fuEFioGOPOdW.kgFWZvQgmMihaBYsUs8rO4cdHFFK7cS',
        'roles': u['roles'],
        'created_at': format_datetime(CURRENT_DATE - timedelta(days=random.randint(0, 365))),
        'updated_at': format_datetime(CURRENT_DATE)
    } for u in initial_users])

    user_id = 6
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

def generate_salesforce_data(users: List[Dict]) -> Dict[str, List[Dict]]:
    sf_data = {
        'accounts': [],
        'contacts': [],
        'campaigns': [],
        'campaign_members': [],
        'opportunities': [],
        'opportunity_contact_roles': [],
        'tasks': []
    }

    industries = ['Finance', 'Healthcare', 'Retail', 'Manufacturing', 'Technology']
    
    # Generate accounts (50 accounts)
    for i in range(50):
        account_id = f"001{i:04d}"
        industry = random.choice(industries)
        account_name = fake.company()
        sf_data['accounts'].append({
            'id': account_id,
            'account_buying_stage_6_sense_c': random.choice(['Awareness', 'Consideration', 'Decision']),
            'account_intent_score_6_sense_c': str(random.randint(50, 90)),
            'account_tier_c': random.choice(['Tier 1', 'Tier 2']),
            'annual_revenue': str(random.randint(5000000, 500000000)),
            'became_customer_date_c': format_date(fake.date_time_between(start_date=START_DATE)),
            'billing_city': fake.city(),
            'billing_country': 'United States',
            'billing_state': fake.state_abbr(),
            'billing_street': fake.street_address(),
            'csm_owner_c': random.choice([u['id'] for u in users if u['roles'] == 'customer_success']),
            'customer_subscription_end_date_c': format_date(fake.future_datetime()),
            'customer_subscription_initial_start_date_c': format_date(fake.date_time_between(start_date=START_DATE)),
            'customer_support_tier_c': random.choice(['Premium', 'Standard']),
            'customer_type_c': random.choice(['Enterprise', 'Mid-Market']),
            'geo_c': random.choice(['NA', 'EMEA', 'APAC']),
            'industry': industry,
            'name': account_name,
            'named_account_c': random.choice(['Yes', 'No']),
            'nps_score_c': str(random.randint(70, 100)),
            'oss_last_ping_date_c': format_date(fake.date_time_this_month()),
            'oss_total_instances_c': str(random.randint(1, 5)),
            'oss_total_pings_c': str(random.randint(100, 1000)),
            'oss_usage_last_updated_c': format_date(fake.date_time_this_year()),
            'oss_user_c': fake.user_name(),
            'owner_id': random.choice([u['id'] for u in users if u['roles'] in ['sales_lead', 'customer_success']]),
            'primary_churn_score_c': str(random.randint(10, 40)),
            'projects_on_annual_plan_c': str(random.randint(1, 5)),
            'projects_on_monthly_plan_c': str(random.randint(0, 3)),
            'purchased_models_v_2_c': str(random.randint(1, 10)),
            'record_type_id': f"012{random.randint(1000, 9999)}",
            'region_c': random.choice(['NA', 'EMEA', 'APAC']),
            'saasoptics_arr_at_end_of_month_c': str(random.randint(100000, 5000000)),
            'type': random.choice(['Customer', 'Prospect']),
            'ultimate_parent_c': '' if random.random() < 0.9 else account_id,
            'usage_annual_prod_models_v_2_c': str(random.randint(1, 10)),
            'usage_annual_v_2_api_last_month_c': str(random.randint(1000, 50000)),
            'usage_annual_v_2_api_yesterday_c': str(random.randint(50, 500)),
            'usage_annual_v_2_data_gb_last_month_c': str(random.randint(10, 100)),
            'usage_annual_v_2_data_gb_yesterday_c': str(random.randint(1, 10)),
            'usage_payg_last_invoiced_amount_c': str(random.randint(1000, 10000)),
            'usage_payg_models_c': str(random.randint(1, 5)),
            'website': f"https://{account_name.lower().replace(' ', '')}.com"
        })

    # Generate contacts (200 contacts)
    for i in range(200):
        contact_id = f"003{i:04d}"
        account = random.choice(sf_data['accounts'])
        first_name = fake.first_name()
        last_name = fake.last_name()
        sf_data['contacts'].append({
            'id': contact_id,
            'account_id': account['id'],
            'cloud_user_activated_date_c': format_date(fake.date_time_this_year()),
            'cloud_user_id_c': str(uuid.uuid4()),
            'contact_grade_6_sense_c': random.choice(['A', 'B', 'C']),
            'contact_intent_score_6_sense_c': str(random.randint(60, 95)),
            'contact_requested_date_c': format_date(fake.date_time_between(start_date=START_DATE)),
            'contact_roles_c': random.choice(['Decision Maker', 'Influencer']),
            'contact_status_c': random.choice(['Active', 'Inactive']),
            'ddn_advanced_trial_end_date_c': format_date(fake.future_datetime()),
            'ddn_advanced_trial_start_date_c': format_date(fake.date_time_this_year()),
            'ddn_base_trial_end_date_c': format_date(fake.future_datetime()),
            'ddn_base_trial_start_date_c': format_date(fake.date_time_this_year()),
            'ddn_signup_date_c': format_date(fake.date_time_between(start_date=START_DATE)),
            'discovery_call_completed_c': random.choice(['Yes', 'No']),
            'discovery_call_notes_c': fake.paragraph(),
            'ead_successful_touch_channel_c': random.choice(['Email', 'Phone']),
            'email': fake.email(),
            'first_name': first_name,
            'free_email_domain_c': random.choice(['Yes', 'No']),
            'groove_last_touch_c': format_date(fake.date_time_this_month()),
            'groove_last_touch_type_c': random.choice(['Email', 'Call']),
            'last_activity_by_c': random.choice([u['id'] for u in users]),
            'last_activity_date_c': format_date(fake.date_time_this_month()),
            'last_discovery_call_c': format_date(fake.date_time_this_year()),
            'last_mql_date_c': format_date(fake.date_time_this_year()),
            'last_name': last_name,
            'last_successful_touch_channel_c': random.choice(['Email', 'Call']),
            'last_successful_touch_date_c': format_date(fake.date_time_this_month()),
            'last_successful_touch_family_c': random.choice(['Sales', 'Support']),
            'last_successful_touch_program_detail_c': random.choice(['Campaign', 'Outreach']),
            'last_successful_touch_type_c': random.choice(['Outbound', 'Inbound']),
            'last_working_date_c': format_date(fake.date_time_this_year()),
            'lead_source': random.choice(['Website', 'Referral']),
            'lead_source_channel_c': random.choice(['Organic', 'Paid']),
            'lead_source_detail_c': random.choice(['Direct', 'Partner']),
            'middle_name': fake.first_name() if random.random() < 0.2 else '',
            'mkto_si_last_interesting_moment_date_c': format_date(fake.date_time_this_month()),
            'mkto_si_last_interesting_moment_desc_c': fake.sentence(),
            'mql_counter_c': str(random.randint(0, 3)),
            'mql_source_c': random.choice(['Webinar', 'Email']),
            'name': f"{first_name} {last_name}",
            'owner_id': random.choice([u['id'] for u in users if u['roles'] in ['sales_lead', 'customer_success']]),
            'person_city_c': fake.city(),
            'person_country_c': 'United States',
            'person_geo_c': random.choice(['NA', 'EMEA', 'APAC']),
            'person_state_c': fake.state_abbr(),
            'prompt_ql_activated_c': random.choice(['Yes', 'No']),
            'prompt_ql_signup_date_c': format_date(fake.date_time_this_year()),
            'status_reason_c': random.choice(['Active', 'No Response']),
            'title': random.choice(['CFO', 'COO', 'VP of Operations', 'Head of Analytics', 'Chief Data Officer']),
            'trial_end_date_c': format_date(fake.future_datetime()),
            'trial_start_date_c': format_date(fake.date_time_this_year()),
            'v_3_user_c': random.choice(['Yes', 'No'])
        })

    # Generate campaigns (10 campaigns)
    campaign_ids = []
    for i in range(10):
        campaign_id = f"701{i:04d}"
        campaign_ids.append(campaign_id)
        sf_data['campaigns'].append({
            'id': campaign_id,
            'name': f"Q{random.randint(1, 4)} {random.choice(['AI Insights Summit', 'Data Strategy Webinar', 'Exec Roundtable'])}",
            'type': random.choice(['Webinar', 'Event', 'Email'])
        })

    # Generate campaign members (100 members)
    for i in range(100):
        sf_data['campaign_members'].append({
            'id': f"00m{i:04d}",
            'campaign_id': random.choice(campaign_ids),
            'company_or_account': random.choice(sf_data['accounts'])['name'],
            'contact_id': random.choice(sf_data['contacts'])['id'],
            'created_date': format_date(fake.date_time_this_year()),
            'lead_id': '',
            'net_new_lead_c': random.choice(['Yes', 'No']),
            'status': random.choice(['Sent', 'Responded', 'Attended'])
        })

    # Generate opportunities (75 opportunities)
    for i in range(75):
        account = random.choice(sf_data['accounts'])
        opp_id = f"006{i:04d}"
        sf_data['opportunities'].append({
            'id': opp_id,
            'account_id': account['id'],
            'name': f"{account['name']} - {random.choice(['AI Data Expansion', 'Enterprise Renewal', 'New Data Layer'])}",
            'amount': str(random.randint(50000, 2000000)),
            'stage': random.choice(['Discovery', 'Evaluation', 'Negotiation', 'Closed Won', 'Closed Lost']),
            'probability': random.randint(20, 90),
            'close_date': format_date(fake.date_time_between(start_date=START_DATE, end_date="+1y")),
            'owner_id': random.choice([u['id'] for u in users if u['roles'] == 'sales_lead']),
            'created_date': format_date(fake.date_time_this_year())
        })

    # Generate opportunity contact roles (150 roles)
    for i in range(150):
        opp = random.choice(sf_data['opportunities'])
        sf_data['opportunity_contact_roles'].append({
            'id': f"00r{i:04d}",
            'contact_id': random.choice(sf_data['contacts'])['id'],
            'is_primary': random.choice(['Yes', 'No']),
            'opportunity_id': opp['id'],
            'role': random.choice(['Decision Maker', 'Influencer', 'Evaluator'])
        })

    # Generate tasks (300 tasks)
    for i in range(300):
        sf_data['tasks'].append({
            'id': f"00T{i:04d}",
            'activity_date': format_date(fake.date_time_between(start_date=START_DATE, end_date="+30d")),
            'call_disposition': random.choice(['', 'Connected', 'No Answer']),
            'call_type': random.choice(['', 'Outbound', 'Inbound']),
            'completed_date_time': format_datetime(fake.date_time_this_month()) if random.random() < 0.5 else '',
            'description': fake.paragraph(),
            'owner_id': random.choice([u['id'] for u in users]),
            'status': random.choice(['Not Started', 'In Progress', 'Completed']),
            'subject': random.choice(['Data Strategy Review', 'PromptQL Demo', 'Contract Discussion']),
            'task_subtype': random.choice(['Call', 'Email', 'Meeting']),
            'type': 'Task',
            'what_id': random.choice(sf_data['accounts'])['id'],
            'who_id': random.choice(sf_data['contacts'])['id']
        })

    return sf_data

def generate_clari_data(sf_data: Dict[str, List[Dict]], users: List[Dict]) -> Dict[str, List[Dict]]:
    clari_data = {
        'calls': [],
        'call_participants': [],
        'call_transcriptions': [],
        'call_action_items': [],
        'call_topics': []
    }

    # Generate calls (100 calls)
    for i in range(100):
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

        call_time = fake.date_time_between(start_date=START_DATE)
        call_id = f"call{i:04d}"
        clari_data['calls'].append({
            'id': call_id,
            'account_name': account['name'],
            'call_action_items_discussed': fake.sentence(),
            'call_action_items_discussed_embedding': '[0,0,0]',  # Placeholder vector
            'call_full_transcript': fake.paragraph(nb_sentences=5),
            'call_full_transcript_embedding': '[0,0,0]',
            'call_key_takeaways': fake.sentence(),
            'call_key_takeaways_embedding': '[0,0,0]',
            'call_review_page': f"https://clari.com/review/{call_id}",
            'call_summary': fake.paragraph(),
            'call_summary_embedding': '[0,0,0]',
            'call_topics_discussed': "Data Access, AI Insights, Integration",
            'call_topics_discussed_embedding': '[0,0,0]',
            'last_modified_time': format_datetime(call_time + timedelta(minutes=60)),
            'salesforce_account_id': account['id'],
            'salesforce_contact_ids': '{' + ','.join(c['id'] for c in random.sample(sf_data['contacts'], min(3, len(sf_data['contacts'])))) + '}',
            'salesforce_deal_id': opp['id'],
            'source_id': f"zoom_{random.randint(1000, 9999)}",
            'time': format_datetime(call_time),
            'title': f"{account['name']} - {random.choice(['Data Strategy', 'AI Demo', 'Exec Briefing'])}",
            'type': random.choice(['strategy_call', 'demo', 'review'])
        })

        # Generate call participants (2-5 per call)
        num_participants = random.randint(2, 5)
        for j in range(num_participants):
            contact = random.choice(sf_data['contacts'])
            clari_data['call_participants'].append({
                'call_id': call_id,
                'call_person_id': f"{call_id}_part{j}",
                'email': contact['email'],
                'is_organizer': 'True' if j == 0 else 'False',
                'name': f"{contact['first_name']} {contact['last_name']}",
                'person_id': random.randint(1, 1000),
                'user_id': random.choice([u['id'] for u in users])
            })

        # Generate transcriptions (one per participant)
        for j in range(num_participants):
            clari_data['call_transcriptions'].append({
                'call_id': call_id,
                'call_person_id': f"{call_id}_part{j}",
                'end_time': random.uniform(30, 60),
                'person_id': random.randint(1, 1000),
                'start_time': random.uniform(0, 30),
                'text': fake.paragraph(),
                'text_embedding': '[0,0,0]',
                'transcription_id': f"trans_{call_id}_{j}"
            })

        # Generate action items (1-3 per call)
        for j in range(random.randint(1, 3)):
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
    auth_users = generate_auth_data()
    write_to_csv(auth_users, 'postgres/auth_users.csv')

    sf_data = generate_salesforce_data(auth_users)
    for table_name, records in sf_data.items():
        write_to_csv(records, f'postgres/salesforce_{table_name}.csv')

    clari_data = generate_clari_data(sf_data, auth_users)
    for table_name, records in clari_data.items():
        write_to_csv(records, f'pgvector/clari_{table_name}.csv')

    print("CSV files have been generated successfully")

if __name__ == "__main__":
    main()