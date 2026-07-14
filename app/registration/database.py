from contextlib import contextmanager
import sqlite3

sqlite_file_name = "school.db"

@contextmanager
def get_db_connection():
    connection = sqlite3.connect(sqlite_file_name)
    connection.row_factory = sqlite3.Row
    try:
        yield connection
    finally:
        connection.close()

def create_table():
    with get_db_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                email TEXT NOT NULL,
                country TEXT NOT NULL,
                id_number INTEGER NOT NULL
            )
        """)
        connection.execute("""
            CREATE TABLE IF NOT EXISTS teachers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                department TEXT NOT NULL,
                salary REAL NOT NULL,
                id_number INTEGER NOT NULL
            )
        """)
        connection.execute("""
            CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                code TEXT NOT NULL,
                credits INTEGER NOT NULL,
                department TEXT NOT NULL,
                max_capacity INTEGER NOT NULL
            )
        """)
        connection.commit()
