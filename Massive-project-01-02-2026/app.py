from flask import Flask, request, render_template, redirect, url_for, session
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = "your_random_secret_key"

# Where all uploads are stored
UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# User database
user_database = {}
total = 0

#------helper function to safely get the current user
def get_current_user():
    if not session:
        return None
    return next(iter(session.keys()))


# ------------------ HOME ------------------
@app.route("/")
def home():
    return render_template("create_user.html")


# ------------------ CREATE SESSION ------------------
@app.route("/session_create/", methods=["GET", "POST"])
def user():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        if not name:
            error = "Please enter a name"
            return render_template("create_user.html", error=error)

        session.setdefault(name, {"name": name, "files": []})
        # Redirect to dashboard instead of render_template to prevent resubmission
        return redirect(url_for("dashboard"))
    return render_template("create_user.html")


# ------------------ FILE UPLOAD ------------------
@app.route("/upload_file/", methods=["GET", "POST"])
def submit():
    return render_template("upload_files.html")


@app.route("/file/", methods=["POST"])
def files():
    uploaded_file = request.files.get("file", "")
    username = get_current_user()
    if not username:
        return redirect(url_for("home"))

    if uploaded_file and uploaded_file.filename != "":
        filename = secure_filename(uploaded_file.filename)

        # Add file to session
        session.setdefault(username, {"name": username, "files": []})["files"].append(filename)
        session.modified = True

        # Save file in user folder
        user_folder = os.path.join(app.config["UPLOAD_FOLDER"], username)
        os.makedirs(user_folder, exist_ok=True)
        uploaded_file.save(os.path.join(user_folder, filename))

    # Redirect to dashboard (PRG)
    return redirect(url_for("dashboard"))


# ------------------ DISPLAY ------------------
@app.route("/display/", methods=["GET", "POST"])
def display():
    username = get_current_user()
    if not username:
        return redirect(url_for("home"))
    files = session[username]["files"]
    total = len(files)
    return render_template("display.html", username=username, total=total, files=files)


# ------------------ DASHBOARD ------------------
@app.route("/dashboard/", methods=["GET"])
def dashboard():
    username = get_current_user()
    if not username:
        return redirect(url_for("home"))
    files = session[username]["files"]
    return render_template("dashboard.html", username=username, files=files)


@app.route("/load_dashboard/", methods=["POST"])
def dashboard_get():
    return redirect(url_for("dashboard"))

# ------------------ SWITCH USERS ------------------
@app.route("/switch_user/", methods=["POST"])
def switch_user():
    username = get_current_user()
    if not username:
        return redirect(url_for("home"))
    files = session[username]["files"]
    user_database.setdefault(username, {"name": username, "files": files})
    user_database[username]["files"] = list(session[username]["files"])

    session.clear()
    return redirect(url_for("load"))  # redirect to home to choose a new user

#  loads form to input name of user you want to login as
@app.route("/load_user/", methods=["POST", "GET"])
def load():
    return render_template("load.html")

# ------------------ CHECK USERS ------------------
@app.route("/check_users/", methods=["POST"])
def check():
    name = request.form.get("name", "").strip()
    if not name:
        error = "Please fill out the name box. Please try again"
        return render_template("load.html", error=error)

    if name in user_database:
        username = user_database[name]["name"]
        files = user_database[name]["files"]

        # Restore session fully
        session[username] = {"name": username, "files": files}
        return redirect(url_for("dashboard"))  # redirect to dashboard
    else:
        error = "Name is not found in the user database. Please try again."
        return render_template("load.html", error=error)


# ------------------ CREATE NEW USER ------------------
@app.route("/new_user/", methods=["POST"])
def new_user():
    username = list(session.keys())[0]
    user_database.setdefault(username, {"name": username, "files": []})
    user_database[username]["files"] = list(session[username]["files"])

    session.clear()
    return redirect(url_for("home"))  # redirect to create a new user


if __name__ == "__main__":
    app.run(debug=True)
