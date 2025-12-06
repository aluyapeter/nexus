from pydantic import BaseModel, EmailStr
from datetime import datetime
from enum import Enum


class UserBase(BaseModel):
    email: EmailStr
    full_name: str | None = None
    profile_picture: str | None = None

class UserCreate(UserBase):
    google_id: str

class UserResponse(UserBase):
    id: int
    google_id: str

    class Config:
        from_attributes = True

class PaymentInitiate(BaseModel):
    amount: int

class PaymentResponse(BaseModel):
    reference: str
    authorization_url: str

class TransactionStatus(str, Enum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"

class TransactionResponse(BaseModel):
    reference: str
    amount: int
    status: TransactionStatus
    created_at: datetime
    paid_at: datetime | None = None

    class Config:
        from_attributes = True