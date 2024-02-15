import boto3
import uuid
import os
import json
#from dotenv import load_dotenv
from decimal import *
from boto3.dynamodb.conditions import Key, Attr
dynamodb = boto3.resource('dynamodb',
                          aws_access_key_id="AKIA42KZIHZE3NIJXCJ2", #insert YOUR aws access key here
                          aws_secret_access_key="ULV7X90uwRxEu72rf4xDCoXmZXltARqt7TJ9zRkx", #insert YOUR aws sec
                          region_name="us-east-1")
# Global Transaction table variables
transactionID = [] 
userTransactions = []
transactionYear = []
transactionMonth = []
transactionDay = []
transactionTime = []
transactionAmount = []
transactionMerchantID = []
transactionMCC = []
transactionLat = []
transactionLong = []
transactionZipcode = []
items = []

#queries the user table given an email and password and determines if the password is correct - need to add code for cases where email is not found
def query_user_login(email, password):
    table = dynamodb.Table('Users')
    response = table.query(
        IndexName = 'Email-index',
        KeyConditionExpression = Key('Email').eq(email)
    )
    items = response['Items']
    UserID = items[0]['UserUUID']
    if password == items[0]['Password']:
        print(f"Successfully logged into {email}")
        return UserID
    else:
        print("Invalid user login credentials")
        return False
    
#queries transactions table for all the transactions of a given userID
def get_user_transaction(UserID):
    #attempt at pagination in order to retrieve ALL the transactions from designated user
    got_items = []
    paginator = dynamodb.meta.client.get_paginator('query')
    for page in paginator.paginate(TableName='Transactions',
                                   IndexName = 'UserUUID-index',
                                   KeyConditionExpression= Key('UserUUID').eq(UserID)):
                                        got_items += page['Items']
                                        this_page = page['Items']
                                        for x in range(len(this_page)):
                                            userTransactions.append(this_page[x]['TransactionUUID'])
                                            transactionYear.append(this_page[x]['Year'])
                                            transactionMonth.append(this_page[x]['Month'])
                                            transactionDay.append(this_page[x]['Day'])
                                            transactionTime.append(this_page[x]['Time'])
                                            transactionAmount.append(this_page[x]['Amount'])
                                            transactionMerchantID.append(this_page[x]['MerchantUUID'])
                                            transactionMCC.append(this_page[x]['MCC'])
    #gets merchant information for each merchantID in each transaction                                        
    for x in range(len(transactionMerchantID)):
        table = dynamodb.Table('Merchants')
        response = table.query(
            KeyConditionExpression = Key('MerchantUUID').eq(transactionMerchantID[x])
        )
        items.extend(response['Items'])
    
    #adds each merchant attribute to their respective list
    for x in range(len(items)):
        try:
            transactionLat.append(items[x]['latitude'])
        except KeyError as ke:
            transactionLat.append("N/A")
        
        try:
            transactionLong.append(items[x]['longitude'])
        except KeyError as ke:
            transactionLong.append("N/A")
        
        try:
            transactionZipcode.append(items[x]['zip'])
        except KeyError as ke:
            transactionZipcode.append("N/A")
        
    #formats all transaction data and puts it into output.json
    zipped = list(zip(userTransactions, transactionAmount, transactionDay, transactionMonth, transactionYear, transactionTime, transactionMerchantID, transactionMCC, transactionLat, transactionLong, transactionZipcode))
    json_data = ',\n'.join(json.dumps(t, separators=(',', ':')) for t in zipped)
    with open('output.json', 'w') as json_file:
        json_file.write(json_data)
                                  
"""
    print(transactionAmount)
    print(transactionTime)
    print(transactionDay)
    print(transactionMonth)
    print(userTransactions)
    print(transactionMerchantID)
    print(transactionMCC)
    print(transactionLat)
    print(transactionLong)
    print(transactionZipcode)"""
    
#inserts a new transaction into the transaction table
def insert_transaction(amount, card, time, day, month, year, isFraud, MCC, merchantCity, merchantState, merchantID, chip, userID, zipcode):
    amount = str(amount)
    userID = str(userID)
    table = dynamodb.Table('Transactions')
    transactionID = uuid.uuid4()
    response = table.put_item(
        Item={
            'transaction_id': transactionID,
            'Amount': amount,
            'Card': card,
            'Day': day,
            'Is Fraud?': isFraud,
            'MCC': MCC,
            'Merchant City': merchantCity,
            'Merchant State': merchantState,
            'Merchant_ID': merchantID,
            'Month': month,
            'Time': time,
            'Use Chip': chip,
            'User': userID,
            'Year': year,
            'Zip': zipcode
        }
    )

#inserts new users into Users table
def insert_user(address, apartment, birthMonth, birthYear, city, age, email, FICOscore, gender, lat, long, numCards, password, perCapitaIncome, name, retirementAge, state, debt, annualIncome, zipcode):
    table = dynamodb.Table('Users')
    """
    client = boto3.client('dynamodb', aws_access_key_id='AKIA42KZIHZE3NIJXCJ2', aws_secret_access_key='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', region_name='us-east-1')
    response = client.describe_table(TableName='Users')
    userID = response['Table']['ItemCount']
    userID = userID + 1
    """
    userID = uuid.uuid4()
    response = table.put_item(
        Item={
            'UserUUID': userID,
           'Address': address,
           'Apartment': apartment,
           'Birth Month': birthMonth,
           'Birth Year': birthYear,
           'City': city,
           'Current Age': age,
           'Email': email,
           'FICO Score': FICOscore,
           'Gender': gender,
           'Latitude': lat,
           'Longitude': long,
           'Nume Credit Cards': numCards,
           'Password (unhashed)': password,
           'Per Capita Income - Zipcode': perCapitaIncome,
           'Person': name,
           'Retirement Age': retirementAge,
           'State': state,
           'Total Debt': debt,
           'Yearly Income - Person': annualIncome,
           'Zipcode': zipcode
        }
    )     
        
        
def main():
    #UserID = query_user_login("Emerson.Rogers@gmail.com", "EmersonRogers123") #just a sample login
    #UserID = 2001
    get_user_transaction("1c146799-2c2c-4a93-9dea-7936ae9c3f41")
    #insert_transaction(44.25, 0, "3:32", 22, 11, 2021, "No", 5541, "Richmond", "VA", 9, "Chip Transaction", 2011, 23220)
    #insert_user("1411 Grove Ave", "11", "August", "2001", "Richmond", 22, "welka@vcu.edu", 750, "male", "37.54873869465798", "37.54873869465798, -77.45798251781274", 
                #2, "AlexWelk123", 10000, "Alex Welk", 70, "VA", 0, 10000, 23220)

    
    
if __name__=="__main__":
    main()