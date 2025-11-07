import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

conn = psycopg2.connect(DATABASE_URL)

def init_db():
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                id SERIAL PRIMARY KEY,
                employee_name TEXT NOT NULL,
                telegram_id BIGINT UNIQUE
            );
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS tasks_warnings (
                id SERIAL PRIMARY KEY,
                employee_id INTEGER REFERENCES employees(id),
                description TEXT,
                status TEXT DEFAULT 'ожидает',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()
