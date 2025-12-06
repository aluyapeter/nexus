from fastapi import APIRouter, Depends, HTTPException, status, Request, Header
from sqlalchemy.orm import Session
import uuid
from ..database import get_db
from .. import models, schemas, crud, utils
from ..services.paystack import PaystackService
from ..dependencies import get_current_user
from datetime import datetime, timezone

router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)

@router.post("/paystack/initiate", response_model=schemas.PaymentResponse, status_code=status.HTTP_201_CREATED)
def initiate_payment(
    payment_in: schemas.PaymentInitiate, 
    current_user: models.User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    tx_ref = str(uuid.uuid4())

    new_tx = models.Transaction(
        user_id=current_user.id,
        reference=tx_ref,
        amount=payment_in.amount,
        status=models.TransactionStatus.PENDING
    )
    db.add(new_tx)
    db.commit()
    
    paystack = PaystackService()
    try:
        auth_url = paystack.initiate_transaction(
            email=current_user.email,
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

@router.post("/paystack/webhook")
async def paystack_webhook(
    request: Request, 
    x_paystack_signature: str = Header(None),
    db: Session = Depends(get_db)
):
    body_bytes = await request.body()
    
    if not utils.verify_paystack_signature(body_bytes, x_paystack_signature):
        print("Invalid Paystack Signature detected!")
        return {"status": "ignored", "message": "Invalid signature"}
    
    payload = await request.json()
    event_type = payload.get("event")
    data = payload.get("data", {})
    
    print(f"Received event: {event_type}")

    if event_type == "charge.success":
        reference = data.get("reference")
        transaction = db.query(models.Transaction).filter_by(
            reference = reference
        ).first()
        
        if transaction:
            transaction.status = models.TransactionStatus.SUCCESS
            transaction.paid_at = datetime.now(timezone.utc)
            db.commit()
            print(f"Payment confirmed for {reference}")
            
    return {"status": "success"}

@router.get("/{reference}/status", response_model=schemas.TransactionResponse)
def get_payment_status(reference: str, db: Session = Depends(get_db)):
    transaction = db.query(models.Transaction).filter_by(reference=reference).first()
    
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
        
    return transaction