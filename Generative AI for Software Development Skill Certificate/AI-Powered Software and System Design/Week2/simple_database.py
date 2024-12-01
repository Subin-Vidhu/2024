#pip install sqlalchemy
from sqlalchemy import create_engine

engine = create_engine('sqlite:///ecommerce.db', echo=True)

with engine.connect() as connection:
    result = connection.execute(text("SELECT 1"))
    # Fetch and print the result
    print(result.scalar()) # This should print 1 if the connection is successful