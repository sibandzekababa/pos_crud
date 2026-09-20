from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class SaleItemBase(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)

class SaleItemCreate(SaleItemBase):
    sale_id: int

class SaleItemUpdate(BaseModel):
    quantity: Optional[int] = Field(None, gt=0)

class SaleItemResponse(SaleItemBase):
    model_config = ConfigDict(from_attributes=True)

    sale_item_id: int
    sale_id: int
    unit_price: float
