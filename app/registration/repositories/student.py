from OOPs.project.app.registration.database import get_db_connection

def add_student(name, age, email, country, id_number):
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO students (name, age, email, country, id_number) 
                VALUES (%s, %s, %s, %s, %s);
                """,
                (name, age, email, country, id_number)
            )
            connection.commit()

def get_students():
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM students;")
            return cursor.fetchall()

def update_student(student_id, name, age, email, country, id_number):
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE students 
                SET name = %s, age = %s, email = %s, country = %s, id_number = %s 
                WHERE id = %s;
                """,
                (name, age, email, country, id_number, student_id)
            )
            connection.commit()
            return True

def delete_student(student_id):
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM students WHERE id = %s;", (student_id,))
            connection.commit()
            return True
