"""
POST request | user
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
    class for common fixtures for all test at post scenarios
    """
    _logger = logger

    @pytest.fixture()
    def full_configuration(self, request):
        """
        full fixture for post scenarios
        1. setup:
        2. cleanup: delete user
        :param request:
        :return: configured headers ???
        """
        try:
            self._logger.info(f"setup for test 'create user': configure payload")
            firstname, lastname, email, completed, username, password, summary = request.param
            yield configure_payload_user_create(firstname=firstname,
                                                lastname=lastname,
                                                email=email,
                                                completed=completed,
                                                username=username,
                                                password=password,
                                                summary=summary)
        finally:
            self._logger.info(f"cleanup for test 'create user': delete user")
            delete_all_users(delete_url=DELETE_USER_LINK,
                             get_url=GET_ALL_USERS_LINK)

    @pytest.fixture()
    def simple_configuration(self):
        """
        simple fixture for post scenarios
        1. setup:
        2. cleanup: delete user
        :return:
        """
        try:
            self._logger.info(f"setup for test 'create user': start session.")
            yield configure_headers()
        finally:
            self._logger.info(f"cleanup for test 'create user': delete one user.")
            delete_all_users(delete_url=DELETE_USER_LINK,
                             get_url=GET_ALL_USERS_LINK)


class TestCreateUserPositive(CommonFixture):
    """
    check status code and message after success create user
    """

    @pytest.mark.parametrize("full_configuration", [
        (generate_random_string(5),
         generate_random_string(5),
         generate_random_string(10),
         False,
         generate_random_string(5),
         generate_random_string_with_digits_and_symbols(10),
         generate_random_string_with_digits(25))
    ], indirect=True)
    def test_positive_create_user_status_code(self, full_configuration):
        """"""
        self._logger.info(f" --- test: status code after create user --- ")
        data = full_configuration
        response = create_user(post_url=POST_USER_LINK,
                               data=data)
        self._logger.info(f"status code is {response.status_code}")
        assert response.status_code == 201

    @pytest.mark.parametrize("full_configuration", [
        (generate_random_string(5),
         generate_random_string(5),
         generate_random_string(10),
         False,
         generate_random_string(5),
         generate_random_string_with_digits_and_symbols(10),
         generate_random_string_with_digits(25))
    ], indirect=True)
    def test_positive_create_user_message(self, full_configuration):
        """"""
        self._logger.info(f" --- test: message after create user --- ")
        data = full_configuration
        response = create_user(post_url=POST_USER_LINK,
                               data=data)
        decoded_response_text = convert_json_string_in_dict(json_data=response.text)
        assert decoded_response_text['message'] == f"success create user"


class TestCreateUserDataMatch(CommonFixture):
    @pytest.mark.parametrize("full_configuration", [
        (generate_random_string(5),
         generate_random_string(5),
         generate_random_string(10),
         False,
         generate_random_string(5),
         generate_random_string_with_digits_and_symbols(10),
         generate_random_string_with_digits(25))
    ], indirect=True)
    def test_positive_create_user_data_match(self, full_configuration):
        """"""
        self._logger.info(f" --- test: data match after create user --- ")
        data = full_configuration
        response_post = create_user(post_url=POST_USER_LINK,
                                    data=data)
        assert response_post.status_code == 201
        decoded_data = convert_json_string_in_dict(json_data=data)
        response_get = get_list_of_all_users(get_url=GET_ALL_USERS_LINK)
        for user in response_get:
            assert decoded_data["firstName"] == user["firstName"]
            assert decoded_data["lastName"] == user["lastName"]
            assert decoded_data["username"] == user["username"]
            assert decoded_data["completed"] == user["completed"]
            assert decoded_data["password"] == user["password"]
            assert decoded_data["summary"] == user["summary"]


class TestCreateUserFieldPositive(CommonFixture):
    """
    check status code and message after create user (work with every field)
    """

    @pytest.mark.parametrize("firstname", [
        (generate_random_string(2)),
        (generate_random_string(5)),
        (generate_random_string(10)),
        (generate_random_string_with_hyphen(6)),
    ])
    def test_positive_user_firstname(self, firstname, simple_configuration):
        self._logger.info(f" --- test: create user with firstname: {firstname} --- ")
        data = configure_payload_user_create(firstname=firstname)
        response = create_user(post_url=POST_USER_LINK,
                               data=data)
        self._logger.info(f"status code is {response.status_code}")
        assert response.status_code == 201

    @pytest.mark.parametrize("lastname", [
        (generate_random_string(2)),
        (generate_random_string(5)),
        (generate_random_string(10)),
        (generate_random_string_with_hyphen(6)),
    ])
    def test_positive_user_lastname(self, lastname, simple_configuration):
        self._logger.info(f" --- test: create user with lastname: {lastname} --- ")
        data = configure_payload_user_create(lastname=lastname)
        response = create_user(post_url=POST_USER_LINK,
                               data=data)
        self._logger.info(f"status code is {response.status_code}")
        assert response.status_code == 201

    @pytest.mark.parametrize("username", [
        (generate_random_string(2)),
        (generate_random_string(5)),
        (generate_random_string(10)),
        (generate_random_string_with_hyphen(6)),
    ])
    def test_positive_user_username(self, username, simple_configuration):
        self._logger.info(f" --- test: create user with username: {username} --- ")
        data = configure_payload_user_create(username=username)
        response = create_user(post_url=POST_USER_LINK,
                               data=data)
        self._logger.info(f"status code is {response.status_code}")
        assert response.status_code == 201


class TestCreateUserNegative(CommonFixture):
    """
    check status code and message after fail attempt to create user
    """

    @pytest.mark.parametrize("full_configuration", [
        ("",
         generate_random_string(5),
         generate_random_string(10),
         False,
         generate_random_string(5),
         generate_random_string_with_digits_and_symbols(10),
         generate_random_string_with_digits(25))
    ], indirect=True)
    def test_negative_after_fail_attempt_to_create_user_status_code(self, full_configuration):
        self._logger.info(f" --- test: status code after fail attempt to create user with empty username --- ")
        data = full_configuration
        response = create_user(post_url=POST_USER_LINK,
                               data=data)
        self._logger.info(f"status code is {response.status_code}")
        assert response.status_code == 400

    @pytest.mark.parametrize("full_configuration", [
        ("",
         generate_random_string(5),
         generate_random_string(10),
         False,
         generate_random_string(5),
         generate_random_string_with_digits_and_symbols(10),
         generate_random_string_with_digits(25))
    ], indirect=True)
    def test_negative_after_fail_attempt_to_create_user_message(self, full_configuration):
        self._logger.info(f" --- test: message after fail attempt to create user with empty firstName --- ")
        data = full_configuration
        response = create_user(post_url=POST_USER_LINK,
                               data=data)
        decoded_response_text = convert_json_string_in_dict(json_data=response.text)
        self._logger.info(f" --- {decoded_response_text['message']}")
        assert decoded_response_text['message'] == f"FirstName include invalid length."


class TestCreateUserNegativeInvalidURL(CommonFixture):
    """
    check all main moments if something fail when post request
    """

    @pytest.mark.parametrize("full_configuration", [
        (generate_random_string(4),
         generate_random_string(5),
         generate_random_string(10),
         False,
         generate_random_string(5),
         generate_random_string_with_digits_and_symbols(10),
         generate_random_string_with_digits(25))
    ], indirect=True)
    def test_negative_after_fail_attempt_post_request_status_code(self, full_configuration):
        """"""
        self._logger.info(f" --- test: status code after attempt to create user with invalid URL --- ")
        data = full_configuration
        response = create_user(post_url=POST_USER_LINK_MISTAKE,
                               data=data)
        self._logger.info(f"status code is {response.status_code}")
        assert response.status_code == 404

    @pytest.mark.parametrize("full_configuration", [
        (generate_random_string(4),
         generate_random_string(5),
         generate_random_string(10),
         False,
         generate_random_string(5),
         generate_random_string_with_digits_and_symbols(10),
         generate_random_string_with_digits(25))
    ], indirect=True)
    def test_negative_fail_attempt_post_request_schema(self, full_configuration):
        """"""
        self._logger.info(f" --- test: schema after fail attempt to create user with invalid URL --- ")
        data = full_configuration
        response = create_user(post_url=POST_USER_LINK_MISTAKE,
                               data=data)
        self._logger.info(f"response: {response.text}")
        try:
            jsonschema.validate(instance=convert_json_string_in_dict(response.text),
                                schema=schema_error.schema_error_without_message)
            self._logger.info(f"response is up to date with schema")
        except jsonschema.exceptions.ValidationError as e:
            self._logger.error(f"data does not match schema: {e}")


class TestCreateUserFieldNegative(CommonFixture):
    """
    check status code and message after fail attempt to create user with invalid values
    """

    @pytest.mark.parametrize("firstname", [
        generate_random_string(11),
        generate_random_string_with_digits(5),
        generate_random_string_with_symbol(6),
        generate_random_integer(),
        generate_random_bool(),
        "\x00",
        None,
        "",
        "\n"
    ])
    def test_negative_user_firstname(self, firstname, simple_configuration):
        """"""
        self._logger.info(f" --- test: fail attempt to create user with firstname: {firstname} --- ")
        data = configure_payload_user_create(firstname=firstname)
        response = create_user(post_url=POST_USER_LINK,
                               data=data)
        try:
            assert response.status_code == 400, f"Status code not valid - {response.status_code}. Expected 400."
        except AssertionError:
            try:
                assert response.status_code == 500, f"Status code not valid - {response.status_code}. Expected 500."
            except AssertionError:
                try:
                    assert response.status_code == 422, f"Status code not valid - {response.status_code}. Expected 422."
                except AssertionError:
                    raise AssertionError(
                        f"Unexpected status code - {response.status_code}. Expected one of: 400, 500, 422.")

    @pytest.mark.parametrize("lastname", [
        generate_random_string(11),
        generate_random_string_with_digits(5),
        generate_random_string_with_symbol(6),
        generate_random_integer(),
        generate_random_bool(),
        "\x00",
        None,
        "",
        "\n"
    ])
    def test_negative_user_lastname(self, lastname, simple_configuration):
        self._logger.info(f" --- test: fail creating user with lastname: {lastname} --- ")
        data = configure_payload_user_create(lastname=lastname)
        response = create_user(post_url=POST_USER_LINK,
                               data=data)
        try:
            assert response.status_code == 400, f"Status code not valid - {response.status_code}. Expected 400."
        except AssertionError:
            try:
                assert response.status_code == 500, f"Status code not valid - {response.status_code}. Expected 500."
            except AssertionError:
                try:
                    assert response.status_code == 422, f"Status code not valid - {response.status_code}. Expected 422."
                except AssertionError:
                    raise AssertionError(
                        f"Unexpected status code - {response.status_code}. Expected one of: 400, 500, 422.")

    @pytest.mark.parametrize("username", [
        generate_random_string(11),
        generate_random_string_with_digits(5),
        generate_random_string_with_symbol(6),
        generate_random_integer(),
        generate_random_bool(),
        "\x00",
        None,
        "",
        "\n"
    ])
    def test_negative_user_username(self, username, simple_configuration):
        self._logger.info(f" --- test: fail creating user with username: {username} --- ")
        data = configure_payload_user_create(username=username)
        response = create_user(post_url=POST_USER_LINK,
                               data=data)
        try:
            assert response.status_code == 400, f"Status code not valid - {response.status_code}. Expected 400."
        except AssertionError:
            try:
                assert response.status_code == 500, f"Status code not valid - {response.status_code}. Expected 500."
            except AssertionError:
                try:
                    assert response.status_code == 422, f"Status code not valid - {response.status_code}. Expected 422."
                except AssertionError:
                    raise AssertionError(
                        f"Unexpected status code - {response.status_code}. Expected one of: 400, 500, 422.")
