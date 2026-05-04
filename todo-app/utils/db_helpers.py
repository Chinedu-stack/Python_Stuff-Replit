from flask import Flask
import os
import sqlite3


db_path = os.path.join("todo-app", "db", "database.db")


### --- OPEN DATABASE 
def open_db():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    return conn, cursor


### --- CLOSE DATABASE (now requires conn)
def close_db(conn):
    conn.commit()
    conn.close()
