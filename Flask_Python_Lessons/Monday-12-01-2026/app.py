from flask import Flask, render_template, request, redirect, url_for, session, make_response

app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # Needed for sessions to work

@app.route("/", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "")
        if username:
            session["username"] = username
            return redirect(url_for("logged"))
        else:
            return render_template("login.html", error="Please enter a username")
    else:
        # If already logged in, redirect to dashboard
        if session.get("username"):
            return redirect(url_for("logged"))
        return render_template("login.html")

    
@app.route("/theme/", methods=["POST", "GET"])
def colors():
    theme = request.form.get("theme", "")
    if not theme:
        return redirect(url_for("logged"))
    resp = make_response(redirect(url_for("logged")))
    resp.set_cookie("theme", theme)

    return resp




@app.route("/signed_in")
def logged():
    theme = request.cookies.get("theme", "light")
    username = session.get("username", "")
    return render_template("logged_in.html", username=username, theme=theme)





if __name__ == "__main__":
    app.run(debug=True)
