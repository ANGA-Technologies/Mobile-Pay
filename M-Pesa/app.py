from flask import Flask, request, jsonify
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os
import base64
from datetime import datetime

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Get credentials
consumer_key = os.getenv("MPESA_CONSUMER_KEY")
consumer_secret = os.getenv("MPESA_CONSUMER_SECRET")
short_code = os.getenv("SHORT_CODE")
passkey = os.getenv("PASSKEY")

# URLs
sandbox_auth_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
sandbox_c2b_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"

# Generate access token
def get_access_token():
    res = requests.get(sandbox_auth_url, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    return res.json()["access_token"]

# Generate password
def generate_password():
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    data_to_encode = short_code + passkey + timestamp
    encoded = base64.b64encode(data_to_encode.encode()).decode('utf-8')
    return encoded, timestamp

@app.route('/')
def index():
    return "M-Pesa C2B Test App Running"

@app.route('/pay', methods=['POST'])
def pay():
    body = request.json
    phone = body.get("phone")
    amount = body.get("amount", "10")

    access_token = get_access_token()
    password, timestamp = generate_password()

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "BusinessShortCode": short_code,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone,
        "PartyB": short_code,
        "PhoneNumber": phone,
        "CallBackURL": "https://mytest.com/callback",  # Use ngrok if local
        "AccountReference": "Test123",
        "TransactionDesc": "C2B Test"
    }

    response = requests.post(sandbox_c2b_url, json=payload, headers=headers)
    return jsonify(response.json())

if __name__ == "__main__":
    app.run(debug=True)
