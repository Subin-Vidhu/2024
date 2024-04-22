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