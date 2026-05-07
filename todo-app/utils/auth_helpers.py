from flask import Flask
import os
import bcrypt
import sqlite3
import base64
import utils.db_helpers as helpers

app = Flask(__name__)


### ========= SECURITY / PASSWORD HANDLING =========

### --- HASHES PASSWORDS
def cipher(password):
    password = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password, salt)
    b64_password = base64.b64encode(hashed).decode('utf-8')
    return b64_password


### ========= USER CREATION =========

### --- ADD USER TO DATABASE
def add(email, hashed_password):
    conn, cursor = helpers.open_db()
    cursor.execute("INSERT INTO users (email, hashed_password) VALUES (?,?)", (email, hashed_password))
    helpers.close_db(conn)


### ========= USER AUTH / CHECKING =========

### --- CHECKING USERS AND PASSWORDS
def check(email):
    conn, cursor = helpers.open_db()
    cursor.execute("SELECT hashed_password FROM users WHERE email = ?", (email,))
    b64_password = cursor.fetchone()

    if b64_password:
        b64_password_str = b64_password[0]
        hashed_password_bytes = base64.b64decode(b64_password_str)
        helpers.close_db(conn)
        return hashed_password_bytes
    else:
        helpers.close_db(conn)
        return None


### --- CHECK TO SEE IF EMAIL EXISTS WHEN CREATING NEW ACCOUNT
def check_email(email):
    conn, cursor = helpers.open_db()
    cursor.execute("""SELECT 1 FROM users
                   WHERE email = ?""", (email,))
    email_exists = cursor.fetchone()
    helpers.close_db(conn)

    if email_exists:
        return True
    return False

### --- Delete Account
def delete_account(email):
    conn, cursor = helpers.open_db()
    cursor.execute("""DELETE FROM users
                   WHERE email = ? """, (email,))
    helpers.close_db(conn)