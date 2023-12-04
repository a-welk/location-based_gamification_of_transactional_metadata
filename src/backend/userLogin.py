import boto3

dynamodb = boto3.resource('dynamodb',
                          aws_access_key_id=AKIA42KZIHZETGWRGQGV,
                          aws_secret_access_key=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)

def __init__(self, dyn_resource):
    self.dyn_resource = dyn_resource
    self.table = None
    
def query_user_login(email, password):
   # email = request.form['email']
   # password = request.form['password']
    
    table = dynamodb.Table('Users')
    response = table.query(
        KeyConditionExpression = Key('email').eq(email)
    )
    items = response['Items']
    UserID = items[0]['User ID']
    if password == items[0]['Password (unhashed)']:
        print(f"Successfully logged into {email}")
        return True
    else:
        print("Invalid user login credentials")
        return False
    
def get_user_transaction(UserID):
    table = dynamodb.Table('Transactions')
    response = table.query(
        KeyConditionExpression = Key('User ID').eq(UserID)
    )
    items = response['Items']
    for item in items: 
        userTransactions = items['Transaction ID']
        transactionYear = items['Year']
        transactionMonth = items['Month']
        transactionDay = items['Day']
        transactionTime = items['Time']
        transactionAmount = items['Amount']
        transactionMerchantID = items['Merchant Name']
        transctionMCC = items['MCC']