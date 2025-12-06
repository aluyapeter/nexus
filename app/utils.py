import hmac
import hashlib
import os
from dotenv import load_dotenv

load_dotenv()

PAYSTACK_SECRET_KEY = os.getenv("PAYSTACK_SECRET_KEY")

def verify_paystack_signature(payload_body: bytes, signature_header: str) -> bool:
    """
    Verifies that the request actually came from Paystack.
    """
    if not signature_header or not PAYSTACK_SECRET_KEY:
        return False
        
    hash_obj = hmac.new(
        key=PAYSTACK_SECRET_KEY.encode('utf-8'),
        msg=payload_body,
        digestmod=hashlib.sha512
    )
    
    expected_signature = hash_obj.hexdigest()
    
    return hmac.compare_digest(expected_signature, signature_header)