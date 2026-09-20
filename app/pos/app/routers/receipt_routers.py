from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.receipt import ReceiptResponse
from app.services.receipt_service import ReceiptService

router = APIRouter(prefix="/receipts", tags=["Receipts"])

def get_receipt_service(db: Session = Depends(get_db)):
    return ReceiptService(db)

@router.get("/", response_model=List[ReceiptResponse])
def read_all_receipts(service: ReceiptService = Depends(get_receipt_service), current_user: User = Depends(get_current_user)):
    return service.get_all_receipts()

@router.get("/sale/{sale_id}", response_model=ReceiptResponse)
def read_receipt_by_sale_id(sale_id: int, service: ReceiptService = Depends(get_receipt_service), current_user: User = Depends(get_current_user)):
    return service.get_receipt_by_sale(sale_id)

@router.get("/{receipt_id}", response_model=ReceiptResponse)
def read_receipt(receipt_id: int, service: ReceiptService = Depends(get_receipt_service), current_user: User = Depends(get_current_user)):
    return service.get_receipt(receipt_id)
