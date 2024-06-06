# # Author: Shidul Islam
# # Date: 10-18-2023
# # */

# import requests
# import json
# from faker import Faker
# from config import API_BASE_URL

# # Create a Faker instance
# fake = Faker()

# LOGIN_ENDPOINT = "/auth/login"


# ###### Valid test for Login ######
# def test_login_user():
#     login_data = {
#         "email": "masud.m360ict@gmail.com",
#         "password": "12345678"
#     }
#     # Send a POST request to the login endpoint
#     res = requests.post(
#         f"{API_BASE_URL}{LOGIN_ENDPOINT}", json=login_data)

#     data = json.loads(res.content)
#     assert isinstance(data['message'], str)
#     assert data['success'] == True
#     assert isinstance(data['token'], str)
#     assert res.status_code == 200


# def test_login_user_for_valid_credential():

#     login_data = {
#         "email": "masud.m360ict@gmail.com",
#         "password": "12345678"
#     }

#     # Send a POST request to the login endpoint
#     res = requests.post(
#         f"{API_BASE_URL}{LOGIN_ENDPOINT}", json=login_data)

#     data = json.loads(res.content)

#     conditions = [
#         type(data['message']) == str,
#         type(data['success']) == bool,
#         res.status_code == 200
#     ]
#     assert all(conditions)


# ###### Invalid test for Login ######
# def test_login_user_invalid_credential():

#     login_data = {
#         "email": "habijabi@gmail.com",
#         "password": "adfadf"
#     }

#     # Send a POST request to the login endpoint
#     res = requests.post(
#         f"{API_BASE_URL}{LOGIN_ENDPOINT}", json=login_data)

#     data = json.loads(res.content)
#     assert data['success'] == False
#     assert res.status_code == 401


# def test_login_user_invalid_password():

#     login_data = {
#         "email": "masud.m360ict@gmail.com",
#         "password": fake.password()
#     }

#     # Send a POST request to the login endpoint
#     res = requests.post(
#         f"{API_BASE_URL}{LOGIN_ENDPOINT}", json=login_data)

#     data = json.loads(res.content)
#     assert data['message'] == 'Login failed'
#     assert data['success'] == False
#     assert res.status_code == 401


# def test_login_user_invalid_email():

#     login_data = {
#         "email": "raha3ddiddddu@gmail.com",
#         "password": fake.password()
#     }

#     # Send a POST request to the login endpoint
#     res = requests.post(
#         f"{API_BASE_URL}{LOGIN_ENDPOINT}", json=login_data)

#     data = json.loads(res.content)
#     assert data['success'] == False
#     assert res.status_code == 401
