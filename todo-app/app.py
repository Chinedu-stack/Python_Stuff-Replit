from flask import Flask, flash, request, render_template, redirect, url_for, session, jsonify
import os
import bcrypt
import sqlite3
import helpers
from datetime import datetime, date
app = Flask(__name__)
app.secret_key = "my_super_secret_key_here"
conn = None
cursor = None


@app.route("/", methods=["GET"])
def landing_page():
    return render_template("landing.html")


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
    errors = []

    if not email or not password:
        errors.append("Please enter email and password")
    if helpers.check_email(email):
        errors.append("Email taken. Please use another email")
    
    if errors:
        return render_template("create_user.html", errors=errors) 
       
    hashed = helpers.cipher(password) 
    helpers.add(email, hashed)
    session["current_user"] = email
    return redirect(url_for("dashboard")) 

### --- LOADS THE DASHBOARD
@app.route("/dashboard", methods=["GET"])
def dashboard():     
    return render_template("dashboard.html")


if __name__ == "__main__":
    app.run(debug=True)