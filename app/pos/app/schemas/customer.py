from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class CustomerBase(BaseModel):
    full_name: Optional[str] = Field(None, max_length=36)
    phone: Optional[str] = Field(None, max_length=20)
    loyalty_points: int = Field(default=0)

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(BaseModel):
    full_name: Optional[str] = Field(None, max_length=36)
    phone: Optional[str] = Field(None, max_length=20)
    loyalty_points: Optional[int] = None

class CustomerResponse(CustomerBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
