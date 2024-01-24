import boto3
from flask_cors import CORS
from flask import Flask, jsonify, request, make_response, session
import jwt
from datetime import datetime, timedelta
from functools import wraps
from decouple import config
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb',
                          aws_access_key_id="AKIA42KZIHZE3NIJXCJ2", #insert YOUR aws access key here
                          aws_secret_access_key="ULV7X90uwRxEu72rf4xDCoXmZXltARqt7TJ9zRkx", #insert YOUR aws sec
                          region_name="us-east-1")

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = config('SECRET_KEY')


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
tempBudget = 10000

@app.route('/signup', methods=['POST'])
def query_user_signup():
       data = request.json
       email = data['email']
       password = data['password']
       table = dynamodb.Table('Users')
       response = table.query(
              
       )

@app.route('/login', methods=['POST'])
def query_user_login():
    data = request.json
    email = data['email']
    password = data['password']
    table = dynamodb.Table('Users')
    response = table.query(
        IndexName='Email-index',
        KeyConditionExpression=Key('Email').eq(email)
    )
    items = response['Items']
    if not items:
        return jsonify({'error': 'User not found', 'status': 404}), 404
    if password == items[0]['Password (unhashed)']:
        # return jsonify({'status': '200'})
        userID = int(items[0]['User ID'])
        token = jwt.encode({'userId': userID, 'email': email}, app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({'token': token}), 200
    return jsonify({'error': 'Invalid credentials', 'status': 401}), 401

# def query_user_login():
#     data = request.form
#     email = data.get('email')
#     print(email)
#     password = data.get('password')
#     table = dynamodb.Table('Users')
#     response = table.query(
#         IndexName = 'Email-index',
#         KeyConditionExpression = Key('Email').eq(email)
#     )
#     items = response['Items']
#     UserID = items[0]['User ID']
#     if password == items[0]['Password (unhashed)']:
#         print(f"Successfully logged into {email}")
#         return jsonify({'Status': 'Logged in'})
#     else:
#         print("Invalid user login credentials")
#         return jsonify({'error': 'Invalid user login credentials'}), 401
    
@app.route('/<int:UserID>/transactions', methods=['GET'])
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
    data = {}
    data[UserID] = []
    arr = []
    table = dynamodb.Table('Merchants')
    for page in paginator.paginate(TableName='Transactions',
                                   IndexName = 'User-index',
                                   KeyConditionExpression= Key('User').eq(UserID)):
                                        got_items += page['Items']
                                        this_page = page['Items']
                                        for x in range(len(this_page)):
                                            response = table.query(
                                                KeyConditionExpression = Key('Merchant ID').eq(this_page[x]['Merchant_ID'])
                                            )
                                            items = response['Items']
                                            transaction = {}
                                            transaction[this_page[x]['transaction_id']] = {
                                                    'day' : this_page[x]['Day'],
                                                    'month' : this_page[x]['Month'],
                                                    'year' : this_page[x]['Year'],
                                                    'time' : this_page[x]['Time'],
                                                    'amount' : this_page[x]['Amount'],
                                                    'merchant_id' : this_page[x]['Merchant_ID'],
                                                    'mcc' : this_page[x]['MCC'],
                                                    'latitude' : items[0]['Latitude'],
                                                    'longitude' : items[0]['Longitude'],
                                                    'zipcode' : items[0]['Zipcode']
                                            }
                                            arr.append(transaction)
    data[UserID] = arr
                                            
    return jsonify(data)
    # print(transactionLat)
    # print(transactionLong)
    # print(transactionZipcode)
                                        
def check_budget(UserID): 
    get_user_transaction(UserID)
  
@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    #reference to dynamodb
    table = dynamodb.Table('Transactions')
    try: 
        #getting transaction payload
        transactions_data = request.get_json()
        #adding transaction to dynamodb
        table.append(transactions_data)
        #print message of completition for testing
        return jsonify({"status": "success", "message": "Transaction added successfully"})
    #error handling
    except Exception as E:
        return jsonify({"status": "error", "message": str(E)})

@app.route('/dashboard')
def dashboard():
    token = request.headers.get('Authorization')
    try:
        decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return jsonify({'message': 'Token decoded successfully', 'user': decoded})
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token'}), 401
    
    # return jsonify({'state': 'logged in'}), 200
       
# def main():
    # UserID = query_user_login("Kiera.Allen@gmail.com", "KieraAllen123") just a sample login
    # get_user_transaction(str(UserID))
    
    
if __name__=="__main__":
    app.debug=True
    app.run()
    # main()
