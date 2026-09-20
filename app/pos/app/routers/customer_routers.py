from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from app.dependencies import get_current_user, require_roles
from app.models.user import User
from app.schemas.customer import CustomerCreate, CustomerResponse, CustomerUpdate
from app.services.customer_service import CustomerService

router = APIRouter(prefix="/customers", tags=["Customers"])

def get_customer_service(db: Session = Depends(get_db)):
    return CustomerService(db)

@router.post("/", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
def create_new_customer(payload: CustomerCreate, service: CustomerService = Depends(get_customer_service), current_user: User = Depends(require_roles("cashier", "manager", "admin"))):
    return service.create_customer(payload.model_dump())

@router.get("/", response_model=List[CustomerResponse])
def read_all_customers(service: CustomerService = Depends(get_customer_service), current_user: User = Depends(get_current_user)):
    return service.get_all_customers()

@router.get("/{customer_id}", response_model=CustomerResponse)
def read_customer(customer_id: int, service: CustomerService = Depends(get_customer_service), current_user: User = Depends(get_current_user)):
    return service.get_customer(customer_id)

@router.put("/{customer_id}", response_model=CustomerResponse)
def update_existing_customer(customer_id: int, payload: CustomerUpdate, service: CustomerService = Depends(get_customer_service), current_user: User = Depends(require_roles("cashier", "manager", "admin"))):
    return service.update_customer(customer_id, payload.model_dump(exclude_unset=True))

@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_customer(customer_id: int, service: CustomerService = Depends(get_customer_service), current_user: User = Depends(require_roles("manager", "admin"))):
    service.delete_customer(customer_id)
