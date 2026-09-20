from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from app.dependencies import get_current_user, require_roles
from app.models.user import User
from app.schemas.supplier import SupplierCreate, SupplierResponse, SupplierUpdate
from app.services.supplier_service import SupplierService

router = APIRouter(prefix="/suppliers", tags=["Suppliers"])

def get_supplier_service(db: Session = Depends(get_db)):
    return SupplierService(db)

@router.post("/", response_model=SupplierResponse, status_code=status.HTTP_201_CREATED)
def create_new_supplier(payload: SupplierCreate, service: SupplierService = Depends(get_supplier_service), current_user: User = Depends(require_roles("manager", "admin"))):
    return service.create_supplier(payload.model_dump())

@router.get("/", response_model=List[SupplierResponse])
def read_all_suppliers(service: SupplierService = Depends(get_supplier_service), current_user: User = Depends(get_current_user)):
    return service.get_all_suppliers()

@router.get("/{supplier_id}", response_model=SupplierResponse)
def read_supplier(supplier_id: int, service: SupplierService = Depends(get_supplier_service), current_user: User = Depends(get_current_user)):
    return service.get_supplier(supplier_id)

@router.put("/{supplier_id}", response_model=SupplierResponse)
def update_existing_supplier(supplier_id: int, payload: SupplierUpdate, service: SupplierService = Depends(get_supplier_service), current_user: User = Depends(require_roles("manager", "admin"))):
    return service.update_supplier(supplier_id, payload.model_dump(exclude_unset=True))

@router.delete("/{supplier_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_supplier(supplier_id: int, service: SupplierService = Depends(get_supplier_service), current_user: User = Depends(require_roles("manager", "admin"))):
    service.delete_supplier(supplier_id)
