from sqlalchemy.orm import Session
from app.models.user import User

class UserRepository:
    def __init__(self, db: Session):
        self.db = db
        self.model = User

    def get_by_id(self, user_id: int):
        return self.db.query(self.model).filter(self.model.id == user_id).first()

    def get_by_username(self, username: str):
        return self.db.query(self.model).filter(self.model.username == username).first()

    def get_all(self):
        return self.db.query(self.model).all()

    def create(self, data: dict):
        db_user = self.model(**data)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def update(self, user_id: int, data: dict):
        db_user = self.get_by_id(user_id)
        if db_user:
            for key, value in data.items():
                if value is not None:
                    setattr(db_user, key, value)
            self.db.commit()
            self.db.refresh(db_user)
        return db_user

    def delete(self, user_id: int):
        db_user = self.get_by_id(user_id)
        if db_user:
            self.db.delete(db_user)
            self.db.commit()
            return True
        return False
