from pydantic import BaseModel

class Student(BaseModel):
    name: str
    age: int
    email: str
    country: str
    id_number: int
