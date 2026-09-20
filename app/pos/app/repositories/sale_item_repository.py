from sqlalchemy.orm import Session
from app.models.sale_item import SaleItem

class SaleItemRepository:
    def __init__(self, db: Session):
        self.db = db
        self.model = SaleItem

    def get_by_id(self, sale_item_id: int):
        return self.db.query(self.model).filter(self.model.sale_item_id == sale_item_id).first()

    def get_by_sale_id(self, sale_id: int):
        return self.db.query(self.model).filter(self.model.sale_id == sale_id).all()

    def get_all(self):
        return self.db.query(self.model).all()
