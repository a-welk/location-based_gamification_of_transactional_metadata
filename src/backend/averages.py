import json

data = json.load(open('zip_summary.json'))

def getAverages(zipcode, month, year):
    try:
        return data[zipcode][year][month]
    except:
        return None
