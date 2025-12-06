from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import requests
from dotenv import load_dotenv
import os
from ..database import get_db
from .. import crud, schemas

load_dotenv()


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")

@router.get("/google")
def login_google():
    """
    Redirect the user to Google's OAuth 2.0 server.
    """
    scope = "openid email profile"
    base_url = "https://accounts.google.com/o/oauth2/v2/auth"
    
    params = (
        f"?response_type=code"
        f"&client_id={GOOGLE_CLIENT_ID}"
        f"&redirect_uri={GOOGLE_REDIRECT_URI}"
        f"&scope={scope}"
        f"&access_type=offline"
    )
    
    return RedirectResponse(url=base_url + params)

@router.get("/google/callback", response_model=schemas.UserResponse)
def callback_google(code: str, db: Session = Depends(get_db)):
    """
    Handling the callback, exchange code for token, and fetch user info.
    """

    token_url = "https://oauth2.googleapis.com/token"
    token_data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code"
    }
    
    token_res = requests.post(token_url, data=token_data)
    
    if token_res.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to get access token from Google")
        
    access_token = token_res.json().get("access_token")
    
    user_info_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    headers = {"Authorization": f"Bearer {access_token}"}
    
    user_res = requests.get(user_info_url, headers=headers)
    
    if user_res.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to get user info from Google")
        
    google_user = user_res.json()
    
    db_user = crud.get_user_by_google_id(db, google_id=google_user["id"])
    
    if not db_user:
        user_in = schemas.UserCreate(
            email=google_user["email"],
            google_id=google_user["id"],
            full_name=google_user.get("name"),
            profile_picture=google_user.get("picture")
        )
        db_user = crud.create_user(db, user_in)
        
    return db_user