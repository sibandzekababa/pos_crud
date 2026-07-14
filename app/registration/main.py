from fastapi import FastAPI
from database import create_table
from routers.student import router as student_router
from routers.teachers import router as teacher_router
from routers.course import router as course_router

app = FastAPI()

create_table()

app.include_router(student_router)
app.include_router(teacher_router)
app.include_router(course_router)
