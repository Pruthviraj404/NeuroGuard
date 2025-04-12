from datetime import datetime
import sqlite3
import os
from flask import session

# Session-based tracker to avoid re-marking in the same session
marked_students_session = {}

def get_college_db():
    college_id = session.get('college_id')
    if not college_id:
        raise Exception("College ID not found in session.")

    # ✅ Ensure folder exists: data/college1/
    db_folder = os.path.join("data", college_id)
    os.makedirs(db_folder, exist_ok=True)

    # ✅ Database path: data/college1/college1attendance.db
    db_file = os.path.join(db_folder, f"{college_id}attendance.db")

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Create table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT NOT NULL,
            class_name TEXT NOT NULL,
            college_id TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    ''')
    conn.commit()
    return conn, cursor, college_id

def mark_attendance(student_name, class_name):
    if student_name == "Unknown":
        print("Unknown student. Ignored.")
        return

    college_id = session.get('college_id')
    if not college_id:
        print("Session college_id not found. Cannot mark attendance.")
        return

    if college_id not in marked_students_session:
        marked_students_session[college_id] = set()

    if student_name not in marked_students_session[college_id]:
        conn, cursor, _ = get_college_db()
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        cursor.execute('''
            INSERT INTO attendance (student_name, class_name, college_id, timestamp)
            VALUES (?, ?, ?, ?)
        ''', (student_name, class_name, college_id, timestamp))

        conn.commit()
        conn.close()

        marked_students_session[college_id].add(student_name)
        print(f"[College {college_id}] Attendance Marked: {student_name}")
    else:
        print(f"[College {college_id}] {student_name} already marked in this session.")
