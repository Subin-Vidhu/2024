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
    # SQLAlchemy 2.0 Select Pattern:
    # 1. Create select statement: db.select(Model)
    # 2. Add any filters/ordering: .order_by()
    # 3. Execute with session: db.session.execute()
    # 4. Convert to objects: .scalars().all()
    todos = db.session.execute(db.select(Todo).order_by(Todo.created_at.desc())).scalars().all()
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title')
    if not title:
        return jsonify({'error': True, 'message': 'Title is required'}), 400
        
    if len(title) > 100:  # Validate title length
        return jsonify({'error': True, 'message': 'Title must be 100 characters or less'}), 400
        
    # SQLAlchemy 2.0 Single Result Pattern:
    # 1. Create select with filter: db.select(Model).filter_by()
    # 2. Execute and get one or none: scalar_one_or_none()
    existing_todo = db.session.execute(db.select(Todo).filter_by(title=title)).scalar_one_or_none()
    if existing_todo:
        return jsonify({
            'error': True,
            'message': 'This task already exists'
        }), 400
    
    # SQLAlchemy 2.0 Insert Pattern:
    # 1. Create model instance
    # 2. Add to session
    # 3. Commit transaction
    new_todo = Todo(title=title)
    db.session.add(new_todo)
    db.session.commit()

    # Record history using same pattern
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

@app.route('/complete/<int:id>')
def complete(id):
    # SQLAlchemy 2.0 Get By Primary Key Pattern:
    # Use session.get() instead of Model.query.get()
    todo = db.session.get(Todo, id)
    if not todo:
        return jsonify({'error': True, 'message': 'Task not found'}), 404
    
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
    # SQLAlchemy 2.0 Get and Delete Pattern:
    # 1. Get object by primary key
    # 2. Delete using session.delete()
    todo = db.session.get(Todo, id)
    if not todo:
        return jsonify({'error': True, 'message': 'Task not found'}), 404
    
    # Record history before deletion
    history = TaskHistory(
        task_id=None,  # Set to None since task will be deleted
        action='deleted',
        task_title=todo.title
    )
    db.session.add(history)
    
    db.session.delete(todo)  # SQLAlchemy 2.0 delete pattern
    db.session.commit()
    
    return jsonify({
        'error': False,
        'message': 'Deleted task'
    })

@app.route('/history')
def get_history():
    # SQLAlchemy 2.0 Select with Order Pattern:
    # Combines select, ordering, and result conversion
    history = db.session.execute(
        db.select(TaskHistory)
        .order_by(TaskHistory.timestamp.desc())  # Chain criteria
    ).scalars().all()
    return jsonify({
        'error': False,
        'history': [item.to_dict() for item in history]
    })

@app.route('/delete-all', methods=['POST'])
def delete_all():
    # SQLAlchemy 2.0 Bulk Operations Pattern:
    # 1. Get all records: db.select()
    # 2. Delete all: db.delete()
    todos = db.session.execute(db.select(Todo)).scalars().all()
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
    
    # SQLAlchemy 2.0 Bulk Delete Pattern
    db.session.execute(db.delete(Todo))
    db.session.commit()
    
    return jsonify({
        'error': False,
        'message': f'Deleted {count} tasks'
    })

@app.route('/complete-all', methods=['POST'])
def complete_all():
    # SQLAlchemy 2.0 Select with Filter Pattern:
    # Combines select and filter in one statement
    todos = db.session.execute(
        db.select(Todo)
        .filter_by(completed=False)  # Chain filters
    ).scalars().all()
    count = len(todos)
    
    if count == 0:
        return jsonify({
            'error': True,
            'message': 'No incomplete tasks found'
        })

    # Bulk update with individual history records
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

@app.route('/clear-history', methods=['POST'])
def clear_history():
    try:
        if not request.is_json:
            return jsonify({
                'error': True,
                'message': 'Invalid content type, expected application/json'
            }), 400
            
        try:
            data = request.get_json()
        except:
            return jsonify({
                'error': True,
                'message': 'Invalid JSON format'
            }), 400
            
        # Get and verify the admin code
        admin_code = data.get('code') if data else None
        
        # Try to get code from app config first (for testing), then fall back to JSON config
        config_code = app.config.get('ADMIN', {}).get('history_clear_code') or config['admin']['history_clear_code']
        
        if not admin_code or admin_code != config_code:
            return jsonify({
                'error': True,
                'message': 'Invalid permission code'
            }), 403

        # SQLAlchemy 2.0 Bulk Delete Pattern
        db.session.execute(db.delete(TaskHistory))
        db.session.commit()
        return jsonify({
            'error': False,
            'message': 'History cleared successfully'
        })
    except Exception as e:
        return jsonify({
            'error': True,
            'message': 'Error clearing history'
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 