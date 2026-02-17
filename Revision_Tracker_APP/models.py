import sqlite3
import os
import helpers

# --- FILE PATH
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, "study_tracker.db")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS users(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               email TEXT NOT NULL,
               hashed_password TEXT NOT NULL)""")

conn.commit()
conn.close()
print("success")