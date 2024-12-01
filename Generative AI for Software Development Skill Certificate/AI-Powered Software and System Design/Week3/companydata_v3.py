import sqlite3
from datetime import datetime, timedelta
import random

# Singleton Pattern for Database Connection
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

db_connection = DatabaseConnection('company_database.db')
conn = DatabaseConnection.get_connection()
cursor = conn.cursor()

# Create the companies table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS companies (
    id INTEGER PRIMARY KEY,
    ticker TEXT NOT NULL,
    name TEXT NOT NULL
)
''')

# Synthesize data for 10 companies
companies = [
    (1, 'AAPL', 'Apple Inc.'),
    (2, 'GOOGL', 'Alphabet Inc.'),
    (3, 'MSFT', 'Microsoft Corporation'),
    (4, 'AMZN', 'Amazon.com Inc.'),
    (5, 'TSLA', 'Tesla Inc.'),
    (6, 'FB', 'Meta Platforms Inc.'),
    (7, 'NVDA', 'NVIDIA Corporation'),
    (8, 'NFLX', 'Netflix Inc.'),
    (9, 'ADBE', 'Adobe Inc.'),
    (10, 'ORCL', 'Oracle Corporation')
]

# Insert data into the companies table
cursor.executemany('''
INSERT OR IGNORE INTO companies (id, ticker, name)
VALUES (?, ?, ?)
''', companies)

# Create the TimeSeries table
cursor.execute('''
CREATE TABLE IF NOT EXISTS TimeSeries (
    id INTEGER PRIMARY KEY,
    company_id INTEGER,
    value REAL,
    date TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(id)
)
''')

# Generate synthetic data for TimeSeries table
start_date = datetime(2023, 1, 1)
num_entries = 100

time_series_data = []

for company in companies:
    company_id = company[0]
    for i in range(num_entries):
        date = start_date + timedelta(days=i)
        value = round(random.uniform(100, 500), 2)  # Generate a random value between 100 and 500
        time_series_data.append((company_id, value, date.strftime('%Y-%m-%d')))

# Insert data into the TimeSeries table
cursor.executemany('''
INSERT INTO TimeSeries (company_id, value, date)
VALUES (?, ?, ?)
''', time_series_data)

# CODE TO IMPLEMENT THE FACTORY PATTERN FOR COMPANY CREATION
# Insert data into the TimeSeries table
cursor.executemany('''
INSERT INTO TimeSeries (company_id, value, date)
VALUES (?, ?, ?)
''', time_series_data)

# Insert synthesized foreign companies
foreign_companies = [
    (1001, 'ZZZZ', 'Foreign Company A'),
    (1002, 'ZZZZ', 'Foreign Company B')
]
cursor.executemany('INSERT INTO companies (id, ticker, name) VALUES (?, ?, ?)', foreign_companies)

# Function to generate time series data
def generate_time_series(company_id, start_date, num_days, initial_value):
    date_list = [start_date + timedelta(days=x) for x in range(num_days)]
    value_list = initial_value + np.random.normal(0, 1, num_days).cumsum()
    return [(company_id, date.strftime('%Y-%m-%d'), value) for date, value in zip(date_list, value_list)]

# Generate 100 data points for each foreign company
start_date = datetime(2023, 1, 1)
time_series_data = generate_time_series(1001, start_date, 100, 100.0)
time_series_data += generate_time_series(1002, start_date, 100, 200.0)

# Insert synthesized time series data for foreign companies
cursor.executemany('INSERT INTO TimeSeries (company_id, date, value) VALUES (?, ?, ?)', time_series_data)

# Commit the transaction and close the connection
conn.commit()

# Define the Bollinger Band width as a global variable
bollinger_width = 2

# Define the Window Size for Movine Average
window_size = 20

class Company:
    def __init__(self, company_id, ticker, name):
        self.company_id = company_id
        self.ticker = ticker
        self.name = name
        self.time_series = None
        self.high_bollinger = None
        self.low_bollinger = None
        self.moving_average = None
        self.grade = None

    def load_time_series(self, conn):
        query = '''
        SELECT date, value
        FROM TimeSeries
        WHERE company_id = ?
        ORDER BY date
        '''
        self.time_series = pd.read_sql_query(query, conn, params=(self.company_id,))
        self.time_series['date'] = pd.to_datetime(self.time_series['date'])

    def calculate_bollinger_bands(self):
        rolling_mean = self.time_series['value'].rolling(window_size).mean()
        rolling_std = self.time_series['value'].rolling(window_size).std()
        self.moving_average = rolling_mean
        self.high_bollinger = rolling_mean + (rolling_std * bollinger_width)
        self.low_bollinger = rolling_mean - (rolling_std * bollinger_width)

    def assign_grade(self):
        latest_value = self.time_series['value'].iloc[-1]
        if latest_value > self.high_bollinger.iloc[-1]:
            self.grade = 'A'
        elif latest_value < self.low_bollinger.iloc[-1]:
            self.grade = 'C'
        else:
            self.grade = 'B'

    def display(self):
        print(f'Company: {self.name} ({self.ticker})')
        print(f'Grade: {self.grade}')
        print('Time Series Data:')
        print(self.time_series.tail())
        print('Moving Average:')
        print(self.moving_average.tail())
        print('High Bollinger Band:')
        print(self.high_bollinger.tail())
        print('Low Bollinger Band:')
        print(self.low_bollinger.tail())

def get_company_by_ticker(ticker, conn):
    cursor = conn.cursor()
    query = 'SELECT id, ticker, name FROM companies WHERE ticker = ?'
    cursor.execute(query, (ticker,))
    row = cursor.fetchone()
    if row:
        return Company(row[0], row[1], row[2])

def get_company_by_ticker_or_id(identifier, conn):
    cursor = conn.cursor()
    if isinstance(identifier, int):
        query = 'SELECT id, ticker, name FROM companies WHERE id = ?'
        cursor.execute(query, (identifier,))
    else:
        query = 'SELECT id, ticker, name FROM companies WHERE ticker = ?'
        cursor.execute(query, (identifier,))
    row = cursor.fetchone()
    if row:
        return Company(row[0], row[1], row[2])
    else:
        return None

# Example usage:
conn = sqlite3.connect('company_database.db')

# Get company by ticker or ID
company = get_company_by_ticker('GOOGL', conn)
if company:
    company.load_time_series(conn)
    company.calculate_bollinger_bands()
    company.assign_grade()
    company.display()

# Concrete classes for company creation
class DomesticCompany(Company):
    def __init__(self, company_id, ticker, name):
        super().__init__(company_id, ticker, name)
        self.company_type = 'Domestic'

class ForeignCompany(Company):
    def __init__(self, company_id, ticker, name):
        super().__init__(company_id, ticker, name)
        self.company_type = 'Foreign'

# Company Factory class code
class CompanyFactory:
    @staticmethod
    def get_company(identifier, conn):
        cursor = conn.cursor()

        if isinstance(identifier, str):
            query = 'SELECT id, ticker, name FROM companies WHERE ticker = ?'
            cursor.execute(query, (identifier,))
            row = cursor.fetchone()
            if row:
                return DomesticCompany(row[0], row[1], row[2])
        else:
            query = 'SELECT id, ticker, name FROM companies WHERE id = ?'
            cursor.execute(query, (identifier,))
            row = cursor.fetchone()
            if row:
                # If ticker is equal to ZZZZ, it's a foreign company
                if row[1] == 'ZZZZ':
                    return ForeignCompany(row[0], row[1], row[2])
                else:
                    return DomesticCompany(row[0], row[1], row[2])
        return None


# Get domestic company by ticker
try:
    domestic_company = CompanyFactory.get_company('AAPL', conn)
    if domestic_company:
        domestic_company.load_time_series(conn)
        domestic_company.calculate_bollinger_bands()
        domestic_company.display()
    else:
        print("Domestic company not found")
except Exception as e:
    print(f"Error processing domestic company: {e}")

# Get foreign company by ID
try:
    foreign_company = CompanyFactory.get_company(1001, conn)
    if foreign_company:
        foreign_company.load_time_series(conn)
        foreign_company.calculate_bollinger_bands()
        foreign_company.display()
    else:
        print("Foreign company not found")
except Exception as e:
    print(f"Error processing foreign company: {e}")

#Print the name and type of each company you just created
print(f"The name of the domestic company is: {domestic_company.name}")
print(f"{domestic_company.name} is a {domestic_company.company_type} company.")
print(f"The name of the foreign company is: {foreign_company.name}")
print(f"{foreign_company.name} is a {foreign_company.company_type} company.")

conn.close()