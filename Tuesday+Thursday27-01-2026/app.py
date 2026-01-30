from flask import Flask, request, render_template, redirect, url_for, session
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = "your_random_secret_key"

# Where all uploads are stored
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

total = 0
@app.route("/")
def home():
    return render_template("session.html")

@app.route("/session_create/", methods = ["GET", "POST"])
def user():
    if request.method == "GET":
        return render_template("session.html")
    name = request.form.get("name","").strip
    if not name:
        error = "Please enter a name"
        return render_template("session.html", error=error)
    session["name"] = {"name": name, "files": []}
    return render_template("form.html")
    

@app.route("/file/", methods=["GET", "POST"])
def files():
    if request.method == "POST":
        uploaded_file = request.files.get("file")
        if uploaded_file and uploaded_file.filename != "":
            filename = secure_filename(uploaded_file.filename)

            # Add file to session
            session["name"]["files"].append(filename)
            session.modified = True

            # Save file in user-specific folder
            user_folder = os.path.join(app.config["UPLOAD_FOLDER"], session["name"]["name"])
            os.makedirs(user_folder, exist_ok=True)
            uploaded_file.save(os.path.join(user_folder, filename))

            # Use session list to display files
            user_files = session["name"]["files"]

            global total
            total += 1
            return render_template("display.html", total=total, files=user_files)

    return render_template("form.html")



if __name__ == "__main__":
    app.run(debug=True)
