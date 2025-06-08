import requests
from requests.auth import HTTPBasicAuth
import base64
from datetime import datetime

CONSUMER_KEY = '3nLQPiUYgRq08l4eWVj2kA9F9ArLlNjYAy4jaRAbFggLP2'
CONSUMER_SECRET = 'TTPIaKvKp7syti5tnbV8QcIcgTIusSRNrVaAZQpVcsehsYmqbFMNSHATJNMasyhmU'
BUSINESS_SHORT_CODE = 'N/A'
PASSKEY = '3nLQPiUYgRq08l4eWVj2kA9F9ArLlNjYAy4jaRAbFggLP2'
CALLBACK_URL = 'https://Littleafrica.com/mpesa/callback'

def get_access_token():
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(url, auth=HTTPBasicAuth(CONSUMER_KEY, CONSUMER_SECRET))
    response.raise_for_status()
    return response.json()['access_token']

def stk_push(phone_number, amount):
    access_token = get_access_token()
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    password = base64.b64encode((BUSINESS_SHORT_CODE + PASSKEY + timestamp).encode()).decode()

    headers = {"Authorization": f"Bearer {access_token}"}
    payload = {
        "BusinessShortCode": BUSINESS_SHORT_CODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone_number,
        "PartyB": BUSINESS_SHORT_CODE,
        "PhoneNumber": phone_number,
        "CallBackURL": CALLBACK_URL,
        "AccountReference": "LittleAfricaBetting",
        "TransactionDesc": "Premium Tip Access"
    }

    url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()
