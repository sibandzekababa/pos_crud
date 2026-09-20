from OOPs.project.app.registration.schemas.student import Student
import OOPs.project.app.registration.repositories.student as repo

def register_student(student: Student):
    repo.add_student(student.name, student.age, student.email, student.country, student.id_number)
    return student

def list_students():
    return repo.get_students()

def edit_student(student_id: int, student: Student):
    return repo.update_student(student_id, student.name, student.age, student.email, student.country, student.id_number)

def remove_student(student_id: int):
    return repo.delete_student(student_id)
