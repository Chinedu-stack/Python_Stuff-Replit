import sqlite3
import os

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, "study.db")

conn = sqlite3.connect(db_path)
cursor = conn.cursor

cursor.execute("""
CREATE TABLE IF NOT EXISTS study_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT
    subject TEXT,
    hours REAL,
    date TEXT 
               
)
""")

cursor.execute("""
INSERT INTO study_sessions (subject, hours, date)
VALUES (?, ?, ?)
""", ("Computer Science", 7, "12-02-2026"))

cursor.commit()

print("Sessions successfully added")