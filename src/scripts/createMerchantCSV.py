import pandas as pd
import json

# Read the JSON file
with open("merchants.json", "r") as file:
    data = json.load(file)

# Prepare an empty DataFrame with specified columns
newData = pd.DataFrame(columns=['Merchant ID', 'Zipcode', 'Latitude', 'Longitude'])

# Iterating through the JSON data to build the DataFrame
rows = []
for key in data:
    merchantId = int(key)
    zipcode = data[key][0]
    latitude = data[key][1]
    longitude = data[key][2]
    if zipcode is None or zipcode <= 9999:
        zipcode = "NULL"
        latitude = "NULL"
        longitude = "NULL"
    if latitude is None:
        latitude = "NULL"
    if longitude is None:
        longitude = "NULL"
    row = {'Merchant ID': merchantId, 'Zipcode': zipcode, 'Latitude': latitude, 'Longitude': longitude}
    rows.append(row)

# Using concat instead of append
newData = pd.concat([newData, pd.DataFrame(rows)], ignore_index=True)

# Convert JSON to CSV
newData.to_csv('merchants.csv', index=False)

print("Conversion to CSV completed successfully.")
