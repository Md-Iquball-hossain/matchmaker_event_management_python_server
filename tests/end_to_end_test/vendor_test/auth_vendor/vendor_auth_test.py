from tests.end_to_end_test.vendor_test.utils_vendor_test.miscellaneous import BASE_URL
import requests
from faker import Faker

fake = Faker()
#---------------------------------- Topics : vendor registration and login API pytest, Author: Md. Iquball Hossain, Date: 03-12-2023 ---------------------

# End points
ROUTE1 = f'{BASE_URL}/auth_vendor/sign-up'
ROUTE2 = f'{BASE_URL}/auth_vendor/log-in'

def test_auth_vendor_sign_up_correct():
    data = {
        "org_name": "Valid_Org_Name",
        "org_username": "mih_5669",
        "email": "example@example.com",
        "password": "123456789",
        "phone_number": "01777044900",
        "address": "Mirpur-11",
        "city": "Khulna",
        "country": "Bangladesh",
        "business_category": "Indoor Venue",
        "details": "My company",
    }
    r = requests.post(ROUTE1, json=data)
    assert r.status_code == 400, f"Expected status code 400, but received {r.status_code}"

def test_auth_vendor_sign_in_correct():
    data = {
        "email_or_username": "iquball.m360ict29@gmail.com",
        "password": "123456789"
    }
    r = requests.post(ROUTE2, json=data)
    assert r.status_code == 200

# python -m pytest "C:\Users\M360ICT\OneDrive\Desktop\match360_server-main\match360_server\tests\end_to_end_test\vendor_test\auth_vendor\vendor_auth_test.py"