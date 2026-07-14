from database import get_db_connection

def add_teacher(name, email, department, salary, id_number):
    with get_db_connection() as connection:
        connection.execute(
            "INSERT INTO teachers (name, email, department, salary, id_number) VALUES (?, ?, ?, ?, ?)",
            (name, email, department, salary, id_number),
        )
        connection.commit()

def get_teachers():
    with get_db_connection() as connection:
        rows = connection.execute("SELECT * FROM teachers").fetchall()
        return [dict(row) for row in rows]

def update_teacher(teacher_id, name, email, department, salary, id_number):
    with get_db_connection() as connection:
        cursor = connection.execute(
            "UPDATE teachers SET name=?, email=?, department=?, salary=?, id_number=? WHERE id=?",
            (name, email, department, salary, id_number, teacher_id)
        )
        connection.commit()
        return cursor.rowcount > 0

def delete_teacher(teacher_id):
    with get_db_connection() as connection:
        cursor = connection.execute("DELETE FROM teachers WHERE id = ?", (teacher_id,))
        connection.commit()
        return cursor.rowcount > 0
