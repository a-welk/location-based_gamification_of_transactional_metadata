import cudf
import cupy as cp
import json


# Read the CSV files using cuDF
df = cudf.read_csv('credit_card_transactions-ibm_v2.csv')
cards = cudf.read_csv('sd254_cards.csv')

# Find the highest index for each user where Card_Number is not NaN
max_index_per_user = cards.groupby('User')['CARD INDEX'].idxmax()

# Creating a new column 'Merchant_ID' based on 'Merchant Name'
merchant_id_map = {merchant: index for index, merchant in enumerate(df['Merchant Name'].unique().to_arrow().to_pylist())}
df['Merchant_ID'] = df['Merchant Name'].map(merchant_id_map)

# Create a dictionary to store unique merchants and their zip codes
merchant_zip_dict = {}

# Iterate over each row in the DataFrame
for row in df.to_pandas().itertuples():
    merchant_name = row._asdict()['Merchant_ID']
    zip_code = row._asdict()['Zip']
    
    # Add merchant to dictionary if it doesn't exist
    if merchant_name not in merchant_zip_dict:
        merchant_zip_dict[merchant_name] = zip_code

# Save the merchant_zip_dict to a JSON file
with open('merchant_zipcodes.json', 'w') as f:
    json.dump(merchant_zip_dict, f)

print("Done")
