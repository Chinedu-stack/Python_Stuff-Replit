from flask import Flask, request, render_template, redirect, url_for, session
from werkzeug.utils import secure_filename
import os
import bcrypt
import sqlite3
import helpers
app = Flask(__name__)
conn = None
cursor = None


### --- LOADS LOGIN PAGE
@app.route("/", methods=["GET"])
def landing_page():
    return render_template("login.html")

### --- CHECKS DATABASE FOR INPUTTED EMAIL AND PASSWORD
@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email", "")
    password = request.form.get("password", "")
    if email and password:
        stored_hash = helpers.check(email)
        if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
            return "Registration successful! Dashboard page coming soon."  ### -- BUILD THE DASHBOARD
        else:
            return render_template("login.html", error="Email or Password not found")
    else:
        return render_template("login.html", error="Please enter Email and Password")
    

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
        helpers.open_db()
        helpers.add(email, hashed)
        helpers.close_db()
        return "Registration successful! Dashboard coming soon." ### --- CREATE DASHBOARD
    else:
        return render_template("create_user.html", error="Please submit an email and password")
    

if __name__ == "__main__":
    app.run(debug=True)
