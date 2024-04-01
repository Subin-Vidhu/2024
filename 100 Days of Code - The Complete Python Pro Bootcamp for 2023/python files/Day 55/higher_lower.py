import random 
from flask import Flask
app=Flask(__name__)

random_number=random.randint(0,9)

@app.route('/')
def home_page():
    return '<h1>Guess a number between 0 and 9</h1>'\
    '<img src="https://media.giphy.com/media/3o7aCSPqXE5C6T8tBC/giphy.gif">'


@app.route("/<int:user_guess>")
def guessing_number(user_guess):
    if user_guess>9:
        return '<h1 style="color:red">Please guess numbers between 0 to 9 only!!</h1>'\
            '<br>'\
            '<br>'\
            '<img src="https://media.giphy.com/media/3taYXLxSBOugHHjocB/giphy.gif" width=350 height=300>'

    else:
        if user_guess < random_number:
            return '<h1 style="color:red">Too low,try again!</h1>'\
                '<br>'\
                '<br>'\
                '<img src="https://media.giphy.com/media/jnQYWZ0T4mkhCmkzcn/giphy.gif">'

        elif user_guess > random_number:
            return '<h1 style="color:orange">Too high,try again!</h1>'\
                '<br>'\
                '<br>'\
                '<img src="https://media.giphy.com/media/Qvm2704d1Dqus/giphy.gif">'
            
        else:
            return '<h1 style="color:green">You found me!</h1>'\
                '<br>'\
                '<br>'\
                '<img src="https://media.giphy.com/media/cXblnKXr2BQOaYnTni/giphy.gif" width=350 height=300>'



if __name__ == "__main__":
    app.run(debug=True)  