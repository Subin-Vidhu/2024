import pytest
from fastapi.testclient import TestClient
from app.main import app
from app import schemas
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.database import get_db, Base
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:password@localhost/FASTAPI" # Database URL
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}_test" # Database URL for testing
 
engine = create_engine(SQLALCHEMY_DATABASE_URL) # create a database engine

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # create a session

# Base = declarative_base() # create a base class



# Dependency
def overrirde_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = overrirde_get_db

@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine) # create the database before the test
    yield TestClient(app) # testing, yield helps in teardown
    Base.metadata.drop_all(bind=engine) # drop the database after the test

# def test_root(client):
#     res = client.get("/")
#     print(res.json().get('message'))
#     assert res.json().get('message') == 'Hello Aramis'
#     assert res.status_code == 200

def test_create_user(client):
    res = client.post(
        "/users/", json={"email": "hel123@gmail.com", "password": "passrd123", "username": "hel123"})

    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "hel123@gmail.com"
    assert res.status_code == 200