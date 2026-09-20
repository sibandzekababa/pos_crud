from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.sale_item import SaleItemResponse
from app.services.sale_item_service import SaleItemService

router = APIRouter(prefix="/sale-items", tags=["Sale Items"])

def get_sale_item_service(db: Session = Depends(get_db)):
    return SaleItemService(db)

@router.get("/", response_model=List[SaleItemResponse])
def read_all_sale_items(service: SaleItemService = Depends(get_sale_item_service), current_user: User = Depends(get_current_user)):
    return service.get_all_sale_items()

@router.get("/sale/{sale_id}", response_model=List[SaleItemResponse])
def read_items_by_sale_id(sale_id: int, service: SaleItemService = Depends(get_sale_item_service), current_user: User = Depends(get_current_user)):
    return service.get_items_by_sale(sale_id)

@router.get("/{sale_item_id}", response_model=SaleItemResponse)
def read_sale_item(sale_item_id: int, service: SaleItemService = Depends(get_sale_item_service), current_user: User = Depends(get_current_user)):
    return service.get_sale_item(sale_item_id)
