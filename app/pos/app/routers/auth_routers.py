from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database import get_db
from app.dependencies import get_current_user, require_roles
from app.models.user import User
from app.schemas.user import LoginResponse, UserCreate, UserResponse
from app.services.auth_service import authenticate, create_user, make_login_response

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=LoginResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = authenticate(db, form_data.username, form_data.password)
    return make_login_response(user)


@router.get("/me", response_model=UserResponse)
def me(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_first_user(
    payload: UserCreate,
    db: Session = Depends(get_db),
):
    """
    Safe bootstrap endpoint: the first account must be created before
    the protected user-management endpoints can be used. Once any user
    exists, registration is manager/admin-only.
    """
    has_users = db.query(User).count() > 0

    if has_users:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Public registration is disabled. A manager or admin must create users.",
        )

    return create_user(db, payload.username, payload.password, payload.full_name, "admin")


@router.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_staff_user(
    payload: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin", "manager")),
):
    role = payload.role.lower()
    if current_user.role.lower() == "manager" and role == "admin":
        raise HTTPException(status_code=403, detail="Managers cannot create admin accounts")

    return create_user(db, payload.username, payload.password, payload.full_name, role)
