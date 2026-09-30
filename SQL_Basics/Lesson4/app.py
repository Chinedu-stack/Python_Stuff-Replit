import sqlite3
import os

# --- FILE PATH
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, "study_tracker.db")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# --- CREATE TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS study_sessions(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject TEXT NOT NULL,
    topic TEXT NOT NULL,
    duration REAL NOT NULL
)
""")


# --- HELPER FUNCTION
def add(subject, topic, duration, date):
    cursor.execute(
        "INSERT INTO study_sessions (subject, topic, duration, date) VALUES (?, ?, ?, ?)",
        (subject, topic, duration, date)
    )


add("biology", "respiration", 0.4, "26/03/2011")
conn.commit()

print("successfully added new column")

cursor.execute("SELECT topic, duration, date FROM study_sessions")
stuff = cursor.fetchall()
for thing in stuff:
    print(thing, end=" | ")


conn.close()

