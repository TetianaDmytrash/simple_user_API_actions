"""
    describe all get requests
"""
import logging
import requests
import pytest
import json

from connect import *
from constants import *


def test_main():
    assert 1 == 1


@pytest.mark.parametrize("test_input,expected", [("3+5", 8), ("2+4", 6), ("6*9", 42)])
def test_eval(test_input, expected):
    assert eval(test_input) == expected


def test_positive_get_all_users_status_code():
    try:
        response = get_all_users(GET_ALL_USERS_LINK)
        assert response.status_code == 200, f"status code: {response.status_code}"
    except requests.exceptions.RequestException as e:
        logging.error(f"Error occurred during registration: {e}")


# decorator
@pytest.mark.parametrize("firstName, lastName, email, completed, username, password, summary", [
    ("name1", "surname1", "test1@example.com", True, "test1", "password123", "simple text 1"),
])
def test_positive_create_user_status_code(firstName, lastName, email, completed, username, password, summary):
    headers = configure_headers()
    payload = configure_payload(firstName,
                                lastName,
                                email,
                                completed,
                                username,
                                password,
                                summary)
    try:
        response = create_user(POST_USER_LINK, headers, payload)
        assert response.status_code == 201, f"status code: {response.status_code}"
    except requests.exceptions.RequestException as e:
        logging.error(f"Error occurred during registration: {e}")
    list_user_uid = get_users_uid(convert_response_to_json(get_all_users(GET_ALL_USERS_LINK)))
    for uid in list_user_uid:
        delete_user_by_uid(DELETE_USER_LINK, uid)


@pytest.mark.parametrize("firstName, lastName, email, completed, username, password, summary", [
    ("name1", "surname1", "test1@example.com", False, "test1", "password123", "simple text 1"),
])
def test_positive_create_user_correct_save(firstName, lastName, email, completed, username, password, summary):
    headers, payload = configure_headers_payload(firstName,
                                                 lastName,
                                                 email,
                                                 completed,
                                                 username,
                                                 password,
                                                 summary)
    try:
        create_user(POST_USER_LINK, headers, payload)
    except requests.exceptions.RequestException as e:
        logging.error(f"Error occurred during registration: {e}")
    payload = json.loads(payload)
    print(type(payload))
    print(payload)
    response_data = convert_response_to_json(get_all_users(GET_ALL_USERS_LINK))
    for r_data in response_data:
        print(type(r_data))
        assert r_data["firstName"] == payload["firstName"]
        assert r_data["lastName"] == payload["lastName"]
        assert r_data["email"] == payload["email"]
        assert r_data["completed"] == payload["completed"]
        assert r_data["username"] == payload["username"]
        assert r_data["password"] == payload["password"]
        assert r_data["summary"] == payload["summary"]
    # ????
    list_user_uid = get_users_uid(response_data)
    for uid in list_user_uid:
        delete_user_by_uid(DELETE_USER_LINK, uid)


def test_positive_delete_users_status_code():
    # simple creation user without checking
    list_user_uid = get_users_uid(convert_response_to_json(get_all_users(GET_ALL_USERS_LINK)))
    for uid in list_user_uid:
        response_delete_user = delete_user_by_uid(DELETE_USER_LINK, uid)
        assert response_delete_user.status_code == 204, f"status code: {response_delete_user.status_code}"


@pytest.mark.parametrize("firstName, lastName, email, completed, username, password, summary", [
    ("name1", "surname1", "test1@example.com", True, "test1", "password123", "simple text 1"),
    ("name2", "surname2", "test2@example.com", True, "test2", "password123", "simple text 2"),
    ("name3", "surname3", "test3@example.com", True, "test3", "password123", "simple text 3"),
])
def test_positive_create_users(firstName, lastName, email, completed, username, password, summary):
    payload = json.dumps({
        "firstName": firstName,
        "lastName": lastName,
        "email": email,
        "completed": completed,
        "username": username,
        "password": password,
        "summary": summary
    })
    headers = {
        'Content-Type': 'application/json'
    }

    try:
        response = create_user(POST_USER_LINK, headers, payload)
        assert response.status_code == 201, f"status code: {response.status_code}"
    except requests.exceptions.RequestException as e:
        logging.error(f"Error occurred during registration: {e}")
