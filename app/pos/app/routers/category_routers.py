from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from app.dependencies import get_current_user, require_roles
from app.models.user import User
from app.schemas.category import CategoryCreate, CategoryResponse, CategoryUpdate
from app.services.category_service import CategoryService

router = APIRouter(prefix="/categories", tags=["Categories"])

def get_category_service(db: Session = Depends(get_db)):
    return CategoryService(db)

@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_new_category(payload: CategoryCreate, service: CategoryService = Depends(get_category_service), current_user: User = Depends(require_roles("manager", "admin"))):
    return service.create_category(payload.model_dump())

@router.get("/", response_model=List[CategoryResponse])
def read_all_categories(service: CategoryService = Depends(get_category_service), current_user: User = Depends(get_current_user)):
    return service.get_all_categories()

@router.get("/{category_id}", response_model=CategoryResponse)
def read_category(category_id: int, service: CategoryService = Depends(get_category_service), current_user: User = Depends(get_current_user)):
    return service.get_category(category_id)

@router.put("/{category_id}", response_model=CategoryResponse)
def update_existing_category(category_id: int, payload: CategoryUpdate, service: CategoryService = Depends(get_category_service), current_user: User = Depends(require_roles("manager", "admin"))):
    return service.update_category(category_id, payload.model_dump(exclude_unset=True))

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_category(category_id: int, service: CategoryService = Depends(get_category_service), current_user: User = Depends(require_roles("manager", "admin"))):
    service.delete_category(category_id)
