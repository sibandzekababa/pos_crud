from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class SupplierBase(BaseModel):
    company_name: str = Field(..., max_length=50)
    contact_name: Optional[str] = Field(None, max_length=36)
    supplier_phoneNumber: str = Field(..., max_length=20)
    supplier_email: Optional[str] = Field(None, max_length=36)

class SupplierCreate(SupplierBase):
    pass

class SupplierUpdate(BaseModel):
    company_name: Optional[str] = Field(None, max_length=50)
    contact_name: Optional[str] = Field(None, max_length=36)
    supplier_phoneNumber: Optional[str] = Field(None, max_length=20)
    supplier_email: Optional[str] = Field(None, max_length=36)

class SupplierResponse(SupplierBase):
    model_config = ConfigDict(from_attributes=True)

    supplier_id: int
