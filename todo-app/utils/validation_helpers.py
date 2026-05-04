import utils.db_helpers as db_helper



### ---- Check to see if there is no other task with that name
def check_name(user_id, task_id):
    conn, cursor = db_helper.open_db()
    cursor.execute("""SELECT 1 FROM tasks
                   WHERE user_id = ? AND task_id = ? """, (user_id, task_id))
    task_exists = cursor.fetchone()
    db_helper.close_db(conn)

    if task_exists:
        return True
    return False


### --- check to see if there if email is in db when creating an account
def check_email(email):
    conn, cursor = db_helper.open_db()
    cursor.execute("""SELECT 1 FROM users
                   WHERE email = ?""", (email,))
    email_exists = cursor.fetchone()
    db_helper.close_db(conn)

    if email_exists:
        return True
    return False