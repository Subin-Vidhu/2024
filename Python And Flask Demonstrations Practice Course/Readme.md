### Notes on Telegram [Revise]. Certificate on Drive.


 - Virtualenv creation, install flask

Flask Hello World

```
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello World"

if __name__ == "__main__":
    app.run(debug=True)   
```

Flask Variable Rules

```
@app.route('/hello/<name>')
def hello_world(name):
    return "Hello World %s!" %name
```
URL Building
```
from flask import Flask, redirect, url_for
app = Flask(__name__)

@app.route('/admin')
def hello_admin() :
    return 'Hello Admin'

@app.route('/guest/<guest>')
def hello_guest(guest):
    return 'Hello %s as Guest' %guest

@app.route('/user/<name>')
def hello_user (name) :
    if name=='admin':
       return redirect(url_for('hello_admin'))
    else:
       return redirect(url_for('hello_guest',guest=name))

if name == 'main':
   app.run(debug=True)
```

HTTP methods
```
from flask import Flask, redirect, url_for, request
app = Flask(__name_)

@app.route('/welcome/<name>')
def welcome(name):
  return 'welcome %s' %name

@app.route('/login',methods=['POST', 'GET'])
def login():
  if request.method=='POST':
    user=request.form['nm']
      return redirect(url_for('welcome',name=user))
  else:
    user=request.args.get('nm')
      return redirect(url_for('welcome',name=user))

if __name__ == '__main__':
  app.run(debug=True)
```
```
<html>
<body>
  <form action="http://localhost:5000/login" method="post">
  <p>Enter Name:</p>
  <p><input type="text" name="nm" /></p>
  <p><input type="submit" value="submit" /></p>
  </form>
</body>
</html>
```

Templates

 - ##### all html files should be inside the templates folder which should be in the same dir as your .py files

```
from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
  return render_template('hello.html')

if __name__ == '__main__':
  app.run(debug=True)
```

 - ##### static folder [all js, css, images and other files to be rendered has to be saved here], should be in the same dir as your .py files

 - hello.html
```
<html>
<head>
<script type = "text/javascript" src = "{{url_for('static', filename = 'js/hello.js')}}"></script>
</head>
<body>
<input type = "button" onclick = "sayHello()" value = "Say Hello" />
</body>
</html>
```
 - hello.js
```
function sayHello() {
  alert("Hello world")
}
```

Flask Request from Object
```
from flask import Flask, render template, request
app = Flask(__name__)

@app.route('/')
def student():
  return render_template('student.html')

@app.route('/result' methods = ['POST', 'GET'])
def result():
  if request.method == 'POST':
    result = request.form
    return render template ('result.html',result = result)

if __name__ == '__main__':
  app.run(debug = True)
```
 - student.html
```
<html>
<body>
  <form action = "http://localhost:5000/result" method = "POST">
    <p>Name</p>
    <p> <input type = "text" name = "Name" /></p>
    <p>Physics</p>
    <p> <input type = "text" name = "Physics" /></p>
    <p>chemistry</p>
    <p> <input Type = "text" name = "chemistry" /></p>
    <p>Maths</p>
    <p> <input type = "text" name = "Mathematics" /></p>
    <p><input type = "submit" value = "submit" /></p>
  </form>
</body>
</html>
```
 - result.html
```
<!doctype html>
<html>
<body>
  <table border = 1>
    {% for key, value in result.iteritems() %}
      <tr>
        <th> {{ key }} </th>
        <td> {{ value }} </td>          
      </tr>
    {% endfor %}
  </table>
</body>
</html>
```

Cookies

 - setcookie.html
```
<html>
<body>
  <form action = "/setcookie" method= "POST">
    <p><h3>Enter userID</h3></p>
    <p><input type = 'text' name = 'nm'/></p>
    <p><input type = 'submit' value = 'Login'/></p>
  </form>
</body>
</html>
```
 - app.py
```
from flask import Flask, render_template, request, make_response
app = Flask(__name__)

@app.route('/')
def index():
  return render_template('setcookie.html')

@app.route('/setcookie', methods = ['POST', 'GET'])
def setcookie():
  if request.method == 'POST':
      user = request.form['nm']
      resp = make_response(render_template('readcookie.html'))
      resp.set_cookie('userID', user)
      return resp

@app.route ('/getcookie')
def getcookie():
  name = request.cookies.get('userID')
  return '<h1>welcome '+name+'</h 1>'

if name == '__main__':
  app.run(debug = True)
```

 - readcookie.html
```
<!doctype html>
<html>
<body>
  <a href="http://localhost:5000/getcookie"><h2>click here to read cookie</h2></a>
</body>
</html>
```

Redirect and Errors

```
from flask import rlask, redirect, url_for, render_template, request
app = Flask(__name__)

@app.route ('/')
def index():
  return render_template('login.html')

@app.route('/login', methods = ['POST', 'GET'])
def login():
  if request.method == 'POST' and request.form['username'] == 'admin' :
    return redirect(url_for('success'))
  return redirect(url_for('index'))

@app.route('/success')
def success():
  return 'logged in successfully'
  
if __name__ == '__main__':
  app.run (debug = True)
```

Message Flashing
```
from flask import Flask, flash, redirect, render_template, request, url_for
app = Flask(__name__)

app.secret_key = 'random_string'
@app.route('/')
def index():
  return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
  error = None
  if request.method == 'POST':
    if request.form['username'] != 'admin' or \
      request.form['password'] != 'admin':
      error = 'Invalid username or password. Please try again!'
    else:
      flash('You were successfully logged in')
      flash('log out before login again')
      return redirect(url_for('index'))
  return render_template('log_in.html', error=error)

if __name__ == "__main__":
  app.run(debug=True)
```

 - log_in.html
```
<html> 
<body> 
<hl>Login</h1>
{% if error %} 
<p><strong>Error: </strong>{{ error }}
{% endif %} 
<form action = "" method = "post">
<dl>
<dt>Username: </dt>
<dd>
<input type = 'text' name = 'username' value = "{{request.form.username }}">
</dd>
<dt>Password: </dt>
<dd><input type = 'password' name = 'password'></dd>
</d1>
<p><input type = 'submit' value = 'Login'></p>
</form>
</body>
</html>
```
 - index.html
```
<!doctype html>
<html>
<head>
<title>Flask Message flashing</title>
</head>
<body>
<hl>Flask Message Flashing Example</hl>
{% with messages = get_flashed_messages() %}
{% if messages %}
<ul>
{% for message in messages %}
<1i>{{ message }}</1i>
{% endfor %}
</ul>
{% endif %}
{% endwith %}
<p>Do you want to <a href="{{ url_for('login') }}"><b>log in?</b></a>
</body>
</html>
```


File Uploading

 - upload.html
 ```
<html>
<body>
  <form action = "http://localhost:5000/uploader" method = "POST" enctype = "multipart/form-data">
    <input type = "file" name = "file" />
    <input type = "submit"/>
  </form>
</body>
</html>
```
 - upload.py
```
from flask import Flask, render_template, request
from werkzeug import secure_filename

app = Flask(__name__)

@app.route('/upload')
def upload():
  return render_template('upload.html')

@app.route ('/uploader', methods = ['GET', 'POST'])
def uploader():
if request.method == 'POST': 
 f = request.files['file']
 f.save(secure_filename(f.filename)) 
 return 'file uploaded successfully' 

if __name__ == '__main__ ': 
  app.run(debug = True)
```
Mail Extension
```   
from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)

mail = Mail(app)

app.config['MAIL_SERVER']='smtp.gmail.com"
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = ‘xyz@gmail.com'
app.config['MAIL_PASSWORD'] = '****'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

@app.route("/")
def index():
  msg = Message('Hello', sender = 'xyz@gmail.com', recipients = ['abc@gmail.com'])
  msg.body = "Hello Flask! This message is sent from Flask-Mail"
  mail.send(msg)
  return "Message Sent"

if __name__ == '__main__':
  app.run(debug = True)
```

WTF Extension

 - forms.py
```
from flask_wtf import Form
from wtforms import TextField, IntegerField, TextAreaField, SubmitField, RadioField, SelectField
from wtforms import validators, ValidationError

class ContactForm(Form) :
  name = TextField("Name Of Student", [validators.Required("Please enter your name.")])
  Gender = RadioField('Gender', choices = [('M','Male'), ('F', 'Female')])
  Address = TextAreaField("Address")
  email = TextField("Email", [validators.Required("Please enter your email address."), validators.Email("Please enter your email:)])
  Age = IntegerField("age")
  language = SelectField('Languages', choices = [('cpp', 'C++'), ('py', 'Python')])
  submit = SubmitField ("Send")
```

  - formexample.py

```
from flask import Flask, render_template, request, flash
from forms import ContactForm

app = Flask(__name__)

app.secret_key = "development_key"

@app.route('/contact', methods = ['GET', 'POST'])
def contact():
  form = ContactForm()
  if request.method == 'POST':
    if form.validate() == False:
      flash('All fields are required.')
      return render_template('contact.html', form = form)
    else:
      return render_template('success.html')
  if request.method == 'GET':
    return render_template('contact.html', form = form)

if __name__ == '__main__':
  app.run(debug = True)
```
 - contact.html

too long, refer video here [Link](https://www.udemy.com/course/python-and-flask-only-demonstration-course/learn/lecture/22468188#overview)

SQLite Database
```
import sqlite3 as sql
with sql.connect("database.db") as conn:
    cur = conn.cursor()
    cur.execute("INSERT INTO ...")
    conn.commit()
```
for code refer here [Link](https://www.udemy.com/course/python-and-flask-only-demonstration-course/learn/lecture/22468218#overview)

SQL Alchemy

  refer [here](https://www.udemy.com/course/python-and-flask-only-demonstration-course/learn/lecture/22468222#overview) ...