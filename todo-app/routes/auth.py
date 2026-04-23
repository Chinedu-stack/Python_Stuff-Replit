from flask import Flask, flash, request, render_template, redirect, url_for, session, jsonify, Blueprint
import os
import utils.helpers as helpers
import bcrypt

auth_bp = Blueprint("auth", __name__)
auth_bp.secret_key = "Chinedu's_Key"
conn = None
cursor = None

@auth_bp.route("/", methods=["GET"])
def landing_page():
    return render_template("landing.html")


@auth_bp.route("/login", methods=["POST"])
def login():
    email = request.form.get("email", "")
    password = request.form.get("password", "")

    stored_hash_bytes = helpers.check(email) ### --- Returns the hashed password for the email in bytes
    if stored_hash_bytes is None: ### - if the email isn't in database check function returns none
            return render_template("landing.html", error="Email or Password not found")

    user_bytes_password = password.encode('utf- 8')
    if bcrypt.checkpw(user_bytes_password, stored_hash_bytes): ### --- takes the salt from the stored_hash_bytes and hashes user_password with same salt and compares results
        session["current_user"] = email
        return redirect(url_for("auth.show_dashboard"))
    
    return render_template("landing.html", error="Email or Password not found")



### --- LOADS CREATE_USER PAGE
@auth_bp.route("/create_user", methods=["GET"])
def new_user():
    return render_template("create_user.html")
    
### --- ADDS EMAIL AND PASSWORD TO DATABASE
@auth_bp.route("/register", methods=["POST"])
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
    return redirect(url_for("auth.show_dashboard")) 

@auth_bp.route("/show_dashboard", methods=["GET", "POST"])
def show_dashboard():
    return render_template("dashboard.html")
