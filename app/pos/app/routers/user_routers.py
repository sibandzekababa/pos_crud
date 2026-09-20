from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from app.dependencies import require_roles
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.services.auth_service import create_user
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])


def get_user_service(db: Session = Depends(get_db)):
    return UserService(db)


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_new_user(
    payload: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin", "manager")),
):
    if current_user.role.lower() == "manager" and payload.role.lower() == "admin":
        from fastapi import HTTPException
        raise HTTPException(403, "Managers cannot create admin accounts")
    return create_user(db, payload.username, payload.password, payload.full_name, payload.role)


@router.get("/", response_model=List[UserResponse])
def read_all_users(
    service: UserService = Depends(get_user_service),
    current_user: User = Depends(require_roles("admin", "manager")),
):
    return service.get_all_users()


@router.get("/{user_id}", response_model=UserResponse)
def read_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
    current_user: User = Depends(require_roles("admin", "manager")),
):
    return service.get_user(user_id)


@router.put("/{user_id}", response_model=UserResponse)
def update_existing_user(
    user_id: int,
    payload: UserUpdate,
    service: UserService = Depends(get_user_service),
    current_user: User = Depends(require_roles("admin", "manager")),
):
    target = service.get_user(user_id)
    if current_user.role.lower() == "manager" and target.role.lower() == "admin":
        from fastapi import HTTPException
        raise HTTPException(403, "Managers cannot modify admin accounts")
    if current_user.role.lower() == "manager" and payload.role == "admin":
        from fastapi import HTTPException
        raise HTTPException(403, "Managers cannot promote users to admin")
    return service.update_user(user_id, payload.model_dump(exclude_unset=True))


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
    current_user: User = Depends(require_roles("admin")),
):
    if user_id == current_user.id:
        from fastapi import HTTPException
        raise HTTPException(400, "You cannot delete your own account")
    service.delete_user(user_id)
