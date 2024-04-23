# Flask Hacking Mastery

 - Create venv [```python -m venv virtualenvName```]
 - activate the venv
 - install the necessary dependencies.

# Hello World

 - First, make sure you've installed Flask.

 - Create a file named hello.py (or any other name you like) and open it in your favorite text editor.

 - Add the following code to the file:

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

## Basically, we're setting up a small web page that says "Hello, World!" when you visit it. 🌍👋
``````



 - Run it with python hello.py and open http://127.0.0.1:5000/ with your web browser.

# Routing explained

 - Imagine your Flask app is like a house.

 - Each route is like a door to a room in that house.

 - When you create a route in Flask: You're deciding where a new door goes.

 - You're also deciding what visitors will see when they enter through that door.

 - For example, the @app.route('/'):

    - This is like the front door of your house.

    - When visitors come to the front door (main page), they see whatever you decided to show in the associated function, like "Hello, World!".

 - If you add another route, like @app.route('/kitchen'): Now you have a door to the kitchen.

 - Visitors see something different when they enter the kitchen, maybe "Here's where we make cookies!".

`So, routing is like setting up doors and deciding what's behind each one! 🚪🏠🍪`

# Dynamic routes explained

 - Imagine you run a magical pet store where each pet says its name when you poke it.

    - A dog would say, "Woof! I'm Dog!"

    - A cat would purr, "Meow! I'm Cat!"

 - Now, imagine your Flask app is like this store, and each dynamic route is like a magic poke on a pet.

    - Instead of setting up a special poke for every single pet, you have a magic poke that works on ANY pet. You just say the pet's name, and it responds!

 - In Flask, a dynamic route lets you do this magic. Instead of making a separate route for dogs, cats, birds, and so on, you make ONE route:

    ```pythonCopy code
    @app.route('/poke/<pet_name>')
    When you visit /poke/dog, it's like poking the dog, and you might see "Woof! I'm Dog!". And if you visit /poke/cat, it's like poking the cat, leading to "Meow! I'm Cat!".
    ```
`So, a dynamic route is like a magical tool that adjusts its behavior based on the pet's name you tell it! ✨`

# SSTI Explained 

 - Imagine you're at a store that customizes T-shirts. You provide them with a message, and they print it on the shirt for you.

 - Usually, you'd give them something simple like "Happy Birthday, Alex!" But one day, you figure out that if you give them a special sequence of symbols or words, their T-shirt machine starts acting weird. Maybe it displays the store's internal records, or perhaps it even starts printing shirts for free.

 - SSTI, or Server-Side Template Injection, is like finding that special sequence for the T-shirt machine, but for websites. Instead of just displaying what it should, the website starts showing or doing things it wasn't supposed to because of the sneaky input it got.

 - Refer Video [here](https://www.udemy.com/course/flask-hacking-mastery/learn/lecture/39956462#overview)

 - [Readme](https://medium.com/@nyomanpradipta120/ssti-in-flask-jinja2-20b068fdaeee)


#   Hacking

- In the realm of web applications, even the most streamlined frameworks like Flask can house vulnerabilities. Uncovering these vulnerabilities in Flask applications can aid both in enhancing security measures and understanding potential attack vectors.

    - Prerequisites:

        - Kali Linux Live USB

    - Recommended

        - Proficiency in Python programming.

        - A foundational understanding of Flask.

- Refer Video 

# What is Enumeration?

- Imagine your computer is a big house, and inside it are your personal treasures. Enumeration is like someone walking around that house, making a list of all the doors and windows to figure out the best way to get in.

- Refer Video [here](https://www.udemy.com/course/flask-hacking-mastery/learn/lecture/39950224#overview)

# Why Enumeration?

 - Let's say you know your front and back doors are always locked. But what about that tiny window in the basement or the attic door? You might forget about them. In the world of computers, there are many ways to get into a system. So, ethical hackers use enumeration to find every possible entry, even the ones you might not think of.

`In short: Enumeration is finding all the possible ways (ports) into the system`

# What is a Brute Force Attack?

 - Imagine you lost the key to your house. Instead of looking for the key, you decide to try every key on your keychain, one by one, until one fits. This approach of trying all possibilities until you find the right one is similar to a brute force attack in the world of computers.

# Hydra on Kali Linux?

Now, think of Hydra as a magic keychain that can produce thousands of keys per minute. And Kali Linux? It's like a special backpack filled with tools that hackers (both good and bad) carry around. Inside that backpack, Hydra is one of the favorite tools when they want to rapidly try many keys to unlock a door (or a password).

### In short: Using Hydra on Kali Linux for a brute force attack is like quickly trying thousands of keys from a magic keychain to open a locked door.

# What is SSTI Vulnerability?

Imagine your computer is like a bank, where tellers (your web application) process transactions based on forms customers submit. SSTI, or Server-Side Template Injection, is like a clever customer submitting a deceptive form that tricks the teller into doing unauthorized transactions or revealing confidential information.

# Why SSTI Vulnerability?

In a secure bank, tellers should verify all requests thoroughly before processing them. If they just process every form without checking, malicious individuals can exploit this lapse. In computer terms, when a web application doesn't scrutinize the data users send it and acts on it blindly, it can lead to harmful consequences like unauthorized access or data leaks.

### In short: SSTI Vulnerability is a loophole that allows someone to deceive a web application, much like a crafty customer in a bank fooling a teller.

# ConfigVars

Imagine your computer system as a bank vault. Now, every vault has a combination code that provides access. The configuration variables (ConfigVars) of your system are similar to that combination. An exposed ConfigVar is like accidentally leaving that combination code written on a sticky note attached to the vault door.

# Why is an Exposed ConfigVar Bad?

Just as anyone finding the vault's combination can easily access all the money inside, in the digital world, exposed ConfigVars can provide malicious individuals with critical information or access. This can lead to unauthorized actions, data theft, or even taking control of the entire system.

### In short: An exposed ConfigVar is a dangerous slip, much like leaving the combination of a bank vault out in the open.