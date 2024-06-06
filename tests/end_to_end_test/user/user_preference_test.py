# # Author: Shidul Islam <shidul.m360ict@gmail.com>
# # Date: 10-11-2023
# # */

# import requests
# import json
# from faker import Faker
# import jwt
# from config import USER_SECRET
# from config import API_BASE_URL
# from utils.miscellaneous.status_code import status_code
# from utils.miscellaneous.response_message import status_message
# from utils.lib.lib import create_token

# # Create a Faker instance
# fake = Faker()

# LOGIN_ENDPOINT = "/user/user_preference"


# ####### Valid test for Login ######
# def test_user_preference_valid_credential():
#     token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyMSwidXNlcm5hbWUiOiJtb210YWogYmVndW0iLCJlbWFpbCI6ImkiLCJwaG9uZV9udW1iZXIiOiIwMTc3NzA0NDgzOCJ9.AJwqjd6KGTSTQilDSCFwptRcjg12K0uFHbsuurYEB3U"
#     headers = {'Authorization': f'Bearer {token}'}

#     # Send a GET request to the user preference endpoint
#     res = requests.get(
#         f"{API_BASE_URL}{LOGIN_ENDPOINT}", headers=headers)

#     data = json.loads(res.content)
#     assert isinstance(data['data']['desired_community'], str)
#     assert isinstance(data['data']['desired_country'], str)
#     assert isinstance(data['data']['desired_education'], str)
#     assert isinstance(data['data']['desired_gender'], str)
#     assert isinstance(data['data']['desired_language'], str)
#     assert isinstance(data['data']['desired_occupation'], str)
#     assert isinstance(data['data']['desired_religion'], str)
#     assert isinstance(data['data']['from_age'], int)
#     assert isinstance(data['data']['to_age'], int)
#     assert isinstance(data['message'], str)
#     assert isinstance(data['success'], bool)
#     assert res.status_code == 200


# # ###### Invalid test for Login ######
# def test_user_preference_Invalid_token():

#     token_data = {
#         "user_id": fake.random_number(digits=5),
#         "username": fake.first_name(),
#         "email": fake.email(),
#         "phone_number": fake.random_number(digits=5),
#     }

#     token = create_token(token_data, USER_SECRET)
#     headers = {'Authorization': f'Bearer {token}'}

#     # Send a POST request to the login endpoint
#     res = requests.get(
#         f"{API_BASE_URL}{LOGIN_ENDPOINT}", headers=headers)

#     data = json.loads(res.content)
#     assert data['message'] == 'The requested page could not be found but may be available again in the future'
#     assert data['success'] == False
#     assert res.status_code == 404


# def test_user_preference_invalid_user_id():

#     token_data = {
#         "users_id": 21,
#         "username": fake.first_name(),
#         "email": fake.email(),
#         "phone_number": fake.random_number(digits=5),
#     }

#     token = create_token(token_data, USER_SECRET)

#     # Send a POST request to the login endpoint
#     res = requests.get(
#         f"{API_BASE_URL}{LOGIN_ENDPOINT}", json=token)

#     data = json.loads(res.content)
#     assert data['message'] == 'The request was a legal request, but the server is refusing to respond to it. For use when authentication is possible but has failed or not yet been provided'
#     assert data['success'] == False
#     assert res.status_code == 401
