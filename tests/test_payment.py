from unittest.mock import patch, MagicMock

def test_initiate_payment_success(client, db_session):
    from app.models import User
    user = User(email="test@example.com", google_id="123", full_name="Tester")
    db_session.add(user)
    db_session.commit()
    
    payload = {"amount": 5000}
    
    with patch("app.services.paystack.PaystackService.initiate_transaction") as mock_init:
        mock_init.return_value = "https://paystack.com/fake-checkout"
        
        response = client.post("/payments/paystack/initiate", json=payload)
        
    assert response.status_code == 201
    data = response.json()
    assert data["authorization_url"] == "https://paystack.com/fake-checkout"
    assert "reference" in data