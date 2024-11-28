tasks = []

def add_task(task):
    tasks.append(task)
    return f"Task '{task}' added."

def remove_task(task):
    if task in tasks:
        tasks.remove(task)
        return f"Task '{task}' removed."
    else:
        return "Task not found."

def list_tasks():
    return tasks

# Example usage
print(add_task("Buy groceries"))
print(add_task("Read a book"))
print(list_tasks())
print(remove_task("Read a book"))
print(list_tasks())

# As an expert software tester, write code that converts the output of the exploratory testing into functional tests using the unittest module in python.

import unittest

# Assuming the functions are imported from the module where they are defined
# from your_module import add_task, remove_task, list_tasks

tasks = []  # Reset the global tasks list for testing

class TestTaskFunctions(unittest.TestCase):

    def setUp(self):
        # Reset the tasks list before each test
        global tasks
        tasks = []

    def test_add_task(self):
        result = add_task("Buy groceries")
        self.assertEqual(result, "Task 'Buy groceries' added.")
        self.assertIn("Buy groceries", list_tasks())

    def test_add_duplicate_task(self):
        add_task("Read a book")
        result = add_task("Read a book")
        # Assuming we want to allow duplicates, check if both are added
        self.assertEqual(result, "Task 'Read a book' added.")
        self.assertEqual(list_tasks().count("Read a book"), 2)

    def test_remove_task(self):
        add_task("Buy groceries")
        result = remove_task("Buy groceries")
        self.assertEqual(result, "Task 'Buy groceries' removed.")
        self.assertNotIn("Buy groceries", list_tasks())

    def test_remove_nonexistent_task(self):
        result = remove_task("Nonexistent task")
        self.assertEqual(result, "Task not found.")

    def test_list_tasks(self):
        add_task("Buy groceries")
        add_task("Read a book")
        self.assertEqual(list_tasks(), ["Buy groceries", "Read a book"])

    def test_list_tasks_empty(self):
        self.assertEqual(list_tasks(), [])

if __name__ == '__main__':
    unittest.main()

# update the code to disallow adding an empty task. Then update the test case for adding an empty task to make sure it responds correctly when trying to add an empty task.

tasks = []

def add_task(task):
    if not task or not isinstance(task, str) or task.strip() == "":
        return "Task cannot be empty."
    tasks.append(task)
    return f"Task '{task}' added."

def remove_task(task):
    if task in tasks:
        tasks.remove(task)
        return f"Task '{task}' removed."
    else:
        return "Task not found."

def list_tasks():
    return tasks

# Example usage
print(add_task("Buy groceries"))
print(add_task("Read a book"))
print(list_tasks())
print(remove_task("Read a book"))
print(list_tasks())

import unittest

# Assuming the functions are imported from the module where they are defined
# from your_module import add_task, remove_task, list_tasks

tasks = []  # Reset the global tasks list for testing

class TestTaskFunctions(unittest.TestCase):

    def setUp(self):
        # Reset the tasks list before each test
        global tasks
        tasks = []

    def test_add_task(self):
        result = add_task("Buy groceries")
        self.assertEqual(result, "Task 'Buy groceries' added.")
        self.assertIn("Buy groceries", list_tasks())

    def test_add_duplicate_task(self):
        add_task("Read a book")
        result = add_task("Read a book")
        # Assuming we want to allow duplicates, check if both are added
        self.assertEqual(result, "Task 'Read a book' added.")
        self.assertEqual(list_tasks().count("Read a book"), 2)

    def test_add_empty_task(self):
        result = add_task("")
        self.assertEqual(result, "Task cannot be empty.")
        self.assertEqual(list_tasks(), [])

    def test_remove_task(self):
        add_task("Buy groceries")
        result = remove_task("Buy groceries")
        self.assertEqual(result, "Task 'Buy groceries' removed.")
        self.assertNotIn("Buy groceries", list_tasks())

    def test_remove_nonexistent_task(self):
        result = remove_task("Nonexistent task")
        self.assertEqual(result, "Task not found.")

    def test_list_tasks(self):
        add_task("Buy groceries")
        add_task("Read a book")
        self.assertEqual(list_tasks(), ["Buy groceries", "Read a book"])

    def test_list_tasks_empty(self):
        self.assertEqual(list_tasks(), [])

if __name__ == '__main__':
    unittest.main()