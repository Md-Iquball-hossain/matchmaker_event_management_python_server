# # Author: Shidul Islam <shidul.m360ict@gmail.com>
# # Date: 10-11-2023
# # */

# import requests
# import json
# from utils.user_data import user_data
# from faker import Faker
# from utils.miscellaneous.status_code import status_code
# from utils.miscellaneous.response_message import status_message

# from config import API_BASE_URL

# # Create a Faker instance
# fake = Faker()

# LOGIN_ENDPOINT = "/auth/sign-up"


# ###### InValid test for Profile ######
# def test_signup_user_invalid_data():
#     invalid_user_data = [
#         {
#             "from_age": fake.random_int(),
#             "to_age": fake.random_int(),
#             "desired_religion": 'muslim',
#             "desired_country": "Bangladesh",
#             "desired_community": "Hindi",
#             "desired_occupation": "Defence",
#             "desired_education": "B.E/B.Tech",
#             "desired_language": "Bengali",
#             "desired_gender": "Male",
#         },
#         {
#             "username": fake.random_int(),
#             "email": fake.email(),
#             "password": fake.password(),
#             "phone_number": fake.random_int(),
#             "photo": fake.sentence(),
#             "date_of_birth": "1990-01-01",
#             "religion": "muslim",
#             "community": "Hindi",
#             "country": "Bangladesh",
#             "gender": "Male",
#             "education": "B.E/B.Tech",
#             "occupation": "Defence",
#             "about_me": fake.sentence(),
#             "language": "Bengali",
#         }

#     ]

#     # Send a POST request to the signup endpoint
#     res = requests.post(
#         f"{API_BASE_URL}{LOGIN_ENDPOINT}", json=invalid_user_data)

#     data = json.loads(res.content)

#     assert data['success'] == False
#     assert data['message'] == status_message['HTTP_UNPROCESSABLE_ENTITY']
#     assert res.status_code == status_code['HTTP_UNPROCESSABLE_ENTITY']


# ###### Valid test for Profile ######
