from flask import Flask
import os
import bcrypt
import sqlite3
import base64

app = Flask(__name__)

db_path = os.path.join("todo-app", "db", "database.db")


### --- OPEN DATABASE 
def open_db():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    return conn, cursor


### --- CLOSE DATABASE (now requires conn)
def close_db(conn):
    conn.commit()
    conn.close()


### --- HASHES PASSWORDS
def cipher(password):
    password = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password, salt)
    b64_password = base64.b64encode(hashed).decode('utf-8')
    return b64_password


### --- ADD TO DATABASE
def add(email, hashed_password):
    conn, cursor = open_db()
    cursor.execute("INSERT INTO users (email, hashed_password) VALUES (?,?)", (email, hashed_password))
    close_db(conn)


### --- CHECKING USERS AND PASSWORDS
def check(email):
    conn, cursor = open_db()
    cursor.execute("SELECT hashed_password FROM users WHERE email = ?", (email,))
    b64_password = cursor.fetchone()

    if b64_password:
        b64_password_str = b64_password[0]
        hashed_password_bytes = base64.b64decode(b64_password_str)
        close_db(conn)
        return hashed_password_bytes
    else:
        close_db(conn)
        return None


### --- GETS USER ID FROM TABLE OF USERS
def get_user_id(current_user):
    conn, cursor = open_db()
    cursor.execute("""SELECT id FROM users
                   WHERE email = ?""", (current_user,))
    user_id = cursor.fetchone()
    close_db(conn)

    if user_id:
        return user_id[0]
    return None


### --- ADDS CREATED TIMETABLE TO DATABASE
def add_task(user_id, task_name, start_date, end_date):
    conn, cursor = open_db()
    cursor.execute("""INSERT INTO tasks (user_id, task_name, start_date, end_date)
                   VALUES (?,?,?,?)""", (user_id, task_name, start_date, end_date))
    close_db(conn)


### --- DELETES Task
def delete_task(user_id, task_id):
    conn, cursor = open_db()
    cursor.execute("""DELETE FROM tasks
                   WHERE user_id = ? AND id = ? """, (user_id, task_id))
    close_db(conn)


### --- Display tasks for that day
def display_tasks_day(user_id, today):
    conn, cursor = open_db()
    cursor.execute("""SELECT task_name, is_done, id FROM tasks
                   WHERE user_id = ? AND start_date <= ?""", (user_id, today))
    results = cursor.fetchall()
    close_db(conn)

    tasks = []
    for task in results:
        tasks.append({"task": task[0], "is_done": task[1], "id": task[2]})
    return tasks


### --- Display All tasks 
def display_all_tasks(user_id):
    conn, cursor = open_db()
    cursor.execute("""SELECT task_name, is_done FROM tasks
                   WHERE user_id = ?""", (user_id,))
    results = cursor.fetchall()
    close_db(conn)

    tasks = []
    for task in results:
        tasks.append({"task": task[0], "is_done": task[1]})
    return tasks


### --- PUTS is_done as TRUE in the DB
def mark_task_done(user_id, task_id):
    conn, cursor = open_db()
    cursor.execute("""UPDATE tasks
                   SET is_done = 1
                   WHERE user_id = ? AND
                   id = ?""", (user_id, task_id))
    close_db(conn)


### ----- DELETE ACCOUNT ------
def delete_account(email, user_id):
    conn, cursor = open_db()
    cursor.execute("""DELETE FROM users
                   WHERE email  = ? """, (email,))
    cursor.execute("""DELETE FROM tasks 
                   WHERE user_id = ? """, (user_id,))
    close_db(conn)


### ---- Check to see if there is no other task with that name
def check_name(user_id, task_id):
    conn, cursor = open_db()
    cursor.execute("""SELECT 1 FROM tasks
                   WHERE user_id = ? AND task_id = ? """, (user_id, task_id))
    task_exists = cursor.fetchone()
    close_db(conn)

    if task_exists:
        return True
    return False


### --- check to see if there if email is in db when creating an account
def check_email(email):
    conn, cursor = open_db()
    cursor.execute("""SELECT 1 FROM users
                   WHERE email = ?""", (email,))
    email_exists = cursor.fetchone()
    close_db(conn)

    if email_exists:
        return True
    return False


### --- Edits task in DB
def edit_task(new_task, user_id, task_id):
    conn, cursor = open_db()
    cursor.execute("""UPDATE tasks
                   SET task_name = ?
                   WHERE user_id = ?
                   AND id = ?""", (new_task, user_id, task_id))
    close_db(conn)


### --- get task id from DB
def get_task_id(user_id, task_name):
    conn,cursor = open_db()
    cursor.execute("""SELECT id FROM tasks
                   WHERE user_id = ? 
                   AND task_name = ?""", (user_id, task_name))
    
    data = cursor.fetchone()
    close_db(conn)
    if data is None:
        return None
    task_id = data[0]
    return task_id

