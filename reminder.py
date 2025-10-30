import sqlite3
from datetime import datetime

class Task:
    def __init__(self, title, description, deadline, priority="Medium", status="Pending"):
        self.title = title
        self.description = description
        self.deadline = deadline
        self.priority = priority
        self.status = status

class Reminder:
    def __init__(self, db_name="tasks.db"):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.create_table()

    def create_table(self):
        query = """CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    description TEXT,
                    deadline TEXT,
                    priority TEXT DEFAULT 'Medium',
                    status TEXT DEFAULT 'Pending'
                )"""
        self.conn.execute(query)
        self.conn.commit()

    def add_task(self, task):
        query = "INSERT INTO tasks (title, description, deadline, priority, status) VALUES (?, ?, ?, ?, ?)"
        self.conn.execute(query, (task.title, task.description, task.deadline, task.priority, task.status))
        self.conn.commit()
        print(f"[+] Task Added: {task.title} (Priority: {task.priority})")

    def get_all_tasks(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM tasks")
        return cursor.fetchall()

    def get_due_tasks(self):
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM tasks WHERE deadline <= ? AND status='Pending'", (now,))
        return cursor.fetchall()

    def mark_completed(self, task_id):
        query = "UPDATE tasks SET status='Completed' WHERE id=?"
        self.conn.execute(query, (task_id,))
        self.conn.commit()
        print(f"[✓] Task ID {task_id} marked as Completed.")

    def delete_task(self, task_id):
        query = "DELETE FROM tasks WHERE id=?"
        self.conn.execute(query, (task_id,))
        self.conn.commit()
        print(f"[-] Task ID {task_id} deleted.")

    def show_tasks(self):
        tasks = self.get_all_tasks()
        if not tasks:
            print("No tasks found.")
            return
        print("\n=== TASK LIST ===")
        for task in tasks:
            task_id, title, desc, deadline, priority, status = task
            print(f"ID: {task_id} | {title} | {deadline} | Priority: {priority} | Status: {status}")
        print("=================\n")
