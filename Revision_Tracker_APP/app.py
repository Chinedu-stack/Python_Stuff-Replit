from flask import Flask, request, render_template, redirect, url_for, session
from werkzeug.utils import secure_filename
import os
import bcrypt
import sqlite3
import helpers
app = Flask(__name__)
conn = None
cursor = None
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir,"Database_Folder", "study_tracker.db") ### --- makes sure the db is made in the same folder as the app.py


### --- LOADS THE LANDING PAGE
@app.route("/", methods=["GET"])
def landing_page():
    return render_template("landing.html")

### --- LOADS THE DASHBOARD
@app.route("/dashboard", methods=["GET"])
def dashboard():
    msg = request.args.get('msg')
    return render_template("dashboard.html", msg=msg)

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
        return redirect(url_for("dashboard", msg="Login successful! Chinedu is currently building the dashboard." ))
    
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
        return redirect(url_for("dashboard", msg="Account created! Chinedu is currently building the dashboard." )) ### --- CREATE DASHBOARD
    else:
        return render_template("create_user.html", error="Please submit an email and password")
    

@app.route("/logout", methods=["POST"])
def logout():
    return redirect(url_for("landing_page"))

if __name__ == "__main__":
    app.run(debug=True)
