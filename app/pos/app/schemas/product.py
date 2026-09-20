from typing import Optional
from pydantic import BaseModel, Field, field_validator, ConfigDict 


class ProductBase(BaseModel):
    barcode: Optional[str] = Field(None, max_length=50)
    product_name: str = Field(..., min_length=1, max_length=30)
    product_price: float = Field(..., ge=0)
    stock_quantity: int = Field(..., ge=0)
    category_id: int = Field(..., gt=0)
    supplier_id: int = Field(..., gt=0)


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    barcode: Optional[str] = Field(None, max_length=50)
    product_name: Optional[str] = Field(None, min_length=1, max_length=30)
    product_price: Optional[float] = Field(None, ge=0)
    stock_quantity: Optional[int] = Field(None, ge=0)
    category_id: Optional[int] = Field(None, gt=0)
    supplier_id: Optional[int] = Field(None, gt=0)


class ProductResponse(ProductBase):
    model_config = ConfigDict(from_attributes=True)

    product_id: int
