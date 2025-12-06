import requests
import os
from fastapi import HTTPException
from dotenv import load_dotenv

load_dotenv()

PAYSTACK_SECRET_KEY = os.getenv("PAYSTACK_SECRET_KEY")
PAYSTACK_INIT_URL = "https://api.paystack.co/transaction/initialize"

class PaystackService:
    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json"
        }

    def initiate_transaction(self, email: str, amount_kobo: int, reference: str):
        data = {
            "email": email,
            "amount": amount_kobo,
            "reference": reference,
            # callback_url for frontend redirection
            # "callback_url": "http://localhost:8000/payment/callback" 
        }
        
        try:
            response = requests.post(PAYSTACK_INIT_URL, json=data, headers=self.headers)
            response_data = response.json()
            
            if response.status_code != 200 or not response_data.get("status"):
                raise HTTPException(status_code=400, detail="Paystack rejected the initialization")
                
            return response_data["data"]["authorization_url"]
            
        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=503, detail="Payment service unavailable")