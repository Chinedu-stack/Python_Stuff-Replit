from flask import Flask, request, render_template, redirect, url_for, session
from werkzeug.utils import secure_filename
import os
import bcrypt
import sqlite3
import base64
app = Flask(__name__)
conn = None
cursor = None



### --- OPEN DATABASE
def open_db():
    global conn, cursor
    conn = sqlite3.connect("study_tracker.db")
    cursor = conn.cursor()

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
    ascii_password = base64.b64encode(hashed).decode('utf-8')
    return ascii_password

### --- ADD TO DATABASE
def add(email, hashed_password):
    open_db()
    cursor.execute("INSERT INTO users (email, hashed_password) VALUES (?,?)", (email, hashed_password))
    close_db()

### --- CHECKING USERS AND PASSWORDS
def check(email):
    open_db()
    cursor.execute("SELECT hashed_password FROM users WHERE email = ?", (email))
    ascii_password = cursor.fetchone()
    hashed_password = base64.b64decode(ascii_password)
    close_db()
    return hashed_password