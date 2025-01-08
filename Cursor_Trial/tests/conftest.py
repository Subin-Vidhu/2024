import os
import tempfile
import pytest
from app import app, db, Todo, TaskHistory

@pytest.fixture(autouse=True)
def app_config():
    """Configure the application for testing."""
    app.config.update({
        'TESTING': True,
        'DEBUG': False,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SECRET_KEY': 'test-key',
        'ADMIN': {'history_clear_code': 'test-admin-code'}
    })
    return app.config

@pytest.fixture(autouse=True)
def clean_db():
    """Clean database before each test."""
    with app.app_context():
        db.session.query(TaskHistory).delete()
        db.session.query(Todo).delete()
        db.session.commit()

@pytest.fixture
def client():
    """Create a test client for the app."""
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client

@pytest.fixture
def sample_todo():
    """Create a sample todo item."""
    todo = Todo(title="Test Task")
    db.session.add(todo)
    db.session.commit()
    return todo

@pytest.fixture
def sample_todos():
    """Create multiple sample todo items."""
    todos = [
        Todo(title="Task 1"),
        Todo(title="Task 2", completed=True),
        Todo(title="Task 3")
    ]
    db.session.add_all(todos)
    db.session.commit()
    return todos

@pytest.fixture
def sample_history():
    """Create sample history entries in reverse chronological order (newest first)."""
    history_entries = [
        TaskHistory(task_title="Task 3", action="deleted"),
        TaskHistory(task_title="Task 2", action="completed"),
        TaskHistory(task_title="Task 1", action="created")
    ]
    db.session.add_all(history_entries)
    db.session.commit()
    return history_entries 