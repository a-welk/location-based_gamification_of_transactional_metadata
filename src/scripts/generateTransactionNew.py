import pandas as pd
import numpy as np
import json
import random
import uuid
from datetime import datetime, timedelta

# Constants
START_DATE = datetime(2024, 1, 1)
END_DATE = datetime(2024, 4, 26)
TRANSACTIONS_PER_USER = 100
USERS_PER_ZIP = 10
TOTAL_TRANSACTIONS = 1000000  # You can adjust this number as long as it meets the minimum requirements

# Load users
with open('users.json', 'r') as file:
    users_data = json.load(file)
    user_uuids = list(users_data.values())  # Extract all UUIDs, which are the values of the dictionary

# Load MCC codes
with open('mcc_codes.json', 'r') as file:
    mcc_data = json.load(file)
    mcc_list = [item['mcc'] for item in mcc_data]  # List comprehension to extract all MCC codes

# Load US Cities with Zip codes
with open('USCities.json', 'r') as file:
    zip_data = json.load(file)
    zip_choices = random.sample(zip_data, k=len(zip_data))  # Shuffle to randomize ZIP code assignment
    zip_info = {
        z['zip_code']: {
            'city': z['city'],
            'state': z['state'],
            'latitude': z['latitude'],
            'longitude': z['longitude'],
            'users': random.sample(user_uuids, k=USERS_PER_ZIP)  # Assign 10 unique users per ZIP code
        } for z in zip_choices if len(user_uuids) >= USERS_PER_ZIP
    }

# Helper functions
def random_date(start, end):
    """Generate a random datetime between `start` and `end`."""
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + timedelta(seconds=random_second)

def generate_amount(mcc_code):
    """Generate a believable transaction amount based on MCC."""
    mcc_item = next((item for item in mcc_data if item['mcc'] == mcc_code), None)
    description = mcc_item['irs_description'] if mcc_item else 'Miscellaneous'
    if 'Grocery' in description:
        return round(random.uniform(30, 150), 2)
    elif 'Fast Food' in description:
        return round(random.uniform(10, 40), 2)
    elif 'Restaurant' in description:
        return round(random.uniform(20, 200), 2)
    else:
        return round(random.uniform(50, 1000), 2)

def generate_transaction(user_uuid, zip_code):
    date_time = random_date(START_DATE, END_DATE)
    mcc = random.choice(mcc_list)
    zip_details = zip_info[zip_code]
    return {
        'TransactionUUID': str(uuid.uuid4()),
        'Amount': generate_amount(mcc),
        'Card': random.randint(0, 3),
        'Day': date_time.day,
        'Errors?': random.choice([None, 'Insufficient Balance', None, None, None]), # 20% chance of minor error
        'Is Fraud?': False if random.random() > 0.01 else True,  # 1% chance of fraud
        'MCC': mcc,
        'Merchant City': zip_details['city'],
        'Merchant State': zip_details['state'],
        'Merchant Latitude': zip_details['latitude'],
        'Merchant Longitude': zip_details['longitude'],
        'Month': date_time.month,
        'Time': date_time.strftime('%H:%M:%S'),
        'Use Chip': random.choice([True, False]),
        'UserUUID': user_uuid,
        'Year': date_time.year,
        'Zip': zip_code
    }

# Generate data ensuring minimum requirements
transactions = []
for zip_code, details in zip_info.items():
    for user in details['users']:
        for _ in range(TRANSACTIONS_PER_USER):
            transactions.append(generate_transaction(user, zip_code))

# Convert to DataFrame
df_transactions = pd.DataFrame(transactions)

# Ensure we have at least the required number of transactions
assert len(transactions) >= TOTAL_TRANSACTIONS, "Total transactions are less than the minimum required."

# Save to CSV
df_transactions.to_csv('transactions.csv', index=False)
print(f"Generated {len(transactions)} transactions.")
