"""
DELETE request | user
"""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import pytest
import jsonschema

from helpMethod import *
from constants import *
from schema import schema_error


class CommonFixture:
    """
    class for common fixture for all tests on delete scenarios
    """
    _logger = logger
    quantity = 2

    @pytest.fixture()
    def configuration(self):
        """
        general fixture for deletion section:
        1. setup: create user
        2. cleanup: delete user (if in tests it didn`t do)
        :return: created user
        """
        try:
            self._logger.info(f"setup for test 'delete user': create {self.quantity} user.")
            yield create_users(post_url=POST_USER_LINK,
                               quantity=self.quantity)
        finally:
            self._logger.info(f" ????? cleanup for test 'delete user': delete {self.quantity} user.")
            try:
                delete_all_users(delete_url=DELETE_USER_LINK,
                                 get_url=GET_ALL_USERS_LINK)
            except requests.exceptions.RequestException as e:
                self._logger.error(f"error occurred during deletion all users: {e}")


class TestDeleteUserPositive(CommonFixture):
    """
    check status code and message if success delete user
    """

    def test_positive_delete_users_uid_status_code(self, configuration):
        """"""
        self._logger.info(f" --- test: status code after delete user --- ")
        users_uid = get_list_of_all_users_uid(get_url=GET_ALL_USERS_LINK)
        self._logger.info(f"get user uid before delete: {users_uid}")
        for uid in users_uid:
            response_delete = delete_user(delete_url=DELETE_USER_LINK,
                                          uid=uid)
            self._logger.info(f"status code is {response_delete.status_code}")
            assert response_delete.status_code == 204

    # def test_positive_delete_users_uid_message(self, configuration):
    #     """"""
    #     self._logger.info(f" --- test: message after delete user --- ")
    #     users_uid = get_list_of_all_users_uid(get_url=GET_ALL_USERS_LINK)
    #     self._logger.info(f"get user uid before delete: {users_uid}")
    #     for uid in users_uid:
    #         response_delete = delete_user(delete_url=DELETE_USER_LINK,
    #                                       uid=uid)
    #         decoded_response_text = convert_json_string_in_dict(json_data=response_delete.text)
    #         self._logger.info(f"message is '{decoded_response_text['message']}'")
    #         assert decoded_response_text['message'] == f"User: {str(uid)} successfully deleted."


class TestFinalDeleteUserPositive(CommonFixture):
    """
    test that user definitely deleted from the system
    """

    def test_positive_deleting_users_uid(self, configuration):
        """"""
        self._logger.info(f" --- test: confirm that user deleted from system --- ")
        response_get_start = get_list_of_all_users_uid(get_url=GET_ALL_USERS_LINK)
        self._logger.info(f"get user uid before delete: {response_get_start}")
        for uid in response_get_start:
            response_delete = delete_user(delete_url=DELETE_USER_LINK,
                                          uid=uid)
            assert response_delete.status_code == 204
        response_get_end = get_list_of_all_users_uid(get_url=GET_ALL_USERS_LINK)
        self._logger.info(f"get user name after delete: {response_get_end}")
        for user_start in response_get_start:
            assert user_start not in response_get_end, f"user {user_start} didn`t delete from system"


class TestDeleteUserNegative(CommonFixture):
    """
    delete request with error
    """
    def test_negative_fail_attempt_to_delete_users_uid_status_code(self, configuration):
        self._logger.info(f" --- test: attempt to delete user with invalid URL (check status code) --- ")
        response_get = get_list_of_all_users_uid(get_url=GET_ALL_USERS_LINK)
        for uid in response_get:
            response_delete = delete_user(delete_url=DELETE_USER_LINK_MISTAKE,
                                          uid=uid)
            self._logger.info(f" status code is {response_delete.status_code}")
            assert response_delete.status_code == 404

    def test_negative_fail_attempt_to_delete_users_uid_message(self, configuration):
        self._logger.info(f" --- test: attempt to delete user with invalid URL (check message) --- ")
        response_get = get_list_of_all_users_uid(get_url=GET_ALL_USERS_LINK)
        for uid in response_get:
            response_delete = delete_user(delete_url=DELETE_USER_LINK_MISTAKE,
                                          uid=uid)
            decoded_response_text = convert_json_string_in_dict(json_data=response_delete.text)
            self._logger.info(f"response '{decoded_response_text}' ")
            assert decoded_response_text["status"] == f"Not Found"

    def test_negative_fail_attempt_to_delete_users_uid_schema(self, configuration):
        self._logger.info(f" --- test: attempt to delete user with invalid URL (check error schema) --- ")
        response_get = get_list_of_all_users_uid(get_url=GET_ALL_USERS_LINK)
        for uid in response_get:
            response_delete = delete_user(delete_url=DELETE_USER_LINK_MISTAKE,
                                          uid=uid)
            try:
                jsonschema.validate(instance=response_delete.text, schema=schema_error.schema_error_without_message)
                self._logger.info(f"response is up to date with schema")
            except jsonschema.exceptions.ValidationError as e:
                self._logger.error(f"data does not match schema: {e}")



