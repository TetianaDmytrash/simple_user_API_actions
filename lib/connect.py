"""
    describe connect to site
"""
import json
import logging

import requests


def get_random_ingredients(kind=None):
    """
    Return a list of random ingredients as strings.

    :param kind: Optional "kind" of ingredients.
    :type kind: list[str] or None
    :raise customErrors.InvalidKindError: If the kind is invalid.
    :return: The ingredients list.
    :rtype: list[str]

    """
    return ["shells", "gorgonzola", "parsley"]


def get_all_users(url):
    """
    get all users method

    :param: url
    :type: string
    :return: response
    :rtype: xz
    """
    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        logging.error(f"Error during grap all users from database: {e}")
    try:
        response.raise_for_status()
        logging.info(f"Request was successful")
    except requests.exceptions.HTTPError as e:
        logging.error(f"HTTP error occurred: {e}")
    return response


def convert_response_to_json(response):
    """
    conversion server response in json format

    :param response
    :type: xz
    :return: response in json format
    :rtype: xz
    """
    return response.json()


def create_user(url, headers, data):
    """
    POST request for create user

    :param url: string
    :param headers: list[str]
    :param data: list[str]
    :return: response
    :rtype: xz
    """
    try:
        response = requests.post(url=url, headers=headers, data=data)
    except requests.exceptions.RequestException as e:
        logging.error(f"Error during create user and add data to database: {e}")
    return response


def configure_headers():
    """
    configure headers for post request

    :return: header
    :rtype: dict[str]
    """
    headers = {
        'Content-Type': 'application/json'
    }
    return headers


def configure_payload(firstname="testdata",
                      lastname="testdata",
                      email="testdata",
                      completed=False,
                      username="testdata",
                      password="testdata",
                      summary="testdata"):
    """
    configure json data for create new user

    :param firstname: has character limit (2 <= fN <= 10)
    :param lastname: has character limit (2 <= lN <= 10)
    :param email: standard email without special domain
    :param completed: boolean
    :param username: has character limit (2 <= uN <= 10)
    :param password: numbers | big/small letters | special symbols
    :param summary: short description
    :return: payload
    :rtype: dict[str]
    """
    payload = json.dumps({
        "firstName": firstname,
        "lastName": lastname,
        "email": email,
        "completed": completed,
        "username": username,
        "password": password,
        "summary": summary
    })
    return payload


def delete_user_by_uid(url, uid):
    """
    delete user by uid

    :param: url
    :type: str
    :param uid: string in special way
    :return: response
    :rtype: dict[str]
    """
    url += ("/" + str(uid))
    try:
        response = requests.delete(url=url)
    except requests.exceptions.RequestException as e:
        logging.error(f"Error during delete user from database: {e}")
    return response


def delete_all_users(get_url, delete_url):
    """
    delete all users

    :param: url
    :type: str
    :return: true
    :rtype: boolean
    """
    response_data = convert_response_to_json(get_all_users(get_url))
    list_user_uid = get_users_uid(response_data)
    for uid in list_user_uid:
        delete_user_by_uid(delete_url, uid)
    logging.info("Delete all users that were created in system")
    return True


def get_user_by_uid(url, uid):
    """
    get user by uid

    :param: url
    :type: str
    :param uid: string in special way
    :return: response
    :rtype: dict[str]
    """
    url += ("/" + str(uid))
    try:
        response = requests.get(url=url)
    except requests.exceptions.RequestException as e:
        logging.error(f"Error during get user from database: {e}")
    return response


def get_users_uid(response_data):
    """
    get uid all users that exist in system

    :param response_data:
    :return:
    """
    print(response_data)
    list_user_uid = [r_data["id"] for r_data in response_data]
    return list_user_uid


