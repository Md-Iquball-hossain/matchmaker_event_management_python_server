# # Author: Shidul Islam <shidul.m360ict@gmail.com>
# # Date: 10-11-2023
# # */

# import requests
# import json
# from faker import Faker
# from config import API_BASE_URL

# fake = Faker()

# LOGIN_ENDPOINT = "/user/profile"
# token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyMSwidXNlcm5hbWUiOiJtb210YWogYmVndW0iLCJlbWFpbCI6ImkiLCJwaG9uZV9udW1iZXIiOiIwMTc3NzA0NDgzOCJ9.AJwqjd6KGTSTQilDSCFwptRcjg12K0uFHbsuurYEB3U"

# ###### Valid test for Profile ######
# def test_profile_user():
#     headers = {'Authorization': f'Bearer {token}'}

#     # Send a GET request to the login endpoint
#     res = requests.get(
#         f"{API_BASE_URL}{LOGIN_ENDPOINT}", headers=headers)

#     data = json.loads(res.content)
#     assert data['success'] == True
#     assert res.status_code == 200


# ###### Invalid test for Profile ######
# def test_profile_invalid_token():
#     headers = {'Authorization': f'Bearer {fake.email}'}

#     # Send a GET request to the login endpoint
#     res = requests.get(
#         f"{API_BASE_URL}{LOGIN_ENDPOINT}", headers=headers)

#     data = json.loads(res.content)
#     assert data['success'] == False
#     assert res.status_code == 401
