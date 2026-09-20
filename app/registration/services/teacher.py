from OOPs.project.app.registration.schemas.teacher import Teacher
import OOPs.project.app.registration.repositories.teacher as repo

def register_teacher(teacher: Teacher):
    repo.add_teacher(teacher.name, teacher.email, teacher.department, teacher.salary, teacher.id_number)
    return teacher

def list_teachers():
    return repo.get_teachers()

def edit_teacher(teacher_id: int, teacher: Teacher):
    return repo.update_teacher(teacher_id, teacher.name, teacher.email, teacher.department, teacher.salary, teacher.id_number)

def remove_teacher(teacher_id: int):
    return repo.delete_teacher(teacher_id)
