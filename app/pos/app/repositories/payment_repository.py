from sqlalchemy.orm import Session
from app.models.payment import Payment

class PaymentRepository:
    def __init__(self, db: Session):
        self.db = db
        self.model = Payment

    def get_by_id(self, payment_id: int):
        return self.db.query(self.model).filter(self.model.payment_id == payment_id).first()

    def get_by_sale_id(self, sale_id: int):
        return self.db.query(self.model).filter(self.model.sale_id == sale_id).all()

    def get_all(self):
        return self.db.query(self.model).all()

    def create(self, data: dict):
        db_payment = self.model(**data)
        self.db.add(db_payment)
        self.db.commit()
        self.db.refresh(db_payment)
        return db_payment
