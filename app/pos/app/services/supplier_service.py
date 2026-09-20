from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.supplier_repository import SupplierRepository

class SupplierService:
    def __init__(self, db: Session):
        self.repository = SupplierRepository(db)

    def get_supplier(self, supplier_id: int):
        supplier = self.repository.get_by_id(supplier_id)
        if not supplier:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Supplier record not found"
            )
        return supplier

    def get_all_suppliers(self):
        return self.repository.get_all()

    def create_supplier(self, data: dict):
        return self.repository.create(data)

    def update_supplier(self, supplier_id: int, data: dict):
        self.get_supplier(supplier_id)
        return self.repository.update(supplier_id, data)

    def delete_supplier(self, supplier_id: int):
        self.get_supplier(supplier_id)
        return self.repository.delete(supplier_id)
