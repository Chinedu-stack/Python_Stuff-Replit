import sqlite3
import os

# get folder where this Python file is located
basedir = os.path.abspath(os.path.dirname(__file__))

# create full path to database file
db_path = os.path.join(basedir, "lesson_2.db")


# connect to database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# CREATE TABLE (so this lesson works alone)
cursor.execute("""
CREATE TABLE IF NOT EXISTS study_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject TEXT,
    hours REAL,
    date TEXT
)
""")

# INSERT DATA
cursor.execute("""
INSERT INTO study_sessions (subject, hours, date)
VALUES (?,?,?)
""", ("spanish", 0.5, "12-02-2026"))



conn.commit()

print("Study session added successfully!")

conn.close()
