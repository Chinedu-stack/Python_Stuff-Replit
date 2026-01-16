from flask import Flask, request, render_template, redirect, flash
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)           # Create the Flask app
app.secret_key = 'supersecret'  # Needed for flash messages

UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Make sure folder exists
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024  # 1 MB max file size
valid = {"png", "jpg"}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in valid



@app.route("/")
def home():
    return render_template("upload.html")

@app.route("/file/", methods=["POST", "GET"])
def validate():
    if request.method == "POST":
        file = request.files["file"]
        if not allowed_file(file.filename):
            flash("Not correct file type. Only JPG and PNG are valid")
            return redirect(request.url)
        if file.filename == "":
            flash("No file selected")
            return redirect(request.url)
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        flash("File successfully saved.")
        return redirect(request.url)
    return render_template("upload.html")



if __name__ == "__main__":
    app.run(debug=True)
