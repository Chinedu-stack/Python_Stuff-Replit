import sqlite3
from pathlib import Path

basedir = Path(__file__).resolve().parent
db_path = basedir / "study_tracker.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("""SELECT name, hours_studied
               FROM subjects
               ORDER BY hours_studied ASC
               LIMIT 1""")

rows = cursor.fetchall()
for row in rows:
    print(f"{row[0]}: {row[1]}")