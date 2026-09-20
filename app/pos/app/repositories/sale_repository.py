from sqlalchemy.orm import Session
from app.models.sale import Sale

class SaleRepository:
    def __init__(self, db: Session):
        self.db = db
        self.model = Sale

    def get_by_id(self, sale_id: int):
        return self.db.query(self.model).filter(self.model.sale_id == sale_id).first()

    def get_all(self):
        return self.db.query(self.model).all()

    def create(self, sale_obj: Sale):
        self.db.add(sale_obj)
        self.db.commit()
        self.db.refresh(sale_obj)
        return sale_obj

    def delete(self, sale_id: int):
        db_sale = self.get_by_id(sale_id)
        if db_sale:
            self.db.delete(db_sale)
            self.db.commit()
            return True
        return False
