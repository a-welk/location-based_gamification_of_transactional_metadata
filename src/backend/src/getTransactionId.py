import boto3


def getHighestTransactionID():
    # Initialize a DynamoDB client
    dynamodb = boto3.resource('dynamodb',
                          aws_access_key_id="AKIA42KZIHZE3NIJXCJ2", #insert YOUR aws access key here
                          aws_secret_access_key="ULV7X90uwRxEu72rf4xDCoXmZXltARqt7TJ9zRkx", #insert YOUR aws sec
                          region_name="us-east-1")
    table = dynamodb.Table('Transactions')

    # Scan the table - this is expensive and slow for large tables
    response = table.scan(
        AttributesToGet=[
            'transaction_id'
        ]
    )

    highest_number = None

    for item in response['Items']:
        current_number = item['transction_id']
        if highest_number is None or current_number > highest_number:
            highest_number = current_number
    print(highest_number)
    return int(highest_number)
