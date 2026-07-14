from database import get_db_connection

def add_course(title, code, credits, department, max_capacity):
    with get_db_connection() as connection:
        connection.execute(
            "INSERT INTO courses (title, code, credits, department, max_capacity) VALUES (?, ?, ?, ?, ?)",
            (title, code, credits, department, max_capacity),
        )
        connection.commit()

def get_courses():
    with get_db_connection() as connection:
        rows = connection.execute("SELECT * FROM courses").fetchall()
        return [dict(row) for row in rows]

def update_course(course_id, title, code, credits, department, max_capacity):
    with get_db_connection() as connection:
        cursor = connection.execute(
            "UPDATE courses SET title=?, code=?, credits=?, department=?, max_capacity=? WHERE id=?",
            (title, code, credits, department, max_capacity, course_id)
        )
        connection.commit()
        return cursor.rowcount > 0

def delete_course(course_id):
    with get_db_connection() as connection:
        cursor = connection.execute("DELETE FROM courses WHERE id = ?", (course_id,))
        connection.commit()
        return cursor.rowcount > 0
