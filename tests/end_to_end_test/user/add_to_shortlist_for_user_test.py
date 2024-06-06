
# Add to shortlist Test
# @Author Md Khairul Islam Ratul <khairul.m360ict@gmail.com>
# Date: 30-11-2023
from utils.miscellaneous.status_code import status_code
import sys
sys.path.append("tests")
from data_for_testing.add_to_shortlist_for_user_data import (add_to_shortlist_best_data,
                                                             remove_from_favorite_list_best_data)
import requests
import json
from config import API_BASE_URL

# End point
ADD_TO_SHORTLIST = f'{API_BASE_URL}/user/add-favourite?id=138'
GET_FAVORITE_LIST = f'{API_BASE_URL}/user/get-favourite-list'
REMOVE_FAVORITE_LIST = f'{API_BASE_URL}/user/add-dislike?id=138'

# Token
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyMywidXNlcm5hbWUiOiJraGFpcnVsMzMzIiwiZW1haWwiOiJrIiwicGhvbmVfbnVtYmVyIjoiMDE3MDc4NjM1NyJ9.iiMSO4ChzIXTs87w5r-9hAUyhoAYzB7l9L0702-oKvg"
headers = {'Authorization': f'Bearer {token}'}

# Test add to shortlist Best Case
def test_add_to_shortlist_best_case():
    payload = add_to_shortlist_best_data()
    res = requests.post(ADD_TO_SHORTLIST, json=payload, headers=headers)
    data = json.loads(res.content)

    conditions = [
        res.status_code == status_code['HTTP_OK'],
        data['success'] == True
    ]
    assert all(conditions)

# Test add to shortlist Wrong Case1
def test_add_to_shortlist_wrong_case1():
    payload = add_to_shortlist_best_data()
    res = requests.post(ADD_TO_SHORTLIST, json=payload, headers=headers)
    data = json.loads(res.content)

    conditions = [
        res.status_code == status_code['HTTP_NOT_FOUND'], #if same id
        data['success'] == False,
    ]
    assert all(conditions)

# Test add to shortlist Wrong Case2
def test_add_to_shortlist_wrong_case2():
    payload = add_to_shortlist_best_data()
    res = requests.post(ADD_TO_SHORTLIST, json=payload)
    data = json.loads(res.content)

    conditions = [
        res.status_code == status_code['HTTP_UNAUTHORIZED'],
        data['success'] == False,
    ]
    assert all(conditions)

# Test get favorite list Best Case
def test_get_favorite_list_best_case():
    res = requests.get(GET_FAVORITE_LIST, headers=headers)
    data = json.loads(res.content)

    conditions = [
        res.status_code == status_code['HTTP_OK'],
        data['success'] == True
    ]
    assert all(conditions)

# Test get favorite list Wrong Case1
def test_get_favorite_list_wrong_case1():
    res = requests.get(GET_FAVORITE_LIST)
    data = json.loads(res.content)

    conditions = [
        res.status_code == status_code['HTTP_UNAUTHORIZED'],
        data['success'] == False,
    ]
    assert all(conditions)

# Test remove from favorite list Best Case
def test_remove_from_favorite_list_best_case():
    payload = remove_from_favorite_list_best_data()
    res = requests.delete(REMOVE_FAVORITE_LIST, json=payload, headers=headers)
    data = json.loads(res.content)

    conditions = [
        res.status_code == status_code['HTTP_OK'],
        data['success'] == True
    ]
    assert all(conditions)

# Test remove from favorite list Wrong Case1
def test_remove_from_favorite_list_wrong_case1():
    payload = remove_from_favorite_list_best_data()
    res = requests.delete(REMOVE_FAVORITE_LIST, json=payload)
    data = json.loads(res.content)

    conditions = [
        res.status_code == status_code['HTTP_UNAUTHORIZED'],
        data['success'] == False,
    ]
    assert all(conditions)