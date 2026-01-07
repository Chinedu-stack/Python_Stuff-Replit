from flask import Flask, session, redirect, url_for

app = Flask(__name__)

app.secret_key = "life"


@app.route("/login/")
def login():
    session["username"] = "Chinedu"
    return redirect(url_for("get_sesh"))


@app.route("/dashboard/")
def get_sesh():
    return session.get("username", "No user stored")




if __name__ == "__main__":
    app.run(debug=True)