from flask import Flask, render_template

app = Flask(__name__)

# Home page
@app.route('/')
def home():
    sports = ["football", "baseball", "Fooseball"]
    username = "Devonte"
    return render_template('home.html', username=username, sports=sports)

# About page
@app.route('/about/')
def about():
    return render_template('about.html')



@app.route('/profile/')
def login():
    username = "Jayden"
    hobbies = ["Eating", "Swimming", "Watching anime"]
    quote = "It's not about how many times you eat poo. It's about how many times you get back up - Some random Guy"
    is_admin = False
    return render_template('profile.html', username=username, hobbies=hobbies, quote=quote, is_admin=is_admin)







if __name__ == '__main__':
    app.run(debug=True)