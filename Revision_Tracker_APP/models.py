import sqlite3
import os
import helpers

# --- FILE PATH
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir,"Database_Folder", "study_tracker.db")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS timetables (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               user_id INTEGER NOT NULL,
               timetable_name TEXT NOT NULL,
               start_date TEXT NOT NULL,
               end_date TEXT NOT NULL,
               duration NOT NULL,
               FOREIGN KEY(user_id) REFERENCES users(id) 
               
               )""")



print("success")

