import sqlite3
from pathlib import Path

# Set up database path
basedir = Path(__file__).parent
conn = sqlite3.connect(basedir / 'study_tracker_lesson6.db')
cursor = conn.cursor()


cursor.execute("""CREATE TABLE IF NOT EXISTS sessions(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               subject TEXT NOT NULL,
               hours INTEGER NOT NULL)""")

def add(subject, hours):
    cursor.execute("""INSERT INTO sessions (subject, hours)
                   VALUES (?,?)""", (subject, hours))
    conn.commit()




cursor.execute(""" SELECT * FROM sessions
               WHERE hours <= (?)""", (2,))

rows = cursor.fetchall()
if rows:
    for row in rows:
        print(row)
else:
    print("no results")


