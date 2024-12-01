from sqlalchemy import create_engine
engine = create_engine('sqlite:///ecommerce.db')

from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
metadata = MetaData()

users = Table('users', metadata,
              Column('id', Integer, primary_key=True),
              Column('name', String),
              Column('email', String, unique=True))

products = Table('products', metadata,
                 Column('id', Integer, primary_key=True),
                 Column('name', String),
                 Column('price', Integer))

orders = Table('orders', metadata,
               Column('id', Integer, primary_key=True),
               Column('user_id', Integer, ForeignKey('users.id')))

order_items = Table('order_items', metadata,
                    Column('id', Integer, primary_key=True),
                    Column('order_id', Integer, ForeignKey('orders.id')),
                    Column('product_id', Integer, ForeignKey('products.id')),
                    Column('quantity', Integer))

# Create all tables
metadata.create_all(engine)