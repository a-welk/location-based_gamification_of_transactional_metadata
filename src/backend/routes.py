import boto3
import flask_cors
from flask import Flask, request
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb',
                          aws_access_key_id="AKIA42KZIHZE3NIJXCJ2", #insert YOUR aws access key here
                          aws_secret_access_key="ULV7X90uwRxEu72rf4xDCoXmZXltARqt7TJ9zRkx", #insert YOUR aws sec
                          region_name="us-east-1")

app = Flask(__name__)
flask_cors.CORS(app)

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

@app.route('/login', methods=['POST'])
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
        return UserID
    else:
        print("Invalid user login credentials")
        return False
    
    
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
    for page in paginator.paginate(TableName='Transactions-temp',
                                   IndexName = 'User-index',
                                   KeyConditionExpression= Key('User').eq(UserID)):
                                        got_items += page['Items']
                                        this_page = page['Items']
                                        for x in range(len(this_page)):
                                            userTransactions.append(this_page[x]['Transaction ID'])
                                            transactionYear.append(this_page[x]['Year'])
                                            transactionMonth.append(this_page[x]['Month'])
                                            transactionDay.append(this_page[x]['Day'])
                                            transactionTime.append(this_page[x]['Time'])
                                            transactionAmount.append(this_page[x]['Amount'])
                                            transactionMerchantID.append(this_page[x]['Merchant Name'])
                                            transactionMCC.append(this_page[x]['MCC'])
                                        print("bonjour")
    print(transactionAmount)
    print(transactionTime)
    print(transactionDay)
    print(transactionMonth)
    
    print(userTransactions)
    print(transactionMerchantID)
    print(transactionMCC)
                                        
def check_budget(UserID): 
    get_user_transaction(UserID)
    
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
        return jsonify9({"status": "error", "message": str(E)})

def main():
    UserID = query_user_login("Kiera.Allen@gmail.com", "KieraAllen123") ##just a sample login
    get_user_transaction(str(UserID))
    
    
if __name__=="__main__":
    app.debug=True
    app.run()
    main()
