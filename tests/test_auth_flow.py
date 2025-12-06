from unittest.mock import patch, MagicMock
from app.main import app

def test_google_callback_json_response(client, db_session):
    mock_token_resp = MagicMock()
    mock_token_resp.status_code = 200
    mock_token_resp.json.return_value = {"access_token": "fake_token"}

    mock_user_resp = MagicMock()
    mock_user_resp.status_code = 200
    mock_user_resp.json.return_value = {
        "id": "99999",
        "email": "grader@test.com",
        "name": "Grader Bot",
        "picture": "http://img.com/pic"
    }

    with patch("app.routers.auth.requests.post", return_value=mock_token_resp):
        with patch("app.routers.auth.requests.get", return_value=mock_user_resp):
            
            response = client.get(
                "/auth/google/callback?code=fake_code_123",
                headers={"Accept": "application/json"}
            )

    assert response.status_code == 200
    
    data = response.json()
    assert data["email"] == "grader@test.com"
    assert "access_token" in data
    assert data["token_type"] == "bearer"