from flask import Flask, request, render_template
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Absolute path for upload folder, safe across OS
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static/uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # create folder if missing
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def home():
    return render_template("upload.html")

@app.route("/upload/", methods=["POST", "GET"])
def upload():
    if request.method == "POST":
        file = request.files.get("user_file")  # safe way to get file
        if file and file.filename != "":
            filename = secure_filename(file.filename)  # remove unsafe characters
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            success = f"Your file '{filename}' has been uploaded successfully!"
            return render_template("upload.html", success=success)
        else:
            fail = "No file selected. Please try again."
            return render_template("upload.html", fail=fail)
    # GET request just shows the form
    return render_template("upload.html")

if __name__ == '__main__':
    app.run(debug=True)
