from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict 
class PaymentBase(BaseModel):
    sale_id: int = Field(..., gt=0)
    payment_method: str = Field(..., min_length=2, max_length=30)
    amount_paid: float = Field(..., gt=0)


class PaymentCreate(PaymentBase):
    pass


class PaymentResponse(PaymentBase):
    model_config = ConfigDict(from_attributes=True)

    payment_id: int
    payment_date: datetime
