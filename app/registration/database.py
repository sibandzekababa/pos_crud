import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager

DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/postgres"

@contextmanager
def get_db_connection():
    connection = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    try:
        yield connection
    finally:
        connection.close()

def create_table():
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            # 1. Students Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL,
                    age INTEGER NOT NULL,
                    email TEXT NOT NULL,
                    country TEXT NOT NULL,
                    id_number INTEGER NOT NULL
                );
            """)
            
            # 2. Teachers Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS teachers (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    department TEXT NOT NULL,
                    salary REAL NOT NULL,
                    id_number INTEGER NOT NULL
                );
            """)

            # 3. Courses Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS courses (
                    id SERIAL PRIMARY KEY,
                    title TEXT NOT NULL,
                    code TEXT NOT NULL,
                    credits INTEGER NOT NULL,
                    department TEXT NOT NULL,
                    max_capacity INTEGER NOT NULL
                );
            """)
            
        connection.commit()
