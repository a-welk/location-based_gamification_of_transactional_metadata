import random
import bcrypt
import boto3
import uuid
import json
import operator
from decimal import *
from boto3.dynamodb.conditions import Key, Attr
import os
from flask import Flask, jsonify, make_response, request, redirect, url_for
from flask_cors import CORS
from decouple import config
from datetime import datetime
import jwt
from functools import wraps
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = config('SECRET_KEY')
dynamodb = boto3.resource('dynamodb',
                          aws_access_key_id="", #insert YOUR aws access key here
                          aws_secret_access_key="", #insert YOUR aws sec
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

@app.route('/signup', methods=['POST'])
def user_signup():
    email = request.json.get('email')
    password = request.json.get('password')
    table = dynamodb.Table('Users')
    response = table.query(
        IndexName='Email-index',
        KeyConditionExpression='Email = :email',
        ExpressionAttributeValues={':email': email}
    )
    if response['Items']:
        return jsonify({'error': 'User already exists', 'status': 409}), 409
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    user_id = str(uuid.uuid4())
    table.put_item(
        Item={
            'UserUUID': user_id,
            'Email': email,
            'Password': hashed_password,
        }
    )
    return jsonify({'message': 'User created successfully'}), 201


@app.route('/login', methods=['POST'])
def query_user_login():
    email = request.json.get('email')
    password = request.json.get('password')
    table = dynamodb.Table('Users')
    response = table.query(
        IndexName='Email-index',
        KeyConditionExpression=Key('Email').eq(email)
    )
    items = response['Items']
    if not items:
        return jsonify({'error': 'User not found', 'status': 404}), 404

    try:
        UserID = items[0]['UserUUID']
        hashed_password = items[0]['Password']
        name = items[0]['Person']
        annualIncome = items[0]['Yearly Income - Person']
        budget = float(items[0]['Budget'])
        if(budget == 0):
            budget = float(annualIncome.replace("$", "")) / 12
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
            token = jwt.encode({'userID': UserID, 'email': email, 'name': name, 'budget': budget}, app.config['SECRET_KEY'], algorithm='HS256')
            missing_fields = onboard_check(UserID)
            needOnboarding = any(missing_fields.values())
            response_data = {
                'token': token,
                'needOnboarding': needOnboarding
            }
            response = jsonify(response_data)
            response.set_cookie('user_id', UserID, httponly=True, secure=True)
            return response, 200
        else:
            return jsonify({'error': 'Invalid credentials', 'status': 401}), 401
    except IndexError as IE:
        print("Invalid user login credentials")
        return jsonify({'error': 'Error processing request', 'status': 500}), 500

def onboard_check(user_id):
    table = dynamodb.Table('Users')
    response = table.get_item(Key={'UserUUID': user_id})
    user = response.get('Item', {})

    required_fields = ['Person', 'Current Age', 'Budget', 'Budget Choice', 'Retirement Age', 'Yearly Income - Person', 'Zipcode']
    return {field: user.get(field) is None for field in required_fields}

# Load mcc_codes_data.json
mcc_data = json.load(open('mcc_codes_data.json'))
mcc_business_names = json.load(open('mcc_business_names.json'))
months = {"1" : "January", "2" : "February", "3" : "March", "4" : "April", "5" : "May", "6" : "June", "7" : "July", "8" : "August", "9" : "September", "10" : "October", "11" : "November", "12" : "December"}
@app.route('/getTransactions', methods=['GET'])
def get_user_transaction():
    # Initialize a DynamoDB resource
    dynamodb = boto3.resource('dynamodb',
                              aws_access_key_id='',
                              aws_secret_access_key='',
                              region_name="us-east-1")
    
    # Specify your Transaction and Merchants table names
    transactions_table_name = 'Transactions_New'
    token = None
    auth_header = request.headers.get('Authorization')
    if auth_header:
        token = auth_header.split(" ")[1]
    user_uuid = ""
    if token:
        try:
            decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token', 'status': 401}), 401
        user_uuid = decoded_token.get('userID', None)
        if not user_uuid:
            return jsonify({'error': 'Token for invalid user ', 'status': 401}), 401
    else:
        return jsonify({'error': 'Token not provided', 'status': 401}), 401
    print(user_uuid)
    # Initialize the tables
    transactions_table = dynamodb.Table(transactions_table_name)
    
    transactions = {}

    # Perform the query operation for transactions
    response = transactions_table.query(
        IndexName='UserUUID-index',
        KeyConditionExpression=boto3.dynamodb.conditions.Key('UserUUID').eq(user_uuid)
    )
    transactions = response['Items'][:50]  # Limiting to first 50 transactions for demonstration
    # Sort the transactions by month, day, and time descending
    # Sort the transactions by Year, Month, Day, and Time descending
    # Convert Year, Month, Day, and Time to integers before sorting in descending order
    # Ensure all components are converted to integers for sorting
    transactions = sorted(
        transactions,
        key=lambda x: (
            int(x['Year']),                       # Convert Year to integer
            int(x['Month']),                      # Convert Month to integer
            int(x['Day']),                        # Convert Day to integer
            int(x['Time'].replace(':', ''))       # Convert Time 'HH:MM:SS' to an integer like 133319
        ),
        reverse=True  # Sorting in descending order
    )


    for transaction in transactions:
        mcc = transaction['MCC']
        mcc_data_entry = mcc_data.get(str(mcc))
        transaction_time = transaction['Time']
        # Convert the time to a 12-hour format with AM/PM
        if transaction_time:
            hour, minute, seconds = map(int, transaction_time.split(':'))
            period = 'AM'
            if hour > 12:
                hour -= 12
                period = 'PM'
            hour = str(hour).zfill(2)  # Pad the hour with a leading zero if necessary
            minute = str(minute).zfill(2)  # Pad the minute with a leading zero if necessary
            transaction['Time'] = f'{hour}:{minute} {period}'
        if mcc_data_entry:
            transaction['Merchant Data'] = mcc_data_entry
        transaction['Merchant Name'] = mcc_business_names.get(str(mcc), 'Unknown')[random.randint(0, 2)]
        transaction['Transaction Date'] = f"{months[transaction['Month']]} {transaction['Day']}"
    return jsonify(transactions)        


@app.route('/leaderboard', methods=['POST'])
def user_leaderboard():

    token = request.json.get('token')
    auth_header = request.headers.get('Authorization')
    if auth_header:
        token = auth_header.split(" ")[1]
    user_uuid = ""
    if token:
        try:
            decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            user_uuid = decoded_token['userID']
            # Continue with the rest of the code using the userID
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token', 'status': 401}), 401
    else:
        zipcode = request.json.get('zipcode')
        return jsonify({'error': 'Token not provided', 'status': 401}), 401
    leaderboard = []
    table = dynamodb.Table('Users')

    response = table.query(
        KeyConditionExpression = Key('UserUUID').eq(user_uuid)
    )
    items = response['Items']
    zipcode = items[0]['Zipcode']
    userName = items[0]['Person']

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
                try:
                    amount = transactions[y]['Amount']
                    amount = amount.replace('$', '')
                    total += float(amount)
                except KeyError as ke:
                    total += 0;
        if (items[x]['UserUUID'] == user_uuid):
            entry = {
                'UserUUID': items[x]['UserUUID'],
                'Name': items[x]['Person'],
                'Total': round(total, 2)
            }
        else:
            entry = {
                'UserUUID': items[x]['UserUUID'],
                'Name': 'Anonymous',
                'Total': round(total, 2)
            }
        leaderboard.append(entry)
    leaderboard = sorted(leaderboard, key= operator.itemgetter('Total'))
    return jsonify(leaderboard), 200


@app.route('/monthly_leaderboard', methods=['POST'])
def user_leaderboard_from_month():
    month = request.json.get('selectedMonth')
    year = request.json.get('selectedYear')
    token = request.json.get('token')
    auth_header = request.headers.get('Authorization')
    if auth_header:
        token = auth_header.split(" ")[1]
    print(token)
    user_uuid = ""
    if token:
        try:
            decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            user_uuid = decoded_token['userID']
            # Continue with the rest of the code using the userID
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token', 'status': 401}), 401
    else:
        zipcode = request.json.get('zipcode')
        return jsonify({'error': 'Token not provided', 'status': 401}), 401


    leaderboard = []
    table = dynamodb.Table('Users')

    response = table.query(
        KeyConditionExpression = Key('UserUUID').eq(user_uuid)
    )
    items = response['Items']
    zipcode = items[0]['Zipcode']
    userName = items[0]['Person']
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
        budget = float(items[x]['Budget'])
        total = 0.00
        points = 0
        for y in range(len(transactions)):
            if(transactions[y]['Month'] == str(month) and transactions[y]['Year'] == str(year)):
                try:
                    amount = transactions[y]['Amount']
                    amount = amount.replace('$', '')
                    total += float(amount)
                except KeyError as ke:
                    total += 0;
                points = budget_points(total, budget)
                if (items[x]['UserUUID'] == user_uuid):
                    entry = {
                        'UserUUID': items[x]['UserUUID'],
                        'Name': items[x]['Person'],
                        'Points': round(points, 2)
                    }
                else:
                    entry = {
                        'UserUUID': items[x]['UserUUID'],
                        'Name': 'Anonymous',
                        'Points': round(points, 2)
                    }
            else:
                if (items[x]['UserUUID'] == user_uuid):
                    entry = {
                        'UserUUID': items[x]['UserUUID'],
                        'Name': items[x]['Person'],
                        'Points': round(points, 2)
                    }
                else:
                    entry = {
                        'UserUUID': items[x]['UserUUID'],
                        'Name': 'Anonymous',
                        'Points': round(points, 2)
                    }
            
        leaderboard.append(entry)
    leaderboard = sorted(leaderboard, key= operator.itemgetter('Points'), reverse=True)
    return leaderboard


def budget_points(total, budget):
    points = 0
    ratio = total / budget
    if(ratio <= .1):
        points += 100
    elif(ratio <= .2 and ratio > .1):
        points += 90
    elif(ratio <= .3 and ratio > .2):
         points += 80
    elif(ratio <= .4 and ratio > .3):
         points += 70
    elif(ratio <= .5 and ratio > .4):
         points += 60
    elif(ratio <= .6 and ratio > .5):
         points += 50
    elif(ratio <= .7 and ratio > .6):
         points += 40
    elif(ratio <= .8 and ratio > .7):
         points += 30
    elif(ratio <= .9 and ratio > .8):
         points += 20
    elif(ratio <= 1 and ratio > .9):
         points += 10
    elif(ratio > 1):
         points += 0

    return points

@app.route('/get_monthly_transactions', methods=['GET'])
def get_monthly_transactions():
    token = request.json.get('token')
    auth_header = request.headers.get('Authorization')
    if auth_header:
        token = auth_header.split(" ")[1]
    print(token)
    user_uuid = ""
    budget = 0
    total = 0
    
    if token:
        try:
            decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            user_uuid = decoded_token['userID']
            budget = decoded_token['budget']
            # Continue with the rest of the code using the userID
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token', 'status': 401}), 401
    else:
        zipcode = request.json.get('zipcode')
        return jsonify({'error': 'Token not provided', 'status': 401}), 401


    year = datetime.today().year
    month = datetime.today().month
    total = 0.00
    table = dynamodb.Table('Transaction')
    response = table.query(
        IndexName = 'UserUUID-index',
        KeyConditionExpression = Key('UserUUID').eq(user_uuid),
        FilterExpression = Attr('Year').eq(str(year))
    )
    items = response['Items']
    for item in range(len(items)):
        if(items[item]['Year'] == str(year) and items[item]['Month'] == str(month)):
                try:
                    amount = items[item]['Amount']
                    amount = amount.replace('$', '')
                    total += float(amount)
                except KeyError as ke:
                    total += 0;
        else:
             total += 0
    total_and_budget = {
        'Total': total,
        'Budget': budget
    }
    return jsonify(total_and_budget), 200


def get_monthly_history():
    token = request.json.get('token')
    auth_header = request.headers.get('Authorization')
    if auth_header:
        token = auth_header.split(" ")[1]
    print(token)
    user_uuid = ""
    budget = 0
    total = 0
    
    if token:
        try:
            decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            user_uuid = decoded_token['userID']
            budget = decoded_token['budget']
            # Continue with the rest of the code using the userID
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token', 'status': 401}), 401
    else:
        zipcode = request.json.get('zipcode')
        return jsonify({'error': 'Token not provided', 'status': 401}), 401


    year = datetime.today().year
    month = datetime.today().month
    janTotal = 0.00
    febTotal = 0.00
    marTotal = 0.00
    aprTotal = 0.00
    mayTotal = 0.00
    juneTotal = 0.00
    julyTotal = 0.00
    augTotal = 0.00
    septTotal = 0.00
    octTotal = 0.00
    novTotal = 0.00
    decTotal = 0.00


    table = dynamodb.Table('Transaction')
    response = table.query(
        IndexName = 'UserUUID-index',
        KeyConditionExpression = Key('UserUUID').eq(user_uuid),
        FilterExpression = Attr('Year').eq(str(year))
    )
    items = response['Items']
    for item in range(len(items)):
        if(items[item]['Year'] == str(year) and items[item]['Month'] == '1'):
                try:
                    amount = items[item]['Amount']
                    amount = amount.replace('$', '')
                    janTotal += float(amount)
                except KeyError as ke:
                    janTotal += 0;
        elif(items[item]['Year'] == str(year) and items[item]['Month'] == '2'):
                try:
                    amount = items[item]['Amount']
                    amount = amount.replace('$', '')
                    febTotal += float(amount)
                except KeyError as ke:
                    febTotal += 0;
        elif(items[item]['Year'] == str(year) and items[item]['Month'] == '3'):
                try:
                    amount = items[item]['Amount']
                    amount = amount.replace('$', '')
                    marTotal += float(amount)
                except KeyError as ke:
                    marTotal += 0;
        elif(items[item]['Year'] == str(year) and items[item]['Month'] == '4'):
                try:
                    amount = items[item]['Amount']
                    amount = amount.replace('$', '')
                    aprTotal += float(amount)
                except KeyError as ke:
                    aprTotal += 0;
        elif(items[item]['Year'] == str(year) and items[item]['Month'] == '5'):
                try:
                    amount = items[item]['Amount']
                    amount = amount.replace('$', '')
                    mayTotal += float(amount)
                except KeyError as ke:
                    mayTotal += 0;
        elif(items[item]['Year'] == str(year) and items[item]['Month'] == '6'):
                try:
                    amount = items[item]['Amount']
                    amount = amount.replace('$', '')
                    juneTotal += float(amount)
                except KeyError as ke:
                    juneTotal += 0;
        elif(items[item]['Year'] == str(year) and items[item]['Month'] == '7'):
                try:
                    amount = items[item]['Amount']
                    amount = amount.replace('$', '')
                    julyTotal += float(amount)
                except KeyError as ke:
                    julyTotal += 0;
        elif(items[item]['Year'] == str(year) and items[item]['Month'] == '8'):
                try:
                    amount = items[item]['Amount']
                    amount = amount.replace('$', '')
                    augTotal += float(amount)
                except KeyError as ke:
                    augTotal += 0;
        elif(items[item]['Year'] == str(year) and items[item]['Month'] == '9'):
                try:
                    amount = items[item]['Amount']
                    amount = amount.replace('$', '')
                    septTotal += float(amount)
                except KeyError as ke:
                    septTotal += 0;
        elif(items[item]['Year'] == str(year) and int(items[item]['Month']) == '10'):
                try:
                    amount = items[item]['Amount']
                    amount = amount.replace('$', '')
                    octTotal += float(amount)
                except KeyError as ke:
                    octTotal += 0;
        elif(items[item]['Year'] == str(year) and items[item]['Month'] == '11'):
                try:
                    amount = items[item]['Amount']
                    amount = amount.replace('$', '')
                    novTotal += float(amount)
                except KeyError as ke:
                    novTotal += 0;
        elif(items[item]['Year'] == str(year) and items[item]['Month'] == '12'):
                try:
                    amount = items[item]['Amount']
                    amount = amount.replace('$', '')
                    decTotal += float(amount)
                except KeyError as ke:
                    decTotal += 0;
    total_and_budget = {
        'Jan': round(janTotal, 2),
        'Feb': round(febTotal, 2),
        'Mar': round(marTotal, 2),
        'Apr': round(aprTotal, 2),
        'May': round(mayTotal, 2),
        'Jun': round(juneTotal, 2),
        'Jul': round(julyTotal, 2),
        'Aug': round(augTotal, 2),
        'Sep': round(septTotal, 2),
        'Oct': round(octTotal, 2),
        'Nov': round(novTotal, 2),
        'Dec': round(decTotal, 2),
        'Budget': budget
    }
    return jsonify(total_and_budget), 200

    
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

@app.route('/update_budget_option', methods=['POST'])
def update_user_budget_option():
    token = request.json.get('token')
    budget_choice = request.json.get('budgetChoice')
    auth_header = request.headers.get('Authorization')
    if auth_header:
        token = auth_header.split(" ")[1]
    user_uuid = ""
    if token:
        try:
            decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            user_uuid = decoded_token['userID']
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token', 'status': 401}), 401
    else:
        return jsonify({'error': 'Token not provided', 'status': 401}), 401
    table = dynamodb.Table('Users')
    response = table.update_item(
        Key={'UserUUID': user_uuid},
        UpdateExpression = "set #budget_choice = :n",
        ExpressionAttributeNames={
            "#budget_choice": "Budget Choice"
        },
        ExpressionAttributeValues={
            ":n": budget_choice
        }
    )


json_data = json.load(open('zip_summary.json'))
@app.route('/getAverages', methods=['GET'])
def getAverages():
    zipcode = request.args.get('zipcode')
    month = request.args.get('month')
    year = request.args.get('year')
    zipcode_data = json_data[str(zipcode)]
    date = f'{month}/{year}'
    returnData = {}
    if zipcode_data.get(date, None):
        date_data = zipcode_data[date]
        for key in date_data.keys():
            returnData[key] = {'User Average': (date_data[key] * random.uniform(0.8, 1.2)), 'Community Average': date_data[key], 'User Target': round((date_data[key] * random.uniform(0.8, 1.2)), 0), 'Community Target': (date_data[key] * random.uniform(0.8, 1.2))}
    else:
        returnData = {'error': 'No data for this date', 'status': 404}
    return returnData                              

        
        
def main():
    UserID = query_user_login("gunter.welk@gmail.com", "guntersnewpassword!") ##just a sample login
    #get_user_transaction(str(UserID))
    #insert_transaction(44.21, 0, "3:32", 22, 11, 2021, "No", 5541, "Richmond", "VA", 9, "Chip Transaction", 731, 23220)
    
    
if __name__=="__main__":
    app.debug=True
    app.run()
