from typing import Optional
from pydantic import BaseModel, Field, field_validator, ConfigDict 

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=36)
    password: str = Field(..., min_length=8, max_length=128)
    full_name: str = Field(..., min_length=2, max_length=100)
    role: str = Field(default="cashier", max_length=20)

    @field_validator("role")
    @classmethod
    def validate_role(cls, value: str) -> str:
        value = value.lower()
        if value not in {"cashier", "manager", "admin"}:
            raise ValueError("Role must be cashier, manager, or admin")
        return value


class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=36)
    password: Optional[str] = Field(None, min_length=8, max_length=128)
    full_name: Optional[str] = Field(None, min_length=2, max_length=100)
    role: Optional[str] = Field(None, max_length=20)
    is_active: Optional[bool] = None

    @field_validator("role")
    @classmethod
    def validate_role(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        value = value.lower()
        if value not in {"cashier", "manager", "admin"}:
            raise ValueError("Role must be cashier, manager, or admin")
        return value


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    full_name: str
    role: str
    is_active: bool


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
