from sqlalchemy.orm import Session
from app.models.supplier import Supplier

class SupplierRepository:
    def __init__(self, db: Session):
        self.db = db
        self.model = Supplier

    def get_by_id(self, supplier_id: int):
        return self.db.query(self.model).filter(self.model.supplier_id == supplier_id).first()

    def get_all(self):
        return self.db.query(self.model).all()

    def create(self, data: dict):
        db_supplier = self.model(**data)
        self.db.add(db_supplier)
        self.db.commit()
        self.db.refresh(db_supplier)
        return db_supplier

    def update(self, supplier_id: int, data: dict):
        db_supplier = self.get_by_id(supplier_id)
        if db_supplier:
            for key, value in data.items():
                if value is not None:
                    setattr(db_supplier, key, value)
            self.db.commit()
            self.db.refresh(db_supplier)
        return db_supplier

    def delete(self, supplier_id: int):
        db_supplier = self.get_by_id(supplier_id)
        if db_supplier:
            self.db.delete(db_supplier)
            self.db.commit()
            return True
        return False
