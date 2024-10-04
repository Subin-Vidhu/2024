import pytest
from fastapi.testclient import TestClient
from app.main import app
from app import schemas
@pytest.fixture
def client():
    return TestClient(app)

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