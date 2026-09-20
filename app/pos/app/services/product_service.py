from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositories.product_repository import ProductRepository

class ProductService:
    def __init__(self, db: Session):
        self.repository = ProductRepository(db)

    def get_product(self, product_id: int):
        product = self.repository.get_by_id(product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        return product

    def get_all_products(self):
        return self.repository.get_all()

    def create_product(self, data: dict):
        return self.repository.create(data)

    def update_product(self, product_id: int, data: dict):
        product = self.repository.update(product_id, data)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        return product

    def delete_product(self, product_id: int):
        success = self.repository.delete(product_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        return {"status": "success", "message": "Product deleted successfully"}

    def scan_product(self, barcode: str):
        product = self.repository.get_by_barcode(barcode)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Scanned item not found or barcode unlisted"
            )
        if product.stock_quantity <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Product '{product.product_name}' is out of stock"
            )
        return product
