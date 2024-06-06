# # Author: Shidul Islam
# # Date: 10-21-2023
# # */

# from faker import Faker
# from app.auth.utils.auth_user import user_information_data, user_preference_data

# fake = Faker()


# user_data = {
#     "username": "red",
#     "email": "rahaddiu@gmail.com",
#     "password": "123456789",
#     "phone_number": "0179376654",
#     # "photo": "photo.jpg",
#     "date_of_birth": "1990-01-01",
#     "religion": "muslim",
#     "community": "Hindi",
#     "country": "Bangladesh",
#     "gender": "Male",
#     "education": "B.E/B.Tech",
#     "occupation": "Defence",
#     "about_me": "hello, its me",
#     "language": "Bengali",
# }

# user_preference = {
#     "desired_gender": "desired_gender",
#     "from_age": 20,
#     "to_age": 30,
#     "desired_country": "desired_country",
#     "desired_community": "desired_community",
#     "desired_occupation": "desired_occupation",
#     "desired_education": "desired_education",
#     "desired_language": "desired_language",
#     "desired_religion": "desired_religion",
# },

# user_information = user_information_data(user_data)
# user_preference = user_preference_data(user_preference)


# def test_user_information():
#     assert isinstance(user_information, object)


# def test_user_preference():
#     assert isinstance(user_preference, object)
