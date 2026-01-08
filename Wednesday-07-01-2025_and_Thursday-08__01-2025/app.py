from flask import Flask, session, redirect, url_for, request, render_template

app = Flask(__name__)

app.secret_key = "life"

########################night 1###########################################################
@app.route("/login/")
def login():
    session["username"] = "Chinedu"
    return redirect(url_for("get_sesh"))


@app.route("/dashboard/")
def get_sesh():
    return session.get("username", "No user stored")

#########################################################################Night 2


@app.route("/", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        age = request.form.get("age", "").strip()
        hobbies = request.form.getlist("hobbies")

        session["profile"] = {
            "name": name,
            "age": age,
            "hobbies": [h.strip() for h in hobbies if h.strip()]
        }
        return redirect(url_for("display"))

    return render_template("form.html")


@app.route("/display/", methods=["GET", "POST"])
def display():
    profile = session.get("profile")
    return render_template("display.html", profile=profile)






if __name__ == "__main__":
    app.run(debug=True)