from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.category_repository import CategoryRepository

class CategoryService:
    def __init__(self, db: Session):
        self.repository = CategoryRepository(db)

    def get_category(self, category_id: int):
        category = self.repository.get_by_id(category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category record not found"
            )
        return category

    def get_all_categories(self):
        return self.repository.get_all()

    def create_category(self, data: dict):
        return self.repository.create(data)

    def update_category(self, category_id: int, data: dict):
        self.get_category(category_id)
        return self.repository.update(category_id, data)

    def delete_category(self, category_id: int):
        self.get_category(category_id)
        return self.repository.delete(category_id)
