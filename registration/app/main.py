from pydantic import BaseModel
from fastapi import FastAPI
app=FastAPI()
@app.get("/")

def home():
         return{"message:Welcome to my firsterver"}
@app.get("/student")
def list_student():
        student=[]
class Student(BaseModel):
      name: str
      age: int
      email: str
      country:str
      id_number: int

student = []
def list_student():
      return student

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

@app.post("/student")
def registration_student(student:Student):
      student.appen(student)
      return{"return":"Student registered","student":student}