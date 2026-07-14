from schemas.corvse import Course
import repositories.corvse as repo

def register_course(course: Course):
    repo.add_course(course.title, course.code, course.credits, course.department, course.max_capacity)
    return course

def list_courses():
    return repo.get_courses()

def edit_course(course_id: int, course: Course):
    return repo.update_course(course_id, course.title, course.code, course.credits, course.department, course.max_capacity)

def remove_course(course_id: int):
    return repo.delete_course(course_id)
