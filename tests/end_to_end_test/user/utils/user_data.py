import requests
import json
from faker import Faker
import random

# Create a Faker instance
fake = Faker()


# Fake data generate
user_data = [
    {
        "from_age": fake.random_int(),
        "to_age": fake.random_int(),
        "desired_religion": 'muslim',
        "desired_country": "Bangladesh",
        "desired_community": "Hindi",
        "desired_occupation": "Defence",
        "desired_education": "B.E/B.Tech",
        "desired_language": "Bengali",
        "desired_gender": "Male",
    },
    {
        "username": fake.word(),
        "email": fake.email(),
        "password": fake.password(),
        "phone_number": fake.random_int(),
        "photo": fake.sentence(),
        "date_of_birth": "1990-01-01",
        "religion": "muslim",
        "community": "Hindi",
        "country": "Bangladesh",
        "gender": "Male",
        "education": "B.E/B.Tech",
        "occupation": "Defence",
        "about_me": fake.sentence(),
        "language": "Bengali",
    }

]
