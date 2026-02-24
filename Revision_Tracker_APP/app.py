from flask import Flask, flash, request, render_template, redirect, url_for, session
import os
import bcrypt
import sqlite3
import helpers
from datetime import datetime, date
app = Flask(__name__)
app.secret_key = "your_super_secret_key_here"
conn = None
cursor = None
basedir = os.path.abspath(os.path.dirname(__file__))

db_path = os.path.join(basedir,"Database_Folder", "study_tracker.db") ### --- makes sure the db is made in the same folder as the app.py


### --- LOADS THE LANDING PAGE
@app.route("/", methods=["GET"])
def landing_page():
    return render_template("landing.html")
    


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("landing_page"))

### --- LOADS THE DASHBOARD
@app.route("/dashboard", methods=["GET"])
def dashboard():
    current_user = session["current_user"]
    tasks = helpers.display(current_user)
    if tasks:
        return render_template("dashboard.html", tasks=tasks)
    return render_template("dashboard.html")

### --- CHECKS DATABASE FOR INPUTTED EMAIL AND PASSWORD
@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email", "")
    password = request.form.get("password", "")

    stored_hash_bytes = helpers.check(email) ### --- Returns the hashed password for the email in bytes
    if stored_hash_bytes is None: ### - if the email isn't in database check function returns none
            return render_template("landing.html", error="Email or Password not found")

    user_bytes_password = password.encode('utf-8')
    if bcrypt.checkpw(user_bytes_password, stored_hash_bytes): ### --- takes the salt from the stored_hash_bytes and hashes user_password with same salt and compares results
        session["current_user"] = email
        return redirect(url_for("dashboard"))
    
    return render_template("landing.html", error="Email or Password not found")
          

    

### --- LOADS CREATE_USER PAGE
@app.route("/create_user", methods=["GET"])
def new_user():
    return render_template("create_user.html")
    
### --- ADDS EMAIL AND PASSWORD TO DATABASE
@app.route("/register", methods=["POST"])
def register():
    email = request.form.get("email", "")
    password = request.form.get("password", "")

    if email and password:
        hashed = helpers.cipher(password) 
        helpers.add(email, hashed)
        session["current_user"] = email
        return redirect(url_for("dashboard",)) 
    else:
        return render_template("create_user.html", error="Please submit an email and password")
    

### --- Loads add timetable page
@app.route("/add_task", methods=["POST"])
def add_task():
    return redirect(url_for("load_add_task"))

@app.route("/load_add_task", methods=["GET"])
def load_add_task():
    return render_template("add_timetable.html")

### --- Creates timetable and stores it
@app.route("/create_task", methods=["POST"])
def create_task():
    today = date.today()
    timetable_name = request.form.get("name", "")
    duration = request.form.get("duration", "")
    start_str = request.form.get("start-date", "")
    end_str = request.form.get("end-date", "") 
    start_date = datetime.strptime(start_str, "%Y-%m-%d").date()
    end_date = datetime.strptime(end_str, "%Y-%m-%d").date()
    current_user = session["current_user"]
    user_id = helpers.get_user_id(current_user)
    if start_date < today:
        flash("Please enter valid date.")
        return redirect(url_for("load_add_task"))
    else:
        helpers.add_task(user_id, timetable_name, start_date, end_date, duration)
        return redirect(url_for("dashboard"))

### --- Deletes Timetable -------

@app.route("/delete_task", methods=["POST"])
def deletion():
    return redirect(url_for("load_delete"))

@app.route("/load_delete", methods=["GET"])
def load_delete():
    current_user = session.get("current_user")
    tasks = helpers.display(current_user)
    return render_template("delete_timetable.html", tasks=tasks)

@app.route("/delete", methods=["POST"])
def delete():
    current_user = session.get("current_user")
    if not current_user:
         return redirect(url_for("landing_page"))
    task_name = request.form.get("task")
    user_id = helpers.get_user_id(current_user)
    helpers.delete(user_id, task_name)
    return redirect(url_for("dashboard"))



if __name__ == "__main__":
    app.run(debug=True)
