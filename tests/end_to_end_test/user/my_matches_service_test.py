
# My matches service Test
# @Author Md Khairul Islam Ratul <khairul.m360ict@gmail.com>
# Date: 30-11-2023
from utils.miscellaneous.status_code import status_code
import requests
import json
from config import API_BASE_URL

# End point
MY_MATCHES_LIST = f'{API_BASE_URL}/user/my-matches?page=1&per_page=10 &filter_country=all&filter_religion=all&filter_occupation=all'
NEAR_ME_LIST = f'{API_BASE_URL}/user/near-me?filter_country=Bangladesh&filter_religion=muslim&filter_occupation=Defence'
TODAYS_MATCH = f'{API_BASE_URL}/user/todays-matches?page=&per_page='
MY_MATCHES_SINGLE_LIST  = f'{API_BASE_URL}/user/my-matches'

# Token
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyMywidXNlcm5hbWUiOiJraGFpcnVsMzMzIiwiZW1haWwiOiJrIiwicGhvbmVfbnVtYmVyIjoiMDE3MDc4NjM1NyJ9.iiMSO4ChzIXTs87w5r-9hAUyhoAYzB7l9L0702-oKvg"
headers = {'Authorization': f'Bearer {token}'}

# Test get my matches list Best Case
def test_get_my_matches_list_best_case():
    res = requests.get(MY_MATCHES_LIST, headers=headers)
    data = json.loads(res.content)

    conditions = [
        res.status_code == status_code['HTTP_OK'],
        data['success'] == True
    ]
    assert all(conditions)

# Test get my matches list Wrong Case1
def test_get_my_matches_list_wrong_case1():
    res = requests.get(MY_MATCHES_LIST)
    data = json.loads(res.content)

    conditions = [
        res.status_code == status_code['HTTP_UNAUTHORIZED'],
        data['success'] == False,
    ]
    assert all(conditions)

# Test get near me list Best Case
def test_get_near_me_list_best_case():
    res = requests.get(NEAR_ME_LIST, headers=headers)
    data = json.loads(res.content)

    conditions = [
        res.status_code == status_code['HTTP_OK'],
        data['success'] == True
    ]
    assert all(conditions)

# Test get near me list Wrong Case1
def test_get_near_me_list_wrong_case1():
    res = requests.get(NEAR_ME_LIST)
    data = json.loads(res.content)

    conditions = [
        res.status_code == status_code['HTTP_UNAUTHORIZED'],
        data['success'] == False,
    ]
    assert all(conditions)

# Test get todays match Best Case
def test_get_todays_match_best_case():
    res = requests.get(TODAYS_MATCH, headers=headers)
    data = json.loads(res.content)

    conditions = [
        res.status_code == status_code['HTTP_OK'],
        data['success'] == True
    ]
    assert all(conditions)

# Test get todays match Wrong Case1
def test_get_todays_match_wrong_case1():
    res = requests.get(TODAYS_MATCH)
    data = json.loads(res.content)

    conditions = [
        res.status_code == status_code['HTTP_UNAUTHORIZED'],
        data['success'] == False,
    ]
    assert all(conditions)

# Test get my matches single list Best Case
def test_get_my_matches_single_list_best_case():
    res = requests.get(MY_MATCHES_SINGLE_LIST, headers=headers)
    data = json.loads(res.content)

    conditions = [
        res.status_code == status_code['HTTP_OK'],
        data['success'] == True
    ]
    assert all(conditions)

# Test get my matches single list Wrong Case1
def test_get_my_matches_single_list_wrong_case1():
    res = requests.get(MY_MATCHES_SINGLE_LIST)
    data = json.loads(res.content)

    conditions = [
        res.status_code == status_code['HTTP_UNAUTHORIZED'],
        data['success'] == False,
    ]
    assert all(conditions)