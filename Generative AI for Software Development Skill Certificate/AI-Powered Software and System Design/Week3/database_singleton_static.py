# Singleton Pattern with staticmethod for Database Connection
class DatabaseConnection:
    _instance = None

    def __new__(cls, db_path):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance.connection = sqlite3.connect(db_path)
        return cls._instance

    @staticmethod
    def get_connection():
        if DatabaseConnection._instance is None:
            raise Exception("DatabaseConnection has not been initialized. Call DatabaseConnection(db_path) first.")
        return DatabaseConnection._instance.connection
