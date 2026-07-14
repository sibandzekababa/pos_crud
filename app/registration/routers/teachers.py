from fastapi import APIRouter, HTTPException
from schemas.teacher import Teacher
import services.teacher as service

router = APIRouter(prefix="/teachers", tags=["Teachers"])

@router.post("")
def register_teacher(teacher: Teacher):
    saved_teacher = service.register_teacher(teacher)
    return {"message": "Teacher registered", "teacher": saved_teacher}

@router.get("")
def list_teachers():
    return service.list_teachers()

@router.put("/{teacher_id}")
def edit_teacher(teacher_id: int, teacher: Teacher):
    if not service.edit_teacher(teacher_id, teacher):
        raise HTTPException(status_code=404, detail="Teacher not found")
    return {"message": "Teacher updated successfully", "teacher": teacher}

@router.delete("/{teacher_id}")
def remove_teacher(teacher_id: int):
    if not service.remove_teacher(teacher_id):
        raise HTTPException(status_code=404, detail="Teacher not found")
    return {"message": "Teacher deleted successfully"}
