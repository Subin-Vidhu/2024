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

# You are a software engineer and tester who is curious and who likes to go through code looking for edge cases. There's some Python code here -- please explore it and find any issues that might cause bugs or poor functionality: 

class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        if not isinstance(task, str):
            raise ValueError("Task must be a string.")
        if task in self.tasks:
            return f"Task '{task}' already exists."
        self.tasks.append(task)
        return f"Task '{task}' added."

    def remove_task(self, task):
        if task in self.tasks:
            self.tasks.remove(task)
            return f"Task '{task}' removed."
        else:
            return "Task not found."

    def list_tasks(self):
        return self.tasks

# Example usage
task_manager = TaskManager()
print(task_manager.add_task("Buy groceries"))
print(task_manager.add_task("Read a book"))
print(task_manager.list_tasks())
print(task_manager.remove_task("Read a book"))
print(task_manager.list_tasks())