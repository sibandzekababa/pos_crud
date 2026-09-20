from sqlalchemy.orm import Session
from app.models.category import Category

class CategoryRepository:
    def __init__(self, db: Session):
        self.db = db
        self.model = Category

    def get_by_id(self, category_id: int):
        return self.db.query(self.model).filter(self.model.id == category_id).first()

    def get_all(self):
        return self.db.query(self.model).all()

    def create(self, data: dict):
        db_category = self.model(**data)
        self.db.add(db_category)
        self.db.commit()
        self.db.refresh(db_category)
        return db_category

    def update(self, category_id: int, data: dict):
        db_category = self.get_by_id(category_id)
        if db_category:
            for key, value in data.items():
                if value is not None:
                    setattr(db_category, key, value)
            self.db.commit()
            self.db.refresh(db_category)
        return db_category

    def delete(self, category_id: int):
        db_category = self.get_by_id(category_id)
        if db_category:
            self.db.delete(db_category)
            self.db.commit()
            return True
        return False
