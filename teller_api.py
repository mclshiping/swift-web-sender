
import os
import requests

TELLER_BASE_URL = "https://api.teller.io"
TELLER_TOKEN = os.environ.get("TELLER_API_TOKEN", "your_token_here")

def send_payment(account_id: str, amount: str, currency: str, description: str, recipient: dict):
    url = f"{TELLER_BASE_URL}/accounts/{account_id}/payments"
    headers = {
        "Authorization": f"Bearer {TELLER_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "amount": amount,
        "currency": currency,
        "description": description,
        "recipient": recipient
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.status_code, response.json()
