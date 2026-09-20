from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.sale_item_repository import SaleItemRepository

class SaleItemService:
    def __init__(self, db: Session):
        self.repository = SaleItemRepository(db)

    def get_sale_item(self, sale_item_id: int):
        sale_item = self.repository.get_by_id(sale_item_id)
        if not sale_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sale item record not found"
            )
        return sale_item

    def get_items_by_sale(self, sale_id: int):
        return self.repository.get_by_sale_id(sale_id)

    def get_all_sale_items(self):
        return self.repository.get_all()
