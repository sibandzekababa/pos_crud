from pydantic import BaseModel, Field, ConfigDict 
from datetime import datetime

class ReceiptResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    receipt_id: int
    receipt_number: str = Field(..., max_length=50)
    sale_id: int
    issued_at: datetime
