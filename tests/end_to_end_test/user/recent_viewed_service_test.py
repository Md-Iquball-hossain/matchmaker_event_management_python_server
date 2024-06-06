
# Recent viewed service Test
# @Author Md Khairul Islam Ratul <khairul.m360ict@gmail.com>
# Date: 30-11-2023
from utils.miscellaneous.status_code import status_code
import requests
import json
from config import API_BASE_URL

# End point
RECENT_VIEWED = f'{API_BASE_URL}/user/recent-view?id=105'
GET_RECENT_VIEWS = f'{API_BASE_URL}/user/get-recent-view'
GET_RECENT_VISITOR = f'{API_BASE_URL}/user/get-recent-visitor'

# Token
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyMywidXNlcm5hbWUiOiJraGFpcnVsMzMzIiwiZW1haWwiOiJrIiwicGhvbmVfbnVtYmVyIjoiMDE3MDc4NjM1NyJ9.iiMSO4ChzIXTs87w5r-9hAUyhoAYzB7l9L0702-oKvg"
headers = {'Authorization': f'Bearer {token}'}

# Test recent viewed Best Case
def test_recent_viewed_best_case():
    res = requests.post(RECENT_VIEWED, headers=headers)
    data = json.loads(res.content)

    conditions = [
        res.status_code == status_code['HTTP_OK'],
        data['success'] == True
    ]
    assert all(conditions)

# Test recent viewed Wrong Case1
def test_recent_viewed_wrong_case1():
    res = requests.post(RECENT_VIEWED)
    data = json.loads(res.content)

    conditions = [
        res.status_code == status_code['HTTP_UNAUTHORIZED'],
        data['success'] == False,
    ]
    assert all(conditions)

# Test get recent views Best Case
def test_get_recent_views_best_case():
    res = requests.get(GET_RECENT_VIEWS, headers=headers)
    data = json.loads(res.content)

    conditions = [
        res.status_code == status_code['HTTP_OK'],
        data['success'] == True
    ]
    assert all(conditions)

# Test get recent views Wrong Case1
def test_get_recent_views_wrong_case1():
    res = requests.get(GET_RECENT_VIEWS)
    data = json.loads(res.content)

    conditions = [
        res.status_code == status_code['HTTP_UNAUTHORIZED'],
        data['success'] == False,
    ]
    assert all(conditions)

# Test get recent visitor Best Case
def test_get_recent_visitor_best_case():
    res = requests.get(GET_RECENT_VISITOR, headers=headers)
    data = json.loads(res.content)

    conditions = [
        res.status_code == status_code['HTTP_OK'],
        data['success'] == True
    ]
    assert all(conditions)

# Test get recent visitor Wrong Case1
def test_get_recent_visitor_wrong_case1():
    res = requests.get(GET_RECENT_VISITOR)
    data = json.loads(res.content)

    conditions = [
        res.status_code == status_code['HTTP_UNAUTHORIZED'],
        data['success'] == False,
    ]
    assert all(conditions)