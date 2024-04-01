import bcrypt
import boto3
import uuid
import json
import operator
#from dotenv import load_dotenv
from decimal import *
from boto3.dynamodb.conditions import Key, Attr
import os
from flask import Flask, jsonify, request, session
from flask_session import Session
from flask_cors import CORS
from decouple import config
from datetime import datetime
import jwt
from functools import wraps

# load_dotenv()
# config = {
#   'accessKey': os.environ.get("accessKey"),
#   'secretKey': os.environ.get("secretKey"),
# }
app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = config('SECRET_KEY')
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

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


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = data['userID']
        except:
            return jsonify({'message': 'Token is invalid!'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

@app.route('/login', methods=['POST'])
def query_user_login():
    email = request.json.get('email')
    password = request.json.get('password')
    table = dynamodb.Table('Users')
    response = table.query(
        IndexName = 'Email-index',
        KeyConditionExpression = Key('Email').eq(email)
    )
    items = response['Items']
    if not items:
        return jsonify({'error': 'User not found', 'status': 404}), 404
    try:
        UserID = items[0]['UserUUID']
        hashed_password = (items[0]['Password'])
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
            session['user_id'] = UserID
            token = jwt.encode({'userID': UserID, 'email': email}, app.config['SECRET_KEY'], algorithm='HS256')
            return jsonify({'token': token}), 200
        else:
            return jsonify({'error': 'Invalid credentials', 'status': 401}), 401
    except IndexError as IE:
          print("Invalid user login credentials")
          return False
           
@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logged out'}), 200

@app.route('/transactions', methods=['GET'])
@token_required
def get_user_transactions(current_user):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Authentication required', 'status': 401}), 401

    user_id = session['user_id']
    transaction_table = dynamodb.Table('Transaction')
    merchant_table = dynamodb.Table('Merchants') 
    data_list = []
    response = transaction_table.query(
        IndexName='UserUUID-index',
        KeyConditionExpression=Key('UserUUID').eq(user_id)
    )
    transactions = response['Items']
    for transaction in transactions:
        response = merchant_table.query(
            KeyConditionExpression=Key('MerchantUUID').eq(transaction['MerchantUUID'])
        )
        merchant = response['Items'][0] if response['Items'] else {}
        data_dict = {
            "transactionID": transaction['TransactionUUID'],
            "transactionAmount": transaction['Amount'],
            "transactionDay": transaction.get('Day', 'N/A'),
            "transactionMonth": transaction.get('Month', 'N/A'),
            "transactionYear": transaction.get('Year', 'N/A'),
            "transactionTime": transaction.get('Time', 'N/A'),
            "transactionMerchantID": transaction['MerchantUUID'],
            "transactionMCC": transaction.get('MCC', 'N/A'),
            "transactionLat": merchant.get('latitude', 'N/A'),
            "transactionLong": merchant.get('longitude', 'N/A'),
            "transactionZipcode": merchant.get('zip', 'N/A'),
        }
        data_list.append(data_dict)

    return jsonify(data_list)

# app.route('/transactions', method=['GET'])
# def get_user_transaction(UserID):
#     merchitems = []
#     data_list = []
#     table = dynamodb.Table('Transaction')
#     response = table.query(
#          IndexName = 'UserUUID-index',
#          KeyConditionExpression = Key('UserUUID').eq(UserID)
#     )
#     items = response['Items']
#     for i in range(len(items)):
#         table = dynamodb.Table('Merchants')
#         response = table.query(
#             KeyConditionExpression = Key('MerchantUUID').eq(items[i]['MerchantUUID'])
#         )
#         merchitems = response['Items']
#         try:
#               thing = merchitems[0]['latitude']
#         except KeyError as ke:
#               merchitems[0]['latitude'] = "N/A"
#         try:
#               thing = merchitems[0]['longitude']
#         except KeyError as ke:
#               merchitems[0]['longitude'] = "N/A"
#         try:
#               thing = merchitems[0]['zip']
#         except KeyError as ke:
#               merchitems[0]['zip'] = "N/A"
#         data_dict = {
#             "transactionID": items[i]['TransactionUUID'],
#             "transactionAmount": items[i]['Amount'],
#             "transactionDay": items[i]['Day'],
#             "transactionMonth": items[i]['Month'],
#             "transactionYear": items[i]['Year'],
#             "transactionTime": items[i]['Time'],
#             "transactionMerchantID": items[i]['MerchantUUID'],
#             "transactionMCC": items[i]['MCC'],
#             "transactionLat": merchitems[0]['latitude'],
#             "transactionLong": merchitems[0]['longitude'],
#             "transactionZipcode": merchitems[0]['zip'],
#         }
#         data_list.append(data_dict)

#     json_data = json.dumps(data_list, separators=(',', ':'), indent=2)

#     with open('output.json', 'w') as json_file:
#         json_file.write(json_data)

#     return data_list

@app.route('/leaderboard', methods=['POST'])
def user_leaderboard():
    zipcode = request.json.get('zipcode')
    leaderboard = []
    table = dynamodb.Table('Users')
    response = table.query(
        IndexName = 'Zipcode-index',
        KeyConditionExpression = Key('Zipcode').eq(zipcode)
    )
    items = response['Items']

    table = dynamodb.Table('Transaction')
    for x in range(len(items)):
        #list = test_transactions(items[x]['UserUUID'])
        list = table.query(
             IndexName = 'UserUUID-index',
             KeyConditionExpression = Key('UserUUID').eq(items[x]['UserUUID'])
        )
        transactions = list['Items']
        total = 0.00
        for y in range(len(transactions)):
                try:
                    amount = transactions[y]['Amount']
                    amount = amount.replace('$', '')
                    total += float(amount)
                except KeyError as ke:
                    total += 0;
        entry = {
             'UserUUID': items[x]['UserUUID'],
             'Name': items[x]['Person'],
             'Total': round(total, 2)
        }
        leaderboard.append(entry)
    leaderboard = sorted(leaderboard, key= operator.itemgetter('Total'))
    return jsonify(leaderboard), 200


@app.route('/monthly_leaderboard', methods=['POST'])
def user_leaderboard_from_month():
    zipcode = request.json.get('zipcode')
    month = datetime.today().month
    year = datetime.today().year
    leaderboard = []
    table = dynamodb.Table('Users')
    response = table.query(
        IndexName = 'Zipcode-index',
        KeyConditionExpression = Key('Zipcode').eq(zipcode)
    )
    items = response['Items']

    table = dynamodb.Table('Transaction')
    for x in range(len(items)):
        list = table.query(
             IndexName = 'UserUUID-index',
             KeyConditionExpression = Key('UserUUID').eq(items[x]['UserUUID'])
        )
        transactions = list['Items']
        total = 0.00
        for y in range(len(transactions)):
            if(transactions[y]['Month'] == str(month) and transactions[y]['Year'] == str(year)):
                try:
                    amount = transactions[y]['Amount']
                    amount = amount.replace('$', '')
                    total += float(amount)
                except KeyError as ke:
                    total += 0;
        entry = {
             'UserUUID': items[x]['UserUUID'],
             'Name': items[x]['Person'],
             'Total': round(total, 2)
        }
        leaderboard.append(entry)
    leaderboard = sorted(leaderboard, key= operator.itemgetter('Total'))
    return leaderboard
    
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

def insert_transaction(amount, card, time, day, month, year, isFraud, MCC, merchantCity, merchantState, merchantID, chip, userID, zipcode):
    amount = str(amount)
    table = dynamodb.Table('Transaction')
    transactionID = uuid.uuid4()
    transactionID = str(transactionID)
    response = table.put_item(
        Item={
            'TransactionUUID': transactionID,
            'Amount': amount,
            'Card': card,
            'Day': day,
            'Is Fraud?': isFraud,
            'MCC': MCC,
            'Merchant City': merchantCity,
            'Merchant State': merchantState,
            'MerchantUUID': merchantID,
            'Month': month,
            'Time': time,
            'Use Chip': chip,
            'UserUUID': userID,
            'Year': year,
            'Zip': zipcode
        }
    )
    status_code = {"status_code": 200}
    return json.dumps(status_code)

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

def user_leaderboard(zipcode):
    leaderboard = []
    table = dynamodb.Table('Users')
    response = table.query(
        IndexName = 'Zipcode-index',
        KeyConditionExpression = Key('Zipcode').eq(zipcode)
    )
    items = response['Items']

    for x in range(len(items)):
        list = get_user_transaction(items[x]['UserUUID'])
        total = 0.00
        for y in range(len(list)):
                try:
                    amount = list[y]['transactionAmount']
                    amount = amount.replace('$', '')
                    total += float(amount)
                except KeyError as ke:
                    total += 0;
        entry = {
             'UserUUID': items[x]['UserUUID'],
             'Name': items[x]['Person'],
             'Total': round(total, 2)
        }
        leaderboard.append(entry)
    leaderboard = sorted(leaderboard, key= operator.itemgetter('Total'))
    return leaderboard


def update_user_password(UserID, password):
     password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
     table = dynamodb.Table('Users')
     response = table.update_item(
          Key={'UserUUID': UserID},
          UpdateExpression = "set #password = :n",
          ExpressionAttributeNames={
               "#password": "Password"
          },
          ExpressionAttributeValues={
               ":n": password
          }
     )

def update_user_income(UserID, income):
     table = dynamodb.Table('Users')
     response = table.update_item(
          Key={'UserUUID': UserID},
          UpdateExpression = "set #income = :n",
          ExpressionAttributeNames={
               "#income": "Yearly Income - Person"
          },
          ExpressionAttributeValues={
               ":n": income
          }
     )
     status_code = {"status_code": 200}
     return (json.dumps(status_code))


def update_user_budget_option(UserID, budget_choice):
     table = dynamodb.Table('Users')
     response = table.update_item(
          Key={'UserUUID': UserID},
          UpdateExpression = "set #budget_choice = :n",
          ExpressionAttributeNames={
               "#budget_choice": "Budget Choice"
          },
          ExpressionAttributeValues={
               ":n": budget_choice
          }
     )

                                
        
        
def main():
    UserID = query_user_login("gunter.welk@gmail.com", "guntersnewpassword!") ##just a sample login
    #get_user_transaction(str(UserID))
    #insert_transaction(44.21, 0, "3:32", 22, 11, 2021, "No", 5541, "Richmond", "VA", 9, "Chip Transaction", 731, 23220)
    
    
if __name__=="__main__":
    app.debug=True
    app.run()
