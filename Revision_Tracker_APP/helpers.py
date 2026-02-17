from flask import Flask, request, render_template, redirect, url_for, session
from werkzeug.utils import secure_filename
import os
import bcrypt
import sqlite3
import base64
app = Flask(__name__)
conn = None
cursor = None
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, "study_tracker.db")


### --- OPEN DATABASE
def open_db():
    global conn, cursor, db_path
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    return conn

### --- CLOSE DATABASE
def close_db():
    global conn, cursor
    conn.commit()
    conn.close()
    conn = None
    cursor = None  

### --- HASHES PASSWORDS
def cipher(password):
    password = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password, salt)
    b64_password = base64.b64encode(hashed).decode('utf-8')
    return b64_password

### --- ADD TO DATABASE
def add(email, hashed_password):
    open_db()
    cursor.execute("INSERT INTO users (email, hashed_password) VALUES (?,?)", (email, hashed_password))
    close_db()

### --- CHECKING USERS AND PASSWORDS
def check(email):
    open_db()
    cursor.execute("SELECT hashed_password FROM users WHERE email = ?", (email,))
    b64_password = cursor.fetchone()
    if b64_password:
        b64_password_str = b64_password[0] ### - takes 1 value from b64_password. Avoids tuple error
        hashed_password_bytes = base64.b64decode(b64_password_str)### converting b64 password to bytes
        close_db()
        return hashed_password_bytes
    else:
        close_db()
        return None