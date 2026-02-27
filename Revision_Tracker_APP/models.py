import sqlite3
import os
import helpers

# --- FILE PATH
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir,"Database_Folder", "task_manager.db")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()





cursor.execute("""CREATE TABLE IF NOT EXISTS tasks (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               user_id INTEGER NOT NULL,
               task_name TEXT NOT NULL,
               start_date TEXT NOT NULL,
               end_date TEXT NOT NULL,
               is_done INTEGER DEFAULT 0,
               FOREIGN KEY(user_id) REFERENCES users(id) 
               
               )""")

cursor.execute("""CREATE TABLE IF NOT EXISTS users (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               email TEXT NOT NULL,
               hashed_password TEXT NOT NULL
               )""")



conn.commit()


conn.close()
print("success")

