from fastapi import FastAPI
from OOPs.project.app.registration.database import create_table
from OOPs.project.app.registration.routers.student import router as student_router
from OOPs.project.app.registration.routers.teachers import router as teacher_router
from OOPs.project.app.registration.routers.course import router as course_router

app = FastAPI()

create_table()

app.include_router(student_router)
app.include_router(teacher_router)
app.include_router(course_router)
