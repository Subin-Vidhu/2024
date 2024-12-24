from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

# Load configuration from config.json
with open('config.json') as config_file:
    config = json.load(config_file)

app = Flask(__name__, static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = config['database']['uri']
app.config['SECRET_KEY'] = config['flask']['secret_key']
app.config['DEBUG'] = config['flask']['debug']
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M'),
            'completed': self.completed
        }

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    todos = Todo.query.order_by(Todo.created_at.desc()).all()
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title')
    if title:
        # Check for duplicate
        existing_todo = Todo.query.filter_by(title=title).first()
        if existing_todo:
            return jsonify({
                'error': True,
                'message': 'This task already exists'
            }), 400
        
        new_todo = Todo(title=title)
        db.session.add(new_todo)
        db.session.commit()
        return jsonify({
            'error': False,
            'message': 'Added new task',
            'todo': new_todo.to_dict()
        })
    return jsonify({'error': True, 'message': 'Title is required'}), 400

@app.route('/complete/<int:id>')
def complete(id):
    todo = Todo.query.get_or_404(id)
    todo.completed = not todo.completed
    db.session.commit()
    status = 'Completed task' if todo.completed else 'Uncompleted task'
    return jsonify({
        'error': False,
        'message': status,
        'todo': todo.to_dict()
    })

@app.route('/delete/<int:id>')
def delete(id):
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    return jsonify({
        'error': False,
        'message': 'Deleted task'
    })

if __name__ == '__main__':
    app.run(debug=True) 