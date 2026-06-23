import sqlite3
from contextlib import contextmanager
from dataclasses import dataclass

@dataclass
class Student:
    name: str
    age: int
    email: str
    country: str
    id_number: int

@dataclass
class Teacher:
    name: str
    department: str
    email: str
    salary: float
    employee_id: int

@dataclass
class Course:
    title: str
    course_code: str
    credits: int
    tranier: str
    max_capacity: int

sqlite_file_name = "school.db"

@contextmanager
def get_db_connection():
    conn = sqlite3.connect(sqlite_file_name)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def create_all_tables():
    with get_db_connection() as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS students(
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     name TEXT NOT NULL,
                     age INTEGER NOT NULL,
                     email TEXT NOT NULL,
                     country TEXT NOT NULL,
                     id_number INTEGER NOT NULL)''')
        
def add_student(name, age, email, country, id_number):
    with get_db_connection() as conn:
        conn.execute(
            'INSERT INTO students(name, age, email, country, id_number) VALUES (?, ?, ?, ?, ?)',
            (name, age, email, country, id_number)
        )
        conn.commit()

def register_student(student: Student):
    add_student(student.name, student.age, student.email, student.country, student.id_number)

def get_student():
    with get_db_connection() as conn:
        return conn.execute('SELECT * FROM students').fetchall()
     
def list_student():
    return get_student()

def get_student_by_id(student_id: int):
    with get_db_connection() as conn:
        return conn.execute('SELECT * FROM students WHERE id = ?', (student_id,)).fetchone()

def update_student(student_id: int, student: Student):
    with get_db_connection() as conn:
        conn.execute(
            'UPDATE students SET name=?, age=?, email=?, country=?, id_number=? WHERE id=?',
            (student.name, student.age, student.email, student.country, student.id_number, student_id)
        )
        conn.commit()

def delete_student(student_id: int):
    with get_db_connection() as conn:
        conn.execute('DELETE FROM students WHERE id = ?', (student_id,))
        conn.commit()
        
def create_all_tables():
    with get_db_connection() as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS teachers(
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     name TEXT NOT NULL,
                     department TEXT NOT NULL,
                     email TEXT NOT NULL,
                     salary REAL NOT NULL,
                     employee_id INTEGER NOT NULL)''')
        
def add_teacher(teacher: Teacher):
    with get_db_connection() as conn:
        conn.execute(
            'INSERT INTO teachers(name, department, email, salary, employee_id) VALUES (?, ?, ?, ?, ?)',
            (teacher.name, teacher.department, teacher.email, teacher.salary, teacher.employee_id)
        )
        conn.commit()

def list_teachers():
    with get_db_connection() as conn:
        return conn.execute('SELECT * FROM teachers').fetchall()

def get_teacher_by_id(teacher_id: int):
    with get_db_connection() as conn:
        return conn.execute('SELECT * FROM teachers WHERE id = ?', (teacher_id,)).fetchone()

def update_teacher(teacher_id: int, teacher: Teacher):
    with get_db_connection() as conn:
        conn.execute(
            'UPDATE teachers SET name=?, department=?, email=?, salary=?, employee_id=? WHERE id=?',
            (teacher.name, teacher.department, teacher.email, teacher.salary, teacher.employee_id, teacher_id)
        )
        conn.commit()

def delete_teacher(teacher_id: int):
    with get_db_connection() as conn:
        conn.execute('DELETE FROM teachers WHERE id = ?', (teacher_id,))
        conn.commit()
        
def create_all_tables():
    with get_db_connection() as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS courses(
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     title TEXT NOT NULL,
                     course_code TEXT NOT NULL,
                     credits INTEGER NOT NULL,
                     tranier TEXT NOT NULL,
                     max_capacity INTEGER NOT NULL)''')
        conn.commit()

def add_course(course: Course):
    with get_db_connection() as conn:
        conn.execute(
            'INSERT INTO courses(title, course_code, credits, tranier, max_capacity) VALUES (?, ?, ?, ?, ?)',
            (course.title, course.course_code, course.credits, course.tranier, course.max_capacity)
        )
        conn.commit()

def list_courses():
    with get_db_connection() as conn:
        return conn.execute('SELECT * FROM courses').fetchall()

def get_course_by_id(course_id: int):
    with get_db_connection() as conn:
        return conn.execute('SELECT * FROM courses WHERE id = ?', (course_id,)).fetchone()

def update_course(course_id: int, course: Course):
    with get_db_connection() as conn:
        conn.execute(
            'UPDATE courses SET title=?, course_code=?, credits=?, tranier=?, max_capacity=? WHERE id=?',
            (course.title, course.course_code, course.credits, course.tranier, course.max_capacity, course_id)
        )
        conn.commit()

def delete_course(course_id: int):
    with get_db_connection() as conn:
        conn.execute('DELETE FROM courses WHERE id = ?', (course_id,))
        conn.commit()
