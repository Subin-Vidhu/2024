import json
import pytest
from app import app, db, Todo, TaskHistory

def test_index_page(client):
    """Test the index page loads correctly."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Radiologist Task Manager' in response.data

def test_add_task(client):
    """Test adding a new task."""
    # Test successful task addition
    response = client.post('/add', data={'title': 'New Task'})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['error'] == False
    assert data['message'] == 'Added new task'
    assert data['todo']['title'] == 'New Task'
    
    # Test duplicate task
    response = client.post('/add', data={'title': 'New Task'})
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['error'] == True
    assert 'already exists' in data['message']
    
    # Test empty title
    response = client.post('/add', data={'title': ''})
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['error'] == True
    assert data['message'] == 'Title is required'

def test_complete_task(client, sample_todo):
    """Test completing and uncompleting a task."""
    # Test completing
    response = client.get(f'/complete/{sample_todo.id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['todo']['completed'] == True
    
    # Test uncompleting
    response = client.get(f'/complete/{sample_todo.id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['todo']['completed'] == False
    
    # Test non-existent task
    response = client.get('/complete/999')
    assert response.status_code == 404

def test_delete_task(client, sample_todo):
    """Test deleting a task."""
    # Test successful deletion
    response = client.get(f'/delete/{sample_todo.id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['error'] == False
    assert data['message'] == 'Deleted task'
    
    # Verify task is deleted
    deleted_todo = db.session.get(Todo, sample_todo.id)
    assert deleted_todo is None
    
    # Test deleting non-existent task
    response = client.get('/delete/999')
    assert response.status_code == 404

def test_get_history(client, sample_history):
    """Test retrieving task history."""
    response = client.get('/history')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['error'] == False
    assert len(data['history']) == len(sample_history)
    # Verify the order (newest first)
    assert data['history'][0]['action'] == 'deleted'
    assert data['history'][1]['action'] == 'completed'
    assert data['history'][2]['action'] == 'created'

def test_delete_all(client, sample_todos):
    """Test deleting all tasks."""
    initial_count = len(sample_todos)
    
    # Test successful deletion
    response = client.post('/delete-all')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['error'] == False
    assert f'Deleted {initial_count} tasks' in data['message']
    
    # Verify all tasks are deleted
    remaining_todos = db.session.execute(db.select(Todo)).scalars().all()
    assert len(remaining_todos) == 0
    
    # Test when no tasks exist
    response = client.post('/delete-all')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['error'] == True
    assert data['message'] == 'No tasks to delete'

def test_complete_all(client, sample_todos):
    """Test completing all tasks."""
    # Test successful completion
    response = client.post('/complete-all')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['error'] == False
    assert 'Completed' in data['message']
    
    # Verify all tasks are completed
    incomplete_todos = db.session.execute(db.select(Todo).filter_by(completed=False)).scalars().all()
    assert len(incomplete_todos) == 0
    
    # Test when all tasks are already completed
    response = client.post('/complete-all')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['error'] == True
    assert data['message'] == 'No incomplete tasks found'

def test_clear_history(client, sample_history, app_config):
    """Test clearing task history."""
    initial_count = len(sample_history)
    
    # Test with invalid code
    response = client.post('/clear-history', 
                          json={'code': 'wrong-code'},
                          content_type='application/json')
    assert response.status_code == 403
    remaining_history = db.session.execute(db.select(TaskHistory)).scalars().all()
    assert len(remaining_history) == initial_count
    
    # Test with valid code
    response = client.post('/clear-history',
                          json={'code': app_config['ADMIN']['history_clear_code']},
                          content_type='application/json')
    assert response.status_code == 200
    remaining_history = db.session.execute(db.select(TaskHistory)).scalars().all()
    assert len(remaining_history) == 0 