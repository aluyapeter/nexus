import requests
import hmac
import hashlib
import json

# CONFIG
URL = "http://localhost:8000/payments/paystack/webhook"
SECRET = "sk_test_826db5a5a1e6b566bdff61af601694d8ef29085b"
REF_TO_CONFIRM = "421b37d0-bab9-4ef0-b119-f9f08dbc102c"

payload = {
    "event": "charge.success",
    "data": {
        "reference": REF_TO_CONFIRM,
        "status": "success"
    }
}

body = json.dumps(payload).encode('utf-8')

signature = hmac.new(SECRET.encode(), body, hashlib.sha512).hexdigest()

headers = {
    "x-paystack-signature": signature,
    "Content-Type": "application/json"
}

print(f"Sending webhook for {REF_TO_CONFIRM}...")
resp = requests.post(URL, data=body, headers=headers)
print(f"Response: {resp.status_code} - {resp.text}")