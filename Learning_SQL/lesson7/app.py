import sqlite3
from pathlib import Path

# Create database in current folder
basedir = Path(__file__).parent
conn = sqlite3.connect(basedir / "study_tracker_lesson7.db")
n = conn.cursor()


n.execute("""SELECT * FROM sessions
          ORDER BY hours DESC""")

stuff = n.fetchall()
for thing in stuff:
    print(thing)

print("--------------------------")
n.execute("""SELECT * FROM sessions
          ORDER BY subject ASC """)

stuff = n.fetchall()
for thing in stuff:
    print(thing) 


conn.commit()
print("sve")