import sqlite3
import os


# Get the folder where your Python file is located
basedir = os.path.dirname(os.path.abspath(__file__))

# Create the database path in the same folder
db_path = os.path.join(basedir, "lesson_1.db")
# This creates a database file called lesson_1.db

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE subjects (
    id INTEGER,
    name TEXT
);
""")

cursor.execute("""
CREATE TABLE sessions (
    id INTEGER,
    subject_id INTEGER,
    hours REAL
);
""")

conn.commit()
conn.close()