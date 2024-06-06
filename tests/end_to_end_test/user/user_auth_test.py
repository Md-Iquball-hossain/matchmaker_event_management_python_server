# User Auth Test
# @Author Md Khairul Islam Ratul <khairul.m360ict@gmail.com>
# Date: 30-11-2023
from utils.miscellaneous.status_code import status_code
import sys
sys.path.append("tests")
from data_for_testing.user_auth_data import (user_login_best_data, user_login_wrong_data, user_sign_up_best_data,
                                             user_sign_up_wrong_data)
import requests
import json
from config import API_BASE_URL

# End point
USER_SIGN_UP = f'{API_BASE_URL}/auth/sign-up'
USER_LOGIN = f'{API_BASE_URL}/auth/login'

# Test Case User Sign Up Best Case
def test_user_sign_up_best_case():
    data, files = user_sign_up_best_data()
    res = requests.post(USER_SIGN_UP, data=data, files=files)
    data = json.loads(res.content)

    conditions = [
        res.status_code == status_code['HTTP_OK'],
        data['success'] == True
    ]
    assert all(conditions)

# Test Case User Sign Up Wrong Case
def test_user_sign_up_wrong_case():
    data, files = user_sign_up_wrong_data()
    res = requests.post(USER_SIGN_UP, data=data, files=files)
    data = json.loads(res.content)

    conditions = [
        res.status_code == status_code['HTTP_INTERNAL_SERVER_ERROR'],
        data['success'] == False,
    ]
    assert all(conditions)

# Test User Login Best Case
def test_user_login_best_case():
    payload = user_login_best_data()
    res = requests.post(USER_LOGIN, json=payload)
    data = json.loads(res.content)

    conditions = [
        res.status_code == status_code['HTTP_OK'],
        data['success'] == True,
        'token' in data
    ]
    assert all(conditions)

# Test User Login Wrong Case
def test_user_login_wrong_case():
    payload = user_login_wrong_data()
    res = requests.post(USER_LOGIN, json=payload)
    data = json.loads(res.content)

    conditions = [
        res.status_code == status_code['HTTP_UNAUTHORIZED'],
        data['success'] == False,
    ]
    assert all(conditions)