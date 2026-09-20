from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.receipt_repository import ReceiptRepository

class ReceiptService:
    def __init__(self, db: Session):
        self.repository = ReceiptRepository(db)

    def get_receipt(self, receipt_id: int):
        receipt = self.repository.get_by_id(receipt_id)
        if not receipt:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Receipt record not found"
            )
        return receipt

    def get_receipt_by_sale(self, sale_id: int):
        receipt = self.repository.get_by_sale_id(sale_id)
        if not receipt:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Receipt for this sale was not found"
            )
        return receipt

    def get_all_receipts(self):
        return self.repository.get_all()
