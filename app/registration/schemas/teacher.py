from pydantic import BaseModel

class Teacher(BaseModel):
    name: str
    email: str
    department: str
    salary: float
    id_number: int


