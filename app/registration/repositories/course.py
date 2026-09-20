from OOPs.project.app.registration.database import get_db_connection

def add_course(title, code, credits, department, max_capacity):
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO courses (title, code, credits, department, max_capacity) 
                VALUES (%s, %s, %s, %s, %s);
                """,
                (title, code, credits, department, max_capacity)
            )
            connection.commit()

def get_courses():
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM courses;")
            return cursor.fetchall()

def update_course(course_id, title, code, credits, department, max_capacity):
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE courses 
                SET title = %s, code = %s, credits = %s, department = %s, max_capacity = %s 
                WHERE id = %s;
                """,
                (title, code, credits, department, max_capacity, course_id)
            )
            connection.commit()
            return cursor.rowcount > 0

def delete_course(course_id):
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM courses WHERE id = %s;", (course_id,))
            connection.commit()
            return cursor.rowcount > 0
