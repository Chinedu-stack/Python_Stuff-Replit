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
    session["username"] = "Chinedu"
    return render_template("form.html")

@app.route("/file/", methods=["GET", "POST"])
def files():
    if request.method == "POST":
        uploaded_file = request.files.get("file","")
        if uploaded_file and uploaded_file.filename != "":
            filename = secure_filename(uploaded_file.filename)
            user_folder = os.path.join(app.config["UPLOAD_FOLDER"], session["username"])
            files = os.listdir(user_folder)
            os.makedirs(user_folder, exist_ok=True)
            uploaded_file.save(os.path.join(user_folder, filename))
            global total
            total += 1
            return render_template("display.html", total=total, files=files)
    return render_template("form.html")    


if __name__ == "__main__":
    app.run(debug=True)
