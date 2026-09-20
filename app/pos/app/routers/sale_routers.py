from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from app.dependencies import get_current_user, require_roles
from app.models.user import User
from app.schemas.sale import SaleCreate, SaleResponse
from app.services.sale_service import SaleService

router = APIRouter(prefix="/sales", tags=["Sales Transaction"])


def get_sale_service(db: Session = Depends(get_db)):
    return SaleService(db)


@router.post("/", response_model=SaleResponse, status_code=status.HTTP_201_CREATED)
def checkout_basket(
    payload: SaleCreate,
    service: SaleService = Depends(get_sale_service),
    current_user: User = Depends(require_roles("cashier", "manager", "admin")),
):
    sale, change_due = service.process_checkout(payload.model_dump(), current_user)
    # change_due is a calculated checkout value; do not persist it as a payment.
    response = SaleResponse.model_validate(sale)
    return response.model_copy(update={"change_due": change_due})


@router.get("/", response_model=List[SaleResponse])
def read_all_sales(
    service: SaleService = Depends(get_sale_service),
    current_user: User = Depends(get_current_user),
):
    return service.get_all_sales()


@router.get("/{sale_id}", response_model=SaleResponse)
def read_sale(
    sale_id: int,
    service: SaleService = Depends(get_sale_service),
    current_user: User = Depends(get_current_user),
):
    return service.get_sale(sale_id)


@router.delete("/{sale_id}", status_code=status.HTTP_204_NO_CONTENT)
def cancel_sale(
    sale_id: int,
    service: SaleService = Depends(get_sale_service),
    current_user: User = Depends(require_roles("manager", "admin")),
):
    service.cancel_sale(sale_id)
