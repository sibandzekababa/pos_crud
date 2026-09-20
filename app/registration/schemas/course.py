from pydantic import BaseModel

class Course(BaseModel):
    title: str
    code: str
    credits: int
    department: str
    max_capacity: int
