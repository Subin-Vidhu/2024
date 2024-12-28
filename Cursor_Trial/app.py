from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone, timedelta
import json

# Define Indian Timezone (UTC+5:30)
IST = timezone(timedelta(hours=5, minutes=30))

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
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(IST))
    completed = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'created_at': self.created_at.astimezone(IST).strftime('%Y-%m-%d %H:%M'),
            'completed': self.completed
        }

class TaskHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('todo.id'), nullable=True)
    action = db.Column(db.String(20), nullable=False)  # 'created', 'completed', 'uncompleted', 'deleted'
    task_title = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(IST))

    def to_dict(self):
        return {
            'id': self.id,
            'task_id': self.task_id,
            'action': self.action,
            'task_title': self.task_title,
            'timestamp': self.timestamp.astimezone(IST).strftime('%Y-%m-%d %H:%M')
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

        # Record history
        history = TaskHistory(
            task_id=new_todo.id,
            action='created',
            task_title=title
        )
        db.session.add(history)
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
    
    # Record history
    action = 'completed' if todo.completed else 'uncompleted'
    history = TaskHistory(
        task_id=todo.id,
        action=action,
        task_title=todo.title
    )
    db.session.add(history)
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
    
    # Record history before deletion
    history = TaskHistory(
        task_id=None,  # Set to None since task will be deleted
        action='deleted',
        task_title=todo.title
    )
    db.session.add(history)
    
    db.session.delete(todo)
    db.session.commit()
    
    return jsonify({
        'error': False,
        'message': 'Deleted task'
    })

@app.route('/history')
def get_history():
    history = TaskHistory.query.order_by(TaskHistory.timestamp.desc()).all()
    return jsonify({
        'error': False,
        'history': [item.to_dict() for item in history]
    })

@app.route('/delete-all', methods=['POST'])
def delete_all():
    todos = Todo.query.all()
    count = len(todos)
    
    if count == 0:
        return jsonify({
            'error': True,
            'message': 'No tasks to delete'
        })

    # Record history for each deletion
    for todo in todos:
        history = TaskHistory(
            task_id=None,
            action='deleted',
            task_title=todo.title
        )
        db.session.add(history)
    
    # Delete all todos
    Todo.query.delete()
    db.session.commit()
    
    return jsonify({
        'error': False,
        'message': f'Deleted {count} tasks'
    })

@app.route('/complete-all', methods=['POST'])
def complete_all():
    todos = Todo.query.filter_by(completed=False).all()
    count = len(todos)
    
    if count == 0:
        return jsonify({
            'error': True,
            'message': 'No incomplete tasks found'
        })

    # Complete all incomplete todos and record history
    for todo in todos:
        todo.completed = True
        history = TaskHistory(
            task_id=todo.id,
            action='completed',
            task_title=todo.title
        )
        db.session.add(history)
    
    db.session.commit()
    
    return jsonify({
        'error': False,
        'message': f'Completed {count} tasks',
        'todos': [todo.to_dict() for todo in todos]
    })

if __name__ == '__main__':
    app.run(debug=True) 