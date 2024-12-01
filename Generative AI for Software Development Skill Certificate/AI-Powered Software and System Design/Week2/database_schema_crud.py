from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship 
import pickle

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    orders = relationship("Order", back_populates="user")

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)
    order_items = relationship("OrderItem", back_populates="product")

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = 'order_items'
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer)
    order = relationship("Order", back_populates="order_items")
    product = relationship("Product", back_populates="order_items")

## You may replace echo = False to not display debugging messages.
engine = create_engine('sqlite:///ecommerce.db', echo=False)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


## USER TABLE CRUD
# Create
def add_user(name, email):
    new_user = User(name=name, email=email)
    session.add(new_user)
    session.commit()

# Read
def get_user(user_id):
    return session.query(User).filter(User.id == user_id).first()

# Update
def update_user(user_id, name=None, email=None):
    user = session.query(User).filter(User.id == user_id).first()
    if user:
        if name:
            user.name = name
        if email:
            user.email = email
        session.commit()

# Delete
def delete_user(user_id):
    user = session.query(User).filter(User.id == user_id).first()
    if user:
        session.delete(user)
        session.commit()

## PRODUCT TABLE CRUD
# Create
def add_product(name, price):
    new_product = Product(name=name, price=price)
    session.add(new_product)
    session.commit()

# Read
def get_product(product_id):
    return session.query(Product).filter(Product.id == product_id).first()

# Update
def update_product(product_id, name=None, price=None):
    product = session.query(Product).filter(Product.id == product_id).first()
    if product:
        if name:
            product.name = name
        if price:
            product.price = price
        session.commit()

# Delete
def delete_product(product_id):
    product = session.query(Product).filter(Product.id == product_id).first()
    if product:
        session.delete(product)
        session.commit()


## ORDERS TABLE CRUD
# Create
def add_order(user_id):
    new_order = Order(user_id=user_id)
    session.add(new_order)
    session.commit()

# Read
def get_order(order_id):
    return session.query(Order).filter(Order.id == order_id).first()

# Update
def update_order(order_id, user_id=None):
    order = session.query(Order).filter(Order.id == order_id).first()
    if order:
        if user_id:
            order.user_id = user_id
        session.commit()

# Delete
def delete_order(order_id):
    order = session.query(Order).filter(Order.id == order_id).first()
    if order:
        session.delete(order)
        session.commit()

## ORDER ITEMS CRUD
# Create
def add_order_item(order_id, product_id, quantity):
    new_order_item = OrderItem(order_id=order_id, product_id=product_id, quantity=quantity)
    session.add(new_order_item)
    session.commit()

# Read
def get_order_item(order_item_id):
    return session.query(OrderItem).filter(OrderItem.id == order_item_id).first()

# Update
def update_order_item(order_item_id, order_id=None, product_id=None, quantity=None):
    order_item = session.query(OrderItem).filter(OrderItem.id == order_item_id).first()
    if order_item:
        if order_id:
            order_item.order_id = order_id
        if product_id:
            order_item.product_id = product_id
        if quantity:
            order_item.quantity = quantity
        session.commit()

# Delete
def delete_order_item(order_item_id):
    order_item = session.query(OrderItem).filter(OrderItem.id == order_item_id).first()
    if order_item:
        session.delete(order_item)
        session.commit()

