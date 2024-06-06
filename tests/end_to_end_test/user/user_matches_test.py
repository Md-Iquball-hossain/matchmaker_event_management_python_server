# # Author: Shidul Islam <shidul.m360ict@gmail.com>
# # Date: 10-11-2023
# # */

# import requests
# import json
# from faker import Faker
# from config import API_BASE_URL
# from config import USER_SECRET
# from utils.miscellaneous.status_code import status_code
# from utils.miscellaneous.response_message import status_message
# from utils.lib.lib import create_token

# # Create a Faker instance
# fake = Faker()

# LOGIN_ENDPOINT = "/user/my-matches"


# ###### Valid test for Matches ######
# def test_user_matches():
#     token_data = {
#         "user_id": 21,
#         "username": 'rahad-soup',
#         "email": 'rahaddiu@gmail.com',
#         "phone_number": '08978766544',
#     }

#     token = create_token(token_data, USER_SECRET)
#     headers = {'Authorization': f'Bearer {token}'}

#     # Send a POST request to the login endpoint
#     res = requests.get(
#         f"{API_BASE_URL}{LOGIN_ENDPOINT}", headers=headers)

#     data = json.loads(res.content)
#     print(data['data'][0])
#     assert isinstance(data['data'][0]['about_me'], str)
#     assert isinstance(data['data'][0]['community'], str)
#     assert isinstance(data['data'][0]['country'], str)
#     assert isinstance(data['data'][0]['date_of_birth'], str)
#     assert isinstance(data['data'][0]['education'], str)
#     assert isinstance(data['data'][0]['email'], str)
#     assert isinstance(data['data'][0]['gender'], str)
#     assert isinstance(data['data'][0]['language'], str)
#     assert isinstance(data['data'][0]['occupation'], str)
#     assert isinstance(data['data'][0]['phone_number'], str)
#     assert isinstance(data['data'][0]['photo'], str)
#     assert isinstance(data['data'][0]['religion'], str)
#     assert isinstance(data['data'][0]['username'], str)
#     assert data['success'] == True
#     assert data['message'] == status_message['HTTP_OK']
#     assert res.status_code == status_code['HTTP_OK']


# def test_user_matches_isArray():
#     token_data = {
#         "user_id": 21,
#         "username": 'rahad-soup',
#         "email": 'rahaddiu@gmail.com',
#         "phone_number": '08978766544',
#     }

#     token = create_token(token_data, USER_SECRET)
#     headers = {'Authorization': f'Bearer {token}'}

#     # Send a POST request to the login endpoint
#     res = requests.get(
#         f"{API_BASE_URL}{LOGIN_ENDPOINT}", headers=headers)

#     data = json.loads(res.content)
#     result = data['data']
#     assert type(data['data'] == result)
#     assert data['success'] == True
#     assert data['message'] == status_message['HTTP_OK']
#     assert res.status_code == status_code['HTTP_OK']


# ###### Invalid test for Matches ######
# def test_user_matches_inValid_token():
#     token_data = {
#         "user_id": fake.random_number(digits=1),
#         "username": fake.first_name(),
#         "email": fake.email(),
#         "phone_number": fake.random_number(digits=11),
#     }

#     token = create_token(token_data, USER_SECRET)
#     headers = {'Authorization': f'Bearer {token}'}

#     # Send a POST request to the login endpoint
#     res = requests.get(
#         f"{API_BASE_URL}{LOGIN_ENDPOINT}", headers=headers)

#     data = json.loads(res.content)

#     assert data['success'] == False
#     assert data['message'] == status_message['HTTP_INTERNAL_SERVER_ERROR']
#     assert res.status_code == status_code['HTTP_INTERNAL_SERVER_ERROR']
