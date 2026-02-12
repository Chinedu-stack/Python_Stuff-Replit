from flask import Flask, request, render_template, redirect, url_for, session
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = "secret_key"

UPLOAD_FOLDER = os.path.join(app.root_path, "static", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


user_database = {}


# ------------------ GET CURRENT USER ------------------

def get_current_user():
    return session.get("current_user")


# ------------------ HOME ------------------

@app.route("/", methods=["GET"])
def home():
    return render_template("create_user.html")


# ------------------ CREATE USER (PRG) ------------------

@app.route("/create_user", methods=["POST"])
def create_user():
    name = request.form.get("name", "").strip()

    if not name:
        return render_template("create_user.html", error="Enter a name")

    session.clear()
    session["current_user"] = name
    session[name] = {"name": name, "files": []}
<<<<<<< HEAD:Uploading_Files_Project_01-02-2026/app.py
    #-----store user in database
    user_database[name] = {"name": name, "files":[]}  
=======
    user_database[name] = {"name":name, "files":[]}
>>>>>>> 16b5f46587088ac93ab84c144e9f519ccadf4ee8:Massive-project-01-02-2026/app.py

    return redirect(url_for("dashboard"))


# ------------------ DASHBOARD ------------------

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    username = get_current_user()
    if not username:
        return redirect(url_for("home"))

    files = session[username]["files"]
    return render_template("dashboard.html", username=username, files=files)


# ------------------ UPLOAD FILE (PRG) ------------------

@app.route("/file", methods=["POST"])
def upload():
    return render_template("upload_files.html")

@app.route("/upload", methods=["POST"])
def post_file():
    username = get_current_user()
    if not username:
        return redirect(url_for("home"))

    uploaded_file = request.files.get("file")

    if uploaded_file and uploaded_file.filename:
        filename = secure_filename(uploaded_file.filename)

        session[username]["files"].append(filename)
        session.modified = True

        user_folder = os.path.join(app.config["UPLOAD_FOLDER"], username)
        os.makedirs(user_folder, exist_ok=True)
        uploaded_file.save(os.path.join(user_folder, filename))
        return redirect(url_for("dashboard"))
    else:
        return render_template("upload_files.html", error="Please enter file name")


# ------------------ DISPLAY FILES ------------------

@app.route("/display", methods=["GET","POST"])
def display():
    username = get_current_user()
    if not username:
        return redirect(url_for("home"))

    files = session[username]["files"]
    return render_template(
        "display.html",
        username=username,
        files=files,
        total=len(files)
    )


# ------------------ SWITCH USER ------------------

@app.route("/switch_user", methods=["POST"])
def switch_user():
    username = get_current_user()
    if not username:
        return redirect(url_for("home"))
#--Save session info in database
    user_database[username] = {
        "name": username,
        "files": list(session[username]["files"])
    }
 
    return redirect(url_for("load_user"))


@app.route("/load_user", methods=["GET"])
def load_user():
    return render_template("load.html")

#-----------------Check If User to switch user exists---------------------

@app.route("/check_user", methods=["POST"])
def load_existing_user():
    name = request.form.get("name", "").strip()

    if not name:
            return render_template("load.html", error="Please enter user")
    if name not in user_database:
        return render_template("load.html", error="User not found")


    session.clear()
    session["current_user"] = name
    session[name] = user_database[name]

    return redirect(url_for("dashboard"))


# ------------------ NEW USER ------------------

@app.route("/new_user", methods=["POST"])
def new_user():
    session.clear()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
