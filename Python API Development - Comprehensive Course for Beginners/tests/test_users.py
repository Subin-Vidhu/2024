from app import schemas
from .database import client, session

# def test_root(client):

#     res = client.get("/")
#     print(res.json().get('message'))
#     assert res.json().get('message') == 'Hello World'
#     assert res.status_code == 200


def test_create_user(client):
    res = client.post(
        "/users/", json={"email": "hel123@gmail.com", "password": "passrd123", "username": "hel123"})
    print(f"Response: {res.json()}")
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "hel123@gmail.com"
    assert res.status_code == 200