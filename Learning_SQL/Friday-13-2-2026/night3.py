import sqlite3
import os

# Create database in current folder
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, "study_tracker.db")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

### -- helper function
def values(subject, topic, hours):
    cursor.execute("""INSERT INTO study_sessions (subject, topic, hours) VALUES
               (?, ?, ?)""", (subject, topic, hours) )




# Create table

cursor.execute("""
CREATE TABLE IF NOT EXISTS study_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject TEXT NOT NULL,
    topic TEXT NOT NULL,
    hours REAL NOT NULL
)
""")

#### ---------input values into table
values("maths", "algebra", 2)
values("english", "creative writing", 0.5)
values("physics", "forces", 99)

conn.commit()

print("Success DB file created")


### --------------fetch data from table

print("All study sessions:")
cursor.execute("SELECT * FROM study_sessions")
rows = cursor.fetchall()

for row in rows:
    print(f"ID: {row[0]}, Subject: {row[1]}, Topic: {row[2]}, Hours: {row[3]}")
print(f"Total sessions stored: {len(rows)}")

conn.close()