# Flask Hacking Mastery

Create venv [```python -m venv virtualenvName```], activate the venv, install the necessary dependencies.

# Hello World

First, make sure you've installed Flask as I explained before.

Create a file named hello.py (or any other name you like) and open it in your favorite text editor.

Add the following code to the file:


``````
## Grab the tools we need from Flask.
from flask import Flask
 
## Make a tiny web app.
app = Flask(__name__)
 
## When someone visits the main page...
@app.route('/')
### ...show them this:
def hello_world():
    return 'Hello, World!'

``````
Basically, we're setting up a small web page that says "Hello, World!" when you visit it. 🌍👋

Run it with python hello.py and open http://127.0.0.1:5000/ with your web browser.

