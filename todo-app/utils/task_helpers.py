from flask import Flask
import utils.db_helpers as db_helper

app = Flask(__name__)


### ========= USER FUNCTIONS =========

### --- GETS USER ID FROM TABLE OF USERS
def get_user_id(current_user):
    conn, cursor = db_helper.open_db()
    cursor.execute("""SELECT id FROM users
                   WHERE email = ?""", (current_user,))
    user_id = cursor.fetchone()
    db_helper.close_db(conn)

    if user_id:
        return user_id[0]
    return None


### ========= TASK CREATION / DELETION =========

### --- ADDS CREATED TASK TO DATABASE
def add_task(user_id, task_name, end_date):
    conn, cursor = db_helper.open_db()
    cursor.execute("""INSERT INTO tasks (user_id, task_name, end_date)
                   VALUES (?,?,?)""", (user_id, task_name, end_date))
    db_helper.close_db(conn)


### --- DELETES Task
def delete_task(user_id, task_id):
    conn, cursor = db_helper.open_db()
    cursor.execute("""DELETE FROM tasks
                   WHERE user_id = ? AND id = ? """, (user_id, task_id))
    db_helper.close_db(conn)


### ========= TASK FETCHING =========

### --- get task id from DB
def get_task_id(user_id, task_name):
    conn,cursor = db_helper.open_db()
    cursor.execute("""SELECT id FROM tasks
                   WHERE user_id = ? 
                   AND task_name = ?""", (user_id, task_name))
    
    data = cursor.fetchone()
    db_helper.close_db(conn)
    if data is None:
        return None
    task_id = data[0]
    return task_id


### --- Display tasks for that day
def display_tasks_day(user_id, today):
    conn, cursor = db_helper.open_db()
    cursor.execute("""SELECT task_name, is_done, id FROM tasks
                   WHERE user_id = ? AND start_date <= ?""", (user_id, today))
    results = cursor.fetchall()
    db_helper.close_db(conn)

    tasks = []
    for task in results:
        tasks.append({"task": task[0], "is_done": task[1], "id": task[2]})
    return tasks


### --- Display All tasks 
def fetch_tasks(user_id):
    conn, cursor = db_helper.open_db()
    cursor.execute("""SELECT task_name, is_done, id FROM tasks
                   WHERE user_id = ?""", (user_id,))
    results = cursor.fetchall()
    db_helper.close_db(conn)

    tasks = []
    for task in results:
        tasks.append({"task": task[0], "is_done": task[1], "task_id": task[2]})
    return tasks


### ========= TASK UPDATES =========

### --- PUTS is_done as TRUE in the DB
def mark_task_done(user_id, task_id):
    conn, cursor = db_helper.open_db()
    cursor.execute("""UPDATE tasks
                   SET is_done = 1
                   WHERE user_id = ? AND
                   id = ?""", (user_id, task_id))
    db_helper.close_db(conn)


### --- Edits task in DB
def edit_task(new_task, user_id, task_id):
    conn, cursor = db_helper.open_db()
    cursor.execute("""UPDATE tasks
                   SET task_name = ?
                   WHERE user_id = ?
                   AND id = ?""", (new_task, user_id, task_id))
    db_helper.close_db(conn)