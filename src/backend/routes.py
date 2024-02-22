import json
import uuid
import bcrypt
import boto3
#from dotenv import load_dotenv
from decimal import *
from boto3.dynamodb.conditions import Key, Attr
import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from decouple import config
import jwt

# load_dotenv()
# config = {
#   'accessKey': os.environ.get("accessKey"),
#   'secretKey': os.environ.get("secretKey"),
# }
app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = config('SECRET_KEY')

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
@app.route('/login', methods=['POST'])
def query_user_login():
    email = request.json.get('email')
    password = request.json.get('password')
    table = dynamodb.Table('Users')
    response = table.query(
        IndexName = 'Email-index',
        KeyConditionExpression = Key('Email').eq(email)
    )
    try:
        items = response['Items']
        UserID = items[0]['UserUUID']
        hashed_password = (items[0]['Password'])
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
            token = jwt.encode({'userID': UserID, 'email': email}, app.config[SECRET_KEY], algorithm='HS256')
            return jsonify({'success': True, 'token': token, 'message': 'Login successful'}), 200

        else:
            return jsonify({'success': False, 'message': 'Invalid credentials'})
    except IndexError as IE:
          return jsonify({'success': False, 'message': 'Invalid credentials'})
    
    
#queries transactions table for all the transactions of a given userID - not working rn bc of UserUUID disputes
def get_user_transaction(UserID):
    #attempt at pagination in order to retrieve ALL the transactions from designated user
    paginator = dynamodb.meta.client.get_paginator('query')
    for page in paginator.paginate(TableName='Transactions',
                                   IndexName = 'UserUUID-index',
                                   KeyConditionExpression= Key('UserUUID').eq(UserID)):
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
    data_list = []

    for i in range(len(userTransactions)):
        data_dict = {
            "transactionID": userTransactions[i],
            "transactionAmount": transactionAmount[i],
            "transactionDay": transactionDay[i],
            "transactionMonth": transactionMonth[i],
            "transactionYear": transactionYear[i],
            "transactionTime": transactionTime[i],
            "transactionMerchantID": transactionMerchantID[i],
            "transactionMCC": transactionMCC[i],
            "transactionLat": transactionLat[i],
            "transactionLong": transactionLong[i],
            "transactionZipcode": transactionZipcode[i],
        }

        data_list.append(data_dict)

    json_data = json.dumps(data_list, separators=(',', ':'), indent=2)

    with open('output.json', 'w') as json_file:
        json_file.write(json_data)
    
#inserts new users into Users table
def insert_user(address, apartment, birthMonth, birthYear, city, age, email, FICOscore, gender, lat, long, numCards, password, perCapitaIncome, name, retirementAge, state, debt, annualIncome, zipcode):
    table = dynamodb.Table('Users')
    password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    userID = uuid.uuid4()
    userID = str(userID)
    response = table.put_item(
        Item={
            'UserUUID': userID,
            'Password': password,
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
            'Per Capita Income - Zipcode': perCapitaIncome,
            'Person': name,
            'Retirement Age': retirementAge,
            'State': state,
            'Total Debt': debt,
            'Yearly Income - Person': annualIncome,
            'Zipcode': zipcode
        }
    )

#inserts new user with just inboarding information
def insert_user_onboarding(email, password, age, retirement_age, annual_income, zipcode, budget, budget_choice):
    table = dynamodb.Table('Users')
    password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    userID = str(uuid.uuid4())
    response = table.put_item(
         Item={
              'UserUUID': userID,
              'Email': email,
              'Password': password,
              'Current Age': age,
              'Retirement Age': retirement_age,
              'Yearly Income - Person': annual_income,
              'Zipcode': zipcode,
              'Budget': budget,
              'Budget Choice': budget_choice
         }
    )

#inserts card with every attribute
def insert_card(date_open, brand, card_index, card_number, dark_web, type, cards_issued, credit_limit, CVV, expiration, has_chip, UserUUID, pin_last_changed):
      table = dynamodb.Table('Cards')
      cardUUID = str(uuid.uuid4())
      response = table.put_item(
            Item={
               'CardUUID': cardUUID,
               'Acct Open Date': date_open,
               'Card Brand': brand,
               'CARD INDEX': card_index,
               'Card Number': card_number,
               'Card on Dark Web': dark_web,
               'Card Type': type,
               'Cards Issued': cards_issued,
               'Credit Limit': credit_limit,
               'CVV': CVV,
               'Expires': expiration,
               'Has Chip': has_chip,
               'USERUUID': UserUUID,
               'Year PIN last Changed': pin_last_changed
            }
      )

#gets all the cards for a given UserID
def get_user_cards(UserID):
     table = dynamodb.Table('Cards')
     response = table.query(
          IndexName = 'USERUUID-index',
          KeyConditionExpression = Key('USERUUID').eq(UserID)
     )
     items = response['Items']
     print(items)

#inserts merchants into merchants table
def insert_merchant(latitude, longitude, zipcode):
    table = dynamodb.Table('Merchants')
    merchantUUID = uuid.uuid4()
    merchantUUID = str(merchantUUID)
    response = table.put_item(
        Item={
            'MerchantUUID': merchantUUID,
            'latitude': latitude,
            'longitude': longitude,
            'zip': zipcode
          }
    )
                                        
        
        
def main():
    UserID = query_user_login("gunter.welk@gmail.com", "GunterWelk123") ##just a sample login
    #get_user_transaction(str(UserID))
    #insert_transaction(44.21, 0, "3:32", 22, 11, 2021, "No", 5541, "Richmond", "VA", 9, "Chip Transaction", 731, 23220)
    
    
if __name__=="__main__":
    app.debug=True
    app.run()
    #main()
