from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator, ConfigDict # Added ConfigDict


class SaleItemCreate(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0)


class SaleItemResponse(BaseModel):
    # Upgraded to modern ConfigDict configuration instance layout
    model_config = ConfigDict(from_attributes=True)

    sale_item_id: int
    sale_id: int
    product_id: int
    quantity: int
    unit_price: float


class PaymentCreateForSale(BaseModel):
    payment_method: str = Field(..., min_length=2, max_length=30)
    amount_paid: float = Field(..., gt=0)

    @field_validator("payment_method")
    @classmethod
    def validate_method(cls, value: str) -> str:
        value = value.strip().lower()
        aliases = {
            "mobile money": "mpesa",
            "m-pesa": "mpesa",
            "mobile_money": "mpesa",
        }
        value = aliases.get(value, value)
        if value not in {"cash", "mpesa", "card", "store_credit"}:
            raise ValueError("Payment method must be cash, mpesa, card, or store_credit")
        return value


class SaleCreate(BaseModel):
    customer_id: Optional[int] = Field(None, gt=0)
    items: List[SaleItemCreate] = Field(..., min_length=1)
    payments: List[PaymentCreateForSale] = Field(..., min_length=1)


class PaymentResponse(BaseModel):
    # Upgraded configuration layout
    model_config = ConfigDict(from_attributes=True)

    payment_id: int
    sale_id: int
    payment_method: str
    amount_paid: float
    payment_date: datetime


class ReceiptResponse(BaseModel):
    # Upgraded configuration layout
    model_config = ConfigDict(from_attributes=True)

    receipt_id: int
    receipt_number: str
    sale_id: int
    issued_at: datetime


class SaleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    sale_id: int
    sale_date: datetime
    total_amount: float
    customer_id: Optional[int]
    user_id: int
    items: List[SaleItemResponse]
    payments: List[PaymentResponse]
    receipt: Optional[ReceiptResponse]
    change_due: float = 0.0
