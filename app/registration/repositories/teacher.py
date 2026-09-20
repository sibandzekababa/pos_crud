from OOPs.project.app.registration.database import get_db_connection

def add_teacher(name, email, department, salary, id_number):
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO teachers (name, email, department, salary, id_number) 
                VALUES (%s, %s, %s, %s, %s);
                """,
                (name, email, department, salary, id_number)
            )
            connection.commit()

def get_teachers():
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM teachers;")
            return cursor.fetchall()

def update_teacher(teacher_id, name, email, department, salary, id_number):
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE teachers 
                SET name = %s, email = %s, department = %s, salary = %s, id_number = %s 
                WHERE id = %s;
                """,
                (name, email, department, salary, id_number, teacher_id)
            )
            connection.commit()
            return cursor.rowcount > 0

def delete_teacher(teacher_id):
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM teachers WHERE id = %s;", (teacher_id,))
            connection.commit()
            return cursor.rowcount > 0
