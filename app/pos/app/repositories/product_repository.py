from sqlalchemy.orm import Session
from app.models.product import Product


class ProductRepository:
    def __init__(self, db: Session):
        self.db = db
        self.model = Product

    def get_by_id(self, product_id: int):
        return self.db.query(self.model).filter(self.model.product_id == product_id).first()

    def get_by_barcode(self, barcode: str):
        # Queries the database for the matching barcode column string
        return self.db.query(self.model).filter(self.model.barcode == barcode).first()

    def get_all(self):
        return self.db.query(self.model).all()

    def create(self, data: dict):
        obj = self.model(**data)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(self, product_id: int, data: dict):
        obj = self.get_by_id(product_id)
        if obj:
            for key, value in data.items():
                if value is not None:
                    setattr(obj, key, value)
            self.db.commit()
            self.db.refresh(obj)
        return obj

    def delete(self, product_id: int):
        obj = self.get_by_id(product_id)
        if obj:
            self.db.delete(obj)
            self.db.commit()
            return True
        return False
