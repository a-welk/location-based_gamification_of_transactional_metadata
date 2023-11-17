import boto3


def getHighestTransactionID():
    # Initialize a DynamoDB client
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('Transactions')

    # Scan the table - this is expensive and slow for large tables
    response = table.scan(
        AttributesToGet=[
            'MerchantLocationID'
        ]
    )

    highest_number = None

    for item in response['Items']:
        current_number = item['MerchantLocationID']
        if highest_number is None or current_number > highest_number:
            highest_number = current_number

    return int(highest_number)
