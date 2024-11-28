tasks = []

def add_task(task):
    if not task:
      raise ValueError("Task cannot be empty.")
    else:
      tasks.append(task)
    return tasks

def remove_task(task):
    if task in tasks:
        tasks.remove(task)
        return tasks
    else:
        return "Task not found."

def list_tasks():
    return tasks

def clear_tasks():
    tasks.clear()
    print(tasks)
    return "Tasks cleared."

# You are an expert in PyTest for automated testing of python code. Please amend this code with a comprehensive set of tests in Pytest to find bugs or
# otherissuesinthecode.

import pytest

# Import the functions to be tested
from your_module import add_task, remove_task, list_tasks, clear_tasks

def setup_function():
    # This function will be run before each test function to ensure a clean state
    clear_tasks()

def test_add_task():
    # Test adding a valid task
    result = add_task("Task 1")
    assert result == ["Task 1"]
    assert list_tasks() == ["Task 1"]

    # Test adding another valid task
    result = add_task("Task 2")
    assert result == ["Task 1", "Task 2"]
    assert list_tasks() == ["Task 1", "Task 2"]

    # Test adding an empty task
    with pytest.raises(ValueError, match="Task cannot be empty."):
        add_task("")

def test_remove_task():
    # Setup initial tasks
    add_task("Task 1")
    add_task("Task 2")

    # Test removing an existing task
    result = remove_task("Task 1")
    assert result == ["Task 2"]
    assert list_tasks() == ["Task 2"]

    # Test removing a non-existing task
    result = remove_task("Task 3")
    assert result == "Task not found."
    assert list_tasks() == ["Task 2"]

def test_list_tasks():
    # Test listing tasks when no tasks are present
    assert list_tasks() == []

    # Test listing tasks when tasks are present
    add_task("Task 1")
    add_task("Task 2")
    assert list_tasks() == ["Task 1", "Task 2"]

def test_clear_tasks():
    # Setup initial tasks
    add_task("Task 1")
    add_task("Task 2")

    # Test clearing tasks
    result = clear_tasks()
    assert result == "Tasks cleared."
    assert list_tasks() == []

# If you want to run the tests directly from this script, you can add the following:
# if __name__ == "__main__":
#     pytest.main()


# Instructions:
# Save your original code in a Python file, e.g., your_module.py.
# Save the above test code in a separate file, e.g., test_tasks.py.
# Run the test using PyTest by executing the command pytest test_tasks.py in your terminal.