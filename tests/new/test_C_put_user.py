"""
POST request | user
"""
import pytest
import jsonschema

from helpMethod import *
from constants import *
from schema import schema_error


class CommonFixture:
    """
    class for common fixtures for all test at put scenarios
    """
    _logger = logger

    @pytest.fixture()
    def configuration(self):
        """
        general fixture for put scenarios
        1. setup: create user
        2. cleanup: delete user
        :return: updated user
        """
        try:
            self._logger.info(f"setup for test 'put all users': update one user.")
            yield create_users(post_url=POST_USER_LINK,
                               quantity=1)
        finally:
            self._logger.info(f"cleanup for test 'put all users': delete one user.")
            delete_all_users(delete_url=DELETE_USER_LINK,
                             get_url=GET_ALL_USERS_LINK)


class TestUpdateUserPositive(CommonFixture):
    """
    check status code and message after success update user
    """

    @pytest.mark.parametrize("firstName", [
        generate_random_string(5)
    ])
    def test_positive_update_user_status_code(self, firstName, configuration):
        """"""
        self._logger.info(f" --- test: status code after update user --- ")
        data = configure_payload_user_update(firstname=firstName)
        user_uid = get_list_of_all_users_uid(get_url=GET_ALL_USERS_LINK)
        for uid in user_uid:
            response_put = update_user(put_url=PUT_USER_LINK,
                                       data=data,
                                       uid=uid)
            self._logger.info(f"status code is {response_put.status_code}")
            assert response_put.status_code == 204

    @pytest.mark.parametrize("firstName", [
        generate_random_string(5)
    ])
    def test_positive_update_user_message(self, firstName, configuration):
        """"""
        self._logger.info(f" --- test: message after update user --- ")
        data = configure_payload_user_update(firstname=firstName)
        user_uid = get_list_of_all_users_uid(get_url=GET_ALL_USERS_LINK)
        for uid in user_uid:
            response_put = update_user(put_url=PUT_USER_LINK,
                                       data=data,
                                       uid=uid)
            self._logger.info(f"response!!!!!!!!!: {response_put.text}")
            # assert decoded_response_text['message'] == f"User: {decoded_data['username']} successfully updated."


class TestUpdateUserDataMatch(CommonFixture):
    @pytest.mark.parametrize("firstName", [
        generate_random_string(5)
    ])
    def test_positive_update_user_data_match(self, firstName, configuration):
        """"""
        self._logger.info(f" --- test: data match after update user --- ")
        data = configure_payload_user_update(firstname=firstName)
        users_uid = get_list_of_all_users_uid(get_url=GET_ALL_USERS_LINK)
        for user_uid in users_uid:
            response_put = update_user(put_url=PUT_USER_LINK,
                                       data=data,
                                       uid=user_uid)
            self._logger.info(f"status code is {response_put.status_code}")
            assert response_put.status_code == 204
        decoded_data = convert_json_string_in_dict(json_data=data)
        response_get = get_list_of_all_users(get_url=GET_ALL_USERS_LINK)
        for user in response_get:
            assert decoded_data["firstName"] == user["firstName"]
            assert decoded_data["lastName"] == user["lastName"]


class TestUpdateUserFieldPositive(CommonFixture):
    """
    check status code and message after update user (work with every field)
    """

    @pytest.mark.parametrize("firstname", [
        (generate_random_string(2)),
        (generate_random_string(5)),
        (generate_random_string(10)),
        (generate_random_string_with_hyphen(6)),
    ])
    def test_positive_user_firstname(self, firstname, configuration):
        self._logger.info(f" --- test: update user with firstname: {firstname} --- ")
        data = configure_payload_user_update(firstname=firstname)
        user_uid = get_list_of_all_users_uid(get_url=GET_ALL_USERS_LINK)
        for uid in user_uid:
            response_put = update_user(put_url=PUT_USER_LINK,
                                       data=data,
                                       uid=uid)
            self._logger.info(f"status code is {response_put.status_code}")
            assert response_put.status_code == 204

    @pytest.mark.parametrize("lastname", [
        (generate_random_string(2)),
        (generate_random_string(5)),
        (generate_random_string(10)),
        (generate_random_string_with_hyphen(6)),
    ])
    def test_positive_user_lastname(self, lastname, configuration):
        self._logger.info(f" --- test: update user with lastname: {lastname} --- ")
        data = configure_payload_user_update(lastname=lastname)
        user_uid = get_list_of_all_users_uid(get_url=GET_ALL_USERS_LINK)
        for uid in user_uid:
            response_put = update_user(put_url=PUT_USER_LINK,
                                       data=data,
                                       uid=uid)
            self._logger.info(f"status code is {response_put.status_code}")
            assert response_put.status_code == 204


class TestUpdateUserNegative(CommonFixture):
    """
    check status code and message after fail attempt to update user
    """

    @pytest.mark.parametrize("firstName", [
        ""
    ])
    def test_negative_after_fail_attempt_to_update_user_status_code(self, firstName, configuration):
        self._logger.info(f" --- test: status code after fail attempt to update user with empty firstName --- ")
        data = configure_payload_user_update(firstname=firstName)
        user_uid = get_list_of_all_users_uid(get_url=GET_ALL_USERS_LINK)
        for uid in user_uid:
            response_put = update_user(put_url=PUT_USER_LINK,
                                       data=data,
                                       uid=uid)
            self._logger.info(f"status code is {response_put.status_code}")
            assert response_put.status_code == 400

    @pytest.mark.parametrize("firstName", [
        ""
    ])
    def test_negative_after_fail_attempt_to_update_user_message(self, firstName, configuration):
        self._logger.info(f" --- test: message after fail attempt to update user with empty firstName --- ")
        data = configure_payload_user_update(firstname=firstName)
        user_uid = get_list_of_all_users_uid(get_url=GET_ALL_USERS_LINK)
        for uid in user_uid:
            response_put = update_user(put_url=PUT_USER_LINK,
                                       data=data,
                                       uid=uid)

            decoded_response_text = convert_json_string_in_dict(json_data=response_put.text)
            self._logger.info(f"response: {response_put.text}")
            assert decoded_response_text['message'] == f"FirstName include invalid length."


class TestUpdateUserNegativeInvalidURL(CommonFixture):
    """
    check all main moments if something fail when put request
    """

    @pytest.mark.parametrize("firstname", [
        generate_random_string(4)
    ])
    def test_negative_after_fail_attempt_put_request_status_code(self, firstname, configuration):
        """"""
        self._logger.info(f" --- test: status code after attempt to update user with invalid URL --- ")
        data = configure_payload_user_update(firstname=firstname)
        user_uid = get_list_of_all_users_uid(get_url=GET_ALL_USERS_LINK)
        for uid in user_uid:
            response_put = update_user(put_url=PUT_USER_LINK_MISTAKE,
                                       data=data,
                                       uid=uid)
            self._logger.info(f"status code is {response_put.status_code}")
            assert response_put.status_code == 404

    @pytest.mark.parametrize("firstname", [
        generate_random_string(4)
    ])
    def test_negative_fail_attempt_put_request_schema(self, firstname, configuration):
        """"""
        self._logger.info(f" --- test: schema after fail attempt to update user with invalid URL --- ")
        data = configure_payload_user_update(firstname=firstname)
        user_uid = get_list_of_all_users_uid(get_url=GET_ALL_USERS_LINK)
        for uid in user_uid:
            response_put = update_user(put_url=PUT_USER_LINK_MISTAKE,
                                       data=data,
                                       uid=uid)
            self._logger.info(f"response: {response_put.text}")
        try:
            jsonschema.validate(instance=convert_json_string_in_dict(response_put.text),
                                schema=schema_error.schema_error_without_message)
            self._logger.info(f"response is up to date with schema")
        except jsonschema.exceptions.ValidationError as e:
            self._logger.error(f"data does not match schema: {e}")


class TestUpdateUserFieldNegative(CommonFixture):
    """
    check status code and message after fail attempt to update user with invalid values
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
    def test_negative_user_firstname(self, firstname, configuration):
        """"""
        self._logger.info(f" --- test: fail attempt to update user with firstname: {firstname} --- ")
        data = configure_payload_user_update(firstname=firstname)
        user_uid = get_list_of_all_users_uid(get_url=GET_ALL_USERS_LINK)
        for current_uid in user_uid:
            response = update_user(put_url=PUT_USER_LINK,
                                   data=data,
                                   uid=current_uid)
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
    def test_negative_user_lastname(self, lastname, configuration):
        self._logger.info(f" --- test: fail updating user with lastname: {lastname} --- ")
        data = configure_payload_user_update(lastname=lastname)
        user_uid = get_list_of_all_users_uid(get_url=GET_ALL_USERS_LINK)
        for current_user in user_uid:
            response = update_user(put_url=PUT_USER_LINK,
                                   data=data,
                                   uid=current_user)
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
