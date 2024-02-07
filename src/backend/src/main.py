import boto3

def addTransactionToTable(transactionID, user, personName, cardNumber, year, month, day, time, amount, useChip, merchantName, merchantCity, merchantState, merchantLocId, zipcode, mcc, errors, isFraud):
    # Initialize a DynamoDB client
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('Transactions')

    # Data item to add
    item = {
        'Transaction ID': transactionID,  # Replace with your primary key and its value
        'User':  user,
        'Person': personName,
        'Card Number': cardNumber,
        'Year' : year,
        'Month'	: month,
        'Day'	: day,
        'Time'	: time,
        'Amount' : 	amount,
        'Use Chip' : useChip,
        'Merchant Name' : merchantName,
        'Merchant City'	: merchantCity,
        'Merchant State' :	merchantState,
        'MerchantLocationID' : merchantLocId,
        'Zip' : zipcode,
        'MCC' : mcc,
        'Errors?' :	errors,
        'Is Fraud?' : isFraud
        # Add other attributes as needed
    }

    try:
        # Add the item to the table
        response = table.put_item(Item=item)
        return 201
    except:
        return 500
