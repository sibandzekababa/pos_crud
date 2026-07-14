from fastapi import APIRouter, HTTPException
from schemas.corvse import Course
import services.course as service

router = APIRouter(prefix="/courses", tags=["Courses"])

@router.post("")
def register_course(course: Course):
    saved_course = service.register_course(course)
    return {"message": "Course registered", "course": saved_course}

@router.get("")
def list_courses():
    return service.list_courses()

@router.put("/{course_id}")
def edit_course(course_id: int, course: Course):
    if not service.edit_course(course_id, course):
        raise HTTPException(status_code=404, detail="Course not found")
    return {"message": "Course updated successfully", "course": course}

@router.delete("/{course_id}")
def remove_course(course_id: int):
    if not service.remove_course(course_id):
        raise HTTPException(status_code=404, detail="Course not found")
    return {"message": "Course deleted successfully"}
