
from flask import Flask, render_template, request, jsonify
from src import getTransactionId, main

app = Flask(__name__)

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

if __name__ == '__main__':
    
    app.run(debug=True, port=5000)
