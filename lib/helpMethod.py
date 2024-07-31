"""
method that help in work with users
"""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))

import requests
import json

from generateRandomMethod import *
from logs.loggerConfig import setup_logger
from constants import GET_ALL_USERS_LINK

logger = setup_logger()
list_uid_created_user_for_one_test = []


def convert_json_string_in_dict(json_data):
    """
    conversion data in json format in dictionary

    :param json_data:
    :return: json data
    :rtype: dict
    """
    logger.debug(f"conversion json in dictionary")
    return json.loads(json_data)


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


def configure_payload_user_create(firstname="testdata",
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


def configure_payload_user_update(firstname="testdata",
                                  lastname="testdata",
                                  email="testdata",
                                  completed=False):
    """
    configure json data for create new user

    :param firstname: has character limit (2 <= fN <= 10)
    :param lastname: has character limit (2 <= lN <= 10)
    :param email: standard email without special domain
    :param completed: boolean
    :return: payload
    :rtype: dict[str]
    """
    payload = json.dumps({
        "firstName": firstname,
        "lastName": lastname,
        "email": email,
        "completed": completed
    })
    return payload


def get_all_users(get_url):
    """
    GET request: get all users
    :param get_url: url in string format
    :return: response
    """
    logger.debug(f"GET request: URL: {get_url}")
    return requests.get(url=get_url, headers=configure_headers(), stream=True)


def get_list_of_all_users(get_url):
    """
    GET request: get all users in list format
    :param get_url: url in string format
    :return: list with users
    """
    logger.debug(f"list with all users")
    response_get = get_all_users(get_url=get_url)
    return convert_json_string_in_dict(response_get.text)


def get_list_of_all_users_uid(get_url):
    """
    GET request: get all users uid in list format
    :param get_url: url in string format
    :return: list with uid
    """
    list_uid_users = []
    logger.debug(f"list with all existing users uid:")
    for user in get_list_of_all_users(get_url=get_url):
        list_uid_users.append(user['id'])
    logger.debug(f"{list_uid_users}")
    return list_uid_users


def create_user(post_url, data):
    """
    POST request: create user
    :param post_url: url in string format
    :param data: all information that need to create user
    :return: created user (response: status code and text)
    """
    global list_uid_created_user_for_one_test
    try:
        logger.debug(f"POST request: URL: {post_url}; data: {data}")
        response_post = requests.post(url=post_url, headers=configure_headers(), data=data, stream=True)
        decoded_data = convert_json_string_in_dict(json_data=data)
        logger.debug(f"{decoded_data}")
        if response_post.status_code == 201:
            for uid in get_list_of_all_users_uid(get_url=GET_ALL_USERS_LINK):
                if uid not in list_uid_created_user_for_one_test:
                    list_uid_created_user_for_one_test.append(str(uid))
                    logger.debug(f"user: {str(uid)} created successfully.")
        else:
            logger.error(f"error: can`t create user. Go to cleanup part. (!error!)")
            logger.error(f"response: {response_post.text}")
    except requests.exceptions.RequestException as e:
        logger.error(f"error occurred during create user and add to database. ")
    return response_post


def create_users(post_url, quantity):
    """
    POST request: help method for creating users
    :param post_url: url in string format
    :param quantity: value
    :return: nothing yet
    """
    logger.debug(f"create {quantity} users")
    for i in range(quantity):
        data = configure_payload_user_create(firstname=generate_random_string(5),
                                             lastname=generate_random_string(5),
                                             email=generate_random_string(10),
                                             completed=False,
                                             username=generate_random_string(5),
                                             password=generate_random_string_with_digits_and_symbols(10),
                                             summary=generate_random_string_with_digits(25))
        create_user(post_url=post_url,
                    data=data)


def update_user(put_url, data, uid):
    """
    PUT request: update user
    :param put_url: url in string format
    :param data:
    :param uid:
    :return: response with status code and data
    """
    put_url = put_url + "/" + str(uid)
    try:
        logger.debug(f"PUT request: URL: {put_url}; data: {data}")
        response_put = requests.put(url=put_url, headers=configure_headers(), data=data, stream=True)
        decoded_data = convert_json_string_in_dict(json_data=data)
        if response_put.status_code == 204:
            logger.debug(f"user: {decoded_data['firstName']} updated successfully.")
            list_uid_created_user_for_one_test.remove(str(uid))
            for uid in get_list_of_all_users_uid(get_url=GET_ALL_USERS_LINK):
                if uid not in list_uid_created_user_for_one_test:
                    list_uid_created_user_for_one_test.append(str(uid))
        else:
            logger.error(f"error: can`t update user.")
    except requests.exceptions.RequestException as e:
        logger.error(f"error occurred during updating user and adding data to database: {e}")
    return response_put


def delete_user(delete_url, uid):
    """
    DELETE request: delete user from system
    :param delete_url: url in string format
    :param uid: uuid
    :return: response with status code and text
    """
    delete_url = delete_url + "/" + str(uid)
    try:
        response_delete = requests.delete(url=delete_url,
                                          headers=configure_headers(),
                                          stream=True)
        if response_delete.status_code == 200:
            logger.debug(f"user: {str(uid)} deleted successfully.")
            list_uid_created_user_for_one_test.remove(str(uid))
        else:
            logger.error(f"error response: {response_delete}")
    except requests.exceptions.RequestException as e:
        logger.error(f"error occurred during delete user form database: {e}")
    return response_delete


def delete_all_users(get_url, delete_url):
    """
    help method for deletion all users
    :param get_url:
    :param delete_url:
    :return:
    """
    logger.debug(f"deletion all users existing in system")
    uid_all_users = get_list_of_all_users_uid(get_url=get_url)
    try:
        logger.debug(f"DELETE request: URL: {delete_url}")
        for uid in uid_all_users:
            delete_user(delete_url=delete_url,
                        uid=uid)
    except requests.exceptions.RequestException as e:
        logger.error(f"error occurred during delete all users: {e}")
