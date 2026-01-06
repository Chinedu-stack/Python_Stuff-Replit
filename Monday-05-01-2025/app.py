from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# Folder where images will be saved
UPLOAD_FOLDER = os.path.join("static", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

file_types = {"png", "jpg"}

def valid_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in file_types


@app.route("/")
def home():
    return render_template("upload.html")


@app.route("/result/", methods=["POST", "GET"])
def process():
    if request.method == "POST":
        errors = []
        name = request.form.get("name", "").strip()
        uploaded_file = request.files.get("profile_pic")
        age = request.form.get("age", "")
        hobbies = request.form.getlist("hobbies")


        if not hobbies:
            errors.append("Must choose a hobby")


        if age.isdigit():
            age = int(age)
            if age > 100:
                errors.append("Age is too large")
        else:
            errors.append("Age must be a number")

        if uploaded_file and uploaded_file.filename != "" and valid_file(uploaded_file.filename):
            safe_name = secure_filename(uploaded_file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, safe_name)
            uploaded_file.save(file_path)
            filename = safe_name
        elif not uploaded_file:
            errors.append("No file uploaded.")
       
        else:
            errors.append("Incorrect file type. Must be .png or .jpg")

        if not name:
            errors.append("Name is not filled out")
        
        if errors:
            return render_template("upload.html", errors=errors)
        else:
            return redirect(url_for("profile", name=name, age=age, hobbies=", ".join(hobbies), filename=filename))

    else:
        return render_template("upload.html")
    

@app.route("/profile/")
def profile():
    name = request.args.get("name")
    age = request.args.get("age")
    hobbies = request.args.get("hobbies", "").split(", ")
    filename = request.args.get("filename")
    return render_template("profile.html",
                           name=name,
                           age=age,
                           hobbies=hobbies,
                           filename=filename)


if __name__ == "__main__":
    app.run(debug=True)
