from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import uuid
from ..database import get_db
from .. import models, schemas, crud
from ..services.paystack import PaystackService

router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)

@router.post("/paystack/initiate", response_model=schemas.PaymentResponse, status_code=status.HTTP_201_CREATED)
def initiate_payment(
    payment_in: schemas.PaymentInitiate, 
    user_id: int = 1, 
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    tx_ref = str(uuid.uuid4())

    new_tx = models.Transaction(
        user_id=user.id,
        reference=tx_ref,
        amount=payment_in.amount,
        status=models.TransactionStatus.PENDING
    )
    db.add(new_tx)
    db.commit()
    
    paystack = PaystackService()
    try:
        auth_url = paystack.initiate_transaction(
            email=user.email,
            amount_kobo=payment_in.amount,
            reference=tx_ref
        )
    except Exception as e:
        new_tx.status = models.TransactionStatus.FAILED
        db.commit()
        raise e

    return {
        "reference": tx_ref,
        "authorization_url": auth_url
    }