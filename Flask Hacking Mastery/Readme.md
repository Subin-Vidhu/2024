# Flask Hacking Mastery

Create venv [```python -m venv virtualenvName```], activate the venv, install the necessary dependencies.

# Hello World

First, make sure you've installed Flask.

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

# Routing explained

Imagine your Flask app is like a house.

Each route is like a door to a room in that house.

When you create a route in Flask:

You're deciding where a new door goes.

You're also deciding what visitors will see when they enter through that door.

For example, the @app.route('/'):

This is like the front door of your house.

When visitors come to the front door (main page), they see whatever you decided to show in the associated function, like "Hello, World!".

If you add another route, like @app.route('/kitchen'):

Now you have a door to the kitchen.

Visitors see something different when they enter the kitchen, maybe "Here's where we make cookies!".

So, routing is like setting up doors and deciding what's behind each one! 🚪🏠🍪

# Dynamic routes explained

Imagine you run a magical pet store where each pet says its name when you poke it.

A dog would say, "Woof! I'm Dog!"

A cat would purr, "Meow! I'm Cat!"

Now, imagine your Flask app is like this store, and each dynamic route is like a magic poke on a pet.

Instead of setting up a special poke for every single pet, you have a magic poke that works on ANY pet. You just say the pet's name, and it responds!

In Flask, a dynamic route lets you do this magic. Instead of making a separate route for dogs, cats, birds, and so on, you make ONE route:

```pythonCopy code
@app.route('/poke/<pet_name>')
When you visit /poke/dog, it's like poking the dog, and you might see "Woof! I'm Dog!". And if you visit /poke/cat, it's like poking the cat, leading to "Meow! I'm Cat!".
``````
So, a dynamic route is like a magical tool that adjusts its behavior based on the pet's name you tell it! ✨