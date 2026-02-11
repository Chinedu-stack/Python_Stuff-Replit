import sqlite3
import os

# Get folder of current script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))



# Build path to app.db in the same folder
db_path = os.path.join(BASE_DIR, "app.db")     


# Connect to the database file (creates it if it doesn't exist)
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

#-----PUTS the values in each of the subsections - subject_id, topic, hours, date
cursor.execute("""
INSERT INTO Sessions (subject_id, topic, hours, date)
VALUES (?, ?, ?, ?)""", (1, "Cosine rule", 1.5, "2026-02-11"))


conn.commit()

cursor.execute("SELECT * FROM Sessions")
print(cursor.fetchall())

conn.close()