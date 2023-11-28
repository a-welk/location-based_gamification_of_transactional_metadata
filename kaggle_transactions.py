'''
Program is used to add more details to the transactions from Kaggle
The main program adds a few attributes to the transactions have unique identifiers for each transaction they are
    1. Add Card number to each transaction from the provided cards csv by converting it to a json format
    2. Get Person name for each transaction using the user index given  and getting names from csv file
    3. Generating Latitude and Longitude from
'''
import os.path
import pandas as pd
import json
import pgeocode

# Convert cards csv file to json file to be later loaded in as dictionary
class GenerateCardsJson:
    def generateCardsJsonFile(self):
        # Read cards csv
        cardsFIle = pd.read_csv('sd254_cards.csv')
        cards = {}
        # loop through the rows using iterrows()
        for index, row in cardsFIle.iterrows():
            card_number = row['Card Number']
            user = row['User']
            card_index = row['CARD INDEX']
            card_brand = row['Card Brand']
            card_type = row['Card Type']
            expiration_date = row['Expires']
            CVV = row['CVV']
            has_chip = row['Has Chip']
            cards_issued = row['Cards Issued']
            credit_limit = row['Credit Limit']
            date_opened = row['Acct Open Date']
            pin_last_changed_year = row['Year PIN last Changed']
            card_on_dark_web = row['Card on Dark Web']
            cards[f'{user}-{card_index}'] = [user, card_index, card_brand, card_type, card_number, expiration_date, CVV,
                                             has_chip, cards_issued, date_opened, pin_last_changed_year, card_on_dark_web]
        json_file = open("cards.json", "w")
        json.dump(cards, json_file)

class AddCardNumbers():
    def get_lat_lon_from_zip(self, zip_code):
        nomi = pgeocode.Nominatim('us')
        query = nomi.query_postal_code(zip_code)
        data = {
            "lat": query["latitude"],
            "lon": query["longitude"]
        }
        return data['lat'], data['lon']
    
    def addCardNumber(self, transactions):
        print("Adding Card Numbers")
        total_rows = len(transactions)
        current_row = 0
        cards_file = open("cards.json", "r")
        cards = json.load(cards_file)
        users_file = pd.read_csv("sd254_users.csv")
        MerchantLocationIDFile = "MerchantLocationID.json"
        merchantLocIdFile = open(MerchantLocationIDFile, "r")
        merchantLocIdJson = json.load(merchantLocIdFile)
        transactions.insert(3, column="Card Number", value=0)
        person_values = []
        merchantLocIDData = []
        transaction_id = []
        card_number_data = []
        transactions.insert(0, column="Transaction ID", value=0)
        transactions.insert(2, column="Person", value=0)
        transactions.insert(14, column="MerchantLocationID", value=0)

        id_count = 0
        for index, row in transactions.iterrows():
            user = row['User']
            card_index = row['Card']
            card_data = cards.get(f'{user}-{card_index}', 0)
            card_number = 0
            if len(card_data) > 1:
                card_number = card_data[4]
            else:
                card_number = 0
            card_number_data.append(card_number)
            transaction_id.append(id_count)
            id_count += 1
            
            user = row['User']
            person = users_file['Person'].get(user, 0)
            person_values.append(person)
            current_row += 1
            percentage_complete = (current_row / total_rows) * 100
            print(f'\r{percentage_complete:.2f}% complete', end='', flush=True)

            merchantName = str(row['Merchant Name'])
            merchantLocID = merchantLocIdJson.get(merchantName, "")
            if merchantLocID == "":
                print(f'{merchantName} location id can\'t be found in {MerchantLocationIDFile}')
            merchantLocIDData.append(merchantLocID)
        transactions['Transaction ID'] = transaction_id
        transactions['Person'] = person_values
        transactions['Card Number'] = card_number_data
        transactions['LocationID'] = merchantLocIDData
        print()
        transactions.head()
        return transactions
        #transactions_file = open("Transactions.csv", "w")
        #transactions.to_csv(transactions_file, index=False)


if __name__ == "__main__":
    if not(os.path.exists("cards.json")):
        GenerateCardsJsonFile = GenerateCardsJson()
        GenerateCardsJsonFile.generateCardsJsonFile()
    transactions = pd.read_csv("User0_credit_card_transactions.csv")
    AddCardNumbersToTable = AddCardNumbers()
    transactions = AddCardNumbersToTable.addCardNumber(transactions)
    print("Done")
    # AddPersonsNameToTable = AddPersonsName()
    # transactions = AddPersonsNameToTable.addNames(transactions)
    # print("Done Adding Persons Name")
    # AddCoordinatesToTable = AddCoordinates()
    # transactions = AddCoordinatesToTable.main(transactions)
    # print("Done Adding Coordinates")
    transactions.to_csv("Transactions_Partial.csv", index=False)
    
