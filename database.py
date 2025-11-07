import sqlite3
import os

DB_PATH = "employees.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_name TEXT NOT NULL,
                telegram_id INTEGER UNIQUE
            );
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks_warnings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id INTEGER NOT NULL,
                description TEXT,
                status TEXT DEFAULT 'ожидает',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (employee_id) REFERENCES employees (id)
            );
        """)
    conn.close()

def get_employee_by_telegram_id(telegram_id):
    conn = sqlite3.connect(DB_PATH)
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM employees WHERE telegram_id = ?", (telegram_id,))
        return cur.fetchone()

def link_employee_to_telegram(full_name, telegram_id):
    conn = sqlite3.connect(DB_PATH)
    with conn:
        cur = conn.cursor()
        cur.execute("UPDATE employees SET telegram_id = ? WHERE employee_name = ?", (telegram_id, full_name))
        return cur.rowcount > 0

def get_tasks_warnings_by_employee_id(emp_id):
    conn = sqlite3.connect(DB_PATH)
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT id, description, status FROM tasks_warnings WHERE employee_id = ?", (emp_id,))
        return cur.fetchall()

def update_task_status(task_id, new_status):
    conn = sqlite3.connect(DB_PATH)
    with conn:
        cur = conn.cursor()
        cur.execute("UPDATE tasks_warnings SET status = ? WHERE id = ?", (new_status, task_id))
        return cur.rowcount > 0

def add_task(employee_id, description):
    conn = sqlite3.connect(DB_PATH)
    with conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO tasks_warnings (employee_id, description) VALUES (?, ?)", (employee_id, description))
        conn.commit()
