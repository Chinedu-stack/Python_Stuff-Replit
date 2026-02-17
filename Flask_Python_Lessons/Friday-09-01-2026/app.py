from flask import Flask, request, redirect, make_response, render_template


app = Flask(__name__)  # create the Flask app




@app.route("/set-theme/<theme>")
def theme(theme):
    color = make_response(redirect("/"))
    color.set_cookie("theme", theme)
    return color

@app.route("/")
def home():
    theme = request.cookies.get("theme", "light")
    if theme == "blue":
        return "blue"
    else:
        return "default"




if __name__ == "__main__":
    app.run(debug=True)
