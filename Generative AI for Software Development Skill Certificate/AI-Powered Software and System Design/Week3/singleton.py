'''
# Original Singleton class
class Singleton:
    _instance = None

    @staticmethod
    def getInstance():
        if Singleton._instance is None:
            Singleton._instance = Singleton()
        return Singleton._instance

    def __init__(self):
        if Singleton._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            Singleton._instance = self
'''

# Updated Singleton
class Singleton:
    _instance = None

    def __init__(self):
        if Singleton._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            Singleton._instance = self
        self.configuration = {}

    @staticmethod
    def getInstance():
        if Singleton._instance is None:
            Singleton._instance = Singleton()
        return Singleton._instance

    def set_config(self, key, value):
        self.configuration[key] = value

    def get_config(self, key):
        return self.configuration.get(key, None)
    
    def display_config(self):
        for key, value in self.configuration.items():
            print(f"{key}: {value}")


# Setting configuration in one part of the application
singleton_instance = Singleton.getInstance()
singleton_instance.set_config('database', 'PostgreSQL')

# Accessing configuration in another part
another_instance = Singleton.getInstance()
another_instance.display_config()

# Both instances are the same
assert singleton_instance is another_instance
print("Instances are the same:", singleton_instance is another_instance)

