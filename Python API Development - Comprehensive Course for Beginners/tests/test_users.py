# import pytest
# from jose import jwt
# from app import schemas

# from app.config import settings


# # def test_root(client):

# #     res = client.get("/")
# #     print(res.json().get('message'))
# #     assert res.json().get('message') == 'Hello World'
# #     assert res.status_code == 200


# def test_create_user(client):
#     res = client.post(
#         "/users/", json={
#   "username": "subin_test_create_user",
#   "email":"subin_test_create_user@gmail.com",
#   "password":"password"
  
# })
#     print(f"res.json(): {res.json()}")
#     new_user = schemas.UserOut(**res.json())
#     assert new_user.email == "subin_test_create_user@gmail.com"
#     assert res.status_code == 201


# def test_login_user(client, test_user):
#     print(f"test_user: {test_user}")
#     res = client.post(
#         "/login", data={"username": test_user['email'], "password": test_user['password']})
#     print(f"res.json(): {res.json()}")
#     login_res = schemas.Token(**res.json())
#     print(f"login_res: {login_res}")
#     payload = jwt.decode(login_res.access_token,
#                          settings.secret_key, algorithms=[settings.algorithm])
#     print(f"payload: {payload}")
#     id = payload.get("id")
#     print(f"id: {id} and test_user['id']: {test_user['id']}")
#     assert id == test_user['id']
#     assert login_res.token_type == "bearer"
#     assert res.status_code == 200


# @pytest.mark.parametrize("email, password, status_code", [
#     ('wrongemail@gmail.com', 'password123', 404),
#     ('sanjeev@gmail.com', 'wrongpassword', 404),
#     ('wrongemail@gmail.com', 'wrongpassword', 404),
#     (None, 'password123', 422),
#     # ('sanjeev@gmail.com', None, 422)
# ])
# def test_incorrect_login(test_user, client, email, password, status_code):
#     res = client.post(
#         "/login", data={"username": email, "password": password})

#     assert res.status_code == status_code
#     # assert res.json().get('detail') == 'Invalid Credentials'