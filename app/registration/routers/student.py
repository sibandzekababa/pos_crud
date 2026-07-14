from fastapi import APIRouter, HTTPException
from schemas.student import Student
import services.student as service

router = APIRouter(prefix="/students", tags=["Students"])

@router.post("")
def register_student(student: Student):
    saved_student = service.register_student(student)
    return {"message": "Student registered", "student": saved_student}

@router.get("")
def list_students():
    return service.list_students()

@router.put("/{student_id}")
def edit_student(student_id: int, student: Student):
    if not service.edit_student(student_id, student):
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student updated successfully", "student": student}

@router.delete("/{student_id}")
def remove_student(student_id: int):
    if not service.remove_student(student_id):
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student deleted successfully"}
