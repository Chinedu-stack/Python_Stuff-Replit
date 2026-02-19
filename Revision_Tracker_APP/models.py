import sqlite3
import os
import helpers

# --- FILE PATH
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir,"Database_Folder", "study_tracker.db")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("""DELETE FROM sqlite_sequence WHERE name='users'""")

conn.commit()
conn.close()

print("success")