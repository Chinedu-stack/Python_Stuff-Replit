import sqlite3, os


# get the folder where this Python file is
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# create the path to app.db in the same folder
db_path = os.path.join(BASE_DIR, "app.db")


# connect to database (creates app.db if it doesn't exist)
conn = sqlite3.connect("app.db")
cursor = conn.cursor()

# create Subjects table
cursor.execute("""
CREATE TABLE IF NOT EXISTS subjects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
)
""")

# create Sessions table
cursor.execute("""
CREATE TABLE IF NOT EXISTS sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_id INTEGER,
    topic TEXT,
    hours REAL,
    date TEXT,
    FOREIGN KEY (subject_id) REFERENCES subjects(id)
)
""")

conn.commit()
conn.close()

print("Database and tables created")
