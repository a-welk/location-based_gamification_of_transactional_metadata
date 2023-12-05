import boto3
from boto3.dynamodb.conditions import Key
dynamodb = boto3.resource('dynamodb',
                          aws_access_key_id="AKIA42KZIHZETGWRGQGV",
                          aws_secret_access_key="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",
                          region_name="us-east-1")

def __init__(self, dyn_resource):
    self.dyn_resource = dyn_resource
    self.table = None
    
def query_user_login(email, password):
   # email = request.form['email']
   # password = request.form['password']
    
    table = dynamodb.Table('Users')
    response = table.query(
        IndexName = 'Email-index',
        KeyConditionExpression = Key('Email').eq(email)
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
    table = dynamodb.Table('Transactions-temp')
    response = table.query(
        KeyConditionExpression = Key('User').eq(UserID)
    )
    items = response['Items']
    print(items)

    for item in items: 
        userTransactions = items[0]['Transaction ID']
        transactionYear = items[0]['Year']
        transactionMonth = items[0]['Month']
        transactionDay = items[0]['Day']
        transactionTime = items[0]['Time']
        transactionAmount = items[0]['Amount']
        transactionMerchantID = items[0]['Merchant Name']
        transctionMCC = items[0]['MCC']

        
def main():
    query_user_login("Leighton.Sullivan@gmail.com", "LeightonSullivan123") ##just a sample login
    get_user_transaction(0)
    
    
if __name__=="__main__":
    main()