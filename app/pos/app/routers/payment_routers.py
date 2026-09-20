from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from app.dependencies import get_current_user, require_roles
from app.models.user import User
from app.schemas.payment import PaymentCreate, PaymentResponse
from app.services.payment_service import PaymentService

router = APIRouter(prefix="/payments", tags=["Payments"])

def get_payment_service(db: Session = Depends(get_db)):
    return PaymentService(db)

@router.post("/", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
def record_payment(
    payload: PaymentCreate,
    service: PaymentService = Depends(get_payment_service),
    current_user: User = Depends(require_roles("manager", "admin")),
):
    return service.create_payment(payload.model_dump())

@router.get("/", response_model=List[PaymentResponse])
def read_all_payments(service: PaymentService = Depends(get_payment_service), current_user: User = Depends(require_roles("manager", "admin"))):
    return service.get_all_payments()

@router.get("/sale/{sale_id}", response_model=List[PaymentResponse])
def read_sale_payments(sale_id: int, service: PaymentService = Depends(get_payment_service), current_user: User = Depends(get_current_user)):
    return service.get_payments_for_sale(sale_id)

@router.get("/{payment_id}", response_model=PaymentResponse)
def read_payment(payment_id: int, service: PaymentService = Depends(get_payment_service), current_user: User = Depends(require_roles("manager", "admin"))):
    return service.get_payment(payment_id)
