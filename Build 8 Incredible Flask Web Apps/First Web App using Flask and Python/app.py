from flask import Flask,render_template
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')
    # return "Welcome to my Flask web app!"

@app.route('/about')
def about():
    return "This is my Flask web app!"