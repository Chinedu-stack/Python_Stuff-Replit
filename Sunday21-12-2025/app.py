from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    name = "Chinedu"
    age = 14
    hobbies = ["Football", "Coding", "Reading"]
    return render_template('index.html', name=name, age=age, hobbies=hobbies)

if __name__ == "__main__":
    app.run(debug=True)

