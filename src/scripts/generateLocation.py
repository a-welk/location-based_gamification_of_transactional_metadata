import json
import pgeocode
import math
import sys

loc = pgeocode.Nominatim('US')

File = open('merchant_zipcodes.json', 'r')
data = json.load(File)


total = len(data)
for i, key in enumerate(data):
    zipcode = data.get(key, None)
    if zipcode.is_integer():
        zipcode = math.floor(zipcode)
        location = loc.query_postal_code(zipcode)
        data[key] = [zipcode, location.latitude, location.longitude]
    else:
        data[key] = [None, None, None]

    # Calculate percentage
    percentage = (i + 1) / total * 100
    sys.stdout.write(f"\rProcessing: {percentage:.2f}%")
    sys.stdout.flush()
print("\n")

with open('merchants.json', 'w') as f:
    json.dump(data, f)


