from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User


def authenticate(db: Session, username: str, password: str) -> User:
    user = db.query(User).filter(User.username == username).first()

    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This user account is inactive",
        )

    return user


def create_user(db: Session, username: str, password: str, full_name: str, role: str) -> User:
    if db.query(User).filter(User.username == username).first():
        raise HTTPException(status_code=409, detail="Username is already registered")

    user = User(
        username=username,
        hashed_password=hash_password(password),
        full_name=full_name,
        role=role.lower(),
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def make_login_response(user: User) -> dict:
    return {
        "access_token": create_access_token(user.id, user.role),
        "token_type": "bearer",
        "user": user,
    }
