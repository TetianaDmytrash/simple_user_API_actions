"""
GET request | user
"""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import pytest
import jsonschema

from lib.helpMethod import *
from constants import *
from schema import schema_user, schema_error


class CommonFixture:
    """
    class for common fixture for all tests on get scenarios
    """
    _logger = logger

    @pytest.fixture()
    def configuration(self):
        """
        general fixture for get scenarios
        1. setup: create user
        2. cleanup: delete user
        :return: created user
        """
        try:
            self._logger.info(f"setup for test 'get all users': create one user.")
            yield create_users(post_url=POST_USER_LINK,
                               quantity=1)
        finally:
            self._logger.info(f"cleanup for test 'get all users': delete one user.")
            try:
                delete_all_users(delete_url=DELETE_USER_LINK,
                                 get_url=GET_ALL_USERS_LINK)
            except requests.exceptions.RequestException as e:
                self._logger.error(f"error occurred during deletion all users: {e}")


class TestGetAllUsersPositive(CommonFixture):
    """
    check all main moments when receive all created users
    """
    def test_positive_get_users_status_code(self, configuration):
        """"""
        self._logger.info(f" --- test: status code after receive all created users --- ")
        response_get = get_all_users(get_url=GET_ALL_USERS_LINK)
        self._logger.info(f"status code is {response_get.status_code}")
        self._logger.info(f"response: {response_get.text}")
        assert response_get.status_code == 200

    def test_positive_get_users_schema(self, configuration):
        """"""
        self._logger.info(f" --- test: validate schema after receive user --- ")
        response_get = get_list_of_all_users(get_url=GET_ALL_USERS_LINK)
        self._logger.info(f"users existing in system: ")
        self._logger.info(f"response: {response_get}")
        for data in response_get:
            try:
                jsonschema.validate(instance=data,
                                    schema=schema_user.schema_user)
                self._logger.info(f"schema is up to date")
            except requests.exceptions.RequestException as e:
                self._logger.error(f"data doesn`t match schema")


class TestGetAllUsersQuantityPositive:
    """"""
    _logger = logger

    @pytest.fixture()
    def configuration_users(self):
        """
        general fixture for get scenarios
        1. setup: create ftp servers
        2. cleanup: delete ftp servers
        :return: created ftp server
        """
        try:
            self._logger.info(f"setup for test 'get all users': create 10 users")
            yield create_users(post_url=POST_USER_LINK,
                               quantity=10)
        finally:
            self._logger.info(f"cleanup for test 'get all users': delete 10 users")
            delete_all_users(delete_url=DELETE_USER_LINK,
                             get_url=GET_ALL_USERS_LINK)

    def test_positive_get_all_users_quantity(self, configuration_users):
        """"""
        self._logger.info(f" --- test: match quantity after receive all users --- ")
        response_get = get_list_of_all_users(get_url=GET_ALL_USERS_LINK)
        # haven’t figured out how to convey the quantity
        assert len(response_get) == 10
        self._logger.info(f"get {len(response_get)} ftp serves, expected - 10")


class TestGetAllUsersNegative(CommonFixture):
    """
    check all main moments if something fail when get request
    """
    def test_negative_fail_attempt_to_get_all_user_status_code(self, configuration):
        """"""
        self._logger.info(f" --- test: status code after fail attempt to get all users --- ")
        response_get = get_all_users(get_url=GET_ALL_USERS_LINK_MISTAKE)
        self._logger.info(f"status code is {response_get.status_code}")
        assert response_get.status_code == 404

    def test_negative_fail_attempt_to_get_all_user_message(self, configuration):
        """"""
        self._logger.info(f" --- test: message after fail attempt to get all users --- ")
        response_get = get_all_users(get_url=GET_ALL_USERS_LINK_MISTAKE)
        decoded_response = convert_json_string_in_dict(response_get.text)
        self._logger.info(f"message is {decoded_response['status']} ")
        assert decoded_response['status'] == "Not Found"

    def test_negative_fail_attempt_to_get_all_user_schema(self, configuration):
        """"""
        self._logger.info(f" --- test: validate error schema --- ")
        response_get = get_all_users(get_url=GET_ALL_USERS_LINK_MISTAKE)
        self._logger.info(f"response: {convert_json_string_in_dict(response_get.text)}")
        try:
            jsonschema.validate(instance=convert_json_string_in_dict(response_get.text),
                                schema=schema_error.schema_error_without_message)
            self._logger.info(f"response is up to date with schema")
        except jsonschema.exceptions.ValidationError as e:
            self._logger.error(f"data does not match schema: {e}")
