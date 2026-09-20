from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, db: Session):
        self.repository = UserRepository(db)

    def get_user(self, user_id: int):
        user = self.repository.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User record not found")
        return user

    def get_all_users(self):
        return self.repository.get_all()

    def create_user(self, data: dict):
        if self.repository.get_by_username(data["username"]):
            raise HTTPException(status_code=409, detail="Username is already registered")
        password = data.pop("password", None)
        if not password:
            raise HTTPException(status_code=400, detail="Password is required")
        data["hashed_password"] = hash_password(password)
        return self.repository.create(data)

    def update_user(self, user_id: int, data: dict):
        self.get_user(user_id)
        if "password" in data:
            data["hashed_password"] = hash_password(data.pop("password"))
        return self.repository.update(user_id, data)

    def delete_user(self, user_id: int):
        self.get_user(user_id)
        return self.repository.delete(user_id)
