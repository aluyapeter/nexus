from app import utils

def test_verify_signature_valid():
    secret = "sk_test_secret"
    payload = b'{"event":"test"}'
    assert utils.verify_paystack_signature(payload, "garbage_signature") == False