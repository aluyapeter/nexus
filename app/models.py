from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime
import enum

class TransactionStatus(str, enum.Enum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email: str = Column(String, unique=True, index=True) # type: ignore
    google_id = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=True)
    profile_picture = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    transactions = relationship("Transaction", back_populates="owner")

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    reference: str = Column(String, unique=True) # type: ignore
    amount = Column(Integer, nullable=False)
    
    status: str = Column(String, default=TransactionStatus.PENDING) # type: ignore
    
    created_at = Column(DateTime, default=datetime.utcnow)
    paid_at: datetime = Column(DateTime, nullable=True) # type: ignore

    owner = relationship("User", back_populates="transactions")