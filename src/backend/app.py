from flask import Flask, render_template, request, jsonify
from src import getTransactionId, main
import boto3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/addTransaction', methods=['POST'])
def addTransaction():
       
    try:
        data = request.json
        user = data.get('user')
        personName = data.get('person')
        year = data.get('year')
        cardNumber = data.get('cardNumber')
        month = data.get('month')
        day = data.get('day')
        time = data.get('time')
        amount = data.get('amount')
        useChip = data.get('useChip')
        merchantName = data.get('merchantName')
        merchantCity = data.get('merchantCity')
        merchantState = data.get('merchantState')
        merchantLocId = data.get('merchantLocationID')
        zipcode = data.get('zipcode')
        mcc = data.get('mcc')
        errors = data.get('errors')
        isFraud = data.get('isFraud')
    except:
        jsonify({"Missing Data"}), 401

    highestTransactionID = getTransactionId.getHighestTransactionID()+ 1
    return jsonify(), main.addTransactionToTable(highestTransactionID, user, personName, cardNumber, year, month, day, time, amount, useChip, merchantName, merchantCity, merchantState, merchantLocId, zipcode, mcc, errors, isFraud)

@app.route('/getTransactions', methods=['GET'])
def get_user_transaction():
    # Initialize a DynamoDB resource
    dynamodb = boto3.resource('dynamodb',
                              aws_access_key_id='AKIA42KZIHZE3NIJXCJ2',
                              aws_secret_access_key='ULV7X90uwRxEu72rf4xDCoXmZXltARqt7TJ9zRkx',
                              region_name="us-east-1")
    
    # Specify your Transaction table name
    transactions_table_name = 'Transactions'

    # Extract the token
    token = request.headers.get('Authorization', '').split(' ')[-1]
    if not token:
        return jsonify({'error': 'Token not provided', 'status': 401}), 401

    try:
        decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        user_uuid = decoded_token['userID']
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token', 'status': 401}), 401

    # Extract month and year from query parameters
    month = request.args.get('month')
    year = request.args.get('year')

    # Initialize the transactions table
    transactions_table = dynamodb.Table(transactions_table_name)

    try:
        # Construct the query condition
        key_condition = Key('UserUUID').eq(user_uuid)
        if month and year:
            key_condition = And(key_condition, Key('Month').eq(month), Key('Year').eq(year))

        # Perform the query operation for transactions
        response = transactions_table.query(
            IndexName='UserUUID-index',  # Adjusted GSI name
            KeyConditionExpression=key_condition
        )

        transactions = response['Items'][:50]  # Limiting to first 50 transactions for demonstration

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify(transactions)


if __name__ == '__main__':
    
    app.run(debug=True, port=5000)