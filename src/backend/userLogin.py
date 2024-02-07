import boto3
import os
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


def query_user_login(email, password):
   # email = request.form['email']
   # password = request.form['password']
    
    table = dynamodb.Table('Users')
    response = table.query(
        IndexName = 'Email-index',
        KeyConditionExpression = Key('Email').eq(email)
    )
    items = response['Items']
    UserID = items[0]['User ID']
    if password == items[0]['Password (unhashed)']:
        print(f"Successfully logged into {email}")
        return UserID
    else:
        print("Invalid user login credentials")
        return False
    
    
def get_user_transaction(UserID):
    
    """
    table = dynamodb.Table('Transactions')
    response = table.query(
        IndexName = 'User-index',
        KeyConditionExpression = Key('User').eq(UserID)
        )
    items = response['Items']
    print(items) ##printing an empty list so something is probably wrong with the original query but idk what
  """
    ##attempt at pagination in order to retrieve ALL the transactions from designated user
    got_items = []
    paginator = dynamodb.meta.client.get_paginator('query')
    for page in paginator.paginate(TableName='Transactions',
                                   IndexName = 'User-index',
                                   KeyConditionExpression= Key('User').eq(UserID)):
                                        got_items += page['Items']
                                        this_page = page['Items']
                                        for x in range(len(this_page)):
                                            userTransactions.append(this_page[x]['transaction_id'])
                                            transactionYear.append(this_page[x]['Year'])
                                            transactionMonth.append(this_page[x]['Month'])
                                            transactionDay.append(this_page[x]['Day'])
                                            transactionTime.append(this_page[x]['Time'])
                                            transactionAmount.append(this_page[x]['Amount'])
                                            transactionMerchantID.append(this_page[x]['Merchant_ID'])
                                            transactionMCC.append(this_page[x]['MCC'])
                                            
    for x in range(len(transactionMerchantID)):
        table = dynamodb.Table('Merchants')
        response = table.query(
            KeyConditionExpression = Key('Merchant ID').eq(transactionMerchantID[x])
        )
        items.append(response['Items'])
        print(response['Items'])

    for x in range(len(items)):
        transactionLat.append(items[x]['Latitude'])
        transactionLong.append(items[x]['Longitude'])
        transactionZipcode.append(items[x]['Zipcode'])
                                  

    print(transactionAmount)
    print(transactionTime)
    print(transactionDay)
    print(transactionMonth)
    
    print(userTransactions)
    print(transactionMerchantID)
    print(transactionMCC)
    print(transactionLat)
    print(transactionLong)
    print(transactionZipcode)
    
def insert_transaction(amount, card, time, day, month, year, isFraud, MCC, merchantCity, merchantState, merchantID, chip, userID, zipcode):
    amount = str(amount)
    userID = str(userID)
    table = dynamodb.Table('Transactions')
    """
    response = table.scan(
        Select='COUNT'
    )
    -----------------------------------------
    client = boto3.client('dynamodb', aws_access_key_id='AKIA42KZIHZE3NIJXCJ2', aws_secret_access_key='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', region_name='us-east-1')
    response = client.describe_table(TableName='Transactions')
    max = response['Table']['ItemCount']
    ------------------------------------------- 
    response = table.update_item(
        Key={'pk': 'transaction_id'},
        UpdateExpression="ADD #cnt :val",
        ExpressionAttributeNames={'#cnt': 'count'},
        ExpressionAttributeValues={':val': 1},
        ReturnValues="UPDATED_NEW"
    )
    """
    
    max = response['Attributes']['count']
    response = table.put_item(
        Item={
            'transaction_id': str(max),
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
    
def insert_user(address, apartment, birthMonth, birthYear, city, age, email, FICOscore, gender, lat, long, numCards, password, perCapitaIncome, name, retirementAge, state, debt, annualIncome, zipcode):
    table = dynamodb.Table('Users')
    client = boto3.client('dynamodb', aws_access_key_id='AKIA42KZIHZE3NIJXCJ2', aws_secret_access_key='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', region_name='us-east-1')
    response = client.describe_table(TableName='Users')
    userID = response['Table']['ItemCount']
    userID = userID + 1
    response = table.put_item(
        Item={
            'User ID': userID,
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
    #UserID = query_user_login("Kiera.Allen@gmail.com", "KieraAllen123") ##just a sample login
    #UserID = 2011
    #get_user_transaction(str(UserID))
    #insert_transaction(44.25, 0, "3:32", 22, 11, 2021, "No", 5541, "Richmond", "VA", 9, "Chip Transaction", 2011, 23220)
    insert_user("1411 Grove Ave", "11", "August", "2001", "Richmond", 22, "welka@vcu.edu", 750, "male", "37.54873869465798", "37.54873869465798, -77.45798251781274", 
                2, "AlexWelk123", 10000, "Alex Welk", 70, "VA", 0, 10000, 23220)

    
    
if __name__=="__main__":
    main()