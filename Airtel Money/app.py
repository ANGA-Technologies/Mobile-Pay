import requests
import json
import uuid
import time

def get_access_token(client_id, client_secret):
    url = "https://openapiuat.airtel.africa/auth/oauth2/token"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials"
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        raise Exception(f"Failed to obtain access token: {response.text}")

def initiate_payment(access_token, reference, phone_number, amount, transaction_id):
    url = "https://openapiuat.airtel.africa/merchant/v1/payments/"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-Country": "TZ",
        "X-Currency": "TZS",
        "Authorization": f"Bearer {access_token}"
    }
    data = {
        "reference": reference,
        "subscriber": {
            "country": "TZ",
            "currency": "TZS",
            "msisdn": phone_number
        },
        "transaction": {
            "amount": amount,
            "country": "TZ",
            "currency": "TZS",
            "id": transaction_id
        }
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()

def main():
    # Replace with your actual client_id and client_secret
    client_id = "your_client_id"
    client_secret = "your_client_secret"

    try:
        access_token = get_access_token(client_id, client_secret)
    except Exception as e:
        print(e)
        return

    phone_number = input("Enter the subscriber's phone number (e.g., 255712345678): ")
    amount = input("Enter the amount to be paid: ")
    reference = input("Enter the payment reference: ")
    transaction_id = str(uuid.uuid4())

    print("Initiating payment...")
    response = initiate_payment(access_token, reference, phone_number, amount, transaction_id)
    print("Response from Airtel API:")
    print(json.dumps(response, indent=4))

if __name__ == "__main__":
    main()
