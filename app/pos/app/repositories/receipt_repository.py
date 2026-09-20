from sqlalchemy.orm import Session
from app.models.receipt import Receipt

class ReceiptRepository:
    def __init__(self, db: Session):
        self.db = db
        self.model = Receipt

    def get_by_id(self, receipt_id: int):
        return self.db.query(self.model).filter(self.model.receipt_id == receipt_id).first()

    def get_by_sale_id(self, sale_id: int):
        return self.db.query(self.model).filter(self.model.sale_id == sale_id).first()

    def get_all(self):
        return self.db.query(self.model).all()
