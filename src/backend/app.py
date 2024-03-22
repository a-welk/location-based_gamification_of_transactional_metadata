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
    
    # Specify your Transaction and Merchants table names
    transactions_table_name = 'Transaction'
    merchants_table_name = 'Merchants'
    
    # Initialize the tables
    transactions_table = dynamodb.Table(transactions_table_name)
    merchants_table = dynamodb.Table(merchants_table_name)
    
    # Specify the UserUUID you're querying for
    user_uuid = "b47522dd-2dc9-4ae9-a4cc-76d57afb3602"
    
    try:
        # Perform the query operation for transactions
        response = transactions_table.query(
            IndexName='UserUUID-index',  # Use the exact name of your GSI
            KeyConditionExpression=boto3.dynamodb.conditions.Key('UserUUID').eq(user_uuid)
        )
        
        transactions = response['Items'][:50]  # Limiting to first 50 transactions for demonstration
        
        # Loop through each transaction to fetch merchant's latitude and longitude
        for transaction in transactions:
            if 'Zip' not in transaction:
                transaction['Zip'] = "Not Available"

            merchant_uuid = transaction['MerchantUUID']
            
            # Query the Merchants table using MerchantUUID
            merchant_response = merchants_table.get_item(
                Key={'MerchantUUID': merchant_uuid}
            )

            
            # Check if merchant details are found
            if 'Item' in merchant_response:
                merchant_details = merchant_response['Item']
                # Add latitude and longitude to the transaction dictionary
                transaction['Latitude'] = merchant_details.get('latitude', 'Not Available')
                transaction['Longitude'] = merchant_details.get('longitude', 'Not Available')
                
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    print(transactions[1].keys())
    return jsonify(transactions)


if __name__ == '__main__':
    
    app.run(debug=True, port=5000)